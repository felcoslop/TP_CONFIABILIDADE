# -*- coding: utf-8 -*-
"""
Gera o Diagrama de Blocos de Confiabilidade (DBC) das tres configuracoes
avaliadas no passo 6 (sistema.py): serie, paralelo ativo e standby a frio.

E uma figura puramente ilustrativa (nao usa dados); serve para o relatorio
deixar claro o que significam as tres topologias antes da simulacao de
Monte Carlo. Salva em resultados/figuras/p6_diagrama_blocos.png.

A "unidade" base e um par de 2 rolamentos em serie (ambos necessarios). Por
isso o paralelo e o standby mostram DOIS pares R1/R2: cada fileira e uma
unidade completa, e a redundancia duplica a unidade inteira (Unidade A e B).
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import config

AZUL = "#4C72B0"
CINZA = "#B7B7B7"

W, H = 1.4, 0.62           # largura e altura do bloco
COL1, COL2 = 2.4, 4.1      # centros horizontais dos dois rolamentos
LBUS, RBUS = 0.9, 5.0      # barras verticais de bifurcacao (entrada/saida)
XIN, XOUT = 0.3, 5.7       # nos de entrada e saida
TOP, BOT, MID = 1.15, 0.05, 0.60   # alturas das fileiras e do eixo central


def _bloco(ax, xc, yc, texto, cor=AZUL, alpha=1.0):
    ax.add_patch(FancyBboxPatch((xc - W / 2, yc - H / 2), W, H,
                 boxstyle="round,pad=0.02,rounding_size=0.08",
                 linewidth=1.5, edgecolor="black", facecolor=cor, alpha=alpha))
    ax.text(xc, yc, texto, ha="center", va="center", fontsize=11,
            color="white" if alpha > 0.6 else "black")


def _l(ax, x0, y0, x1, y1, dashed=False):
    ax.plot([x0, x1], [y0, y1], color="black", lw=1.4, zorder=1,
            ls="--" if dashed else "-")


def _no(ax, x, y):
    ax.plot([x], [y], "o", color="black", ms=5, zorder=3)


def _fileira(ax, yc, cor, alpha, r_esq, r_dir, dashed=False):
    """Desenha um par de rolamentos em serie (uma unidade) na altura yc.
    r_esq e r_dir sao os rotulos dos dois rolamentos (ex.: R1 e R2)."""
    _bloco(ax, COL1, yc, r_esq, cor=cor, alpha=alpha)
    _bloco(ax, COL2, yc, r_dir, cor=cor, alpha=alpha)
    _l(ax, COL1 + W / 2, yc, COL2 - W / 2, yc, dashed)


def gerar():
    fig, axs = plt.subplots(3, 1, figsize=(7.4, 8.2))

    # ---------------- (a) SERIE: 1 unidade (2 rolamentos em serie) -----------
    ax = axs[0]
    ax.set_title("(a) Série — 1 unidade (2 rolamentos em série, sem redundância)",
                 fontsize=10, loc="left")
    _no(ax, XIN, MID); _no(ax, XOUT, MID)
    _bloco(ax, COL1, MID, r"Rolamento 1")
    _bloco(ax, COL2, MID, r"Rolamento 2")
    _l(ax, XIN, MID, COL1 - W / 2, MID)
    _l(ax, COL1 + W / 2, MID, COL2 - W / 2, MID)
    _l(ax, COL2 + W / 2, MID, XOUT, MID)
    ax.text(3.0, 1.85, r"$t_{\mathrm{sis}}=\min(t_1,t_2)$  —  cai quando o 1º rolamento falha",
            ha="center", fontsize=9)

    # ---------------- (b) PARALELO ativo: 2 unidades, basta uma -------------
    ax = axs[1]
    ax.set_title("(b) Paralelo ativo — 2 unidades operando juntas: basta uma de pé",
                 fontsize=10, loc="left")
    _no(ax, XIN, MID); _no(ax, XOUT, MID)
    _fileira(ax, TOP, AZUL, 1.0, r"R$_1$", r"R$_2$")
    _fileira(ax, BOT, AZUL, 1.0, r"R$_3$", r"R$_4$")
    # entrada: no -> barra que sobe/desce -> cada unidade
    _l(ax, XIN, MID, LBUS, MID)
    _l(ax, LBUS, BOT, LBUS, TOP)
    _l(ax, LBUS, TOP, COL1 - W / 2, TOP)
    _l(ax, LBUS, BOT, COL1 - W / 2, BOT)
    # saida: cada unidade -> barra -> no
    _l(ax, COL2 + W / 2, TOP, RBUS, TOP)
    _l(ax, COL2 + W / 2, BOT, RBUS, BOT)
    _l(ax, RBUS, BOT, RBUS, TOP)
    _l(ax, RBUS, MID, XOUT, MID)
    ax.text(3.25, TOP + 0.5, "Unidade A (par em série)", ha="center", fontsize=8, color="#33415c")
    ax.text(3.25, BOT - 0.5, "Unidade B (par em série)", ha="center", fontsize=8, color="#33415c")
    ax.text(3.0, 1.95, r"$t_{\mathrm{sis}}=\max(t_A,t_B)$  —  só cai quando as DUAS unidades falham",
            ha="center", fontsize=9)

    # ---------------- (c) STANDBY a frio: 1 ativa + 1 reserva --------------
    ax = axs[2]
    ax.set_title("(c) Standby a frio — 1 unidade ativa + reserva que só entra após a falha",
                 fontsize=10, loc="left")
    _no(ax, XIN, MID); _no(ax, XOUT, MID)
    _fileira(ax, TOP, AZUL, 1.0, r"R$_1$", r"R$_2$")                 # ativa (solida)
    _fileira(ax, BOT, CINZA, 0.5, r"R$_3$", r"R$_4$", dashed=True)   # reserva
    # chave seletora na entrada
    xsw = 0.6
    _l(ax, XIN, MID, xsw, MID)
    ax.plot([xsw], [MID], "s", color="black", ms=8, zorder=3)
    _l(ax, xsw, MID, xsw, TOP); _l(ax, xsw, TOP, COL1 - W / 2, TOP)          # -> ativa
    _l(ax, xsw, MID, xsw, BOT, dashed=True)
    _l(ax, xsw, BOT, COL1 - W / 2, BOT, dashed=True)                         # -> reserva
    ax.text(xsw, MID - 0.95, "chave", ha="center", fontsize=8)
    # saida
    _l(ax, COL2 + W / 2, TOP, RBUS, TOP); _l(ax, RBUS, MID, RBUS, TOP)
    _l(ax, COL2 + W / 2, BOT, RBUS, BOT, dashed=True)
    _l(ax, RBUS, BOT, RBUS, MID, dashed=True)
    _l(ax, RBUS, MID, XOUT, MID)
    ax.text(3.25, TOP + 0.5, "Unidade A (ativa)", ha="center", fontsize=8, color="#33415c")
    ax.text(3.25, BOT - 0.5, "Unidade B (reserva fria)", ha="center", fontsize=8, color="gray")
    ax.text(3.0, 1.95, r"$t_{\mathrm{sis}}=t_A+t_B$  —  soma as vidas das duas unidades",
            ha="center", fontsize=9)

    for ax in axs:
        ax.set_xlim(-0.1, 6.1)
        ax.set_ylim(-0.95, 2.3)
        ax.axis("off")

    fig.suptitle("Diagrama de Blocos de Confiabilidade — sistema hipotético de rolamentos\n"
                 "(cada unidade = par de 2 rolamentos em série; a redundância duplica a unidade)",
                 fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    cam = os.path.join(config.SAIDA_FIG, "p6_diagrama_blocos.png")
    fig.savefig(cam, dpi=130)
    plt.close(fig)
    print("salvo:", cam)
    return cam


if __name__ == "__main__":
    gerar()
