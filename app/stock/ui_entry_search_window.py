# app/stock/ui_entry_search_window.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit,
    QComboBox, QPushButton, QTableView, QHeaderView, QAbstractItemView,
    QDateEdit, QStackedWidget
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QDate
from app.stock.service import StockService
from app.utils.ui_utils import show_error_message
from app.stock.ui_entry_edit_window import EntryEditWindow
from app.utils.date_utils import format_date_for_display, BR_DATE_FORMAT, parse_date_for_db

class EntrySearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.stock_service = StockService()
        self.edit_window = None
        self.setWindowTitle("Pesquisa de Entradas de Insumo")
        self.setGeometry(200, 200, 900, 700)
        self.setup_ui()
        self.load_entries()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        search_group = QGroupBox("Pesquisa")
        search_layout = QHBoxLayout()
        self.search_field = QComboBox()
        self.search_field.addItems(["ID", "Nº Nota", "Data Entrada", "Valor Total", "Status"])
        self.search_field.currentTextChanged.connect(self.update_search_widget)

        self.search_stack = QStackedWidget()
        self.search_term_text = QLineEdit()
        self.search_term_text.returnPressed.connect(self.load_entries)
        self.search_term_date = QDateEdit(calendarPopup=True)
        self.search_term_date.setDisplayFormat(BR_DATE_FORMAT)
        self.search_term_date.setDate(QDate.currentDate())

        self.search_stack.addWidget(self.search_term_text)
        self.search_stack.addWidget(self.search_term_date)

        self.update_search_widget(self.search_field.currentText())

        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.load_entries)
        new_button = QPushButton("Nova Entrada")
        new_button.clicked.connect(self.open_new_entry_window)

        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_stack, 1)
        search_layout.addWidget(search_button)
        search_layout.addWidget(new_button)
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)

        results_group = QGroupBox("Resultados")
        results_layout = QVBoxLayout()
        self.table_view = QTableView()
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(["ID", "Data Entrada", "Nº Nota", "Valor Total", "Status"])
        self.table_view.setModel(self.table_model)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSortingEnabled(True)
        self.table_view.setStyleSheet("QTableView::item:selected { background-color: #D3D3D3; color: black; }")
        self.table_view.doubleClicked.connect(self.open_edit_entry_window)

        results_layout.addWidget(self.table_view)
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)

    def load_entries(self):
        self.table_model.removeRows(0, self.table_model.rowCount())
        search_field = self.search_field.currentText()

        if search_field == "Data Entrada":
            search_term = parse_date_for_db(self.search_term_date.date())
        else:
            search_term = self.search_term_text.text()

        response = self.stock_service.list_entries(search_term, search_field)

        if response["success"]:
            for entry in response["data"]:
                row = [
                    QStandardItem(str(entry['ID'])),
                    QStandardItem(format_date_for_display(entry.get('DATA_ENTRADA', ''))),
                    QStandardItem(entry.get('NUMERO_NOTA', '')),
                    QStandardItem(f"{entry.get('VALOR_TOTAL', 0):.2f}" if entry.get('VALOR_TOTAL') is not None else "N/A"),
                    QStandardItem(entry.get('STATUS', ''))
                ]
                self.table_model.appendRow(row)
        else:
            show_error_message(self, "Error", response["message"])

    def open_new_entry_window(self):
        self.show_edit_window(entry_id=None)

    def open_edit_entry_window(self, model_index):
        entry_id = int(self.table_model.item(model_index.row(), 0).text())
        self.show_edit_window(entry_id=entry_id)

    def show_edit_window(self, entry_id):
        if self.edit_window is None:
            self.edit_window = EntryEditWindow(entry_id=entry_id)
            self.edit_window.destroyed.connect(self.on_edit_window_closed)
            self.edit_window.show()
        else:
            self.edit_window.activateWindow()
            self.edit_window.raise_()

    def on_edit_window_closed(self):
        self.edit_window = None
        self.load_entries()

    def update_search_widget(self, field):
        placeholders = {
            "Valor Total": "Pesquisar por valor (ex: 50.25)...",
            "ID": "Pesquisar por ID...",
            "Nº Nota": "Pesquisar por número da nota...",
            "Status": "Pesquisar por status (Em Aberto, Finalizada)..."
        }

        if field == "Data Entrada":
            self.search_stack.setCurrentIndex(1)
        else:
            self.search_stack.setCurrentIndex(0)
            self.search_term_text.setPlaceholderText(placeholders.get(field, "Digite para pesquisar..."))
