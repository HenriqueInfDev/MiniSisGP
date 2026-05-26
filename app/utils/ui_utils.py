# app/utils/ui_utils.py
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from app.styles.buttons_styles import button_style, GREEN, RED, YELLOW, GRAY


def configure_table_columns(table_view, total_width=None, padding=36):
    """Configura larguras iniciais de colunas para exibir o cabeçalho completo.

    A largura mínima de cada coluna fica baseada no tamanho do texto do cabeçalho,
    e a largura total é distribuída proporcionalmente no espaço disponível.
    """
    model = table_view.model()
    if model is None or model.columnCount() == 0:
        return

    fm = QFontMetrics(table_view.font())
    header = table_view.horizontalHeader()
    column_count = model.columnCount()
    min_widths = []
    for column in range(column_count):
        header_label = model.headerData(column, Qt.Horizontal) or ""
        label_width = fm.horizontalAdvance(str(header_label))
        min_widths.append(max(label_width + padding, header.minimumSectionSize()))

    if total_width is None or total_width <= 0:
        total_width = max(table_view.viewport().width(), table_view.width())

    total_width = max(total_width, sum(min_widths))
    total_min = sum(min_widths)
    widths = []

    if total_min == 0:
        widths = [max(100, total_width // column_count)] * column_count
    else:
        for min_width in min_widths:
            widths.append(max(min_width, int(total_width * min_width / total_min)))

    for index, width in enumerate(widths):
        table_view.setColumnWidth(index, width)


def show_warning_message(parent, title, message):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    ok_button = msg_box.addButton("OK", QMessageBox.AcceptRole)
    ok_button.setStyleSheet(button_style(YELLOW))
    msg_box.exec()

def show_error_message(parent, title, message):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    ok_button = msg_box.addButton("OK", QMessageBox.AcceptRole)
    ok_button.setStyleSheet(button_style(RED))
    msg_box.exec()

def show_success_message(parent, title, message):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    ok_button = msg_box.addButton("OK", QMessageBox.AcceptRole)
    ok_button.setStyleSheet(button_style(GREEN))
    msg_box.exec()

def show_confirmation_message(parent, title, message):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    
    yes_button = msg_box.addButton("Sim", QMessageBox.YesRole)
    no_button = msg_box.addButton("Não", QMessageBox.NoRole)
    
    yes_button.setStyleSheet(button_style(GREEN))
    no_button.setStyleSheet(button_style(RED))
    
    msg_box.exec()
    
    if msg_box.clickedButton() == yes_button:
        return QMessageBox.Yes
    return QMessageBox.No

def show_custom_confirmation(parent, title, message, buttons_config):
    """
    buttons_config: list of dicts {'text': '...', 'role': ..., 'style': ..., 'result': ...}
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    
    button_widgets = {}
    for cfg in buttons_config:
        btn = msg_box.addButton(cfg['text'], cfg['role'])
        btn.setStyleSheet(button_style(cfg['style']))
        button_widgets[btn] = cfg['result']
        
    msg_box.exec()
    return button_widgets.get(msg_box.clickedButton())

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
