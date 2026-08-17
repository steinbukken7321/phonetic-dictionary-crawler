import requests
import pandas as pd
from pathlib import Path
from html.parser import HTMLParser
import inquirer
import time

# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_URL = "https://www.portaldalinguaportuguesa.org/index.php"

PASTA_DATA = Path("data")
PASTA_DATA.mkdir(parents=True, exist_ok=True)

LETRAS = "abcdefghijklmnopqrstuvwxyz"

# Número de tentativas para uma página que apresentar erro
MAX_TENTATIVAS = 5

# Tempo de espera entre tentativas
TEMPO_ESPERA = 5

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

# ============================================================
# REGIÕES
# ============================================================

REGIOES = {
    "Luanda": "lda",
    "Rio de Janeiro (não padrão)": "rjo",
    "Rio de Janeiro (padrão)": "rjx",
    "São Paulo (padrão)": "spx",
    "São Paulo (não padrão)": "spo",
    "Maputo (não padrão)": "map",
    "Maputo (padrão)": "mpx",
    "Lisboa (padrão)": "lbx",
    "Lisboa (não padrão)": "lbn",
    "Díli": "dli",
}

# ============================================================
# EXTRATOR DE TEXTO DO HTML
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
# LER UMA PÁGINA
# ============================================================

def ler_pagina(regiao, letra, start):

    params = {
        "action": "fonetica",
        "region": regiao,
        "act": "list",
        "letter": letra,
    }

    if start > 0:
        params["start"] = start

    # ========================================================
    # ACESSAR A PÁGINA
    # ========================================================

    tentativa = 1

    while tentativa <= MAX_TENTATIVAS:

        try:

            response = requests.get(
                BASE_URL,
                params=params,
                headers=HEADERS,
                timeout=30,
            )

            # ------------------------------------------------
            # VERIFICAR STATUS HTTP
            # ------------------------------------------------

            if response.status_code != 200:

                print(
                    f"⚠ Erro HTTP {response.status_code} "
                    f"em {regiao} / {letra.upper()} / "
                    f"start={start}"
                )

                if tentativa < MAX_TENTATIVAS:

                    print(
                        f"  Tentativa "
                        f"{tentativa}/{MAX_TENTATIVAS}. "
                        f"Aguardando {TEMPO_ESPERA}s..."
                    )

                    time.sleep(TEMPO_ESPERA)

                    tentativa += 1
                    continue

                raise requests.RequestException(
                    f"Erro HTTP {response.status_code}"
                )

            # ------------------------------------------------
            # REQUISIÇÃO BEM-SUCEDIDA
            # ------------------------------------------------

            break

        except requests.RequestException as erro:

            print(
                f"⚠ Erro ao acessar "
                f"{regiao} / {letra.upper()} / "
                f"start={start}"
            )

            print(
                f"  {erro}"
            )

            if tentativa >= MAX_TENTATIVAS:

                print()
                print(
                    "❌ Não foi possível acessar a página "
                    "após várias tentativas."
                )

                print(
                    "O crawler será interrompido para evitar "
                    "perda de dados."
                )

                raise

            print(
                f"  Tentativa "
                f"{tentativa}/{MAX_TENTATIVAS}. "
                f"Aguardando {TEMPO_ESPERA}s..."
            )

            time.sleep(TEMPO_ESPERA)

            tentativa += 1

    # ========================================================
    # LOCALIZAR A TABELA
    # ========================================================

    html = response.text

    inicio = html.find(
        "<table  cellpadding=4px id=rollovertable"
    )

    if inicio == -1:
        return []

    fim = html.find(
        "</table>",
        inicio
    )

    if fim == -1:
        return []

    tabela = html[inicio:fim]

    # ========================================================
    # SEPARAR OS TDs
    # ========================================================

    partes = tabela.split("<td")

    celulas = []

    for parte in partes:

        if ">" not in parte:
            continue

        conteudo = parte.split(">", 1)[1]

        if "<tr" in conteudo:
            conteudo = conteudo.split("<tr", 1)[0]

        parser = ExtratorTexto()

        parser.feed(conteudo)

        texto = parser.resultado()

        texto = texto.replace("\n", "")
        texto = texto.replace("\t", "")

        celulas.append(texto)

    # ========================================================
    # REMOVER CABEÇALHO
    # ========================================================

    celulas = celulas[1:]

    # ========================================================
    # TRANSFORMAR EM REGISTROS
    # ========================================================

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

    return linhas


# ============================================================
# BAIXAR UMA REGIÃO
# ============================================================

def baixar_regiao(nome_regiao, codigo_regiao):

    print()
    print("=" * 70)
    print(f"REGIÃO: {nome_regiao} ({codigo_regiao})")
    print("=" * 70)

    todos_dados = []

    # ========================================================
    # PERCORRER TODAS AS LETRAS
    # ========================================================

    for letra in LETRAS:

        start = 0
        total_letra = 0

        while True:

            dados = ler_pagina(
                regiao=codigo_regiao,
                letra=letra,
                start=start,
            )

            # =================================================
            # NÃO HÁ MAIS REGISTROS NESSA LETRA
            # =================================================

            if not dados:

                if start == 0:
                    print(
                        f"{letra.upper()}: "
                        f"nenhuma palavra"
                    )

                break

            # =================================================
            # ADICIONAR DADOS
            # =================================================

            todos_dados.extend(dados)

            quantidade = len(dados)

            total_letra += quantidade

            # =================================================
            # MOSTRAR SOMENTE A QUANTIDADE
            # =================================================

            print(
                f"{letra.upper()} "
                f"(start={start}): "
                f"{quantidade} palavras"
            )

            # =================================================
            # SE TIVER MENOS DE 20, ESSA É A ÚLTIMA PÁGINA
            # =================================================

            if quantidade < 20:
                break

            # =================================================
            # PRÓXIMA PÁGINA
            # =================================================

            start += 20

        # ====================================================
        # TOTAL DA LETRA
        # ====================================================

        if total_letra > 0:

            print(
                f"  → Total {letra.upper()}: "
                f"{total_letra} palavras"
            )

    # ========================================================
    # CRIAR DATAFRAME
    # ========================================================

    df = pd.DataFrame(
        todos_dados,
        columns=[
            "Palavra",
            "Categoria Gramatical",
            "Fonética",
        ]
    )

    # ========================================================
    # SALVAR CSV
    # ========================================================

    arquivo_csv = (
        PASTA_DATA /
        f"Dicionario_Fonetico_{codigo_regiao}.csv"
    )

    df.to_csv(
        arquivo_csv,
        index=False,
        encoding="utf-8-sig",
    )

    # ========================================================
    # RESULTADO DA REGIÃO
    # ========================================================

    print()

    print(
        f"✓ {nome_regiao} concluída"
    )

    print(
        f"✓ Total de registros: {len(df):,}"
    )

    print(
        f"✓ Arquivo: {arquivo_csv}"
    )

    return df


# ============================================================
# MENU DE REGIÕES
# ============================================================

def selecionar_regioes():

    choices = [
        ("🌎 Todas as regiões", "TODAS")
    ]

    for nome, codigo in REGIOES.items():

        choices.append(
            (nome, codigo)
        )

    questions = [

        inquirer.Checkbox(
            "regioes",

            message=(
                "Selecione as regiões que deseja baixar "
                "(Espaço = selecionar | Enter = confirmar)"
            ),

            choices=choices,

            validate=lambda _, resposta:
                len(resposta) > 0
                or "Selecione pelo menos uma região.",
        )
    ]

    respostas = inquirer.prompt(
        questions
    )

    if not respostas:
        return []

    selecionadas = respostas["regioes"]

    # ========================================================
    # TODAS AS REGIÕES
    # ========================================================

    if "TODAS" in selecionadas:

        return list(
            REGIOES.items()
        )

    # ========================================================
    # REGIÕES SELECIONADAS
    # ========================================================

    regioes_selecionadas = []

    for nome, codigo in REGIOES.items():

        if codigo in selecionadas:

            regioes_selecionadas.append(
                (nome, codigo)
            )

    return regioes_selecionadas


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("WEBCRAWLER - DICIONÁRIO FONÉTICO")
    print("Portal da Língua Portuguesa")
    print("=" * 70)

    print()

    print(
        "O crawler percorre todas as letras "
        "e todas as páginas disponíveis."
    )

    # ========================================================
    # SELECIONAR REGIÕES
    # ========================================================

    regioes = selecionar_regioes()

    if not regioes:

        print()

        print(
            "Nenhuma região selecionada. "
            "Encerrando."
        )

        return

    # ========================================================
    # MOSTRAR REGIÕES
    # ========================================================

    print()
    print("=" * 70)
    print("REGIÕES SELECIONADAS")
    print("=" * 70)

    for nome, codigo in regioes:

        print(
            f"✓ {nome} ({codigo})"
        )

    print("=" * 70)

    # ========================================================
    # BAIXAR REGIÕES
    # ========================================================

    for nome, codigo in regioes:

        baixar_regiao(
            nome_regiao=nome,
            codigo_regiao=codigo,
        )

    # ========================================================
    # FINAL
    # ========================================================

    print()
    print("=" * 70)
    print("🎉 DOWNLOAD FINALIZADO")
    print("=" * 70)

    print()

    print(
        f"Os arquivos estão salvos em:\n"
        f"{PASTA_DATA.resolve()}"
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()