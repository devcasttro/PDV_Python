import sqlite3

def conectar():
    return sqlite3.connect("pdv.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de Vendas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            desconto_total_valor REAL DEFAULT 0.0,
            desconto_total_percentual REAL DEFAULT 0.0,
            total_bruto REAL NOT NULL,
            total_liquido REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );
    """)

    # Tabela de Itens da Venda
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            desconto_valor REAL DEFAULT 0.0,
            desconto_percentual REAL DEFAULT 0.0,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
    """)

    # Tabela de Formas de Pagamento
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS formas_pagamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL UNIQUE
        );
    """)

    # Inserir formas de pagamento padrão
    formas_pagamento = [
        ('Dinheiro',),
        ('Cartão de Crédito',),
        ('Cartão de Débito',),
        ('PIX',),
        ('Boleto',),
        ('Transferência Bancária',),
        ('Cheque',),
        ('Outros',)
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO formas_pagamento (descricao) VALUES (?);
    """, formas_pagamento)

    # Tabela de Pagamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            forma_pagamento_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id),
            FOREIGN KEY (forma_pagamento_id) REFERENCES formas_pagamento(id)
        );
    """)

    conn.commit()
    conn.close()
