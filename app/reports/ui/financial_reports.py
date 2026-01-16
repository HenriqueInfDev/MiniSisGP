
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QDateEdit
from PySide6.QtCore import Qt
from app.database.db import get_db_manager
from app.reports.export import export_to_pdf, export_to_excel
from app.utils.ui_utils import get_save_filename, show_success_message
import os

class FinancialReportWindow(QWidget):
    def __init__(self, report_type):
        super().__init__()
        self.report_type = report_type
        self.setWindowTitle(f"Relatório de {report_type}")
        self.layout = QVBoxLayout(self)
        self.setup_filters()
        self.setup_buttons()

    def setup_filters(self):
        self.filters_layout = QFormLayout()
        self.filters = {}

        if self.report_type == "Lucro por Produto":
            self.filters["produto_de"] = QLineEdit()
            self.filters["produto_ate"] = QLineEdit()
            self.filters["periodo_de"] = QDateEdit()
            self.filters["periodo_ate"] = QDateEdit()
            self.filters["periodo_de"].setCalendarPopup(True)
            self.filters["periodo_ate"].setCalendarPopup(True)
            self.filters_layout.addRow("Produto (de):", self.filters["produto_de"])
            self.filters_layout.addRow("Produto (até):", self.filters["produto_ate"])
            self.filters_layout.addRow("Período (de):", self.filters["periodo_de"])
            self.filters_layout.addRow("Período (até):", self.filters["periodo_ate"])
        elif self.report_type == "Lucro por Período":
            self.filters["data_inicial"] = QDateEdit()
            self.filters["data_final"] = QDateEdit()
            self.filters["data_inicial"].setCalendarPopup(True)
            self.filters["data_final"].setCalendarPopup(True)
            self.filters_layout.addRow("Data Inicial:", self.filters["data_inicial"])
            self.filters_layout.addRow("Data Final:", self.filters["data_final"])
        elif self.report_type == "Custo do Produto":
            self.filters["produto_de"] = QLineEdit()
            self.filters["produto_ate"] = QLineEdit()
            self.filters_layout.addRow("Produto (de):", self.filters["produto_de"])
            self.filters_layout.addRow("Produto (até):", self.filters["produto_ate"])

        self.layout.addLayout(self.filters_layout)

    def setup_buttons(self):
        self.generate_button = QPushButton("Gerar Relatório")
        self.generate_button.clicked.connect(self.generate_report)
        self.layout.addWidget(self.generate_button)

    def generate_report(self):
        if self.report_type == "Lucro por Produto":
            headers, data = self.generate_profit_by_product_report()
        elif self.report_type == "Lucro por Período":
            headers, data = self.generate_profit_by_period_report()
        elif self.report_type == "Custo do Produto":
            headers, data = self.generate_product_cost_report()
        else:
            headers, data = [], []

        if data:
            self.show_preview(headers, data)
        else:
            show_success_message(self, "Relatório", "Nenhum dado encontrado para os filtros selecionados.")

    def show_preview(self, headers, data):
        dialog = QDialog(self)
        dialog.setWindowTitle("Pré-visualização do Relatório")
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

    def generate_profit_by_product_report(self):
        filters = {
            "produto_de": self.filters["produto_de"].text(),
            "produto_ate": self.filters["produto_ate"].text(),
            "periodo_de": self.filters["periodo_de"].date().toString("yyyy-MM-dd"),
            "periodo_ate": self.filters["periodo_ate"].date().toString("yyyy-MM-dd"),
        }
        
        db_manager = get_db_manager()
        profit_data = db_manager.get_profit_by_product(filters)
        
        headers = ["Produto", "Custo Unitário", "Preço de Venda", "Quantidade Vendida", "Lucro Unitário", "Lucro Total"]
        data = [
            [
                d["produto"],
                d["custo_unitario"],
                d["preco_venda"],
                d["quantidade_vendida"],
                d["lucro_unitario"],
                d["lucro_total"],
            ]
            for d in profit_data
        ]
        
        return headers, data
        
    def generate_product_cost_report(self):
        filters = {
            "produto_de": self.filters["produto_de"].text(),
            "produto_ate": self.filters["produto_ate"].text(),
        }
        
        db_manager = get_db_manager()
        cost_data = db_manager.get_product_cost_report(filters)
        
        headers = ["Produto", "Custo Médio"]
        data = [[c["produto"], c["custo_medio"]] for c in cost_data]
        
        return headers, data

    def generate_profit_by_period_report(self):
        filters = {
            "data_inicial": self.filters["data_inicial"].date().toString("yyyy-MM-dd"),
            "data_final": self.filters["data_final"].date().toString("yyyy-MM-dd"),
        }
        
        db_manager = get_db_manager()
        profit_data = db_manager.get_profit_by_period(filters)
        
        headers = ["Total de Vendas", "Custo Total", "Lucro Final"]
        data = []
        if profit_data and profit_data["total_vendas"] is not None:
            data.append([
                profit_data["total_vendas"],
                profit_data["custo_total"],
                profit_data["lucro_final"],
            ])
        
        return headers, data
