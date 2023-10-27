class Analise_curso:
    def __init__(self, nome, periodo_analise, lista_analise_disciplinas, lista_analise_anual):
        self.nome = nome
        self.periodo_analise = periodo_analise
        self.lista_analise_disciplinas = lista_analise_disciplinas
        self.lista_analise_anual = lista_analise_anual

class Analise_disciplina:
    def __init__(self, sigla, nome, ano, estatisticas_descritivas, distribuicao_freq_aprovados, grafico_freq_aprovados, distribuicao_freq_notas, grafico_freq_notas):
        self.sigla = sigla
        self.nome = nome
        self.ano = ano
        self.estatisticas_descritivas = estatisticas_descritivas  # dict
        self.distribuicao_freq_aprovados = distribuicao_freq_aprovados  # DataFrame
        self.grafico_freq_aprovados = grafico_freq_aprovados  # bytes
        self.distribuicao_freq_notas = distribuicao_freq_notas  # DataFrame
        self.grafico_freq_notas = grafico_freq_notas  # bytes

class Analise_anual:
    def __init__(self, ano, distribuicao_freq_aprovados_reprovados):
        self.ano = ano
        self.distribuicao_freq_aprovados_reprovados = distribuicao_freq_aprovados_reprovados  # bytes