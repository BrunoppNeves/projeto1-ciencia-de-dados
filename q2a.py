import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações iniciais
sns.set(style="whitegrid")
pd.set_option('display.max_columns', 100)

# 1. Leitura dos Dados
arquivo_csv = 'MICRODADOS_ENEM_2023.csv'
df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')

# 2. Limpeza básica
df = df.drop_duplicates()
df = df[df['NU_NOTA_CH'].notnull()]
df = df[df['TP_FAIXA_ETARIA'].notnull()]

# 3. Mapeamento das variáveis
# Mapeamento da escolaridade dos pais (Q001 e Q002)
escolaridade_map = {
    'A': 'A',
    'B': 'B',
    'C': 'C',
    'D': 'D',
    'E': 'E',
    'F': 'F',
    'G': 'G',
    'H': 'H'
}

# Mapeamento do tipo de escola (TP_ESCOLA)
tipo_escola_map = {
    1: '1',
    2: '2',
    3: '3'
}

# Criando colunas com a descrição da escolaridade e tipo de escola
df['ESCOLARIDADE_PAI'] = df['Q001'].map(escolaridade_map)
df['ESCOLARIDADE_MAE'] = df['Q002'].map(escolaridade_map)
df['TIPO_ESCOLA'] = df['TP_ESCOLA'].map(tipo_escola_map)

# 4. Gráfico de barras: Média das notas de Ciências Humanas por escolaridade do pai
plt.figure(figsize=(14, 6))
sns.barplot(x='ESCOLARIDADE_PAI', y='NU_NOTA_CH', data=df, estimator='mean', order=escolaridade_map.values())
plt.title('Média das Notas de Ciências Humanas por Escolaridade do Pai', fontsize=16)
plt.xlabel('Escolaridade do Pai', fontsize=14)
plt.ylabel('Média da Nota em Ciências Humanas', fontsize=14)
plt.xticks(rotation=0)  # Sem rotação para melhor visualização
plt.tight_layout()
plt.show()

# 5. Gráfico de barras: Média das notas de Ciências Humanas por escolaridade da mãe
plt.figure(figsize=(14, 6))
sns.barplot(x='ESCOLARIDADE_MAE', y='NU_NOTA_CH', data=df, estimator='mean', order=escolaridade_map.values())
plt.title('Média das Notas de Ciências Humanas por Escolaridade da Mãe', fontsize=16)
plt.xlabel('Escolaridade da Mãe', fontsize=14)
plt.ylabel('Média da Nota em Ciências Humanas', fontsize=14)
plt.xticks(rotation=0)  # Sem rotação para melhor visualização
plt.tight_layout()
plt.show()

# 6. Gráfico de barras agrupado: Média das notas por escolaridade do pai e tipo de escola
plt.figure(figsize=(16, 8))
sns.barplot(x='ESCOLARIDADE_PAI', y='NU_NOTA_CH', hue='TIPO_ESCOLA', data=df, estimator='mean', order=escolaridade_map.values())
plt.title('Média das Notas de Ciências Humanas por Escolaridade do Pai e Tipo de Escola', fontsize=16)
plt.xlabel('Escolaridade do Pai', fontsize=14)
plt.ylabel('Média da Nota em Ciências Humanas', fontsize=14)
plt.xticks(rotation=0)  # Sem rotação para melhor visualização
plt.legend(title='Tipo de Escola')
plt.tight_layout()
plt.show()

# 7. Gráfico de barras agrupado: Média das notas por escolaridade da mãe e tipo de escola
plt.figure(figsize=(16, 8))
sns.barplot(x='ESCOLARIDADE_MAE', y='NU_NOTA_CH', hue='TIPO_ESCOLA', data=df, estimator='mean', order=escolaridade_map.values())
plt.title('Média das Notas de Ciências Humanas por Escolaridade da Mãe e Tipo de Escola', fontsize=16)
plt.xlabel('Escolaridade da Mãe', fontsize=14)
plt.ylabel('Média da Nota em Ciências Humanas', fontsize=14)
plt.xticks(rotation=0)  # Sem rotação para melhor visualização
plt.legend(title='Tipo de Escola')
plt.tight_layout()
plt.show()

# 8. Análise de correlação
# Mapeamento da escolaridade para valores numéricos
escolaridade_numerica_map = {
    'A': 0,  # Nunca estudou
    'B': 1,  # Não completou a 4ª série/5º ano
    'C': 2,  # Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano
    'D': 3,  # Completou a 8ª série/9º ano, mas não completou o Ensino Médio
    'E': 4,  # Completou o Ensino Médio, mas não completou a Faculdade
    'F': 5,  # Completou a Faculdade, mas não completou a Pós-graduação
    'G': 6,  # Completou a Pós-graduação
    'H': None  # Não sei (vamos remover esses casos)
}

# Criando colunas com valores numéricos para escolaridade
df['ESCOLARIDADE_PAI_NUM'] = df['Q001'].map(escolaridade_numerica_map)
df['ESCOLARIDADE_MAE_NUM'] = df['Q002'].map(escolaridade_numerica_map)

# Removendo registros onde a escolaridade é "Não sei"
df = df.dropna(subset=['ESCOLARIDADE_PAI_NUM', 'ESCOLARIDADE_MAE_NUM'])

# Calculando a correlação
correlacao_pai = df['ESCOLARIDADE_PAI_NUM'].corr(df['NU_NOTA_CH'])
correlacao_mae = df['ESCOLARIDADE_MAE_NUM'].corr(df['NU_NOTA_CH'])

print(f"Correlação entre escolaridade do pai e notas de Ciências Humanas: {correlacao_pai:.2f}")
print(f"Correlação entre escolaridade da mãe e notas de Ciências Humanas: {correlacao_mae:.2f}")