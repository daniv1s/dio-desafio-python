import sqlite3
import textwrap
import os
from datetime import datetime, date

db_path = os.path.join(os.path.dirname(__file__), 'banco_db.db')

# Classes

class Usuario:
    def __init__(self, nome, cpf, data_nasc, senha):
        self._nome = nome
        self._cpf = cpf
        self._data_nasc = data_nasc
        self._senha = senha
    
class Endereco:
    def __init__(self, logradouro, numero, bairro, cidade, uf):
        self._logradouro = logradouro
        self._numero = numero
        self._bairro = bairro
        self._cidade = cidade
        self._uf = uf

class Conta:
    def __init__(self, cpf_usuario):
        self._cpf_usuario = cpf_usuario
        self._agencia = '0001'
        self._saldo = 0
        self._limite = 500
        self._limite_saques = 3
        
# Funções

def menu_usuario():
    menu_usuario = """
    ---------------------------------

    Bem vindo ao sistema bancário!

    Escolha uma das seguintes opções:

    [1] Entrar na conta
    [2] Criar conta
    [3] Sair

    ---------------------------------

    => """

    return input(textwrap.dedent(menu_usuario))

def menu_conta(nome_usuario):
    menu_conta = f"""
    ---------------------------------

    Bem vindo, {nome_usuario}!

    Escolha uma das seguintes opções:

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [i] Dados cadastrais
    [l] Dados bancários
    [q] Sair

    ---------------------------------

    => """

    return input(textwrap.dedent(menu_conta))

def executar_no_banco(query, dados):
    try:
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        cursor.execute(query, dados)

        conexao.commit()
        print("Operação realizada com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao executar a operação!: {e}")
        return False
    finally:
        conexao.close()

def verifica_usuario (cpf):
    try:
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        cursor.execute("SELECT cpf FROM usuarios WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()

        if resultado:
            return True  # Usuário encontrado
        else:
            return False  # Usuário não encontrado
        
    except sqlite3.Error as e:
        print(f"Erro ao executar a operação!: {e}")
        return None
    finally:
        conexao.close()

def login_usuario(cpf, senha):
    usuario = verifica_usuario(cpf)

    if usuario is None:
        print("Erro na verificação do usuário.")
        return False, None, None, None

    if usuario:
        try:
            conexao = sqlite3.connect(db_path)
            cursor = conexao.cursor()

            cursor.execute("SELECT nome, senha, cpf FROM usuarios WHERE cpf = ? AND senha = ?", (cpf, senha,))
            resultado = cursor.fetchone()

            cursor.execute("SELECT numero_conta FROM contas WHERE cpf_usuario = ?", (cpf,))
            resultado_conta = cursor.fetchone()

            if resultado and resultado_conta:
                nome_usuario = resultado[0]
                cpf_usuario = resultado[2]
                conta_usuario = resultado_conta[0]
                return True, nome_usuario, cpf_usuario, conta_usuario
            else:
                print("\nCredenciais inválidas!\n")
                return False, None, None, None
            
        except sqlite3.Error as e:
            print(f"Erro ao executar a operação!: {e}")
            return False, None, None, None
        finally:
            conexao.close()
        
    else:
        return False, None, None, None

def cadastrar_usuario(*, nome, cpf, data_nasc, senha):
    novo_usuario = Usuario(nome, cpf, data_nasc, senha)
    dados_usuario = (novo_usuario._nome, novo_usuario._cpf, novo_usuario._data_nasc, novo_usuario._senha)

    query = '''
        INSERT INTO usuarios (nome, cpf, data_nasc, senha)
        VALUES (?, ?, ?, ?)
    '''

    executar_no_banco(query, dados_usuario)

    return cpf

def cadastrar_endereco(*, logradouro, numero, bairro, cidade, uf, cpf_usuario):
    novo_endereco = Endereco(logradouro, numero, bairro, cidade, uf)
    dados_endereco = (novo_endereco._logradouro, novo_endereco._numero, novo_endereco._bairro, novo_endereco._cidade, novo_endereco._uf, cpf_usuario)

    query = '''
        INSERT INTO enderecos (logradouro, numero, bairro, cidade, uf, cpf_usuario)
        VALUES (?, ?, ?, ?, ?, ?)
    '''

    executar_no_banco(query, dados_endereco)

def cadastrar_conta(*, cpf_usuario):
    nova_conta = Conta(cpf_usuario)
    dados_conta = (nova_conta._agencia, nova_conta._saldo, nova_conta._limite, nova_conta._limite_saques, nova_conta._cpf_usuario)

    query = '''
        INSERT INTO contas (agencia, saldo, limite_valor_saque, limite_quantidade_saques, cpf_usuario)
        VALUES (?, ?, ?, ?, ?)
    '''

    executar_no_banco(query, dados_conta)

def depositar (valor, cpf_usuario, numero_conta):
    try:
        valor = float(valor)
        if valor > 0:
            query = "UPDATE contas SET saldo = saldo + ? WHERE cpf_usuario = ?"
            dados_deposito = valor, cpf_usuario
            executar_no_banco(query, dados_deposito)

            data = date.today().strftime("%d/%m/%Y")
            hora = datetime.now().strftime('%H:%M:%S')

            query = '''
                INSERT INTO transacoes (tipo_transacao, valor, numero_conta, data, hora)
                VALUES (?, ?, ?, ?, ?)
            '''
            tipo = "deposito"
            dados_transacao = tipo, valor, numero_conta, data, hora
            executar_no_banco(query, dados_transacao)

            print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("\nPor favor, digite um valor válido!\n")
    except ValueError:
            print("\nErro ao processar a solicitação. Por favor, tente novamente!\n")

def sacar (valor, cpf_usuario, numero_conta):
    try:
        valor = float(valor)

        if valor > 0:
            try:
                conexao = sqlite3.connect(db_path)
                cursor = conexao.cursor()

                cursor.execute("SELECT saldo, limite_valor_saque, limite_quantidade_saques FROM contas WHERE cpf_usuario = ?", (cpf_usuario,))
                resultado = cursor.fetchone()
                saldo = resultado[0]
                limite_valor_saque = resultado[1]
                limite_quantidade_saques = resultado[2]

                tipo = "saque"
                data_atual = date.today().strftime("%d/%m/%Y")
                cursor.execute("SELECT COUNT(*) FROM transacoes WHERE numero_conta = ? AND tipo_transacao = ? AND data = ?", (numero_conta, tipo, data_atual,))
                contagem_saques = cursor.fetchone()
                quantidade_saques = contagem_saques[0]

                if (saldo - valor < 0):
                    print("\nErro ao realizar saque! Confira o saldo da sua conta.\n")
                elif valor > limite_valor_saque:
                    print(f"\nQuantidade não permitida! É apenas permitido saques de até R$ {limite_valor_saque},00\n")
                elif quantidade_saques == limite_quantidade_saques:
                    print("\nNão foi possível realizar a operação! O limite de saques diários foi atingido.\n")
                else:
                    query = "UPDATE contas SET saldo = saldo - ? WHERE cpf_usuario = ?"
                    dados_saque = valor, cpf_usuario
                    executar_no_banco(query, dados_saque)

                    data = date.today().strftime("%d/%m/%Y")
                    hora = datetime.now().strftime('%H:%M:%S')

                    query = '''
                        INSERT INTO transacoes (tipo_transacao, valor, numero_conta, data, hora)
                        VALUES (?, ?, ?, ?, ?)
                    '''
                    dados_transacao = tipo, valor, numero_conta, data, hora
                    executar_no_banco(query, dados_transacao)

                    print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!\n")
            except sqlite3.Error as e:
                print(f"Erro ao executar a operação!: {e}")
                return None
            finally:
                conexao.close()

        else:
            print("\nPor favor, digite um valor válido!\n")
    except ValueError:
        print("\nErro ao processar a solicitação. Por favor, tente novamente!\n")

def extrato (numero_conta, tipo_operacao, data_inicial = None, data_final = None):
    try:
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        query = """
            SELECT c.numero_conta,
                c.saldo,
                t.valor, 
                t.tipo_transacao,
                t.data,
                t.hora
            FROM contas c
            JOIN transacoes t ON c.numero_conta = t.numero_conta
            WHERE c.numero_conta = ? AND t.tipo_transacao LIKE ? 
        """

        # Adicionando o filtro de data, se ambos os valores forem fornecidos
        if data_inicial and data_final:
            query += " AND t.data BETWEEN ? AND ?"
            params = (numero_conta, tipo_operacao, data_inicial, data_final)
        else:
            # Se não fornecer intervalo de datas, vamos usar o tipo e retornar tudo
            params = (numero_conta, tipo_operacao,)

        cursor.execute(query, params)
        resultados = cursor.fetchall()

        print(f"\n{'Valor Transação':<20}{'Tipo Transação':<20}{'Data':<20}{'Hora':<20}")
        print("-" * 95)

        for linha in resultados:
            numero_conta, saldo_atual, valor, tipo_transacao, data, hora = linha
            print(f"R$ {valor:<20.2f}{tipo_transacao:<20}{data:<20}{hora:<20}")

        print(f"\nSaldo atual: R$ {saldo_atual:<20.2f}\n")
        print("-" * 95)

    except sqlite3.Error as e:
        print(f"Erro ao executar a operação SQLite: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
    finally:
        conexao.close()
    
def main():

    while True:
        opcao = menu_usuario()

        if opcao == '1':
            print("\n----- Entrar na conta -----\n")

            login = input("Digite seu CPF: ").strip()
            password = input("Digite sua senha: ").strip()
            if len(login) == 11 and login.isdigit() and len(password) == 6 and password.isdigit():
                login = str(login)
                password = str(password)
                usuario_logado, nome_usuario, cpf_usuario, numero_conta = login_usuario(login, password)
            else:
                print("\nFormato de CPF ou senha inválido! O CPF deve ter 11 dígitos numéricos e a senha 6 dígitos numéricos.\n")
                usuario_logado = None

            if usuario_logado:
                while True:
                    opcao = menu_conta(nome_usuario)

                    if opcao == 'd':
                        valor_deposito = input("\nDigite a quantidade que deseja depositar: ")
                        depositar(valor_deposito, cpf_usuario, numero_conta)

                    elif opcao == 's':
                        valor_saque = input("\nDigite a quantidade que deseja sacar: ")
                        sacar(valor_saque, cpf_usuario, numero_conta)

                    elif opcao == 'e':
                        try:
                            tipo_operacao = input(textwrap.dedent("""
                                ---------------------------------
                                            
                                Escolha o tipo da operação:
                                        
                                [d] Depósito
                                [s] Saque
                                [t] Todas as operações
                                            
                                ---------------------------------
                                            
                                => """)).strip().lower()
                            
                            if tipo_operacao not in ["d", "s", "t"]:
                                print("\nOpção inválida!\n")
                            else:
                                tipo_operacao = {"d": "deposito", "s": "saque", "t": "%"}.get(tipo_operacao)
                                
                                periodo = input(textwrap.dedent("""
                                    ---------------------------------
                                                                                            
                                    Deseja filtrar por período?

                                    [s] Sim
                                    [n] Não
                                                                
                                    ---------------------------------                            

                                    => """)).strip().lower()

                                while periodo != "s" and periodo != "n":
                                    print("\nOpção inválida!\n")
                                    periodo = input(textwrap.dedent("""
                                        ---------------------------------
                                                                                                
                                        Deseja filtrar por período?

                                        [s] Sim
                                        [n] Não
                                                                    
                                        ---------------------------------                            

                                        => """)).strip().lower()
                                
                                if periodo == "s":
                                    while True:
                                        try:
                                            data_inicial = input("Data inicial (dd/mm/aaaa): ").strip()
                                            data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
                                            break
                                        except ValueError:
                                            print("\nFormato de data inválido! Por favor, insira no formato dd/mm/aaaa.\n")

                                    while True:
                                        try:
                                            data_final = input("Data final (dd/mm/aaaa): ").strip()
                                            data_final = datetime.strptime(data_final, "%d/%m/%Y")
                                            break
                                        except ValueError:
                                            print("\nFormato de data inválido! Por favor, insira no formato dd/mm/aaaa.\n")

                                    data_inicial = data_inicial.strftime("%d/%m/%Y")
                                    data_final = data_final.strftime("%d/%m/%Y")
                                
                                if periodo == "n":
                                    data_inicial = None
                                    data_final = None

                                extrato(numero_conta, tipo_operacao, data_inicial, data_final)

                        except ValueError:
                            print("\nErro ao processar a solicitação. Por favor, tente novamente!\n")

                    elif opcao == 'i':
                        try:
                            conexao = sqlite3.connect(db_path)
                            cursor = conexao.cursor()

                            query = """
                                SELECT u.nome,
                                    u.cpf,
                                    u.data_nasc, 
                                    e.logradouro,
                                    e.numero,
                                    e.bairro,
                                    e.cidade,
                                    e.uf
                                FROM usuarios u
                                JOIN enderecos e ON u.cpf = e.cpf_usuario
                                WHERE cpf = ?
                            """

                            cursor.execute(query, (cpf_usuario,))
                            resultados = cursor.fetchall()

                            nome_info, cpf_info, data_nasc_info, logradouro_info, numero_info, bairro_info, cidade_info, uf_info = resultados[0]

                            print("\n------- Dados cadastrais -------\n")
                            print(textwrap.dedent(f"""
                                Nome: {nome_info}
                                CPF: {cpf_info}
                                Data de Nascimento: {data_nasc_info}

                                Logradouro: {logradouro_info}
                                Número: {numero_info}
                                Bairro: {bairro_info}
                                Cidade: {cidade_info}
                                UF: {uf_info}
                            """))
                            print("\n--------------------------------\n")

                        except sqlite3.Error as e:
                            print(f"Erro ao executar a operação SQLite: {e}")
                        except Exception as e:
                            print(f"Erro inesperado: {e}")
                        finally:
                            conexao.close()

                    elif opcao == 'l':
                        try:
                            conexao = sqlite3.connect(db_path)
                            cursor = conexao.cursor()

                            query = """
                                SELECT u.nome,
                                    u.cpf,
                                    c.numero_conta, 
                                    c.agencia
                                FROM usuarios u
                                JOIN contas c ON u.cpf = c.cpf_usuario
                                WHERE cpf = ?
                            """

                            cursor.execute(query, (cpf_usuario,))
                            resultados = cursor.fetchall()

                            nome_info, cpf_info, numero_conta_info, agencia_info = resultados[0]

                            print("\n------- Dados bancários -------\n")
                            print(textwrap.dedent(f"""
                                Numero da conta: {numero_conta_info}
                                Agência: {agencia_info}
                                Titular: {nome_info}
                                CPF: {cpf_info}
                            """))
                            print("\n--------------------------------\n")

                        except sqlite3.Error as e:
                            print(f"Erro ao executar a operação SQLite: {e}")
                        except Exception as e:
                            print(f"Erro inesperado: {e}")
                        finally:
                            conexao.close()

                    elif opcao == 'q':
                        print("\nSaindo da conta...\n")
                        break

                    else:
                        print("\nOpção inválida! Tente novamente.\n")

            else:
                print("\nCPF ou senha incorretos, ou não encontrados! Por favor, tente novamente ou faça seu cadastro.\n")
            
        elif opcao == '2':
            print("\n----- Realizar Cadastro -----\n")

            while True:
                cpf = input("CPF: ").strip()

                if len(cpf) == 11 and cpf.isdigit():
                    cpf = str(cpf)
                    usuario_existe = verifica_usuario(cpf)
                    break
                else:
                    print("\nFormato de CPF inválido! Tente novamente.\n")

            if not usuario_existe:
                while True:
                    senha = input("Senha (06 dígitos numéricos): ").strip()
                    if len(senha) == 6 and senha.isdigit():
                        senha = str(senha)
                        break
                    else:
                        print("\nSenha inválida. Tente novamente.\n")
                
                while True:
                    nome = input("Nome: ").strip()
                    if nome and all(c.isalpha() or c.isspace() for c in nome):
                         break
                    else:
                        print("\nNome inválido! Por favor, tente novamente.\n")

                while True:
                    try:
                        data_nasc = input("Data de nascimento (dd/mm/aaaa): ").strip()
                        data_nasc = datetime.strptime(data_nasc, "%d/%m/%Y")
                        data_nasc = data_nasc.strftime("%d/%m/%Y")
                        break
                    except ValueError:
                        print("\nData inválida! Por favor, digite novamente.\n")

                while True:
                    logradouro = input("Logradouro: ").strip()
                    numero = input("Número: ").strip()
                    bairro = input("Bairro: ").strip()
                    cidade = input("Cidade: ").strip()
                    uf = input("UF: ").strip()

                    if logradouro and numero and bairro and cidade and uf:
                        break
                    else:
                        print("\nAlgum campo está vazio. Por favor, tente novamente!\n")

                cpf_usuario = cadastrar_usuario(nome= nome, cpf= cpf, data_nasc= data_nasc, senha= senha)
                cadastrar_endereco(logradouro= logradouro, numero= numero, bairro= bairro, cidade= cidade, uf= uf, cpf_usuario= cpf_usuario)
                cadastrar_conta(cpf_usuario= cpf_usuario)
            else:
                print("\nUsuário já cadastrado!\n")

        elif opcao == '3':
            print("\nSaindo da aplicação...\n")
            break

        else:
            print("\nOpção inválida! Tente novamente.\n")

main()