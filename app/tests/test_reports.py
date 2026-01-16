
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.reports.ui.financial_reports import FinancialReportWindow
from app.reports.ui.production_reports import ProductionReportWindow
from app.reports.ui.stock_reports import StockReportWindow
from app.reports.export import export_to_pdf, export_to_excel

class TestReportGeneration(unittest.TestCase):

    def _create_mock_line_edit(self, text=""):
        mock = MagicMock()
        mock.text.return_value = text
        return mock

    def _create_mock_date_edit(self, date_str="2023-01-01"):
        mock = MagicMock()
        mock_date = MagicMock()
        mock_date.toString.return_value = date_str
        mock.date.return_value = mock_date
        return mock

    @patch('app.reports.ui.financial_reports.get_db_manager')
    def test_financial_report_data(self, mock_get_db_manager):
        with patch.object(FinancialReportWindow, '__init__', lambda s, r: None):
            mock_db_instance = MagicMock()
            mock_get_db_manager.return_value = mock_db_instance
            mock_db_instance.get_profit_by_product.return_value = [
                {"produto": "Test Product", "custo_unitario": 10, "preco_venda": 20, "quantidade_vendida": 5, "lucro_unitario": 10, "lucro_total": 50}
            ]

            window = FinancialReportWindow("Lucro por Produto")
            window.report_type = "Lucro por Produto"
            window.filters = {
                "produto_de": self._create_mock_line_edit(), "produto_ate": self._create_mock_line_edit(),
                "periodo_de": self._create_mock_date_edit(), "periodo_ate": self._create_mock_date_edit()
            }
            headers, data = window.generate_profit_by_product_report()

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0][0], "Test Product")
            self.assertEqual(len(headers), 6)

    @patch('app.reports.ui.production_reports.get_db_manager')
    def test_production_report_data(self, mock_get_db_manager):
        with patch.object(ProductionReportWindow, '__init__', lambda s, r: None):
            mock_db_instance = MagicMock()
            mock_get_db_manager.return_value = mock_db_instance
            mock_db_instance.get_production_orders.return_value = [
                {"id": 1, "produto": "Test Product", "status": "Completed", "data_criacao": "2023-01-01", "quantidade": 100}
            ]

            window = ProductionReportWindow("Ordens de Produção")
            window.report_type = "Ordens de Produção"
            window.filters = {
                "id_de": self._create_mock_line_edit(), "id_ate": self._create_mock_line_edit(),
                "produto_de": self._create_mock_line_edit(), "produto_ate": self._create_mock_line_edit(),
                "status": self._create_mock_line_edit(), "periodo_de": self._create_mock_date_edit(),
                "periodo_ate": self._create_mock_date_edit()
            }
            headers, data = window.generate_production_orders_report()

            self.assertEqual(len(data), 1)
            self.assertEqual('Test Product', data[0][1])
            self.assertEqual(len(headers), 5)

    @patch('app.reports.ui.stock_reports.get_db_manager')
    def test_stock_report_data(self, mock_get_db_manager):
        with patch.object(StockReportWindow, '__init__', lambda s, r: None):
            mock_db_instance = MagicMock()
            mock_get_db_manager.return_value = mock_db_instance
            mock_db_instance.get_current_stock.return_value = [
                {"DESCRICAO": "Test Item", "SALDO_ESTOQUE": 100, "CUSTO_MEDIO": 10}
            ]

            window = StockReportWindow("Estoque Atual")
            window.report_type = "Estoque Atual"
            headers, data = window.generate_current_stock_report()

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0][0], "Test Item")
            self.assertEqual(len(headers), 3)

    @patch('app.reports.export.SimpleDocTemplate')
    def test_pdf_export(self, mock_doc):
        headers = ["Header1", "Header2"]
        data = [["Data1", "Data2"]]

        export_to_pdf("test.pdf", data, headers)

        mock_doc.assert_called_once_with("test.pdf", pagesize=(612.0, 792.0))

    @patch('app.reports.export.Workbook')
    def test_excel_export(self, mock_workbook):
        headers = ["Header1", "Header2"]
        data = [["Data1", "Data2"]]

        export_to_excel("test.xlsx", data, headers)

        mock_workbook.assert_called_once()

    @patch('app.reports.ui.production_reports.get_db_manager')
    def test_production_by_period_report_data(self, mock_get_db_manager):
        with patch.object(ProductionReportWindow, '__init__', lambda s, r: None):
            mock_db_instance = MagicMock()
            mock_get_db_manager.return_value = mock_db_instance
            mock_db_instance.get_production_by_period.return_value = [
                {"produto": "Test Product", "quantidade_produzida": 100, "data_producao": "2023-01-01"}
            ]

            window = ProductionReportWindow("Produção por Período")
            window.report_type = "Produção por Período"
            window.filters = {
                "periodo_de": self._create_mock_date_edit(), "periodo_ate": self._create_mock_date_edit()
            }
            headers, data = window.generate_production_by_period_report()

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0][0], "Test Product")
            self.assertEqual(len(headers), 3)

    @patch('app.reports.ui.stock_reports.get_db_manager')
    def test_entry_items_report_data(self, mock_get_db_manager):
        with patch.object(StockReportWindow, '__init__', lambda s, r: None):
            mock_db_instance = MagicMock()
            mock_get_db_manager.return_value = mock_db_instance
            mock_db_instance.get_entry_items_report.return_value = [
                {"nota": 1, "insumo": "Test Material", "quantidade": 10, "valor_unitario": 5, "valor_total": 50}
            ]

            window = StockReportWindow("Itens da Nota de Entrada")
            window.report_type = "Itens da Nota de Entrada"
            window.filters = {
                "nota_de": self._create_mock_line_edit(), "nota_ate": self._create_mock_line_edit()
            }
            headers, data = window.generate_entry_items_report()

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0][1], "Test Material")
            self.assertEqual(len(headers), 5)

    @patch('app.reports.ui.financial_reports.get_db_manager')
    def test_product_cost_report_data(self, mock_get_db_manager):
        with patch.object(FinancialReportWindow, '__init__', lambda s, r: None):
            mock_db_instance = MagicMock()
            mock_get_db_manager.return_value = mock_db_instance
            mock_db_instance.get_product_cost_report.return_value = [
                {"produto": "Test Product", "custo_medio": 10}
            ]

            window = FinancialReportWindow("Custo do Produto")
            window.report_type = "Custo do Produto"
            window.filters = {
                "produto_de": self._create_mock_line_edit(), "produto_ate": self._create_mock_line_edit()
            }
            headers, data = window.generate_product_cost_report()

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0][0], "Test Product")
            self.assertEqual(len(headers), 2)

if __name__ == '__main__':
    unittest.main()
