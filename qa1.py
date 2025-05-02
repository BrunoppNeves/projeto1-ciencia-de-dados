import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações
sns.set(style="whitegrid")
pd.set_option('display.max_columns', 100)

# Leitura dos dados
arquivo_csv = 'MICRODADOS_ENEM_2023.csv'
df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')

# Conversão da coluna Q005 para numérica
df['Q005'] = pd.to_numeric(df['Q005'], errors='coerce')

# Filtragem básica
df = df.drop_duplicates()
df = df[df['NU_NOTA_CH'].notnull()]
df = df[df['Q005'].notnull()]

# Gráfico
plt.figure(figsize=(14, 6))
sns.barplot(x='Q005', y='NU_NOTA_CH', data=df, estimator='mean', palette='viridis')
plt.title('Média da Nota de Ciências Humanas por Nº de Pessoas na Casa')
plt.xlabel('Nº de Pessoas na Casa (Q005)')
plt.ylabel('Média da Nota em Ciências Humanas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
