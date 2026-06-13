import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 3000, 400)
D0 = 0.43
rho_mean = 9.4e-5
D_mean = D0 * np.exp(rho_mean * t)

plt.figure(figsize=(6, 4))
plt.plot(t, D_mean, 'b-', lw=2, label=r'Trajetória Média ($\bar{\rho}$)')

# Some sample paths
for rho in [11.5e-5, 5.71e-5, 2.83e-5]:
    plt.plot(t, D0 * np.exp(rho * t), '--', alpha=0.6, label=rf'Trajetória sorteada ($\rho={rho:.2e}$)')

plt.axhline(0.50, color='r', linestyle=':', lw=2, label='Limiar L (0,50)')
plt.axvline(3000, color='k', linestyle=':', label=r'$\tau_{max}$ (3000 h)')

plt.xlabel(r'Tempo $\tau$ [h]')
plt.ylabel(r'Degradação $D(\tau)$ [g]')
plt.title(r'Curva de Degradação $D(\tau) = D_0 e^{\rho \tau}$')
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('exemplo_curva.png', dpi=150)
