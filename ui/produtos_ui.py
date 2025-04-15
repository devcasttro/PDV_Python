from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from models import produtos_model


class TelaProdutos(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("color: white;")
        layout = QVBoxLayout()

        # Formulário
        form_layout = QHBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do produto")

        self.cat_input = QLineEdit()
        self.cat_input.setPlaceholderText("Categoria")

        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText("Preço de venda")

        self.custo_input = QLineEdit()
        self.custo_input.setPlaceholderText("Custo")

        self.estoque_input = QLineEdit()
        self.estoque_input.setPlaceholderText("Estoque inicial")

        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("Código de barras")

        form_layout.addWidget(self.nome_input)
        form_layout.addWidget(self.cat_input)
        form_layout.addWidget(self.preco_input)
        form_layout.addWidget(self.custo_input)
        form_layout.addWidget(self.estoque_input)
        form_layout.addWidget(self.codigo_input)

        layout.addLayout(form_layout)

        # Botões
        botoes_layout = QHBoxLayout()
        self.btn_salvar = QPushButton("Salvar")
        self.btn_limpar = QPushButton("Limpar")
        botoes_layout.addWidget(self.btn_salvar)
        botoes_layout.addWidget(self.btn_limpar)
        layout.addLayout(botoes_layout)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Categoria", "Preço", "Estoque"])
        layout.addWidget(self.tabela)

        self.setLayout(layout)

        # Conexões
        self.btn_salvar.clicked.connect(self.salvar_produto)
        self.btn_limpar.clicked.connect(self.limpar_campos)

        self.carregar_produtos()

    def salvar_produto(self):
        nome = self.nome_input.text()
        categoria = self.cat_input.text()
        preco = self.preco_input.text()
        custo = self.custo_input.text()
        estoque = self.estoque_input.text()
        codigo = self.codigo_input.text()

        if not nome or not preco:
            QMessageBox.warning(self, "Erro", "Preencha ao menos nome e preço.")
            return

        try:
            produtos_model.inserir_produto(nome, categoria, float(preco), float(custo or 0), int(estoque or 0), codigo)
            QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_produtos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")

    def limpar_campos(self):
        self.nome_input.clear()
        self.cat_input.clear()
        self.preco_input.clear()
        self.custo_input.clear()
        self.estoque_input.clear()
        self.codigo_input.clear()

    def carregar_produtos(self):
        self.tabela.setRowCount(0)
        produtos = produtos_model.listar_produtos()
        for row_idx, row_data in enumerate(produtos):
            self.tabela.insertRow(row_idx)
            for col_idx, valor in enumerate(row_data):
                self.tabela.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))
