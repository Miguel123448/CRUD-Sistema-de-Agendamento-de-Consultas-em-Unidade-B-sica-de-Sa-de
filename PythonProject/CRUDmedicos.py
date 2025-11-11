import db

def menu():
    while True:
        print("""
      BEM VINDO DOUTOR(A) AO MENU DOS MÉDICOS!

ESCOLHA UMA OPÇÃO :
1. Cadastrar médico
2. Listar médicos
3. Atualizar médico
4. Deletar médico
5. Sair
""")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_medico()
        elif opcao == '2':
            ler_medicos()
        elif opcao == '3':
            atualizar_medico()
        elif opcao == '4':
            id_medico = input("Digite o ID do médico que deseja deletar: ")
            deletar_medico(id_medico)
            print(" Médico deletado com sucesso!")
        elif opcao == '5':
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()

#  CREATE 
def criar_medico():
    print("\n--- Cadastrar novo médico ---")
    nome = input("1. Nome: ")
    crm = input("2. CRM: ")
    especialidade = input("3. Especialidade: ")
    telefone = input("4. Telefone: ")
    horario_inicio = input("5. Horário de entrada (HH:MM:SS): ")
    horario_fim = input("6. Horário de saída (HH:MM:SS): ")

    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = """
        INSERT INTO medicos (nome, crm, especialidade, telefone, horario_inicio, horario_fim)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (nome, crm, especialidade, telefone, horario_inicio, horario_fim)
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

    print(f"\nMédico {nome} cadastrado com sucesso!")

# READ 
def ler_medicos():
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = "SELECT * FROM medicos"
    cursor.execute(comando)
    resultado = cursor.fetchall() 

    cursor.close()
    conexao.close()

    if not resultado:
        print("\nNenhum médico encontrado no banco de dados.")
        return resultado  

    print("\nLista de Médicos:")
    for (id_medico, nome, crm, especialidade, telefone, horario_inicio, horario_fim) in resultado:
        print(f"""
ID: {id_medico}
Nome: {nome}
CRM: {crm}
Especialidade: {especialidade}
Telefone: {telefone}
Horário: {horario_inicio} - {horario_fim}
----------------------------""")

    return resultado

# UPDATE
def atualizar_medico():
    ler_medicos()

    conexao = db.obter_conexao()
    cursor = conexao.cursor()

    id_medico = input("Digite o ID do médico que deseja atualizar: ")

    while True:
        print("""
Qual dado você deseja atualizar?
1. Nome
2. CRM
3. Especialidade
4. Telefone
5. Horário de entrada
6. Horário de saída
7. Sair
""")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            novo_nome = input("Digite o novo nome: ")
            comando = "UPDATE medicos SET nome = %s WHERE medico_id = %s"
            valores = (novo_nome, id_medico)
        elif opcao == '2':
            novo_crm = input("Digite o novo CRM: ")
            comando = "UPDATE medicos SET crm = %s WHERE medico_id = %s"
            valores = (novo_crm, id_medico)
        elif opcao == '3':
            nova_especialidade = input("Digite a nova especialidade: ")
            comando = "UPDATE medicos SET especialidade = %s WHERE medico_id = %s"
            valores = (nova_especialidade, id_medico)
        elif opcao == '4':
            novo_telefone = input("Digite o novo telefone: ")
            comando = "UPDATE medicos SET telefone = %s WHERE medico_id = %s"
            valores = (novo_telefone, id_medico)
        elif opcao == '5':
            novo_horario_inicio = input("Digite o novo horário de entrada (HH:MM:SS): ")
            comando = "UPDATE medicos SET horario_inicio = %s WHERE medico_id = %s"
            valores = (novo_horario_inicio, id_medico)
        elif opcao == '6':
            novo_horario_fim = input("Digite o novo horário de saída (HH:MM:SS): ")
            comando = "UPDATE medicos SET horario_fim = %s WHERE medico_id = %s"
            valores = (novo_horario_fim, id_medico)
        elif opcao == '7':
            print("Saindo da atualização.")
            break
        else:
            print("Opção inválida.")
            continue

        cursor.execute(comando, valores)
        conexao.commit()
        print("Dado atualizado com sucesso!\n")

    cursor.close()
    conexao.close()

# DELETE
def deletar_medico(id_medico):
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = "DELETE FROM medicos WHERE medico_id = %s"
    cursor.execute(comando, (id_medico,))
    conexao.commit()
    cursor.close()

    conexao.close()

