import sqlite3
from database import conectar

def inserir_cliente(nome, cpf_cnpj, telefone, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, cpf_cnpj, telefone, email)
        VALUES (?, ?, ?, ?)
    """, (nome, cpf_cnpj, telefone, email))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, cpf_cnpj, telefone, email
        FROM clientes
        WHERE ativo = 1
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_cliente(id, nome, cpf_cnpj, telefone, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes SET
            nome = ?, cpf_cnpj = ?, telefone = ?, email = ?
        WHERE id = ?
    """, (nome, cpf_cnpj, telefone, email, id))
    conn.commit()
    conn.close()
