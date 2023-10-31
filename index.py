# Importe os módulos necessários
from anonimizacao.src.uteis import geral_uteis as anonimizar_uteis
from analise_boletins.src.uteis import geral_uteis as analisar_uteis

anonimizar_uteis.gerar_boletins_anonimizados()
analisar_uteis.gerar_analise_boletins()
