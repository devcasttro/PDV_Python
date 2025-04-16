from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QComboBox, QSpinBox
)
from PyQt5.QtCore import Qt
import database


class TelaVendas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tela de Vendas")
        self.setGeometry(100, 100, 800, 600)

        self.conn = database.conectar()
        self.cursor = self.conn.cursor()

        self.carrinho = []

        self.layout = QVBoxLayout()

        # Cliente
        cliente_layout = QHBoxLayout()
        cliente_label = QLabel("Cliente:")
        self.cliente_combo = QComboBox()
        self.carregar_clientes()
        cliente_layout.addWidget(cliente_label)
        cliente_layout.addWidget(self.cliente_combo)
        self.layout.addLayout(cliente_layout)

        # Produto + quantidade
        produto_layout = QHBoxLayout()
        produto_label = QLabel("Produto:")
        self.produto_combo = QComboBox()
        self.carregar_produtos()
        quantidade_label = QLabel("Qtd:")
        self.quantidade_spin = QSpinBox()
        self.quantidade_spin.setMinimum(1)
        btn_add = QPushButton("Adicionar")
        btn_add.clicked.connect(self.adicionar_ao_carrinho)
        produto_layout.addWidget(produto_label)
        produto_layout.addWidget(self.produto_combo)
        produto_layout.addWidget(quantidade_label)
        produto_layout.addWidget(self.quantidade_spin)
        produto_layout.addWidget(btn_add)
        self.layout.addLayout(produto_layout)

        # Tabela carrinho
        self.tabela_carrinho = QTableWidget()
        self.tabela_carrinho.setColumnCount(5)
        self.tabela_carrinho.setHorizontalHeaderLabels(
            ["Produto", "Qtd", "Preço", "Desconto", "Subtotal"]
        )
        self.layout.addWidget(self.tabela_carrinho)

        # Desconto total
        desconto_layout = QHBoxLayout()
        desconto_label = QLabel("Desconto total:")
        self.desconto_input = QLineEdit()
        self.desconto_input.setPlaceholderText("0.00")
        desconto_layout.addWidget(desconto_label)
        desconto_layout.addWidget(self.desconto_input)
        self.layout.addLayout(desconto_layout)

        # Forma de pagamento
        pagamento_layout = QHBoxLayout()
        pagamento_label = QLabel("Forma de Pagamento:")
        self.pagamento_combo = QComboBox()
        self.carregar_formas_pagamento()
        pagamento_layout.addWidget(pagamento_label)
        pagamento_layout.addWidget(self.pagamento_combo)
        self.layout.addLayout(pagamento_layout)

        # Botão finalizar
        btn_finalizar = QPushButton("Finalizar Venda")
        btn_finalizar.clicked.connect(self.finalizar_venda)
        self.layout.addWidget(btn_finalizar)

        self.setLayout(self.layout)

    def carregar_clientes(self):
        self.cursor.execute("SELECT id, nome FROM clientes WHERE ativo = 1")
        clientes = self.cursor.fetchall()
        self.cliente_combo.clear()
        for nome, id in [(c[1], c[0]) for c in clientes]:
            self.cliente_combo.addItem(nome, id)

    def carregar_produtos(self):
        self.cursor.execute("SELECT id, nome, preco_venda FROM produtos WHERE ativo = 1")
        produtos = self.cursor.fetchall()
        self.produto_combo.clear()
        for p in produtos:
            self.produto_combo.addItem(f"{p[1]} - R${p[2]:.2f}", (p[0], p[2]))

    def carregar_formas_pagamento(self):
        self.cursor.execute("SELECT id, descricao FROM formas_pagamento")
        formas = self.cursor.fetchall()
        self.pagamento_combo.clear()
        for f in formas:
            self.pagamento_combo.addItem(f[1], f[0])

    def adicionar_ao_carrinho(self):
        produto_data = self.produto_combo.currentData()
        quantidade = self.quantidade_spin.value()
        produto_id, preco_unitario = produto_data
        nome = self.produto_combo.currentText().split(" - ")[0]
        subtotal = quantidade * preco_unitario
        self.carrinho.append({
            "produto_id": produto_id,
            "nome": nome,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "desconto": 0.0,
            "subtotal": subtotal
        })
        self.atualizar_tabela_carrinho()

    def atualizar_tabela_carrinho(self):
        self.tabela_carrinho.setRowCount(0)
        for item in self.carrinho:
            row = self.tabela_carrinho.rowCount()
            self.tabela_carrinho.insertRow(row)
            self.tabela_carrinho.setItem(row, 0, QTableWidgetItem(item["nome"]))
            self.tabela_carrinho.setItem(row, 1, QTableWidgetItem(str(item["quantidade"])))
            self.tabela_carrinho.setItem(row, 2, QTableWidgetItem(f"R${item['preco_unitario']:.2f}"))
            self.tabela_carrinho.setItem(row, 3, QTableWidgetItem(f"R${item['desconto']:.2f}"))
            self.tabela_carrinho.setItem(row, 4, QTableWidgetItem(f"R${item['subtotal']:.2f}"))

    def finalizar_venda(self):
        if not self.carrinho:
            QMessageBox.warning(self, "Carrinho Vazio", "Adicione produtos antes de finalizar.")
            return

        try:
            cliente_id = self.cliente_combo.currentData()
            forma_pagamento_id = self.pagamento_combo.currentData()
            desconto_total = float(self.desconto_input.text().replace(",", ".") or 0.0)

            total_bruto = sum(i["subtotal"] for i in self.carrinho)
            total_liquido = total_bruto - desconto_total

            self.cursor.execute("""
                INSERT INTO vendas (cliente_id, desconto_total_valor, total_bruto, total_liquido)
                VALUES (?, ?, ?, ?)
            """, (cliente_id, desconto_total, total_bruto, total_liquido))
            venda_id = self.cursor.lastrowid

            for item in self.carrinho:
                self.cursor.execute("""
                    INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, desconto_valor, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    venda_id,
                    item["produto_id"],
                    item["quantidade"],
                    item["preco_unitario"],
                    item["desconto"],
                    item["subtotal"]
                ))

            self.cursor.execute("""
                INSERT INTO pagamentos (venda_id, forma_pagamento_id, valor)
                VALUES (?, ?, ?)
            """, (venda_id, forma_pagamento_id, total_liquido))

            self.conn.commit()
            QMessageBox.information(self, "Venda Finalizada", "Venda registrada com sucesso.")
            self.carrinho.clear()
            self.atualizar_tabela_carrinho()
            self.desconto_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro:\n{e}")
            self.conn.rollback()