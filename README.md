# projeto-avc---Logica

**SIGEP — Sistema de Gestão de Estoque e Pedidos**
Distribuidora Vale Azul Bebidas Ltda. · Projeto AVC de Lógica de Programação · Grupo de 7

Sistema em Python (só biblioteca padrão, Python 3.8 ou superior) com menu no terminal para
cadastrar produtos e clientes, controlar o estoque, montar pedidos, organizar a fila FIFO de
separação e emitir relatórios.

## Como rodar

- **PyCharm:** clique com o botão direito em `main.py` → **Run** (ou `Shift + F10`).
- **Terminal:** `python main.py`

O `main.py` roda desde o primeiro dia: módulos que ainda não estão na pasta aparecem no menu
como `(em desenvolvimento)`. Quando o arquivo de um integrante chega na pasta, a opção é
liberada sozinha — não é preciso editar o `main.py`.

## Arquivos

| Nº | Arquivo         | Responsabilidade                                   |
|----|-----------------|----------------------------------------------------|
| —  | `dados.py`      | Listas compartilhadas (produtos, clientes, pedidos, fila) |
| —  | `utils.py`      | Funções de tela e leitura de dados com tratamento de erro |
| 1  | `main.py`       | Menu principal e integração dos módulos            |
| 2  | `estoque.py`    | Entrada, saída e alerta de estoque mínimo          |
| 3  | `pedidos.py`    | Cadastro e manutenção de pedidos                   |
| 4  | `relatorios.py` | Relatórios gerenciais (só lê os dados)             |
| 5  | `fila.py`       | Fila FIFO de separação de pedidos                  |
| 6  | `produtos.py`   | Cadastro de produtos (CRUD)                        |
| 7  | `clientes.py`   | Cadastro de clientes (CRUD)                        |

Cada módulo precisa ter a função de submenu que o `main.py` chama:
`menu_produtos()`, `menu_clientes()`, `menu_estoque()`, `menu_pedidos()`, `menu_fila()` e
`menu_relatorios()`.

## Diagrama de blocos

```
                         +-------------------+
                         |      main.py      |
                         |  menu principal   |
                         +---------+---------+
                                   |
     +-----------+-----------+-----+-----+-----------+-------------+
     |           |           |           |           |             |
 1 Produtos  2 Clientes  3 Estoque   4 Pedidos    5 Fila     6 Relatorios
 produtos.py clientes.py estoque.py  pedidos.py   fila.py    relatorios.py
     |           |           |           |           |             |
     +-----------+-----------+-----+-----+-----------+-------------+
                                   |
                 +-----------------+-----------------+
                 |                                   |
        +--------+--------+                 +--------+--------+
        |    dados.py     |                 |    utils.py     |
        | listas e        |                 | telas e leitura |
        | contadores      |                 | de dados        |
        +-----------------+                 +-----------------+
```

Fluxo do `main.py`: mostra o menu → lê a opção com `ler_inteiro()` → chama o submenu do
módulo escolhido → volta ao menu → repete até o usuário digitar `0`.
