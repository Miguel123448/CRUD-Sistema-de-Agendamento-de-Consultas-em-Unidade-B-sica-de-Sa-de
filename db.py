import mysql.connector

def obter_conexao():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='',
    )
    return conexao