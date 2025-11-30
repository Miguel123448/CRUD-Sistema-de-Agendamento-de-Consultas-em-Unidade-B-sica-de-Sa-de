import db
from datetime import datetime

STATUS_VALIDOS = ["AGENDADO", "AGENDADA", "CONCLUIDA", "CONCLUÍDA", "CANCELADA", "FALTA"]

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
                return True 
            return resultado[0] > 0
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"Erro na verificação de conflito: {e}")
        return True

def criar_consulta():
    print("--- Nova Consulta ---")

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
    except Exception as e:
        print(f"❌ ERRO ao conectar no banco: {e}")
        return

    try:
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

        while True:
            print("\n--- Agendamento ---")
            print("Informe a data da consulta:")
            
            dia = input("Dia (Ex: 05): ").strip()
            mes = input("Mês (Ex: 12): ").strip()
            ano = input("Ano (Ex: 2025): ").strip()
            
            print("Informe o horário:")
            hora = input("Hora (HH:MM): ").strip()

            try:
                data_hora_final = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)} {hora}:00"
                
                datetime.strptime(data_hora_final, '%Y-%m-%d %H:%M:%S')
                
                if datetime.strptime(data_hora_final, '%Y-%m-%d %H:%M:%S') < datetime.now():
                    print("❌ Você não pode agendar uma consulta no passado!")
                    continue

            except ValueError:
                print("❌ Data inválida! Verifique se o dia existe no mês (ex: 30 de Fevereiro) ou o formato da hora.")
                continue

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

def listar_consulta():
    print("\n--- Listagem de Consultas ---")

    try:
        conexao = db.obter_conexao()
        if conexao is None: return
        cursor = conexao.cursor()

        sql = """
            SELECT c.consulta_id, c.data_hora, p.nome, m.nome, c.status
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.idprontuario
            JOIN medicos m ON c.medico_id = m.medico_id
            ORDER BY c.data_hora
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

        if not resultados:
            print("📭 Nenhuma consulta agendada.")
            return

        print("-" * 85)
        print(f"{'ID':<4} | {'DATA/HORA':<18} | {'PACIENTE':<20} | {'MÉDICO':<15} | {'STATUS'}")
        print("-" * 85)

        for linha in resultados:
            id_con = linha[0]
            data = linha[1].strftime('%d/%m/%Y %H:%M')
            paciente = linha[2]
            medico = linha[3]
            status = linha[4]

            print(f"{id_con:<4} | {data:<18} | {paciente[:19]:<20} | {medico[:14]:<15} | {status}")
        
        print("-" * 85)

    except Exception as e:
        print(f"❌ Erro ao listar: {e}")
    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

def atualizar_consulta():
    print("\n--- Atualizar Consulta ---")

    try:
        conexao = db.obter_conexao()
        if conexao is None:
            return
        cursor = conexao.cursor()
    except Exception as e:
        print(f"❌ ERRO ao conectar no banco: {e}")
        return

    try:
        while True:
            consulta_id = input("ID da consulta que deseja atualizar: ").strip()
            
            if not consulta_id.isdigit():
                print("❌ ERRO: O ID deve ser um número.")
                continue

            sql = "SELECT medico_id, data_hora, status, observacoes FROM consultas WHERE consulta_id = %s"
            cursor.execute(sql, (consulta_id,))
            resultado = cursor.fetchone()

            if not resultado:
                print(f"❌ ERRO: Consulta {consulta_id} não encontrada.")
                continue
            
            medico_id_atual = resultado[0]
            data_atual = resultado[1]
            status_atual = resultado[2]
            obs_atual = resultado[3]
            
            data_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
            
            print(f"\n🔎 DADOS ATUAIS DA CONSULTA {consulta_id}:")
            print(f"   Data: {data_formatada}")
            print(f"   Status: {status_atual}")
            print(f"   Observação: {obs_atual}")
            break

        while True:
            print("\nO que você deseja alterar?")
            print("1. Status (Agendada/Concluída/Cancelada/Falta)")
            print("2. Data e Horário")
            print("3. Observações")
            print("4. Voltar (Cancelar operação)")
            
            opcao = input("Escolha uma opção (1-4): ").strip()

            if opcao == "1":
                while True:
                    print(f"Status Atual: {status_atual}")
                    novo_status = input("Novo Status (AGENDADA, CONCLUIDA, CANCELADA, FALTA): ").strip().upper()
                    
                    lista_status = ['AGENDADA', 'CONCLUIDA', 'CANCELADA', 'FALTA']
                    
                    if novo_status not in lista_status:
                        print(f"❌ Status inválido. Escolha entre: {lista_status}")
                        continue 

                    if novo_status != 'CANCELADA':
                        if verificar_conflito_horario(medico_id_atual, data_atual, consulta_id_existente=consulta_id):
                            print("\n❌ ERRO: Conflito de horário!")
                            print("Não é possível reativar esta consulta pois o horário já foi ocupado.")
                            break 

                    cursor.execute("UPDATE consultas SET status = %s WHERE consulta_id = %s", (novo_status, consulta_id))
                    conexao.commit()
                    print("✅ Status atualizado com sucesso!")
                    return

            elif opcao == "2":
                while True:
                    print("\nInforme a NOVA data e horário:")
                    dia = input("Dia (Ex: 05): ").strip()
                    mes = input("Mês (Ex: 12): ").strip()
                    ano = input("Ano (Ex: 2025): ").strip()
                    hora = input("Hora (HH:MM): ").strip()

                    try:
                        nova_data_hora = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)} {hora}:00"
                        if datetime.strptime(nova_data_hora, '%Y-%m-%d %H:%M:%S') < datetime.now():
                             print("❌ Data no passado não permitida.")
                             continue
                    except ValueError:
                        print("❌ Data inválida.")
                        continue

                    if verificar_conflito_horario(medico_id_atual, nova_data_hora, consulta_id_existente=consulta_id):
                        print("❌ Médico indisponível neste novo horário.")
                        continue 

                    cursor.execute("UPDATE consultas SET data_hora = %s WHERE consulta_id = %s", (nova_data_hora, consulta_id))
                    conexao.commit()
                    print("✅ Data reagendada com sucesso!")
                    return

            elif opcao == "3":
                print(f"Obs Atual: {obs_atual}")
                nova_obs = input("Digite a nova observação: ")
                
                cursor.execute("UPDATE consultas SET observacoes = %s WHERE consulta_id = %s", (nova_obs, consulta_id))
                conexao.commit()
                print("✅ Observação atualizada!")
                return

            elif opcao == "4":
                print("Operação cancelada.")
                return

            else:
                print("❌ Opção inválida.")

    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao atualizar: {e}")

    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

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