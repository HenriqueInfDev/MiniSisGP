DEFAULTINPUT = {
    "border-radius": "6px",
    "padding": "6px 6px",
    "font-weight": "500",
    "border-color": "#B3B3B3"
}

def input_style(color):
    """Retorna QSS padrão para botões"""
    return f"""
    QLineEdit, QTextEdit {{
        border-radius: {color['border-radius']};
        padding: {color['padding']};
        font-weight: {color['font-weight']};
        font-size: 14px;
    }}
    """
def input_date_style(color):
    return f"""
    /* ===== INPUT DE DATA / DATA+HORA ===== */
    QDateEdit, QDateTimeEdit {{
        border: 1px solid {color['border-color']};
        border-radius: {color['border-radius']};
        padding: {color['padding']};
        font-weight: {color['font-weight']};
        font-size: 14px;
        background-color: white;
        color: #333333;
    }}

    QDateEdit:hover, QDateTimeEdit:hover {{
        border-color: #999999;
    }}

    QDateEdit:focus, QDateTimeEdit:focus {{
        border-color: #7A7A7A;
    }}

    /* ===== BOTÃO DO CALENDÁRIO ===== */
    QDateEdit::drop-down, QDateTimeEdit::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: right center;
        width: 30px;
        border-left: 1px solid {color['border-color']};
        background-color: #F5F5F5;
    }}

    QDateEdit::down-arrow, QDateTimeEdit::down-arrow {{
        image: url(app/styles/images/icons/calendar.svg);
        width: 14px;
        height: 14px;
    }}

    /* ===== CALENDÁRIO ===== */
    QCalendarWidget {{
        background-color: white;
        border: 1px solid {color['border-color']};
        border-radius: 8px;

        /* GARANTE ESPAÇO */
        min-width: 280px;
        min-height: 260px;
    }}

    /* ===== BARRA DE NAVEGAÇÃO (MÊS / ANO) ===== */
    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background-color: #F2F2F2;
        border-bottom: 1px solid #DDDDDD;
    }}

    /* Botões de navegação (setas e texto) */
    QCalendarWidget QToolButton {{
        color: #333333;
        font-weight: 600;
        background: transparent;
        padding: 6px 10px;
        margin: 2px;
    }}

    QCalendarWidget QToolButton:hover {{
        background-color: #E0E0E0;
        border-radius: 4px;
    }}

    /* REMOVE SETA DO DROPDOWN DO MÊS */
    QCalendarWidget QToolButton::menu-indicator {{
        image: none;
        width: 0px;
    }}

    /* ===== DIAS DA SEMANA ===== */
    QCalendarWidget QHeaderView::section {{
        background-color: #FAFAFA;
        color: #666666;
        padding: 6px;
        font-weight: 600;
        border: none;
    }}

    /* ===== GRADE ===== */
    QCalendarWidget QAbstractItemView {{
        gridline-color: #E6E6E6;
        selection-background-color: #198754;
        selection-color: white;
        outline: none;
        font-size: 13px;
    }}

    /* ===== DIAS ===== */
    QCalendarWidget QAbstractItemView::item {{
        background-color: white;
        color: #333333;

        /* 🔥 ISSO REMOVE OS "..." */
        min-width: 36px;
        min-height: 32px;

        padding: 6px;
        border-radius: 6px;
    }}

    QCalendarWidget QAbstractItemView::item:hover {{
        background-color: #EAEAEA;
    }}

    /* ===== DIAS FORA DO MÊS ===== */
    QCalendarWidget QAbstractItemView::item:disabled {{
        background-color: #F3F3F3;
        color: #B5B5B5;
    }}

    /* ===== DIA SELECIONADO ===== */
    QCalendarWidget QAbstractItemView::item:selected {{
        background-color: #198754;
        color: white;
        font-weight: 600;
    }}
    """

