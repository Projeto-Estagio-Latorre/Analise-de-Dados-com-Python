import os

def criar_pasta(nome_pasta):

    if not os.path.exists(nome_pasta):
        try:
            os.mkdir(nome_pasta)
        except OSError:
            print ("A criação da pasta %s falhou" % nome_pasta)

def apagar_pasta(pasta):
    if os.path.exists(pasta):
        for nome_arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            try:
                if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                    os.unlink(caminho_arquivo)
                elif os.path.isdir(caminho_arquivo):
                    shutil.rmtree(caminho_arquivo)
            except Exception as e:
                print(f'Falha ao excluir {caminho_arquivo}. Erro: {e}')
        os.rmdir(pasta)
    else:
        print(f'A pasta {pasta} não existe.')

def obter_caminho_arquivo(pasta_atual):

    cwd = os.getcwd()
    
    caminho_completo = os.path.join(cwd, pasta_atual)
    
    lista_arquivos = obter_arquivos_pasta(caminho_completo)

    return lista_arquivos

def obter_arquivos_pasta(caminho_completo):
    
    arquivos = []
    for item in os.listdir(caminho_completo):
        caminho_item = os.path.join(caminho_completo, item)
        if os.path.isfile(caminho_item):
            arquivos.append(item)

    return arquivos

def obter_pastas_pasta(caminho_completo):
    
    pastas = []
    for item in os.listdir(caminho_completo):
        caminho_item = os.path.join(caminho_completo, item)
        if os.path.isdir(caminho_item):
            pastas.append(item)

    return pastas
