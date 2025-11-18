import db

def menu_pacientes():
    print('------ Bem vindo ao CRUD de pacientes -----')
    return int(input(
        ' 1 - Cadastrar paciente\n 2 - Ver lista de cadastros\n'
        ' 3 - Atualizar cadastros\n 4 - Remover cadastros\n 5 - Sair\nEscolha uma opção: '))

def cadastrar_paciente():
    print('----- Cadastrando paciente -----')
    nome = input('Insira o nome do paciente: ')
    cpf = input('Insira o CPF do paciente (somente números): ')
    nascimento = input('Insira a data de nascimento do paciente (somente números): ')
    telefone = input('Insira o telefone do paciente (somente números): ')
    endereco = input('Insira o endereço do paciente: ')
    cep = input('Insira o cep do paciente: ')

    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = ("INSERT INTO pacientes (nome, cpf, nascimento, telefone, endereco, cep) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
    valores = (nome, cpf, nascimento, telefone, endereco, cep)
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()
    print('Cadastro realizado com sucesso!')

def ler_paciente():
    print('----- Lista de cadastros -----')
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    comando = "SELECT * FROM pacientes"
    cursor.execute(comando)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    for linha in resultado:
        print(linha)

def atualizar_paciente():
    print('----- Atualizando cadastro -----')

    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    
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
        cursor.close()
        conexao.close()

def deletar_paciente():
    print('----- Removendo cadastro -----')
    conexao = db.obter_conexao()
    cursor = conexao.cursor()
    ler_paciente()
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
        cursor.close()
        conexao.close()

def main():
    while True:
        opcao = menu_pacientes()
        if opcao == 1:
            cadastrar_paciente()
        elif opcao == 2:
            ler_paciente()
        elif opcao == 3:
            atualizar_paciente()
        elif opcao == 4:
            deletar_paciente()
        elif opcao == 5:
            print('Saindo do sistema. Até logo!')
            break
        else:
            print('Opção inválida. Por favor, escolha um número de 1 a 5.')

if __name__ == "__main__":
    main()

