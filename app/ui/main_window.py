from PyQt5 import QtWidgets
from controllers.anotacao_controller import AnotacaoController

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.controller = AnotacaoController(self)
        self.editing = False
        self.editing_id = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MedNotas")
        self.setGeometry(100, 100, 1200, 600)
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.controller._atualizar_lista()

    def create_widgets(self):

        # Campo de pesquisa
        self.entry_pesquisa = QtWidgets.QLineEdit(self)
        self.entry_pesquisa.setPlaceholderText("Pesquisar...")

        # Botões
        self.btn_novo = QtWidgets.QPushButton("Novo", self)
        self.btn_editar = QtWidgets.QPushButton("Editar", self)
        self.btn_apagar = QtWidgets.QPushButton("Apagar", self)
        self.btn_pesquisar = QtWidgets.QPushButton("Pesquisar", self)

        # Tabela
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID", "Data", "Procedimento", "Quant. Procedimento", "Quant. Ampola", "Custo", "Local", "Médico", "Observação"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Layout de Pesquisa
        pesquisa_layout = QtWidgets.QHBoxLayout()
        pesquisa_layout.addWidget(self.entry_pesquisa)
        pesquisa_layout.addWidget(self.btn_pesquisar)
        main_layout.addLayout(pesquisa_layout)

        # Tabela
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # Layout de Botões
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.btn_novo)
        button_layout.addWidget(self.btn_editar)
        button_layout.addWidget(self.btn_apagar)
        main_layout.addLayout(button_layout)

    def connect_signals(self):
        self.btn_novo.clicked.connect(self.controller.adicionar_anotacao)
        self.btn_editar.clicked.connect(self.controller.editar_anotacao)
        self.btn_apagar.clicked.connect(self.controller.deletar_anotacao)
        self.btn_pesquisar.clicked.connect(self.controller.pesquisar_anotacao)