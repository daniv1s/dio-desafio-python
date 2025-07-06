menu = """

Bem vindo ao sistema bancário!
Escolha uma das seguintes opções:

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

# Valores da conta

saldo = 0
limite = 500
LIMITE_SAQUES = 3
quantidade_saques = 0
depositos_realizados = []
saques_realizados = []

# Menu e opções

while True:
 
    opcao = input(menu)

    while opcao not in ('d', 's', 'e', 'q'):
        print("Opção inválida! Tente novamente.")
        opcao = input(menu)

    if opcao == "d":

        novo_deposito = input("Digite a quantidade que deseja depositar: ")

        try:
            valor_deposito = float(novo_deposito)

            if valor_deposito > 0:
                saldo += valor_deposito
                depositos_realizados.append(valor_deposito)
                print(f"Quantia depositada com sucesso!\nSaldo da conta: R$ {saldo:.2f}")
            else:
                print("Por favor, digite um valor válido!")
        except ValueError:
            print("Erro ao processar a solicitação. Por favor, tente novamente!")

    if opcao == "s":

        novo_saque = input("Digite a quantidade que deseja sacar: ")

        try:
            valor_saque = float(novo_saque)

            if valor_saque > 0:

                if (saldo - valor_saque < 0):
                    print("Erro ao realizar saque! Confira o saldo da sua conta.")
                elif valor_saque > limite:
                    print("Quantidade não permitida! É apenas permitido saques de até R$ 500,00")
                elif quantidade_saques == LIMITE_SAQUES:
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

    if opcao == "e":
        
         #Formata os valores das listas com "R$" e 2 casas decimais
        depositos_formatados = ", ".join([f"R$ {valor:.2f}" for valor in depositos_realizados])
        saques_formatados = ", ".join([f"R$ {valor:.2f}" for valor in saques_realizados])

        print(f"""
              --- Extrato da conta ---

              Depósitos realizados: {depositos_formatados}

              Saques realizados: {saques_formatados}

              Saldo da conta: R$ {saldo:.2f}
              """)

    if opcao == "q":
        print("Saindo da aplicação...")
        break