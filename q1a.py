# Questão 1: Distribuição de Notas de Ciências Humanas

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

# 3. Análise dos fatores que podem influenciar outliers

# Criando categoria pública x privada
df['CATEGORIA_ESCOLA'] = df['TP_DEPENDENCIA_ADM_ESC'].apply(lambda x: 'Privada' if x == 4 else 'Pública')

# Gráfico de barras: Notas de Ciências Humanas por categoria de escola
plt.figure(figsize=(10, 6))
sns.barplot(x='CATEGORIA_ESCOLA', y='NU_NOTA_CH', data=df, estimator='mean')
plt.title('Média das Notas de Ciências Humanas - Escola Pública vs Privada')
plt.xlabel('Categoria da Escola')
plt.ylabel('Média da Nota em Ciências Humanas')
plt.show()

# Gráfico de barras: Média das Notas de Ciências Humanas por faixa de renda
plt.figure(figsize=(14, 6))
sns.barplot(x='Q006', y='NU_NOTA_CH', data=df, estimator='mean', order=sorted(df['Q006'].unique()))
plt.title('Média das Notas de Ciências Humanas por Faixa de Renda Familiar')
plt.xlabel('Faixa de Renda Familiar (Q006)')
plt.ylabel('Média da Nota em Ciências Humanas')
plt.xticks(rotation=45)
plt.show()

# Gráfico de barras: Média das Notas de Ciências Humanas por estado de prova
plt.figure(figsize=(18, 6))
sns.barplot(x='SG_UF_PROVA', y='NU_NOTA_CH', data=df, estimator='mean')
plt.title('Média das Notas de Ciências Humanas por Estado de Aplicação da Prova')
plt.xlabel('Estado de Aplicação da Prova')
plt.ylabel('Média da Nota em Ciências Humanas')
plt.xticks(rotation=45)
plt.show()

print("Análise da Questão 1 concluída!")
