import sqlite3
import os

DB_NAME = "pdv.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def inicializar_banco():
    if os.path.exists(DB_NAME):
        return

    conn = conectar()
    cursor = conn.cursor()

    # Produtos
    cursor.execute("""
        CREATE TABLE produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            preco_venda REAL,
            custo REAL,
            estoque INTEGER DEFAULT 0,
            codigo_barras TEXT,
            ativo INTEGER DEFAULT 1
        )
    """)

    # Vendas
    cursor.execute("""
        CREATE TABLE vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            valor_total REAL,
            forma_pagamento TEXT,
            cliente_id INTEGER
        )
    """)

    # Itens da venda
    cursor.execute("""
        CREATE TABLE itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER,
            preco_unitario REAL
        )
    """)

    # Clientes
    cursor.execute("""
        CREATE TABLE clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf_cnpj TEXT,
            telefone TEXT,
            email TEXT,
            ativo INTEGER DEFAULT 1
        )
    """)

    # Fornecedores
    cursor.execute("""
        CREATE TABLE fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            razao_social TEXT,
            cnpj TEXT,
            telefone TEXT,
            email TEXT,
            ativo INTEGER DEFAULT 1
        )
    """)

    # Contas a pagar e receber
    cursor.execute("""
        CREATE TABLE financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT, -- 'pagar' ou 'receber'
            descricao TEXT,
            valor REAL,
            vencimento TEXT,
            pago INTEGER DEFAULT 0,
            data_pagamento TEXT,
            pessoa_id INTEGER,
            pessoa_tipo TEXT -- 'cliente' ou 'fornecedor'
        )
    """)

    conn.commit()
    conn.close()

# Chamada automática ao rodar
if __name__ == "__main__":
    inicializar_banco()
