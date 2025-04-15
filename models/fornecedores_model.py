import sqlite3
from database import conectar

def inserir_fornecedor(razao_social, cnpj, telefone, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fornecedores (razao_social, cnpj, telefone, email)
        VALUES (?, ?, ?, ?)
    """, (razao_social, cnpj, telefone, email))
    conn.commit()
    conn.close()

def listar_fornecedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, razao_social, cnpj, telefone, email
        FROM fornecedores
        WHERE ativo = 1
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_fornecedor(id, razao_social, cnpj, telefone, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE fornecedores SET
            razao_social = ?, cnpj = ?, telefone = ?, email = ?
        WHERE id = ?
    """, (razao_social, cnpj, telefone, email, id))
    conn.commit()
    conn.close()
