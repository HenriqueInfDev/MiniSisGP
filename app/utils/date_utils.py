# app/utils/date_utils.py
from datetime import datetime
from PySide6.QtCore import QDate, QDateTime

# --- Constantes de Formato ---
DB_DATE_FORMAT = "yyyy-MM-dd"
DB_DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
BR_DATE_FORMAT = "dd/MM/yyyy"
BR_DATETIME_FORMAT = "dd/MM/yyyy HH:mm:ss"

# --- Funções de Formatação para Display ---

def format_date_for_display(date_str):
    """Converte uma data string (YYYY-MM-DD) para o formato brasileiro (DD/MM/YYYY)."""
    if not date_str:
        return ""
    try:
        # Tenta converter de QDate se for o caso
        if isinstance(date_str, QDate):
            return date_str.toString(BR_DATE_FORMAT)
        # Tenta converter de string
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return date_str # Retorna o original se a conversão falhar

def format_datetime_for_display(datetime_str):
    """Converte uma string de data/hora (YYYY-MM-DD HH:mm:ss) para o formato brasileiro."""
    if not datetime_str:
        return ""
    try:
        # Tenta converter de QDateTime
        if isinstance(datetime_str, QDateTime):
            return datetime_str.toString(BR_DATETIME_FORMAT)
        # Tenta converter de string
        dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    except (ValueError, TypeError):
        return datetime_str

# --- Funções de Parsing para Banco de Dados ---

def parse_date_for_db(qdate_obj):
    """Converte um objeto QDate do PySide6 para uma string (YYYY-MM-DD)."""
    if not isinstance(qdate_obj, QDate):
        return None
    return qdate_obj.toString(DB_DATE_FORMAT)

def parse_datetime_for_db(qdatetime_obj):
    """Converte um objeto QDateTime do PySide6 para uma string (YYYY-MM-DD HH:mm:ss)."""
    if not isinstance(qdatetime_obj, QDateTime):
        return None
    return qdatetime_obj.toString(DB_DATETIME_FORMAT)

# --- Funções de Conversão de String para QDate/QDateTime ---

def string_to_qdate(date_str_br):
    """Converte uma string de data no formato brasileiro (DD/MM/YYYY) para um objeto QDate."""
    if not date_str_br:
        return QDate.currentDate()
    try:
        return QDate.fromString(date_str_br, BR_DATE_FORMAT)
    except (ValueError, TypeError):
        return QDate.currentDate()

def string_to_qdatetime(datetime_str_br):
    """Converte uma string de data/hora no formato brasileiro para um objeto QDateTime."""
    if not datetime_str_br:
        return QDateTime.currentDateTime()
    try:
        return QDateTime.fromString(datetime_str_br, BR_DATETIME_FORMAT)
    except (ValueError, TypeError):
        return QDateTime.currentDateTime()

def db_string_to_qdate(date_str_db):
    """Converte uma string de data do banco de dados (YYYY-MM-DD) para um objeto QDate."""
    if not date_str_db:
        return QDate.currentDate()
    return QDate.fromString(date_str_db, DB_DATE_FORMAT)

def db_string_to_qdatetime(datetime_str_db):
    """Converte uma string de data/hora do banco de dados para um objeto QDateTime."""
    if not datetime_str_db:
        return QDateTime.currentDateTime()
    return QDateTime.fromString(datetime_str_db, DB_DATETIME_FORMAT)
