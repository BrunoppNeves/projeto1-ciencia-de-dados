import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações iniciais
plt.style.use('ggplot')

# 1. Importar e preparar os dados
try:
    df = pd.read_csv('MICRODADOS_ENEM_2023.csv', sep=';', encoding='latin-1',
                     usecols=['SG_UF_PROVA', 'Q006', 'Q001', 'Q002', 'TP_ESCOLA'])
except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho.")
    exit()

# Remover valores nulos para evitar distorções
df = df.dropna()

# 2. Mapeamento de renda familiar
renda_baixa = ['A', 'B', 'C']  # Até R$1.320,00
renda_media = ['D', 'E', 'F', 'G']  # De R$1.320,00 a R$8.250,00
renda_alta = ['H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']  # Acima de R$8.250,00

df['RENDA_FAMILIAR'] = df['Q006'].apply(
    lambda x: 'Baixa' if x in renda_baixa else 'Média' if x in renda_media else 'Alta'
)

# 3. Pais com graduação completa (F e G representam pais com ensino superior)
df['PAIS_GRADUADOS'] = df['Q001'].isin(['F', 'G']) | df['Q002'].isin(['F', 'G'])

# 4. Tipo de escola (1 = pública, 2, 3 e 4 = privada)
df['ESCOLA_PRIVADA'] = df['TP_ESCOLA'].isin([2, 3, 4])

# 5. Agrupar os dados por estado
estatisticas_estado = df.groupby('SG_UF_PROVA').agg({
    'RENDA_FAMILIAR': lambda x: (x == 'Baixa').mean(),  # Percentual de baixa renda
    'PAIS_GRADUADOS': 'mean',  # Percentual de pais graduados
    'ESCOLA_PRIVADA': 'mean'  # Percentual de alunos em escola privada
}).reset_index()

# Converter para percentual
estatisticas_estado[['RENDA_FAMILIAR', 'PAIS_GRADUADOS', 'ESCOLA_PRIVADA']] *= 100

# 6. Criar gráfico comparativo por estado
plt.figure(figsize=(18, 8))
estatisticas_estado.set_index('SG_UF_PROVA').plot(kind='bar', stacked=False, figsize=(18, 6), colormap='viridis')
plt.title('Comparação de Alunos por Estado - Renda, Escolaridade dos Pais e Tipo de Escola')
plt.ylabel('Percentual (%)')
plt.xlabel('Estado')
plt.xticks(rotation=45)
plt.legend(['Baixa Renda', 'Pais Graduados', 'Escola Privada'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 7. Contar quantidade de escolas públicas e privadas por estado
escolas_estado = df.groupby(['SG_UF_PROVA', 'ESCOLA_PRIVADA']).size().unstack().fillna(0)
escolas_estado.columns = ['Pública', 'Privada']

# 8. Criar gráfico de quantidade de escolas por estado
escolas_estado.plot(kind='bar', stacked=True, figsize=(18, 6), colormap='coolwarm')
plt.title('Quantidade de Escolas Públicas e Privadas por Estado')
plt.ylabel('Quantidade de Escolas')
plt.xlabel('Estado')
plt.xticks(rotation=45)
plt.legend(['Pública', 'Privada'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 9. Mapeamento de estados para regiões
mapa_regioes = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

# Criar nova coluna 'Região'
df['REGIAO'] = df['SG_UF_PROVA'].map(lambda uf: next((reg for reg, estados in mapa_regioes.items() if uf in estados), 'Desconhecido'))

# 10. Contar quantidade de escolas públicas e privadas por região
escolas_regiao = df.groupby(['REGIAO', 'ESCOLA_PRIVADA']).size().unstack().fillna(0)
escolas_regiao.columns = ['Pública', 'Privada']

# 11. Criar gráfico de quantidade de escolas por região
escolas_regiao.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='coolwarm')
plt.title('Quantidade de Escolas Públicas e Privadas por Região')
plt.ylabel('Quantidade de Escolas')
plt.xlabel('Região')
plt.xticks(rotation=0)
plt.legend(['Pública', 'Privada'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
