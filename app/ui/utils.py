from PyQt5 import QtWidgets

class Utils:
    @staticmethod
    def formatar_data(data):
        """ Formata a data no formato dd/mm/yyyy. """
        if '/' not in data:
            return f'{data[:2]}/{data[2:4]}/{data[4:]}' if len(data) == 8 else data
        return data

    @staticmethod
    def formatar_custo(custo_str):
        """ Formata o custo no formato R$ 1.234,56. """
        try:
            if custo_str.startswith("R$"):
                custo_str = custo_str[2:].strip()  # Remove 'R$' e espaços extras
            custo_str = custo_str.replace('.', '').replace(',', '.')  # Substitui '.' por ',' e vice-versa

            if custo_str:
                valor = float(custo_str)
            else:
                valor = 0.0

            return f'R$ {valor:,.2f}'.replace('.', ',')
        
        except ValueError:
            raise ValueError("Custo inválido. Certifique-se de usar um número válido para o campo Custo.")

    @staticmethod
    def validar_campos(main_window):
        """ Valida se todos os campos obrigatórios estão preenchidos. """
        campos_obrigatorios = {
            "Data": main_window.entry_data.text(),
            "Procedimento": main_window.entry_procedimento.text(),
            "Quantidade de Procedimento": main_window.entry_quant_procedimento.text(),
            "Quantidade de Ampola": main_window.entry_quant_ampola.text(),
            "Local": main_window.entry_local.text(),
        }

        for campo, valor in campos_obrigatorios.items():
            if not valor.strip():
                QtWidgets.QMessageBox.warning(main_window, "Validação", f"O campo {campo} não pode estar vazio.")
                return False

        if not campos_obrigatorios["Quantidade de Procedimento"].isdigit() or not campos_obrigatorios["Quantidade de Ampola"].isdigit():
            QtWidgets.QMessageBox.warning(main_window, "Validação", "Os campos de Quantidade devem conter valores numéricos válidos.")
            return False

        return True
