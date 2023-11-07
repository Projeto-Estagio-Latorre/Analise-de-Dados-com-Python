import pdfplumber
import os
import pandas as pd
from anonimizacao.src.uteis import dataframe_uteis as f_df
from anonimizacao.src.uteis import anonimizar_uteis as f_anonimizar
from anonimizacao.src.uteis import arquivo_uteis as f_arquivo

def gerar_boletins_anonimizados():
    print(f"Começou a extração de dados do pdf para os csv.")
    diretorio_boletins = "analise_boletins/src/boletins/"

    lista_pastas = f_arquivo.obter_pastas_pasta(diretorio_boletins)
    lista_pastas = f_arquivo.ordenar_pastas(lista_pastas)

    for nome_pasta_curso in lista_pastas:
        print(f"Extraindo dados do curso {nome_pasta_curso}.")
        if os.path.isfile(f'{diretorio_boletins}{nome_pasta_curso}/junçao.csv'):
            os.remove(f'{diretorio_boletins}{nome_pasta_curso}/junçao.csv')
            f_arquivo.apagar_pasta(f'{diretorio_boletins}{nome_pasta_curso}/csv')
            print(f"Os arquivos da análise anterior foram limpos com sucesso.")

        lista_arquivos = f_arquivo.obter_arquivos_pasta(f'{diretorio_boletins}{nome_pasta_curso}')
        contador = 0
        for nome_arquivo in lista_arquivos:
            contador += 1
            print(f"Extraindo dados do arquivo {nome_arquivo} [{contador}/{len(lista_arquivos)}]." )

            diretorio_atual = diretorio_boletins + nome_pasta_curso
            nome_arquivo = nome_arquivo.replace('.pdf', '')
            
            arquivo = f_df.abrir_arquivo(f'{diretorio_atual}/{nome_arquivo}.pdf')
            boletins = f_df.formatar_dataframe(arquivo, nome_arquivo+".pdf")                                    
                
            f_arquivo.criar_pasta(f'{diretorio_boletins}{nome_pasta_curso}/csv')
            
            boletins.to_csv(f'{diretorio_boletins}{nome_pasta_curso}/csv/{nome_arquivo}.csv', index=False)

            boletins, relacao = f_anonimizar.anonimizar(boletins)

            boletins.to_csv(f'{diretorio_boletins}{nome_pasta_curso}/csv/{nome_arquivo}_Anonimizado.csv', index=False)
            relacao.to_csv(f'{diretorio_boletins}{nome_pasta_curso}/csv/Relacao.csv', index=False)
            f_df.fechar_arquivo(arquivo)
            print(f"{nome_arquivo}_Anonimizado.csv anonimizado e finalizado com sucesso")


    print(f"Os dados dos boletins foram extraídos com sucesso em csv.")
