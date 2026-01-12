
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from app.database.db import get_db_manager

class StockReportWindow(QWidget):
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

        if self.report_type == "Entrada de Insumos":
            self.filters["numero_de"] = QLineEdit()
            self.filters["numero_ate"] = QLineEdit()
            self.filters["fornecedor"] = QLineEdit()
            self.filters["data_inicial"] = QLineEdit()
            self.filters["data_final"] = QLineEdit()
            self.filters_layout.addRow("Número (de):", self.filters["numero_de"])
            self.filters_layout.addRow("Número (até):", self.filters["numero_ate"])
            self.filters_layout.addRow("Fornecedor:", self.filters["fornecedor"])
            self.filters_layout.addRow("Data Inicial:", self.filters["data_inicial"])
            self.filters_layout.addRow("Data Final:", self.filters["data_final"])
        elif self.report_type == "Movimentação de Estoque":
            self.filters["item_de"] = QLineEdit()
            self.filters["item_ate"] = QLineEdit()
            self.filters["periodo_de"] = QLineEdit()
            self.filters["periodo_ate"] = QLineEdit()
            self.filters_layout.addRow("Item (de):", self.filters["item_de"])
            self.filters_layout.addRow("Item (até):", self.filters["item_ate"])
            self.filters_layout.addRow("Período (de):", self.filters["periodo_de"])
            self.filters_layout.addRow("Período (até):", self.filters["periodo_ate"])
        elif self.report_type == "Estoque Atual":
            pass # No filters for this report

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
        if self.report_type == "Entrada de Insumos":
            self.generate_input_supplies_report()
        elif self.report_type == "Movimentação de Estoque":
            self.generate_stock_movement_report()
        elif self.report_type == "Estoque Atual":
            self.generate_current_stock_report()
        
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

    def generate_input_supplies_report(self):
        filters = {
            "numero_de": self.filters["numero_de"].text(),
            "numero_ate": self.filters["numero_ate"].text(),
            "fornecedor": self.filters["fornecedor"].text(),
            "data_inicial": self.filters["data_inicial"].text(),
            "data_final": self.filters["data_final"].text(),
        }
        
        db_manager = get_db_manager()
        entries = db_manager.get_stock_entries(filters)
        
        self.table.setRowCount(len(entries))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Número", "Fornecedor", "Data", "Total"])
        
        for row, entry in enumerate(entries):
            self.table.setItem(row, 0, QTableWidgetItem(str(entry["numero"])))
            self.table.setItem(row, 1, QTableWidgetItem(entry["fornecedor"]))
            self.table.setItem(row, 2, QTableWidgetItem(entry["data"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(entry["total"])))
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def generate_stock_movement_report(self):
        filters = {
            "item_de": self.filters["item_de"].text(),
            "item_ate": self.filters["item_ate"].text(),
            "periodo_de": self.filters["periodo_de"].text(),
            "periodo_ate": self.filters["periodo_ate"].text(),
        }
        
        db_manager = get_db_manager()
        movements = db_manager.get_stock_movements(filters)
        
        self.table.setRowCount(len(movements))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Item", "Tipo de Movimento", "Quantidade", "Valor Unitário", "Data"])
        
        for row, movement in enumerate(movements):
            self.table.setItem(row, 0, QTableWidgetItem(movement["item"]))
            self.table.setItem(row, 1, QTableWidgetItem(movement["tipo_movimento"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(movement["quantidade"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(movement["valor_unitario"])))
            self.table.setItem(row, 4, QTableWidgetItem(movement["data_movimento"]))
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def generate_current_stock_report(self):
        db_manager = get_db_manager()
        stock = db_manager.get_current_stock()
        
        self.table.setRowCount(len(stock))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Item", "Saldo em Estoque", "Custo Médio"])
        
        for row, item in enumerate(stock):
            self.table.setItem(row, 0, QTableWidgetItem(item["descricao"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["saldo_estoque"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["custo_medio"])))
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def export_to_pdf(self):
        from app.reports.export import export_to_pdf
        
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            data.append([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            
        export_to_pdf("relatorio_estoque.pdf", data, headers)

    def export_to_excel(self):
        from app.reports.export import export_to_excel
        
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            data.append([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            
        export_to_excel("relatorio_estoque.xlsx", data, headers)
