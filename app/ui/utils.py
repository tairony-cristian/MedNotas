from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
import re

class Utils:

    @staticmethod
    def converter_string_para_qdate(data_str, formato="dd/MM/yyyy"):
        """Converte uma string de data no formato especificado para QDate."""
        data = QDate.fromString(data_str, formato)
        if data.isValid():
            return data
        else:
            return QDate.currentDate()  # Retorna a data atual como fallback
    
    @staticmethod
    def formatar_data_para_exibicao(data):
        """Converte a data de yyyy/mm/dd ou yyyy-mm-dd para dd/mm/yyyy."""
        if '-' in data:
            parts = data.split('-')
        elif '/' in data:
            parts = data.split('/')
        else:
            raise ValueError("Formato de data inválido. Use o formato yyyy-mm-dd ou yyyy/mm/dd.")

        if len(parts) == 3:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
        else:
            raise ValueError("Formato de data inválido. Use o formato yyyy-mm-dd ou yyyy/mm/dd.")

    @staticmethod   
    def formatar_data_para_banco(data):
        """Formata a data de dd/mm/yyyy para yyyy-mm-dd para salvar no banco de dados."""
        if '/' in data:
            partes = data.split('/')
            # Converte a data para o formato yyyy-mm-dd
            return f'{partes[2]}-{partes[1]}-{partes[0]}'
        else:
            raise ValueError("Formato de data inválido. Use o formato dd/mm/yyyy.")

    @staticmethod
    def formatar_custo_para_banco(custo):
        """Formata o custo para salvar no banco de dados como float."""
        if isinstance(custo, float):
            return custo
        elif isinstance(custo, str):
            try:
                # Remove 'R$', espaços e outros caracteres não numéricos
                custo = re.sub(r'[^\d,]', '', custo)
                
                # Substituir a vírgula por ponto para conversão para float
                custo = custo.replace(',', '.')
                return float(custo)
            except ValueError:
                raise ValueError("Custo inválido. Certifique-se de usar um número válido no formato R$ 1.234,56.")
        else:
            raise ValueError("Custo deve ser uma string ou float.")

    @staticmethod
    def formatar_custo_para_exibicao(custo):
        """Formata o custo para exibição no padrão monetário brasileiro."""
        if isinstance(custo, float):
            # Formata para exibição no padrão R$ 1.234,56
            return f"R$ {custo:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
        raise ValueError("Custo deve ser um valor float.")

    @staticmethod
    def converter_string_para_float(custo_str):
        """Converte uma string de custo para float."""
        if isinstance(custo_str, str):
            try:
                # Remove 'R$', espaços e substitui vírgulas por pontos
                custo = re.sub(r'[^\d,]', '', custo_str).replace(',', '.')
                return float(custo)
            except ValueError:
                raise ValueError("Custo inválido. Certifique-se de usar um número válido no formato R$ 1.234,56.")
        raise ValueError("Custo deve ser uma string.")

    @staticmethod
    def validar_campos(dialog):
        """Valida se todos os campos obrigatórios estão preenchidos no diálogo fornecido."""
        try:
            campos_obrigatorios = {
                "Data": dialog.entry_data,
                "Procedimento": dialog.entry_procedimento,
                "Quantidade de Procedimento": dialog.entry_quant_procedimento,
                "Quantidade de Ampola": dialog.entry_quant_ampola,
                "Custo": dialog.entry_custo,  # Verificar valor diretamente do QDoubleSpinBox
                "Local": dialog.entry_local,
                "Médico": dialog.entry_medico,
            }

            estilo_padrao = "border: none;"

            estilo_erro = "border: 1px solid red;"

            # Verifica se os campos obrigatórios estão preenchidos
            for campo, widget in campos_obrigatorios.items():
                if isinstance(widget, QtWidgets.QLineEdit) and not widget.text().strip():
                    widget.setStyleSheet(estilo_erro)
                    widget.setFocus()
                    raise ValueError(f"O campo '{campo}' não pode estar vazio.")
                else:
                    widget.setStyleSheet(estilo_padrao)  # Remove o estilo de erro

            # Valida as quantidades
            Utils._validar_quantidade(dialog.entry_quant_procedimento, dialog.entry_quant_ampola)

            # Valida o custo
            if dialog.entry_custo.value() == 0:  # Usar valor do QDoubleSpinBox diretamente
                dialog.entry_custo.setStyleSheet(estilo_erro)
                dialog.entry_custo.setFocus()
                raise ValueError("O custo deve ser um número válido.")
            else:
                dialog.entry_custo.setStyleSheet(estilo_padrao)  # Remove o estilo de erro

            return True

        except ValueError as e:
            QtWidgets.QMessageBox.warning(dialog, "Validação", str(e))
            return False

    @staticmethod
    def _validar_quantidade(quantidade_procedimento, quantidade_ampola):
        """Valida que as quantidades são coerentes, seguindo as regras de negócio."""
        if quantidade_procedimento.value() == 0 and quantidade_ampola.value() == 0:
            quantidade_procedimento.setStyleSheet("border: 1px solid red;")
            quantidade_ampola.setStyleSheet("border: 1px solid red;")
            raise ValueError("Pelo menos um dos campos deve ser maior que zero.")
        else:
            quantidade_procedimento.setStyleSheet("border: none;")
            quantidade_ampola.setStyleSheet("border: none;")
