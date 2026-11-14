#!/usr/bin/env python3
"""Monta a prancha A2 do PS-001 a partir das projeções exportadas pelo SolidCraft.

Entrada : out/draw/v017/{frente,lado,topo,iso}.dxf  (file.export_view_dxf, 1:1)
          docs/construcao/BOM.csv                   (lista de materiais oficial)
Saída   : out/draw/v017/PS-001_A2.dxf                (ABNT A2, 1º diedro, 1:2)

O DXF gerado é o de trabalho. A publicação (PS-001-DR-001 rev. A) sai do OpenCADStudio:
abrir o DXF, `ocs_audit` (dxf/2018), `plot` A2 1:1 e `save_verified` para
out/draw/v017/PS-001-DR-001_rA_prancha-a2.{pdf,dxf}.

A geometria das vistas NÃO é desenhada aqui: vem do modelo. Este script só
reposiciona, escala e acrescenta a moldura, o carimbo, as cotas e a BOM.
"""
import csv
import math
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "out/draw/v017")
OUT = os.path.join(SRC, "PS-001_A2.dxf")
BOM = os.path.join(ROOT, "docs/construcao/BOM.csv")

SHEET_W, SHEET_H = 594.0, 420.0     # A2 paisagem
MARGIN = 10.0
SCALE = 0.5                          # 1:2
TXT = 2.6                            # altura de texto padrão
TXT_SM = 2.1

# ------------------------------------------------------------------ DXF base


def group(code, value):
    return f"{code}\n{value}\n"


class Drawing:
    def __init__(self):
        self.ent = []

    def line(self, x1, y1, x2, y2, layer="CONTORNO"):
        self.ent.append(f"0\nLINE\n8\n{layer}\n10\n{x1:.3f}\n20\n{y1:.3f}\n30\n0\n"
                        f"11\n{x2:.3f}\n21\n{y2:.3f}\n31\n0\n")

    def poly(self, pts, layer="CONTORNO", closed=False):
        s = f"0\nLWPOLYLINE\n8\n{layer}\n90\n{len(pts)}\n70\n{1 if closed else 0}\n"
        for p in pts:
            s += f"10\n{p[0]:.3f}\n20\n{p[1]:.3f}\n"
        self.ent.append(s)

    def text(self, x, y, h, s, layer="TEXTO", align="left", rot=0.0):
        # alinhamento 72/73: 0 esquerda, 1 centro, 2 direita
        code = {"left": 0, "center": 1, "right": 2}[align]
        body = f"0\nTEXT\n8\n{layer}\n10\n{x:.3f}\n20\n{y:.3f}\n30\n0\n40\n{h:.2f}\n1\n{s}\n50\n{rot}\n7\nSTANDARD\n"
        if code:
            body += f"72\n{code}\n11\n{x:.3f}\n21\n{y:.3f}\n31\n0\n"
        self.ent.append(body)

    def rect(self, x0, y0, x1, y1, layer="CONTORNO"):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer, closed=True)

    def write(self, path):
        header = ("0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1015\n9\n$INSUNITS\n70\n4\n"
                  "9\n$MEASUREMENT\n70\n1\n9\n$EXTMIN\n10\n0\n20\n0\n30\n0\n"
                  f"9\n$EXTMAX\n10\n{SHEET_W}\n20\n{SHEET_H}\n30\n0\n0\nENDSEC\n")
        layers = [("CONTORNO", 7), ("OCULTO", 8), ("TEXTO", 7), ("COTA", 7), ("TABELA", 7)]
        tables = "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n%d\n" % len(layers)
        for name, color in layers:
            tables += (f"0\nLAYER\n2\n{name}\n70\n0\n62\n{color}\n6\nCONTINUOUS\n")
        tables += "0\nENDTAB\n0\nENDSEC\n"
        ents = "0\nSECTION\n2\nENTITIES\n" + "".join(self.ent) + "0\nENDSEC\n0\nEOF\n"
        with open(path, "w") as f:
            f.write(header + tables + ents)


# ------------------------------------------------------------- leitura DXF
def read_dxf(path):
    """Devolve [(tipo, camada, [(x,y)…], [bulges])] de LINE e LWPOLYLINE."""
    raw = open(path, errors="ignore").read().split("\n")
    while raw and not raw[-1].strip():      # só o vazio final; vazios internos são valores
        raw.pop()
    pairs = [(raw[i].strip(), raw[i + 1].strip()) for i in range(0, len(raw) - 1, 2)]
    out, cur, pts, bul, layer = [], None, [], [], ""

    def flush():
        if layer == "SKETCH":
            return
        if cur == "LINE" and len(pts) >= 2:
            out.append(("LINE", layer, [pts[0], pts[1]], []))
        elif cur == "LWPOLYLINE" and len(pts) >= 2:
            out.append(("LW", layer, pts[:], bul[:]))

    for code, val in pairs:
        if code == "0":
            flush()
            cur, pts, bul = (val if val in ("LINE", "LWPOLYLINE") else None), [], []
        elif cur:
            if code == "8":
                layer = val
            elif code in ("10", "11"):
                pts.append([float(val), 0.0])
            elif code in ("20", "21"):
                if pts:
                    pts[-1][1] = float(val)
            elif code == "42":
                bul.append(float(val))
            elif code == "70":
                pass
    flush()
    return out


# ------------------------------------------------------------------ cotas
def dim_h(d, x1, x2, y, ytext, label, tick=1.6):
    d.line(x1, y, x1, y + tick * 0.7, "COTA")
    d.line(x2, y, x2, y + tick * 0.7, "COTA")
    d.line(x1, y, x2, y, "COTA")
    for x in (x1, x2):
        d.line(x, y, x + (2.4 if x == x1 else -2.4), y + 0.9, "COTA")
        d.line(x, y, x + (2.4 if x == x1 else -2.4), y - 0.9, "COTA")
    d.text((x1 + x2) / 2, ytext, TXT_SM, label, "COTA", "center")


def dim_v(d, y1, y2, x, xtext, label, tick=1.6):
    d.line(x, y1, x - tick * 0.7, y1, "COTA")
    d.line(x, y2, x - tick * 0.7, y2, "COTA")
    d.line(x, y1, x, y2, "COTA")
    for y in (y1, y2):
        d.line(x, y, x + 0.9, y + (2.4 if y == y1 else -2.4), "COTA")
        d.line(x, y, x - 0.9, y + (2.4 if y == y1 else -2.4), "COTA")
    d.text(xtext, (y1 + y2) / 2, TXT_SM, label, "COTA", "center", 90)


def leader(d, x, y, tx, ty, label):
    d.line(x, y, tx, ty, "COTA")
    d.line(tx, ty, tx + (6 if tx > x else -6), ty, "COTA")
    d.text(tx + (7 if tx > x else -7), ty - 0.8, TXT_SM, label, "COTA",
           "left" if tx > x else "right")


# ------------------------------------------------------------- montagem
def main():
    d = Drawing()
    # moldura
    d.rect(0, 0, SHEET_W, SHEET_H, "CONTORNO")
    d.rect(MARGIN, MARGIN, SHEET_W - MARGIN, SHEET_H - MARGIN, "CONTORNO")

    views = {n: read_dxf(os.path.join(SRC, n + ".dxf"))
             for n in ("frente", "lado", "topo", "iso", "detalhe")}

    def bbox(ents):
        xs, ys = [], []
        for _, _, pts, _ in ents:
            for x, y in pts:
                xs.append(x)
                ys.append(y)
        return min(xs), min(ys), max(xs), max(ys)

    # no DXF a projeção sai em coordenadas da câmera (centrada no alvo 10,0,-110)
    # frente: (x+10, y-110) = (X, Z); lado: (x, y-110) = (Y, Z); topo: (x+10, y) = (X, Y)
    off = {"frente": (10, -110), "lado": (0, -110), "topo": (10, 0),
           "iso": (10, -110), "detalhe": (0, 0)}
    sizes = {}
    for n, ents in views.items():
        x0, y0, x1, y1 = bbox(ents)
        sizes[n] = ((x1 - x0) * SCALE, (y1 - y0) * SCALE)
    print("tamanhos 1:2:", {k: (round(v[0], 1), round(v[1], 1)) for k, v in sizes.items()})

    def place(name, sx, sy, scale=None, offset=None):
        ents = views[name]
        x0, y0, _, _ = bbox(ents)
        ox, oy = offset or off[name]
        sc = SCALE if scale is None else scale
        for typ, layer, pts, bul in ents:
            if layer == "SKETCH":
                continue
            lay = "OCULTO" if layer == "HIDDEN" else "CONTORNO"
            m = [(sx + ((x + ox) - (x0 + ox)) * sc,
                  sy + ((y + oy) - (y0 + oy)) * sc) for x, y in pts]
            if typ == "LINE":
                d.line(m[0][0], m[0][1], m[1][0], m[1][1], lay)
            else:
                s = f"0\nLWPOLYLINE\n8\n{lay}\n90\n{len(m)}\n70\n0\n"
                bb = (bul + [0.0] * len(m))[:len(m)]
                for k, p in enumerate(m):
                    s += f"10\n{p[0]:.3f}\n20\n{p[1]:.3f}\n42\n{bb[k]}\n"
                d.ent.append(s)

    # dados principais (canto superior esquerdo)
    d.text(22, 386, TXT, "DADOS PRINCIPAIS", "TEXTO")
    dados = [
        ("Envelope (X x Y x Z)", "148,3 x 52,3 x 312,7 mm"),
        ("Potência / tensão", "550 W / 127 V ~ 60 Hz"),
        ("Núcleo", "EI-75: 75 x 75 x 35; janela 12,5 x 50; perna 12,5"),
        ("Primário", "~700 espiras AWG 28; carretel 37 x 47 x 44"),
        ("Secundário", "1 tira de Cu 2 x 9 mm; 2,5 voltas; passo 12,8"),
        ("Ponta", "tubo de Cu 4,5 x 0,75; de X 34 a X 96,1"),
        ("Massa", "não informada — CAD sem densidade por material"),
    ]
    for i, (k, v) in enumerate(dados):
        y = 378 - i * 5.6
        d.text(22, y, TXT_SM, k, "TEXTO")
        d.text(100, y, TXT_SM, v, "TEXTO")
    d.line(22, 384, 306, 384, "TABELA")

    # vistas (1º diedro): frontal no alto, superior abaixo, lateral esquerda à direita
    VF = (60, 130)                     # canto inferior esquerdo da vista frontal
    place("frente", *VF)
    place("topo", VF[0], 78)           # 1º diedro: superior abaixo da frontal
    place("lado", VF[0] + sizes["frente"][0] + 41, VF[1])
    place("iso", 235, VF[1])

    # rótulos das vistas (abaixo de cada vista)
    d.text(VF[0], 121, TXT, "VISTA FRONTAL", "TEXTO")
    d.text(VF[0], 69, TXT, "VISTA SUPERIOR", "TEXTO")
    d.text(VF[0] + sizes["frente"][0] + 41, 121, TXT, "VISTA LATERAL ESQ.", "TEXTO")
    d.text(235, 119, TXT, "PERSPECTIVA", "TEXTO")

    # detalhe 1:1 do conjunto magnético (exportado com o resto oculto)
    place("detalhe", 380, 108, scale=1.0)
    d.text(380, 100, TXT, "DETALHE A — CONJUNTO MAGNÉTICO (ESCALA 1:1)", "TEXTO")
    d.text(380, 93, TXT_SM, "Núcleo EI-75, carretel com primário, secundário e cantoneiras", "TEXTO")

    # cotas de envelope (escala 1:2)
    fw, fh = sizes["frente"]
    dim_h(d, VF[0], VF[0] + fw, VF[1] + fh + 9, VF[1] + fh + 12, "148,3")
    dim_v(d, VF[1], VF[1] + fh, VF[0] - 14, VF[0] - 20, "312,7")
    tw, th = sizes["topo"]
    dim_v(d, 78, 78 + th, VF[0] - 14, VF[0] - 20, "52,3")

    # carimbo (canto inferior direito)
    tb_w, tb_h = 180.0, 66.0
    tx0, ty0 = SHEET_W - MARGIN - tb_w, MARGIN
    d.rect(tx0, ty0, tx0 + tb_w, ty0 + tb_h, "TABELA")
    for y in (ty0 + 44, ty0 + 32, ty0 + 22, ty0 + 11):
        d.line(tx0, y, tx0 + tb_w, y, "TABELA")
    d.line(tx0 + 96, ty0, tx0 + 96, ty0 + 32, "TABELA")

    d.text(tx0 + 4, ty0 + 52, 7.0, "PS-001  PISTOLA DE SOLDA", "TEXTO")
    d.text(tx0 + 4, ty0 + 47, 2.2, "ESTANHADOR 550 W / 127 V — ESTUDO DE MODELAGEM", "TEXTO")
    d.text(tx0 + 4, ty0 + 35, 6.0, "CONJUNTO GERAL", "TEXTO")
    d.text(tx0 + 4, ty0 + 26, TXT_SM, "PROJEÇÃO 1º DIEDRO · COTAS EM mm", "TEXTO")
    d.text(tx0 + 4, ty0 + 15, TXT_SM, "DOC PS-001-DR-001", "TEXTO")
    d.text(tx0 + 4, ty0 + 5, TXT_SM, "FOLHA A2 · DATA 2026-11-14", "TEXTO")
    d.text(tx0 + 100, ty0 + 24, 6.0, "ESCALA 1:2", "TEXTO")
    d.text(tx0 + 100, ty0 + 14, TXT_SM, "REV. A", "TEXTO")
    d.text(tx0 + 100, ty0 + 5, TXT_SM, "1 DE 1", "TEXTO")

    # aviso no rodapé esquerdo
    d.text(20, 20, TXT, "ESTUDO — NÃO É DESENHO DE FABRICAÇÃO", "TEXTO")
    d.text(20, 14, TXT_SM, "Licença CC BY-NC-SA 4.0 · modelo: cad/solidcraft/PS-001.sc (v0.15.0) · ver LEGAL.md", "TEXTO")

    # BOM (canto superior direito)
    rows = list(csv.DictReader(open(BOM)))
    bx, by = 340.0, 300.0
    cols = [0, 12, 44, 196, 216]      # item | código | descrição | qtd
    rh = 5.6
    d.text(bx, by + rh * (len(rows) + 2) + 3.2, TXT, "LISTA DE MATERIAIS (PS-001-LM-001)", "TEXTO")
    header = ["ITEM", "CÓDIGO", "DESCRIÇÃO", "QTD"]
    for i in range(len(cols)):
        d.line(bx + cols[i], by, bx + cols[i], by + rh * (len(rows) + 2), "TABELA")
    for r in range(len(rows) + 2):
        y = by + r * rh
        d.line(bx, y, bx + cols[-1], y, "TABELA")
    yh = by + (len(rows) + 1) * rh
    for i, h in enumerate(header):
        d.text(bx + cols[i] + 1.5, yh + 1.4, TXT_SM, h, "TEXTO")
    for r, row in enumerate(rows):
        y = yh - (r + 1) * rh + 1.4
        d.text(bx + cols[0] + 1.5, y, TXT_SM, row["item"], "TEXTO")
        d.text(bx + cols[1] + 1.5, y, TXT_SM, row["codigo"], "TEXTO")
        d.text(bx + cols[2] + 1.5, y, TXT_SM, row["descricao"], "TEXTO")
        d.text(bx + cols[3] + 1.5, y, TXT_SM, row["qtd"], "TEXTO")

    # notas
    notas = [
        "NOTAS",
        "1. Modelo 3D paramétrico: cad/solidcraft/PS-001.sc (tag v0.15.0, 22 corpos).",
        "2. Vistas obtidas por projeção do modelo; escala 1:2, cotas em mm.",
        "3. Material, dimensões e volumes de cada item: PS-001-LM-001 (BOM.csv).",
        "4. Detalhe A: conjunto magnético ampliado a 1:1, a partir da vista frontal.",
        "5. Linhas ocultas omitidas; vistas sem corte.",
        "6. Sequência de montagem em PS-001-CO-001; uso e segurança em PS-001-US-001.",
        "7. Estudo sem certificação: não é instrução de fabricação. Ver LEGAL.md.",
    ]
    for i, t in enumerate(notas):
        d.text(340, 288 - i * 6.4, TXT if i == 0 else TXT_SM, t, "TEXTO")

    d.write(OUT)
    print("escrito:", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
