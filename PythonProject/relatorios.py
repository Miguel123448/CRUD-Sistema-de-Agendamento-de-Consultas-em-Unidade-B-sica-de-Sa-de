import db


def relatorioMedicos():
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT medico_id, nome FROM medicos")
    medicos = cursor.fetchall()
    print("\nMédicos cadastrados ---")
    print("ID | Nome")
    print("-------------------")
    for medico in medicos:
        print(f"{medico[0]} - {medico[1]}") 
    
    IdMedico = input("\nEscreva o ID do médico que você quer gerar o relátorio:")
    cursor.execute("SELECT nome FROM medicos WHERE medico_id = %s", (IdMedico,))
    nomeMedico = cursor.fetchone()
    print(f"\nSeu medico selecionado é {nomeMedico}")
    cursor.execute("SELECT medico_id FROM medicos WHERE medico_id = %s", (IdMedico,))
    resultado = cursor.fetchall()
    
    medicoSelecionado = resultado[0][0]
    cursor.execute("SELECT * FROM consultas WHERE medico_id = %s", (medicoSelecionado,))
    relatorio = cursor.fetchall()
    print("\nConsultas do médico selecionado:\n")
    for consulta in relatorio:
     print(f"ID da consulta: {consulta[0]}")
     cursor.execute("SELECT nome FROM pacientes WHERE idprontuario= %s", (consulta[1],))
     nomePaciente = cursor.fetchone() 
     print("\n========== INFORMAÇÕES DA CONSULTA ==========\n")

    print("------ PACIENTE ------")
    print(f"Nome: {nomePaciente[0]}")
    print(f"ID:   {consulta[1]}\n")

    print("------ MÉDICO ------")
    print(f"Nome: {nomeMedico[0]}")
    print(f"ID:   {consulta[2]}\n")

    print("------ DETALHES ------")
    print(f"Data e Hora : {consulta[3]}")
    print(f"Status      : {consulta[4]}")
    print(f"Observações : {consulta[5]}")

    print("\n==============================================\n")

    cursor.close()
    conexao.close()




def relatorioData():
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT DATE(data_hora) FROM consultas")
    datasDisponiveis = cursor.fetchall()
    
    print("\nAs datas disponíveis para relatório são:")
    for data in datasDisponiveis:
     print(data[0])
     
    dataSelecionada = input("\nDe qual data você deseja gerar um relatório\n")
    cursor.execute("SELECT * FROM consultas WHERE DATE(data_hora) = %s", (dataSelecionada,))
    resultado = cursor.fetchall()
    if not resultado:
        print("\nNenhuma consulta encontrada nessa data.")
        return
    
    for consulta in resultado:
        
        consulta_id = consulta[0]
        paciente_id = consulta[1]
        medico_id = consulta[2]
        status = consulta[4]
        observacoes = consulta[5]
        
        cursor.execute("SELECT nome FROM pacientes WHERE idprontuario = %s", (paciente_id,))
        nomePaciente = cursor.fetchone()
        
        cursor.execute("SELECT nome FROM medicos WHERE medico_id = %s", (consulta[2],))
        nomeMedico = cursor.fetchone()
        
     
        print("\n========== RELATÓRIO DA CONSULTA ==========\n")

        print("------ PACIENTE ------")
        print(f"Nome: {nomePaciente[0]}")

        print("\n------ MÉDICO ------")
        print(f"Nome: {nomeMedico[0]}")
        print(f"ID:   {medico_id}")

        print("\n------ DETALHES ------")
        print(f"ID da Consulta : {consulta_id}")
        print(f"Status         : {status}")
        print(f"Observação     : {observacoes}")

    print("\n===========================================\n")
    cursor.close()
    conexao.close()
    
       
#UPDATE - Atualizar uma Consulta
def menu_relatorio():
    while True:
        print('----- SELECIONE SEU TIPO DE RELATÓRIO -----')
        print('1. Relatório por Médico')
        print('2. Relátorio por Data')
        print('3. Voltar ao menu principal')
        print('4. Sair')
        opcao = int(input('Escolha uma opção (1-4): '))
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
