# utils.py - funcoes de tela usadas por todos os modulos

def cabecalho(titulo):
    """Imprime o titulo de uma tela no padrao do sistema."""
    print()
    print("=" * 50)
    print(titulo.upper().center(50))
    print("=" * 50)


def mensagem_erro(texto):
    """Imprime uma mensagem de erro no padrao do sistema."""
    print("[ERRO] " + texto)


def mensagem_ok(texto):
    """Imprime uma mensagem de sucesso no padrao do sistema."""
    print("[OK] " + texto)


def pausar():
    """Segura a tela ate o usuario apertar Enter."""
    input("\nPressione Enter para continuar...")


def ler_inteiro(pergunta):
    """Pergunta ate o usuario digitar um numero inteiro valido."""
    while True:
        try:
            return int(input(pergunta))
        except ValueError:
            mensagem_erro("Digite apenas numeros inteiros.")


def ler_decimal(pergunta):
    """Pergunta ate o usuario digitar um numero com virgula valido."""
    while True:
        try:
            return float(input(pergunta).replace(",", "."))
        except ValueError:
            mensagem_erro("Digite um numero. Exemplo: 2,50")


def ler_texto(pergunta):
    """Pergunta ate o usuario digitar algo que nao seja vazio."""
    while True:
        valor = input(pergunta).strip()
        if valor != "":
            return valor
        mensagem_erro("Este campo nao pode ficar vazio.")