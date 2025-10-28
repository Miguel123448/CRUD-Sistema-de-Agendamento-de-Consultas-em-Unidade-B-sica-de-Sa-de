# CRUD Sistema de Agendamento de Consultas em Unidade Básica de Saúde
# Funções desenvolvidas
`carregar_dados(caminho)`

caminho: Diretório do arquivo que desejamos ler.
Retorna o carregamento do arquivo ou 0 caso não exista arquivo nesse diretório.

`salvar_dados(caminho,dados)`

Caminho: diretório do arquivo aonde desejamos salvar, configurado como 'w' - criar ou sobrescrever o que existir.
Dados: o dados que vamos salvar no arquivo, sempre utilizamos dicionário.

# Resumo funções (Python)

# Arquivos
| Função             | Verifica se...   | Retorna `True` quando...           |
| ------------------ | ---------------- | ---------------------------------- |
| `os.path.exists()` | O caminho existe | O arquivo ou pasta existe          |
| `os.path.isfile()` | É um arquivo     | O caminho é um arquivo existente   |
| `os.path.isdir()`  | É uma pasta      | O caminho é um diretório existente |

# Open

open(arquivo, modo, encoding)

| Parâmetro  | Descrição                                                      |
| ---------- | -------------------------------------------------------------- |
| `arquivo`  | Caminho ou nome do arquivo (ex: `"dados.txt"`)                 |
| `modo`     | Define como o arquivo será aberto (leitura, escrita, etc.)     |
| `encoding` | (opcional) Define a codificação de texto, geralmente `"utf-8"` |

| Modo  | Significado | O que faz                                             |
| ----- | ----------- | ----------------------------------------------------- |
| `'r'` | **read**    | Abre o arquivo para **leitura** (erro se não existir) |
| `'w'` | **write**   | Abre para **escrita** (cria ou **sobrescreve**)       |
| `'a'` | **append**  | Abre para **acrescentar** dados ao final              |
| `'x'` | **create**  | Cria um novo arquivo (**erro se já existir**)         |
| `'b'` | **binary**  | Abre em modo **binário** (para imagens, PDFs etc.)    |
| `'t'` | **text**    | Modo **texto** (padrão)                               |
| `'+'` | **update**  | Permite **leitura e escrita** no mesmo arquivo        |

- Usando with open() (maneira recomendada)
A forma moderna e segura é usar o gerenciador de contexto with, que fecha o arquivo automaticamente:
```
with open("dados.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
    print(conteudo)
# aqui o arquivo já foi fechado automaticamente
```
