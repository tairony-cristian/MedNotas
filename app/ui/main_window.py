from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets, QtCore, QtGui
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

        self.setWindowIcon(QtGui.QIcon('C:/projeto_python/MedNotas/app/resources/mednotas.ico')) # Definir o ícone da janela

        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.controller._atualizar_lista()

    def create_widgets(self):

        # Configure o locale para Português
        locale = QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil)
     
        # Campo de pesquisa
        self.combo_pesquisa = QtWidgets.QComboBox(self)
        self.combo_pesquisa.addItems(["ID", "Período de Data", "Local", "Médico", "Nota Fiscal", "Todos os Campos"])

        self.entry_pesquisa = QtWidgets.QLineEdit(self)
        self.entry_pesquisa.setPlaceholderText("Pesquisar...")

        self.date_inicial = QtWidgets.QDateEdit(self)
        self.date_inicial.setCalendarPopup(True)
        self.date_inicial.setDisplayFormat("dd/MM/yyyy")  # Define o formato de exibição
        self.date_inicial.setLocale(locale)  # Ajusta o locale
        self.date_inicial.setDate(QDate.currentDate())  # Define a data atual como padrão
        
        self.date_final = QtWidgets.QDateEdit(self)
        self.date_final.setCalendarPopup(True)
        self.date_final.setDisplayFormat("dd/MM/yyyy")  # Define o formato de exibição
        self.date_final.setLocale(locale)  # Ajusta o locale
        self.date_final.setDate(QDate.currentDate())  # Define a data atual como padrão


        self.label_data_inicial = QtWidgets.QLabel("Data Inicial:", self)
        self.label_data_final = QtWidgets.QLabel("Data Final:", self)

        self.date_inicial.hide()
        self.date_final.hide()
        self.label_data_inicial.hide()
        self.label_data_final.hide()

        # Botões
        self.btn_novo = QtWidgets.QPushButton("Novo", self)
        self.btn_editar = QtWidgets.QPushButton("Editar", self)
        self.btn_apagar = QtWidgets.QPushButton("Apagar", self)
        self.btn_pesquisar = QtWidgets.QPushButton("Pesquisar", self)

        # Tabela
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["ID", "Data", "Procedimento", "Quant. Procedimento", "Quant. Ampola", "Custo", "Local", "Médico", "Nota Fiscal", "Observação"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Layout de Pesquisa
        pesquisa_layout = QtWidgets.QHBoxLayout()
        pesquisa_layout.addWidget(self.entry_pesquisa)
        pesquisa_layout.addWidget(self.label_data_inicial)
        pesquisa_layout.addWidget(self.date_inicial)
        pesquisa_layout.addWidget(self.label_data_final)
        pesquisa_layout.addWidget(self.date_final)
        pesquisa_layout.addWidget(self.combo_pesquisa)
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
        self.combo_pesquisa.currentIndexChanged.connect(self.update_search_fields)
        self.entry_pesquisa.returnPressed.connect(self.controller.pesquisar_anotacao)

    def update_search_fields(self):
        """ Atualiza os campos de entrada conforme a seleção no combobox. """
        selected_option = self.combo_pesquisa.currentText()

        # Reseta os campos de pesquisa
        self.entry_pesquisa.clear()
        self.date_inicial.hide()
        self.date_final.hide()
        self.label_data_inicial.hide()
        self.label_data_final.hide()
        self.entry_pesquisa.show()

        if selected_option == "Período de Data":
            self.entry_pesquisa.hide()
            self.label_data_inicial.show()
            self.date_inicial.show()
            self.label_data_final.show()
            self.date_final.show()
