# clientes.py - cadastro de clientes da distribuidora

import dados
from utils import cabecalho, mensagem_erro, mensagem_ok, ler_inteiro, ler_texto, pausar

TIPOS_VALIDOS = ["Bar", "Mercado", "Restaurante", "Adega"]



# FUNCOES PRINCIPAIS (as que o guia do grupo pede)


def cadastrar_cliente(nome, tipo, bairro, telefone):
    """Monta o dicionario do cliente e acrescenta em dados.clientes.
    tipo e um destes: Bar, Mercado, Restaurante, Adega.
    Usa dados.proximo_codigo_cliente e soma 1 nele."""
    cliente = {
        "codigo": dados.proximo_codigo_cliente,
        "nome": nome,
        "tipo": tipo,
        "bairro": bairro,
        "telefone": telefone,
    }
    dados.clientes.append(cliente)
    dados.proximo_codigo_cliente += 1
    return cliente


def imprimir_tabela(lista):
    """Imprime uma lista de clientes em formato de tabela."""
    print(f"{'COD':<5}{'NOME':<22}{'TIPO':<13}{'BAIRRO':<15}{'TELEFONE'}")
    print("-" * 65)
    for c in lista:
        print(f"{c['codigo']:<5}{c['nome']:<22}{c['tipo']:<13}{c['bairro']:<15}{c['telefone']}")


def listar_clientes():
    """Imprime todos os clientes em formato de tabela."""
    cabecalho("Clientes cadastrados")

    if len(dados.clientes) == 0:
        print("Nenhum cliente cadastrado.")
        return

    imprimir_tabela(dados.clientes)


def buscar_cliente(codigo):
    """Retorna o dicionario do cliente, ou None se nao existir.
    USADA PELO MODULO DE PEDIDOS."""
    for c in dados.clientes:
        if c["codigo"] == codigo:
            return c
    return None


def listar_por_bairro(bairro):
    """Retorna so os clientes de um bairro."""
    resultado = []
    for c in dados.clientes:
        if c["bairro"].lower() == bairro.lower():
            resultado.append(c)
    return resultado


def alterar_cliente(codigo, campo, novo_valor):
    """Altera um campo do cliente.
    Retorna False se o cliente ou o campo nao existir."""
    cliente = buscar_cliente(codigo)
    if cliente is None:
        return False
    if campo == "codigo" or campo not in cliente:
        return False
    cliente[campo] = novo_valor
    return True


def remover_cliente(codigo):
    """Remove o cliente da lista. Retorna False se nao existir."""
    cliente = buscar_cliente(codigo)
    if cliente is None:
        return False
    dados.clientes.remove(cliente)
    return True



# TELAS DO MENU (conversam com o usuario e chamam as funcoes acima)

def ler_tipo():
    """Pergunta o tipo do cliente ate o usuario digitar um tipo valido."""
    while True:
        valor = ler_texto("Tipo (Bar, Mercado, Restaurante, Adega): ").capitalize()
        if valor in TIPOS_VALIDOS:
            return valor
        mensagem_erro("Tipo invalido. Escolha: Bar, Mercado, Restaurante ou Adega.")


def tela_cadastrar():
    cabecalho("Cadastrar cliente")
    nome = ler_texto("Nome: ")
    tipo = ler_tipo()
    bairro = ler_texto("Bairro: ")
    telefone = ler_texto("Telefone: ")
    cliente = cadastrar_cliente(nome, tipo, bairro, telefone)
    mensagem_ok("Cliente cadastrado com o codigo " + str(cliente["codigo"]) + ".")


def tela_buscar():
    cabecalho("Buscar cliente")
    codigo = ler_inteiro("Codigo do cliente: ")
    cliente = buscar_cliente(codigo)
    if cliente is None:
        mensagem_erro("Cliente nao encontrado.")
    else:
        imprimir_tabela([cliente])


def tela_bairro():
    cabecalho("Clientes por bairro")
    bairro = ler_texto("Bairro: ")
    achados = listar_por_bairro(bairro)
    if len(achados) == 0:
        mensagem_erro("Nenhum cliente nesse bairro.")
    else:
        imprimir_tabela(achados)


def tela_alterar():
    cabecalho("Alterar cliente")
    codigo = ler_inteiro("Codigo do cliente: ")
    if buscar_cliente(codigo) is None:
        mensagem_erro("Cliente nao encontrado.")
        return

    print("1 - Nome")
    print("2 - Tipo")
    print("3 - Bairro")
    print("4 - Telefone")
    opcao = ler_inteiro("Qual campo alterar? ")

    campos = {1: "nome", 2: "tipo", 3: "bairro", 4: "telefone"}
    if opcao not in campos:
        mensagem_erro("Opcao invalida.")
        return

    campo = campos[opcao]
    if campo == "tipo":
        novo_valor = ler_tipo()
    else:
        novo_valor = ler_texto("Novo valor: ")

    alterar_cliente(codigo, campo, novo_valor)
    mensagem_ok("Cliente alterado.")


def tela_remover():
    cabecalho("Remover cliente")
    codigo = ler_inteiro("Codigo do cliente: ")
    if buscar_cliente(codigo) is None:
        mensagem_erro("Cliente nao encontrado.")
        return

    # Nao deixa apagar cliente que ja tem pedido (o pedido guarda o codigo dele)
    for p in dados.pedidos:
        if p["cliente"] == codigo:
            mensagem_erro("Este cliente tem pedidos e nao pode ser removido.")
            return

    resposta = ler_texto("Tem certeza? (s/n): ").lower()
    if resposta == "s":
        remover_cliente(codigo)
        mensagem_ok("Cliente removido.")
    else:
        print("Remocao cancelada.")


def menu_clientes():
    """Submenu do modulo, chamado pelo main.py."""
    while True:
        cabecalho("Clientes")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Buscar cliente por codigo")
        print("4 - Listar clientes por bairro")
        print("5 - Alterar cliente")
        print("6 - Remover cliente")
        print("0 - Voltar")

        opcao = ler_inteiro("Escolha uma opcao: ")

        if opcao == 1:
            tela_cadastrar()
        elif opcao == 2:
            listar_clientes()
        elif opcao == 3:
            tela_buscar()
        elif opcao == 4:
            tela_bairro()
        elif opcao == 5:
            tela_alterar()
        elif opcao == 6:
            tela_remover()
        elif opcao == 0:
            break
        else:
            mensagem_erro("Opcao invalida.")
            continue

        pausar()


if __name__ == "__main__":
    # Teste do modulo - nao roda quando o main.py importa este arquivo
    cadastrar_cliente("Padaria Boa", "Mercado", "Centro", "11 95555-0000")
    listar_clientes()
    print("Buscar codigo 2:", buscar_cliente(2))
    print("Buscar codigo 99 (nao existe):", buscar_cliente(99))
    print("Bairro Socorro:", listar_por_bairro("socorro"))
    print("Bairro Lua (nao existe):", listar_por_bairro("Lua"))
    print("Alterar telefone do 1:", alterar_cliente(1, "telefone", "11 90000-0000"))
    print("Alterar codigo 99 (nao existe):", alterar_cliente(99, "telefone", "x"))
    print("Remover codigo 4:", remover_cliente(4))
    print("Remover codigo 99 (nao existe):", remover_cliente(99))
