import db
from datetime import datetime

def verificar_conflito_horario(medico_id, data_hora, consulta_id_existente=None):
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    try:
        if consulta_id_existente:
            comando = """
            SELECT COUNT(*) FROM consultas
            WHERE medico_id = %s 
            AND data_hora = %s 
            AND consulta_id != %s
            AND status != 'CANCELADA' 
        """
            valores = (medico_id, data_hora, consulta_id_existente)
        else:
            comando = """
            SELECT COUNT(*) FROM consultas
            WHERE medico_id = %s 
            AND data_hora = %s
            AND status != 'CANCELADA' 
        """
            valores = (medico_id, data_hora)           
        cursor.execute(comando,valores)
        resultado = cursor.fetchone()[0]
        return resultado > 0
    
    except Exception as e:
        print(f"Erro na verificação: {e}")
        return True

    finally:
        cursor.close()
        conexao.close()

#CREAT - Criar uma Nova Consulta
def criar_consulta():
    print("--- Nova Consulta ---")

    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    while True:
        paciente_id = input("ID do paciente: ").strip()

        if not paciente_id.isdigit():
            print("❌ ERRO: O ID do paciente deve ser um número.")
            continue

        cursor.execute("SELECT COUNT(*) FROM pacientes WHERE idprontuario = %s", (paciente_id,))
        if cursor.fetchone()[0] == 0:
            print(f"❌ Erro: Paciente com ID {paciente_id} não encontrado.")
            continue

        break

    while True:
        medico_id = input("ID do médico: ").strip()

        if not medico_id.isdigit():
            print("❌ O ID do médico deve ser um número.")
            continue

        cursor.execute("SELECT COUNT(*) FROM medicos WHERE medico_id = %s", (medico_id,))
        if cursor.fetchone()[0] == 0:
            print(f"❌ Erro: Médico com ID {medico_id} não encontrado.")
            continue
        
        break
    
    while True:
        print("\n--- Agendamento ---")
        data_consulta = input("Data (AAA-MM-DD): ").strip()
        hora_consulta = input("Hora (HH:MM): ").strip()
        
        data_hora_final = f"{data_consulta} {hora_consulta}:00"
        try:
            datetime.strptime(data_hora_final, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            print("❌ Data ou Hora inválidas! Verifique se usou o formato correto.")
            print("Exemplo Data: 2024-12-25 | Exemplo Hora: 14:30")
            continue
        if verificar_conflito_horario(medico_id, data_hora_final):
            print("❌ Médico indisponível neste horário. Escolha outro.")
            continue
            
        break

    observacoes = input("Observações: ")
    status = "AGENDADO"
    
    try:
        comando = """
            INSERT INTO consultas (paciente_id, medico_id, data_hora, status, observacoes) 
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (paciente_id, medico_id, data_hora_final, status, observacoes)

        cursor.execute(comando, valores)
        conexao.commit()
        
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        
    finally:
        cursor.close()
        conexao.close()

    print("\n✅ Consulta agendada com sucesso!")


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

    if not consulta_id.isdigit():
        print("\n❌ ERRO: O ID da consulta deve ser um número.\n")
        return

    status_valido = ["Agendada", "Concluída", "Cancelada"]
    if novo_status not in status_valido:
        print("\n❌ ERRO: Status inválido. Use: Agendada, Concluída ou Cancelada.\n")
        return

    try:
        datetime.strptime(nova_data_hora, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("\n❌ ERRO: Data e hora no formato inválido. Use: AAAA-MM-DD HH:MM:SS\n")
        return

    # --- Verificação de conflito de horário ---
    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    # Busca o médico da consulta que será atualizada
    cursor.execute("SELECT medico_id FROM consultas WHERE consulta_id = %s", (consulta_id,))
    resultado = cursor.fetchone()
    if not resultado:
        print("\n❌ ERRO: Consulta não encontrada.\n")
        cursor.close()
        conexao.close()
        return

    medico_id = resultado[0]

    # Checa se há conflito com outra consulta
    if verificar_conflito_horario(medico_id, nova_data_hora, consulta_id_existente=consulta_id):
        print("\n❌ ERRO: Já existe uma consulta marcada para este médico nesse horário.\n")
        cursor.close()
        conexao.close()
        return

    # Atualiza consulta
    comando = 'UPDATE consultas SET status = %s, data_hora = %s WHERE consulta_id = %s'
    valores = (novo_status, nova_data_hora, consulta_id)
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

    print("\n--- Consulta atualizada com sucesso!! ---")

#DELETE - Excluir uma consulta
def deletar_consulta():
    print("\n--- Excluir Consulta ---")
    consulta_id = input("ID da consulta que deseja excluir: ")

    if not consulta_id.isdigit():
        print("\n❌ ERRO: O ID da consulta deve ser um número.\n")
        return

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
           deletar_consulta()

        case "5":
            print("Encerrando o sistema...")
            break

        case _:
            print(" \n--- Opção inválida! Tente novamente! ---")