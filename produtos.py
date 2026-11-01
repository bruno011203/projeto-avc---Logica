# produtos.py - cadastro de produtos
import dados
from utils import cabecalho, mensagem_erro, mensagem_ok, pausar, ler_inteiro, ler_decimal, ler_texto

CAMPOS_ALTERAVEIS = ["nome", "categoria", "preco", "quantidade", "estoque_minimo"]


def cadastrar_produto(nome, categoria, preco, quantidade, estoque_minimo):
    """Monta o dicionario do produto e acrescenta em dados.produtos.
    Usa dados.proximo_codigo_produto e soma 1 nele"""
    novo_produto = {
        "codigo": dados.proximo_codigo_produto,
        "nome": nome,
        "categoria": categoria,
        "preco": round(preco, 2),
        "quantidade": quantidade,
        "estoque_minimo": estoque_minimo
    }
    dados.produtos.append(novo_produto)
    dados.proximo_codigo_produto += 1
    return novo_produto["codigo"]


def listar_produtos():
    """Imprime todos os produtos em formato de tabela."""
    cabecalho("Lista de Produtos")
    if not dados.produtos:
        print("Nenhum produto cadastrado.")
        return

    print(f"{'Codigo':<6} {'Nome':<25} {'Categoria':<15} {'Preco (R$)':<10} {'Quantidade':<10} {'Estoque Minimo':<14}")
    print("-" * 85)
    for p in dados.produtos:
        print(f"{p['codigo']:<6} {p['nome']:<25} {p['categoria']:<15} {p['preco']:<10.2f} {p['quantidade']:<10} {p['estoque_minimo']:<14}")


def buscar_produto(codigo):
    """Retorna o dicionario do produto, ou None se nao existir.
    ESTA FUNCAO E USADA POR TODOS OS OUTROS MODULOS, NAO MEXER NELA"""
    for p in dados.produtos:
        if p["codigo"] == codigo:
            return p
    return None


def alterar_produto(codigo, campo, novo_valor):
    """Alterar um campo do produto (preco, nome, estoque_minimo...)"""
    produto = buscar_produto(codigo)
    if produto is None:
        return False
    if campo in CAMPOS_ALTERAVEIS:
        produto[campo] = novo_valor
        return True
    return False


def remover_produto(codigo):
    """Remove o produto da lista. Retorna False se nao existir."""
    produto = buscar_produto(codigo)
    if produto is None:
        return False
    dados.produtos.remove(produto)
    return True


def produto_em_pedido(codigo):
    """Retorna True se o produto aparece em algum pedido."""
    for pedido in dados.pedidos:
        for item in pedido["itens"]:
            if item["codigo"] == codigo:
                return True
    return False


def ler_preco(pergunta):
    """Pergunta ate o usuario digitar um preco maior que zero."""
    while True:
        valor = ler_decimal(pergunta)
        if valor > 0:
            return round(valor, 2)
        mensagem_erro("O preco deve ser maior que zero.")


def ler_inteiro_nao_negativo(pergunta):
    """Pergunta ate o usuario digitar um inteiro maior ou igual a zero."""
    while True:
        valor = ler_inteiro(pergunta)
        if valor >= 0:
            return valor
        mensagem_erro("O valor nao pode ser negativo.")


def menu_produtos():
    """Submenu do modulo, chamado pelo main.py."""
    while True:
        cabecalho("Menu de Produtos")
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Buscar Produto")
        print("4. Alterar Produto")
        print("5. Remover Produto")
        print("0. Voltar ao Menu Principal")

        opcao = ler_inteiro("Escolha uma opcao: ")

        if opcao == 1:
            cabecalho("Cadastrar Produto")
            nome = ler_texto("Nome do produto: ")
            categoria = ler_texto("Categoria: ")
            preco = ler_preco("Preco: ")
            quantidade = ler_inteiro_nao_negativo("Quantidade inicial em estoque: ")
            estoque_minimo = ler_inteiro_nao_negativo("Estoque minimo: ")

            codigo = cadastrar_produto(nome, categoria, preco, quantidade, estoque_minimo)
            mensagem_ok("Produto cadastrado com sucesso! Codigo: " + str(codigo))

        elif opcao == 2:
            listar_produtos()

        elif opcao == 3:
            cabecalho("Buscar Produto")
            codigo = ler_inteiro("Codigo do produto: ")
            produto = buscar_produto(codigo)
            if produto:
                print("Produto Encontrado")
                print(f"Codigo: {produto['codigo']}")
                print(f"Nome: {produto['nome']}")
                print(f"Categoria: {produto['categoria']}")
                print(f"Preco: {produto['preco']:.2f}")
                print(f"Quantidade: {produto['quantidade']}")
                print(f"Estoque Minimo: {produto['estoque_minimo']}")
            else:
                mensagem_erro("Produto nao encontrado.")

        elif opcao == 4:
            cabecalho("Alterar Produto")
            codigo = ler_inteiro("Digite o codigo do produto: ")
            produto = buscar_produto(codigo)
            if not produto:
                mensagem_erro("Produto nao encontrado.")
            else:
                print(f"Produto atual: {produto['nome']}")
                print("Campos disponiveis: nome, categoria, preco, quantidade, estoque_minimo")
                campo = ler_texto("Qual campo deseja alterar? ").strip().lower()
                if campo not in CAMPOS_ALTERAVEIS:
                    mensagem_erro("Campo invalido.")
                else:
                    if campo == "preco":
                        novo_valor = ler_preco("Novo preco: ")
                    elif campo in ["quantidade", "estoque_minimo"]:
                        novo_valor = ler_inteiro_nao_negativo("Novo valor inteiro: ")
                    else:
                        novo_valor = ler_texto("Novo valor: ")

                    if alterar_produto(codigo, campo, novo_valor):
                        mensagem_ok("Produto alterado com sucesso!")
                    else:
                        mensagem_erro("Erro ao alterar produto.")

        elif opcao == 5:
            cabecalho("Remover Produto")
            codigo = ler_inteiro("Digite o codigo do produto a remover: ")
            if buscar_produto(codigo) is None:
                mensagem_erro("Produto nao encontrado.")
            elif produto_em_pedido(codigo):
                # O pedido guarda o codigo do produto: remover deixaria o pedido sem preco
                mensagem_erro("Este produto aparece em pedidos e nao pode ser removido.")
            elif remover_produto(codigo):
                mensagem_ok("Produto removido com sucesso!")

        elif opcao == 0:
            break
        else:
            mensagem_erro("Opcao invalida.")
            continue

        pausar()


if __name__ == "__main__":
    # Teste do modulo - nao roda quando o main.py importa este arquivo
    listar_produtos()
    print("Buscar 101:", buscar_produto(101))
    print("Buscar 999 (nao existe):", buscar_produto(999))
    print("Novo codigo:", cadastrar_produto("Cha Gelado 1L", "Cha", 5.99, 40, 10))
    print("Alterar preco do 106:", alterar_produto(106, "preco", 6.49))
    print("Alterar campo invalido:", alterar_produto(106, "codigo", 1))
    print("Produto 101 em pedido:", produto_em_pedido(101))
    print("Produto 106 em pedido:", produto_em_pedido(106))
    print("Remover 106:", remover_produto(106))
    print("Remover 999 (nao existe):", remover_produto(999))
