# produtos.py
import dados
from utils import cabecalho, mensagem_erro, mensagem_ok, ler_inteiro, ler_decimal, ler_texto

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

    print(f"{'Codigo':<6} {'Nome':<25} {'Categoria':<15} {'preco (R$)': <10} {'Quantidade':<6} {'Estoque Minimo':<6}")
    print("-" * 75)
for p in dados.produtos:
    print(f"{p['codigo']:<6} {p['nome']:<25} {p['categoria']:<15} {p['preco']:<10.2f} {p['quantidade']:<6} {p['estoque_minimo']:<6}") 


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
    if campo in produto:
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

        opcao = ler_inteiro("Escolha uma opção: ")

        if opcao == 1:
            cabecalho("Cadastrar Produto")
            nome = ler_texto("Nome do produto:")
            categoria = ler_texto("Categoria: ")
            preco = ler_decimal("Preço: ")
            quantidade = ler_inteiro("Quantidade inicial em estoque:")
            estoque_minimo = ler_inteiro("Estoque mínimo:")

            cadastrar_produto(nome, categoria, preco, quantidade, estoque_minimo)
            mensagem_ok("Produto cadastrado com sucesso!")

        elif opcao == 2:
            listar_produtos()

        elif opcao == 3:
            cabecalho("Buscar Produto")
            codigo = ler_inteiro("Código do produto: ")
            produto = buscar_produto(codigo)
            if produto:
               print (f"Produto Encontrado")
               print (f"Codigo: {produto['codigo']}")
               print (f"Nome: {produto['nome']}")
               print (f"Categoria: {produto['categoria']}")
               print (f"Preco: {produto['preco']:.2f}")
               print (f"Quantidade: {produto['quantidade']}")
               print (f"Estoque Minimo: {produto['estoque_minimo']}")
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
                campo = ler_texto("Qual campo deseja alterar? ")
                if campo not in produto or campo == "codigo":
                    mensagem_erro("Campo invalido.")
                else:
                    if campo in ["preco"]:
                        novo_valor = ler_decimal("Novo preco: ")
                    elif campo in ["quantidade", "estoque_minimo"]:
                        novo_valor = ler_inteiro("Novo valor inteiro: ")
                    else:
                        novo_valor = ler_texto("Novo valor: ")
                    
                    if alterar_produto(codigo, campo, novo_valor):
                        mensagem_ok("Produto alterado com sucesso!")
                    else:
                        mensagem_erro("Erro ao alterar produto.")
                        
        elif opcao == 5:
            cabecalho("Remover Produto")
            codigo = ler_inteiro("Digite o codigo do produto a remover: ")
            if remover_produto(codigo):
                mensagem_ok("Produto removido com sucesso!")
            else:
                mensagem_erro("Produto nao encontrado.")
                
        elif opcao == 0:
            break
        else:
            mensagem_erro("Opcao invalida.")
    
            