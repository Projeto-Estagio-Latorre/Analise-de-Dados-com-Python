import os
import pandas as pd
import matplotlib.pyplot as plt
from analise_boletins.src.uteis import calcular_uteis as calc
from analise_boletins.src.uteis import formatar_uteis as frmt
from analise_boletins.src.uteis import model_uteis as modl
from analise_boletins.src.uteis import pdf_uteis as pdf
from anonimizacao.src.uteis import arquivo_uteis as f_arquivo
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def gerar_juncao_csv():
    lista_cursos = f_arquivo.obter_pastas_pasta('analise_boletins/src/boletins/')
    lista_cursos = f_arquivo.ordenar_pastas(lista_cursos)
    array_boletim_geral = []
    for curso in lista_cursos:
        print(f"Juntando csvs do curso {curso}.")
        diretorio = f'analise_boletins/src/boletins/{curso}/csv/'
        dataframes = []
        if os.path.isfile(f'{diretorio}Boletim_Geral.csv'):
            os.remove(f'{diretorio}Boletim_Geral.csv')
            print(f"O arquivo csv com a junção anterior foi excluído com sucesso.")
        contador_arquivo = 0
        for arquivo in os.listdir(f'{diretorio}'):
            if arquivo.endswith('.csv'):
                contador_arquivo += 1
                print(f"Juntando csv {arquivo} [{contador_arquivo}/{len(os.listdir(diretorio))}]")
                caminho_arquivo = os.path.join(diretorio, arquivo)
                df = pd.read_csv(caminho_arquivo)
                dataframes.append(df)

        df_final = pd.concat(dataframes, ignore_index=True)
        df_final.to_csv(f'{diretorio}Boletim_Geral.csv', index=False)
        array_boletim_geral.append(f'{diretorio}Boletim_Geral.csv')
        print(f"O arquivo Boletim_Geral.csv do curso {curso} criado com sucesso.")
    return array_boletim_geral


def formatar_juncao_csv(array_boletim_geral):
    # Fazer código para entrada de csvs etc
    array_dfs = []
    for arquivo in array_boletim_geral:
        print(f"Formatando csv {arquivo}.")
        df = pd.read_csv(arquivo)

        df = frmt.renomear_colunas(df)
        df = frmt.deleta_notas(df)
        # df = frmt.remover_linhas_com_hifen(df) # erro aqui
        df = frmt.parse_coluna_media(df)
        df = frmt.juntar_situacao(df)
        df = frmt.tratar_materia(df)

        array_dfs.append(df)
    return array_dfs


def gerar_pdf_final(array_dfs):
    print('Gerando objetos de analise disciplina.')
    lista_cursos = f_arquivo.obter_pastas_pasta('analise_boletins/src/boletins/')
    lista_cursos = f_arquivo.ordenar_pastas(lista_cursos)
    diretorios = []
    contador = 0
    for curso in lista_cursos:
        contador += 1
        diretorios.append({
            'caminho': f'analise_boletins/src/boletins/{curso}/',
            'curso': curso
        })
    i = 0
    for df in array_dfs:
        
        tupla_disciplinas = calc.get_tupla_disciplinas(df)
        # periodo = calc.get_anos(df) # erro aqui
        periodo = [2017, 2018, 2019, 2020]

        lista_analise_disciplina = []
        lista_analise_anual = []

        total_disciplinas = 0
        for ano in tupla_disciplinas:
            total_disciplinas += len(ano)

        contador_disciplina = 0
        for ano in tupla_disciplinas:
            for disciplina in ano:
                contador_disciplina += 1
                print(f"Gerando analise: {disciplina[1]} [{contador_disciplina}/{total_disciplinas}]")
                disciplina_sigla = disciplina[0]
                disciplina_nome = disciplina[1]
                ano = disciplina_sigla[-1]

                estatisticas_descritiva = calc.media_por_sigla(df, disciplina_sigla)

                distribuicao_freq_aprovados = calc.tabela_freq_relativa(
                    df, disciplina_sigla)
                grafico_freq_aprovados = calc.retorna_grafico_relativo_setores(
                    df, disciplina_sigla)

                distribuicao_freq_notas = calc.gerar_frequencia_de_notas(
                    df, disciplina_sigla)
                grafico_freq_notas = calc.gerar_grafico_frequencia_de_notas(
                    df, disciplina_sigla)

                analise_disciplina = modl.Analise_disciplina(disciplina_sigla, disciplina_nome, ano, estatisticas_descritiva,
                                                            distribuicao_freq_aprovados, grafico_freq_aprovados, distribuicao_freq_notas, grafico_freq_notas)
                lista_analise_disciplina.append(analise_disciplina)

        print('Objetos de analise disciplina finalizados.')
        print('Gerando objetos de analise anual.')
        anos = [1, 2, 3, 4]

        for ano in anos:
            plot_byte = calc.graf_freq_aprovados(ano, df)
            analise_anual = modl.Analise_anual(ano, plot_byte)
            if analise_anual:
                lista_analise_anual.append(analise_anual)

        periodo_analise = str(min(periodo)) + " à " + str(max(periodo))
        analise_curso = modl.Analise_curso(
            diretorios[i]["curso"], periodo_analise, lista_analise_disciplina, lista_analise_anual)
        print('Objetos de analise anual finalizados.')

        # codigo colocando em um pdf
        pdf.gerar_pdf(analise_curso, tupla_disciplinas, diretorios[i]["caminho"])
        i += 1

def gerar_analise_boletins():
    array_boletim_geral = gerar_juncao_csv()
    array_dfs = formatar_juncao_csv(array_boletim_geral)
    gerar_pdf_final(array_dfs)
    # print('Análise disponível em resultados.')
