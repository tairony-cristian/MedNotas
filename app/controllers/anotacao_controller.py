from ui.utils import Utils
from PyQt5 import QtWidgets
from models.anotacao import Anotacao
from database import DatabaseConnection
from ui.edit_annotation_dialog import EditAnnotationDialog

class AnotacaoController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = DatabaseConnection()
    
    def adicionar_anotacao(self):
        """ Adiciona uma nova anotação ao banco de dados. """
        dialog = EditAnnotationDialog(self.main_window)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                anotacao = dialog.get_anotacao()
                self.db.adicionar_anotacao(anotacao)
                self._atualizar_lista()
                QtWidgets.QMessageBox.information(self.main_window, "Sucesso", "Anotação adicionada com sucesso!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self.main_window, "Erro", f"Erro ao adicionar anotação: {str(e)}")

    def editar_anotacao(self):
        """ Ativa o modo de edição de uma anotação existente. """
        selected_items = self.main_window.table.selectedItems()
        if selected_items:
            id_anotacao = selected_items[0].text()
            anotacao = self.db.buscar_anotacao_por_id(id_anotacao)
            if anotacao:
                anotacao['custo'] = Utils.formatar_custo_para_exibicao(anotacao['custo'])
                anotacao['data'] = Utils.formatar_data_para_exibicao(anotacao['data'])
                dialog = EditAnnotationDialog(self.main_window, anotacao)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    try:
                        updated_anotacao = dialog.get_anotacao()
                        self.db.atualizar_anotacao(id_anotacao, updated_anotacao)
                        self._atualizar_lista()
                        QtWidgets.QMessageBox.information(self.main_window, "Sucesso", "Anotação atualizada com sucesso!")
                    except Exception as e:
                        QtWidgets.QMessageBox.critical(self.main_window, "Erro", f"Erro ao atualizar anotação: {str(e)}")
            else:
                QtWidgets.QMessageBox.warning(self.main_window, "Erro", "Anotação não encontrada.")
        else:
            QtWidgets.QMessageBox.warning(self.main_window, "Nenhum item selecionado", "Por favor, selecione uma anotação para editar.")
      
    def gravar_anotacao(self):
        if Utils.validar_campos(self.main_window):
            try:
                # Abra o diálogo para obter os dados
                dialog = EditAnnotationDialog(self.main_window)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    anotacao = dialog.get_anotacao()

                    if self.main_window.editing:
                        self.db.atualizar_anotacao(self.main_window.editing_id, anotacao)
                        QtWidgets.QMessageBox.information(self.main_window, "Sucesso", "Anotação atualizada com sucesso!")
                    else:
                        self.db.adicionar_anotacao(anotacao)
                        QtWidgets.QMessageBox.information(self.main_window, "Sucesso", "Anotação adicionada com sucesso!")

                    self.main_window.editing = False
                    self.main_window.editing_id = None
                    self._atualizar_lista()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self.main_window, "Erro", f"Erro ao salvar anotação: {str(e)}")

    def deletar_anotacao(self):
        """ Deleta uma anotação selecionada. """
        selected_items = self.main_window.table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self.main_window, "Erro", "Por favor, selecione um registro para deletar.")
            return

        selected_row = selected_items[0].row()
        id_anotacao = self.main_window.table.item(selected_row, 0).text()

        reply = QtWidgets.QMessageBox.question(
            self.main_window, 
            'Confirmar Exclusão', 
            f"Tem certeza de que deseja excluir o registro com ID: {id_anotacao}?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.db.deletar_anotacao(int(id_anotacao))
                self._atualizar_lista()
                QtWidgets.QMessageBox.information(self.main_window, "Sucesso", f"Registro com ID {id_anotacao} excluído com sucesso.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self.main_window, "Erro", f"Erro ao excluir Registro: {str(e)}")

    def pesquisar_anotacao(self):
        criterio = self.main_window.combo_pesquisa.currentText()
        try:
            # Mapeamento do critério para a busca no banco de dados
            if criterio == "ID":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotacoes = self.db.buscar_anotacao_por_id(termo_pesquisa)
            elif criterio == "Período de Data":
                data_inicio = self.main_window.date_inicial.date().toString("yyyy-MM-dd")
                data_fim = self.main_window.date_final.date().toString("yyyy-MM-dd")
                anotacoes = self.db.buscar_anotacao_por_periodo_data(data_inicio, data_fim)
            elif criterio == "Local":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotacoes = self.db.buscar_anotacao_por_local(termo_pesquisa)
            elif criterio == "Médico":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotacoes = self.db.buscar_anotacao_por_medico(termo_pesquisa)
            elif criterio == "Nota Fiscal":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotacoes = self.db.buscar_anotacao_por_nota_fiscal(termo_pesquisa)
            elif criterio == "Todos os Campos":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotacoes = self.db.buscar_anotacao(termo_pesquisa)
            else:
                QtWidgets.QMessageBox.warning(self.main_window, "Critério Inválido", "Selecione um critério válido de pesquisa.")
                return

            if anotacoes:
                self._atualizar_tabela(anotacoes)
            else:
                QtWidgets.QMessageBox.information(self.main_window, "Resultado", "Nenhuma anotação encontrada.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Erro", f"Erro ao pesquisar anotações: {str(e)}")
  
    def _atualizar_lista(self):
        """ Atualiza a lista de anotações exibida na interface. """
        try:
            anotações = self.db.listar_anotacoes()
            self._atualizar_tabela(anotações)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Erro", f"Erro ao atualizar lista de anotações: {str(e)}")

    def _atualizar_tabela(self, anotacoes):
        """ Atualiza a tabela na interface com os dados das anotações. """
        self.main_window.table.setRowCount(0)
        
        # Verifique se 'anotacoes' é um dicionário (um único registro) e converta para lista
        if isinstance(anotacoes, dict):
            anotacoes = [tuple(anotacoes.values())]  # Converta o dicionário para uma tupla e coloque em uma lista
        
        # Verifique se 'anotacoes' é uma lista de dicionários
        elif isinstance(anotacoes, list) and len(anotacoes) > 0 and isinstance(anotacoes[0], dict):
            anotacoes = [tuple(anotacao.values()) for anotacao in anotacoes]
        
        # Atualize a tabela com os dados
        for anotacao in anotacoes:
            row_position = self.main_window.table.rowCount()
            self.main_window.table.insertRow(row_position)
            for i, data in enumerate(anotacao):
                if i == 5:  # coluna de custo é a 6ª (index 5)
                    data = Utils.formatar_custo_para_exibicao(data)
                elif i == 1:  #  coluna de data é a 2ª (index 1)
                    data = Utils.formatar_data_para_exibicao(data)
                
                self.main_window.table.setItem(row_position, i, QtWidgets.QTableWidgetItem(str(data)))