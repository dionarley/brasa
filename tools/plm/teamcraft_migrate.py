#!/usr/bin/env python3
"""Migra o PS-001 do fluxo caseiro para uma instância do TeamCraft.

Cria (ou atualiza, se reexecutado) no TeamCraft:

* o grupo de projeto ``PS-001`` e seus membros;
* o item de conjunto ``PS-001`` com o modelo ``.sc``, STEP, 3MF e renders;
* os documentos controlados ``PS-001-DR-001``, ``-US-001``, ``-CO-001``,
  ``-PL-001``, ``-PL-002`` e ``-LM-001`` com os PDFs/CSV publicados;
* os 16 itens da lista de materiais (``PS-001-LM-01`` … ``-16``);
* a BOM do conjunto e as referências de documento;
* uma ordem de mudança (ECO) que leva todas as revisões A de *em trabalho*
  para *liberado*, com aprovação de quatro olhos pelo usuário revisor.

O script é idempotente: itens, arquivos (por sha256), linhas de BOM,
referências, revisões da ECO e aprovações já existentes são detectados e
não repetidos. Revisões já liberadas não são alteradas.

Uso (variáveis de ambiente):

    TEAMCRAFT_SERVER=http://127.0.0.1:8080 \
    TEAMCRAFT_ADMIN_TOKEN=tc_pat_… \
    TEAMCRAFT_REVIEWER_TOKEN=tc_pat_… \
    python3 tools/plm/teamcraft_migrate.py

Sem ``TEAMCRAFT_REVIEWER_TOKEN`` a ECO é submetida mas não aprovada
(``--no-approve`` faz o mesmo de propósito).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist" / "v0.17.1"
CAD = ROOT / "cad" / "solidcraft"
DRAW = ROOT / "out" / "draw" / "v017"
BOM_CSV = ROOT / "docs" / "construcao" / "BOM.csv"

PROJECT = {
    "code": "PS-001",
    "name": "Pistola de solda 550 W / 127 V",
    "description": (
        "Estudo aberto de pistola de solda por transformador (The Black Tools). "
        "Não certificado; 127 V. Modelo aprovado v0.15.0, prancha A2 rev. A."
    ),
}
MEMBERS = [
    ("dionarley", True),
    ("revisor", False),
]
ASSEMBLY = "PS-001"
DOCS = {
    "PS-001-DR-001": {
        "name": "Prancha 2D A2 — conjunto geral",
        "description": (
            "Vistas ortográficas em 1º diedro, escala 1:2, detalhe A 1:1, "
            "lista de materiais e notas. Rev. A publicada em v0.17.0."
        ),
        "files": [
            (DRAW / "PS-001-DR-001_rA_prancha-a2.pdf", "drawing"),
            (DRAW / "PS-001-DR-001_rA_prancha-a2.dxf", "drawing"),
        ],
        "kind": "drawing",
    },
    "PS-001-US-001": {
        "name": "Manual de uso e segurança",
        "description": "Operação, limites de uso, segurança em 127 V e manutenção. Rev. A.",
        "files": [(DIST / "PS-001-US-001_rA_uso.pdf", "docs")],
        "kind": "specification",
    },
    "PS-001-CO-001": {
        "name": "Guia de construção (estudo)",
        "description": "Sequência de montagem do transformador, secundário e cabo. Rev. B.",
        "files": [(DIST / "PS-001-CO-001_rB_construcao.pdf", "docs")],
        "kind": "specification",
    },
    "PS-001-PL-001": {
        "name": "Plano de ciclo de vida (PLM)",
        "description": "Numeração, revisões, estados e liberação usados no projeto. Rev. A.",
        "files": [(DIST / "PS-001-PL-001_rA_plano-plm.pdf", "docs")],
        "kind": "specification",
    },
    "PS-001-PL-002": {
        "name": "Registro mestre de documentos",
        "description": "Índice controlado de documentos, revisões e artefatos. Rev. A.",
        "files": [(DIST / "PS-001-PL-002_rA_registro-documentos.pdf", "docs")],
        "kind": "specification",
    },
    "PS-001-LM-001": {
        "name": "Lista de materiais (BOM)",
        "description": (
            "Lista controlada com 16 linhas; no TeamCraft a estrutura também é "
            "mantida como BOM do conjunto PS-001. Rev. A."
        ),
        "files": [(DIST / "PS-001-LM-001_rA_bom.csv", "docs")],
        "kind": "specification",
    },
}
ASSEMBLY_FILES = [
    (CAD / "PS-001.sc", "cad"),
    (CAD / "PS-001.step", "cad"),
    (CAD / "PS-001.3mf", "cad"),
] + [(DIST / "renders" / f"PS-001_{view}_rA.png", "renders")
     for view in ("frontal", "iso", "perfil", "topo", "trafo")]

# Código da BOM → classificação no TeamCraft (make, purchased, standard).
CLASSIFICATION = {
    "PS-001-LM-01": "purchased",
    "PS-001-LM-02": "make",
    "PS-001-LM-03": "purchased",
    "PS-001-LM-04": "purchased",
    "PS-001-LM-05": "make",
    "PS-001-LM-06": "make",
    "PS-001-LM-07": "standard",
    "PS-001-LM-08": "standard",
    "PS-001-LM-09": "standard",
    "PS-001-LM-10": "make",
    "PS-001-LM-11": "purchased",
    "PS-001-LM-12": "make",
    "PS-001-LM-13": "purchased",
    "PS-001-LM-14": "purchased",
    "PS-001-LM-15": "purchased",
    "PS-001-LM-16": "purchased",
}

CHANGE_TITLE = "PS-001 — liberação inicial rev. A"


class Api:
    def __init__(self, server: str, token: str):
        self.base = server.rstrip("/") + "/api/v1"
        self.token = token

    def call(self, method: str, path: str, body=None, raw: bytes | None = None,
             content_type: str | None = None, ok=(200, 201, 204)):
        url = self.base + path
        data = raw
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode()
            content_type = "application/json"
        if content_type:
            headers["Content-Type"] = content_type
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                payload = resp.read()
                status = resp.status
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            try:
                msg = json.loads(detail)["error"]["message"]
            except Exception:
                msg = detail[:400]
            if e.code in ok:
                return e.code, None
            raise RuntimeError(f"{method} {path}: HTTP {e.code} — {msg}") from None
        if status in (204,) or not payload:
            return status, None
        return status, json.loads(payload)

    def url(self, path: str) -> str:
        return self.base + path

    def download(self, path: str) -> bytes:
        req = urllib.request.Request(self.url(path),
                                     headers={"Authorization": f"Bearer {self.token}"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def multipart(files, fields=None):
    boundary = "----ps001" + hashlib.sha256(os.urandom(16)).hexdigest()[:24]
    out = bytearray()
    for key, value in (fields or {}).items():
        out += f"--{boundary}\r\n".encode()
        out += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
        out += str(value).encode() + b"\r\n"
    for path, _folder in files:
        name = path.name
        ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
        out += f"--{boundary}\r\n".encode()
        out += (f'Content-Disposition: form-data; name="file"; filename="{name}"\r\n'
                f"Content-Type: {ctype}\r\n\r\n").encode()
        out += path.read_bytes() + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def check_inputs():
    missing = [p for p in [BOM_CSV, *[p for p, _ in ASSEMBLY_FILES],
                           *[p for d in DOCS.values() for p, _ in d["files"]]]
               if not p.is_file()]
    if missing:
        sys.exit("Arquivos ausentes:\n  " + "\n  ".join(str(p) for p in missing))


def read_bom():
    """Lê ``docs/construcao/BOM.csv``.

    O arquivo é um CSV sem aspas com vírgulas decimais em dimensões e notas
    (ex.: "janela 12,5 × 50"), então o leitor padrão desalinha as colunas.
    As seis primeiras colunas não têm vírgula; o restante é separado pelo
    volume, o único decimal com ponto (ou o último travessão da linha).
    """
    rows = []
    lines = BOM_CSV.read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split(",", 6)
        if len(parts) < 7:
            continue
        _, code, desc, qty_raw, body, material, rest = parts
        code = code.strip()
        if not code:
            continue
        tokens = rest.split(",")
        vol = next((i for i, t in enumerate(tokens)
                    if re.fullmatch(r"\d+\.\d+", t.strip())), None)
        if vol is None:
            vol = max((i for i, t in enumerate(tokens) if t.strip() == "—"),
                      default=len(tokens) - 1)
        dims = ",".join(tokens[:vol]).strip()
        volume = tokens[vol].strip() if vol < len(tokens) else ""
        note = ",".join(tokens[vol + 1:]).strip().strip(",")
        # a linha 5 traz um "1" solto antes do volume (ver BOM.csv)
        if code == "PS-001-LM-05" and dims.endswith(",1"):
            dims = dims[:-2]
        try:
            qty = float(qty_raw)
        except ValueError:
            qty = 1.0
        rows.append({
            "number": code,
            "name": desc.strip(),
            "quantity": qty,
            "material": material.strip(),
            "dimensions": dims,
            "volume": volume,
            "note": note,
            "body": body.strip(),
            "qty_raw": qty_raw.strip(),
        })
    if len(rows) != 16:
        print(f"aviso: BOM.csv tem {len(rows)} linhas, esperado 16")
    return rows


def ensure_project(api: Api):
    _, projects = api.call("GET", "/projects")
    codes = {p["code"] for p in projects}
    if PROJECT["code"] not in codes:
        api.call("POST", "/projects", PROJECT)
        print(f"grupo {PROJECT['code']} criado")
    else:
        print(f"grupo {PROJECT['code']} já existe")
    _, members = api.call("GET", f"/projects/{PROJECT['code']}/members")
    have = {m["username"] for m in members}
    for username, manager in MEMBERS:
        if username not in have:
            api.call("POST", f"/projects/{PROJECT['code']}/members",
                     {"username": username, "manager": manager})
            print(f"  membro {username} adicionado")


def get_item(api: Api, number: str):
    try:
        _, data = api.call("GET", f"/items/{urllib.parse.quote(number)}")
        return data
    except RuntimeError as e:
        if "HTTP 404" in str(e):
            return None
        raise


def revision(data, code="A"):
    for rev in data.get("revisions", []):
        if rev["code"] == code:
            return rev
    return None


def ensure_checkout(api: Api, number: str, rev):
    """Garante que a revisão em trabalho está sob nosso check-out."""
    if rev["state"] != "in_work":
        return False
    _, me = api.call("GET", "/me")
    if rev.get("checked_out_by") == me["id"]:
        return True
    if rev.get("checked_out_by"):
        raise RuntimeError(
            f"{number} rev {rev['code']} está em check-out de "
            f"{rev.get('checked_out_by_name')}; libere antes de migrar")
    api.call("POST", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/checkout")
    print(f"  check-out de {number} rev {rev['code']}")
    return True


def ensure_metadata(api: Api, number: str, rev: dict, name: str, description: str,
                    material: str = "", classification: str | None = None):
    """Mantém nome/descrição/material da revisão em trabalho iguais à fonte."""
    if rev["state"] != "in_work":
        return
    changed = (rev.get("name") != name
               or rev.get("description", "") != description
               or rev.get("material", "") != material)
    if changed:
        ensure_checkout(api, number, rev)
        api.call("PATCH", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}",
                 {"name": name, "description": description, "material": material})
        print(f"  metadados de {number} atualizados")
    if classification:
        data = get_item(api, number)
        if data["item"].get("classification") != classification:
            api.call("PATCH", f"/items/{urllib.parse.quote(number)}",
                     {"classification": classification})


def ensure_item(api: Api, number: str, item_type: str, name: str, description: str,
                material: str = "", classification: str | None = None) -> dict:
    data = get_item(api, number)
    if data is None:
        body = {
            "item_type": item_type,
            "name": name,
            "number": number,
            "project": PROJECT["code"],
            "description": description,
            "idempotency_key": f"ps001-{number}",
        }
        if material:
            body["material"] = material
        if classification:
            body["classification"] = classification
        _, data = api.call("POST", "/items", body)
        data = {"item": data, "revisions": [data]}
        print(f"item {number} criado ({item_type})")
    else:
        print(f"item {number} já existe")
    rev = revision(data)
    if rev:
        ensure_metadata(api, number, rev, name, description, material, classification)
        data = get_item(api, number)
    return data


def ensure_files(api: Api, number: str, rev: dict, files, comment: str):
    if rev["state"] != "in_work":
        print(f"  {number} rev {rev['code']} está {rev['state']}: arquivos não alterados")
        return
    _, current = api.call(
        "GET", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/files")
    by_name = {f["filename"]: f for f in current}
    todo = []
    for path, folder in files:
        digest = sha256_file(path)
        have = by_name.get(path.name)
        if have and have["sha256"] == digest:
            continue
        todo.append((path, folder))
    if not todo:
        print(f"  {number}: {len(files)} arquivos já presentes")
        return
    ensure_checkout(api, number, rev)
    folders = {path.name: folder for path, folder in todo}
    body, ctype = multipart(todo, {"comment": comment, "folders": json.dumps(folders)})
    api.call("POST", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/files",
             raw=body, content_type=ctype)
    print(f"  {number}: {len(todo)} arquivo(s) enviado(s)")


def bom_child_numbers(lines):
    numbers = []
    for line in lines:
        for key in ("child_number", "child_item_number", "item_number", "number"):
            if line.get(key):
                numbers.append(line[key])
                break
        else:
            numbers.append(None)
    return numbers


def ensure_bom(api: Api, number: str, rev: dict, children):
    path = f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/bom"
    _, lines = api.call("GET", path)
    present = set(n for n in bom_child_numbers(lines) if n)
    if rev["state"] != "in_work":
        print(f"  BOM: {len(present)} linha(s) existente(s), revisão {rev['state']}")
        return
    ensure_checkout(api, number, rev)
    added = 0
    for find, child in enumerate(children, start=1):
        if child["number"] in present:
            continue
        note = f"Corpo no modelo: {child['body']}. " if child["body"] not in ("", "—") else ""
        if child["note"]:
            note += child["note"]
        if child["quantity"] != 1.0:
            note += f" Quantidade: {child['qty_raw']}."
        api.call("POST", path, {
            "child": child["number"],
            "quantity": child["quantity"],
            "find_number": find,
            "notes": note.strip()[:500],
        })
        added += 1
    print(f"  BOM: {len(present)} linha(s) existente(s), {added} adicionada(s)")


def ensure_references(api: Api, number: str, rev: dict, docs):
    path = f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/references"
    _, data = api.call("GET", path)
    present = set()
    for ref in data.get("outgoing", []):
        for key in ("to_number", "item_number", "number"):
            if isinstance(ref.get(key), str):
                present.add(ref[key])
                break
    if rev["state"] != "in_work":
        print(f"  referências: {len(present)} existente(s), revisão {rev['state']}")
        return
    ensure_checkout(api, number, rev)
    added = 0
    for doc_number, meta in docs.items():
        if doc_number in present:
            continue
        api.call("POST", path, {"item": doc_number, "kind": meta["kind"],
                               "note": "Documento controlado do PS-001"})
        added += 1
    print(f"  referências: {len(present)} existente(s), {added} adicionada(s)")


def find_change(api: Api):
    _, data = api.call("GET", "/changes?limit=100")
    for change in data.get("changes", []):
        if change["title"] == CHANGE_TITLE:
            return change
    return None


def change_item_keys(api: Api, number: str):
    _, data = api.call("GET", f"/changes/{number}")
    return {(i.get("item_number"), i.get("code") or i.get("revision_code"))
            for i in data.get("items", [])}


def ensure_change(api: Api, items, approve: bool, reviewer_api: Api | None):
    change = find_change(api)
    if change is None:
        _, change = api.call("POST", "/changes", {
            "title": CHANGE_TITLE,
            "description": (
                "Primeira liberação do PS-001: modelo 3D aprovado (v0.15.0), "
                "prancha A2 rev. A (v0.17.0), documentos US/CO/PL/LM e os 16 "
                "itens da lista de materiais. Revisão A de todos os itens."
            ),
            "priority": "high",
        })
        print(f"ECO {change['number']} criada")
    else:
        print(f"ECO {change['number']} já existe ({change['status']})")

    if change["status"] == "draft":
        have = change_item_keys(api, change["number"])
        for number, code in items:
            if (number, code) in have:
                continue
            api.call("POST", f"/changes/{change['number']}/items",
                     {"item": number, "revision": code})
        _, data = api.call("GET", f"/changes/{change['number']}")
        reviewer_names = {r["reviewer_username"] for r in data.get("reviews", [])}
        if "revisor" not in reviewer_names:
            api.call("POST", f"/changes/{change['number']}/reviewers", {"username": "revisor"})
            print("  revisor adicionado")
        _, readiness = api.call("GET", f"/changes/{change['number']}/readiness")
        print(f"  prontidão: ready={readiness['ready']} "
              f"blockers={len(readiness['blockers'])} warnings={len(readiness['warnings'])}")
        if readiness["blockers"]:
            for b in readiness["blockers"]:
                print("   blocker:", b)
            sys.exit("a ECO tem bloqueios; corrija antes de submeter")
        _, data = api.call("POST", f"/changes/{change['number']}/submit")
        change = data["change"]
        print(f"  ECO submetida: {change['status']}")

    if change["status"] == "in_review" and approve:
        if reviewer_api is None:
            print("  sem TEAMCRAFT_REVIEWER_TOKEN: ECO fica em revisão")
            return change
        _, data = api.call("GET", f"/changes/{change['number']}")
        pending = [r["reviewer_username"] for r in data.get("reviews", [])
                   if r.get("decision") == "pending"]
        for username in pending:
            if username != "revisor":
                print(f"  revisor pendente inesperado: {username}")
                continue
            _, data = reviewer_api.call(
                "POST", f"/changes/{change['number']}/review",
                {"decision": "approve",
                 "comment": "Revisão A conferida contra o modelo e a prancha publicados."})
            change = data["change"]
            print(f"  ECO aprovada por {username}: {change['status']}")
    return change


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-approve", action="store_true",
                        help="submete a ECO mas não aprova")
    args = parser.parse_args()

    check_inputs()
    server = os.environ.get("TEAMCRAFT_SERVER", "http://127.0.0.1:8080")
    admin_token = os.environ.get("TEAMCRAFT_ADMIN_TOKEN")
    reviewer_token = os.environ.get("TEAMCRAFT_REVIEWER_TOKEN")
    if not admin_token:
        sys.exit("defina TEAMCRAFT_ADMIN_TOKEN")
    api = Api(server, admin_token)
    reviewer_api = Api(server, reviewer_token) if reviewer_token else None

    bom = read_bom()
    ensure_project(api)

    print("\n== documentos ==")
    for number, meta in DOCS.items():
        data = ensure_item(api, number, "document", meta["name"], meta["description"])
        rev = revision(data)
        ensure_files(api, number, rev, meta["files"], f"{number} rev. A")
        data = get_item(api, number)
        rev = revision(data)

    print("\n== itens da lista de materiais ==")
    for child in bom:
        description = " ".join(part for part in [
            child["dimensions"],
            f"Volume {child['volume']} cm³." if child["volume"] not in ("", "—") else "",
            child["note"],
        ] if part).strip()
        ensure_item(api, child["number"], "part", child["name"], description,
                    material=child["material"],
                    classification=CLASSIFICATION.get(child["number"]))

    print("\n== conjunto ==")
    assembly = ensure_item(
        api, ASSEMBLY, "assembly", PROJECT["name"],
        "Modelo 3D aprovado (v0.15.0): 22 corpos, envelope 148,31 × 52,25 × 312,72 mm, "
        "448,4 cm³ de material. Transformador EI-75, secundário de fita de cobre, "
        "cabo em madeira. Estudo não certificado; 127 V.",
        classification="make")
    rev = revision(assembly)
    ensure_files(api, ASSEMBLY, rev, ASSEMBLY_FILES, "PS-001 rev. A — modelo e renders")

    print("\n== estrutura ==")
    assembly = get_item(api, ASSEMBLY)
    rev = revision(assembly)
    ensure_bom(api, ASSEMBLY, rev, bom)
    ensure_references(api, ASSEMBLY, rev, DOCS)

    print("\n== ciclo de vida ==")
    items = [(ASSEMBLY, "A"), *[(d, "A") for d in DOCS], *[(b["number"], "A") for b in bom]]
    change = ensure_change(api, items, approve=not args.no_approve,
                           reviewer_api=reviewer_api)

    print("\n== verificação ==")
    expected = [n for n, _ in items]
    states = {}
    for number in expected:
        data = get_item(api, number)
        rev = revision(data)
        states[number] = rev["state"] if rev else "sem rev. A"
    bad = {n: s for n, s in states.items() if s != "released"}
    print(f"itens liberados: {len(expected) - len(bad)}/{len(expected)}; ECO {change['number']}: "
          f"{change['status']}")
    if bad:
        print("pendentes:", bad)
        sys.exit(1)
    print("migração concluída")


if __name__ == "__main__":
    main()
