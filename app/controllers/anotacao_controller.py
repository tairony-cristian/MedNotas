from PyQt5 import QtWidgets
from models.anotacao import Anotacao
from database import DatabaseConnection
from ui.utils import Utils
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
                anotacao = dialog.get_anotacao()  # Certifique-se de que get_anotacao retorna um dicionário
                # Passa o dicionário diretamente ao método que insere no banco de dados
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
                anotacao['custo'] = Utils.formatar_custo_para_exibicao(anotacao['custo'])  # Converte para exibição
                anotacao['data'] = Utils.formatar_data_para_exibicao(anotacao['data'])  # Converte para dd/mm/yyyy ao exibir
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
                anotacao = self._get_anotacao_from_inputs()
                anotacao['custo'] = Utils.formatar_custo_para_banco(anotacao['custo'])  # Converte para o banco

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

        # Solicita confirmação
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
                QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao excluir Registro: {str(e)}")

    def pesquisar_anotacao(self):
        """ Pesquisa anotações com base no termo fornecido e no critério selecionado. """
        criterio = self.main_window.combo_pesquisa.currentText()

        try:
            # Mapeamento do critério para a busca no banco de dados
            if criterio == "ID":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotações = self.db.buscar_anotacao_por_id(termo_pesquisa)
            elif criterio == "Período de Data":
                # Obtém as datas dos campos QDateEdit no formato 'yyyy-MM-dd'
                data_inicio = self.main_window.date_inicial.date().toString("yyyy-MM-dd")
                data_fim = self.main_window.date_final.date().toString("yyyy-MM-dd")

                # Passa as datas formatadas para a função de busca
                anotações = self.db.buscar_anotacao_por_periodo_data(data_inicio, data_fim)
            elif criterio == "Local":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotações = self.db.buscar_anotacao_por_local(termo_pesquisa)
            elif criterio == "Médico":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotações = self.db.buscar_anotacao_por_medico(termo_pesquisa)
            elif criterio == "Nota Fiscal":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotações = self.db.buscar_anotacao_por_nota_fiscal(termo_pesquisa)
            elif criterio == "Todos os Campos":
                termo_pesquisa = self.main_window.entry_pesquisa.text()
                anotações = self.db.buscar_anotacao(termo_pesquisa)
            else:
                QtWidgets.QMessageBox.warning(self.main_window, "Critério Inválido", "Selecione um critério válido de pesquisa.")
                return

            # Verifica se alguma anotação foi encontrada e atualiza a tabela
            if anotações:
                self._atualizar_tabela(anotações)
            else:
                QtWidgets.QMessageBox.information(self.main_window, "Resultado", "Nenhuma anotação encontrada.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Erro", f"Erro ao pesquisar anotações: {str(e)}")


    def _get_anotacao_from_inputs(self):
        """ Cria uma instância de Anotacao a partir dos campos de entrada. """
        return Anotacao(
            id=None,  # O ID é gerado automaticamente pelo banco de dados
            data=self.main_window.entry_data.text(),
            procedimento=self.main_window.entry_procedimento.text(),
            quant_procedimento=int(self.main_window.entry_quant_procedimento.text()),
            quant_ampola=int(self.main_window.entry_quant_ampola.text()),
            custo=self.main_window.entry_custo.text(),
            local=self.main_window.entry_local.text(),
            medico=self.main_window.entry_medico.text(),
            nota_fiscal=self.main_window.entry_nota_fiscal.text(),
            observacao=self.main_window.entry_observacao.text()
        )

    def _preencher_campos(self, anotacao):
        """ Preenche os campos da interface com os dados da anotação selecionada. """
        self.entry_data.setText(anotacao['data'])
        self.entry_procedimento.setText(anotacao['procedimento'])
        self.entry_quant_procedimento.setValue(anotacao['quant_procedimento'])
        self.entry_quant_ampola.setValue(anotacao['quant_ampola'])
        self.entry_custo.setText(Utils.formatar_custo_para_exibicao(anotacao['custo']))
        self.entry_local.setText(anotacao['local'])
        self.entry_medico.setText(anotacao['medico'])
        self.entry_nota_fiscal.setText(anotacao['nota_fiscal'])
        self.entry_observacao.setText(anotacao['observacao'])

    def _atualizar_lista(self):
        """ Atualiza a lista de anotações exibida na interface. """
        try:
            anotações = self.db.listar_anotacoes()
            self._atualizar_tabela(anotações)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Erro", f"Erro ao atualizar lista de anotações: {str(e)}")

    def _atualizar_tabela(self, anotações):
        """ Atualiza a tabela na interface com os dados das anotações. """
        self.main_window.table.setRowCount(0)
        
        # Verifique se 'anotações' é um dicionário (um único registro) e converta para lista
        if isinstance(anotações, dict):
            anotações = [tuple(anotações.values())]  # Converta o dicionário para uma tupla e coloque em uma lista
        
        # Verifique se 'anotações' é uma lista de dicionários
        elif isinstance(anotações, list) and len(anotações) > 0 and isinstance(anotações[0], dict):
            anotações = [tuple(anotacao.values()) for anotacao in anotações]
        
        # Atualize a tabela com os dados
        for anotacao in anotações:
            row_position = self.main_window.table.rowCount()
            self.main_window.table.insertRow(row_position)
            for i, data in enumerate(anotacao):
                if i == 5:  # coluna de custo é a 6ª (index 5)
                    data = Utils.formatar_custo_para_exibicao(data)
                elif i == 1:  #  coluna de data é a 2ª (index 1)
                    data = Utils.formatar_data_para_exibicao(data)
                
                self.main_window.table.setItem(row_position, i, QtWidgets.QTableWidgetItem(str(data)))