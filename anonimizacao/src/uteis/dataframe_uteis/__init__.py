import pdfplumber
import pandas as pd
import os


def abrir_arquivo(caminho_arquivo):
    return pdfplumber.open(caminho_arquivo)

def fechar_arquivo(arquivo):
    arquivo.close()


def extrair_ano_e_periodo(caminho_arquivo):
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_base = os.path.splitext(nome_arquivo)[0]
    periodo = nome_base[-1]
    ano = nome_base[0:4]
    return ano, periodo


def extrair_nome_prontuario(dados):
    indice_aluno = dados.index("Aluno(a):")
    indice_matricula = dados.index("Matrícula:")
    nome = dados[indice_aluno + len("Aluno(a):"):indice_matricula].strip()
    prontuario = dados[indice_matricula + len("Matrícula:"):].strip()
    return nome, prontuario


def deletar_linha_por_valor(valor_procurado, df):

    linha_encontrada = None

    # Itera pelas colunas e linhas do DataFrame
    for index, row in df.iterrows():
        if valor_procurado in row.values:
            linha_encontrada = row
            break  # Para quando o valor é encontrado

    if linha_encontrada is not None:
        return df.drop(index=linha_encontrada.name, inplace=True)


def extrair_tabela(page):
    tabela = pd.DataFrame(page.extract_table())
    deletar_linha_por_valor('Total', tabela)
    deletar_linha_por_valor('Diário', tabela)
    deletar_linha_por_valor('Situação', tabela)
    deletar_linha_por_valor('N', tabela)
    return tabela


def renomear_colunas(dataframe):

    dataframe = dataframe.rename(columns={
            'Ano': 'Ano',
            'Período"A/S"': 'Período"A/S"',
            'Aluno(a)': 'Aluno(a)',
            'Prontuário': 'Prontuário',
            0: 'Diário',
            'Código': 'Código',
            'Sigla': 'Sigla',
            'Matéria': 'Matéria',
            2: 'C.H. Horas',
            3: 'C.H. Aulas',
            4: 'T. de Aulas',
            5: 'T. Faltas',
            6: 'Freq.',
            7: 'Situação',
            8: 'N1',
            9: 'F1',
            10: 'N2',
            11: 'F2',
            12: 'N3',
            13: 'F3',
            14: 'N4',
            15: 'F4',
            16: 'MD',
            17: 'NAF N',
            18: 'NAF F',
            19: 'MFD/Conceito'
            }, inplace=False)

    return dataframe


def formatar_dataframe(arquivo, caminho_arquivo):
    tabelas = pd.DataFrame()

    ano, periodo = extrair_ano_e_periodo(caminho_arquivo)

    nome, prontuario = None, None

    for i in range(len(arquivo.pages)):
        texto = arquivo.pages[i].extract_text()
        dados = texto.split('\n')[4]

        if 'Aluno(a):' in dados:
            nome, prontuario = extrair_nome_prontuario(dados)

        tabela = extrair_tabela(arquivo.pages[i])

        tabela.insert(0, 'Aluno(a)', nome)
        tabela.insert(1, 'Prontuário', prontuario)

        tabelas = tabelas._append(tabela, ignore_index=True)

    tabelas.insert(0, 'Ano', ano)
    tabelas.insert(1, 'Período"A/S"', periodo)

    tabelas = formatar_campos(tabelas)
    tabelas = desmembrar_disciplina(tabelas)
    tabelas = renomear_colunas(tabelas)

    return tabelas


def salvar_csv(dataframe, caminho_csv):
    dataframe.to_csv(caminho_csv, index=False)


def extrair_dados_colunas(lista):
    codigos = []
    siglas = []
    materias = []

    for item in lista:
        codigos.append(item[0:9])
        siglas.append(item[10:17])
        materias.append(item[20:])

    return codigos, siglas, materias


def desmembrar_disciplina(tabelas):
    lista = list(tabelas[1][0:])
    codigos, siglas, materias = extrair_dados_colunas(lista)
    siglas = [sigla.replace('(', '').replace(')', '') for sigla in siglas]

    tabelas.insert(5, "Código", codigos)
    tabelas.insert(6, "Sigla", siglas)
    tabelas.insert(7, "Matéria", materias)

    del tabelas[1]
    return tabelas

# Métodos de formatação


def remover_quebra_linha(cell):
    if isinstance(cell, str):
        cell = cell.replace('\n', ' ')
        return cell
    return cell


def substituir_por_ponto(cell):
    if isinstance(cell, str):
        cell = cell.replace(',', '.')
        return cell
    return cell


def remover_porcentagem(cell):
    if isinstance(cell, str):
        cell = cell.replace('%', '')
        return cell
    return cell


def remover_is_none(data):
    return data.applymap(lambda x: '' if x is None else x)


def formatar_campos(dataframe):
    dataframe = dataframe.applymap(remover_quebra_linha)
    dataframe = dataframe.applymap(substituir_por_ponto)
    dataframe = dataframe.applymap(remover_porcentagem)
    dataframe = dataframe.fillna('')
    dataframe = remover_is_none(dataframe)
    return dataframe
