import sqlite3
from database import conectar

def inserir_produto(nome, categoria, preco_venda, custo, estoque, codigo_barras):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, categoria, preco_venda, custo, estoque, codigo_barras)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, categoria, preco_venda, custo, estoque, codigo_barras))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, categoria, preco_venda, estoque FROM produtos WHERE ativo = 1")
    produtos = cursor.fetchall()
    conn.close()
    return produtos
