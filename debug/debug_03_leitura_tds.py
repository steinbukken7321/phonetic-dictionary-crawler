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

ARQUIVO = PASTA_RESULTADOS / "debug_03_tds.txt"


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


# ============================================================
# ORGANIZAR RESULTADO
# ============================================================

resultado = []

numero = 0

for td in tds:

    if ">" not in td:
        continue

    numero += 1

    conteudo = td.split(">", 1)[1]

    conteudo = conteudo.split("</td>", 1)[0]

    resultado.append(
        f"TD {numero}\n"
        f"{'-' * 80}\n"
        f"{conteudo}\n"
    )


# ============================================================
# SALVAR
# ============================================================

ARQUIVO.write_text(
    "\n".join(resultado),
    encoding="utf-8"
)


# ============================================================
# RESULTADO
# ============================================================

print("=" * 70)
print("DEBUG 03 - LEITURA DOS TDs")
print("=" * 70)

print(f"TDs encontrados: {numero}")
print(f"Arquivo: {ARQUIVO}")