from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

class Utils:

    @staticmethod
    def converter_string_para_qdate(data_str, formato="dd/MM/yyyy"):
        """ Converte uma string de data no formato especificado para QDate. """
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
            raise ValueError("Data inválida. Use o formato yyyy-mm-dd ou yyyy/mm/dd.")

        if len(parts) == 3:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
        else:
            raise ValueError("Data inválida. Use o formato yyyy-mm-dd ou yyyy/mm/dd.")
        
    def formatar_data_para_banco(data):
        """ Formata a data de dd/mm/yyyy para yyyy-mm-dd para salvar no banco de dados. """
        if '/' in data:
            partes = data.split('/')
            # Converte a data para o formato yyyy-mm-dd
            return f'{partes[2]}-{partes[1]}-{partes[0]}'
        else:
            raise ValueError("Data inválida. Use o formato dd/mm/yyyy.")


    @staticmethod
    def formatar_custo_para_exibicao(custo):
        try:
            valor = float(custo)  # Certifica-se de que o valor é float
            # Formata para exibição no padrão brasileiro
            return f"R$ {valor:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
        except ValueError:
            raise ValueError("Custo inválido. Certifique-se de usar um número válido no formato R$ 1.234,56")

    @staticmethod
    def formatar_custo_para_banco(custo_str):
        try:
            # Remove 'R$', espaços e substitui vírgulas por pontos
            custo = custo_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            valor = float(custo)  # Converte para float
            return valor
        except ValueError:
            raise ValueError("Custo inválido. Certifique-se de usar um número válido no formato R$ 1.234,56")

        
    @staticmethod
    def validar_campos(dialog):
        """ Valida se todos os campos obrigatórios estão preenchidos no diálogo fornecido. """
        try:
            campos_obrigatorios = {
                "Data": dialog.entry_data,
                "Procedimento": dialog.entry_procedimento,
                "Quantidade de Procedimento": dialog.entry_quant_procedimento,
                "Quantidade de Ampola": dialog.entry_quant_ampola,
                "Local": dialog.entry_local,
                "Medico": dialog.entry_medico,
            }

            # Verifica se os campos obrigatórios estão preenchidos
            for campo, widget in campos_obrigatorios.items():
                if not widget.text().strip():
                    widget.setFocus()
                    raise ValueError(f"O campo {campo} não pode estar vazio.")

            # Valida as quantidades
            Utils._validar_quantidade(campos_obrigatorios["Quantidade de Procedimento"].text())
            Utils._validar_quantidade(campos_obrigatorios["Quantidade de Ampola"].text())

            # Valida o custo
            if not Utils._validar_custo(dialog.entry_custo.text()):
                dialog.entry_custo.setFocus()
                raise ValueError("O custo deve ser um número válido no formato 1234.56.")

            return True

        except ValueError as e:
            QtWidgets.QMessageBox.warning(dialog, "Validação", str(e))
            return False

    @staticmethod
    def _validar_custo(custo_str):
        """ Valida se o custo é um número válido. """
        try:
            # Remove 'R$', espaços e substitui vírgulas por pontos
            custo = custo_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            float(custo)  # Tenta converter para float
            return True
        except ValueError:
            return False

    @staticmethod
    def _validar_quantidade(quantidade):
        """ Valida se a quantidade é um número válido. """
        if not quantidade.isdigit():
            raise ValueError("Os campos de Quantidade devem conter valores numéricos válidos.")
