from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from models import clientes_model


class TelaClientes(QWidget):
    def __init__(self):
        super().__init__()

        self.cliente_id_edicao = None  # usado para edição

        layout = QVBoxLayout()

        # Campos de entrada
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome completo")

        self.input_cpf = QLineEdit()
        self.input_cpf.setPlaceholderText("CPF ou CNPJ")

        self.input_telefone = QLineEdit()
        self.input_telefone.setPlaceholderText("Telefone")

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.input_nome)
        form_layout.addWidget(self.input_cpf)
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
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "CPF/CNPJ", "Telefone", "Email"])
        layout.addWidget(self.tabela)

        self.setLayout(layout)

        # Ações
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.btn_limpar.clicked.connect(self.limpar)
        self.tabela.cellClicked.connect(self.selecionar_cliente)

        self.carregar_clientes()

    def salvar_cliente(self):
        nome = self.input_nome.text()
        cpf = self.input_cpf.text()
        telefone = self.input_telefone.text()
        email = self.input_email.text()

        if not nome or not cpf:
            QMessageBox.warning(self, "Erro", "Nome e CPF/CNPJ são obrigatórios.")
            return

        try:
            if self.cliente_id_edicao is None:
                clientes_model.inserir_cliente(nome, cpf, telefone, email)
                QMessageBox.information(self, "Sucesso", "Cliente cadastrado com sucesso!")
            else:
                clientes_model.atualizar_cliente(self.cliente_id_edicao, nome, cpf, telefone, email)
                QMessageBox.information(self, "Sucesso", "Cliente atualizado com sucesso!")

            self.limpar()
            self.carregar_clientes()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar cliente:\n{e}")

    def limpar(self):
        self.cliente_id_edicao = None
        self.input_nome.clear()
        self.input_cpf.clear()
        self.input_telefone.clear()
        self.input_email.clear()
        self.tabela.clearSelection()

    def carregar_clientes(self):
        self.tabela.setRowCount(0)
        dados = clientes_model.listar_clientes()
        for row_idx, row_data in enumerate(dados):
            self.tabela.insertRow(row_idx)
            for col_idx, valor in enumerate(row_data):
                self.tabela.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))

    def selecionar_cliente(self, row, column):
        self.cliente_id_edicao = int(self.tabela.item(row, 0).text())
        self.input_nome.setText(self.tabela.item(row, 1).text())
        self.input_cpf.setText(self.tabela.item(row, 2).text())
        self.input_telefone.setText(self.tabela.item(row, 3).text())
        self.input_email.setText(self.tabela.item(row, 4).text())
