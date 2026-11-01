# fila.py - Fila FIFO de separacao de pedidos (SIGEP)
# Distribuidora Vale Azul Bebidas Ltda.
#
# FIFO = First In, First Out (o primeiro que entra e o primeiro que sai).
# A fila e a lista "fila_separacao" do dados.py. Ela guarda apenas o NUMERO
# do pedido. Os dados completos do pedido continuam na lista "pedidos".
#
# IMPORTANTE: nunca escreva "fila_separacao = []" neste arquivo.
# Isso criaria uma lista nova e desconectaria dos outros modulos.
# Use sempre append(), pop() e remove(), que alteram a lista original.

from dados import fila_separacao, pedidos, clientes, produtos
from utils import cabecalho, mensagem_erro, mensagem_ok, pausar, ler_inteiro


# ---------------------------------------------------------------
# FUNCOES AUXILIARES (pequenas ajudas usadas pelas funcoes principais)
# ---------------------------------------------------------------

def buscar_pedido(numero):
    """Procura um pedido pelo numero. Devolve o pedido ou None."""
    for pedido in pedidos:
        if pedido["numero"] == numero:
            return pedido
    return None


def nome_do_cliente(codigo):
    """Recebe o codigo do cliente e devolve o nome dele."""
    for cliente in clientes:
        if cliente["codigo"] == codigo:
            return cliente["nome"]
    return "Cliente nao encontrado"


def nome_do_produto(codigo):
    """Recebe o codigo do produto e devolve o nome dele."""
    for produto in produtos:
        if produto["codigo"] == codigo:
            return produto["nome"]
    return "Produto nao encontrado"


def buscar_produto_por_codigo(codigo):
    """Procura um produto pelo codigo. Devolve o produto ou None."""
    for produto in produtos:
        if produto["codigo"] == codigo:
            return produto
    return None


def itens_sem_estoque(pedido):
    """Confere se ha saldo para todos os itens do pedido.
    Devolve uma lista de textos com o que falta (lista vazia = tem tudo)."""
    faltando = []
    for item in pedido["itens"]:
        produto = buscar_produto_por_codigo(item["codigo"])
        if produto is None:
            faltando.append("produto " + str(item["codigo"]) + " nao existe mais no cadastro")
        elif produto["quantidade"] < item["qtd"]:
            falta = item["qtd"] - produto["quantidade"]
            faltando.append(produto["nome"] + ": pedido " + str(item["qtd"])
                            + ", em estoque " + str(produto["quantidade"])
                            + " (faltam " + str(falta) + ")")
    return faltando


# ---------------------------------------------------------------
# FUNCOES PRINCIPAIS (uma para cada opcao do menu)
# ---------------------------------------------------------------

def adicionar_na_fila():
    """ENQUEUE: coloca um pedido no FINAL da fila."""
    cabecalho("Adicionar pedido na fila")
    numero = ler_inteiro("Numero do pedido: ")

    pedido = buscar_pedido(numero)

    if pedido is None:
        mensagem_erro("Pedido nao encontrado.")
        return

    if numero in fila_separacao:
        mensagem_erro("Este pedido ja esta na fila.")
        return

    if pedido["status"] != "aguardando":
        mensagem_erro("So pedidos com status 'aguardando' podem entrar na fila.")
        mensagem_erro("Status atual deste pedido: " + pedido["status"])
        return

    fila_separacao.append(numero)      # entra no final da fila
    pedido["status"] = "na fila"
    posicao = len(fila_separacao)
    mensagem_ok("Pedido " + str(numero) + " entrou na fila na posicao " + str(posicao) + ".")


def chamar_proximo():
    """DEQUEUE: tira o pedido do INICIO da fila para ser separado.
    Antes de tirar, confere o estoque. Se faltar algum produto, o pedido
    continua no inicio da fila e nada e descontado. Se tiver tudo,
    os itens sao descontados do estoque."""
    cabecalho("Chamar proximo da fila")

    if len(fila_separacao) == 0:
        mensagem_erro("A fila esta vazia. Nao ha pedidos para separar.")
        return

    numero = fila_separacao[0]         # olha o primeiro sem tirar ainda
    pedido = buscar_pedido(numero)

    faltando = itens_sem_estoque(pedido)
    if len(faltando) > 0:
        mensagem_erro("Estoque insuficiente para separar o pedido " + str(numero) + ":")
        for texto in faltando:
            print("  - " + texto)
        print("O pedido continua no inicio da fila. De entrada no estoque e chame de novo.")
        return

    fila_separacao.pop(0)              # sai do inicio da fila
    pedido["status"] = "separado"

    print("Pedido a separar: " + str(numero))
    print("Cliente: " + nome_do_cliente(pedido["cliente"]))
    print("Itens:")
    for item in pedido["itens"]:
        produto = buscar_produto_por_codigo(item["codigo"])
        produto["quantidade"] = produto["quantidade"] - item["qtd"]   # baixa no estoque
        print("  - " + str(item["qtd"]) + " x " + produto["nome"]
              + " (restam " + str(produto["quantidade"]) + ")")

    mensagem_ok("Pedido " + str(numero) + " marcado como separado e baixado do estoque.")

    for item in pedido["itens"]:
        produto = buscar_produto_por_codigo(item["codigo"])
        if produto["quantidade"] < produto["estoque_minimo"]:
            print("[ALERTA] " + produto["nome"] + " ficou abaixo do minimo ("
                  + str(produto["quantidade"]) + " de "
                  + str(produto["estoque_minimo"]) + ").")


def visualizar_fila():
    """Mostra todos os pedidos da fila, do primeiro ao ultimo."""
    cabecalho("Fila de separacao")

    if len(fila_separacao) == 0:
        print("A fila esta vazia.")
        return

    print("Posicao | Pedido | Cliente")
    print("-" * 50)
    posicao = 1
    for numero in fila_separacao:
        pedido = buscar_pedido(numero)
        cliente = nome_do_cliente(pedido["cliente"])
        print(str(posicao).ljust(7) + " | " + str(numero).ljust(6) + " | " + cliente)
        posicao += 1

    print("-" * 50)
    print("Total na fila: " + str(len(fila_separacao)))


def remover_da_fila():
    """Tira um pedido especifico da fila (ex.: cliente cancelou)."""
    cabecalho("Remover pedido da fila")

    if len(fila_separacao) == 0:
        mensagem_erro("A fila esta vazia.")
        return

    numero = ler_inteiro("Numero do pedido a remover: ")

    if numero not in fila_separacao:
        mensagem_erro("Este pedido nao esta na fila.")
        return

    fila_separacao.remove(numero)
    pedido = buscar_pedido(numero)
    pedido["status"] = "aguardando"    # volta ao status original
    mensagem_ok("Pedido " + str(numero) + " removido da fila.")


# ---------------------------------------------------------------
# SUBMENU (e esta funcao que o main.py chama)
# ---------------------------------------------------------------

def menu_fila():
    while True:
        cabecalho("Fila de separacao")
        print("1 - Adicionar pedido na fila")
        print("2 - Chamar proximo da fila")
        print("3 - Visualizar fila")
        print("4 - Remover pedido da fila")
        print("0 - Voltar ao menu principal")

        opcao = ler_inteiro("Escolha uma opcao: ")

        if opcao == 1:
            adicionar_na_fila()
        elif opcao == 2:
            chamar_proximo()
        elif opcao == 3:
            visualizar_fila()
        elif opcao == 4:
            remover_da_fila()
        elif opcao == 0:
            break
        else:
            mensagem_erro("Opcao invalida.")

        if opcao != 0:
            pausar()


# Permite testar este arquivo sozinho (botao direito > Run 'fila').
# Quando o main.py importa o fila.py, este bloco NAO roda.
if __name__ == "__main__":
    menu_fila()
