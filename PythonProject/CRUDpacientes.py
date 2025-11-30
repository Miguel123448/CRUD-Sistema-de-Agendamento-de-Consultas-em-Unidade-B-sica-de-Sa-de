import db

def menu_pacientes():
    print('------ Bem vindo ao CRUD de pacientes -----')
    try:
        return int(input(
            ' 1 - Cadastrar paciente\n 2 - Ver lista de cadastros\n'
            ' 3 - Atualizar cadastros\n 4 - Remover cadastros\n 5 - Sair\nEscolha uma opção: '))
    except ValueError:
        return 0

def validar_nome(nome):
    if not nome or nome.strip() == '':
        print('Erro: Nome não pode ser vazio.')
        return False
    if len(nome.strip()) < 3:
        print('Erro: Nome deve ter no mínimo 3 caracteres.')
        return False
    return True

def validar_cpf(cpf):
    if not cpf.isdigit():
        print('Erro: CPF deve conter apenas dígitos.')
        return False
    if len(cpf) != 11:
        print('Erro: CPF deve conter exatamente 11 dígitos.')
        return False
    return True

def validar_telefone(telefone):
    if not telefone.isdigit():
        print('Erro: Telefone deve conter apenas dígitos.')
        return False
    if len(telefone) < 10 or len(telefone) > 11:
        print('Erro: Telefone deve ter 10 ou 11 dígitos.')
        return False
    return True

def validar_cep(cep):
    if not cep.isdigit():
        print('Erro: CEP deve conter apenas dígitos.')
        return False
    if len(cep) != 8:
        print('Erro: CEP deve conter exatamente 8 dígitos.')
        return False
    return True

def validar_nascimento(dia, mes, ano):
    if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
        print('Erro: A data deve conter apenas números.')
        return False

    d, m, a = int(dia), int(mes), int(ano)

    if not (1 <= m <= 12):
        print('Erro: Mês inválido.')
        return False
    if not (1 <= d <= 31):
        print('Erro: Dia inválido.')
        return False
    if len(ano) != 4:
        print('Erro: Ano deve ter 4 dígitos.')
        return False
    return True

def cadastrar_paciente():
    print('----- Cadastrando paciente -----')

    while True:
        nome = input('Insira o nome do paciente: ')
        if validar_nome(nome):
            break

    while True:
        cpf = input('Insira o CPF do paciente (11 dígitos): ')
        if validar_cpf(cpf):
            break

    while True:
        dia = input('Insira o dia de nascimento (DD): ')
        mes = input('Insira o mês de nascimento (MM): ')
        ano = input('Insira o ano de nascimento (YYYY): ')

        if validar_nascimento(dia, mes, ano):
            nascimento = f"{ano}-{mes}-{dia}"
            break

    while True:
        telefone = input('Insira o telefone do paciente (10 ou 11 dígitos): ')
        if validar_telefone(telefone):
            break

    endereco = input('Insira o endereço do paciente: ')

    while True:
        cep = input('Insira o CEP do paciente (8 dígitos): ')
        if validar_cep(cep):
            break

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
        comando = ("INSERT INTO pacientes (nome, cpf, nascimento, telefone, endereco, cep) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
        valores = (nome, cpf, nascimento, telefone, endereco, cep)
        cursor.execute(comando, valores)
        conexao.commit()
        print('Cadastro realizado com sucesso!')
    except Exception as e:
        print(f"Erro ao cadastrar paciente: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexao' in locals(): conexao.close()

def ler_paciente():
    print('\n----- Lista de cadastros -----')
    conexao = None
    cursor = None
    resultado = []

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()

        comando = "SELECT idprontuario, nome, cpf, nascimento, telefone, endereco, cep FROM pacientes"
        cursor.execute(comando)
        resultado = cursor.fetchall()

    except Exception as e:
        print(f"Erro ao ler pacientes: {e}")
        return
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

    if not resultado:
        print("Nenhum paciente cadastrado.")
        return

    print(f"{'ID':<5} | {'NOME':<20} | {'CPF':<14} | {'NASCIMENTO':<12} | {'TELEFONE':<14} | {'ENDERECO':<20} | {'CEP':<10}")
    print("-" * 110)

    for linha in resultado:
        idprontuario, nome, cpf, nascimento, telefone, endereco, cep = linha

        data_visual = str(nascimento)
        if '-' in data_visual:
            try:
                ano_b, mes_b, dia_b = data_visual.split('-')
                data_visual = f"{dia_b}/{mes_b}/{ano_b}"
            except:
                pass

        print(f"{idprontuario:<5} | {nome:<20} | {cpf:<14} | {data_visual:<12} | {telefone:<14} | {endereco:<20} | {cep:<10}")

def cpf_existe(cpf):
    conexao = None
    cursor = None
    existe = False

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT 1 FROM pacientes WHERE cpf = %s", (cpf,))
        existe = cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar CPF: {e}")
        existe = False
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

    return existe

def atualizar_paciente():
    print('----- Atualizando cadastro -----')

    cpf_paciente = input('Digite o CPF do paciente que deseja atualizar: ')

    if not cpf_existe(cpf_paciente):
        print(f"Erro: CPF {cpf_paciente} não encontrado no sistema.")
        return

    print('\nQual campo deseja atualizar?')
    print(' 1 - Nome\n 2 - Data de Nascimento\n 3 - Telefone\n 4 - Endereço\n 5 - CEP')

    conexao = None
    cursor = None

    try:
        campo_opcao = int(input('Digite o número do campo: '))
        campos = {1: "nome", 2: "nascimento", 3: "telefone", 4: "endereco", 5: "cep"}
        campo_db = campos.get(campo_opcao)

        if not campo_db:
            print('Opção inválida. Operação cancelada.')
            return

        novo_valor = input('Digite o NOVO valor para o campo selecionado: ')

        if campo_opcao == 2:
            if '/' in novo_valor:
                try:
                    dia, mes, ano = novo_valor.split('/')
                    novo_valor = f"{ano}-{mes}-{dia}"
                except ValueError:
                    print("Erro no formato da data. Use DD/MM/AAAA.")
                    return
            elif '-' in novo_valor:
                try:
                    dia, mes, ano = novo_valor.split('-')
                    if len(ano) == 4:
                        novo_valor = f"{ano}-{mes}-{dia}"
                except:
                    pass

        conexao = db.obter_conexao()
        cursor = conexao.cursor()
        comando = f"UPDATE pacientes SET {campo_db} = %s WHERE cpf = %s"
        valores = (novo_valor, cpf_paciente)
        cursor.execute(comando, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            print('Cadastro atualizado com sucesso!')
        else:
            print('Erro ao atualizar. Verifique se o valor é diferente do atual.')

    except ValueError:
        print("Erro: Opção inválida. Por favor, digite um número.")
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o paciente: {e}")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

def deletar_paciente():
    print('----- Removendo cadastro -----')

    ler_paciente()

    cpf_paciente = input('\nDigite o CPF do paciente que deseja remover: ')

    if not cpf_existe(cpf_paciente):
        print("Paciente não encontrado.")
        return

    try:
        conexao = db.obter_conexao()
        cursor = conexao.cursor()
        comando = "DELETE FROM pacientes WHERE cpf = %s"
        valores = (cpf_paciente,)
        cursor.execute(comando, valores)
        conexao.commit()
        print('Paciente removido com sucesso!')
    except Exception as e:
        print(f"Ocorreu um erro ao tentar remover: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexao' in locals(): conexao.close()

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
