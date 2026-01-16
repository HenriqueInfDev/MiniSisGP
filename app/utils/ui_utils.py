# app/utils/ui_utils.py
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog
from PySide6.QtCore import Qt

def show_error_message(parent, title, message):
    QMessageBox.critical(parent, title, message)

def show_success_message(parent, title, message):
    QMessageBox.information(parent, title, message)

def show_confirmation_message(parent, title, message):
    return QMessageBox.question(parent, title, message, QMessageBox.Yes | QMessageBox.No)

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except (ValueError, TypeError):
            return super().__lt__(other)

def get_save_filename(parent, caption, filter):
    """
    Abre um diálogo para salvar arquivo.
    Retorna o caminho do arquivo selecionado e o filtro de tipo de arquivo.
    """
    filename, selected_filter = QFileDialog.getSaveFileName(parent, caption, filter=filter)
    return filename, selected_filter
