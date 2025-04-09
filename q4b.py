import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurações
plt.style.use('ggplot')
sns.set_palette('pastel')
plt.rcParams['figure.figsize'] = [12, 6]

# Carregar dados
try:
    df = pd.read_csv('MICRODADOS_ENEM_2023.csv', sep=';', encoding='latin-1',
                    usecols=['CO_MUNICIPIO_PROVA', 'NO_MUNICIPIO_PROVA', 'SG_UF_PROVA',
                            'NU_NOTA_CH', 'TP_ESCOLA', 'Q006'])
except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho.")
    exit()

# Preparação dos dados
df['MUNICIPIO'] = df['NO_MUNICIPIO_PROVA'] + '/' + df['SG_UF_PROVA']
df['TIPO_ESCOLA'] = df['TP_ESCOLA'].map({1: 'Pública', 2: 'Privada', 3: 'Exterior'})
df['FAIXA_RENDA'] = df['Q006'].map({
    'A': 'Sem renda', 'B': 'Até R$ 1.212', 'C': 'R$ 1.212-1.818',
    'D': 'R$ 1.818-2.424', 'E': 'R$ 2.424-3.030', 'F': 'R$ 3.030-3.636',
    'G': 'R$ 3.636-4.848', 'H': 'R$ 4.848-6.060', 'I': 'R$ 6.060-7.272',
    'J': 'R$ 7.272-8.484', 'K': 'R$ 8.484-9.696', 'L': 'R$ 9.696-10.908',
    'M': 'R$ 10.908-12.120', 'N': 'R$ 12.120-14.544', 'O': 'R$ 14.544-18.180',
    'P': 'R$ 18.180-24.240', 'Q': 'Acima de R$ 24.240'
})

# 1. Variação por município (Top 15)
variacao = df.groupby('MUNICIPIO')['NU_NOTA_CH'].agg(['mean', 'std', 'count'])
variacao = variacao[variacao['count'] > 50]  # Filtro mínimo
variacao['CV'] = (variacao['std'] / variacao['mean']) * 100

top_var = variacao.nlargest(15, 'CV')
low_var = variacao.nsmallest(15, 'CV')

# Gráfico 1: Top municípios com maior variação
plt.figure(figsize=(14, 8))
sns.barplot(x='CV', y=top_var.index, data=top_var.reset_index(), color='#e74c3c')
plt.title('15 Municípios com Maior Variação de Notas (Coeficiente de Variação)', fontsize=16)
plt.xlabel('Coeficiente de Variação (%)', fontsize=12)
plt.ylabel('Município', fontsize=12)
plt.tight_layout()
plt.show()

# Gráfico 2: Top municípios com menor variação
plt.figure(figsize=(14, 8))
sns.barplot(x='CV', y=low_var.index, data=low_var.reset_index(), color='#2ecc71')
plt.title('15 Municípios com Menor Variação de Notas (Coeficiente de Variação)', fontsize=16)
plt.xlabel('Coeficiente de Variação (%)', fontsize=12)
plt.ylabel('Município', fontsize=12)
plt.tight_layout()
plt.show()

# 2. Análise por tipo de escola (Gráfico 3)
# 2. Análise de quantidade de alunos por tipo de escola por município (Barras lado a lado)
# Filtrar municípios com mais de 50 alunos e pegar os top 20
contagem_escolas = df.groupby(['MUNICIPIO', 'TIPO_ESCOLA']).size().unstack().fillna(0)
contagem_escolas = contagem_escolas[contagem_escolas.sum(axis=1) > 50].nlargest(20, 'Pública')  # Top 20 por escolas públicas

# Preparar dados para barplot lado a lado
contagem_escolas_melt = contagem_escolas.reset_index().melt(
    id_vars='MUNICIPIO', 
    value_vars=['Pública', 'Privada'],
    var_name='Tipo Escola', 
    value_name='Alunos'
)

# Plot
plt.figure(figsize=(16, 8))
bar = sns.barplot(
    x='MUNICIPIO',
    y='Alunos',
    hue='Tipo Escola',
    data=contagem_escolas_melt,
    palette=['#3498db', '#e74c3c'],  # Azul para pública, vermelho para privada
    ci=None
)

plt.title('Comparação Direta: Alunos em Escolas Públicas vs. Privadas (Top 20 Municípios)', fontsize=16)
plt.xlabel('Município', fontsize=12)
plt.ylabel('Número de Alunos', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Tipo de Escola', bbox_to_anchor=(1.05, 1))
plt.grid(axis='y', alpha=0.3)

# Adicionar rótulos de valor
for p in bar.patches:
    bar.annotate(
        f'{int(p.get_height())}', 
        (p.get_x() + p.get_width() / 2., p.get_height()), 
        ha='center', 
        va='center', 
        xytext=(0, 5), 
        textcoords='offset points',
        fontsize=9
    )

plt.tight_layout()
plt.show()