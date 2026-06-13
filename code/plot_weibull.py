import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import weibull_min

x = np.linspace(0, 5, 200)

plt.figure(figsize=(5, 3))
plt.plot(x, weibull_min.pdf(x, c=1.5, scale=1.0), 'b-', lw=2, label=r'$\beta=1.5$ (Desgaste inicial)')
plt.plot(x, weibull_min.pdf(x, c=3.0, scale=1.0), 'r-', lw=2, label=r'$\beta=3.0$ (Desgaste avançado)')
plt.title("Distribuição Weibull (Comparação Visual)")
plt.xlabel("Tempo")
plt.ylabel("Densidade de Probabilidade (PDF)")
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('C:/Users/Felipe Costa/Downloads/BACKUP/Downloads/TCC_1_FELIPE_COSTA_LOPES-master/confiabilidade/code/resultados/figuras/weibull_generica.png', dpi=150)
