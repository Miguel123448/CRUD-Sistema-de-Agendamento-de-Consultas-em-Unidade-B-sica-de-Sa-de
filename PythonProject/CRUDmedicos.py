import db
import re

def menu():
    while True:
        print("""
      MENU DOS MÉDICOS 

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
             deletar_medico()
             print("\nMédico deletado com sucesso!")
        elif opcao == '5':
            print("\nSaindo do sistema.")
            break
        else:
            print("Opção inválida.\n")


def validar_horario(h):
    return bool(re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", h))


def criar_medico():
    print("\n--- Cadastro de Médico ---")

    while True:
        nome = input("Nome: ").strip()
        if nome:
            break
        print("Nome inválido.\n")

    while True:
        crm = input("CRM (mínimo 4 números — pode ter letras): ").strip()
        if len(re.findall(r"\d", crm)) >= 4:
            break
        print("CRM inválido. Deve ter ao menos 4 números.\n")

    while True:
        especialidade = input("Especialidade: ").strip()
        if especialidade:
            break
        print("Especialidade inválida.\n")

    while True:
        telefone = input("Telefone (somente números): ").strip()
        if telefone.isdigit():
            break
        print("Telefone inválido.\n")

    while True:
        horario_inicio = input("Horário de entrada (HH:MM): ").strip()
        if validar_horario(horario_inicio):
            break
        print("Horário inválido.\n")

    while True:
        horario_fim = input("Horário de saída (HH:MM): ").strip()
        if validar_horario(horario_fim):
            break
        print("Horário inválido.\n")

    conexao = None
    cursor = None
    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
        comando = """
            INSERT INTO medicos (nome, crm, especialidade, telefone, horario_inicio, horario_fim)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (nome, crm, especialidade, telefone, horario_inicio, horario_fim)
        cursor.execute(comando, valores)
        conexao.commit()
        print(f"\nMédico {nome} cadastrado com sucesso!\n")
    except Exception as e:
        print(f"Erro ao cadastrar médico: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def ler_medicos():
    conexao = None
    cursor = None
    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM medicos")
        resultado = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao ler médicos: {e}")
        return
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

    if not resultado:
        print("\nNenhum médico cadastrado.\n")
        return []

    print("\n LISTA DE MÉDICOS \n")
    for (id_medico, nome, crm, especialidade, telefone, horario_inicio, horario_fim) in resultado:
        print(
f"""
ID: {id_medico}
Nome: {nome}
CRM: {crm}
Especialidade: {especialidade}
Telefone: {telefone}
Horário: {horario_inicio} às {horario_fim}

"""
        )
    return resultado


def atualizar_medico():
    lista = ler_medicos()
    if not lista:
        return

    conexao = None
    cursor = None

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()

        id_medico = input("ID do médico para atualizar: ")

        cursor.execute("SELECT * FROM medicos WHERE medico_id = %s", (id_medico,))
        medico = cursor.fetchone()

        if not medico:
            print("\nID não encontrado.\n")
            return

        while True:
            print("""
 O que deseja atualizar? 

1. Nome
2. CRM
3. Especialidade
4. Telefone
5. Horário de entrada
6. Horário de saída
7. Sair
""")
            opcao = input("Escolha: ")

            if opcao == '1':
                novo = input("Novo nome: ")
                comando = "UPDATE medicos SET nome = %s WHERE medico_id = %s"

            elif opcao == '2':
                while True:
                    novo = input("Novo CRM (mínimo 4 números — pode ter letras): ").strip()
                    if len(re.findall(r"\d", novo)) >= 4:
                        break
                    print("CRM inválido.\n")
                comando = "UPDATE medicos SET crm = %s WHERE medico_id = %s"

            elif opcao == '3':
                novo = input("Nova especialidade: ")
                comando = "UPDATE medicos SET especialidade = %s WHERE medico_id = %s"

            elif opcao == '4':
                while True:
                    novo = input("Novo telefone (somente números): ")
                    if novo.isdigit():
                        break
                    print("Telefone inválido.")
                comando = "UPDATE medicos SET telefone = %s WHERE medico_id = %s"

            elif opcao == '5':
                while True:
                    novo = input("Novo horário de entrada (HH:MM): ")
                    if validar_horario(novo):
                        break
                    print("Horário inválido.")
                comando = "UPDATE medicos SET horario_inicio = %s WHERE medico_id = %s"

            elif opcao == '6':
                while True:
                    novo = input("Novo horário de saída (HH:MM): ")
                    if validar_horario(novo):
                        break
                    print("Horário inválido.")
                comando = "UPDATE medicos SET horario_fim = %s WHERE medico_id = %s"

            elif opcao == '7':
                print("\nAtualização finalizada.\n")
                break

            else:
                print("Opção inválida.\n")
                continue

            try:
                cursor.execute(comando, (novo, id_medico))
                conexao.commit()
                print("Atualizado com sucesso!\n")
            except Exception as e:
                print(f"Erro ao atualizar: {e}")

    except Exception as e:
        print(f"Erro na atualização: {e}")

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def deletar_medico():
    id_medico = input("ID do médico para deletar: ")

    conexao = None
    cursor = None
    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM medicos WHERE medico_id = %s", (id_medico,))
        conexao.commit()
    except Exception as e:
        print(f"Erro ao deletar: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


if __name__ == "__main__":
    menu()
