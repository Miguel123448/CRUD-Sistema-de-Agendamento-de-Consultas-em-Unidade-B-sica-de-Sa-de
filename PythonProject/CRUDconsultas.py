import db
from datetime import datetime

def verificar_conflito_horario(medico_id, data_hora):
    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    comando = "SELECT COUNT(*) FROM consultas WHERE medico_id = %s AND data_hora = %s"
    cursor.execute(comando, (medico_id, data_hora))
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
def atualizar_consulta():
    print("\n--- Atualizar Consulta ---")

    consulta_id = input("ID da consulta que deseja atualizar: ")
    novo_status = input("Novo status (Agendada, Concluída, Cancelada): ")
    nova_data_hora = input("Nova data e hora (AAAA-MM-DD HH:MM:SS): ")

    # Validações
    if not consulta_id.isdigit():
        print("\n❌ ERRO: ID da consulta deve ser um número.")
        return

    status_valido = ["Agendada", "Concluída", "Cancelada"]
    if novo_status not in status_valido:
        print("\n❌ ERRO: Status inválido. Use: Agendada, Concluída ou Cancelada.")
        return

    from datetime import datetime
    try:
        datetime.strptime(nova_data_hora, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("\n❌ ERRO: Data e hora no formato inválido. Use AAAA-MM-DD HH:MM:SS")
        return

    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    # Buscar médico vinculado à consulta
    cursor.execute("SELECT medico_id FROM consultas WHERE consulta_id = %s", (consulta_id,))
    resultado = cursor.fetchone()

    if not resultado:
        print("\n❌ ERRO: Consulta não encontrada.")
        return

    medico_id = resultado[0]

    # Verificar conflito de horário
    if verificar_conflito_horario(medico_id, nova_data_hora):
        print("\n❌ ERRO: Já existe uma consulta marcada para esse médico nesse horário.")
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
            atualizar_consulta()

        case "4":
            consulta_id = input("ID da consulta que deseja excluir: ")
            deletar_consulta(consulta_id)

        case "5":
            print("Encerrando o sistema...")
            break

        case _:
            print(" \n--- Opção inválida! Tente novamente! ---")