import CRUDconsultas
import CRUDmedicos
import CRUDpacientes
import relatorios

def menu():
    while True:
        print('----- Menu Principal -----')
        print('1. Gerenciar Pacientes')
        print('2. Gerenciar Médicos')
        print('3. Gerenciar Consultas')
        print('4. Ver Relatórios')
        print('5. Sair')
        opcao = int(input('Escolha uma opção (1-5): '))
        if opcao == 1:
            menu_pacientes()
        elif opcao == 2:
            menu_medicos()
        elif opcao == 3:
            menu_consultas()
        elif opcao == 4:
            relatorios.menu_relatorio()
        elif opcao == 5:
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_pacientes():
    while True:
        print("------ Bem vindo ao CRUD de pacientes -----")
        print(" 1 - Cadastrar paciente\n 2 - Ver lista de pacientes\n 3 - Atualizar cadastro de paciente\n 4 - Remover cadastro de paciente\n 5 - Voltar ao menu principal")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            CRUDpacientes.cadastrar_paciente()
        elif opcao == 2:
            CRUDpacientes.ler_paciente()
        elif opcao == 3:
            CRUDpacientes.atualizar_paciente()
        elif opcao == 4:
            CRUDpacientes.deletar_paciente()
        elif opcao == 5:
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_medicos():
    while True:
        print("------ Bem vindo ao CRUD de médicos -----")
        print(" 1 - Cadastrar médico\n 2 - Ver lista de médicos\n 3 - Atualizar cadastro de médico\n 4 - Remover cadastro de médico\n 5 - Voltar ao menu principal")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            CRUDmedicos.criar_medico()
        elif opcao == 2:
            CRUDmedicos.ler_medicos()
        elif opcao == 3:
            CRUDmedicos.atualizar_medico()
        elif opcao == 4:
            CRUDmedicos.deletar_medico()
        elif opcao == 5:
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_consultas():
    while True:
        print("------ Bem vindo ao CRUD de consultas -----")
        print(" 1 - Cadastrar consulta\n 2 - Ver lista de consultas\n 3 - Atualizar consulta\n 4 - Remover consulta\n 5 - Voltar ao menu principal")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            CRUDconsultas.criar_consulta()
        elif opcao == 2:
            CRUDconsultas.listar_consulta()
        elif opcao == 3:
            CRUDconsultas.atualizar_consulta()
        elif opcao == 4:
            CRUDconsultas.deletar_consulta()
        elif opcao == 5:
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()
