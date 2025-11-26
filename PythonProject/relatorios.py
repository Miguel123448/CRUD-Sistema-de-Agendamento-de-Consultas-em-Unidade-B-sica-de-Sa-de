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
    
    nomeMedico = input("\nEscreva o nome do médico que você quer gerar o relátorio:")
    print(f"\nSeu medico selecionado é {nomeMedico}")
    
    cursor.execute("SELECT medico_id FROM medicos WHERE nome = %s", (nomeMedico,))
    resultado = cursor.fetchall()
    
    medicoSelecionado = resultado[0][0]
    cursor.execute("SELECT * FROM consultas WHERE medico_id = %s", (medicoSelecionado,))
    relatorio = cursor.fetchall()
    print("\nConsultas do médico selecionado:")
    for consulta in relatorio:
     print(f"ID da consulta: {consulta[0]}")
     print(f"ID do paciente: {consulta[1]}")
     print(f"ID do médico: {consulta[2]}")
     print(f"Data e hora: {consulta[3]}")
     print(f"Status: {consulta[4]}")
     print(f"Observações: {consulta[5]}")
     print("---------------------------------------")

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
     
        print("\n-----Relatório-----")
        print(f"ID da consulta: {consulta_id}")
        print(f"Nome do paciente: {nomePaciente}")
        print(f"ID do Médico: {medico_id}")
        print(f"Status: {status}")
        print(f"Observação: {observacoes}")
        
    print("\n----- FIM DO RELATÓRIO -----")
    cursor.close()
    conexao.close()
    
       
#UPDATE - Atualizar uma Consulta
def menu_relatorio():
    while True:
        print('----- Tipo -----')
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
