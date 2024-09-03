import sys
import locale
from PyQt5 import QtWidgets
from ui.main_window import MainWindow

def main():
    # Definir a localidade para pt_BR (Português do Brasil)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    # Criar a aplicação Qt
    app = QtWidgets.QApplication(sys.argv)
    
    # Carregar o estilo QSS
    style_path = "app/resources/style.qss"
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Arquivo de estilo não encontrado: {style_path}")
    
    # Criar e exibir a janela principal
    window = MainWindow()
    window.show()
    
    # Executar o loop de eventos da aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
