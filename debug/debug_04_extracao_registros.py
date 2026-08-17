import requests
import pandas as pd
from pathlib import Path
from html.parser import HTMLParser


# ============================================================
# CONFIGURAÇÃO
# ============================================================

URL = (
    "https://www.portaldalinguaportuguesa.org/"
    "index.php?action=fonetica"
    "&region=lda"
    "&act=list"
    "&letter=a"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


# ============================================================
# PASTA DE RESULTADOS
# ============================================================

PASTA_RESULTADOS = Path("debug/resultados")
PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

ARQUIVO = PASTA_RESULTADOS / "debug_04_registros.csv"


# ============================================================
# EXTRATOR DE TEXTO
# ============================================================

class ExtratorTexto(HTMLParser):

    def __init__(self):
        super().__init__()
        self.texto = []

    def handle_data(self, data):
        self.texto.append(data)

    def resultado(self):
        return "".join(self.texto)


# ============================================================
# BAIXAR PÁGINA
# ============================================================

response = requests.get(
    URL,
    headers=HEADERS,
    timeout=30,
)

html = response.text


# ============================================================
# PEGAR SOMENTE A ROLLOVERTABLE
# ============================================================

inicio = html.find(
    "<table  cellpadding=4px id=rollovertable"
)

if inicio == -1:
    print("Tabela rollovertable não encontrada.")
    exit()


fim = html.find(
    "</table>",
    inicio
)

if fim == -1:
    print("Fim da tabela não encontrado.")
    exit()


tabela = html[inicio:fim]


# ============================================================
# SEPARAR OS TDs
# ============================================================

tds = tabela.split("<td")

celulas = []

for td in tds:

    if ">" not in td:
        continue

    conteudo = td.split(">", 1)[1]

    conteudo = conteudo.split("</td>", 1)[0]

    parser = ExtratorTexto()

    parser.feed(conteudo)

    texto = parser.resultado()

    texto = texto.replace("\n", "")
    texto = texto.replace("\t", "")

    celulas.append(texto)


# ============================================================
# REMOVER CABEÇALHO
# ============================================================

celulas = celulas[1:]


# ============================================================
# TRANSFORMAR EM REGISTROS
# ============================================================

linhas = []

for i in range(0, len(celulas), 3):

    if i + 2 >= len(celulas):
        break

    linhas.append(
        {
            "Palavra": celulas[i],
            "Categoria Gramatical": celulas[i + 1],
            "Fonética": celulas[i + 2],
        }
    )


# ============================================================
# CRIAR DATAFRAME
# ============================================================

df = pd.DataFrame(
    linhas,
    columns=[
        "Palavra",
        "Categoria Gramatical",
        "Fonética",
    ]
)


# ============================================================
# SALVAR CSV
# ============================================================

df.to_csv(
    ARQUIVO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# RESULTADO
# ============================================================

print("=" * 70)
print("DEBUG 04 - EXTRAÇÃO DOS REGISTROS")
print("=" * 70)

print(f"Registros encontrados: {len(df)}")
print(f"Arquivo: {ARQUIVO}")