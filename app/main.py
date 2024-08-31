# Quando clicar em editar anotação verificar se tem algum campo selecionado senão exibir 
# mensagem para selecionar um registro para editar

import sys
import locale
from PyQt5 import QtWidgets
from ui.main_window import MainWindow

def main():
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    app = QtWidgets.QApplication(sys.argv)
    
    # Carregar o estilo QSS
    style_path = "app/resources/style.qss"
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Arquivo de estilo não encontrado: {style_path}")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
