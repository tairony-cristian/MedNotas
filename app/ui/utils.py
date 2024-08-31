from PyQt5 import QtWidgets

class Utils:
    @staticmethod
    def formatar_data(data):
        """ Formata a data no formato dd/mm/yyyy. """
        if '/' not in data:
            if len(data) == 8:
                return f'{data[:2]}/{data[2:4]}/{data[4:]}'
            else:
                raise ValueError("Data inválida. Use o formato ddmmaaaa ou dd/mm/yyyy.")
        return data

    @staticmethod
    def formatar_custo(custo_str):
        """ Formata o custo no formato R$ 1.234,56. """
        try:
            if custo_str.startswith("R$"):
                custo_str = custo_str[2:].strip()  # Remove 'R$' e espaços extras
            custo_str = custo_str.replace('.', '').replace(',', '.')  # Substitui '.' por ',' e vice-versa

            valor = float(custo_str)
            return f'R$ {valor:,.2f}'.replace('.', ',')

        except ValueError:
            raise ValueError("Custo inválido. Certifique-se de usar um número válido no formato R$ x.xxx,xx.")

    @staticmethod
    def validar_campos(dialog):
        """ Valida se todos os campos obrigatórios estão preenchidos no diálogo fornecido. """
        try:
            campos_obrigatorios = {
                "Data": dialog.entry_data.text(),
                "Procedimento": dialog.entry_procedimento.text(),
                "Quantidade de Procedimento": dialog.entry_quant_procedimento.text(),
                "Quantidade de Ampola": dialog.entry_quant_ampola.text(),
                "Local": dialog.entry_local.text(),
                "Medico": dialog.entry_medico.text(),
            }

            for campo, valor in campos_obrigatorios.items():
                if not valor.strip():
                    raise ValueError(f"O campo {campo} não pode estar vazio.")

            Utils._validar_quantidade(campos_obrigatorios["Quantidade de Procedimento"])
            Utils._validar_quantidade(campos_obrigatorios["Quantidade de Ampola"])

            return True

        except ValueError as e:
            QtWidgets.QMessageBox.warning(dialog, "Validação", str(e))
            return False


    @staticmethod
    def _validar_quantidade(quantidade):
        """ Valida se a quantidade é um número válido. """
        if not quantidade.isdigit():
            raise ValueError("Os campos de Quantidade devem conter valores numéricos válidos.")
