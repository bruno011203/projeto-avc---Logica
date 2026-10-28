import dados
from utils import cabecalho, mensagem_erro, pausar, ler_inteiro


def _moeda(valor):
    texto=f"{valor:,.2f}"
    texto= texto.replace(",", "X").replace(".", ".").replace("X", ".")
    return "R$" + texto

def _achar_produto(codigo):
    """Devolve o dicionario do produto ou None se nao existir"""
    for produto in dados.produtos:
        if produto["codigo"] == codigo:
            return produto
    return None

def _achar_cliente(codigo):
    """Devolve o dicionario do cliente ou None se nao existir"""
    for cliente in dados.clientes:
        if cliente["codigo"] == codigo:
            return cliente
        return None

def _total_do_pedido(codigo):
    """Soma qtd x preco de cada item do pedido"""
    total=0
    for item in pedido["itens"]:
        produto = _achar_produto(Item["codigo"])
        if produto is not None:
            total += item["qtd"] * produto["preco"]
    return total


#Relatorios
def relatorio_estoque_critico():
    """Imprime os produtos abaixo do estoque minimo, do mais critico para o menos critico"""
    cabecalho("Estoque critico")

    criticos=[]
    for produto in dados.produtos:
        if produto["qtd"] < produto["estoque_minimo"]:
            criticos.append(produto)

        if len(criticos) == 0:
            print("Nenhum produto abaixo do estoque minimo.")
        return

    criticos = sorted(criticos, key=lambda p:["estoque minimo"] - p["qtd"], reverse=True)
    #O sorted() recebe uma lista e devolve uma versão ordenada dela
    #O key diz ao sorted qual valor usar para comparar os produtos.
    #lambda p: é uma função de uma linha, sem nome; ela recebe um produto e devolve um número
    #sorted ordena do menor para o maior, com reverse=True, ele inverte e põe o maior primeiro

    print(f"{'codigo':<8}{'produto':<28}{'saldo':>7}{'minimo':>8}{'falta':>7}")
    print("-" * 56)
    for produto in criticos:
        falta = produto["estoque_minimo"] - produto["quantidade"]
        print(f"{produto['codigo']:<8}{produto['nome']:<26}"
              f"{produto['qtd']:>7}{produto['estoque_minimo']:>8}{falta:>7}")
    print("-") * 56
    print(f"Total de produtos em situacao critica: {len(criticos)}")


def relatorio_por_giro():
     """Conta quanto de cada produto saiu nos pedidos e imprime 
     do mais vendido para o menos vendido. Pedidos cancelados nao contam como venda"""
     cabecalho("Giro de produtos")

     vendido = []
     for pedido in dados.pedidos:
         if pedido["status"] == "cancelado":
             continue
         for item in pedido["itens"]:
             codigo = item["codigo"]
             vendido[codigo] - vendido.get(codigo, 0) + item["qtd"]

    if len(vendido) == 0:
        print("Nenhum ")