# dados.py - estruturas de dados compartilhadas do SIGEP
# Distribuidora Vale Azul Bebidas Ltda.
# ATENCAO: nao altere este arquivo sem avisar o grupo.

# Cada produto e um dicionario dentro da lista produtos
produtos = [
    {"codigo": 101, "nome": "Agua Mineral 500ml", "categoria": "Agua",
     "preco": 2.50, "quantidade": 300, "estoque_minimo": 50},
    {"codigo": 102, "nome": "Refrigerante Cola 2L", "categoria": "Refrigerante",
     "preco": 8.90, "quantidade": 120, "estoque_minimo": 40},
    {"codigo": 103, "nome": "Cerveja Pilsen 350ml", "categoria": "Cerveja",
     "preco": 3.75, "quantidade": 30, "estoque_minimo": 60},
    {"codigo": 104, "nome": "Suco de Laranja 1L", "categoria": "Suco",
     "preco": 6.40, "quantidade": 80, "estoque_minimo": 25},
    {"codigo": 105, "nome": "Energetico 250ml", "categoria": "Energetico",
     "preco": 7.20, "quantidade": 15, "estoque_minimo": 30},
]

# Cada cliente e um dicionario dentro da lista clientes
clientes = [
    {"codigo": 1, "nome": "Bar do Ze", "tipo": "Bar",
     "bairro": "Santo Amaro", "telefone": "11 98888-1111"},
    {"codigo": 2, "nome": "Mercado Sao Jorge", "tipo": "Mercado",
     "bairro": "Campo Grande", "telefone": "11 97777-2222"},
    {"codigo": 3, "nome": "Adega Central", "tipo": "Adega",
     "bairro": "Socorro", "telefone": "11 96666-3333"},
]

# Cada pedido guarda o CODIGO do cliente, nao o nome
pedidos = [
    {"numero": 1, "cliente": 1, "status": "aguardando",
     "itens": [{"codigo": 101, "qtd": 20}, {"codigo": 103, "qtd": 10}]},
    {"numero": 2, "cliente": 2, "status": "aguardando",
     "itens": [{"codigo": 102, "qtd": 15}]},
]

# Fila FIFO de separacao: guarda apenas os numeros dos pedidos
fila_separacao = []

# Contadores para gerar codigos novos
proximo_codigo_produto = 106
proximo_codigo_cliente = 4
proximo_numero_pedido = 3