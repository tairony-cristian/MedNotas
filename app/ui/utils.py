import locale
from PyQt5 import QtWidgets

def formatar_data(data):
    if '/' not in data:
        return f'{data[:2]}/{data[2:4]}/{data[4:]}' if len(data) == 8 else data
    return data

def formatar_custo(custo_str):
    if custo_str.startswith("R$"):
        custo_str = custo_str[2:].strip()
    custo_str = custo_str.replace('.', '').replace(',', '.')
    try:
        return float(custo_str) if custo_str else None
    except ValueError:
        raise ValueError("Custo inválido. Certifique-se de usar um número válido para o campo Custo.")
    
def validar_campos(self):
        data = self.entry_data.text()
        procedimento = self.entry_procedimento.text()
        quant_procedimento = self.entry_quant_procedimento.text()
        quant_ampola = self.entry_quant_ampola.text()
        local = self.entry_local.text()
        return data and procedimento and quant_procedimento and quant_ampola and local

def preencher_campos(self, row_data):
        self.entry_data.setText(row_data[1])
        self.entry_procedimento.setText(row_data[2])
        self.entry_quant_procedimento.setText(row_data[3])
        self.entry_quant_ampola.setText(row_data[4])
        self.entry_custo.setText(row_data[5])
        self.entry_local.setText(row_data[6])
        self.entry_medico.setText(row_data[7])
        self.entry_observacao.setText(row_data[8])

def limpar_campos(self):
        self.entry_data.clear()
        self.entry_procedimento.clear()
        self.entry_quant_procedimento.clear()
        self.entry_quant_ampola.clear()
        self.entry_custo.clear()
        self.entry_local.clear()
        self.entry_medico.clear()
        self.entry_observacao.clear()

def atualizar_tabela(self, rows):
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column_index, data in enumerate(row):
                if column_index == 5 and data is not None:
                    data = locale.currency(data, grouping=True)
                self.table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(str(data)))