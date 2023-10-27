#  Descrição

O Sistema de Análise de Boletins Escolares é uma poderosa ferramenta de automação feita em python projetada para simplificar e aprimorar o processo de coleta de dados importantes e a análise estatística do desempenho dos alunos.

## Funcionalidades

### **Coleta de dados:**
O sistema automatiza a coleta de boletins escolares armazenados em um PDF dos alunos de determinado curso, poupando tempo e esforço. Os dados coletados incluem o nome do aluno, prontuário, frequência, situação atual e se o aluno foi aprovado ou não nas matérias.

### **Anonimização:**
Priorizamos a privacidade dos alunos e, portanto, implementamos um sistema de anonimização. Este recurso permite a remoção de dados sensíveis, mantendo apenas as informações essenciais para análises estatísticas do desempenho dos alunos. Dessa forma, evitamos possíveis vazamentos de dados e garantimos a conformidade com as regulamentações de privacidade.

### **Análise estatística:**
Utilizando algoritmos de análise de dados, o projeto fornece uma análise completa do desempenho dos alunos nas matérias, identificando tendências, áreas de melhoria e pontos fortes.

### **Visualizações Intuitivas:**
Apresentamos os resultados da análise de forma clara e intuitiva, por meio de gráficos e relatórios fáceis de entender.

### **Relatório em PDF:**
Os resultados da análise são compilados em relatórios em formato PDF, permitindo uma fácil distribuição e armazenamento dos dados. Esses relatórios fornecem uma visão completa e pronta para uso do desempenho dos alunos nas matérias, facilitando a tomada de decisões informadas e o acompanhamento do progresso ao longo do tempo

## Tecnologias utilizadas

Python 3.x

## Rodando o projeto
Para rodar o seu projeto a partir de um terminal na pasta raiz, onde está localizada o arquivo index.py, e siga estas etapas:

1 - Abra um terminal.

2 - Instale as bibliotecas no seu ambiente virtual

```
pip install pdfplumber
pip install pandas
pip install faker
pip install matplotlib
pip install reportlab
pip install pillow
```

3 - Crie uma pasta com nome do curso da analise
```
analise_boletins/src/boletins/pasta_curso
```

4 - Adicione o PDF com os boletins vindos do SUAP na pasta criada
```
analise_boletins/src/boletins/pasta_curso/boletins_informatica.pdf
```

5 - Rode o seguinte comando
```
python index.py
```

## Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="http://github.com/PauloKenji">
        <img src="https://avatars.githubusercontent.com/u/84166469?&v=4" width="100px;" alt="Foto de Tati Alves no GitHub"/><br>
        <sub>
          <b>Paulo Kenji</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="http://github.com/josineudo-arruda">
        <img src="https://avatars.githubusercontent.com/u/96135176?&v=4" width="100px;" alt="Foto de Tati Alves no GitHub"/><br>
        <sub>
          <b>Josineudo Arruda</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="http://github.com/analuisa714">
        <img src="https://avatars.githubusercontent.com/u/96425830?&v=4" width="100px;" alt="Foto de Tati Alves no GitHub"/><br>
        <sub>
          <b>Ana Luisa</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="http://github.com/julia-furquim">
        <img src="https://avatars.githubusercontent.com/u/101726785?&v=4" width="100px;" alt="Foto de Tati Alves no GitHub"/><br>
        <sub>
          <b>Julia Furquim</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="http://github.com/ryan-salomao">
        <img src="https://avatars.githubusercontent.com/u/101951438?&v=4" width="100px;" alt="Foto de Tati Alves no GitHub"/><br>
        <sub>
          <b>Ryan Salomão</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="http://github.com/VictorTPaim">
        <img src="https://avatars.githubusercontent.com/u/102189438?&v=4" width="100px;" alt="Foto de Tati Alves no GitHub"/><br>
        <sub>
          <b>Victor Paim</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="http://github.com/josecarlos3040">
        <img src="https://avatars.githubusercontent.com/u/102222057?&v=4" width="100px;" alt="Foto de Tati Alves no GitHub"/><br>
        <sub>
          <b>Jose Carlos</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

### Organização da equipe
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Projeto-Estagio-Latorre">
        <img src="https://avatars.githubusercontent.com/u/148801533?s=200&v=4" width="100px;" alt="Foto de Tati Alves no GitHub"/><br>
        <sub>
          <b> Projeto-Estagio-Latorre </b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
