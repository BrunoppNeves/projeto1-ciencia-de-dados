import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações
sns.set(style="whitegrid")

# Leitura do CSV
arquivo_csv = 'MICRODADOS_ENEM_2023.csv'
df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')

# Filtragem de dados válidos
df = df.drop_duplicates()
df = df[df['NU_NOTA_CH'].notnull()]
df = df[df['TP_DEPENDENCIA_ADM_ESC'].notnull()]

# Mapeamento das categorias da escola
mapa_dependencia = {
    1: 'Federal',
    2: 'Estadual',
    3: 'Municipal',
    4: 'Privada'
}
df['TIPO_ESCOLA'] = df['TP_DEPENDENCIA_ADM_ESC'].map(mapa_dependencia)

# Gráfico
plt.figure(figsize=(10, 6))
sns.barplot(x='TIPO_ESCOLA', y='NU_NOTA_CH', data=df, estimator='mean', palette='Set2')
plt.title('Média da Nota de Ciências Humanas por Tipo de Escola')
plt.xlabel('Tipo de Escola')
plt.ylabel('Média da Nota em Ciências Humanas')
plt.tight_layout()
plt.show()
