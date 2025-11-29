# CRUDconsultas.py
import db
from datetime import datetime

STATUS_VALIDOS = ["AGENDADO", "AGENDADA", "CONCLUIDA", "CONCLUÍDA", "CANCELADA"]

def verificar_conflito_horario(medico_id, data_hora, consulta_id_existente=None):
    try:
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

            cursor.execute(comando, valores)
            resultado = cursor.fetchone()
            if resultado is None:
                return True  # tratamos como conflito/erro para segurança
            return resultado[0] > 0
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"Erro na verificação de conflito: {e}")
        return True  # em caso de erro, considerar como conflito para evitar marcação inválida



# CREATE

def criar_consulta():
    print("--- Nova Consulta ---")

    # Tenta abrir conexão e cursor - se falhar, retorna
    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
    except Exception as e:
        print(f"❌ ERRO ao conectar no banco: {e}")
        return

    try:
        # valida paciente
        while True:
            paciente_id = input("ID do paciente: ").strip()
            if not paciente_id.isdigit():
                print("❌ ERRO: O ID do paciente deve ser um número.")
                continue

            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE idprontuario = %s", (paciente_id,))
            resultado = cursor.fetchone()
            if not resultado or resultado[0] == 0:
                print(f"❌ Erro: Paciente com ID {paciente_id} não encontrado.")
                continue

            break

        # valida medico
        while True:
            medico_id = input("ID do médico: ").strip()
            if not medico_id.isdigit():
                print("❌ ERRO: O ID do médico deve ser um número.")
                continue

            cursor.execute("SELECT COUNT(*) FROM medicos WHERE medico_id = %s", (medico_id,))
            resultado = cursor.fetchone()
            if not resultado or resultado[0] == 0:
                print(f"❌ Erro: Médico com ID {medico_id} não encontrado.")
                continue

            break

        # data/hora e conflito
        while True:
            print("\n--- Agendamento ---")
            data_consulta = input("Data (AAAA-MM-DD): ").strip()
            hora_consulta = input("Hora (HH:MM): ").strip()

            data_hora_final = f"{data_consulta} {hora_consulta}:00"
            try:
                # valida formato
                datetime.strptime(data_hora_final, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print("❌ Data ou Hora inválidas! Verifique se usou o formato correto.")
                print("Exemplo Data: 2024-12-25 | Exemplo Hora: 14:30")
                continue

            # verifica conflito
            if verificar_conflito_horario(medico_id, data_hora_final):
                print("❌ Médico indisponível neste horário. Escolha outro.")
                continue

            break

        observacoes = input("Observações: ").strip()
        status = "AGENDADO"

        try:
            comando = """
                INSERT INTO consultas (paciente_id, medico_id, data_hora, status, observacoes) 
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (paciente_id, medico_id, data_hora_final, status, observacoes)
            cursor.execute(comando, valores)
            conexao.commit()
            print("\n✅ Consulta agendada com sucesso!")
        except Exception as e:
            conexao.rollback()
            print(f"❌ Erro ao salvar: {e}")

    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conexao.close()
        except:
            pass



# READ

def listar_consulta():
    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
    except Exception as e:
        print(f"❌ Erro ao conectar no banco: {e}")
        return

    try:
        cursor.execute("SELECT * FROM consultas")
        resultado = cursor.fetchall()
        print("\n Consultas cadastradas:")
        for consulta in resultado:
            print(consulta)
    except Exception as e:
        print(f"❌ Erro ao listar consultas: {e}")
    finally:
        cursor.close()
        conexao.close()



# UPDATE

def atualizar_consulta():
    print("\n--- Atualizar Consulta ---")

    # conecta
    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
    except Exception as e:
        print(f"❌ ERRO ao conectar no banco: {e}")
        return

    try:
        # pede e valida consulta_id e obtém medico_id atual
        consulta_id = input("ID da consulta que deseja atualizar: ").strip()
        if not consulta_id.isdigit():
            print("\n❌ ERRO: O ID da consulta deve ser um número.\n")
            return

        cursor.execute("SELECT medico_id FROM consultas WHERE consulta_id = %s", (consulta_id,))
        resultado = cursor.fetchone()
        if not resultado:
            print("\n❌ ERRO: Consulta não encontrada.\n")
            return

        medico_id = resultado[0]  # pega médico associado à consulta

        # pede e valida novo status
        novo_status = input("Novo status (Agendada, Concluída, Cancelada): ").strip()
        # normaliza para maiúsculas sem acento para comparação simples
        novo_status_normalizado = novo_status.upper().replace("Á", "A").replace("Ç", "C").replace("Í", "I").replace("Ú", "U").replace("Ó", "O").replace("É", "E")
        if novo_status_normalizado not in [s.replace("Á", "A").replace("Ã","A") for s in STATUS_VALIDOS]:
            print("\n❌ ERRO: Status inválido. Use: Agendada, Concluída ou Cancelada.\n")
            return

        # pede e valida nova data/hora
        nova_data_hora = input("Nova data e hora (AAAA-MM-DD HH:MM:SS): ").strip()
        try:
            datetime.strptime(nova_data_hora, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("\n❌ ERRO: Data e hora no formato inválido. Use: AAAA-MM-DD HH:MM:SS\n")
            return

        # verifica conflito (passando o id da consulta para ignorá-la)
        if verificar_conflito_horario(medico_id, nova_data_hora, consulta_id_existente=consulta_id):
            print("\n❌ ERRO: Já existe uma consulta marcada para este médico nesse horário.\n")
            return

        # atualiza
        comando = 'UPDATE consultas SET status = %s, data_hora = %s WHERE consulta_id = %s'
        valores = (novo_status, nova_data_hora, consulta_id)
        cursor.execute(comando, valores)
        conexao.commit()
        print("\n--- Consulta atualizada com sucesso!! ---")

    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao atualizar consulta: {e}")
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conexao.close()
        except:
            pass



# DELETE

def deletar_consulta():
    print("\n--- Excluir Consulta ---")

    consulta_id = input("ID da consulta que deseja excluir: ").strip()
    if not consulta_id.isdigit():
        print("\n❌ ERRO: O ID da consulta deve ser um número.\n")
        return

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
    except Exception as e:
        print(f"❌ Erro ao conectar no banco: {e}")
        return

    try:
        comando = 'DELETE FROM consultas WHERE consulta_id = %s'
        valor = (consulta_id,)
        cursor.execute(comando, valor)
        conexao.commit()
        print("\n--- Consulta excluída com sucesso!! ---")
    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao excluir consulta: {e}")
    finally:
        cursor.close()
        conexao.close()
