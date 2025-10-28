# CRUD Sistema de Agendamento de Consultas em Unidade Básica de Saúde
# Funções desenvolvidas
`carregar_dados(caminho)`

caminho: Diretório do arquivo que desejamos ler.
Retorna o carregamento do arquivo ou 0 caso não exista arquivo nesse diretório.

`salvar_dados(caminho,dados)`

Caminho: diretório do arquivo aonde desejamos salvar, configurado como 'w' - criar ou sobrescrever o que existir.
Dados: o dados que vamos salvar no arquivo, sempre utilizamos dicionário.
