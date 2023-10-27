import os
import io
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

def get_tupla_disciplinas(df):
    tupla_anos = []

    for i in range(1, 5):
        tupla_materias = set()
        for index, row in df.iterrows():
            sigla = row['Sigla']
            if sigla.endswith('-' + str(i)):
                materia = row['Matéria'].capitalize()
                tupla_materias.add((sigla, materia))
        tupla_materias = tuple(tupla_materias)
        tupla_anos.append(tupla_materias)

    resultado = tuple(tupla_anos)

    return resultado

def formatar_dict(dicionario):
    resultado = ""
    for chave, valor in dicionario.items():
        resultado += f'\n{chave}: {valor}, '

    lista_separada = resultado.split(',')
    return lista_separada

def media_por_sigla(dataframe, sigla):
    filtro = dataframe['Sigla'] == sigla
    notas = dataframe.loc[filtro, 'MFD/Conceito']

    media = round(notas.mean(), 2)
    mediana = round(notas.median(), 2)
    maior_nota = round(notas.max(), 2)
    menor_nota = round(notas.min(), 2)

    estatistica_descritiva = {
        'Média': media,
        'Mediana': mediana,
        'Maior nota': maior_nota,
        'Menor nota': menor_nota
    }

    estatistica_descritiva_str = formatar_dict(estatistica_descritiva)

    return estatistica_descritiva_str


def tabela_freq_relativa(df, sigla):
    frequencia_absoluta = retornar_frequencia_absoluta(df, sigla)
    frequencia_relativa = retorna_frequencia_relativa(df, sigla)

    frequencia_relativa.sort_index()

    registro = {
        sigla: frequencia_relativa.keys(),
        'Frequência Absoluta': frequencia_absoluta,
        'Frequência Relativa (%)': [round(valor, 2) for valor in frequencia_relativa],
    }

    tabela_freq = pd.DataFrame(registro)
    return tabela_freq


def retornar_frequencia_absoluta(df, sigla):

    filtro_disciplina = df['Sigla'] == sigla

    situacao_counts = df[filtro_disciplina]['Situação'].value_counts(0)

    total = len(df[filtro_disciplina])
    aprovados_disciplina = situacao_counts.get('Aprovado', 0)
    aprovados_bloco_conselho_disciplina = situacao_counts.get('Aprovado por bloco ou conselho', 0)
    reprovados_disciplina = situacao_counts.get('Reprovado', 0)

    freq_absoluta = [aprovados_disciplina, aprovados_bloco_conselho_disciplina,reprovados_disciplina, total]

    return freq_absoluta

def retorna_frequencia_relativa(df, sigla):
    filtro_disciplina = df['Sigla'] == sigla
    
    frequencia_relativa = df[filtro_disciplina]['Situação'].value_counts(1) * 100
    
    frequencia_relativa['Total'] = 100

    if not 'Aprovado' in frequencia_relativa.index:
        frequencia_relativa['Aprovado'] = 0

    if not 'Aprovado por bloco ou conselho' in frequencia_relativa.index:
        frequencia_relativa['Aprovado por bloco ou conselho'] = 0

    if not 'Reprovado' in frequencia_relativa.index:
        frequencia_relativa['Reprovado'] = 0

    ordenacao = ['Aprovado', 'Aprovado por bloco ou conselho', 'Reprovado', 'Total']

    frequencia_relativa_ordenada = frequencia_relativa.reindex(ordenacao)

    print('frequencia relativa: ', frequencia_relativa)
    print('frequencia relativa ordenada: ', frequencia_relativa_ordenada)

    return frequencia_relativa_ordenada

def get_linha(coluna, valor, dataframe):
    resultado = dataframe[dataframe[coluna] == valor]
    return resultado

def get_notas_disciplina(disciplina, dataframe):
    alunos_disciplina = get_linha('Sigla', disciplina, dataframe)
    notas = alunos_disciplina['MFD/Conceito'].tolist()
    notas_float = [float(nota) for nota in notas]
    return notas_float

def get_anos(dataframe):
    anos = dataframe['Ano'].unique()
    anos_int = [int(ano) for ano in anos]
    return anos_int

def dividir_frequencia_absoluta(medias):
    medias_0_a_2 = []
    medias_2_a_4 = []
    medias_4_a_6 = []
    medias_6_a_8 = []
    medias_8_a_10 = []

    for media in medias:
        if 0.00 <= media <= 1.99:
            medias_0_a_2.append(media)
        elif 2.00 <= media <= 3.99:
            medias_2_a_4.append(media)
        elif 4.00 <= media <= 5.99:
            medias_4_a_6.append(media)
        elif 6.00 <= media <= 7.99:
            medias_6_a_8.append(media)
        elif 8.00 <= media <= 10.00:
            medias_8_a_10.append(media)

    categorias = [
        len(medias_0_a_2),
        len(medias_2_a_4),
        len(medias_4_a_6),
        len(medias_6_a_8),
        len(medias_8_a_10)
    ]
    return categorias


def calcular_frequencia_relativa(notas_distribuidas, total_alunos):
    frequencia_relativa = []
    for nota in notas_distribuidas:
        frequencia_relativa.append((nota * 100) / total_alunos)

    return frequencia_relativa

def calcular_frequencia_acumulada(frequencia_absoluta):
    frequencia_acumulada = []
    acumulado = 0 
    for valor in frequencia_absoluta:
        acumulado += valor  
        frequencia_acumulada.append(acumulado)  
    return frequencia_acumulada

def gerar_frequencia_de_notas(df, disciplina):
    medias = get_notas_disciplina(disciplina, df)

    frequencia_absoluta = dividir_frequencia_absoluta(medias)
    frequencia_relativa = calcular_frequencia_relativa(frequencia_absoluta, len(medias))
    frequencia_acumulada = calcular_frequencia_acumulada(frequencia_absoluta)
    frequencia_acumulada_em_porcentagem = calcular_frequencia_relativa(frequencia_acumulada, len(medias))

    faixas = ['0.0 - 1.99', '2.0 - 3.99', '4.0 - 5.99', '6.0 - 7.99', '8.0 - 10.00']

    data = {
        'Nota': faixas,
        'Frequência Absoluta': frequencia_absoluta,
        'Frequência Relativa (%)': frequencia_relativa,
        'Frequência Acumulada': frequencia_acumulada,
        'Frequência Acumulada (%)': frequencia_acumulada_em_porcentagem
    }

    df_freq = pd.DataFrame(data)
    total_row = {
        'Nota': 'Total',
        'Frequência Absoluta': sum(frequencia_absoluta),
        'Frequência Relativa (%)': 100.0,
    }
    total_df = pd.DataFrame(total_row, index=[0])
    frequencia_df = pd.concat([df_freq, total_df], ignore_index=True)

    frequencia_df = frequencia_df.round(2)
    frequencia_df = frequencia_df.fillna('-')

    return frequencia_df

def deletar_colunas(colunas, dataframe):
    for coluna in colunas:
        if coluna in dataframe.columns:
            dataframe = dataframe.drop(coluna, axis=1)
    return dataframe

def somar_colunas(colunas, dataframe):
    colunas_presentes = []

    for coluna in colunas:
        if coluna in dataframe.columns:
              colunas_presentes.append(coluna)

    return dataframe[colunas_presentes].sum(axis=1)

def retorna_grafico_relativo_setores(df, disciplina):

    freq_relativa = retorna_frequencia_relativa(df, disciplina)
    freq_relativa = freq_relativa.drop(freq_relativa.index[-1])

    if freq_relativa["Aprovado"] == 0.0:
        freq_relativa = freq_relativa[freq_relativa.index != "Aprovado"]
    if freq_relativa["Aprovado por bloco ou conselho"] == 0.0:
        freq_relativa = freq_relativa[freq_relativa.index != "Aprovado por bloco ou conselho"]
    if freq_relativa["Reprovado"] == 0.0:
        freq_relativa = freq_relativa[freq_relativa.index != "Reprovado"]
    

    plt.rcParams["figure.figsize"] = [9, 5]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["font.size"] = 14

    _ = freq_relativa.plot.pie(autopct='%1.1f%%')

    _ = plt.title(f"Situação dos alunos no curso {disciplina}")

    plt.gca().axes.get_yaxis().set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    plt.close()

    return buffer

def gerar_grafico_frequencia_de_notas(df, disciplina):
    medias = get_notas_disciplina(disciplina, df)
    data = {
      'Nota': ['0.0 - 1.99', '2.0 - 3.99', '4.0 - 5.99', '6.0 - 7.99', '8.0 - 10.00'],
      'Frequência Absoluta': dividir_frequencia_absoluta(medias),
      'Frequência Relativa (%)': calcular_frequencia_relativa(dividir_frequencia_absoluta(medias), len(medias))
    }
    grafico_df = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(grafico_df['Nota'], grafico_df['Frequência Relativa (%)'], color='blue', alpha=0.7, label='Frequência Relativa (%)')

    plt.xlabel('Nota')
    plt.ylabel('Frequência Relativa (%)')
    plt.title('Distribuição de Frequência de Notas (Escalada de 0% a 100%)')
    plt.ylim(0, 100)

    estatisticas = grafico_df['Frequência Relativa (%)']
    for bar, valor in zip(bars, estatisticas):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{valor:.2f}%',
                 ha='center', va='bottom', color='black', fontsize=14)
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    plt.close()

    return buffer

def graf_freq_aprovados(ano, df):
    Debugg = True

    alunos_por_ano = df[df['Sigla'].str.contains('-'+str(ano))]
    agrupamento_sigla = alunos_por_ano.groupby(['Sigla'])

    analise = agrupamento_sigla['Situação'].value_counts().unstack().fillna(0)

    analise['total'] = analise.sum(axis=1)

    colunas = ['Aprovado', 'Reprovado', 'Aprovado por bloco ou conselho']
    for coluna in colunas:
        try:
            analise[coluna + ' %'] = (analise[coluna] / analise['total']) * 100
        except:
            continue

    analise.reset_index()
    try:
        print("Salvando gráfico do ano " + str(ano))
        plot = analise.plot(kind='bar', y=['Aprovado %', 'Reprovado %', 'Aprovado por bloco ou conselho %'], figsize=(25, 6))
        plot.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          fancybox=True, shadow=True, ncol=5)
        plot.set_xlabel("")
        plot_buffer = io.BytesIO()
        plot.figure.savefig(plot_buffer, format='png')
        plot_buffer.seek(0)
    except Exception as e:
        if Debugg:
            print(e)
        else:
            print("Não foi possível gerar o gráfico do ano " + str(ano))
        return None, None

    return plot_buffer
      