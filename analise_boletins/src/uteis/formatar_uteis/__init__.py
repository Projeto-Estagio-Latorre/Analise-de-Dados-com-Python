import os
import pandas as pd
import matplotlib.pyplot as plt


def juntar_csv(diretorio):
    dataframes = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            df = pd.read_csv(caminho_arquivo)
            dataframes.append(df)

    df_final = pd.concat(dataframes, ignore_index=True)

    df_final.to_csv('analise_boletins/src/boletins/junçao.csv', index=False)

def renomear_colunas(df):
    df.rename(columns={'7': 'Situação'}, inplace=True)
    df.rename(columns={'19': 'MFD/Conceito'}, inplace=True)
    df.rename(columns={'10': 'Nota'}, inplace=True)
    df.rename(columns={'12': 'Nota'}, inplace=True)
    df.rename(columns={'14': 'Nota'}, inplace=True)
    df.rename(columns={'16': 'Nota'}, inplace=True)
    df.rename(columns={'17': 'MFD'}, inplace=True)

    return df

def remover_linhas_com_hifen(df):
    df_filtrado = df[~df['MFD/Conceito'].str.contains('-')]
    
    return df_filtrado

def deleta_situacoes(coluna, valores, dataframe):
    for valor in valores:
        dataframe[coluna].replace(valor, pd.NA, inplace=True)
        dataframe.dropna(subset=[coluna], inplace=True)
    return dataframe

def deleta_notas(df):
    df = deleta_situacoes('Situação', ['Cancelado', 'Pendente', 'Dispensado', 'Trancado', 'Cursando'], df)
    df.reset_index(drop=True, inplace=True)

    return df

def ordenar_por_sigla(array):
    array.sort(key=lambda x: x.sigla)
    return array

def juntar_situacao(df):
    df.loc[(df['MFD/Conceito'] < 6) & (df['Situação'] == 'Aprovado'), 'Situação'] = 'Aprovado por bloco ou conselho'
    df.loc[(df['Situação'] == 'Aprovado/ Reprovado no Módulo'), 'Situação'] = 'Reprovado'
    df.loc[(df['Situação'] == 'Aprovado/Reprovado no Módulo'), 'Situação'] = 'Reprovado'
    df.loc[(df['Situação'] == 'Reprov. por Falta'), 'Situação'] = 'Reprovado'

    return df

def parse_coluna_media(df):
    df['MFD/Conceito'] = df['MFD/Conceito'].astype(float)
    return df

def remover_texto_depois_parenteses(texto):
    index = texto.find(" (")
    if index != -1:
        return texto[:index]
    return texto

def tratar_materia(df):
    df['Matéria'] = df['Matéria'].apply(
        remover_texto_depois_parenteses)
    return df
