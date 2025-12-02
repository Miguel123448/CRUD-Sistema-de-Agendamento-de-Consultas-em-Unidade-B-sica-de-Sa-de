import db
import mysql.connector


def relatorioMedicos():
    conexao = None
    cursor = None

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("SELECT medico_id, nome FROM medicos")
        medicos = cursor.fetchall()

        print("\nMédicos cadastrados ---")
        print("ID | Nome")
        print("-------------------")
        for medico in medicos:
            print(f"{medico[0]} - {medico[1]}")

        IdMedico = input("\nEscreva o ID do médico que você quer gerar o relatório: ").strip()
        if not IdMedico.isdigit():
            print("\nID inválido. Digite apenas números.")
            return

        cursor.execute("SELECT nome FROM medicos WHERE medico_id = %s", (IdMedico,))
        nomeMedico = cursor.fetchone()
        if not nomeMedico:
            print("\nNenhum médico encontrado com esse ID.")
            return

        print(f"\nSeu médico selecionado é {nomeMedico[0]}")

        cursor.execute("SELECT * FROM consultas WHERE medico_id = %s", (IdMedico,))
        consultas = cursor.fetchall()

        if not consultas:
            print("\nNenhuma consulta encontrada para este médico.")
            return

        print("\nConsultas do médico selecionado:\n")

        for consulta in consultas:
            consulta_id = consulta[0]
            paciente_id = consulta[1]
            medico_id = consulta[2]

            cursor.execute("SELECT nome FROM pacientes WHERE idprontuario = %s", (paciente_id,))
            nomePaciente = cursor.fetchone()

            print("\n========== INFORMAÇÕES DA CONSULTA ==========\n")

            print("------ PACIENTE ------")
            print(f"Nome: {nomePaciente[0] if nomePaciente else 'Não encontrado'}")
            print(f"ID:   {paciente_id}\n")

            print("------ MÉDICO ------")
            print(f"Nome: {nomeMedico[0]}")
            print(f"ID:   {medico_id}\n")

            print("------ DETALHES ------")
            print(f"ID da consulta : {consulta_id}")
            print(f"Data e Hora    : {consulta[3]}")
            print(f"Status         : {consulta[4]}")
            print(f"Observações    : {consulta[5]}")

            print("\n==============================================\n")

    except mysql.connector.Error as erro_db:
        print(f"\nErro no banco de dados: {erro_db}")

    except Exception as erro:
        print(f"\nOcorreu um erro inesperado: {erro}")

    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass

        if conexao:
            try:
                conexao.close()
            except:
                pass



def relatorioData():
    conexao = None
    cursor = None

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("SELECT DISTINCT DATE(data_hora) FROM consultas")
        datas = cursor.fetchall()

        print("\nAs datas disponíveis para relatório são:")
        for data in datas:
            print(data[0])

        dataSelecionada = input("\nDe qual data você deseja gerar o relatório (AAAA-MM-DD): ").strip()

        cursor.execute("SELECT * FROM consultas WHERE DATE(data_hora) = %s", (dataSelecionada,))
        consultas = cursor.fetchall()

        if not consultas:
            print("\nNenhuma consulta encontrada nessa data.")
            return

        for consulta in consultas:
            consulta_id = consulta[0]
            paciente_id = consulta[1]
            medico_id = consulta[2]
            status = consulta[4]
            obs = consulta[5]

            cursor.execute("SELECT nome FROM pacientes WHERE idprontuario = %s", (paciente_id,))
            nomePaciente = cursor.fetchone()

            cursor.execute("SELECT nome FROM medicos WHERE medico_id = %s", (medico_id,))
            nomeMedico = cursor.fetchone()

            print("\n========== RELATÓRIO DA CONSULTA ==========\n")

            print("------ PACIENTE ------")
            print(f"Nome: {nomePaciente[0] if nomePaciente else 'Não encontrado'}")

            print("\n------ MÉDICO ------")
            print(f"Nome: {nomeMedico[0] if nomeMedico else 'Não encontrado'}")
            print(f"ID:   {medico_id}")

            print("\n------ DETALHES ------")
            print(f"ID da Consulta : {consulta_id}")
            print(f"Status         : {status}")
            print(f"Observação     : {obs}")

        print("\n===========================================\n")

    except mysql.connector.Error as erro_db:
        print(f"\nErro no banco de dados: {erro_db}")

    except Exception as erro:
        print(f"\nOcorreu um erro inesperado: {erro}")

    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass

        if conexao:
            try:
                conexao.close()
            except:
                pass



def menu_relatorio():
    while True:
        try:
            print('----- SELECIONE SEU TIPO DE RELATÓRIO -----')
            print('1. Relatório por Médico')
            print('2. Relátorio por Data')
            print('3. Voltar ao menu principal')
            print('4. Sair')
            opcao = int(input('Escolha uma opção (1-4): '))
        except ValueError:
            print("Digite um número válido.")
            continue

        if opcao == 1:
            relatorioMedicos()
        elif opcao == 2:
            relatorioData()
        elif opcao == 3:
            break
        elif opcao == 4:
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")



if __name__ == "__main__":
    menu_relatorio()
