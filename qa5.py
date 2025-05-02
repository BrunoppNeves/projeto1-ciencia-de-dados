import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Lendo os dados do arquivo CSV (substitua pelo caminho do seu arquivo)
# Exemplo: 'microdados_enem.csv' ou o caminho completo do seu arquivo
df = pd.read_csv('MICRODADOS_ENEM_2023.csv', sep=';', encoding='latin1')

# Mapeando os códigos para as cores das provas, incluindo reaplicações e versões adaptadas
mapa_cores = {
    1191: 'Azul',
    1192: 'Amarela',
    1193: 'Branca',
    1194: 'Rosa',
    1195: 'Rosa - Ampliada',
    1196: 'Rosa - Superampliada',
    1197: 'Laranja - Braile',
    1198: 'Laranja - Adaptada Ledor',
    1199: 'Verde - Videoprova - Libras',
    1271: 'Azul (Reaplicação)',
    1272: 'Amarela (Reaplicação)',
    1273: 'Branca (Reaplicação)',
    1274: 'Rosa (Reaplicação)'
}

# Filtrando apenas os códigos de prova de Ciências Humanas relevantes
df_ch = df[df['CO_PROVA_CH'].isin(mapa_cores.keys())].copy()

# Mapeando o nome da cor da prova
df_ch['COR_PROVA'] = df_ch['CO_PROVA_CH'].map(mapa_cores)

# Removendo notas ausentes
df_ch = df_ch[['NU_NOTA_CH', 'COR_PROVA']].dropna()

# Plotando o boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_ch, x='COR_PROVA', y='NU_NOTA_CH', palette='pastel')
plt.xticks(rotation=45)
plt.title('Distribuição das Notas de Ciências Humanas por Cor da Prova')
plt.xlabel('Cor da Prova')
plt.ylabel('Nota de Ciências Humanas (NU_NOTA_CH)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Calculando e imprimindo as médias por cor
medias = df_ch.groupby('COR_PROVA')['NU_NOTA_CH'].mean().sort_values()
print("Média de notas por cor de prova:")
print(medias)
