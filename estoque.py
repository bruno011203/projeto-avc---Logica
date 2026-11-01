# estoque.py - entrada, saida e alerta de estoque minimo do SIGEP
# Distribuidora Vale Azul Bebidas Ltda.

import dados
from utils import (cabecalho, mensagem_erro, mensagem_ok, pausar,
                   ler_inteiro)


def buscar_produto(codigo):
    """Procura um produto pelo codigo. Devolve o dicionario ou None."""
    for produto in dados.produtos:
        if produto["codigo"] == codigo:
            return produto
    return None


def abaixo_do_minimo(produto):
    """Devolve True se a quantidade em estoque esta abaixo do minimo."""
    return produto["quantidade"] < produto["estoque_minimo"]


def ler_quantidade_positiva(pergunta):
    """Pergunta ate o usuario digitar um inteiro maior que zero."""
    while True:
        valor = ler_inteiro(pergunta)
        if valor > 0:
            return valor
        mensagem_erro("A quantidade deve ser maior que zero.")


def pedir_produto():
    """Pede o codigo e devolve o produto, ou None se nao existir."""
    codigo = ler_inteiro("Codigo do produto: ")
    produto = buscar_produto(codigo)
    if produto is None:
        mensagem_erro("Produto " + str(codigo) + " nao encontrado.")
    return produto


def avisar_se_baixo(produto):
    """Mostra um aviso se o produto ficou abaixo do estoque minimo."""
    if abaixo_do_minimo(produto):
        print("[ALERTA] " + produto["nome"] + " esta abaixo do minimo ("
              + str(produto["quantidade"]) + " de "
              + str(produto["estoque_minimo"]) + ").")


def consultar_estoque():
    """Lista todos os produtos com a quantidade e a situacao do estoque."""
    cabecalho("Consulta de estoque")
    if len(dados.produtos) == 0:
        mensagem_erro("Nenhum produto cadastrado.")
        return

    print("%-6s %-24s %6s %6s  %s" % ("Cod", "Produto", "Qtd", "Min", "Situacao"))
    print("-" * 56)
    for produto in dados.produtos:
        if abaixo_do_minimo(produto):
            situacao = "BAIXO"
        else:
            situacao = "ok"
        print("%-6d %-24s %6d %6d  %s" % (produto["codigo"], produto["nome"],
                                         produto["quantidade"],
                                         produto["estoque_minimo"], situacao))


def registrar_entrada():
    """Soma ao estoque a quantidade que chegou de um fornecedor."""
    cabecalho("Entrada de estoque")
    produto = pedir_produto()
    if produto is None:
        return

    print("Produto: " + produto["nome"] + " | em estoque: "
          + str(produto["quantidade"]))
    qtd = ler_quantidade_positiva("Quantidade que entrou: ")

    produto["quantidade"] = produto["quantidade"] + qtd
    mensagem_ok("Entrada registrada. Novo estoque de " + produto["nome"]
                + ": " + str(produto["quantidade"]))


def registrar_saida():
    """Tira do estoque uma quantidade, sem deixar o saldo ficar negativo."""
    cabecalho("Saida de estoque")
    produto = pedir_produto()
    if produto is None:
        return

    print("Produto: " + produto["nome"] + " | em estoque: "
          + str(produto["quantidade"]))
    qtd = ler_quantidade_positiva("Quantidade que saiu: ")

    if qtd > produto["quantidade"]:
        mensagem_erro("Estoque insuficiente. Disponivel: "
                      + str(produto["quantidade"]))
        return

    produto["quantidade"] = produto["quantidade"] - qtd
    mensagem_ok("Saida registrada. Novo estoque de " + produto["nome"]
                + ": " + str(produto["quantidade"]))
    avisar_se_baixo(produto)


def alerta_estoque_minimo():
    """Lista os produtos abaixo do estoque minimo e quanto falta repor."""
    cabecalho("Alerta de estoque minimo")
    encontrou = False

    for produto in dados.produtos:
        if abaixo_do_minimo(produto):
            if not encontrou:
                print("%-6s %-24s %6s %6s %8s" % ("Cod", "Produto", "Qtd",
                                                  "Min", "Repor"))
                print("-" * 56)
                encontrou = True
            falta = produto["estoque_minimo"] - produto["quantidade"]
            print("%-6d %-24s %6d %6d %8d" % (produto["codigo"],
                                             produto["nome"],
                                             produto["quantidade"],
                                             produto["estoque_minimo"],
                                             falta))

    if not encontrou:
        mensagem_ok("Todos os produtos estao com estoque acima do minimo.")


def menu_estoque():
    """Submenu de estoque chamado pelo main.py."""
    while True:
        cabecalho("Estoque")
        print("1 - Entrada de estoque")
        print("2 - Saida de estoque")
        print("3 - Consultar estoque")
        print("4 - Alerta de estoque minimo")
        print("0 - Voltar")
        print("-" * 50)

        opcao = ler_inteiro("Escolha uma opcao: ")

        if opcao == 0:
            break
        elif opcao == 1:
            registrar_entrada()
        elif opcao == 2:
            registrar_saida()
        elif opcao == 3:
            consultar_estoque()
        elif opcao == 4:
            alerta_estoque_minimo()
        else:
            mensagem_erro("Opcao invalida. Escolha um numero de 0 a 4.")
            continue
        pausar()
