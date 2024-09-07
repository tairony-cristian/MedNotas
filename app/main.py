import sys
import os
import locale
from PyQt5 import QtWidgets
from ui.main_window import MainWindow

def resource_path(relative_path):
    """ Obtém o caminho absoluto para os recursos no ambiente de execução. """
    try:
        # Para o ambiente de desenvolvimento
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)
    except NameError:
        # Para o ambiente do PyInstaller
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        return os.path.join(base_path, relative_path)

def main():
    # Definir a localidade para pt_BR (Português do Brasil)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    # Criar a aplicação Qt
    app = QtWidgets.QApplication(sys.argv)
    
    # Carregar o estilo QSS
    style_path = resource_path("resources/style.qss")
    try:
        with open(style_path, "r", encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Arquivo de estilo não encontrado: {style_path}")
    except UnicodeDecodeError as e:
        print(f"Erro ao ler o arquivo de estilo: {e}")
    
    # Criar e exibir a janela principal
    window = MainWindow()
    window.show()
    
    # Executar o loop de eventos da aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
