# main.py - menu principal do SIGEP
# Distribuidora Vale Azul Bebidas Ltda.
#
# Cada modulo e importado dentro de um try: enquanto o arquivo do integrante
# ainda nao estiver na pasta, o modulo fica como None e aparece no menu como
# "(em desenvolvimento)". Quando o arquivo chegar, ele e liberado sozinho,
# sem precisar mexer neste arquivo.

from utils import cabecalho, mensagem_erro, mensagem_ok, pausar, ler_inteiro

try:
    import produtos
except ImportError:
    produtos = None

try:
    import clientes
except ImportError:
    clientes = None

try:
    import estoque
except ImportError:
    estoque = None

try:
    import pedidos
except ImportError:
    pedidos = None

try:
    import fila
except ImportError:
    fila = None

try:
    import relatorios
except ImportError:
    relatorios = None


def situacao(modulo, nome_funcao):
    """Devolve o aviso que aparece ao lado da opcao se o modulo ainda nao chegou."""
    if modulo is None or not hasattr(modulo, nome_funcao):
        return "  (em desenvolvimento)"
    return ""


def exibir_menu():
    """Mostra as opcoes do menu principal na tela."""
    cabecalho("SIGEP - Distribuidora Vale Azul")
    print("1 - Produtos" + situacao(produtos, "menu_produtos"))
    print("2 - Clientes" + situacao(clientes, "menu_clientes"))
    print("3 - Estoque" + situacao(estoque, "menu_estoque"))
    print("4 - Pedidos" + situacao(pedidos, "menu_pedidos"))
    print("5 - Fila de separacao" + situacao(fila, "menu_fila"))
    print("6 - Relatorios" + situacao(relatorios, "menu_relatorios"))
    print("0 - Sair")
    print("-" * 50)


def abrir_submenu(modulo, nome_funcao, nome_modulo):
    """Chama o submenu de um modulo.
    Se o modulo ainda nao foi integrado, ou se der erro dentro dele,
    avisa com mensagem_erro e volta ao menu principal sem fechar o sistema."""
    if modulo is None or not hasattr(modulo, nome_funcao):
        mensagem_erro("Modulo " + nome_modulo + " ainda nao foi integrado.")
        pausar()
        return

    try:
        funcao = getattr(modulo, nome_funcao)
        funcao()
    except (KeyboardInterrupt, EOFError):
        raise
    except Exception as erro:
        mensagem_erro("Falha no modulo " + nome_modulo + ": " + str(erro))
        pausar()


def executar_opcao(opcao):
    """Recebe o numero escolhido e chama o submenu do modulo certo.
    Opcao invalida: avisa com mensagem_erro e volta ao menu."""
    if opcao == 1:
        abrir_submenu(produtos, "menu_produtos", "Produtos")
    elif opcao == 2:
        abrir_submenu(clientes, "menu_clientes", "Clientes")
    elif opcao == 3:
        abrir_submenu(estoque, "menu_estoque", "Estoque")
    elif opcao == 4:
        abrir_submenu(pedidos, "menu_pedidos", "Pedidos")
    elif opcao == 5:
        abrir_submenu(fila, "menu_fila", "Fila de separacao")
    elif opcao == 6:
        abrir_submenu(relatorios, "menu_relatorios", "Relatorios")
    else:
        mensagem_erro("Opcao invalida. Escolha um numero de 0 a 6.")


def main():
    """Laco principal: mostra o menu e le a opcao ate o usuario sair (0)."""
    try:
        while True:
            exibir_menu()
            opcao = ler_inteiro("Escolha uma opcao: ")
            if opcao == 0:
                break
            executar_opcao(opcao)
    except (KeyboardInterrupt, EOFError):
        print()
    mensagem_ok("Sistema encerrado. Ate logo!")


if __name__ == "__main__":
    main()
