
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from app.database.db import get_db_manager

class ProductionReportWindow(QWidget):
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

        if self.report_type == "Ordens de Produção":
            self.filters["id_de"] = QLineEdit()
            self.filters["id_ate"] = QLineEdit()
            self.filters["produto_de"] = QLineEdit()
            self.filters["produto_ate"] = QLineEdit()
            self.filters["status"] = QLineEdit()
            self.filters["periodo_de"] = QLineEdit()
            self.filters["periodo_ate"] = QLineEdit()
            self.filters_layout.addRow("ID (de):", self.filters["id_de"])
            self.filters_layout.addRow("ID (até):", self.filters["id_ate"])
            self.filters_layout.addRow("Produto (de):", self.filters["produto_de"])
            self.filters_layout.addRow("Produto (até):", self.filters["produto_ate"])
            self.filters_layout.addRow("Status:", self.filters["status"])
            self.filters_layout.addRow("Período (de):", self.filters["periodo_de"])
            self.filters_layout.addRow("Período (até):", self.filters["periodo_ate"])
        elif self.report_type == "Produção por Linha":
            self.filters["linha_de"] = QLineEdit()
            self.filters["linha_ate"] = QLineEdit()
            self.filters["periodo_de"] = QLineEdit()
            self.filters["periodo_ate"] = QLineEdit()
            self.filters_layout.addRow("Linha (de):", self.filters["linha_de"])
            self.filters_layout.addRow("Linha (até):", self.filters["linha_ate"])
            self.filters_layout.addRow("Período (de):", self.filters["periodo_de"])
            self.filters_layout.addRow("Período (até):", self.filters["periodo_ate"])
        elif self.report_type == "Composição / Estrutura de Produto":
            self.filters["produto_de"] = QLineEdit()
            self.filters["produto_ate"] = QLineEdit()
            self.filters_layout.addRow("Produto (de):", self.filters["produto_de"])
            self.filters_layout.addRow("Produto (até):", self.filters["produto_ate"])

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
        if self.report_type == "Ordens de Produção":
            self.generate_production_orders_report()
        elif self.report_type == "Produção por Linha":
            self.generate_production_by_line_report()
        elif self.report_type == "Composição / Estrutura de Produto":
            self.generate_product_composition_report()
            
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

    def generate_production_orders_report(self):
        filters = {
            "id_de": self.filters["id_de"].text(),
            "id_ate": self.filters["id_ate"].text(),
            "produto_de": self.filters["produto_de"].text(),
            "produto_ate": self.filters["produto_ate"].text(),
            "status": self.filters["status"].text(),
            "periodo_de": self.filters["periodo_de"].text(),
            "periodo_ate": self.filters["periodo_ate"].text(),
        }
        
        db_manager = get_db_manager()
        orders = db_manager.get_production_orders(filters)
        
        self.table.setRowCount(len(orders))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Produto", "Status", "Data de Criação", "Quantidade"])
        
        for row, order in enumerate(orders):
            self.table.setItem(row, 0, QTableWidgetItem(str(order["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(order["produto"]))
            self.table.setItem(row, 2, QTableWidgetItem(order["status"]))
            self.table.setItem(row, 3, QTableWidgetItem(order["data_criacao"]))
            self.table.setItem(row, 4, QTableWidgetItem(str(order["quantidade"])))
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def generate_production_by_line_report(self):
        filters = {
            "linha_de": self.filters["linha_de"].text(),
            "linha_ate": self.filters["linha_ate"].text(),
            "periodo_de": self.filters["periodo_de"].text(),
            "periodo_ate": self.filters["periodo_ate"].text(),
        }
        
        db_manager = get_db_manager()
        production = db_manager.get_production_by_line(filters)
        
        self.table.setRowCount(len(production))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Linha de Produção", "Produto", "Quantidade Produzida"])
        
        for row, item in enumerate(production):
            self.table.setItem(row, 0, QTableWidgetItem(item["linha"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["produto"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["quantidade"])))
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def generate_product_composition_report(self):
        filters = {
            "produto_de": self.filters["produto_de"].text(),
            "produto_ate": self.filters["produto_ate"].text(),
        }
        
        db_manager = get_db_manager()
        composition = db_manager.get_product_composition(filters)
        
        self.table.setRowCount(len(composition))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Insumo", "Quantidade"])
        
        for row, item in enumerate(composition):
            self.table.setItem(row, 0, QTableWidgetItem(item["insumo"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["quantidade"])))
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def export_to_pdf(self):
        from app.reports.export import export_to_pdf
        
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            data.append([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            
        export_to_pdf("relatorio_producao.pdf", data, headers)

    def export_to_excel(self):
        from app.reports.export import export_to_excel
        
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            data.append([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            
        export_to_excel("relatorio_producao.xlsx", data, headers)
