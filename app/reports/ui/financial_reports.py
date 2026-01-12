
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from app.database.db import get_db_manager

class FinancialReportWindow(QWidget):
    def __init__(self, report_type):
        super().__init__()
        self.report_type = report_type
        self.setWindowTitle(f"Relatório de {report_type}")
        self.layout = QVBoxLayout(self)
        self.setup_filters()
        self.setup_table()
        self.setup_buttons()

    def setup_filters(self):
        self.filters_layout = QFormLayout()
        self.filters = {}

        if self.report_type == "Lucro por Produto":
            self.filters["produto_de"] = QLineEdit()
            self.filters["produto_ate"] = QLineEdit()
            self.filters["periodo_de"] = QLineEdit()
            self.filters["periodo_ate"] = QLineEdit()
            self.filters_layout.addRow("Produto (de):", self.filters["produto_de"])
            self.filters_layout.addRow("Produto (até):", self.filters["produto_ate"])
            self.filters_layout.addRow("Período (de):", self.filters["periodo_de"])
            self.filters_layout.addRow("Período (até):", self.filters["periodo_ate"])
        elif self.report_type == "Lucro por Período":
            self.filters["data_inicial"] = QLineEdit()
            self.filters["data_final"] = QLineEdit()
            self.filters_layout.addRow("Data Inicial:", self.filters["data_inicial"])
            self.filters_layout.addRow("Data Final:", self.filters["data_final"])

        self.layout.addLayout(self.filters_layout)

    def setup_table(self):
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def setup_buttons(self):
        self.generate_button = QPushButton("Gerar Relatório")
        self.generate_button.clicked.connect(self.generate_report)
        self.layout.addWidget(self.generate_button)

        pass

    def generate_report(self):
        if self.report_type == "Lucro por Produto":
            self.generate_profit_by_product_report()
        elif self.report_type == "Lucro por Período":
            self.generate_profit_by_period_report()
            
        self.prompt_export()

    def prompt_export(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Exportar Relatório")
        layout = QVBoxLayout(dialog)
        
        pdf_button = QPushButton("Exportar para PDF")
        pdf_button.clicked.connect(lambda: self.export_and_open("pdf"))
        layout.addWidget(pdf_button)
        
        excel_button = QPushButton("Exportar para Excel")
        excel_button.clicked.connect(lambda: self.export_and_open("excel"))
        layout.addWidget(excel_button)
        
        dialog.exec()

    def export_and_open(self, file_format):
        from app.reports.export import export_to_pdf, export_to_excel
        import os
        
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            data.append([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            
        if file_format == "pdf":
            filename = "relatorio.pdf"
            export_to_pdf(filename, data, headers)
        else:
            filename = "relatorio.xlsx"
            export_to_excel(filename, data, headers)
            
        self.open_file(filename)

    def open_file(self, filename):
        import subprocess
        import sys
        
        if sys.platform == "win32":
            os.startfile(filename)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", filename])
        else:
            subprocess.Popen(["xdg-open", filename])

    def generate_profit_by_product_report(self):
        filters = {
            "produto_de": self.filters["produto_de"].text(),
            "produto_ate": self.filters["produto_ate"].text(),
            "periodo_de": self.filters["periodo_de"].text(),
            "periodo_ate": self.filters["periodo_ate"].text(),
        }
        
        db_manager = get_db_manager()
        profit_data = db_manager.get_profit_by_product(filters)
        
        self.table.setRowCount(len(profit_data))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Produto", "Custo Unitário", "Preço de Venda", "Quantidade Vendida", "Lucro Unitário", "Lucro Total"])
        
        for row, data in enumerate(profit_data):
            self.table.setItem(row, 0, QTableWidgetItem(data["produto"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(data["custo_unitario"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(data["preco_venda"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(data["quantidade_vendida"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(data["lucro_unitario"])))
            self.table.setItem(row, 5, QTableWidgetItem(str(data["lucro_total"])))
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def generate_profit_by_period_report(self):
        filters = {
            "data_inicial": self.filters["data_inicial"].text(),
            "data_final": self.filters["data_final"].text(),
        }
        
        db_manager = get_db_manager()
        profit_data = db_manager.get_profit_by_period(filters)
        
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Total de Vendas", "Custo Total", "Lucro Final"])
        
        self.table.setItem(0, 0, QTableWidgetItem(str(profit_data["total_vendas"])))
        self.table.setItem(0, 1, QTableWidgetItem(str(profit_data["custo_total"])))
        self.table.setItem(0, 2, QTableWidgetItem(str(profit_data["lucro_final"])))
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def export_to_pdf(self):
        from app.reports.export import export_to_pdf
        
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            data.append([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            
        export_to_pdf("relatorio_financeiro.pdf", data, headers)

    def export_to_excel(self):
        from app.reports.export import export_to_excel
        
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            data.append([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            
        export_to_excel("relatorio_financeiro.xlsx", data, headers)
