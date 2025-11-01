import db

# CREATE
def criar_tabela():
    conexao = db.obter_conexao() # obtém a conexão do banco de dados
    cursor = conexao.cursor()    # cria o cursor para executar comandos SQL
    nome_produto = "chocolate"
    valor = 15
    comando = "INSERT INTO vendas (nome_produto, valor) VALUES (%s, %s)" # o comando dessa forma evita SQL Injection
    cursor.execute(comando, (nome_produto, valor)) #insere no banco de dados
    conexao.commit() # salva no banco de dados
    cursor.close()  # fecha o cursor


# READ
def ler_produtos():
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = 'SELECT * FROM vendas'
    cursor.execute(comando)
    resultado = cursor.fetchall() # ler o banco de dados inteiro, retorna uma lista de tuplas também temos o fetchone() que retorna apenas o primeiro resultado e o fetchmany(n) que retorna os n primeiros resultados
    cursor.close()
    conexao.close()
    return resultado


# UPDATE
def editar_valor(nome, novo_valor):
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = "UPDATE vendas SET valor = %s WHERE nome_produto = %s" # o WHERE procura pelo nome do produto
    cursor.execute(comando, (novo_valor, nome))
    conexao.commit() # edita o banco de dados
    cursor.close()
    conexao.close()


# DELETE
def apagar_produto(nome):
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = 'DELETE FROM vendas WHERE nome_produto = %s'
    cursor.execute(comando, (nome,))
    conexao.commit() # edita o banco de dados
    cursor.close()
    conexao.close()