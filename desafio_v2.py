import textwrap
from datetime import datetime

# Classes

class Usuario:
    def __init__(self, nome, cpf, data_nasc, endereco, senha):
        self._nome = nome
        self._cpf = cpf
        self._data_nasc = data_nasc
        self._endereco = endereco
        self._senha = senha
        self._conta = None

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nasc(self):
        return self._data_nasc

    @property
    def endereco(self):
        return self._endereco

    @property
    def senha(self):
        return self._senha
    
    def vincular_conta(self, conta):
        self._conta = conta

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Data de Nascimento: {self.data_nasc}\n"
                f"Endereço: {self.endereco}")
    
class Endereco:
    def __init__(self, rua, numero, bairro, cidade, uf):
        self._rua = rua
        self._numero = numero
        self._bairro = bairro
        self._cidade = cidade
        self._uf = uf

    def __str__(self):
        return f"{self._rua}, {self._numero} - {self._bairro}, {self._cidade}/{self._uf}"

class Conta:
    def __init__(self, usuario, numero_conta):
        self._usuario = usuario
        self._numero_conta = numero_conta
        self._agencia = '0001'
        self._saldo = 0
        self._limite = 500
        self._limite_saques = 3
        self._quantidade_saques = 0
        self._depositos_realizados = []
        self._saques_realizados = []
        usuario.vincular_conta(self)

    @property
    def numero_conta(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._agencia

    @property
    def saldo(self):
        return self._saldo

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    @property
    def quantidade_saques(self):
        return self._quantidade_saques

    @property
    def depositos_realizados(self):
        return self._depositos_realizados

    @property
    def saques_realizados(self):
        return self._saques_realizados
    
    def __str__(self):
        return (
            f"Titular: {self._usuario.nome}\n"
            f"CPF: {self._usuario.cpf}\n"
            f"Conta: {self._numero_conta}\n"
            f"Agência: {self._agencia}\n"
            f"Saldo: R$ {self._saldo:.2f}"
        )

    def depositar (self, valor):
        try:
            valor = float(valor)
            if valor > 0:
                self._saldo += valor
                data_hora = datetime.now()
                data_hora = data_hora.strftime("%d/%m/%Y %H:%M:%S")
                self._depositos_realizados.append((valor, data_hora))
                print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
                print(f"Saldo atual: R$ {self._saldo:.2f}\n")
            else:
                print("\nPor favor, digite um valor válido!\n")
        except ValueError:
                print("\nErro ao processar a solicitação. Por favor, tente novamente!\n")
    
    def sacar (self, valor):
        data_atual = datetime.now().date()
        contador_data = 0
        ultima_data_saque = None
        
        if self._saques_realizados:

            ultima_data_saque = datetime.strptime(self._saques_realizados[-1][1], "%d/%m/%Y %H:%M:%S").date()

            if ultima_data_saque != data_atual:
                contador_data = 0

            for saque in self._saques_realizados:
                data_saque = datetime.strptime(saque[1], "%d/%m/%Y %H:%M:%S").date()
                if data_saque == data_atual:
                    contador_data += 1

        try:
            valor = float(valor)
            if valor > 0:
                if (self._saldo - valor < 0):
                    print("\nErro ao realizar saque! Confira o saldo da sua conta.\n")
                elif valor > self._limite:
                    print(f"\nQuantidade não permitida! É apenas permitido saques de até R$ {self._limite},00\n")
                elif contador_data == self._limite_saques:
                    print("\nNão foi possível realizar a operação! O limite de saques diários foi atingido.\n")
                else:
                    self._saldo -= valor
                    data_hora = datetime.now()
                    data_hora = data_hora.strftime("%d/%m/%Y %H:%M:%S")
                    self._saques_realizados.append((valor, data_hora))
                    print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!\nSaldo da conta: R$ {self._saldo:.2f}\n")
            else:
                print("\nPor favor, digite um valor válido!\n")
        except ValueError:
            print("\nErro ao processar a solicitação. Por favor, tente novamente!\n")

    def extrato (self):
        #Formata os valores das listas com "R$" e 2 casas decimais
        depositos_formatados = "\n".join([f"Valor: R$ {float(valor):.2f} | Data e Hora: {data}" for valor, data in self._depositos_realizados])
        saques_formatados = "\n".join([f"Valor: R$ {float(valor):.2f} | Data e Hora: {data}" for valor, data in self._saques_realizados])

        print(textwrap.dedent("\n-------------------- Extrato da conta --------------------\n"))
        print(textwrap.dedent("Depósitos realizados:\n"))
        print(textwrap.dedent(f"{depositos_formatados}\n"))
        print(textwrap.dedent("Saques realizados:\n"))
        print(textwrap.dedent(f"{saques_formatados}\n"))
        print(textwrap.dedent(f"Saldo da conta: R$ {self._saldo:.2f}\n"))
        print(textwrap.dedent("----------------------------------------------------------"))
        
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

def verifica_usuario (cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return False

def login_usuario(login, password, usuarios):
    usuario = verifica_usuario(login, usuarios)

    if usuario:
        if usuario.senha == password:
            return usuario
        else:
            print("\nSenha incorreta!\n")
            return False
    else:
        return False

def cadastrar_usuario(*, nome, cpf, data_nasc, endereco, senha):
    novo_usuario = Usuario(nome, cpf, data_nasc, endereco, senha)
    return novo_usuario

def cadastrar_endereco(*, logradouro, numero, bairro, cidade, estado):
    novo_endereco = Endereco(logradouro, numero, bairro, cidade, estado)
    return novo_endereco

def cadastrar_conta(*, usuario, numero_conta):
    nova_conta = Conta(usuario, numero_conta)
    return nova_conta

def main():
    usuarios = []
    admins = [{'nome': 'Admin', 'cpf': '12345678911', 'senha': '123456'}]
    contas = []
    numero_conta = 1

    while True:
        opcao = menu_usuario()

        if opcao == '1':
            print("\n----- Entrar na conta -----\n")

            login = input("Digite seu CPF: ").strip()
            password = input("Digite sua senha: ").strip()
            if len(login) == 11 and login.isdigit() and len(password) == 6 and password.isdigit():
                login = str(login)
                password = str(password)
                usuario_logado = login_usuario(login, password, usuarios)
            else:
                print("\nFormato de CPF ou senha inválido! O CPF deve ter 11 dígitos numéricos e a senha 6 dígitos numéricos.\n")
                usuario_logado = None

            if usuario_logado:
                while True:
                    opcao = menu_conta(usuario_logado.nome)

                    if opcao == 'd':
                        valor_deposito = input("\nDigite a quantidade que deseja depositar: ")
                        usuario_logado._conta.depositar(valor_deposito)

                    elif opcao == 's':
                        valor_saque = input("\nDigite a quantidade que deseja sacar: ")
                        usuario_logado._conta.sacar(valor_saque)

                    elif opcao == 'e':
                        try:
                            usuario_logado._conta.extrato()
                        except ValueError:
                            print("\nErro ao processar solicitação! Por favor, tente novamente.\n")

                    elif opcao == 'i':
                        print("\n------- Dados cadastrais -------\n")
                        print(usuario_logado)
                        print("\n--------------------------------\n")

                    elif opcao == 'l':
                        print("\n------- Dados bancários -------\n")
                        print(usuario_logado._conta)
                        print("\n--------------------------------\n")

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
                    usuario_existe = verifica_usuario(cpf, usuarios)
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
                    estado = input("Estado: ").strip()

                    if logradouro and numero and bairro and cidade and estado:
                        break
                    else:
                        print("\nAlgum campo está vazio. Por favor, tente novamente!\n")

                endereco = cadastrar_endereco(logradouro= logradouro, numero= numero, bairro= bairro, cidade= cidade, estado= estado)
                usuario = cadastrar_usuario(nome= nome, cpf= cpf, data_nasc= data_nasc, endereco= endereco, senha= senha)
                conta = cadastrar_conta(usuario= usuario, numero_conta= numero_conta)

                if endereco and usuario and conta:
                    usuarios.append(usuario)
                    contas.append(conta)
                    numero_conta += 1
                    print("\nUsuário e conta cadastrados com sucesso!\n")
                else:
                    print("\nErro ao processar solicitação! Por favor, tente novamente.\n")
            
            else:
                print("\nUsuário já cadastrado!\n")

        elif opcao == '3':
            print("\nSaindo da aplicação...\n")
            break

        elif opcao == 'master':

            login_admin = input("Login: ").strip()
            senha_admin = input("Senha: ").strip()

            if len(login_admin) == 11 and login_admin.isdigit() and len(senha_admin) == 6 and senha_admin.isdigit():

                login_adm = str(login_admin)
                senha_adm = str(senha_admin)

                admin_encontrado = False

                for adm in admins:
                    if adm['cpf'] == login_adm and str(adm['senha']) == senha_adm:
                        admin_encontrado = True
                        break

                if admin_encontrado:
                    menu_adm = textwrap.dedent("""
                    ---------------------------------

                    Bem-vindo, Admin!

                    Escolha uma das seguintes opções:

                    [u] Visualizar todos os usuários
                    [c] Visualizar todas as contas
                    [q] Sair

                    ---------------------------------
                    => """)

                    while True:
                        opcao_adm = input(menu_adm)

                        if opcao_adm not in ('u', 'c', 'q'):
                            print("\nOpção inválida! Tente novamente.\n")
                            continue

                        if opcao_adm == 'u':
                            print("\n--- Lista de Usuários ---\n")
                            for u in usuarios:
                                print(u)
                                print()

                        elif opcao_adm == 'c':
                            print("\n--- Lista de Contas ---\n")
                            for c in contas:
                                print(c)
                                print()

                        elif opcao_adm == 'q':
                            print("\nSaindo do modo Admin...\n")
                            break

                else:
                    print("\nLogin ou senha incorretos, ou não encontrados! Por favor, tente novamente.\n")

            else:
                print("\nPor favor, digite um login válido e uma senha de seis dígitos.\n")

        else:
            print("\nOpção inválida! Tente novamente.\n")

main()