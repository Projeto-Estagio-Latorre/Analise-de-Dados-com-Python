from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import pandas as pd
import os
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import utils
from PIL import Image as PILImage
from anonimizacao.src.uteis import arquivo_uteis as f_arquivo
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def calcularTamanhoImagem(imagem_original, doc, margem_esquerda, margem_direita, margem_superior, margem_inferior):
    
    imagem = PILImage.open(imagem_original)

    largura_disponivel = doc.width - margem_esquerda - margem_direita
    altura_disponivel = doc.height - margem_superior - margem_inferior
    
    largura_original, altura_original = imagem.size

    
    proporcao = min(largura_disponivel / largura_original, altura_disponivel / altura_original)

    largura_redimensionada = largura_original * proporcao
    altura_redimensionada = altura_original * proporcao


    imagem_redimensionada = Image(imagem_original, width=largura_redimensionada, height=altura_redimensionada)

    return imagem_redimensionada


def toList(df):
    return [list(df.columns)] + df.values.tolist()

def styleTable(tabela):
    return tabela.setStyle(TableStyle([
    ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
]))

def padronizar_df(df):
    df_list = toList(df)
    tabela = Table(df_list)
    tabela.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))

    return tabela

def encontrar_analise(valor, lista, tipo):
    if tipo == 'disciplina':
        for analise in lista:
            if analise.sigla == valor:
                return analise
    else:
        for analise in lista:
            if analise.ano == valor:
                return analise

def adicionar_marcadores(pdf_file, ano):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    for i, disciplina in enumerate(ano):
        disciplina_name = disciplina[1]
        disciplina_acronym = disciplina[0]
        c.drawCentredString(300, 300, disciplina_name)
        c.bookmarkPage(disciplina_name)
        c.addOutlineEntry(disciplina_acronym, disciplina_name)
    c.save()
    
def gerar_pdf(analise_curso, tupla_disciplinas, caminho):
    if not os.path.exists(f'{caminho}resultados/'):
        os.makedirs(f'{caminho}resultados/')

    script_directory = os.path.dirname(f"{caminho}resultados/")
    
    pdf_file = os.path.join(script_directory, f'analise_completa_{analise_curso.nome}.pdf')
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=100, 
        leftMargin=100,
        topMargin=40,
        bottomMargin=40,
    )

    content = []
    titulo = Paragraph(
        'Análise do curso ' + analise_curso.nome + ' no período de ' + analise_curso.periodo_analise,
        ParagraphStyle(name='Name',
                       fontName='Helvetica-Bold',
                       fontSize=15.5,
                       alignment=TA_LEFT)

    )

    content.append(titulo)
    content.append(Spacer(1, 20))
    count = 1

    total_alunos_analise = 0
    for ano in tupla_disciplinas:
        total_alunos_ano = 0
        contador_disciplina = 0
        for disciplina in ano:
            analise_disciplina = encontrar_analise(disciplina[0], analise_curso.lista_analise_disciplinas, 'disciplina')
            total_alunos_disciplina = (analise_disciplina.distribuicao_freq_aprovados['Frequência Absoluta'][3])
            total_alunos_ano += total_alunos_disciplina
            contador_disciplina += 1

        if contador_disciplina > 0:
            total_alunos_ano = total_alunos_ano/contador_disciplina
            total_alunos_ano = int(total_alunos_ano) if total_alunos_ano.is_integer() else int(total_alunos_ano) + 1
            total_alunos_analise += total_alunos_ano

    content.append(Paragraph(
            "Alunos avaliados neste período: " + str(total_alunos_analise), 
            ParagraphStyle(name='Name',fontSize=10)))

    content.append(PageBreak())

    for ano in tupla_disciplinas:
        total_alunos_ano = 0
        contador_disciplina = 0
        for disciplina in ano:
            analise_disciplina = encontrar_analise(disciplina[0], analise_curso.lista_analise_disciplinas, 'disciplina')
            total_alunos_disciplina = (analise_disciplina.distribuicao_freq_aprovados['Frequência Absoluta'][3])
            total_alunos_ano += total_alunos_disciplina
            contador_disciplina += 1

        if contador_disciplina > 0:
            total_alunos_ano = total_alunos_ano/contador_disciplina
            total_alunos_ano = int(total_alunos_ano) if total_alunos_ano.is_integer() else int(total_alunos_ano) + 1

        content.append(Paragraph(
            "Análise do "+str(count)+"º ano", 
            ParagraphStyle(
                    name='Name',
                    fontName='Helvetica-Bold',
                    fontSize=13)))
        
        content.append(Paragraph(
            "Alunos avaliados neste ano: " + str(total_alunos_ano), 
            ParagraphStyle(name='Name',fontSize=10)))

        adicionar_marcadores(pdf_file, ano) 

        for disciplina in ano:
            analise_disciplina = encontrar_analise(disciplina[0], analise_curso.lista_analise_disciplinas, 'disciplina')
            
            tabela_distribuicao_freq_aprovados = padronizar_df(analise_disciplina.distribuicao_freq_aprovados)
            
            tabela_distribuicao_freq_notas = padronizar_df(analise_disciplina.distribuicao_freq_notas)

            total_alunos_disciplina = (analise_disciplina.distribuicao_freq_aprovados['Frequência Absoluta'][3]) # total de notas -> (total de alunos)
            
            textos = [
                str(analise_disciplina.ano)+"° ano",
                analise_disciplina.nome + " (" + analise_disciplina.sigla + ")",                
                "Distribuição de frequência de  aprovados e reprovados no componente curricular "+ analise_disciplina.nome + " (" + analise_disciplina.sigla + ")",
                "Gráfico de setores de aprovados e reprovados usando frequência relativa no componente curricular "+analise_disciplina.sigla,
                "Distribuição de frequências de notas de alunos no componente curricular "+analise_disciplina.sigla,
                "Gráfico de barras de notas usando as faixas de notas do componente curricular "+analise_disciplina.sigla,
                "Distribuição de frequências de aprovação e reprovação dos componentes curriculares do "+str(analise_disciplina.ano)+"º ano",
                "Alunos avaliados nesta disciplina: " + str(total_alunos_disciplina),
            ]

            imagem = calcularTamanhoImagem(analise_disciplina.grafico_freq_aprovados, doc, 40, 40, 40, 40)

            imagem2 = calcularTamanhoImagem(analise_disciplina.grafico_freq_notas, doc, 0, 0, 0, 0)

            content.extend([
                Spacer(1, 12),
                Paragraph(textos[1],  ParagraphStyle(name='Name',fontName='Helvetica-Bold')),
                Spacer(1, 12),
                Paragraph(textos[7], ParagraphStyle(name='Name',fontSize=10)),
                Spacer(1, 12)
            ])

            for elemento in analise_disciplina.estatisticas_descritivas:
                content.append(Paragraph(elemento))

            content.extend([
                Spacer(1, 12),
                Paragraph(textos[2], ParagraphStyle(name='Name', fontSize=9,
                       alignment=TA_CENTER)),
                Spacer(1, 12),
                
                tabela_distribuicao_freq_aprovados,
                Spacer(1, 12),
                
                Paragraph(textos[3], ParagraphStyle(name='Name', fontSize=9,
                       alignment=TA_CENTER)),
                Spacer(1, 12),
                imagem,
               

                Paragraph(textos[4], ParagraphStyle(name='Name', fontSize=9,
                       alignment=TA_CENTER)),
                Spacer(1, 12),
                tabela_distribuicao_freq_notas,

                PageBreak(),

                Paragraph(textos[5], ParagraphStyle(name='Name', fontSize=9,
                       alignment=TA_CENTER)),
                Spacer(1, 12),
                imagem2,

                PageBreak(),
                Spacer(1, 12)
            ])     
        
        analise_anual = encontrar_analise(count, analise_curso.lista_analise_anual, 'anual')
        imagem3 = calcularTamanhoImagem(analise_anual.distribuicao_freq_aprovados_reprovados, doc, -80, -80, 0, 0)

        content.append(Paragraph(textos[6], ParagraphStyle(name='Name', fontSize=9, alignment=TA_CENTER)))
        content.append(Spacer(1, 12))
        content.append(imagem3)
        content.append(PageBreak())
        count += 1

    doc.build(content)
    
        