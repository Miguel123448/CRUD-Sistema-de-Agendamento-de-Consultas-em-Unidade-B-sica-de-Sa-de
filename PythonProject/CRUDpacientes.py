from optparse import Values

import mysql.connector
from annotated_types.test_cases import cases

conexao = mysql.connector.connect(
  host="localhost",
  user="",
  passwd="",
  database="banco"
)
cursor = conexao.cursor()

print('------ Bem vindo ao CRUD de pacientes -----')
opcao = int(input(' 1 - Cadastrar paciente\n 2 - Ver lista de cadastros\n 3 - Atualizar cadastros \n 4 - Remover cadastros '))
if opcao == 1:
    print('----- Cadastrando paciente, porfavor preencha as informações abaixo ----- ')
    nome = input('Insira o nome do paciente: ')
    cpf = input('Insira o CPF do paciente (somente números): ')
    nascimento = input('Insira a data de nascimento do paciente (somente números): ')
    telefone = input('Insira o telefone do paciente (somente números): ')
    endereco = input('Insira o endereço do paciente: ')
    cep = input('Insira o cep do paciente: ')
    print('Cadastro realizado com sucesso!')
    comando = "INSERT INTO pacientes (nome, cpf, nascimento, telefone, endereco, cep) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (nome, cpf, nascimento,  telefone, endereco, cep)
    cursor.execute(comando, valores)
    conexao.commit()
elif opcao == 2:
    print('----- Carregando lista de cadastros.... -----')
    comando = "SELECT * FROM pacientes"
    cursor.execute(comando)
    resultado = cursor.fetchall()
    print(resultado)
elif opcao == 3:
    print('----- Atualizando cadastro -----')

    cpf_paciente = input('Digite o CPF do paciente que deseja atualizar (somente números): ')

    print('\nQual campo deseja atualizar?')
    print(' 1 - Nome')
    print(' 2 - Data de Nascimento')
    print(' 3 - Telefone')
    print(' 4 - Endereço')
    print(' 5 - CEP')

    try:

        campo_opcao = int(input('Digite o número do campo: '))
        novo_valor = input(f'Digite o NOVO valor para o campo selecionado: ')

        campo_db = ""
        if campo_opcao == 1:
            campo_db = "nome"
        elif campo_opcao == 2:
            campo_db = "nascimento"
        elif campo_opcao == 3:
            campo_db = "telefone"
        elif campo_opcao == 4:
            campo_db = "endereco"
        elif campo_opcao == 5:
            campo_db = "cep"
        else:
            print('Opção inválida. Operação cancelada.')


        if campo_db:
            comando = f"UPDATE pacientes SET {campo_db} = %s WHERE cpf = %s"
            valores = (novo_valor, cpf_paciente)

            cursor.execute(comando, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                print(f'Cadastro do paciente (CPF: {cpf_paciente}) atualizado com sucesso!')
            else:
                print(f'Nenhum paciente encontrado com o CPF: {cpf_paciente}. Nenhuma alteração foi feita.')

    except ValueError:
        print("Erro: Opção inválida. Por favor, digite um número.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        conexao.rollback()
elif opcao == 4:
    print('----- Removendo cadastro -----')
    cpf_paciente = input('Digite o CPF do paciente que deseja remover (somente números): ')

    try:
        comando = "DELETE FROM pacientes WHERE cpf = %s"
        valores = (cpf_paciente,)

        cursor.execute(comando, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            print(f'Paciente (CPF: {cpf_paciente}) removido com sucesso!')
        else:
            print(f'Nenhum paciente encontrado com o CPF: {cpf_paciente}. Nenhuma remoção foi feita.')

    except Exception as e:
        print(f"Ocorreu um erro ao tentar remover: {e}")
        conexao.rollback()

else:
    print('Opção inválida. Por favor, escolha um número de 1 a 4.')
    print('Operação cancelada.')


cursor.close()
conexao.close()