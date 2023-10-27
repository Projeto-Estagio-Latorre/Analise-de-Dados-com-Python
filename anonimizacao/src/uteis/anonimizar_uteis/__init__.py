import uuid
import pandas as pd
from faker import Faker

def existe_prontuario(prontuario, relacao_dataframe):
    if prontuario in relacao_dataframe['prontuario'].values:
        return True  # já existe
    return False


def criar_series_relacao(prontuario, relacao_dataframe):
    novo_uuid = uuid.uuid4()
    novo_nome = Faker().name()
    relacao = pd.Series([prontuario, novo_uuid, novo_nome],index=relacao_dataframe.columns)
    return relacao

def salvar_relacao(prontuario, dataframe):
    relacao = criar_series_relacao(prontuario, dataframe)
    dataframe = dataframe._append(relacao, ignore_index=True)
    return dataframe  # Retorna o DataFrame modificado

def relacionar(prontuario, relacao_dataframe):

    relacao_dataframe = salvar_relacao(prontuario, relacao_dataframe)
    return relacao_dataframe

# print(relacao_dataframe)

def anonimizar(boletim_csv):
    try:
        relacao_dataframe = pd.read_csv('./boletins/SP079/csv/Relacao.csv')
    except Exception as e:
        relacao_dataframe = None

    if relacao_dataframe is None:
        relacao_dataframe = pd.DataFrame(columns=['prontuario', 'uuid' , 'nome'])
    for indice, linha in boletim_csv.iterrows():
        prontuario = linha.Prontuário.strip()
        
        if not existe_prontuario(prontuario, relacao_dataframe):
            relacao_dataframe = relacionar(prontuario, relacao_dataframe)
        uuid_relacionado = relacao_dataframe.loc[relacao_dataframe['prontuario'] == prontuario]['uuid'].values[0]
        nome_relacionado = relacao_dataframe.loc[relacao_dataframe['prontuario'] == prontuario]['nome'].values[0]
        boletim_csv.at[boletim_csv.index[indice], 'Prontuário'] = uuid_relacionado
        boletim_csv.at[boletim_csv.index[indice], 'Aluno(a)'] = nome_relacionado

    return boletim_csv, relacao_dataframe

    # relacao_dataframe.to_csv('./src/arquivos/csv/relacao_alunos.csv', index=False)
    # boletim_csv.to_csv('./src/arquivos/csv/2020_A.csv', index=False)
        
