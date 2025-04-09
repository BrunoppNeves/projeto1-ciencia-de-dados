import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função para detecção de outliers com IQR
def detectar_outliers(df, coluna):
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    return df[(df[coluna] < limite_inferior) | (df[coluna] > limite_superior)]

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

# 3. Mapeamento das faixas etárias
faixa_etaria_map = {
    1: 'Menor de 17 anos',
    2: '17 anos',
    3: '18 anos',
    4: '19 anos',
    5: '20 anos',
    6: '21 anos',
    7: '22 anos',
    8: '23 anos',
    9: '24 anos',
    10: '25 anos',
    11: '26-30 anos',
    12: '31-35 anos',
    13: '36-40 anos',
    14: '41-45 anos',
    15: '46-50 anos',
    16: '51-55 anos',
    17: '56-60 anos',
    18: '61-65 anos',
    19: '66-70 anos',
    20: 'Maior de 70 anos'
}

# Criando a coluna FAIXA_ETARIA com as descrições
df['FAIXA_ETARIA'] = df['TP_FAIXA_ETARIA'].map(faixa_etaria_map)

# 4. Detectar outliers nas notas (opcional)
outliers = detectar_outliers(df, 'NU_NOTA_CH')
print(f'Número de outliers detectados: {len(outliers)}')

# 5. Gráfico de barras: Média das Notas de Ciências Humanas por Faixa Etária
plt.figure(figsize=(16, 8))
ax = sns.barplot(x='FAIXA_ETARIA', y='NU_NOTA_CH', data=df, estimator='mean', order=faixa_etaria_map.values())
plt.title('Média das Notas de Ciências Humanas por Faixa Etária', fontsize=16)
plt.xlabel('Faixa Etária', fontsize=14)
plt.ylabel('Média da Nota em Ciências Humanas', fontsize=14)
plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos do eixo x para melhor visualização

# Adicionando rótulos de valor nas barras
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 10), 
                textcoords='offset points')

# Adicionando uma linha horizontal para a média geral
media_geral = df['NU_NOTA_CH'].mean()
plt.axhline(media_geral, color='red', linestyle='--', label=f'Média Geral: {media_geral:.2f}')
plt.legend()

plt.tight_layout()  # Ajusta o layout para evitar cortes
plt.show()

print("Análise da Questão 1 concluída!")