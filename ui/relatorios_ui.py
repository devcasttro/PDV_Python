from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit
)
from PyQt5.QtCore import QDate
import database
import sqlite3


class TelaRelatorios(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Relatórios de Vendas")
        self.conn = database.conectar()
        self.cursor = self.conn.cursor()

        layout = QVBoxLayout()

        # Filtros
        filtros_layout = QHBoxLayout()

        self.data_inicio = QDateEdit()
        self.data_inicio.setCalendarPopup(True)
        self.data_inicio.setDate(QDate.currentDate().addMonths(-1))

        self.data_fim = QDateEdit()
        self.data_fim.setCalendarPopup(True)
        self.data_fim.setDate(QDate.currentDate())

        self.cliente_combo = QComboBox()
        self.forma_pgto_combo = QComboBox()

        self.carregar_clientes()
        self.carregar_formas_pagamento()

        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.clicked.connect(self.filtrar_vendas)

        filtros_layout.addWidget(QLabel("Data Inicial:"))
        filtros_layout.addWidget(self.data_inicio)
        filtros_layout.addWidget(QLabel("Data Final:"))
        filtros_layout.addWidget(self.data_fim)
        filtros_layout.addWidget(QLabel("Cliente:"))
        filtros_layout.addWidget(self.cliente_combo)
        filtros_layout.addWidget(QLabel("Pagamento:"))
        filtros_layout.addWidget(self.forma_pgto_combo)
        filtros_layout.addWidget(btn_filtrar)

        layout.addLayout(filtros_layout)

        # Tabela de resultados
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels([
            "Data", "Cliente", "Bruto", "Desconto", "Líquido", "Pagamento"
        ])
        layout.addWidget(self.tabela)

        # Totais
        self.label_totais = QLabel("Total Bruto: R$0.00 | Desconto: R$0.00 | Líquido: R$0.00")
        layout.addWidget(self.label_totais)

        self.setLayout(layout)

    def carregar_clientes(self):
        self.cursor.execute("SELECT id, nome FROM clientes WHERE ativo = 1")
        clientes = self.cursor.fetchall()
        self.cliente_combo.addItem("Todos", None)
        for c in clientes:
            self.cliente_combo.addItem(c[1], c[0])

    def carregar_formas_pagamento(self):
        self.cursor.execute("SELECT id, descricao FROM formas_pagamento")
        formas = self.cursor.fetchall()
        self.forma_pgto_combo.addItem("Todas", None)
        for f in formas:
            self.forma_pgto_combo.addItem(f[1], f[0])

    def filtrar_vendas(self):
        data_ini = self.data_inicio.date().toString("yyyy-MM-dd")
        data_fim = self.data_fim.date().toString("yyyy-MM-dd")
        cliente_id = self.cliente_combo.currentData()
        forma_id = self.forma_pgto_combo.currentData()

        query = """
            SELECT v.data_hora, c.nome, v.total_bruto, v.desconto_total_valor, v.total_liquido, f.descricao
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN pagamentos p ON v.id = p.venda_id
            LEFT JOIN formas_pagamento f ON p.forma_pagamento_id = f.id
            WHERE date(v.data_hora) BETWEEN ? AND ?
        """
        params = [data_ini, data_fim]

        if cliente_id:
            query += " AND v.cliente_id = ?"
            params.append(cliente_id)

        if forma_id:
            query += " AND p.forma_pagamento_id = ?"
            params.append(forma_id)

        self.cursor.execute(query, params)
        resultados = self.cursor.fetchall()

        self.tabela.setRowCount(0)
        total_bruto = total_desc = total_liquido = 0

        for row_data in resultados:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            for col, valor in enumerate(row_data):
                self.tabela.setItem(row, col, QTableWidgetItem(str(valor)))
            total_bruto += row_data[2]
            total_desc += row_data[3]
            total_liquido += row_data[4]

        self.label_totais.setText(
            f"Total Bruto: R${total_bruto:.2f} | Desconto: R${total_desc:.2f} | Líquido: R${total_liquido:.2f}"
        )
