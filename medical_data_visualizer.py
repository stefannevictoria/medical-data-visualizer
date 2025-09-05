# importa as bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv') # carrega o banco de dados

# 2
bmi = df['weight'] / ((df['height']/100)**2) # cria uma função que armazena o cálculo do BMI
df['overweight'] = (bmi > 25).map({True: 1, False: 0}) # create a new column which 0 means not overweight, and 1 overweight. bmi>25 create a series of true/false for each row, and .map converts to 1 if true and 0 if false

# 3
df['cholesterol'] = (df['cholesterol'] == 1).map({True: 0, False: 1}) # converts values equal to 1 in the column to 0, and values higher than 1 to 1
df['gluc'] = (df['gluc'] == 1).map({True: 0, False: 1}) # converts values equal to 1 in the column to 0, and values higher than 1 to 1

# 4
def draw_cat_plot():
    
    # 5
    df_cat = pd.melt(df, # pd.melt() transforma uma tabela de um formato largo para um formato longo
        id_vars=['cardio'], # coluna que quero que esteja fixa (não quero transformar)
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'], # colunas que quero que se tranformem em linhas
        var_name='variable', # nome da nova coluna que vai armazenar as novas linhas (que antes eram colunas)
        value_name='value' # nome da coluna que vai armazenar os valores
    )
    
    # 6
    group = df_cat.groupby(['cardio', 'variable', 'value']) # variável que armazena os agrupamentos -> .groupby() cria grupos (conjuntos) baseados nos valores das colunas cardio, variable e value (ou seja, cria grupos formado com os valores dessas colunas)
    size_groups = group.size() # armazena a quantidade de linhas que existem em cada um dos agrupamentos criados
    df_cat = size_groups.reset_index(name='total') # coloca os valores da contagem feita em uma coluna "total"

    # 7
    # sns.caplot() faz com que seja possível visualizar algumas variáveis (como gluc) em relação à outras (como cardio)
    chart = sns.catplot(
        data = df_cat,
        x = "variable", # define o eixo x
        y = "total",    # define o eixo y
        hue = "value",  # faz com que valores diferentes tenham cores diferentes no gráfico (ex: 0 vai ser de uma cor, e 1 vai ser de outra)
        col = "cardio", # separa o gráfico em dois subgráficos dentro do mesmo gráfico
        kind = "bar"    # tipo do gráfico
    )

    
    # 8
    fig = chart.figure # armazena o gráfico na variável fig
    
    # 9
    fig.savefig('catplot.png') # salva a figura do gráfico
    return fig

# 10
def draw_heat_map():
    
    # 11
    # a variável irá armazenar os filtros apenas com os dados corretos e desejados
    df_heat = df[df['ap_lo'] <= df['ap_hi']] # pressão diastólica <= sistólica

    df_heat = df_heat[
        (df_heat['height'] >= df['height'].quantile(0.025)) &
        (df_heat['height'] <= df['height'].quantile(0.975))
    ] # altura entre percentis 2.5% e 97.5%

    df_heat = df_heat[
        (df_heat['weight'] >= df['weight'].quantile(0.025)) &
        (df_heat['weight'] <= df['weight'].quantile(0.975))
    ] # peso entre percentis 2.5% e 97.5%
    
    # 12
    corr = df_heat.corr() # calcula a matriz de correlação e armazena na variável
    
    # 13
    mask = np.triu(corr) # cria uma "máscara" para esconder um dos triângulos e só mostrar o outro
    
    # 14
    fig, ax = plt.subplots(figsize=(12, 10)) # cria a figura e eixo para o gráfico
    
    # 15
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", cmap='magma', linewidths=0.5, ax=ax) # sns.heatmap() cria o heatmap (gráfico de calor), que é a representação de uma matriz

    # 16
    fig.savefig('heatmap.png') # salva a figura do gráfico
    return fig