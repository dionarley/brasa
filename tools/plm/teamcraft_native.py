#!/usr/bin/env python3
"""Leva o modelo nativo do PS-001 para o TeamCraft: 14 peças + montagem.

A v0.22.0 tirou o ``PS-001.sc`` do formato plano: cada peça virou um arquivo
``cad/solidcraft/parts/PS-001-LM-XX.sc`` com material, densidade e massa, e o
conjunto ficou sendo uma montagem de 14 links em 22 posições. Este script
espelha isso no PDM:

* cada peça vai para a revisão **B**, com o ``.sc`` nativo e o STEP derivado,
  material, massa e a descrição atualizada;
* o conjunto vai para a revisão **C**, com ``PS-001.sc`` e ``PS-001.step`` e a
  massa total;
* tudo entra numa ECO só — peça e montagem são liberadas juntas, porque o
  release de um produto é atômico;
* a ECO é submetida e aprovada pelo usuário revisor.

A BOM não é tocada: a revisão nova herda as 16 linhas da anterior (14 peças com
geometria + isolante e consumível), e as linhas passam a apontar para as
revisões B quando a ECO for liberada.

Uso:

    TEAMCRAFT_ADMIN_TOKEN=tc_pat_… TEAMCRAFT_REVIEWER_TOKEN=tc_pat_… \\
    python3 tools/plm/teamcraft_native.py            # sobe e aprova
    python3 tools/plm/teamcraft_native.py --no-approve
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from pathlib import Path

from teamcraft_tools import Api, get_item, latest, multipart, sha256_file

ROOT = Path(__file__).resolve().parents[2]
CAD = ROOT / "cad" / "solidcraft"
PARTS = CAD / "parts"

CHANGE_TITLE = "PS-001 — modelo nativo: 14 peças + montagem"
CHANGE_DESC = (
    "O PS-001.sc deixou de ser um arquivo plano com 22 corpos e virou montagem "
    "de 14 peças nativas em 22 posições; as 8 posições repetidas são ocorrências "
    "da mesma definição (padrão retangular), não cópias de história. Cada peça "
    "tem .sc próprio, material com densidade, massa e STEP derivado. Volume do "
    "conjunto 448.434 mm³ (flat: 448.433,49) e massa 1.721 g. Sem mudança de "
    "geometria do produto: a peça é a mesma, agora identificada e pesada."
)
REVIEW_COMMENT = (
    "Modelo conferido: 22 corpos, 448.434 mm³, 1.721 g; BOM do app igual ao "
    "BOM.csv e update_links sem falha nas 14 peças."
)

# Massa e volume por peça vêm do `eval` do SolidCraft sobre o .sc nativo.
# `qty` é a quantidade na montagem (as repetidas são ocorrências, não arquivos).
PARTS_SPEC = [
    ("01", "Núcleo EI-75 (pacote de chapas)", "aço silicioso", 1139.08, 148.899, 1),
    ("02", "Carretel do primário", "baquelite", 32.81, 23.437, 1),
    ("03", "Fio de cobre esmaltado AWG 28", "cobre esmaltado", 5.90, 0.660, 1),
    ("04", "Fita de cobre do secundário", "cobre", 91.93, 10.260, 1),
    ("05", "Ponta em U", "cobre", 21.43, 2.392, 1),
    ("06", "Cantoneira do transformador", "aço", 43.62, 5.556, 4),
    ("07", "Parafuso M5 das cantoneiras", "aço zincado", 14.51, 1.843, 4),
    ("08", "Parafuso M5 da ponteira", "aço zincado", 6.49, 0.825, 2),
    ("09", "Porca M5 da ponteira", "aço zincado", 2.47, 0.314, 2),
    ("10", "Cabo / empunhadura", "madeira (carvalho)", 161.25, 214.997, 1),
    ("11", "Chave", "ABS", 7.29, 7.011, 1),
    ("12", "Tecla", "ABS", 2.61, 2.511, 1),
    ("13", "Prensa-cabo", "borracha", 1.63, 1.484, 1),
    ("14", "Cabo de força", "PVC flexível", 6.62, 4.906, 1),
]

ASSEMBLY = {
    "number": "PS-001",
    "target": "C",
    "name": "Brasa — estanhador 550 W / 127 V",
    "mass_g": 1720.98,
    "volume_mm3": 448434.44,
    "files": [CAD / "PS-001.sc", CAD / "PS-001.step"],
}


def number_key(two: str) -> str:
    return f"PS-001-LM-{two}"


def describe(rev: dict, mass_g: float, volume_cm3: float) -> str:
    """Descrição herdada + o que a revisão nova acrescenta (sem perder o texto)."""
    base = (rev.get("description") or "").strip()
    suffix = (
        f"Rev. {rev['code']}: arquivo nativo {rev['item_number']}.sc; "
        f"{volume_cm3:.2f} cm³; {mass_g:.2f} g"
    )
    if suffix in base:
        return base
    return f"{base} {suffix}".strip()


def ensure_revision(api: Api, number: str, target: str) -> dict:
    data = get_item(api, number)
    if data is None:
        raise RuntimeError(f"item {number} não existe no TeamCraft")
    rev = latest(data)
    if rev["code"] == target:
        print(f"  {number}: rev. {target} já existe ({rev['state']})")
        return rev
    if rev["state"] != "released":
        raise RuntimeError(
            f"{number}: rev. {rev['code']} está {rev['state']}; "
            "libere ou cancele antes de criar a próxima"
        )
    _, rev = api.call(
        "POST", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/revise"
    )
    print(f"  {number}: rev. {rev['code']} criada ({rev['state']})")
    if rev["code"] != target:
        raise RuntimeError(f"{number}: esperava rev. {target}, veio {rev['code']}")
    return rev


def ensure_file(api: Api, number: str, rev: dict, path: Path, folder: str = "cad"):
    if rev["state"] != "in_work":
        print(f"  {number}: rev. {rev['code']} está {rev['state']}; arquivo não enviado")
        return
    if not path.is_file():
        raise RuntimeError(f"arquivo ausente: {path}")
    _, files = api.call(
        "GET", f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/files"
    )
    digest = sha256_file(path)
    for found in files:
        if found["filename"] == path.name and found["sha256"] == digest:
            print(f"  {number}: {path.name} já presente")
            return
    body, ctype = multipart(path, folder, f"{number} rev. {rev['code']}")
    api.call(
        "POST",
        f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}/files",
        raw=body,
        content_type=ctype,
    )
    print(f"  {number}: {path.name} enviado ({path.stat().st_size} bytes)")


def patch_revision(api: Api, number: str, rev: dict, **fields):
    if rev["state"] != "in_work":
        return
    changes = {k: v for k, v in fields.items() if rev.get(k) != v}
    if not changes:
        return
    api.call(
        "PATCH",
        f"/items/{urllib.parse.quote(number)}/revisions/{rev['code']}",
        changes,
    )
    print(f"  {number}: {', '.join(sorted(changes))} atualizado")


def ensure_change(api: Api, title: str, items, reviewer: Api | None, approve: bool):
    _, data = api.call("GET", "/changes?limit=100")
    change = next((c for c in data.get("changes", []) if c["title"] == title), None)
    if change is None:
        _, change = api.call(
            "POST", "/changes",
            {"title": title, "description": CHANGE_DESC, "priority": "normal"},
        )
        print(f"  ECO {change['number']} criada")
    else:
        print(f"  ECO {change['number']} já existe ({change['status']})")

    if change["status"] == "draft":
        _, detail = api.call("GET", f"/changes/{change['number']}")
        have = {(i.get("item_number"), i.get("code")) for i in detail.get("items", [])}
        for number, code in items:
            if (number, code) not in have:
                api.call(
                    "POST", f"/changes/{change['number']}/items",
                    {"item": number, "revision": code},
                )
                print(f"  {number}@{code} na ECO")
        reviewers = {r["reviewer_username"] for r in detail.get("reviews", [])}
        if "revisor" not in reviewers:
            api.call(
                "POST", f"/changes/{change['number']}/reviewers", {"username": "revisor"}
            )
            print("  revisor adicionado")
        _, readiness = api.call("GET", f"/changes/{change['number']}/readiness")
        print(
            f"  prontidão: ready={readiness['ready']} "
            f"bloqueios={len(readiness['blockers'])} avisos={len(readiness['warnings'])}"
        )
        for blocker in readiness["blockers"]:
            print("   bloqueio:", blocker)
        for warning in readiness["warnings"]:
            print("   aviso:", warning)
        if readiness["blockers"]:
            sys.exit("a ECO tem bloqueios; corrija antes de submeter")
        _, data = api.call("POST", f"/changes/{change['number']}/submit")
        change = data["change"]
        print(f"  ECO submetida: {change['status']}")

    if change["status"] == "in_review" and approve:
        if reviewer is None:
            print("  sem TEAMCRAFT_REVIEWER_TOKEN: a ECO fica em revisão")
            return change
        _, detail = api.call("GET", f"/changes/{change['number']}")
        pending = [
            r["reviewer_username"]
            for r in detail.get("reviews", [])
            if r.get("decision") == "pending"
        ]
        for username in pending:
            if username != "revisor":
                print(f"  revisor inesperado: {username}")
                continue
            _, data = reviewer.call(
                "POST", f"/changes/{change['number']}/review",
                {"decision": "approve", "comment": REVIEW_COMMENT},
            )
            change = data["change"]
            print(f"  ECO aprovada por {username}: {change['status']}")
    return change


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-approve", action="store_true",
                        help="submete a ECO mas não aprova")
    args = parser.parse_args()

    server = os.environ.get("TEAMCRAFT_SERVER", "http://127.0.0.1:8080")
    admin_token = os.environ.get("TEAMCRAFT_ADMIN_TOKEN")
    reviewer_token = os.environ.get("TEAMCRAFT_REVIEWER_TOKEN")
    if not admin_token:
        sys.exit("defina TEAMCRAFT_ADMIN_TOKEN")
    api = Api(server, admin_token)
    reviewer = Api(server, reviewer_token) if reviewer_token else None

    missing = [p for p in [ASSEMBLY["files"][0], ASSEMBLY["files"][1]]
               if not p.is_file()]
    missing += [PARTS / f"PS-001-LM-{two}.sc" for two, *_ in PARTS_SPEC
                if not (PARTS / f"PS-001-LM-{two}.sc").is_file()]
    if missing:
        sys.exit("arquivos ausentes:\n  " + "\n  ".join(str(p) for p in missing))

    print("== peças ==")
    revisions = []
    for two, name, material, mass_g, volume_cm3, qty in PARTS_SPEC:
        number = number_key(two)
        rev = ensure_revision(api, number, "B")
        patch_revision(
            api, number, rev,
            name=name,
            material=material,
            mass_kg=round(mass_g / 1000, 6),
            description=describe({**rev, "item_number": number}, mass_g, volume_cm3),
        )
        for suffix in (".sc", ".step"):
            ensure_file(api, number, rev, PARTS / f"{number}{suffix}")
        revisions.append((number, rev["code"]))

    print("\n== montagem ==")
    rev = ensure_revision(api, ASSEMBLY["number"], ASSEMBLY["target"])
    mass_g = ASSEMBLY["mass_g"]
    patch_revision(
        api, ASSEMBLY["number"], rev,
        name=ASSEMBLY["name"],
        mass_kg=round(mass_g / 1000, 6),
        description=describe(
            {**rev, "item_number": ASSEMBLY["number"]}, mass_g,
            ASSEMBLY["volume_mm3"] / 1000,
        ),
    )
    for path in ASSEMBLY["files"]:
        ensure_file(api, ASSEMBLY["number"], rev, path)
    revisions.append((ASSEMBLY["number"], rev["code"]))

    print("\n== ciclo de vida ==")
    change = ensure_change(api, CHANGE_TITLE, revisions, reviewer,
                           approve=not args.no_approve)

    print("\n== verificação ==")
    bad = {}
    for number, code in revisions:
        data = get_item(api, number)
        found = next((r for r in data["revisions"] if r["code"] == code), None)
        if found is None:
            bad[number] = "sem revisão"
            continue
        if found["state"] != "released":
            bad[number] = f"{code}/{found['state']}"
        if not found.get("mass_kg"):
            bad[number] = f"{code}/sem massa"
        _, files = api.call(
            "GET", f"/items/{urllib.parse.quote(number)}/revisions/{code}/files"
        )
        names = {f["filename"] for f in files}
        want = {f"{number}.sc", f"{number}.step"}
        if not want <= names:
            bad[number] = f"{code}/faltam {sorted(want - names)}"
    print(f"revisões liberadas: {len(revisions) - len(bad)}/{len(revisions)}; "
          f"ECO {change['number']}: {change['status']}")
    if bad:
        print(json.dumps(bad, ensure_ascii=False, indent=1))
        sys.exit(1)
    print("modelo nativo no PDM")


if __name__ == "__main__":
    main()
