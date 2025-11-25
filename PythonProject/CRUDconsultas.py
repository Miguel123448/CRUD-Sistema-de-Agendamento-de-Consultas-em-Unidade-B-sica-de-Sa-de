import db
from datetime import datetime

#CREAT - Criar uma Nova Consulta
def criar_consulta():
    print("\n--- Cadastro de Nova Consulta ---")

    paciente_id = input("ID do paciente: ")
    medico_id = input("ID do médico: ")
    data_hora = input("Data e hora (AAAA-MM-DD HH:MM:SS): ")
    status = input("Status (Agendada, Concluída, Cancelada): ")
    observacoes = input("Observações: ")

    if not paciente_id.isdigit() or not medico_id.isdigit():
        print("\n❌ ERRO: O ID do paciente e o ID do médico devem ser números.\n")
        return

    try:
        datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("\n❌ ERRO: Data e hora no formato inválido.\nUse: AAAA-MM-DD HH:MM:SS\n")
        return

    status_valido = ["Agendada", "Concluída", "Cancelada"]
    if status not in status_valido:
        print("\n❌ ERRO: Status inválido. Use: Agendada, Concluída ou Cancelada.\n")
        return

    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    comando = """
        INSERT INTO consultas (paciente_id, medico_id, data_hora, status, observacoes)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (paciente_id, medico_id, data_hora, status, observacoes)

    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

    print("\n--- Consulta cadastrada com sucesso!! ---")


#READ - Ler/Listar as consultas
def listar_consulta():
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM consultas")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    print("\n Consultas cadastradas:")
    for consultas in resultado:
        print(consultas)
    
#UPDATE - Atualizar uma Consulta
def atualizar_consulta(consulta_id, novo_status, nova_data_hora):
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = 'UPDATE consultas SET status = %s, data_hora = %s WHERE consulta_id = %s'
    valores = (novo_status, nova_data_hora, consulta_id)
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()
    print("\n--- Consulta atualizada com sucesso!! ---")

#DELETE - Excluir uma consulta
def deletar_consulta(consulta_id):
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = 'DELETE FROM consultas WHERE consulta_id = %s'
    valor = (consulta_id,)
    cursor.execute(comando, valor)
    conexao.commit()
    cursor.close()
    conexao.close()
    print("\n--- Consulta excluída com sucesso!! ---")

#Menu para teste do CRUD
while True:
    print("\n--- Sistema de Consultas UBS ---")
    print("1. Cadastrar nova consulta")
    print("2. Listar consultas")
    print("3. Atualizar consulta")
    print("4. Excluir consulta")
    print("5. Sair")

    opcao = input("\nEscolha uma opção: ")

    match opcao:
        case "1":
            criar_consulta()

        case "2":
            listar_consulta()

        case "3":
            consulta_id = input("ID da consulta que deseja atualizar: ")
            novo_status = input("Novo status: ")
            nova_data_hora = input("Nova data e hora (AAAA-MM-DD HH:MM:SS): ")
            atualizar_consulta(consulta_id, novo_status, nova_data_hora)

        case "4":
            consulta_id = input("ID da consulta que deseja excluir: ")
            deletar_consulta(consulta_id)

        case "5":
            print("Encerrando o sistema...")
            break

        case _:
            print(" \n--- Opção inválida! Tente novamente! ---")