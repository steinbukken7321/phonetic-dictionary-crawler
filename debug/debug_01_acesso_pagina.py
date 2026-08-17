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

ARQUIVO = PASTA_RESULTADOS / "debug_01_pagina.html"


# ============================================================
# ACESSAR PÁGINA
# ============================================================

response = requests.get(
    URL,
    headers=HEADERS,
    timeout=30,
)


# ============================================================
# SALVAR HTML
# ============================================================

ARQUIVO.write_text(
    response.text,
    encoding="utf-8"
)


# ============================================================
# RESULTADO
# ============================================================

print("=" * 70)
print("DEBUG 01 - ACESSO À PÁGINA")
print("=" * 70)

print(f"Status: {response.status_code}")
print(f"Tamanho: {len(response.text)} bytes")
print(f"Arquivo: {ARQUIVO}")