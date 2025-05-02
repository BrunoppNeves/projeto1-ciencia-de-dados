import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Carregando os dados
df = pd.read_csv("MICRODADOS_ENEM_2023.csv", sep=';', encoding='latin1')

# Selecionando as colunas de interesse e removendo valores ausentes
df_filtrado = df[['NU_NOTA_MT', 'NU_NOTA_CN']].dropna()

# Removendo notas zero (provavelmente ausências ou anulações)
df_limpo = df_filtrado[(df_filtrado['NU_NOTA_MT'] > 0) & (df_filtrado['NU_NOTA_CN'] > 0)]

# Gráfico de dispersão com linha de tendência
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_limpo, x='NU_NOTA_MT', y='NU_NOTA_CN', alpha=0.4, edgecolor=None)
sns.regplot(data=df_limpo, x='NU_NOTA_MT', y='NU_NOTA_CN', scatter=False, color='red', label='Tendência linear')
plt.title('Correlação entre notas de Matemática e Ciências da Natureza (com dados limpos)')
plt.xlabel('Nota de Matemática (NU_NOTA_MT)')
plt.ylabel('Nota de Ciências da Natureza (NU_NOTA_CN)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Correlação com dados limpos
corr_limpo, p_limpo = pearsonr(df_limpo['NU_NOTA_MT'], df_limpo['NU_NOTA_CN'])
print("Com dados limpos (sem zeros):")
print(f"  Correlação de Pearson: {corr_limpo:.4f}")
print(f"  Valor-p: {p_limpo:.2e}")

# (Opcional) Correlação com dados originais, incluindo zeros
corr_todos, p_todos = pearsonr(df_filtrado['NU_NOTA_MT'], df_filtrado['NU_NOTA_CN'])
print("\nCom todos os dados (incluindo zeros):")
print(f"  Correlação de Pearson: {corr_todos:.4f}")
print(f"  Valor-p: {p_todos:.2e}")
