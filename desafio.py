from datetime import datetime

# Funções

def cria_usuario (*, nome, cpf, data_nasc, endereco, senha):

    novo_usuario = {
        'nome': nome,
        'cpf': cpf,
        'data_nasc': data_nasc,
        'endereco': endereco,
        'senha': senha
    }

    return novo_usuario

def cria_endereco (*, logradouro, numero, bairro, cidade, estado):
    
    endereco = {
        'logradouro': logradouro,
        'numero': numero,
        'bairro': bairro,
        'cidade': cidade,
        'estado': estado
    }

    return endereco

def cria_conta (*, cpf, numero_conta):

    conta = {
        'cpf': cpf,
        'numero_conta': numero_conta,
        'agencia': '0001',
        'saldo': 0,
        'limite': 500,
        'limite_saques': 3,
        'quantidade_saques': 0,
        'depositos_realizados': [],
        'saques_realizados': []
    }

    return conta

def saque (*, valor, saldo, limite, limite_saques, quantidade_saques, saques_realizados):

    try:
        valor_saque = float(valor)

        if valor_saque > 0:
            if (saldo - valor_saque < 0):
                print("Erro ao realizar saque! Confira o saldo da sua conta.")
            elif valor_saque > limite:
                print("Quantidade não permitida! É apenas permitido saques de até R$ 500,00")
            elif quantidade_saques == limite_saques:
                print("Não foi possível realizar a operação! O limite de saques diários foi atingido.")
            else:
                saldo -= valor_saque
                quantidade_saques += 1
                saques_realizados.append(valor_saque)
                print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!\nSaldo da conta: R$ {saldo:.2f}")
        else:
            print("Por favor, digite um valor válido!")

    except ValueError:
        print("Erro ao processar a solicitação. Por favor, tente novamente!")

    return saldo, quantidade_saques, saques_realizados

# Tela principal

usuarios = [
    {
    'nome': 'Admin',
    'cpf': '12345678911',
    'data_nasc': '01/01/2000',
    'endereco': {
        'logradouro': 'Rua das Flores',
        'numero': '841',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP'
        },
    'senha': '123456'
    }
    ]

contas = []

menu_usuario = """
---------------------------------

Bem vindo ao sistema bancário!

Escolha uma das seguintes opções:

[1] Entrar na conta
[2] Criar conta
[3] Criar usuário
[4] Sair

---------------------------------

=> """

# Opções menu_usuario

while True:

    opcao_usuario = input(menu_usuario)

    while opcao_usuario not in ('1', '2', '3', '4'):
        print("\nOpção inválida! Tente novamente.")
        opcao_usuario = input(menu_usuario)

    if opcao_usuario == '1':

        print("\n----- Entrar na conta -----\n")

        login = input("Digite seu CPF: ").strip()
        password = input("Digite sua senha: ").strip()

        if len(login) == 11 and login.isdigit() and len(password) == 6 and password.isdigit():

            cpf_entrada = str(login)
            senha_entrada = str(password)

            usuario_encontrado = False

            for i in usuarios:
                if i['cpf'] == cpf_entrada:
                    for chave_dic, valor_dic in i.items():
                        if chave_dic == 'senha' and str(valor_dic) == senha_entrada:
                            usuario_encontrado = True

                            # Dados cadastrais
                            nome_usuario = i['nome']
                            cpf_usuario = i['cpf']
                            data_nasc_usuario = i['data_nasc']
                            logradouro_usuario = i['endereco']['logradouro']
                            numero_usuario = i['endereco']['numero']
                            bairro_usuario = i['endereco']['bairro']
                            cidade_usuario = i['endereco']['cidade']
                            estado_usuario = i['endereco']['estado']

                            break
                    if usuario_encontrado:
                        break
            else:
                print("\nCPF ou senha incorretos, ou não encontrados! Por favor, tente novamente ou faça seu cadastro.")
            
            if usuario_encontrado:

                menu_conta = f"""
                ---------------------------------

                Bem vindo, {nome_usuario}!

                Escolha uma das seguintes opções:

                [d] Depositar
                [s] Sacar
                [e] Extrato
                [i] Dados cadastrais
                [q] Sair

                ---------------------------------

                => """

                # Opções menu_conta

                while True:
                
                    opcao_conta = input(menu_conta)

                    while opcao_conta not in ('d', 's', 'e', 'i', 'q'):
                        print("\nOpção inválida! Tente novamente.")
                        opcao_conta = input(menu_conta)

                    if opcao_conta == "d":

                        novo_deposito = input("\nDigite a quantidade que deseja depositar: ")

                        try:
                            valor_deposito = float(novo_deposito)

                            if valor_deposito > 0:
                                saldo += valor_deposito
                                depositos_realizados.append(valor_deposito)
                                print(f"\nQuantia depositada com sucesso!\nSaldo da conta: R$ {saldo:.2f}")
                            else:
                                print("\nPor favor, digite um valor válido!")
                        except ValueError:
                            print("\nErro ao processar a solicitação. Por favor, tente novamente!")

                    if opcao_conta == "s":
                        novo_saque = input("\nDigite a quantidade que deseja sacar: ")
                        saldo, quantidade_saques, saques_realizados = saque(valor = novo_saque, saldo = saldo, limite = limite, limite_saques = limite_saques, quantidade_saques = quantidade_saques, saques_realizados = saques_realizados)

                    if opcao_conta == "e":
                        
                        #Formata os valores das listas com "R$" e 2 casas decimais
                        depositos_formatados = ", ".join([f"R$ {valor:.2f}" for valor in depositos_realizados])
                        saques_formatados = ", ".join([f"R$ {valor:.2f}" for valor in saques_realizados])

                        print(f"""
                            --- Extrato da conta ---

                            Depósitos realizados: {depositos_formatados}

                            Saques realizados: {saques_formatados}

                            Saldo da conta: R$ {saldo:.2f}

                            ------------------------
                            """)

                    if opcao_conta == "i":
                        print(f"""
                              
                            ------- Dados cadastrais -------

                            Nome: {nome_usuario}
                            CPF: {cpf_usuario}
                            Data de nascimento: {data_nasc_usuario}
                            
                            Logradouro: {logradouro_usuario}
                            Número da casa: {numero_usuario}
                            Bairro: {bairro_usuario}
                            Cidade: {cidade_usuario}
                            Estado: {estado_usuario}

                            --------------------------------
                              
                            """)

                    if opcao_conta == "q":
                        print("\nSaindo da conta...")
                        break
        else:
            print("\nPor favor, digite um CPF válido e uma senha de seis dígitos.")

    if opcao_usuario == '2':
        
        print("\n----- Realizar Cadastro -----\n")

        while True:

            cpf = input("CPF: ").strip()
            senha = input("Senha (06 dígitos numéricos): ").strip()

            if len(cpf) == 11 and cpf.isdigit() and len(senha) == 6 and senha.isdigit():

                cpf_cadastro = str(cpf)
                senha_cadastro = str(senha)

                cliente_encontrado = False

                for i in usuarios:
                    if i['cpf'] == cpf_cadastro:
                        cliente_encontrado = True
                        break
                else:
                    while True:
                        nome_entrada = input("Nome: ").strip()
                        if nome_entrada and all(c.isalpha() or c.isspace() for c in nome_entrada):
                            nome = nome_entrada
                            break
                        else:
                            print("\nNome inválido! Por favor, tente novamente.")

                    while True:        
                        try:
                            entrada_data_nasc = input("Data de nascimento (dd/mm/aaaa): ").strip()
                            data_nasc_formato = datetime.strptime(entrada_data_nasc, "%d/%m/%Y")
                            data_nasc = data_nasc_formato.strftime("%d/%m/%Y")
                            break
                        except ValueError:
                            print("\nData inválida! Por favor, digite novamente.")

                    while True:
                        logradouro = input("Logradouro: ").strip()
                        numero = input("Número: ").strip()
                        bairro = input("Bairro: ").strip()
                        cidade = input("Cidade: ").strip()
                        estado = input("Estado: ").strip()

                        if logradouro and numero and bairro and cidade and estado:
                            break
                        else:
                            print("\nAlgum campo está vazio. Por favor, tente novamente!")

                    endereco = cria_endereco(logradouro = logradouro, numero = numero, bairro = bairro, cidade = cidade, estado = estado)
                    usuario = cria_usuario(nome = nome, cpf = cpf, data_nasc = data_nasc, endereco = endereco, senha = senha)

                    usuarios.append(usuario)
                    print("\nUsuário cadastrado com sucesso!")
                    break

                if cliente_encontrado:
                    print("\nUsuário já cadastrado!")
                    break
            else:
                print("\nPor favor, digite um CPF válido e uma senha de seis dígitos.")

    # if opcao_usuario == '3':

    if opcao_usuario == '4':
        print("\nSaindo da aplicação...")
        break
