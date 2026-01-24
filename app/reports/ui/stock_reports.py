
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QDateEdit
from PySide6.QtCore import Qt
from app.database.db import get_db_manager
from app.reports.export import export_to_pdf, export_to_excel
from app.utils.ui_utils import get_save_filename, show_success_message

from app.styles.buttons_styles import (
    button_style, BLUE, GREEN
)
from app.styles.windows_style import (
    window_style, LIGHT
)
from app.styles.input_styles import (
    input_style, DEFAULTINPUT
)

class StockReportWindow(QWidget):
    def __init__(self, report_type):
        super().__init__()
        self.report_type = report_type
        self.setWindowTitle(f"Relatório de {report_type}")
        self.setStyleSheet(window_style(LIGHT))
        self.layout = QVBoxLayout(self)
        self.setup_filters()
        self.setup_buttons()
        self.apply_styles_to_filters()

    def setup_filters(self):
        self.filters_layout = QFormLayout()
        self.filters = {}

        if self.report_type == "Entradas (Compras)":
            self.filters["numero_de"] = QLineEdit()
            self.filters["numero_ate"] = QLineEdit()
            self.filters["fornecedor"] = QLineEdit()
            self.filters["data_inicial"] = QDateEdit()
            self.filters["data_final"] = QDateEdit()
            self.filters["data_inicial"].setCalendarPopup(True)
            self.filters["data_final"].setCalendarPopup(True)
            self.filters_layout.addRow("Número (de):", self.filters["numero_de"])
            self.filters_layout.addRow("Número (até):", self.filters["numero_ate"])
            self.filters_layout.addRow("Fornecedor:", self.filters["fornecedor"])
            self.filters_layout.addRow("Data Inicial:", self.filters["data_inicial"])
            self.filters_layout.addRow("Data Final:", self.filters["data_final"])
        elif self.report_type == "Movimentação de Estoque":
            self.filters["item_de"] = QLineEdit()
            self.filters["item_ate"] = QLineEdit()
            self.filters["periodo_de"] = QDateEdit()
            self.filters["periodo_ate"] = QDateEdit()
            self.filters["periodo_de"].setCalendarPopup(True)
            self.filters["periodo_ate"].setCalendarPopup(True)
            self.filters_layout.addRow("Item (de):", self.filters["item_de"])
            self.filters_layout.addRow("Item (até):", self.filters["item_ate"])
            self.filters_layout.addRow("Período (de):", self.filters["periodo_de"])
            self.filters_layout.addRow("Período (até):", self.filters["periodo_ate"])
        elif self.report_type == "Estoque Atual":
            pass # No filters for this report
        elif self.report_type == "Itens da Nota de Entrada":
            self.filters["nota_de"] = QLineEdit()
            self.filters["nota_ate"] = QLineEdit()
            self.filters_layout.addRow("Nota (de):", self.filters["nota_de"])
            self.filters_layout.addRow("Nota (até):", self.filters["nota_ate"])

        self.layout.addLayout(self.filters_layout)

    def setup_buttons(self):
        self.generate_button = QPushButton("Gerar Relatório")
        self.generate_button.setStyleSheet(button_style(BLUE))
        self.generate_button.clicked.connect(self.generate_report)
        self.layout.addWidget(self.generate_button)

    def apply_styles_to_filters(self):
        for widget in self.filters.values():
            if isinstance(widget, (QLineEdit, QDateEdit)):
                widget.setStyleSheet(input_style(DEFAULTINPUT))

    def generate_report(self):
        if self.report_type == "Entradas (Compras)":
            headers, data = self.generate_input_supplies_report()
        elif self.report_type == "Movimentação de Estoque":
            headers, data = self.generate_stock_movement_report()
        elif self.report_type == "Estoque Atual":
            headers, data = self.generate_current_stock_report()
        elif self.report_type == "Itens da Nota de Entrada":
            headers, data = self.generate_entry_items_report()
        else:
            headers, data = [], []

        if data:
            self.show_preview(headers, data)
        else:
            show_success_message(self, "Relatório", "Nenhum dado encontrado para os filtros selecionados.")

    def show_preview(self, headers, data):
        dialog = QDialog(self)
        dialog.setWindowTitle("Pré-visualização do Relatório")
        dialog.setStyleSheet(window_style(LIGHT))
        dialog.setMinimumSize(800, 600)
        layout = QVBoxLayout(dialog)
        
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data))
        
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(item)))
        
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table)
        
        save_button = QPushButton("Salvar")
        save_button.setStyleSheet(button_style(GREEN))
        save_button.clicked.connect(lambda: self.save_report(headers, data))
        layout.addWidget(save_button)
        
        dialog.exec()

    def save_report(self, headers, data):
        filename, selected_filter = get_save_filename(self, "Salvar Relatório", "PDF (*.pdf);;Excel (*.xlsx)")
        
        if filename:
            if "pdf" in selected_filter:
                export_to_pdf(filename, data, headers)
            elif "xlsx" in selected_filter:
                export_to_excel(filename, data, headers)

    def generate_input_supplies_report(self):
        filters = {
            "numero_de": self.filters["numero_de"].text(),
            "numero_ate": self.filters["numero_ate"].text(),
            "fornecedor": self.filters["fornecedor"].text(),
            "data_inicial": self.filters["data_inicial"].date().toString("yyyy-MM-dd"),
            "data_final": self.filters["data_final"].date().toString("yyyy-MM-dd"),
        }
        
        db_manager = get_db_manager()
        entries = db_manager.get_stock_entries(filters)
        
        headers = ["Número", "Fornecedor", "Data", "Total"]
        data = [[e["numero"], e["fornecedor"], e["data"], e["total"]] for e in entries]
        
        return headers, data

    def generate_stock_movement_report(self):
        filters = {
            "item_de": self.filters["item_de"].text(),
            "item_ate": self.filters["item_ate"].text(),
            "periodo_de": self.filters["periodo_de"].date().toString("yyyy-MM-dd"),
            "periodo_ate": self.filters["periodo_ate"].date().toString("yyyy-MM-dd"),
        }
        
        db_manager = get_db_manager()
        movements = db_manager.get_stock_movements(filters)
        
        headers = ["Item", "Tipo de Movimento", "Quantidade", "Valor Unitário", "Data"]
        data = [[m["item"], m["tipo_movimento"], m["quantidade"], m["valor_unitario"], m["data_movimento"]] for m in movements]
        
        return headers, data

    def generate_current_stock_report(self):
        db_manager = get_db_manager()
        stock = db_manager.get_current_stock()
        
        headers = ["Item", "Saldo em Estoque", "Custo Médio"]
        data = [[s["DESCRICAO"], s["SALDO_ESTOQUE"], s["CUSTO_MEDIO"]] for s in stock]
        
        return headers, data

    def generate_entry_items_report(self):
        filters = {
            "nota_de": self.filters["nota_de"].text(),
            "nota_ate": self.filters["nota_ate"].text(),
        }
        
        db_manager = get_db_manager()
        entry_items_data = db_manager.get_entry_items_report(filters)
        
        headers = ["Nota", "Insumo", "Quantidade", "Valor Unitário", "Valor Total"]
        data = [[i["nota"], i["insumo"], i["quantidade"], i["valor_unitario"], i["valor_total"]] for i in entry_items_data]
        
        return headers, data
