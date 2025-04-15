from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from models import produtos_model


class TelaProdutos(QWidget):
    def __init__(self):
        super().__init__()

        self.produto_id_edicao = None  # None = novo / ID = edição

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

        # Eventos
        self.btn_salvar.clicked.connect(self.salvar_produto)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.tabela.cellClicked.connect(self.selecionar_produto)

        self.carregar_produtos()

    def salvar_produto(self):
        nome = self.nome_input.text().strip()
        categoria = self.cat_input.text()
        preco = self.preco_input.text().replace(",", ".").strip()
        custo = self.custo_input.text().replace(",", ".").strip()
        estoque = self.estoque_input.text()
        codigo = self.codigo_input.text()

        if not nome:
            QMessageBox.warning(self, "Erro", "O nome do produto é obrigatório.")
            return

        if not preco:
            QMessageBox.warning(self, "Erro", "O preço de venda é obrigatório.")
            return

        try:
            preco = float(preco)
            custo = float(custo) if custo else 0.0
            estoque = int(estoque) if estoque else 0
        except ValueError:
            QMessageBox.critical(self, "Erro", "Preço, custo e estoque devem ser números válidos.")
            return

        try:
            if self.produto_id_edicao is None:
                produtos_model.inserir_produto(nome, categoria, preco, custo, estoque, codigo)
                QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso.")
            else:
                produtos_model.atualizar_produto(self.produto_id_edicao, nome, categoria, preco, custo, estoque, codigo)
                QMessageBox.information(self, "Sucesso", "Produto atualizado com sucesso.")

            self.limpar_campos()
            self.carregar_produtos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar produto:\n{e}")

    def limpar_campos(self):
        self.produto_id_edicao = None
        self.nome_input.clear()
        self.cat_input.clear()
        self.preco_input.clear()
        self.custo_input.clear()
        self.estoque_input.clear()
        self.codigo_input.clear()
        self.tabela.clearSelection()

    def carregar_produtos(self):
        self.tabela.setRowCount(0)
        produtos = produtos_model.listar_produtos()
        for row_idx, row_data in enumerate(produtos):
            self.tabela.insertRow(row_idx)
            for col_idx, valor in enumerate(row_data):
                self.tabela.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))

    def selecionar_produto(self, row, column):
        self.produto_id_edicao = int(self.tabela.item(row, 0).text())
        self.nome_input.setText(self.tabela.item(row, 1).text())
        self.cat_input.setText(self.tabela.item(row, 2).text())
        self.preco_input.setText(self.tabela.item(row, 3).text())
        self.estoque_input.setText(self.tabela.item(row, 4).text())

        dados_completos = produtos_model.buscar_produto_por_id(self.produto_id_edicao)
        if dados_completos:
            _, _, _, _, custo, _, codigo = dados_completos
            self.custo_input.setText(str(custo))
            self.codigo_input.setText(str(codigo))
