from PyQt5 import QtWidgets
from app.ui.utils import formatar_data, formatar_custo
from app.models.anotacao import Anotacao
from app.controllers.anotacao_controller import AnotacaoController

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.controller = AnotacaoController()
        self.editing = False
        self.editing_id = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MedNotas")
        self.setGeometry(100, 100, 1200, 600)
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.atualizar_lista()

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
        self.btn_novo.clicked.connect(self.adicionar_anotacao)
        self.btn_editar.clicked.connect(self.editar_anotacao)
        self.btn_gravar.clicked.connect(self.gravar_anotacao)
        self.btn_apagar.clicked.connect(self.deletar_anotacao)
        self.btn_pesquisar.clicked.connect(self.pesquisar_anotacao)
        

    def adicionar_anotacao(self):
        if not self.validar_campos():
            return
        try:
            # Coleta os dados dos campos de entrada
            data = formatar_data(self.entry_data.text())
            procedimento = self.entry_procedimento.text()
            quant_procedimento = self.entry_quant_procedimento.text()
            quant_ampola = self.entry_quant_ampola.text()
            custo = formatar_custo(self.entry_custo.text())
            local = self.entry_local.text()
            medico = self.entry_medico.text()
            observacao = self.entry_observacao.text()

            # Cria o objeto Anotacao com os dados coletados
            anotacao = Anotacao(
            data=data,
            procedimento=procedimento,
            quant_procedimento=quant_procedimento,
            quant_ampola=quant_ampola,
            custo=custo,
            local=local,
            medico=medico,
            observacao=observacao
        )
            # Chama o método do controlador para adicionar a anotação
            self.controller.adicionar_anotacao(anotacao)

            QtWidgets.QMessageBox.information(self, "Sucesso", "Anotação adicionada com sucesso")
            self.limpar_campos()
            self.atualizar_lista()
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Erro de Validação", str(e))

    def editar_anotacao(self):
        try:
            selected_item = self.table.currentRow()
            selected_id = self.table.item(selected_item, 0).text()
            
            resposta = QtWidgets.QMessageBox.question(self, "Editar Anotação", f"Deseja editar o Registro {selected_id}?", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            
            if resposta == QtWidgets.QMessageBox.Ok:
                self.entry_data.setText(self.table.item(selected_item, 1).text())
                self.entry_procedimento.setText(self.table.item(selected_item, 2).text())
                self.entry_quant_procedimento.setText(self.table.item(selected_item, 3).text())
                self.entry_quant_ampola.setText(self.table.item(selected_item, 4).text())
                self.entry_custo.setText(self.table.item(selected_item, 5).text())
                self.entry_local.setText(self.table.item(selected_item, 6).text())
                self.entry_medico.setText(self.table.item(selected_item, 7).text())
                self.entry_observacao.setText(self.table.item(selected_item, 8).text())
                self.editing = True
                self.editing_id = selected_id
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Por favor, selecione uma anotação para editar")

    def gravar_anotacao(self):
        if not self.editing_id:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Por favor, selecione uma anotação para atualizar")
            return

        # Verificação e formatação dos dados
        try:
            data = formatar_data(self.entry_data.text())
            procedimento = self.entry_procedimento.text()
            quant_procedimento = self.entry_quant_procedimento.text()
            quant_ampola = self.entry_quant_ampola.text()
            custo = formatar_custo(self.entry_custo.text())
            observacao = self.entry_observacao.text()
            local = self.entry_local.text()
            medico = self.entry_medico.text()

            if not data or not procedimento or not quant_procedimento or not quant_ampola or not local:
                raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")
            
            # Cria o objeto Anotacao com os dados coletados
            anotacao = Anotacao(
            data=data,
            procedimento=procedimento,
            quant_procedimento=quant_procedimento,
            quant_ampola=quant_ampola,
            custo=custo,
            local=local,
            medico=medico,
            observacao=observacao
        )

            # Chama o método do controlador para atualizar a anotação
            self.controller.atualizar_anotacao(
                self.editing_id,  # Inclua o ID da anotação a ser atualizada
                anotacao)

            QtWidgets.QMessageBox.information(self, "Sucesso", "Anotação atualizada com sucesso")
            self.limpar_campos()
            self.atualizar_lista()

        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Erro de Validação", str(e))


    def deletar_anotacao(self):
        # Verifica se há uma anotação selecionada
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            id_anotacao = self.table.item(row, 0).text()

            # Chama o método do controlador para deletar a anotação
            self.controller.deletar_anotacao(id_anotacao)

            # Atualiza a lista na tabela
            self.atualizar_lista()
        else:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhuma anotação selecionada para deletar.")

    def pesquisar_anotacao(self):
        termo_pesquisa = self.entry_pesquisa.text()
        resultados = self.controller.buscar_anotacao(termo_pesquisa)

        # Atualiza a tabela com os resultados da pesquisa
        self.table.setRowCount(0)
        for anotacao in resultados:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, value in enumerate(anotacao):
                self.table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(value)))

    def atualizar_lista(self):
        # Atualiza a tabela com todas as anotações
        self.table.setRowCount(0)
        anotacoes = self.controller.listar_anotacoes()
        for anotacao in anotacoes:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, value in enumerate(anotacao):
                self.table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(value)))

    def validar_campos(self):
        data = self.entry_data.text().strip()
        procedimento = self.entry_procedimento.text().strip()
        quant_procedimento = self.entry_quant_procedimento.text().strip()
        quant_ampola = self.entry_quant_ampola.text().strip()
        local = self.entry_local.text().strip()

        if not data:
            QtWidgets.QMessageBox.warning(self, "Validação", "O campo Data não pode estar vazio.")
            return False
        if not procedimento:
            QtWidgets.QMessageBox.warning(self, "Validação", "O campo Procedimento não pode estar vazio.")
            return False
        if not quant_procedimento or not quant_procedimento.isdigit():
            QtWidgets.QMessageBox.warning(self, "Validação", "O campo Quantidade de Procedimento deve conter um valor numérico válido.")
            return False

        if not quant_ampola or not quant_ampola.isdigit():
            QtWidgets.QMessageBox.warning(self, "Validação", "O campo Quantidade de Ampola deve conter um valor numérico válido.")
            return False
        if not local:
            QtWidgets.QMessageBox.warning(self, "Validação", "O campo Local não pode estar vazio.")
            return False

        return True
    
    def limpar_campos(self):
        self.entry_data.clear()
        self.entry_procedimento.clear()
        self.entry_quant_procedimento.clear()
        self.entry_quant_ampola.clear()
        self.entry_custo.clear()
        self.entry_local.clear()
        self.entry_medico.clear()
        self.entry_observacao.clear()

