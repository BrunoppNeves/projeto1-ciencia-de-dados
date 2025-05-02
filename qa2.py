import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações
sns.set(style="whitegrid")

# Leitura
arquivo_csv = 'MICRODADOS_ENEM_2023.csv'
df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')

# Limpeza e filtragem
df = df.drop_duplicates()
df = df[df['NU_NOTA_CH'].notnull()]
df = df[df['Q024'].notnull()]

# Mapeando Q024 para facilitar leitura
mapa_q024 = {
    'A': 'Não tem computador',
    'B': 'Sim, um',
    'C': 'Sim, dois ou mais'
}
df['TEM_COMPUTADOR'] = df['Q024'].map(mapa_q024)

# Gerar gráfico
plt.figure(figsize=(10, 6))
sns.barplot(x='TEM_COMPUTADOR', y='NU_NOTA_CH', data=df, estimator='mean', palette='pastel')
plt.title('Média da Nota de Ciências Humanas por Acesso a Computador em Casa')
plt.xlabel('Acesso a Computador')
plt.ylabel('Média da Nota em Ciências Humanas')
plt.tight_layout()
plt.show()
