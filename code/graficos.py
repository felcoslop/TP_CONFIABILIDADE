# -*- coding: utf-8 -*-
"""
Todas as funcoes de plotagem ficam aqui pra manter os passos limpos.
Backend Agg (nao abre janela, so salva PNG).
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

import config

plt.rcParams.update({"font.size": 12, "figure.dpi": 110})


def _salvar(fig, nome):
    """Salva a figura na pasta de figuras e fecha."""
    cam = os.path.join(config.SAIDA_FIG, nome)
    fig.tight_layout()
    fig.savefig(cam)
    plt.close(fig)
    return cam


# =============================================================================
# Passo 1 - assinatura de degradacao (indicador vs tempo)
# =============================================================================
def fig_assinatura_pronostia(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Plota a curva de degradacao de cada rolamento
    for rolamento, dados in df.groupby("rolamento"):
        ax.plot(dados["tempo_horas"], dados["rms"], alpha=0.6, label=rolamento)
        
    ax.set_ylabel("RMS na banda [g]")
    ax.set_xlabel("Tempo de operação [horas]")
    ax.set_title("Evolução da Degradação - PRONOSTIA (17 rolamentos)")
    ax.grid(True, alpha=0.3)
    
    # Colocar legenda fora do grafico para nao poluir
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=8, ncol=1)
    
    # Ajusta bordas para caber a legenda
    fig.subplots_adjust(right=0.75)
    
    return _salvar(fig, "p1_assinatura_pronostia_all.png")


# =============================================================================
# Passo 2 - distribuicao dos TTF construidos (com censura)
# =============================================================================
def fig_ttf_hist(modo, falhas, n_censura, L, horizonte):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(falhas, bins=30, color="#4C72B0", alpha=0.85, label="falhas")
    if n_censura > 0:
        ax.axvline(horizonte, color="red", ls="--",
                   label="horizonte / %d censuras" % n_censura)
    ax.set_xlabel("tempo ate a falha  [h]")
    ax.set_ylabel("frequencia")
    pct = 100 * n_censura / (len(falhas) + n_censura)
    ax.set_title("TTF construidos - %s  (censura: %.0f%%)" % (modo["nome"], pct))
    ax.legend()
    ax.grid(True, alpha=0.3)
    return _salvar(fig, "p2_ttf_%s.png" % modo["id"])


# =============================================================================
# Passo 3 - papel de probabilidade Weibull e comparacao de CDFs
# =============================================================================
def fig_papel_weibull(modo, pares_mr, beta, eta):
    t = np.array([p[0] for p in pares_mr])
    F = np.array([p[1] for p in pares_mr])
    x = np.log(t)
    y = np.log(-np.log(1 - F))           # linearizacao da Weibull
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(x, y, color="k", zorder=3, label="dados (median rank)")
    xx = np.linspace(x.min(), x.max(), 50)
    ax.plot(xx, beta * (xx - np.log(eta)), "r-",
            label=r"ajuste: $\beta$=%.2f, $\eta$=%.0f h" % (beta, eta))
    ax.set_xlabel(r"$\ln(t)$")
    ax.set_ylabel(r"$\ln(-\ln(1-F))$")
    ax.set_title("Papel de probabilidade Weibull - %s" % modo["nome"])
    ax.legend()
    ax.grid(True, alpha=0.3)
    return _salvar(fig, "p3_weibull_%s.png" % modo["id"])


def fig_ajuste_cdf(modo, pares_mr, distribuicoes, tmax, n_falhas=None, n_total=None):
    t = np.array([p[0] for p in pares_mr])
    F = np.array([p[1] for p in pares_mr])
    # estende o eixo x ate onde a melhor distribuicao chega a F=0.95
    # para mostrar a curva completa mesmo quando ha muita censura
    try:
        dist_ref = list(distribuicoes.values())[0]
        tmax_ext = max(tmax, float(dist_ref.quantile(0.95)))
    except Exception:
        tmax_ext = tmax * 2
    tt = np.linspace(1, tmax_ext, 600)
    fig, ax = plt.subplots(figsize=(8, 5))
    # pontos empiricos: so existem para as falhas observadas (nao para as censuradas)
    pct_cens = 0
    if n_falhas is not None and n_total is not None:
        pct_cens = 100.0 * (n_total - n_falhas) / n_total
        label_emp = (u"empírica (median rank)\n"
                     u"%.0f%% censura → pontos vão até F≈%.2f"
                     % (pct_cens, F.max()))
    else:
        label_emp = u"empírica (median rank)"
    ax.scatter(t, F, color="k", s=18, zorder=4, label=label_emp)
    # linha pontilhada vertical no ultimo TTF observado para deixar claro o limite
    ax.axvline(t.max(), color="gray", ls=":", lw=1, alpha=0.7,
               label=u"último TTF observado (%.0f h)" % t.max())
    cores = {"Weibull": "#C44E52", "Exponencial": "#55A868", "Lognormal": "#4C72B0"}
    for nome, dist in distribuicoes.items():
        # show_plot=False: so queremos os valores; sem isso a 'reliability'
        # plota sozinha a curva + banda de IC propria (em cor trocada).
        ax.plot(tt, dist.CDF(tt, show_plot=False), color=cores.get(nome),
                label=nome, lw=2)
    ax.set_xlabel("t  [h]")
    ax.set_ylabel("F(t)  —  probabilidade acumulada de falha")
    ax.set_title(u"Ajuste das distribuições - %s" % modo["nome"])
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    return _salvar(fig, "p3_cdf_%s.png" % modo["id"])


# =============================================================================
# Passo 4 - histogramas do bootstrap
# =============================================================================
def fig_bootstrap(modo, amostras, rotulos, ics):
    fig, axs = plt.subplots(1, len(amostras), figsize=(11, 4.2))
    if len(amostras) == 1:
        axs = [axs]
    for ax, am, rot, ic in zip(axs, amostras, rotulos, ics):
        ax.hist(am, bins=40, color="#8172B3", alpha=0.85)
        ax.axvline(ic[0], color="k", ls="--")
        ax.axvline(ic[1], color="k", ls="--")
        ax.set_title("%s\nIC95%% = [%.3g, %.3g]" % (rot, ic[0], ic[1]))
        ax.grid(True, alpha=0.3)
    fig.suptitle("Bootstrap dos parametros - %s" % modo["nome"])
    return _salvar(fig, "p4_bootstrap_%s.png" % modo["id"])


# =============================================================================
# Passo 5 - indices R(t), h(t), f(t) e R(t) com banda de confianca
# =============================================================================
def fig_indices(modo, dist, tmax):
    tt = np.linspace(1, tmax, 400)
    fig, axs = plt.subplots(1, 3, figsize=(13, 4))
    axs[0].plot(tt, dist.SF(tt, show_plot=False), "#4C72B0"); axs[0].set_title("R(t)")
    axs[1].plot(tt, dist.HF(tt, show_plot=False), "#C44E52"); axs[1].set_title("h(t) - taxa de falha")
    axs[2].plot(tt, dist.PDF(tt, show_plot=False), "#55A868"); axs[2].set_title("f(t)")
    for ax in axs:
        ax.set_xlabel("t  [h]"); ax.grid(True, alpha=0.3)
    fig.suptitle("Indices de confiabilidade - %s" % modo["nome"])
    return _salvar(fig, "p5_indices_%s.png" % modo["id"])


def fig_R_banda(modo, t, R, R_lo, R_hi):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, R, "b-", label="R(t)")
    ax.fill_between(t, R_lo, R_hi, color="b", alpha=0.2, label="IC 95% (bootstrap)")
    ax.set_xlabel("t  [h]"); ax.set_ylabel("R(t)")
    ax.set_ylim(0, 1)
    ax.set_title("Confiabilidade com banda de confianca - %s" % modo["nome"])
    ax.legend(); ax.grid(True, alpha=0.3)
    return _salvar(fig, "p5_R_banda_%s.png" % modo["id"])


# =============================================================================
# Passo 6 - sistema
# =============================================================================
def fig_sistema_R(t, curvas):
    fig, ax = plt.subplots(figsize=(8, 5))
    estilos = {"Serie": "-", "Paralelo": "--", "Standby": "-."}
    for nome, R in curvas.items():
        ax.plot(t, R, estilos.get(nome, "-"), label=nome, lw=2)
    ax.set_xlabel("t  [h]"); ax.set_ylabel("R do sistema")
    ax.set_ylim(0, 1)
    ax.set_title("Confiabilidade do sistema (2 rolamentos PRONOSTIA em série/paralelo)")
    ax.legend(); ax.grid(True, alpha=0.3)
    return _salvar(fig, "p6_sistema_R.png")


def fig_disponibilidade(nomes, A_analitico, A_mc):
    x = np.arange(len(nomes))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(x - 0.2, A_analitico, 0.4, label="analitico", color="#4C72B0")
    # so plota as barras de MC que existem (standby nao e simulado -> NaN)
    xm = [xi + 0.2 for xi, a in zip(x, A_mc) if not np.isnan(a)]
    ym = [a for a in A_mc if not np.isnan(a)]
    ax.bar(xm, ym, 0.4, label="Monte Carlo", color="#C44E52")
    ax.set_xticks(x); ax.set_xticklabels(nomes)
    ax.set_ylabel("Disponibilidade A")
    validos = A_analitico + ym
    ax.set_ylim(min(validos) - 0.01, 1.0)
    ax.set_title("Disponibilidade por configuracao")
    ax.legend(); ax.grid(True, axis="y", alpha=0.3)
    return _salvar(fig, "p6_disponibilidade.png")


# =============================================================================
# Resumo geral
# =============================================================================
def fig_resumo(nomes, mttfs, betas):
    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    x = np.arange(len(nomes))
    ax1.bar(x, mttfs, color="#4C72B0", alpha=0.8)
    ax1.set_ylabel("MTTF  [h]", color="#4C72B0")
    ax1.set_xticks(x); ax1.set_xticklabels(nomes, rotation=30, ha="right")
    ax2 = ax1.twinx()
    ax2.plot(x, betas, "ro-", label=r"$\beta$ Weibull")
    ax2.axhline(1.0, color="gray", ls=":", lw=1)
    ax2.set_ylabel(r"$\beta$ (forma Weibull)", color="r")
    ax1.set_title("Resumo: MTTF e forma da falha por modo")
    return _salvar(fig, "resumo_modos.png")


# =============================================================================
# Figuras combinadas (todos os modos juntos)
# =============================================================================
def fig_rt_todos(modos_nomes, dists_dict, tmax_h=8000):
    """R(t) de todos os modos num so grafico — facil de comparar."""
    tt = np.linspace(1, tmax_h, 600)
    cores = ["#4C72B0", "#C44E52", "#55A868", "#8172B3"]
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, (nome, dist) in enumerate(dists_dict.items()):
        ax.plot(tt, dist.SF(tt, show_plot=False), color=cores[i % len(cores)],
                lw=2, label=nome)
    ax.axhline(0.9, color="gray", ls=":", lw=1, label="R=0,90")
    ax.axhline(0.5, color="gray", ls="--", lw=1, label="R=0,50 (mediana)")
    ax.set_xlabel("t  [h]  —  tempo de operacao acumulada")
    ax.set_ylabel("R(t)  —  probabilidade de nao ter falhado ate t")
    ax.set_ylim(0, 1)
    ax.set_title(u"Confiabilidade R(t) por modo de falha\n"
                 u"(quanto mais a curva se afasta para a direita, mais duravel o equipamento)")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    return _salvar(fig, "comparacao_Rt_modos.png")


def fig_ht_todos(modos_nomes, dists_dict, tmax_h=8000):
    """h(t) de todos os modos: mostra o estagio na curva da banheira."""
    tt = np.linspace(10, tmax_h, 600)
    cores = ["#4C72B0", "#C44E52", "#55A868", "#8172B3"]
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, (nome, dist) in enumerate(dists_dict.items()):
        ht = dist.HF(tt, show_plot=False)
        ax.plot(tt, ht, color=cores[i % len(cores)], lw=2, label=nome)
    ax.set_xlabel("t  [h]  —  tempo de operacao acumulada")
    ax.set_ylabel(u"h(t)  —  taxa instantanea de falha [1/h]")
    ax.set_title(u"Taxa de falha h(t) por modo\n"
                 u"(taxa crescente = desgaste; taxa constante = vida útil; decrescente = mortalidade infantil)")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    return _salvar(fig, "comparacao_ht_modos.png")


def fig_banheira_esquema():
    """Figura esquematica da curva da banheira com anotacoes dos modos."""
    t = np.linspace(0, 100, 500)
    # curva banheira = mortalidade infantil + vida util + desgaste
    h = (2.0 * np.exp(-0.08 * t)          # mortalidade infantil
         + 0.15                            # taxa base (vida util)
         + 0.0008 * t**1.5)               # desgaste
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(t, h, "k-", lw=3)
    ax.fill_between(t[:120], h[:120], alpha=0.15, color="#C44E52",
                    label=u"Mortalidade infantil (β<1)")
    ax.fill_between(t[120:300], h[120:300], alpha=0.15, color="#55A868",
                    label=u"Vida útil / taxa constante (β≈1)")
    ax.fill_between(t[300:], h[300:], alpha=0.15, color="#4C72B0",
                    label=u"Desgaste (β>1)")
    ax.annotate(u"Desgaste Natural\n(PRONOSTIA)",
                xy=(88, h[440]), xytext=(60, h[440] + 2.0),
                arrowprops=dict(arrowstyle="->"), fontsize=10, color="#4C72B0")
    ax.set_xlabel(u"Tempo de operação  (escala relativa)")
    ax.set_ylabel(u"Taxa de falha h(t)")
    ax.set_title(u"Curva da banheira: posicionamento do desgaste\n"
                 u"(baseado no parâmetro β da distribuição Weibull ajustada)")
    ax.legend(fontsize=9, loc="upper right")
    ax.set_ylim(0, None)
    ax.grid(True, alpha=0.3)
    return _salvar(fig, "curva_banheira.png")
