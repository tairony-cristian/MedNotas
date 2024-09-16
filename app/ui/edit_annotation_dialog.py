from PyQt5 import QtWidgets, QtCore
from ui.utils import Utils
from PyQt5.QtCore import QDate, QLocale

class EditAnnotationDialog(QtWidgets.QDialog):
    def __init__(self, parent, anotacao=None):
        super().__init__(parent)
        self.parent = parent
        self.anotacao = anotacao
        self.setWindowTitle("Editar Anotação")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        """ Inicializa a interface do diálogo. """
        layout = QtWidgets.QVBoxLayout()
        self.setFixedSize(450, 680)

        # Campo de data com QDateEdit
        self.entry_data = QtWidgets.QDateEdit(self)
        self.entry_data.setCalendarPopup(True)
        self.entry_data.setDisplayFormat("dd/MM/yyyy")  # Define o formato de exibição
        self.entry_data.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))  # Define o locale

        # Outros campos de entrada
        self.entry_procedimento = QtWidgets.QLineEdit()
        self.entry_quant_procedimento = QtWidgets.QSpinBox()
        self.entry_quant_procedimento.setMaximum(10000)
        self.entry_quant_ampola = QtWidgets.QSpinBox()
        self.entry_quant_ampola.setMaximum(10000)
        
        # Campo de custo com formatação customizada
        self.entry_custo = QtWidgets.QLineEdit()
        self.entry_custo.setPlaceholderText("R$ 0,00")
        self.entry_custo.setAlignment(QtCore.Qt.AlignLeft)  
        self.entry_custo.textChanged.connect(lambda: Utils.atualizar_formatacao_custo(self.entry_custo))

        self.entry_local = QtWidgets.QLineEdit()
        self.entry_medico = QtWidgets.QLineEdit()
        self.entry_nota_fiscal = QtWidgets.QLineEdit()
        self.entry_observacao = QtWidgets.QTextEdit()

        # Adiciona os campos ao layout
        layout.addWidget(QtWidgets.QLabel("Data:"))
        layout.addWidget(self.entry_data)
        layout.addWidget(QtWidgets.QLabel("Procedimento:"))
        layout.addWidget(self.entry_procedimento)
        layout.addWidget(QtWidgets.QLabel("Quantidade de Procedimento:"))
        layout.addWidget(self.entry_quant_procedimento)
        layout.addWidget(QtWidgets.QLabel("Quantidade de Ampola:"))
        layout.addWidget(self.entry_quant_ampola)
        layout.addWidget(QtWidgets.QLabel("Custo:"))
        layout.addWidget(self.entry_custo)
        layout.addWidget(QtWidgets.QLabel("Local:"))
        layout.addWidget(self.entry_local)
        layout.addWidget(QtWidgets.QLabel("Médico:"))
        layout.addWidget(self.entry_medico)
        layout.addWidget(QtWidgets.QLabel("Nota Fiscal:"))
        layout.addWidget(self.entry_nota_fiscal)
        layout.addWidget(QtWidgets.QLabel("Observação:"))
        layout.addWidget(self.entry_observacao)
        
        # Botões
        button_layout = QtWidgets.QHBoxLayout()
        btn_save = QtWidgets.QPushButton("Salvar")
        btn_cancel = QtWidgets.QPushButton("Cancelar")
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)

        # Adiciona os botões ao layout principal
        layout.addLayout(button_layout)

        # Configura os botões
        btn_save.clicked.connect(self.save_changes)
        btn_cancel.clicked.connect(self.reject)

        self.setLayout(layout)

        if self.anotacao:
            self._preencher_campos(self.anotacao)
        else:
            # Se for uma nova anotação, preenche com a data atual
            self.entry_data.setDate(QDate.currentDate())

    def _preencher_campos(self, anotacao):
        data_str = anotacao['data']
        data = Utils.converter_string_para_qdate(data_str, "dd/MM/yyyy")
        self.entry_data.setDate(data)
        self.entry_procedimento.setText(anotacao['procedimento'])
        self.entry_quant_procedimento.setValue(anotacao['quant_procedimento'])
        self.entry_quant_ampola.setValue(anotacao['quant_ampola'])

        custo = anotacao['custo']
        if isinstance(custo, str):
            custo = Utils.formatar_custo_para_banco(custo)
        formatted_custo = Utils.formatar_custo_para_exibicao(custo)
        self.entry_custo.setText(formatted_custo)
        
        self.entry_local.setText(anotacao['local'])
        self.entry_medico.setText(anotacao['medico'])
        self.entry_nota_fiscal.setText(anotacao['nota_fiscal'])
        self.entry_observacao.setText(anotacao['observacao'])

    def save_changes(self):
        """ Salva as alterações feitas nos campos de entrada. """
        if Utils.validar_campos(self):
            self.accept()  # Fecha o diálogo e indica que as alterações foram aceitas

    def get_anotacao(self):
        return {
            'data': Utils.formatar_data_para_banco(self.entry_data.text().strip()),
            'procedimento': self.entry_procedimento.text().strip(),
            'quant_procedimento': self.entry_quant_procedimento.value(),
            'quant_ampola': self.entry_quant_ampola.value(),
            'custo': Utils.formatar_custo_para_banco(self.entry_custo.text().strip()),
            'local': self.entry_local.text().strip(),
            'medico': self.entry_medico.text().strip(),
            'nota_fiscal': self.entry_nota_fiscal.text().strip(),
            'observacao': self.entry_observacao.toPlainText().strip()
        }