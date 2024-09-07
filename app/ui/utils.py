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
                custo = re.sub(r'[^\d,]', '', custo).replace(',', '.')
                return float(custo)
            except ValueError:
                raise ValueError("Custo inválido. Certifique-se de usar um número válido no formato R$ 1.234,56.")
        else:
            raise ValueError("Custo deve ser uma string ou float.")

    @staticmethod
    def formatar_custo_para_exibicao(custo):
        """ Formata o custo para exibição como valor monetário. """
        if not isinstance(custo, (float, int)):
            raise ValueError("Custo deve ser um valor numérico.")

        return f"R$ {custo:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

    @staticmethod
    def atualizar_formatacao_custo(entry_custo):
        """Atualiza a formatação do campo de custo em tempo real para formato monetário R$."""
        try:
            texto = entry_custo.text().strip().replace("R$", "").replace(".", "").replace(",", "").strip()
            if not texto or int(texto) == 0:
                entry_custo.setText("R$ 0,00")
                entry_custo.setCursorPosition(entry_custo.text().index("0,00"))
                return

            texto = texto.zfill(3)
            valor_float = float(texto[:-2] + "." + texto[-2:])
            entry_custo.setText(Utils.formatar_custo_para_exibicao(valor_float))
            entry_custo.setCursorPosition(len(entry_custo.text()))
        except ValueError:
            entry_custo.setText("R$ 0,00")
            entry_custo.setCursorPosition(entry_custo.text().index("0,00"))

    @staticmethod
    def validar_campos(dialog):
        """Valida se todos os campos obrigatórios estão preenchidos no diálogo fornecido."""
        try:
            campos_obrigatorios = {
                "Data": dialog.entry_data,
                "Procedimento": dialog.entry_procedimento,
                "Quantidade de Procedimento": dialog.entry_quant_procedimento,
                "Quantidade de Ampola": dialog.entry_quant_ampola,
                "Custo": dialog.entry_custo,
                "Local": dialog.entry_local,
                "Médico": dialog.entry_medico,
            }

            estilo_padrao = "border: none;"
            estilo_erro = "border: 1px solid red;"

            for campo, widget in campos_obrigatorios.items():
                if isinstance(widget, QtWidgets.QLineEdit) and not widget.text().strip():
                    widget.setStyleSheet(estilo_erro)
                    widget.setFocus()
                    raise ValueError(f"O campo '{campo}' não pode estar vazio.")
                else:
                    widget.setStyleSheet(estilo_padrao)

            Utils._validar_quantidade(dialog.entry_quant_procedimento, dialog.entry_quant_ampola)

            custo_texto = dialog.entry_custo.text().strip()
            if not custo_texto or Utils.formatar_custo_para_banco(custo_texto) == 0:
                dialog.entry_custo.setStyleSheet(estilo_erro)
                dialog.entry_custo.setFocus()
                raise ValueError("O custo deve ser um número válido.")
            else:
                dialog.entry_custo.setStyleSheet(estilo_padrao)

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