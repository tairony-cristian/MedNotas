import csv
from PyQt5 import QtWidgets
from openpyxl import Workbook
from reportlab.lib.pagesizes import  A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from fpdf import FPDF

class RelatorioExporter:
    def __init__(self, main_window, dados_filtrados=None):
        self.main_window = main_window
        self.dados_filtrados = dados_filtrados or []

    def exportar_relatorio(self):
        if not hasattr(self.main_window, 'table'):
            raise AttributeError("O objeto MainWindow não possui o atributo 'table'.")

        if not self.dados_filtrados:
            QtWidgets.QMessageBox.critical(
                self.main_window, 
                "Erro ao Exportar", 
                "Nenhum dado disponível para exportar."
            )
            return

        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.main_window, 
            "Salvar Relatório", 
            "",
            "Excel Files (*.xlsx);;PDF Files (*.pdf);;CSV Files (*.csv);;All Files (*)",
            options=options
        )
        
        if file_name:
            try:
                if file_name.endswith('.csv'):
                    self.salvar_relatorio_csv(file_name)
                elif file_name.endswith('.xlsx'):
                    self.salvar_relatorio_excel(file_name)
                elif file_name.endswith('.pdf'):
                    self.salvar_relatorio_pdf(file_name)
                QtWidgets.QMessageBox.information(
                    self.main_window, 
                    "Exportar Relatório", 
                    "Relatório exportado com sucesso!"
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self.main_window, 
                    "Erro ao Exportar", 
                    f"Não foi possível exportar o relatório: {str(e)}"
                )

    def salvar_relatorio_csv(self, file_name):
        try:
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Adiciona o cabeçalho
                writer.writerow(["ID", "Data", "Procedimento", "Quant. Procedimento", "Quant. Ampola", "Custo", "Local", "Médico", "Nota Fiscal", "Observação"])
                # Adiciona os dados
                for row in self.dados_filtrados:
                    # Encode and decode to ensure special characters are handled
                    row = [str(cell).encode('utf-8', errors='replace').decode('utf-8') for cell in row]
                    writer.writerow(row)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.main_window, 
                "Erro ao Exportar CSV", 
                f"Não foi possível exportar o CSV: {str(e)}"
            )

    def salvar_relatorio_excel(self, file_name):
        wb = Workbook()
        ws = wb.active

        # Adiciona o cabeçalho
        ws.append(["ID", "Data", "Procedimento", "Quant. Procedimento", "Quant. Ampola", "Custo", "Local", "Médico", "Nota Fiscal", "Observação"])

        # Adiciona os dados
        if self.dados_filtrados:
            for row in self.dados_filtrados:
                ws.append(row)

        wb.save(file_name)


    def salvar_relatorio_pdf(self, file_name):
        # Define o documento com margens ajustadas
        doc = SimpleDocTemplate(file_name, pagesize=A4, rightMargin=0.5*inch, leftMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []

        # Cabeçalhos da tabela
        data = [["ID", "Data", "Procedimento", "Quant. Proced.", "Quant. Ampola", "Custo", "Local", "Médico", "Nota Fiscal", "Observação"]]
        
        # Adiciona os dados filtrados
        for row in self.dados_filtrados:
            data.append(row)

        # Cria a tabela
        table = Table(data)

        # Calcula a largura disponível para a tabela (considerando as margens ajustadas)
        page_width = A4[0]  # Largura da página A4
        margin = 0.5 * inch  # Margens ajustadas para 0.5 polegada (esquerda e direita)
        available_width = page_width - 2 * margin  # Largura disponível para a tabela

        # Define larguras das colunas proporcionalmente ao espaço disponível
        col_widths = [
            available_width * 0.06,  # ID
            available_width * 0.10,  # Data
            available_width * 0.14,  # Procedimento
            available_width * 0.12,  # Quant. Procedimento
            available_width * 0.12,  # Quant. Ampola
            available_width * 0.10,  # Custo
            available_width * 0.12,  # Local
            available_width * 0.10,  # Médico
            available_width * 0.10,  # Nota Fiscal
            available_width * 0.14   # Observação
        ]
        table._argW = col_widths

        # Estiliza a tabela com fontes menores e quebra de linha automática
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-8, -1), 'CENTER'),  # Mantém alinhado ao centro para os outros campos
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),  # Procedimento
            ('ALIGN', (6, 1), (6, -1), 'LEFT'),  # Local
            ('ALIGN', (7, 1), (7, -1), 'LEFT'),  # Médico
            ('ALIGN', (8, 1), (8, -1), 'LEFT'),  # Nota Fiscal
            ('ALIGN', (9, 1), (9, -1), 'LEFT'),  # Observação
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 6.5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('WORDWRAP', (0, 1), (-1, -1), 'TRUE'),  # Quebra de linha automática para todos os campos
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alinhamento no topo das células
            ('ROWHEIGHT', (0, 1), (-1, -1), 20),  # Define altura mínima das linhas
        ])
        table.setStyle(style)

        # Adiciona a tabela aos elementos
        elements.append(table)

        # Constrói o documento
        doc.build(elements)
