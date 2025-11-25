import db
from datetime import datetime

def verificar_conflito_horario(medico_id, data_hora):
    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    comando = """
        SELECT COUNT(*)
        FROM consultas
        WHERE medico_id = %s
        AND data_hora = %s
    """

    valores = (medico_id, data_hora)
    cursor.execute(comando, valores)
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado[0] > 0

#CREAT - Criar uma Nova Consulta
def criar_consulta():
    paciente_id = input("ID do paciente: ")
    medico_id = input("ID do médico: ")
    data_hora = input("Data e hora (AAAA-MM-DD HH:MM:SS): ")
    status = input("Status (Agendada, Concluída, Cancelada): ")
    observacoes = input("Observações: ")

    if not paciente_id.isdigit():
        print("❌ O ID do paciente deve ser um número.")
        return

    if not medico_id.isdigit():
        print("❌ O ID do médico deve ser um número.")
        return

    if data_hora.strip() == "":
        print("❌ A data e hora não podem estar vazias.")
        return

    status_permitidos = ["Agendada", "Concluída", "Cancelada"]
    if status not in status_permitidos:
        print("❌ Status inválido. Escolha entre: Agendada, Concluída ou Cancelada.")
        return

    if verificar_conflito_horario(medico_id, data_hora):
        print("❌ Já existe uma consulta marcada para esse médico nesse horário.")
        return

    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    comando = """
        INSERT INTO consultas (paciente_id, medico_id, data_hora, status, observacoes)
        VALUES (?, ?, ?, ?, ?)
    """

    valores = (paciente_id, medico_id, data_hora, status, observacoes)
    cursor.execute(comando, valores)
    conexao.commit()
    conexao.close()

    print("Consulta criada com sucesso!")


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
    if not str(consulta_id).isdigit():
        print("\n❌ ERRO: ID da consulta inválido.")
        return
    consulta_id = int(consulta_id)

    try:
        datetime.strptime(nova_data_hora, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("\n❌ ERRO: Data e hora no formato inválido. Use: AAAA-MM-DD HH:MM:SS")
        return

    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT medico_id FROM consultas WHERE consulta_id = %s", (consulta_id,))
    row = cursor.fetchone()
    if not row:
        print("\n❌ ERRO: Consulta não encontrada.")
        cursor.close()
        conexao.close()
        return
    medico_id = row[0]

    conflito_sql = "SELECT COUNT(*) FROM consultas WHERE medico_id = %s AND data_hora = %s AND consulta_id <> %s"
    cursor.execute(conflito_sql, (medico_id, nova_data_hora, consulta_id))
    (contagem,) = cursor.fetchone()
    if contagem > 0:
        print("\n❌ ERRO: Conflito de horário — já existe outra consulta para esse médico nesse horário.")
        cursor.close()
        conexao.close()
        return

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