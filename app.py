# 1. Importação das Bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Configurações Iniciais
sns.set(style="whitegrid")
pd.set_option('display.max_columns', 100)

# 3. Leitura dos Dados
arquivo_csv = 'MICRODADOS_ENEM_2023.csv'
df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')

# 4. Verificando as Primeiras Informações
print("Visualizando o DataFrame:")
print(df.head())

print("\nInformações do DataFrame:")
print(df.info())

# 5. Limpeza dos Dados
# Remover duplicados
df.drop_duplicates(inplace=True)

# Remover linhas com ausência de nota de Ciências Humanas
df = df[df['NU_NOTA_CH'].notnull()]

# Verificar valores nulos após a limpeza
print("\nValores nulos após limpeza:")
print(df.isnull().sum())
