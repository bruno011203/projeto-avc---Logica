# pedidos.py - cadastro e manutencao de pedidos
import dados
from utils import cabecalho, mensagem_erro, mensagem_ok, pausar, ler_inteiro


def criar_pedido(codigo_cliente):
    """Cria um pedido vazio com status 'aguardando'.
    Retorna o numero do pedido criado, ou None se o cliente nao existir."""
    cliente_existe = False
    for cliente in dados.clientes:
        if cliente["codigo"] == codigo_cliente:
            cliente_existe = True

    if not cliente_existe:
        return None

    numero = dados.proximo_numero_pedido
    novo_pedido = {"numero": numero, "cliente": codigo_cliente,
                   "status": "aguardando", "itens": []}
    dados.pedidos.append(novo_pedido)
    dados.proximo_numero_pedido += 1
    return numero


def adicionar_item(numero, codigo_produto, qtd):
    """Acrescenta um item na lista 'itens' do pedido.
    Retorna True se deu certo, False se algo estiver errado."""
    pedido = buscar_pedido(numero)
    if pedido is None:
        return False

    if pedido["status"] != "aguardando":
        return False

    if qtd <= 0:
        return False

    produto_existe = False
    for produto in dados.produtos:
        if produto["codigo"] == codigo_produto:
            produto_existe = True
    if not produto_existe:
        return False

    for item in pedido["itens"]:
        if item["codigo"] == codigo_produto:
            item["qtd"] += qtd
            return True

    pedido["itens"].append({"codigo": codigo_produto, "qtd": qtd})
    return True


def calcular_total(numero):
    """Soma qtd x preco de cada item do pedido.
    Retorna None se o pedido nao existir."""
    pedido = buscar_pedido(numero)
    if pedido is None:
        return None

    total = 0
    for item in pedido["itens"]:
        for produto in dados.produtos:
            if produto["codigo"] == item["codigo"]:
                total += item["qtd"] * produto["preco"]
    return total


def buscar_pedido(numero):
    """Retorna o dicionario do pedido, ou None se nao existir."""
    for pedido in dados.pedidos:
        if pedido["numero"] == numero:
            return pedido
    return None


def cancelar_pedido(numero):
    """Muda o status do pedido para 'cancelado'.
    Retorna True se cancelou, False se nao foi possivel."""
    pedido = buscar_pedido(numero)
    if pedido is None:
        return False

    if pedido["status"] != "aguardando":
        return False

    pedido["status"] = "cancelado"

    if numero in dados.fila_separacao:
        dados.fila_separacao.remove(numero)

    return True


def tela_novo_pedido():
    """Tela que conduz o usuario na criacao de um pedido."""
    cabecalho("Novo pedido")

    print("Clientes:")
    for cliente in dados.clientes:
        print(cliente["codigo"], "-", cliente["nome"])
    codigo_cliente = ler_inteiro("\nCodigo do cliente: ")

    numero = criar_pedido(codigo_cliente)
    if numero is None:
        mensagem_erro("Cliente nao encontrado.")
        pausar()
        return
    mensagem_ok("Pedido " + str(numero) + " criado.")

    print("\nProdutos:")
    for produto in dados.produtos:
        print(produto["codigo"], "-", produto["nome"],
              "- R$", f"{produto['preco']:.2f}")

    while True:
        codigo_produto = ler_inteiro("\nCodigo do produto (0 para finalizar): ")
        if codigo_produto == 0:
            break
        qtd = ler_inteiro("Quantidade: ")
        if adicionar_item(numero, codigo_produto, qtd):
            mensagem_ok("Item adicionado.")
        else:
            mensagem_erro("Nao foi possivel adicionar. Confira o produto e a quantidade.")

    if len(buscar_pedido(numero)["itens"]) == 0:
        cancelar_pedido(numero)
        mensagem_erro("Pedido sem itens foi cancelado.")
        pausar()
        return

    print("\nTotal do pedido: R$", f"{calcular_total(numero):.2f}")
    pausar()


def tela_consultar_pedido():
    """Tela que mostra os detalhes de um pedido."""
    cabecalho("Consultar pedido")
    numero = ler_inteiro("Numero do pedido: ")
    pedido = buscar_pedido(numero)
    if pedido is None:
        mensagem_erro("Pedido nao encontrado.")
        pausar()
        return

    nome_cliente = "(cliente nao encontrado)"
    for cliente in dados.clientes:
        if cliente["codigo"] == pedido["cliente"]:
            nome_cliente = cliente["nome"]

    print("\nPedido:", pedido["numero"])
    print("Cliente:", nome_cliente)
    print("Status:", pedido["status"])
    print("\nItens:")
    if len(pedido["itens"]) == 0:
        print("(nenhum item)")
    for item in pedido["itens"]:
        for produto in dados.produtos:
            if produto["codigo"] == item["codigo"]:
                subtotal = item["qtd"] * produto["preco"]
                print(item["qtd"], "x", produto["nome"], "- R$", f"{subtotal:.2f}")

    print("\nTotal: R$", f"{calcular_total(numero):.2f}")
    pausar()


def tela_cancelar_pedido():
    """Tela que cancela um pedido pelo numero."""
    cabecalho("Cancelar pedido")
    numero = ler_inteiro("Numero do pedido: ")
    if cancelar_pedido(numero):
        mensagem_ok("Pedido " + str(numero) + " cancelado.")
    else:
        mensagem_erro("Nao foi possivel cancelar. Confira se o pedido existe e esta aguardando.")
    pausar()


def menu_pedidos():
    """Submenu do modulo, chamado pelo main.py."""
    while True:
        cabecalho("Pedidos")
        print("1 - Novo pedido")
        print("2 - Consultar pedido")
        print("3 - Cancelar pedido")
        print("0 - Voltar")
        opcao = ler_inteiro("Escolha uma opcao: ")

        if opcao == 0:
            break
        elif opcao == 1:
            tela_novo_pedido()
        elif opcao == 2:
            tela_consultar_pedido()
        elif opcao == 3:
            tela_cancelar_pedido()
        else:
            mensagem_erro("Opcao invalida.")





##Bloco de testes

if __name__ == "__main__":
    # Teste do modulo - nao roda quando o main.py importa este arquivo
    print("Pedido 1:", buscar_pedido(1))
    print("Pedido 99:", buscar_pedido(99))

    print("Novo pedido:", criar_pedido(3))
    print("Outro pedido:", criar_pedido(1))
    print("Cliente inexistente:", criar_pedido(99))
    print("Buscar pedido 3:", buscar_pedido(3))
    print("Proximo numero:", dados.proximo_numero_pedido)

    print("Item novo:", adicionar_item(3, 101, 10))
    print("Mesmo produto de novo:", adicionar_item(3, 101, 5))
    print("Outro produto:", adicionar_item(3, 105, 2))
    print("Pedido inexistente:", adicionar_item(99, 101, 1))
    print("Produto inexistente:", adicionar_item(3, 999, 1))
    print("Quantidade zero:", adicionar_item(3, 101, 0))
    print("Quantidade negativa:", adicionar_item(3, 101, -4))
    print("Pedido 3:", buscar_pedido(3))

    print("Total do pedido 1:", calcular_total(1))
    print("Total do pedido 2:", calcular_total(2))
    print("Total do pedido 3:", calcular_total(3))
    print("Total do pedido 4 (vazio):", calcular_total(4))
    print("Total de pedido inexistente:", calcular_total(99))
    print("Total formatado do pedido 3:", f"{calcular_total(3):.2f}")

    print("Cancelar pedido 4:", cancelar_pedido(4))
    print("Status do pedido 4:", buscar_pedido(4)["status"])
    print("Cancelar de novo:", cancelar_pedido(4))
    print("Cancelar inexistente:", cancelar_pedido(99))
    print("Item em pedido cancelado:", adicionar_item(4, 101, 1))
    dados.fila_separacao.append(3)
    print("Fila antes:", dados.fila_separacao)
    print("Cancelar pedido 3 na fila:", cancelar_pedido(3))
    print("Fila depois:", dados.fila_separacao)
    dados.pedidos[0]["status"] = "separado"
    print("Cancelar pedido separado:", cancelar_pedido(1))
    print("Status do pedido 1:", buscar_pedido(1)["status"])