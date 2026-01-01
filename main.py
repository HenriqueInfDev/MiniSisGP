# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

from app.database import initialize_database
from app.item.ui_search_window import SearchWindow
from app.production.ui_op_window import OPWindow
from app.stock.ui_entry_search_window import EntrySearchWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search_window = None
        self.op_window = None
        self.entry_search_window = None

        self.setWindowTitle("GP - MiniSis")
        self.setWindowIcon(QIcon("app/assets/logo.png"))
        self.setGeometry(100, 100, 1024, 768)

        self.setup_menus()
        self.setup_central_widget()
        self.statusBar().showMessage("Pronto")

    def setup_menus(self):
        menu_bar = self.menuBar()

        # Menu Cadastros
        registers_menu = menu_bar.addMenu("&Cadastros")
        products_action = QAction("Produtos...", self)
        products_action.triggered.connect(self.open_products_window)
        registers_menu.addAction(products_action)

        # Menu Movimento
        movement_menu = menu_bar.addMenu("&Movimento")
        entry_action = QAction("Entrada de Insumos...", self)
        entry_action.triggered.connect(self.open_entry_search_window)
        movement_menu.addAction(entry_action)

        op_action = QAction("Ordem de Produção...", self)
        op_action.triggered.connect(self.open_op_window)
        movement_menu.addAction(op_action)

        # Menu Configurações
        settings_menu = menu_bar.addMenu("&Configurações")

    def setup_central_widget(self):
        central_widget = QLabel("Bem-vindo ao MiniSis - Gestão de Produção")
        central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(central_widget)

    def open_products_window(self):
        """Abre a janela de pesquisa de produtos, garantindo que apenas uma instância exista."""
        if self.search_window is None:
            self.search_window = SearchWindow(parent=self)
            self.search_window.destroyed.connect(lambda: setattr(self, 'search_window', None))
            self.search_window.show()
        else:
            self.search_window.activateWindow()
            self.search_window.raise_()

    def open_op_window(self):
        """Abre a janela de Ordem de Produção, garantindo que apenas uma instância exista."""
        if self.op_window is None:
            self.op_window = OPWindow(parent=self)
            self.op_window.destroyed.connect(lambda: setattr(self, 'op_window', None))
            self.op_window.show()
        else:
            self.op_window.activateWindow()
            self.op_window.raise_()

    def open_entry_search_window(self):
        """Abre a janela de pesquisa de entradas de insumo, garantindo que apenas uma instância exista."""
        if self.entry_search_window is None:
            self.entry_search_window = EntrySearchWindow(parent=self)
            self.entry_search_window.destroyed.connect(lambda: setattr(self, 'entry_search_window', None))
            self.entry_search_window.show()
        else:
            self.entry_search_window.activateWindow()
            self.entry_search_window.raise_()

def main():
    """Função principal que inicia a aplicação."""
    print("Inicializando o banco de dados...")
    initialize_database()

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
