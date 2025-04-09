import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# 1. IMPORTAR OS DADOS
try:
    # Substitua pelo caminho do seu arquivo
    df = pd.read_csv('MICRODADOS_ENEM_2023.csv', sep=';', encoding='latin-1', 
                     usecols=['TP_ESCOLA', 'NU_NOTA_CH', 'SG_UF_PROVA', 'TP_LOCALIZACAO_ESC'])
    
    print("Dados carregados com sucesso!")
    print(f"Total de registros: {len(df):,}")
    
except Exception as e:
    print(f"Erro ao carregar dados: {str(e)}")
    exit()

# 2. PRÉ-PROCESSAMENTO
# Mapear tipo de escola conforme sua tabela
df['TIPO_ESCOLA'] = df['TP_ESCOLA'].map({
    1: 'Não Respondeu',
    2: 'Pública',
    3: 'Privada'
})

# Filtrar apenas escolas públicas e privadas (remover 'Não Respondeu')
df = df[df['TP_ESCOLA'].isin([2, 3])].copy()

# Mapear localização (assumindo mesma estrutura anterior)
df['LOCALIZACAO'] = df['TP_LOCALIZACAO_ESC'].map({
    1: 'Urbana',
    2: 'Rural'
})

# Agrupar regiões por UF
regioes = {
    'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}
df['REGIAO'] = df['SG_UF_PROVA'].apply(lambda x: next((k for k, v in regioes.items() if x in v), 'Outro'))

# 3. ANÁLISE GERAL PÚBLICAS vs PRIVADAS
plt.figure(figsize=(10, 6))
sns.barplot(x='TIPO_ESCOLA', y='NU_NOTA_CH', data=df, estimator=np.mean,
            order=['Pública', 'Privada'], errorbar=None,
            palette={'Pública': '#3498db', 'Privada': '#e74c3c'})

plt.title('Comparação de Desempenho: Escolas Públicas vs Privadas', fontsize=14)
plt.xlabel('Tipo de Escola')
plt.ylabel('Nota Média em Ciências Humanas')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Adicionar valores nas barras
medias = df.groupby('TIPO_ESCOLA')['NU_NOTA_CH'].mean()
for i, (tipo, media) in enumerate(medias.items()):
    plt.text(i, media+15, f'{media:.1f}', ha='center', va='center', fontweight='bold')

plt.tight_layout()
plt.show()

# 4. ANÁLISE POR REGIÃO
plt.figure(figsize=(14, 7))
sns.barplot(x='REGIAO', y='NU_NOTA_CH', hue='TIPO_ESCOLA', data=df,
            estimator=np.mean, errorbar=None,
            palette={'Pública': '#3498db', 'Privada': '#e74c3c'},
            order=['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'])

plt.title('Desempenho por Região e Tipo de Escola', fontsize=14)
plt.xlabel('Região')
plt.ylabel('Nota Média')
plt.legend(title='Tipo de Escola', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 5. ANÁLISE CAPITAL vs INTERIOR
plt.figure(figsize=(12, 6))
sns.barplot(x='LOCALIZACAO', y='NU_NOTA_CH', hue='TIPO_ESCOLA', data=df,
            estimator=np.mean, errorbar=None,
            palette={'Pública': '#3498db', 'Privada': '#e74c3c'})

plt.title('Desempenho em Áreas Urbanas vs Rurais', fontsize=14)
plt.xlabel('Localização')
plt.ylabel('Nota Média')
plt.legend(title='Tipo de Escola')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 6. TESTE ESTATÍSTICO
publicas = df[df['TIPO_ESCOLA'] == 'Pública']['NU_NOTA_CH'].dropna()
privadas = df[df['TIPO_ESCOLA'] == 'Privada']['NU_NOTA_CH'].dropna()

t_stat, p_valor = stats.ttest_ind(publicas, privadas, equal_var=False)
diff = privadas.mean() - publicas.mean()

print("\nRESULTADOS ESTATÍSTICOS:")
print(f"Escolas Públicas (Média): {publicas.mean():.1f} pontos")
print(f"Escolas Privadas (Média): {privadas.mean():.1f} pontos")
print(f"Diferença: {diff:.1f} pontos ({diff/publicas.mean()*100:.1f}% maior)")
print(f"\nTeste t de Student: t = {t_stat:.2f}, p = {p_valor:.5f}")
print("Diferença estatisticamente significativa" if p_valor < 0.05 else "Diferença não significativa")

# 7. TABELA COMPARATIVA
print("\nTABELA COMPARATIVA (Médias por Região e Localização):")
tabela = df.groupby(['REGIAO', 'LOCALIZACAO', 'TIPO_ESCOLA'])['NU_NOTA_CH'].mean().unstack()
print(tabela.round(1))