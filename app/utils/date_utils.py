# app/utils/date_utils.py
from PySide6.QtCore import QDate, QDateTime

BRAZILIAN_DATE_FORMAT = "dd-MM-yyyy"
DB_DATE_FORMAT = "yyyy-MM-dd"
DB_DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"

def format_date_for_display(date_str):
    """Converts a date string from DB format (yyyy-MM-dd) to Brazilian format (dd-MM-yyyy)."""
    if not date_str:
        return ""
    try:
        # First, try to parse it as a full datetime
        dt = QDateTime.fromString(date_str, DB_DATETIME_FORMAT)
        if dt.isValid():
            return dt.toString(BRAZILIAN_DATE_FORMAT)
        
        # If not, try to parse it as just a date
        d = QDate.fromString(date_str, DB_DATE_FORMAT)
        if d.isValid():
            return d.toString(BRAZILIAN_DATE_FORMAT)
            
        return date_str # Return original if parsing fails
    except (TypeError, ValueError):
        return date_str


def format_qdate_for_db(qdate_obj):
    """Converts a QDate object to DB format string (yyyy-MM-dd)."""
    if not isinstance(qdate_obj, QDate):
        return None
    return qdate_obj.toString(DB_DATE_FORMAT)

def format_qdatetime_for_db(qdatetime_obj):
    """Converts a QDateTime object to DB format string (yyyy-MM-dd HH:mm:ss)."""
    if not isinstance(qdatetime_obj, QDateTime):
        return None
    return qdatetime_obj.toString(DB_DATETIME_FORMAT)