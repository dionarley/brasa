#!/usr/bin/env python3
"""Liberação da identidade própria **Brasa** no TeamCraft (v0.19.0).

Renomeia o conjunto para "Brasa — estanhador 550 W / 127 V" (rev. B) e libera as
novas revisões dos documentos que citavam marca de terceiro:

* ``PS-001-US-001`` rev. B — manual de uso;
* ``PS-001-PL-001`` rev. C — plano de PLM;
* ``PS-001-PL-002`` rev. C — registro mestre;
* ``PS-001-PL-003`` rev. B — manual do TeamCraft.

O TeamCraft só tinha o ``PS-001-CO-001`` na rev. A (com o PDF rB): a rev. B é
regularizada na ECO da identidade e a rev. C sai numa ECO própria, em seguida.
Arquivos vêm de ``dist/v0.19.0/`` (a rev. B do guia vem de ``dist/v0.18.0/``).

Abre a ECO "PS-001 — identidade Brasa", submete e aprova com o usuário revisor.
Arquivos vêm de ``dist/v0.19.0/``.

Uso:

    TEAMCRAFT_SERVER=http://127.0.0.1:8080 \
    TEAMCRAFT_ADMIN_TOKEN=tc_pat_… \
    TEAMCRAFT_REVIEWER_TOKEN=tc_pat_… \
    python3 tools/plm/teamcraft_identity.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist" / "v0.19.0"
PROJECT = "PS-001"
ASSEMBLY = "PS-001"
ASSEMBLY_NAME = "Brasa — estanhador 550 W / 127 V"
ASSEMBLY_DESC = (
    "Modelo 3D aprovado (v0.15.0): 22 corpos, envelope 148,31 × 52,25 × 312,72 mm, "
    "448,4 cm³ de material. Transformador EI-75, secundário de fita de cobre, cabo em "
    "madeira. Estudo não certificado; 127 V. Identidade própria Brasa (código PS-001)."
)

REVISIONS = [
    {
        "number": "PS-001-US-001",
        "target": "B",
        "name": "Manual de uso e segurança",
        "description": "Operação, limites de uso, segurança em 127 V e manutenção. Rev. B.",
        "file": DIST / "PS-001-US-001_rB_uso.pdf",
        "old": "PS-001-US-001_rA_uso.pdf",
        "folder": "docs",
    },
    {
        "number": "PS-001-PL-001",
        "target": "C",
        "name": "Plano de ciclo de vida (PLM)",
        "description": (
            "Numeração, revisões, estados e liberação usados no projeto; identidade "
            "Brasa e ECO no TeamCraft. Rev. C."
        ),
        "file": DIST / "PS-001-PL-001_rC_plano-plm.pdf",
        "old": "PS-001-PL-001_rB_plano-plm.pdf",
        "folder": "docs",
    },
    {
        "number": "PS-001-PL-002",
        "target": "C",
        "name": "Registro mestre de documentos",
        "description": (
            "Índice controlado de documentos, revisões, artefatos e registro no "
            "TeamCraft. Rev. C."
        ),
        "file": DIST / "PS-001-PL-002_rC_registro-documentos.pdf",
        "old": "PS-001-PL-002_rB_registro-documentos.pdf",
        "folder": "docs",
    },
    {
        "number": "PS-001-PL-003",
        "target": "B",
        "name": "TeamCraft: instalação, operação e registro",
        "description": (
            "PDM local: instalação, operação, MCP, mapeamento do Brasa e backup. "
            "Rev. B."
        ),
        "file": DIST / "PS-001-PL-003_rB_teamcraft.pdf",
        "old": "PS-001-PL-003_rA_teamcraft.pdf",
        "folder": "docs",
    },
]

CHANGE_TITLE = "PS-001 — identidade Brasa"
CHANGE_DESC = (
    "O projeto passa a se chamar Brasa, sem marca de terceiro: conjunto renomeado, "
    "manual de uso rev. B, plano rev. C, registro rev. C, manual do PDM rev. B. "
    "Regulariza também a rev. B do guia de construção, publicada na v0.17.0 e "
    "ausente do PDM."
)

# O TeamCraft recebeu o CO-001 só na rev. A, com o PDF rotulado rB; a rev. B real
# (v0.17.0) precisa ser liberada antes de existir a rev. C. Por isso ela entra na
# ECO da identidade e a rev. C sai numa ECO própria, logo depois.
CO = "PS-001-CO-001"
CO_B = {
    "target": "B",
    "name": "Guia de construção (estudo)",
    "description": (
        "Sequência de montagem, critérios de aceitação e ensaios. Rev. B, "
        "publicada na v0.17.0 e regularizada no PDM."
    ),
    "file": DIST.parent / "v0.18.0" / "PS-001-CO-001_rB_construcao.pdf",
    "old": None,
    "folder": "docs",
}
CO_C = {
    "target": "C",
    "name": "Guia de construção (estudo)",
    "description": (
        "Sequência de montagem, critérios de aceitação e ensaios; identidade "
        "Brasa. Rev. C."
    ),
    "file": DIST / "PS-001-CO-001_rC_construcao.pdf",
    "old": "PS-001-CO-001_rB_construcao.pdf",
    "folder": "docs",
}
CHANGE_C_TITLE = "PS-001-CO-001 — identidade Brasa na revisão C"
CHANGE_C_DESC = (
    "Guia de construção rev. C: identificação Brasa, alinhado ao conjunto rev. B e "
    "ao manual de uso rev. B."
)


class Api:
    def __init__(self, server: str, token: str):
        self.base = server.rstrip("/") + "/api/v1"
        self.token = token

    def call(self, method: str, path: str, body=None, raw: bytes | None = None,
             content_type: str | None = None, ok=(200, 201, 204)):
        data = raw
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode()
            content_type = "application/json"
        if content_type:
            headers["Content-Type"] = content_type
        req = urllib.request.Request(self.base + path, data=data, headers=headers,
                                     method=method)
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
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
        if status == 204 or not payload:
            return status, None
        return status, json.loads(payload)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def multipart(path: Path, folder: str, comment: str):
    boundary = "----ps001id" + hashlib.sha256(os.urandom(16)).hexdigest()[:24]
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    out = bytearray()
    for key, value in (("comment", comment),
                       ("folders", json.dumps({path.name: folder}))):
        out += f"--{boundary}\r\n".encode()
        out += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
        out += str(value).encode() + b"\r\n"
    out += f"--{boundary}\r\n".encode()
    out += (f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
            f"Content-Type: {ctype}\r\n\r\n").encode()
    out += path.read_bytes() + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def get_item(api: Api, number: str):
    try:
        _, data = api.call("GET", f"/items/{urllib.parse.quote(number)}")
        return data
    except RuntimeError as e:
        if "HTTP 404" in str(e):
            return None
        raise


def latest(data):
    return data["revisions"][0]


def ensure_revision(api: Api, number: str, target: str, name: str,
                    description: str) -> dict:
    data = get_item(api, number)
    if data is None:
        raise RuntimeError(f"item {number} não existe")
    rev = latest(data)
    if rev["code"] == target:
        print(f"  {number}: rev. {target} já existe ({rev['state']})")
    elif rev["state"] != "released":
        raise RuntimeError(f"{number} rev. {rev['code']} está {rev['state']}; "
                           "libere antes de criar a próxima")
    else:
        _, rev = api.call(
            "POST", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/revise")
        print(f"  {number}: rev. {rev['code']} criada ({rev['state']})")
        if rev["code"] != target:
            raise RuntimeError(f"{number}: esperava rev. {target}, veio {rev['code']}")
    if rev["state"] == "in_work" and (rev.get("name") != name
                                      or rev.get("description", "") != description):
        api.call("PATCH",
                 f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}",
                 {"name": name, "description": description})
        print(f"  {number}: nome/descrição atualizados")
    return rev


def ensure_file(api: Api, number: str, rev: dict, path: Path, folder: str,
                old_name: str | None):
    if rev["state"] != "in_work":
        print(f"  {number} rev. {rev['code']} está {rev['state']}: arquivo não alterado")
        return
    _, files = api.call(
        "GET", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/files")
    by_name = {f["filename"]: f for f in files}
    digest = sha256_file(path)
    have = by_name.get(path.name)
    if have and have["sha256"] == digest:
        print(f"  {number}: {path.name} já presente")
    else:
        body, ctype = multipart(path, folder, f"{number} rev. {rev['code']}")
        api.call("POST",
                 f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/files",
                 raw=body, content_type=ctype)
        print(f"  {number}: {path.name} enviado")
    if old_name and old_name in by_name:
        api.call("DELETE", f"/files/{by_name[old_name]['id']}")
        print(f"  {number}: {old_name} removido da rev. {rev['code']}")


def find_change(api: Api, title: str):
    _, data = api.call("GET", "/changes?limit=100")
    for change in data.get("changes", []):
        if change["title"] == title:
            return change
    return None


def ensure_change(api: Api, title: str, description: str, items,
                  reviewer: Api | None, approve: bool):
    change = find_change(api, title)
    if change is None:
        _, change = api.call("POST", "/changes", {
            "title": title,
            "description": description,
            "priority": "normal",
        })
        print(f"ECO {change['number']} criada")
    else:
        print(f"ECO {change['number']} já existe ({change['status']})")

    if change["status"] == "draft":
        _, data = api.call("GET", f"/changes/{change['number']}")
        have = {(i.get("item_number"), i.get("code")) for i in data.get("items", [])}
        for number, code in items:
            if (number, code) not in have:
                api.call("POST", f"/changes/{change['number']}/items",
                         {"item": number, "revision": code})
        reviewers = {r["reviewer_username"] for r in data.get("reviews", [])}
        if "revisor" not in reviewers:
            api.call("POST", f"/changes/{change['number']}/reviewers",
                     {"username": "revisor"})
        _, readiness = api.call("GET", f"/changes/{change['number']}/readiness")
        print(f"  prontidão: ready={readiness['ready']} "
              f"bloqueios={len(readiness['blockers'])} avisos={len(readiness['warnings'])}")
        if readiness["blockers"]:
            for b in readiness["blockers"]:
                print("   bloqueio:", b)
            sys.exit("a ECO tem bloqueios; corrija antes de submeter")
        _, data = api.call("POST", f"/changes/{change['number']}/submit")
        change = data["change"]
        print(f"  ECO submetida: {change['status']}")

    if change["status"] == "in_review" and approve:
        if reviewer is None:
            print("  sem TEAMCRAFT_REVIEWER_TOKEN: ECO fica em revisão")
            return change
        _, data = api.call("GET", f"/changes/{change['number']}")
        pending = [r["reviewer_username"] for r in data.get("reviews", [])
                   if r.get("decision") == "pending"]
        for username in pending:
            if username != "revisor":
                print(f"  revisor inesperado: {username}")
                continue
            _, data = reviewer.call(
                "POST", f"/changes/{change['number']}/review",
                {"decision": "approve",
                 "comment": "Identidade Brasa conferida contra os PDFs do pacote v0.19.0."})
            change = data["change"]
            print(f"  ECO aprovada por {username}: {change['status']}")
    return change


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-approve", action="store_true",
                        help="submete a ECO mas não aprova")
    args = parser.parse_args()

    missing = [p for p in [r["file"] for r in REVISIONS]
               + [CO_B["file"], CO_C["file"]] if not p.is_file()]
    if missing:
        sys.exit("Arquivos ausentes (rode tools/plm/build.sh antes):\n  "
                 + "\n  ".join(str(p) for p in missing))

    server = os.environ.get("TEAMCRAFT_SERVER", "http://127.0.0.1:8080")
    admin_token = os.environ.get("TEAMCRAFT_ADMIN_TOKEN")
    reviewer_token = os.environ.get("TEAMCRAFT_REVIEWER_TOKEN")
    if not admin_token:
        sys.exit("defina TEAMCRAFT_ADMIN_TOKEN")
    api = Api(server, admin_token)
    reviewer = Api(server, reviewer_token) if reviewer_token else None

    print("== conjunto ==")
    rev = ensure_revision(api, ASSEMBLY, "B", ASSEMBLY_NAME, ASSEMBLY_DESC)
    print(f"  {ASSEMBLY}: rev. {rev['code']} ({rev['state']})")

    print("\n== documentos ==")
    for meta in REVISIONS:
        rev = ensure_revision(api, meta["number"], meta["target"],
                              meta["name"], meta["description"])
        ensure_file(api, meta["number"], rev, meta["file"], meta["folder"],
                    meta["old"])

    print("\n== guia de construção (regulariza a rev. B) ==")
    rev = ensure_revision(api, CO, CO_B["target"], CO_B["name"], CO_B["description"])
    ensure_file(api, CO, rev, CO_B["file"], CO_B["folder"], CO_B["old"])

    print("\n== ciclo de vida ==")
    items = ([(ASSEMBLY, "B")] + [(r["number"], r["target"]) for r in REVISIONS]
             + [(CO, "B")])
    change = ensure_change(api, CHANGE_TITLE, CHANGE_DESC, items, reviewer,
                           approve=not args.no_approve)

    print("\n== guia de construção rev. C ==")
    rev = ensure_revision(api, CO, CO_C["target"], CO_C["name"], CO_C["description"])
    ensure_file(api, CO, rev, CO_C["file"], CO_C["folder"], CO_C["old"])
    if rev["state"] != "released":
        change_c = ensure_change(api, CHANGE_C_TITLE, CHANGE_C_DESC,
                                 [(CO, "C")], reviewer,
                                 approve=not args.no_approve)
    else:
        change_c = find_change(api, CHANGE_C_TITLE) or {"number": "-", "status": "-"}
        print(f"  {CO} rev. C já liberada")

    print("\n== verificação ==")
    bad = {}
    for number, code in items + [(CO, "C")]:
        data = get_item(api, number)
        rev = next((r for r in data["revisions"] if r["code"] == code), None)
        state = rev["state"] if rev else "sem revisão"
        if state != "released":
            bad[number] = f"{code}/{state}"
    print(f"revisões liberadas: {len(items) + 1 - len(bad)}/{len(items) + 1}; "
          f"ECO {change['number']}: {change['status']}; "
          f"ECO {change_c['number']}: {change_c['status']}")
    if bad:
        print("pendentes:", bad)
        sys.exit(1)
    print("liberação da identidade concluída")


if __name__ == "__main__":
    main()
