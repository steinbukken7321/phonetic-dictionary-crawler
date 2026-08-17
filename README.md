# 🗣️ Web Crawler — Dicionário Fonético

Web crawler desenvolvido em Python para realizar a coleta automática de **palavras, categorias gramaticais e transcrições fonéticas** disponibilizadas pelo Dicionário Fonético do [Portal da Língua Portuguesa](https://www.portaldalinguaportuguesa.org/).

O projeto realiza requisições HTTP ao portal, identifica a tabela de resultados, extrai os registros e organiza os dados em arquivos CSV separados por região.

---

## 📌 Sobre o projeto

O crawler foi desenvolvido para automatizar a coleta dos dados fonéticos disponíveis no portal.

Para cada região selecionada, o programa:

1. Acessa as páginas do Dicionário Fonético;
2. Percorre as letras do alfabeto;
3. Percorre automaticamente as páginas utilizando o parâmetro `start`;
4. Localiza a tabela `rollovertable`;
5. Extrai os dados presentes nas células HTML;
6. Organiza os registros em:
   - Palavra;
   - Categoria Gramatical;
   - Fonética;
7. Gera um arquivo CSV para cada região.

### Fluxo geral

```text
                  Portal da Língua Portuguesa
                             │
                             ▼
                         requests
                             │
                             ▼
                         Página HTML
                             │
                             ▼
                    tabela rollovertable
                             │
                             ▼
                        HTMLParser
                             │
                             ▼
             Palavra / Categoria / Fonética
                             │
                             ▼
                           Pandas
                             │
                             ▼
                       Arquivo CSV
                             │
                             ▼
                           data/
```

---

# 📁 Estrutura do projeto

```text
dicionario-fonetico/
│
├── .venv/
│   └── Ambiente virtual Python
│
├── data/
│   └── Dicionario_Fonetico_*.csv
│
├── debug/
│   ├── resultados/
│   │   ├── debug_01_pagina.html
│   │   ├── debug_02_tabela_rollovertable.html
│   │   ├── debug_03_tds.txt
│   │   └── debug_04_registros.csv
│   │
│   ├── debug_01_acesso_pagina.py
│   ├── debug_02_estrutura_tabela.py
│   ├── debug_03_leitura_tds.py
│   └── debug_04_extracao_registros.py
│
├── .gitignore
├── Guia_Web_Crawler_Dicionario_Fonetico.pdf
├── main.py
├── README.md
└── requirements.txt
```

### Principais arquivos e diretórios

| Arquivo / Pasta | Descrição |
|---|---|
| `main.py` | Crawler principal responsável pela coleta dos dados |
| `requirements.txt` | Dependências Python utilizadas pelo projeto |
| `README.md` | Documentação resumida do projeto |
| `Guia_Web_Crawler_Dicionario_Fonetico.pdf` | Guia completo de configuração e utilização |
| `debug/` | Scripts utilizados durante a investigação e desenvolvimento |
| `debug/resultados/` | Arquivos gerados pelos testes de debug |
| `data/` | Armazena os arquivos CSV gerados pelo crawler |
| `.venv/` | Ambiente virtual Python |

> **Observação:** `.venv/`, `data/` e `debug/resultados/` são diretórios destinados ao ambiente local e aos dados/resultados gerados durante a execução. Eles não devem ser versionados no Git.

---

# ⚙️ Tecnologias utilizadas

O projeto utiliza:

- **Python**
- **Requests**
- **Pandas**
- **Inquirer**
- **HTMLParser**

### Requests

Utilizado para realizar as requisições HTTP ao Portal da Língua Portuguesa.

### Pandas

Utilizado para organizar os registros coletados e gerar os arquivos CSV.

### Inquirer

Utilizado para criar o menu interativo de seleção das regiões.

### HTMLParser

Utilizado para interpretar e extrair informações do HTML.

O `HTMLParser` faz parte da biblioteca padrão do Python e, portanto, não precisa ser instalado separadamente.

---

# 🐍 Requisitos

Antes de executar o projeto, é necessário possuir:

- Python 3.x;
- pip;
- Git (opcional, caso o projeto seja versionado);
- conexão com a Internet.

Recomenda-se utilizar um ambiente virtual Python (`.venv`).

---

# 🚀 Instalação

## 1. Clonar o repositório

```powershell
git clone https://github.com/SEU_USUARIO/dicionario-fonetico.git
```

Entre na pasta:

```powershell
cd dicionario-fonetico
```

---

## 2. Criar o ambiente virtual

No Windows:

```powershell
py -m venv .venv
```

---

## 3. Ativar o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Após a ativação, o terminal deverá apresentar algo semelhante a:

```text
(.venv) PS C:\...\dicionario-fonetico>
```

---

## 4. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
python -m pip install --upgrade pip
```

Depois:

```powershell
python -m pip install -r requirements.txt
```

---

## 5. Verificar a instalação

Execute:

```powershell
python -c "import requests, pandas, inquirer; print('Todas as dependencias foram instaladas corretamente!')"
```

Se aparecer:

```text
Todas as dependencias foram instaladas corretamente!
```

o ambiente está configurado.

---

# ▶️ Executando o crawler

Com o ambiente virtual ativado:

```powershell
python main.py
```

O programa apresentará um menu interativo para seleção das regiões.

Utilize:

- `Espaço` → selecionar/desmarcar uma região;
- `Enter` → confirmar a seleção.

Também é possível selecionar:

```text
Todas as regiões
```

---

# 🌎 Regiões disponíveis

O crawler atualmente trabalha com as seguintes regiões:

| Região | Código |
|---|---|
| Luanda | `lda` |
| Rio de Janeiro (não padrão) | `rjo` |
| Rio de Janeiro (padrão) | `rjx` |
| São Paulo (padrão) | `spx` |
| São Paulo (não padrão) | `spo` |
| Maputo (não padrão) | `map` |
| Maputo (padrão) | `mpx` |
| Lisboa (padrão) | `lbx` |
| Lisboa (não padrão) | `lbn` |
| Díli | `dli` |

---

# 🔎 Funcionamento da coleta

Para cada região selecionada, o crawler percorre automaticamente as letras:

```text
a → b → c → ... → z
```

Para cada letra, o portal utiliza paginação através do parâmetro:

```text
start
```

Exemplo:

```text
start=0
start=20
start=40
start=60
...
```

Cada página normalmente contém até 20 registros.

Quando uma página possui menos de 20 registros, o crawler considera que chegou ao final daquela letra.

---

# 📊 Dados coletados

Cada registro possui três informações principais:

| Campo | Descrição |
|---|---|
| `Palavra` | Palavra encontrada no dicionário |
| `Categoria Gramatical` | Classificação gramatical da palavra |
| `Fonética` | Transcrição fonética correspondente |

Exemplo:

```text
Palavra              Categoria Gramatical      Fonética

a                    artigo                    a
a                    preposição                a
á-bê-cê              nome masculino            ˌa.bˌe.sˈe
a-pro·pó·si·to       nome masculino            a.pɾo.pˈɔ.zi.tʊ
```

---

# 💾 Arquivos gerados

Os dados são armazenados na pasta:

```text
data/
```

O nome do arquivo utiliza o código da região.

Exemplos:

```text
data/Dicionario_Fonetico_lda.csv
data/Dicionario_Fonetico_lbx.csv
data/Dicionario_Fonetico_rjx.csv
```

Os arquivos são salvos utilizando:

```python
encoding="utf-8-sig"
```

Isso permite preservar corretamente:

- acentos;
- caracteres especiais;
- símbolos do Alfabeto Fonético Internacional (IPA).

Também facilita a abertura dos arquivos no Excel.

---

# 🧪 Testes e Debug

A pasta `debug/` contém scripts desenvolvidos durante a investigação da estrutura do site.

Eles documentam as etapas utilizadas para compreender como os dados estavam organizados no HTML.

## Debug 01 — Acesso à página

```text
debug/debug_01_acesso_pagina.py
```

Verifica:

- acesso à página;
- status HTTP;
- URL final;
- tamanho da resposta;
- encoding.

---

## Debug 02 — Estrutura da tabela

```text
debug/debug_02_estrutura_tabela.py
```

Localiza a tabela:

```html
<table id="rollovertable">
```

e analisa sua estrutura.

---

## Debug 03 — Leitura dos `<td>`

```text
debug/debug_03_leitura_tds.py
```

Analisa como os dados estão distribuídos nas células HTML.

A investigação identificou a sequência:

```text
Palavra
Categoria
Fonética
Palavra
Categoria
Fonética
...
```

---

## Debug 04 — Extração dos registros

```text
debug/debug_04_extracao_registros.py
```

Valida a transformação dos dados HTML em registros estruturados:

```text
Palavra
Categoria Gramatical
Fonética
```

---

## Fluxo de desenvolvimento

```text
DEBUG 01
   │
   ▼
A página pode ser acessada?
   │
   ▼
DEBUG 02
   │
   ▼
Onde está a tabela?
   │
   ▼
DEBUG 03
   │
   ▼
Como os TDs estão organizados?
   │
   ▼
DEBUG 04
   │
   ▼
Como transformar os dados em registros?
   │
   ▼
main.py
   │
   ▼
Crawler completo
```

---

# 🛠️ Executar os testes de debug

Exemplo:

```powershell
python debug\debug_01_acesso_pagina.py
```

Os demais podem ser executados com:

```powershell
python debug\debug_02_estrutura_tabela.py
```

```powershell
python debug\debug_03_leitura_tds.py
```

```powershell
python debug\debug_04_extracao_registros.py
```

Os arquivos produzidos pelos testes são armazenados em:

```text
debug/resultados/
```

---

# 🧹 Organização e versionamento

O projeto possui um `.gitignore` configurado para evitar o versionamento de arquivos gerados localmente.

Não devem ser enviados ao Git:

```text
.venv/
data/
debug/resultados/
```

Os principais arquivos versionados são:

```text
main.py
requirements.txt
README.md
Guia_Web_Crawler_Dicionario_Fonetico.pdf
.gitignore
debug/
```

---

# 📖 Guia completo

Para obter instruções detalhadas de configuração, execução, troubleshooting e versionamento, consulte:

**[Guia Web Crawler — Dicionário Fonético](Guia_Web_Crawler_Dicionario_Fonetico.pdf)**

O guia contém explicações detalhadas sobre:

- configuração do Python;
- criação do ambiente virtual;
- instalação das dependências;
- execução do crawler;
- funcionamento da paginação;
- regiões disponíveis;
- geração dos CSVs;
- códigos de debug;
- configuração do Git;
- publicação no GitHub;
- problemas comuns;
- comandos úteis.

---

# ⚠️ Problemas comuns

### PowerShell bloqueando o ambiente virtual

Execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Biblioteca não encontrada

Verifique se o ambiente virtual está ativo e execute:

```powershell
python -m pip install -r requirements.txt
```

### `requirements.txt` não encontrado

Confirme que o terminal está localizado na raiz do projeto:

```powershell
dir
```

Devem aparecer:

```text
main.py
requirements.txt
README.md
```

### CSV não aparece

Verifique se o crawler terminou sem erros:

```powershell
dir data
```

### Caracteres incorretos no CSV

Os arquivos utilizam:

```python
encoding="utf-8-sig"
```

para preservar os caracteres especiais e fonéticos.

---

# ⛔ Interromper a execução

Para interromper o crawler:

```text
Ctrl + C
```

> O crawler atual não possui sistema de checkpoint. Caso seja interrompido, uma nova execução da região começará novamente do início.

---


# 📚 Fonte dos dados

Os dados são coletados do:

**Dicionário Fonético — Portal da Língua Portuguesa**

https://www.portaldalinguaportuguesa.org/

Os dados utilizados pelo crawler são provenientes de uma fonte externa.

Antes de redistribuir os dados coletados, recomenda-se verificar os termos de uso e as condições de acesso do portal.

---

# 📌 Resumo

```text
Instalar Python
      │
      ▼
Criar .venv
      │
      ▼
Ativar ambiente virtual
      │
      ▼
Instalar requirements.txt
      │
      ▼
Executar main.py
      │
      ▼
Selecionar regiões
      │
      ▼
Percorrer letras A–Z
      │
      ▼
Percorrer páginas
start=0,20,40,...
      │
      ▼
Extrair dados
      │
      ▼
Palavra / Categoria / Fonética
      │
      ▼
Pandas
      │
      ▼
CSV
      │
      ▼
data/
```

---

# 👨‍💻 Projeto

**Web Crawler — Dicionário Fonético**

Projeto desenvolvido em Python para automação da coleta e organização de dados fonéticos do Portal da Língua Portuguesa.
