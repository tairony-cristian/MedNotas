from PyQt5 import QtWidgets
from models.anotacao import Anotacao
from database import DatabaseConnection
from ui.utils import Utils

class AnotacaoController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = DatabaseConnection()
    
    def adicionar_anotacao(self):
        """ Adiciona uma nova anotação ao banco de dados. """
        if Utils.validar_campos(self.main_window):
            anotacao = self._get_anotacao_from_inputs()
            self.db.adicionar_anotacao(anotacao)
            self._atualizar_lista()

    def editar_anotacao(self):
        """ Ativa o modo de edição de uma anotação existente. """
        selected_items = self.main_window.table.selectedItems()
        if selected_items:
            self.main_window.editing = True
            self.main_window.editing_id = selected_items[0].text()
            anotacao = self.db.buscar_anotacao_por_id(self.main_window.editing_id)
            if anotacao:
                self._preencher_campos(anotacao)

    def gravar_anotacao(self):
        """ Salva as alterações em uma anotação existente ou adiciona uma nova. """
        if Utils.validar_campos(self.main_window):
            if self.main_window.editing:
                anotacao = self._get_anotacao_from_inputs()
                self.db.atualizar_anotacao(self.main_window.editing_id, anotacao)
            else:
                self.adicionar_anotacao()
            self.main_window.editing = False
            self.main_window.editing_id = None
            self._atualizar_lista()

    def deletar_anotacao(self):
        """ Deleta uma anotação selecionada. """
        selected_items = self.main_window.table.selectedItems()
        if selected_items:
            id_anotacao = selected_items[0].text()
            self.db.deletar_anotacao(id_anotacao)
            self._atualizar_lista()

    def pesquisar_anotacao(self):
        """ Pesquisa anotações com base no termo fornecido. """
        termo_pesquisa = self.main_window.entry_pesquisa.text()
        anotações = self.db.buscar_anotacao(termo_pesquisa)
        self._atualizar_tabela(anotações)

    def _get_anotacao_from_inputs(self):
        """ Cria uma instância de Anotacao a partir dos campos de entrada. """
        return Anotacao(
            id=None,  # O ID é gerado automaticamente pelo banco de dados
            data=Utils.formatar_data(self.main_window.entry_data.text()),
            procedimento=self.main_window.entry_procedimento.text(),
            quant_procedimento=int(self.main_window.entry_quant_procedimento.text()),
            quant_ampola=int(self.main_window.entry_quant_ampola.text()),
            custo=Utils.formatar_custo(self.main_window.entry_custo.text()),
            local=self.main_window.entry_local.text(),
            medico=self.main_window.entry_medico.text(),
            observacao=self.main_window.entry_observacao.text()
        )

    def _preencher_campos(self, anotacao):
        """ Preenche os campos da interface com os dados da anotação selecionada. """
        self.main_window.entry_data.setText(anotacao[1])
        self.main_window.entry_procedimento.setText(anotacao[2])
        self.main_window.entry_quant_procedimento.setText(str(anotacao[3]))
        self.main_window.entry_quant_ampola.setText(str(anotacao[4]))
        self.main_window.entry_custo.setText(Utils.formatar_custo(str(anotacao[5])))
        self.main_window.entry_local.setText(anotacao[6])
        self.main_window.entry_medico.setText(anotacao[7])
        self.main_window.entry_observacao.setText(anotacao[8])

    def _atualizar_lista(self):
        """ Atualiza a lista de anotações exibida na interface. """
        anotações = self.db.listar_anotacoes()
        self._atualizar_tabela(anotações)

    def _atualizar_tabela(self, anotações):
        """ Atualiza a tabela na interface com as anotações fornecidas. """
        table = self.main_window.table
        table.setRowCount(0)
        for anotacao in anotações:
            row = table.rowCount()
            table.insertRow(row)
            for column, data in enumerate(anotacao):
                item = QtWidgets.QTableWidgetItem(str(data))
                table.setItem(row, column, item)
