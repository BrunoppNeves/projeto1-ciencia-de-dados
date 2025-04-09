import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurações iniciais
plt.style.use('ggplot')
sns.set_palette('pastel')

# 1. Carregar e preparar os dados
try:
    df = pd.read_csv('MICRODADOS_ENEM_2023.csv', sep=';', encoding='latin-1',
                    usecols=['CO_MUNICIPIO_PROVA', 'NO_MUNICIPIO_PROVA', 'SG_UF_PROVA', 
                            'NU_NOTA_CH', 'TP_ST_CONCLUSAO'])
except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho.")
    exit()

# 2. Processamento dos dados
# Criar coluna combinada de Município/UF
df['MUNICIPIO'] = df['NO_MUNICIPIO_PROVA'] + '/' + df['SG_UF_PROVA']

mapa_conclusao = {
    1: 'Concluído',
    2: 'Concluirá em 2023',
    3: 'Concluirá após 2023',
    4: 'Não cursando'
}

df['SITUACAO_CONCLUSAO'] = df['TP_ST_CONCLUSAO'].map(mapa_conclusao)

# 3. Gráfico 1: Top 20 municípios por média de notas
plt.figure(figsize=(14, 8))
media_municipio = df.groupby('MUNICIPIO')['NU_NOTA_CH'].mean().sort_values(ascending=False).head(20)
sns.barplot(x=media_municipio.values, y=media_municipio.index, color='#3498db')

plt.title('Top 20 Médias de Notas em Ciências Humanas por Município', fontsize=16)
plt.xlabel('Nota Média', fontsize=14)
plt.ylabel('Município', fontsize=14)

# Adicionar valores nas barras
for i, v in enumerate(media_municipio.values):
    plt.text(v+5, i, f"{v:.1f}", ha='left', va='center')

plt.tight_layout()
plt.show()

# 4. Gráfico 2: Situação de Conclusão do Ensino Médio por Município (Top 20)
plt.figure(figsize=(14, 10))
top_municipios = df['MUNICIPIO'].value_counts().head(20).index
df_top = df[df['MUNICIPIO'].isin(top_municipios)]

conclusao_municipio = df_top.groupby(['MUNICIPIO', 'SITUACAO_CONCLUSAO']).size().unstack().fillna(0)
conclusao_municipio = conclusao_municipio.div(conclusao_municipio.sum(axis=1), axis=0) * 100  # Converter para porcentagem

# Ordenar pela maior taxa de concluídos
conclusao_municipio = conclusao_municipio.sort_values('Concluído', ascending=False)
conclusao_municipio.plot(kind='barh', stacked=True, figsize=(14, 10))

plt.title('Situação de Conclusão do Ensino Médio por Município (Top 20) (%)', fontsize=16)
plt.xlabel('Percentual', fontsize=14)
plt.ylabel('Município', fontsize=14)
plt.legend(title='Situação', bbox_to_anchor=(1.05, 1))
plt.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

# 5. Gráfico 3: Relação entre Conclusão EM e Desempenho por Município (Top 50)
plt.figure(figsize=(12, 12))

# Selecionar municípios com mais participantes para melhor visualização
top_municipios = df['MUNICIPIO'].value_counts().head(50).index
df_top = df[df['MUNICIPIO'].isin(top_municipios)]

# Calcular % de concluídos por município
percent_concluidos = df_top.groupby('MUNICIPIO')['TP_ST_CONCLUSAO'].apply(
    lambda x: (x == 1).mean() * 100).reset_index()
percent_concluidos.columns = ['MUNICIPIO', 'PERCENT_CONCLUIDOS']

# Calcular nota média por município
media_municipio = df_top.groupby('MUNICIPIO')['NU_NOTA_CH'].mean().reset_index()
media_municipio.columns = ['MUNICIPIO', 'NU_NOTA_CH']

# Combinar os dados
df_analise = pd.merge(media_municipio, percent_concluidos, on='MUNICIPIO')

sns.scatterplot(x='PERCENT_CONCLUIDOS', y='NU_NOTA_CH', data=df_analise, s=100)

plt.title('Relação entre Conclusão do Ensino Médio e Desempenho por Município (Top 50)', fontsize=16)
plt.xlabel('Percentual de Alunos que Já Concluíram o Ensino Médio (%)', fontsize=14)
plt.ylabel('Nota Média em Ciências Humanas', fontsize=14)

# Adicionar rótulos dos municípios (apenas para alguns destaques)
for i, row in df_analise.iterrows():
    if row['PERCENT_CONCLUIDOS'] > 75 or row['NU_NOTA_CH'] > df_analise['NU_NOTA_CH'].quantile(0.9):
        plt.text(row['PERCENT_CONCLUIDOS']+0.5, row['NU_NOTA_CH']+1, row['MUNICIPIO'],
                 ha='left', va='center', fontsize=8)

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()