import db

def menu():
    print('------ Bem vindo ao CRUD de pacientes -----')
    return int(input(
        ' 1 - Cadastrar paciente\n 2 - Ver lista de cadastros\n'
        ' 3 - Atualizar cadastros\n 4 - Remover cadastros\n 5 - Sair\nEscolha uma opção: '))

def cadastrar(cursor, conexao):
    print('----- Cadastrando paciente -----')
    nome = input('Insira o nome do paciente: ')
    cpf = input('Insira o CPF do paciente (somente números): ')
    nascimento = input('Insira a data de nascimento do paciente (somente números): ')
    telefone = input('Insira o telefone do paciente (somente números): ')
    endereco = input('Insira o endereço do paciente: ')
    cep = input('Insira o cep do paciente: ')
    comando = ("INSERT INTO pacientes (nome, cpf, nascimento, telefone, endereco, cep) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
    valores = (nome, cpf, nascimento, telefone, endereco, cep)
    cursor.execute(comando, valores)
    conexao.commit()
    print('Cadastro realizado com sucesso!')

def ler(cursor):
    print('----- Lista de cadastros -----')
    comando = "SELECT * FROM pacientes"
    cursor.execute(comando)
    resultado = cursor.fetchall()
    for linha in resultado:
        print(linha)

def atualizar(cursor, conexao):
    print('----- Atualizando cadastro -----')
    cpf_paciente = input('Digite o CPF do paciente que deseja atualizar: ')
    print('\nQual campo deseja atualizar?')
    print(' 1 - Nome\n 2 - Data de Nascimento\n 3 - Telefone\n 4 - Endereço\n 5 - CEP')
    try:
        campo_opcao = int(input('Digite o número do campo: '))
        novo_valor = input('Digite o NOVO valor para o campo selecionado: ')
        campos = {1: "nome", 2: "nascimento", 3: "telefone", 4: "endereco", 5: "cep"}
        campo_db = campos.get(campo_opcao)
        if not campo_db:
            print('Opção inválida. Operação cancelada.')
            return
        comando = f"UPDATE pacientes SET {campo_db} = %s WHERE cpf = %s"
        valores = (novo_valor, cpf_paciente)
        cursor.execute(comando, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print('Cadastro atualizado com sucesso!')
        else:
            print('Nenhum paciente encontrado com o CPF informado.')
    except ValueError:
        print("Erro: Opção inválida. Por favor, digite um número.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        conexao.rollback()

def deletar(cursor, conexao):
    print('----- Removendo cadastro -----')
    cpf_paciente = input('Digite o CPF do paciente que deseja remover: ')
    try:
        comando = "DELETE FROM pacientes WHERE cpf = %s"
        valores = (cpf_paciente,)
        cursor.execute(comando, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print('Paciente removido com sucesso!')
        else:
            print('Nenhum paciente encontrado com o CPF informado.')
    except Exception as e:
        print(f"Ocorreu um erro ao tentar remover: {e}")
        conexao.rollback()

def main():
    conexao = db.conexao
    cursor = conexao.cursor()
    while True:
        opcao = menu()
        if opcao == 1:
            cadastrar(cursor, conexao)
        elif opcao == 2:
            ler(cursor)
        elif opcao == 3:
            atualizar(cursor, conexao)
        elif opcao == 4:
            deletar(cursor, conexao)
        elif opcao == 5:
            print('Saindo do sistema. Até logo!')
            break
        else:
            print('Opção inválida. Por favor, escolha um número de 1 a 5.')
    cursor.close()
    conexao.close()

if __name__ == "__main__":
    main()
