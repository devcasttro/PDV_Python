from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from models import fornecedores_model


class TelaFornecedores(QWidget):
    def __init__(self):
        super().__init__()

        self.fornecedor_id_edicao = None  # usado para edição

        layout = QVBoxLayout()

        # Campos
        self.input_razao = QLineEdit()
        self.input_razao.setPlaceholderText("Razão Social")

        self.input_cnpj = QLineEdit()
        self.input_cnpj.setPlaceholderText("CNPJ")

        self.input_telefone = QLineEdit()
        self.input_telefone.setPlaceholderText("Telefone")

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.input_razao)
        form_layout.addWidget(self.input_cnpj)
        form_layout.addWidget(self.input_telefone)
        form_layout.addWidget(self.input_email)
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
        self.tabela.setHorizontalHeaderLabels(["ID", "Razão Social", "CNPJ", "Telefone", "Email"])
        layout.addWidget(self.tabela)

        self.setLayout(layout)

        # Ações
        self.btn_salvar.clicked.connect(self.salvar)
        self.btn_limpar.clicked.connect(self.limpar)
        self.tabela.cellClicked.connect(self.selecionar)

        self.carregar()

    def salvar(self):
        razao = self.input_razao.text()
        cnpj = self.input_cnpj.text()
        telefone = self.input_telefone.text()
        email = self.input_email.text()

        if not razao or not cnpj:
            QMessageBox.warning(self, "Erro", "Razão Social e CNPJ são obrigatórios.")
            return

        try:
            if self.fornecedor_id_edicao is None:
                fornecedores_model.inserir_fornecedor(razao, cnpj, telefone, email)
                QMessageBox.information(self, "Sucesso", "Fornecedor cadastrado com sucesso.")
            else:
                fornecedores_model.atualizar_fornecedor(self.fornecedor_id_edicao, razao, cnpj, telefone, email)
                QMessageBox.information(self, "Sucesso", "Fornecedor atualizado com sucesso.")

            self.limpar()
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")

    def limpar(self):
        self.fornecedor_id_edicao = None
        self.input_razao.clear()
        self.input_cnpj.clear()
        self.input_telefone.clear()
        self.input_email.clear()
        self.tabela.clearSelection()

    def carregar(self):
        self.tabela.setRowCount(0)
        dados = fornecedores_model.listar_fornecedores()
        for row_idx, row_data in enumerate(dados):
            self.tabela.insertRow(row_idx)
            for col_idx, valor in enumerate(row_data):
                self.tabela.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))

    def selecionar(self, row, column):
        self.fornecedor_id_edicao = int(self.tabela.item(row, 0).text())
        self.input_razao.setText(self.tabela.item(row, 1).text())
        self.input_cnpj.setText(self.tabela.item(row, 2).text())
        self.input_telefone.setText(self.tabela.item(row, 3).text())
        self.input_email.setText(self.tabela.item(row, 4).text())
