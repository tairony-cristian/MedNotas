from PyQt5 import QtWidgets
from ui.utils import Utils

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

        # Campos de entrada
        self.entry_data = QtWidgets.QLineEdit()
        self.entry_procedimento = QtWidgets.QLineEdit()
        self.entry_quant_procedimento = QtWidgets.QSpinBox()
        self.entry_quant_ampola = QtWidgets.QSpinBox()
        self.entry_custo = QtWidgets.QLineEdit()
        self.entry_local = QtWidgets.QLineEdit()
        self.entry_medico = QtWidgets.QLineEdit()
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

    def _preencher_campos(self, anotacao):
        """ Preenche os campos da interface com os dados da anotação selecionada. """
        self.entry_data.setText(Utils.formatar_data(anotacao['data']))
        self.entry_procedimento.setText(anotacao['procedimento'])
        self.entry_quant_procedimento.setValue(anotacao['quant_procedimento'])
        self.entry_quant_ampola.setValue(anotacao['quant_ampola'])
        self.entry_custo.setText(Utils.formatar_custo(anotacao['custo']))
        self.entry_local.setText(anotacao['local'])
        self.entry_medico.setText(anotacao['medico'])
        self.entry_observacao.setText(anotacao['observacao'])

    def save_changes(self):
        """ Salva as alterações feitas nos campos de entrada. """
        if Utils.validar_campos(self.parent):
            updated_anotacao = {
                'data': Utils.formatar_data(self.entry_data.text()),
                'procedimento': self.entry_procedimento.text(),
                'quant_procedimento': self.entry_quant_procedimento.value(),
                'quant_ampola': self.entry_quant_ampola.value(),
                'custo': Utils.formatar_custo(self.entry_custo.text()),
                'local': self.entry_local.text(),
                'medico': self.entry_medico.text(),
                'observacao': self.entry_observacao.toPlainText()
            }
            try:
                db = self.parent.db_connection
                if self.anotacao:
                    db.atualizar_anotacao(self.anotacao['id'], updated_anotacao)
                else:
                    db.adicionar_anotacao(updated_anotacao)
                self.accept()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Erro", f"Erro ao salvar anotação: {e}")
        else:
            QtWidgets.QMessageBox.warning(self, "Validação", "Por favor, preencha todos os campos obrigatórios.")
