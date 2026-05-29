# main.py
import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QWidget,
    QPushButton,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
    QToolBar,
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, QSize
from functools import partial

from app.styles.windows_style import (
    window_style, LIGHT
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windows = {}
        self.setWindowTitle("GP - MiniSis")
        self.setWindowIcon(QIcon(self._resolve_icon('home.svg')))
        self.setGeometry(100, 100, 1200, 820)
        self.setStyleSheet(window_style(LIGHT))
        self.setup_menus()
        self.setup_toolbar()
        self.setup_central_widget()
        self.statusBar().showMessage("Pronto")

    def _resolve_icon(self, icon_name):
        project_root = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(project_root, "app", "styles", "images", "icons", icon_name)

    def setup_menus(self):
        menu_bar = self.menuBar()
        
        # Menu Cadastros
        registers_menu = menu_bar.addMenu("&Cadastros")
        
        from app.item.ui_search_window import ItemSearchWindow
        self._add_menu_action(registers_menu, "Produtos", "item_search_window", ItemSearchWindow, 'registro_produto_icon.svg')
        
        from app.supplier.ui_search_window import SupplierSearchWindow
        self._add_menu_action(registers_menu, "Fornecedores", "supplier_search_window", SupplierSearchWindow, 'fornecedor_registro.svg')
        
        registers_menu.addSeparator()

        from app.unit.ui_unit_window import UnitWindow
        self._add_menu_action(registers_menu, "Unidades de Medida", "unit_window", UnitWindow)
        
        # Menu Movimento
        movement_menu = menu_bar.addMenu("&Movimento")
        
        from app.stock.ui_entry_search_window import EntrySearchWindow
        self._add_menu_action(movement_menu, "Entrada de Insumos", "stock_entry_window", EntrySearchWindow, 'entrada_insumos.svg')

        movement_menu.addSeparator()

        from app.production_line.ui_line_list_window import LineListWindow
        self._add_menu_action(movement_menu, "Linhas de Produção", "line_list_window", LineListWindow, 'linha_producao_icon.svg')
        
        from app.production.ui_op_search_window import OPSearchWindow
        self._add_menu_action(movement_menu, "Ordem de Produção", "op_search_window", OPSearchWindow, 'order_producao.svg')
        
        movement_menu.addSeparator()

        from app.sales.ui_sale_search_window import SaleSearchWindow
        self._add_menu_action(movement_menu, "Saída de Produtos", "sale_search_window", SaleSearchWindow, 'saida_produtos.svg')

        # Menu Relatórios
        reports_menu = menu_bar.addMenu("&Relatórios")
        
        # Submenu Cadastros
        general_reports_menu = reports_menu.addMenu("Cadastros")
        from app.reports.ui.general_reports import GeneralReportWindow
        self._add_menu_action(general_reports_menu, "Fornecedores", "suppliers_report", lambda: GeneralReportWindow("Fornecedores"))
        self._add_menu_action(general_reports_menu, "Itens", "items_report", lambda: GeneralReportWindow("Itens"))

        # Submenu Estoque
        stock_reports_menu = reports_menu.addMenu("Estoque")
        from app.reports.ui.stock_reports import StockReportWindow
        self._add_menu_action(stock_reports_menu, "Entradas (Compras)", "stock_entry_report", lambda: StockReportWindow("Entradas (Compras)"))
        self._add_menu_action(stock_reports_menu, "Itens da Nota de Entrada", "entry_items_report", lambda: StockReportWindow("Itens da Nota de Entrada"))
        self._add_menu_action(stock_reports_menu, "Movimentação de Estoque", "stock_movement_report", lambda: StockReportWindow("Movimentação de Estoque"))
        self._add_menu_action(stock_reports_menu, "Estoque Atual", "current_stock_report", lambda: StockReportWindow("Estoque Atual"))
        self._add_menu_action(stock_reports_menu, "Estoque Baixo", "low_stock_report", lambda: StockReportWindow("Estoque Baixo"))
        self._add_menu_action(stock_reports_menu, "Curva ABC de Estoque", "abc_report", lambda: StockReportWindow("Curva ABC de Estoque"))
        self._add_menu_action(stock_reports_menu, "Itens Sem Giro", "inactive_report", lambda: StockReportWindow("Itens Sem Giro"))

        # Submenu Produção
        production_reports_menu = reports_menu.addMenu("Produção")
        from app.reports.ui.production_reports import ProductionReportWindow
        self._add_menu_action(production_reports_menu, "Ordens de Produção", "production_orders_report", lambda: ProductionReportWindow("Ordens de Produção"))
        self._add_menu_action(production_reports_menu, "Produção por Período", "production_by_period_report", lambda: ProductionReportWindow("Produção por Período"))
        self._add_menu_action(production_reports_menu, "Produção por Linha", "production_by_line_report", lambda: ProductionReportWindow("Produção por Linha"))
        self._add_menu_action(production_reports_menu, "Composição de Produto", "product_composition_report", lambda: ProductionReportWindow("Composição / Estrutura de Produto"))
        self._add_menu_action(production_reports_menu, "Rendimento de OP", "yield_report", lambda: ProductionReportWindow("Rendimento de OP"))
        self._add_menu_action(production_reports_menu, "Necessidade de Insumos", "requirements_report", lambda: ProductionReportWindow("Necessidade de Insumos"))

        # Submenu Financeiro
        financial_reports_menu = reports_menu.addMenu("Financeiro")
        from app.reports.ui.financial_reports import FinancialReportWindow
        self._add_menu_action(financial_reports_menu, "Custo do Produto", "product_cost_report", lambda: FinancialReportWindow("Custo do Produto"))
        self._add_menu_action(financial_reports_menu, "Lucro por Produto", "profit_by_product_report", lambda: FinancialReportWindow("Lucro por Produto"))
        self._add_menu_action(financial_reports_menu, "Lucro por Período", "profit_by_period_report", lambda: FinancialReportWindow("Lucro por Período"))

        # Menu Configurações
        # settings_menu = menu_bar.addMenu("&Configurações")

    def _add_menu_action(self, menu, text, window_name, window_class, icon_name=None):
        action = QAction(text, self)
        if icon_name:
            action.setIcon(QIcon(self._resolve_icon(icon_name)))
        action.triggered.connect(partial(self._open_window, window_name, window_class))
        menu.addAction(action)

    def _open_window(self, window_name, window_class):
        if window_name not in self.windows:
            self.windows[window_name] = window_class() if callable(window_class) else window_class

        window = self.windows[window_name]
        window.show()
        window.raise_()

    def setup_toolbar(self):
        from app.item.ui_search_window import ItemSearchWindow
        from app.reports.ui.stock_reports import StockReportWindow
        from app.supplier.ui_search_window import SupplierSearchWindow

        toolbar = QToolBar("Ações Rápidas")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setStyleSheet(
            "QToolBar { background-color: #FFFFFF; border-bottom: 1px solid #D1D9E6; spacing: 10px; padding: 8px; }"
            "QToolButton { background: transparent; border: none; padding: 8px 12px; border-radius: 12px; color: #0F172A; }"
            "QToolButton:hover { background-color: #EFF4FF; }"
            "QToolButton:checked { background-color: #E0E7FF; }"
        )

        dashboard_action = QAction(QIcon(self._resolve_icon('home.svg')), "Dashboard", self)
        products_action = QAction(QIcon(self._resolve_icon('registro_produto_icon.svg')), "Produtos", self)
        reports_action = QAction(QIcon(self._resolve_icon('reports.svg')), "Relatórios", self)
        supplier_action = QAction(QIcon(self._resolve_icon('fornecedor_registro.svg')), "Fornecedores", self)

        dashboard_action.triggered.connect(self.show_home)
        products_action.triggered.connect(partial(self._open_window, "item_search_window", ItemSearchWindow))
        reports_action.triggered.connect(partial(self._open_window, "stock_report_window", lambda: StockReportWindow("Estoque Atual")))
        supplier_action.triggered.connect(partial(self._open_window, "supplier_search_window", SupplierSearchWindow))

        toolbar.addAction(dashboard_action)
        toolbar.addAction(products_action)
        toolbar.addAction(reports_action)
        toolbar.addAction(supplier_action)
        toolbar.addSeparator()

        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def show_home(self):
        self.setCentralWidget(self.central_widget)

    def setup_central_widget(self):
        self.central_widget = QWidget()
        central_layout = QVBoxLayout(self.central_widget)
        central_layout.setContentsMargins(24, 24, 24, 24)
        central_layout.setSpacing(20)
        central_layout.addStretch(1)

        title = QLabel("Bem-vindo ao SOFME")
        title.setStyleSheet("font-size: 32px; font-weight: 800; color: #0F172A; text-align: center;")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel(
            "Sistema de organização financeira para microempreendedor."
        )
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #475569; line-height: 1.8;")

        central_layout.addWidget(title)
        central_layout.addWidget(subtitle)
        central_layout.addStretch(1)

        self.setCentralWidget(self.central_widget)


import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

import traceback

def main():
    try:
        from app.database.db import get_db_manager
        get_db_manager()

        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.showMaximized()
        sys.exit(app.exec())

    except Exception:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
