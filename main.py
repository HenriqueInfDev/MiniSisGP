# main.py
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

# Get the absolute path to the directory containing main.py
project_root = os.path.dirname(os.path.abspath(__file__))
# Add the project root to the Python path. This is crucial for absolute imports.
sys.path.insert(0, project_root)

from app.database import get_db_manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GP - MiniSis")
        try:
            logo_path = os.path.join(project_root, "app", "assets", "logo.png")
            if os.path.exists(logo_path):
                self.setWindowIcon(QIcon(logo_path))
        except Exception as e:
            print(f"Could not load window icon: {e}")

        self.setGeometry(100, 100, 1024, 768)

        self.setup_menus()
        self.setup_central_widget()
        self.statusBar().showMessage("Pronto")

        # Child window references
        self.child_windows = {}

    def setup_menus(self):
        menu_bar = self.menuBar()

        registers_menu = menu_bar.addMenu("&Cadastros")
        products_action = QAction("Produtos...", self)
        products_action.triggered.connect(lambda: self.open_window("item_search"))
        registers_menu.addAction(products_action)

        supplier_action = QAction("Fornecedores...", self)
        supplier_action.triggered.connect(lambda: self.open_window("supplier_search"))
        registers_menu.addAction(supplier_action)

        movement_menu = menu_bar.addMenu("&Movimento")
        entry_action = QAction("Entrada de Insumos...", self)
        entry_action.triggered.connect(lambda: self.open_window("stock_entry_search"))
        movement_menu.addAction(entry_action)

        op_action = QAction("Ordem de Produção...", self)
        op_action.triggered.connect(lambda: self.open_window("production_order"))
        movement_menu.addAction(op_action)

        settings_menu = menu_bar.addMenu("&Configurações")

    def setup_central_widget(self):
        central_widget = QLabel("Bem-vindo ao MiniSis - Gestão de Produção")
        central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(central_widget)

    def open_window(self, window_name):
        # Local imports to avoid circular dependencies
        from app.item.ui_search_window import SearchWindow
        from app.supplier.ui_supplier_search_window import SupplierSearchWindow
        from app.stock.ui_entry_search_window import EntrySearchWindow
        from app.production.ui_op_window import OPWindow

        if self.child_windows.get(window_name) is None:
            if window_name == "item_search":
                window = SearchWindow(parent=self)
            elif window_name == "supplier_search":
                window = SupplierSearchWindow(parent=self)
            elif window_name == "stock_entry_search":
                window = EntrySearchWindow(parent=self)
            elif window_name == "production_order":
                window = OPWindow(parent=self)
            else:
                return

            self.child_windows[window_name] = window
            window.destroyed.connect(lambda: self.child_windows.pop(window_name, None))
            window.show()
        else:
            self.child_windows[window_name].activateWindow()
            self.child_windows[window_name].raise_()

def main():
    print("Inicializando o banco de dados...")
    get_db_manager()

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
