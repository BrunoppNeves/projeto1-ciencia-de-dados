import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. IMPORTAR OS DADOS (substitua pelo caminho do seu arquivo)
try:
    df = pd.read_csv('MICRODADOS_ENEM_2023.csv', sep=';', encoding='latin-1')
except FileNotFoundError:
    print("Erro: Arquivo não encontrado. Verifique o caminho.")
    exit()

# 2. PREPARAR OS DADOS
# Mapear acesso à internet (Q025)
df['ACESSO_INTERNET'] = df['Q025'].map({'A': 'Sem internet', 'B': 'Com internet'})

# 3. GRÁFICO DE BARRAS - MÉDIA DE NOTAS
plt.figure(figsize=(10, 6))
sns.barplot(x='ACESSO_INTERNET', 
            y='NU_NOTA_CH', 
            data=df,
            estimator='mean',
            errorbar=None,
            palette=['#ff7f0e', '#1f77b4'])

# Adicionar valores em cima das barras
medias = df.groupby('ACESSO_INTERNET')['NU_NOTA_CH'].mean()
for i, media in enumerate(medias):
    plt.text(i, media + 10, f'{media:.1f}', ha='center', va='center', fontsize=12)

plt.title('Média de Notas em Ciências Humanas\npor Acesso à Internet', fontsize=14)
plt.xlabel('Acesso à Internet em Casa', fontsize=12)
plt.ylabel('Média da Nota', fontsize=12)
plt.ylim(0, 800)  # Ajuste conforme suas notas
plt.show()

# 4. GRÁFICO DE BARRAS - COMPARAÇÃO POR TIPO DE ESCOLA
if 'TP_ESCOLA' in df.columns:
    # Mapear tipo de escola
    df['TIPO_ESCOLA'] = df['TP_ESCOLA'].map({1: 'Não respondeu', 2: 'Pública', 3: 'Privada'})
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='TIPO_ESCOLA',
                y='NU_NOTA_CH',
                hue='ACESSO_INTERNET',
                data=df,
                estimator='mean',
                errorbar=None,
                palette=['#ff7f0e', '#1f77b4'])
    
    plt.title('Média de Notas por Acesso à Internet e Tipo de Escola', fontsize=14)
    plt.xlabel('Tipo de Escola', fontsize=12)
    plt.ylabel('Média da Nota', fontsize=12)
    plt.legend(title='Acesso à Internet')
    plt.ylim(0, 800)  # Ajuste conforme suas notas
    plt.show()