# app/utils/ui_utils.py
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QPushButton
from PySide6.QtCore import Qt
from app.styles.buttons_styles import button_style, GREEN, RED, YELLOW, GRAY

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
