# ======================================================
# SEARCH FIELD / COMBOBOX
# ======================================================

DEFAULT = {
    "border-radius": "14px",
    "padding": "10px 14px",
    "font-weight": "600",
    "border-color": "#D1D9E6",
}


def search_field_style(c):
    return f"""
    /* ===== COMBOBOX ===== */
    QComboBox {{
        padding: {c['padding']};
        font-weight: {c['font-weight']};
        border: 1px solid {c['border-color']};
        border-radius: {c['border-radius']};
        background-color: white;
        color: #0F172A;
    }}

    QComboBox:hover {{
        border-color: #A3BFFA;
    }}

    QComboBox:focus {{
        border-color: #2563EB;
    }}

    /* ===== BOTÃO DROPDOWN ===== */
    QComboBox::drop-down {{
        background: transparent;
        border: none;
        width: 34px;
    }}

    QComboBox::down-arrow {{
        image: url(app/styles/images/icons/search_field_arrow_down.svg);
        width: 14px;
        height: 14px;
    }}

    /* ===== LISTA SUSPENSA ===== */
    QComboBox QAbstractItemView {{
        background-color: white;
        border: 1px solid #D1D9E6;
        selection-background-color: #E8F0FF;
        selection-color: #0F172A;
        outline: 0;
    }}

    QComboBox QAbstractItemView::item:hover {{
        background-color: #EFF4FF;
    }}

    QComboBox QAbstractItemView::item:selected {{
        background-color: #DCE8FF;
        color: #0F172A;
    }}
    """
