import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de estilo
plt.style.use('ggplot')

# 1. Importar e preparar os dados
try:
    df = pd.read_csv('MICRODADOS_ENEM_2023.csv', sep=';', encoding='latin-1',
                     usecols=['TP_LOCALIZACAO_ESC', 'SG_UF_PROVA'])
except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho.")
    exit()

# 2. Mapeando os tipos de escola
df['TIPO_ESCOLA'] = df['TP_LOCALIZACAO_ESC'].map({1: 'Urbana', 2: 'Rural'})

# 3. Agrupar os dados por estado e tipo de escola
dados = df.groupby(['SG_UF_PROVA', 'TIPO_ESCOLA']).size().unstack(fill_value=0)

# 4. Criar o gráfico
plt.figure(figsize=(15, 7))

dados.plot(kind='bar', stacked=False, width=0.8, color=['#3498db', '#e74c3c'])

# 5. Personalização do gráfico
plt.xlabel('Estado', fontsize=14)
plt.ylabel('Quantidade de Escolas', fontsize=14)
plt.title('Comparação entre Escolas Urbanas e Rurais por Estado (ENEM 2023)', fontsize=16)
plt.xticks(rotation=45)
plt.legend(title="Tipo de Escola", loc='upper right')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar o gráfico
plt.show()
