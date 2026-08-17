import requests
from pathlib import Path


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

ARQUIVO = PASTA_RESULTADOS / "debug_02_tabela_rollovertable.html"


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
# LOCALIZAR TABELA rollovertable
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


tabela = html[
    inicio:
    fim + len("</table>")
]


# ============================================================
# SALVAR TABELA
# ============================================================

ARQUIVO.write_text(
    tabela,
    encoding="utf-8"
)


# ============================================================
# RESULTADO
# ============================================================

print("=" * 70)
print("DEBUG 02 - ESTRUTURA DA TABELA")
print("=" * 70)

print(f"Tamanho da tabela: {len(tabela)} bytes")
print(f"Arquivo: {ARQUIVO}")