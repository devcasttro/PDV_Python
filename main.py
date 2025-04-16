import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDateTime, QTimer
import database

from ui.produtos_ui import TelaProdutos
from ui.clientes_ui import TelaClientes
from ui.fornecedores_ui import TelaFornecedores
from ui.vendas_ui import TelaVendas
from ui.relatorios_ui import TelaRelatorios
from themes import tema_claro, tema_escuro


class MenuLateral(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.btn_vendas = self.criar_botao("Vendas")
        self.btn_produtos = self.criar_botao("Produtos")
        self.btn_estoque = self.criar_botao("Estoque")
        self.btn_clientes = self.criar_botao("Clientes")
        self.btn_fornecedores = self.criar_botao("Fornecedores")
        self.btn_financeiro = self.criar_botao("Financeiro")
        self.btn_relatorios = self.criar_botao("Relatórios")
        self.btn_sair = self.criar_botao("Sair")

        for btn in [
            self.btn_vendas, self.btn_produtos, self.btn_estoque,
            self.btn_clientes, self.btn_fornecedores,
            self.btn_financeiro, self.btn_relatorios, self.btn_sair
        ]:
            layout.addWidget(btn)

        layout.addStretch()
        self.setLayout(layout)

    def criar_botao(self, texto):
        btn = QPushButton(f"  {texto}")
        btn.setFont(QFont("Segoe UI", 10))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333;
                border-radius: 8px;
            }
        """)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return btn


class TelaSimples(QWidget):
    def __init__(self, titulo):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(titulo)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Segoe UI", 20))
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema PDV")
        self.setGeometry(100, 100, 1100, 650)

        self.tema_atual = "escuro"

        self.menu_lateral = MenuLateral()
        self.stack = QStackedWidget()

        self.telas = {
            "Vendas": TelaVendas(),
            "Produtos": TelaProdutos(),
            "Estoque": TelaSimples("Tela de Estoque"),
            "Clientes": TelaClientes(),
            "Fornecedores": TelaFornecedores(),
            "Financeiro": TelaSimples("Tela Financeira"),
            "Relatórios": TelaRelatorios()
        }

        for tela in self.telas.values():
            self.stack.addWidget(tela)

        self.label_datahora = QLabel()
        self.label_datahora.setAlignment(Qt.AlignRight)
        self.label_datahora.setFont(QFont("Segoe UI", 10))

        self.btn_tema = QPushButton("🌙")
        self.btn_tema.setFixedSize(30, 30)
        self.btn_tema.setStyleSheet("border: none;")
        self.btn_tema.clicked.connect(self.alternar_tema)

        self.atualizar_datahora()
        timer = QTimer(self)
        timer.timeout.connect(self.atualizar_datahora)
        timer.start(1000)

        cabecalho = QHBoxLayout()
        titulo = QLabel("  🧾  Sistema PDV")
        titulo.setFont(QFont("Segoe UI", 12, QFont.Bold))
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.label_datahora)
        cabecalho.addWidget(self.btn_tema)

        cabecalho_widget = QWidget()
        cabecalho_widget.setLayout(cabecalho)

        layout_principal = QVBoxLayout()
        layout_conteudo = QHBoxLayout()
        layout_conteudo.addWidget(self.menu_lateral)
        layout_conteudo.addWidget(self.stack)

        layout_principal.addWidget(cabecalho_widget)
        layout_principal.addLayout(layout_conteudo)

        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)

        # Conectar botões
        self.menu_lateral.btn_vendas.clicked.connect(lambda: self.stack.setCurrentWidget(self.telas["Vendas"]))
        self.menu_lateral.btn_produtos.clicked.connect(lambda: self.stack.setCurrentWidget(self.telas["Produtos"]))
        self.menu_lateral.btn_estoque.clicked.connect(lambda: self.stack.setCurrentWidget(self.telas["Estoque"]))
        self.menu_lateral.btn_clientes.clicked.connect(lambda: self.stack.setCurrentWidget(self.telas["Clientes"]))
        self.menu_lateral.btn_fornecedores.clicked.connect(lambda: self.stack.setCurrentWidget(self.telas["Fornecedores"]))
        self.menu_lateral.btn_financeiro.clicked.connect(lambda: self.stack.setCurrentWidget(self.telas["Financeiro"]))
        self.menu_lateral.btn_relatorios.clicked.connect(lambda: self.stack.setCurrentWidget(self.telas["Relatórios"]))
        self.menu_lateral.btn_sair.clicked.connect(self.close)

        self.setStyleSheet(tema_escuro())

    def atualizar_datahora(self):
        agora = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        self.label_datahora.setText(agora)

    def alternar_tema(self):
        if self.tema_atual == "escuro":
            self.tema_atual = "claro"
            self.setStyleSheet(tema_claro())
            self.btn_tema.setText("☀️")
        else:
            self.tema_atual = "escuro"
            self.setStyleSheet(tema_escuro())
            self.btn_tema.setText("🌙")


if __name__ == "__main__":
    database.criar_tabelas()
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec_())
