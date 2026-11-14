#!/usr/bin/env python3
"""Segunda liberação do PS-001 no TeamCraft: documentação do PDM.

Cria ``PS-001-PL-003`` rev. A (manual do TeamCraft) e revisa ``PS-001-PL-001``
e ``PS-001-PL-002`` para a rev. B, anexando os PDFs de ``dist/v0.18.0/``.
Abre a ECO "PS-001 — documentação do PLM no TeamCraft", submete e aprova com o
usuário revisor.

O script é idempotente: itens e revisões existentes são reaproveitados, arquivos
são comparados por sha256 e a ECO é retomada pelo título.

Uso:

    TEAMCRAFT_SERVER=http://127.0.0.1:8080 \
    TEAMCRAFT_ADMIN_TOKEN=tc_pat_… \
    TEAMCRAFT_REVIEWER_TOKEN=tc_pat_… \
    python3 tools/plm/teamcraft_docs_b.py
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
DIST = ROOT / "dist" / "v0.18.0"
PROJECT = "PS-001"

NEW_DOC = {
    "number": "PS-001-PL-003",
    "name": "TeamCraft: instalação, operação e registro",
    "description": (
        "PDM local: instalação do TeamCraft 0.2.7, PostgreSQL em podman, usuários e "
        "tokens, operação de check-out/ECO, MCP do OpenCode, mapeamento do PS-001 e "
        "backup/restauração. Rev. A."
    ),
    "file": DIST / "PS-001-PL-003_rA_teamcraft.pdf",
    "folder": "docs",
}

REVISIONS = [
    {
        "number": "PS-001-PL-001",
        "file": DIST / "PS-001-PL-001_rB_plano-plm.pdf",
        "old": "PS-001-PL-001_rA_plano-plm.pdf",
        "folder": "docs",
    },
    {
        "number": "PS-001-PL-002",
        "file": DIST / "PS-001-PL-002_rB_registro-documentos.pdf",
        "old": "PS-001-PL-002_rA_registro-documentos.pdf",
        "folder": "docs",
    },
]

CHANGE_TITLE = "PS-001 — documentação do PLM no TeamCraft"
CHANGE_DESC = (
    "Adoção do TeamCraft como PDM: PL-001 rev. B (processo com ECO e quatro olhos), "
    "PL-002 rev. B (registro do PDM) e PL-003 rev. A (manual de instalação, operação, "
    "MCP e backup). Os PDFs vêm do pacote v0.18.0."
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
    boundary = "----ps001b" + hashlib.sha256(os.urandom(16)).hexdigest()[:24]
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
    revs = data.get("revisions", [])
    return revs[0] if revs else None


def ensure_item(api: Api, number: str, name: str, description: str):
    data = get_item(api, number)
    if data is None:
        _, rev = api.call("POST", "/items", {
            "item_type": "document",
            "name": name,
            "number": number,
            "project": PROJECT,
            "description": description,
            "idempotency_key": f"ps001-docs-b-{number}",
        })
        print(f"item {number} criado (rev. {rev['code']}, {rev['state']})")
        return get_item(api, number)
    print(f"item {number} já existe (rev. {latest(data)['code']}, {latest(data)['state']})")
    return data


def ensure_revision_b(api: Api, number: str):
    data = get_item(api, number)
    rev = latest(data)
    if rev["code"] == "B":
        print(f"  {number}: rev. B já existe ({rev['state']})")
        return rev
    if rev["state"] != "released":
        raise RuntimeError(f"{number} rev. {rev['code']} está {rev['state']}; "
                           "libere antes de criar a rev. B")
    _, new = api.call(
        "POST", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/revise")
    print(f"  {number}: rev. {new['code']} criada ({new['state']})")
    return new


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


def find_change(api: Api):
    _, data = api.call("GET", "/changes?limit=100")
    for change in data.get("changes", []):
        if change["title"] == CHANGE_TITLE:
            return change
    return None


def ensure_change(api: Api, items, reviewer: Api | None, approve: bool):
    change = find_change(api)
    if change is None:
        _, change = api.call("POST", "/changes", {
            "title": CHANGE_TITLE,
            "description": CHANGE_DESC,
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
                 "comment": "Documentação conferida contra os PDFs do pacote v0.18.0."})
            change = data["change"]
            print(f"  ECO aprovada por {username}: {change['status']}")
    return change


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-approve", action="store_true",
                        help="submete a ECO mas não aprova")
    args = parser.parse_args()

    missing = [p for p in [NEW_DOC["file"], *[r["file"] for r in REVISIONS]]
               if not p.is_file()]
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

    print("== PL-003 ==")
    ensure_item(api, NEW_DOC["number"], NEW_DOC["name"], NEW_DOC["description"])
    rev = latest(get_item(api, NEW_DOC["number"]))
    ensure_file(api, NEW_DOC["number"], rev, NEW_DOC["file"], NEW_DOC["folder"], None)

    print("\n== revisões B ==")
    for meta in REVISIONS:
        ensure_item(api, meta["number"],
                    latest(get_item(api, meta["number"]))["name"],
                    latest(get_item(api, meta["number"])).get("description", ""))
        rev = ensure_revision_b(api, meta["number"])
        ensure_file(api, meta["number"], rev, meta["file"], meta["folder"],
                    meta["old"])

    print("\n== ciclo de vida ==")
    items = [(NEW_DOC["number"], "A"),
             *[(r["number"], "B") for r in REVISIONS]]
    change = ensure_change(api, items, reviewer, approve=not args.no_approve)

    print("\n== verificação ==")
    bad = {}
    for number, code in items:
        data = get_item(api, number)
        rev = next((r for r in data["revisions"] if r["code"] == code), None)
        state = rev["state"] if rev else "sem revisão"
        if state != "released":
            bad[number] = f"{code}/{state}"
    print(f"revisões liberadas: {len(items) - len(bad)}/{len(items)}; "
          f"ECO {change['number']}: {change['status']}")
    if bad:
        print("pendentes:", bad)
        sys.exit(1)
    print("segunda liberação concluída")


if __name__ == "__main__":
    main()
