import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

# Pasta para salvar
pasta_salvar = r"c:\Users\Felipe Costa\Downloads\BACKUP\Downloads\TCC_1_FELIPE_COSTA_LOPES-master\confiabilidade\code\resultados\figuras"
os.makedirs(pasta_salvar, exist_ok=True)

plt.rcParams.update({"font.size": 12, "figure.dpi": 110})

# 1. Curva Teórica de Degradação
def plot_curva_teorica():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    tau = np.linspace(0, 3000, 100)
    D0 = 0.43
    Dmax = 0.57
    L = 0.50
    rho = np.log(Dmax/D0)/3000.0
    
    # 3 curvas
    D_mediana = D0 * np.exp(rho * tau)
    D_rapida = 0.41 * np.exp((rho * 1.5) * tau)
    D_lenta = 0.44 * np.exp((rho * 0.5) * tau)
    
    ax.plot(tau, D_mediana, label="taxa média", color="blue", lw=2)
    ax.plot(tau, D_rapida, label="rápida", color="red", lw=2)
    ax.plot(tau, D_lenta, label="lenta", color="green", lw=2)
    
    ax.axhline(L, color="black", ls="--", label="Limiar L (Falha)")
    ax.axvline(3000, color="gray", ls=":", label=r"Horizonte ($\tau_{max}$)")
    
    ax.set_xlabel(r"Tempo $\tau$ [h]")
    ax.set_ylabel("Degradação D")
    ax.set_xlim(0, 3200)
    ax.set_ylim(0.35, 0.65)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title("Evolução Teórica da Degradação")
    
    fig.tight_layout()
    fig.savefig(os.path.join(pasta_salvar, "curva_teorica.png"))
    plt.close()

# 2. Weibull Genérica
def plot_weibull_generica():
    from scipy.stats import weibull_min
    
    fig, ax = plt.subplots(figsize=(6, 3.5))
    x = np.linspace(0.1, 3, 200)
    
    y_infantil = weibull_min.pdf(x, 0.5, scale=1) # beta < 1
    y_constante = weibull_min.pdf(x, 1, scale=1)  # beta = 1
    y_desgaste = weibull_min.pdf(x, 3, scale=1)   # beta > 1
    
    ax.plot(x, y_infantil, color="green", label=r"$\beta < 1$ (Infantil)", lw=2)
    ax.plot(x, y_constante, color="gray", label=r"$\beta \approx 1$ (Constante)", lw=2)
    ax.plot(x, y_desgaste, color="red", label=r"$\beta > 1$ (Desgaste)", lw=2)
    
    ax.set_ylim(0, 2)
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Densidade de Falha f(t)")
    ax.set_title("Formas da Distribuição Weibull")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    fig.savefig(os.path.join(pasta_salvar, "weibull_generica.png"))
    plt.close()

plot_curva_teorica()
plot_weibull_generica()
print("Gráficos extras gerados.")
