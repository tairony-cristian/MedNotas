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
        # Campos de entrada de dados
        self.entry_data = QtWidgets.QLineEdit(self)
        self.entry_procedimento = QtWidgets.QLineEdit(self)
        self.entry_quant_procedimento = QtWidgets.QLineEdit(self)
        self.entry_quant_ampola = QtWidgets.QLineEdit(self)
        self.entry_custo = QtWidgets.QLineEdit(self)
        self.entry_local = QtWidgets.QLineEdit(self)
        self.entry_medico = QtWidgets.QLineEdit(self)
        self.entry_observacao = QtWidgets.QLineEdit(self)

        # Campo de pesquisa
        self.entry_pesquisa = QtWidgets.QLineEdit(self)
        self.entry_pesquisa.setPlaceholderText("Pesquisar...")

        # Botões
        self.btn_novo = QtWidgets.QPushButton("Novo", self)
        self.btn_editar = QtWidgets.QPushButton("Editar", self)
        self.btn_gravar = QtWidgets.QPushButton("Gravar", self)
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

        # Layout de Entrada de Dados
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Data:", self.entry_data)
        form_layout.addRow("Procedimento:", self.entry_procedimento)
        form_layout.addRow("Quant Procedimento:", self.entry_quant_procedimento)
        form_layout.addRow("Quant Ampola:", self.entry_quant_ampola)
        form_layout.addRow("Custo (R$):", self.entry_custo)
        form_layout.addRow("Local:", self.entry_local)
        form_layout.addRow("Médico:", self.entry_medico)
        form_layout.addRow("Observação:", self.entry_observacao)
        main_layout.addLayout(form_layout)

        # Layout de Botões
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.btn_novo)
        button_layout.addWidget(self.btn_editar)
        button_layout.addWidget(self.btn_gravar)
        button_layout.addWidget(self.btn_apagar)
        main_layout.addLayout(button_layout)

        # Tabela
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def connect_signals(self):
        self.btn_novo.clicked.connect(self.controller.adicionar_anotacao)
        self.btn_editar.clicked.connect(self.controller.editar_anotacao)
        self.btn_gravar.clicked.connect(self.controller.gravar_anotacao)
        self.btn_apagar.clicked.connect(self.controller.deletar_anotacao)
        self.btn_pesquisar.clicked.connect(self.controller.pesquisar_anotacao)