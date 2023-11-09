import subprocess

libraries = ["pdfplumber", "pandas==2.0.3", "faker", "matplotlib", "reportlab", "pillow"]

for lib in libraries:
    subprocess.run(["pip", "install", lib])

from anonimizacao.src.uteis import geral_uteis as anonimizar_uteis
from analise_boletins.src.uteis import geral_uteis as analisar_uteis

anonimizar_uteis.gerar_boletins_anonimizados()
analisar_uteis.gerar_analise_boletins()
