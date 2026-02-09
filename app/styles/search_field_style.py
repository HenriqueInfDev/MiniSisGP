# ======================================================
# SEARCH FIELD / COMBOBOX
# ======================================================

DEFAULT = {
    "border-radius": "6px",
    "padding": "6px 8px",
    "font-weight": "500",
    "border-color": "#B3B3B3",
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
    }}

    QComboBox:hover {{
        border-color: #999999;
    }}

    QComboBox:focus {{
        border-color: #7A7A7A;
    }}

    /* ===== BOTÃO DROPDOWN ===== */
    QComboBox::drop-down {{
        background: transparent;
        border: none;
        width: 28px;
    }}

    QComboBox::down-arrow {{
        image: url(app/styles/images/icons/search_field_arrow_down.svg);
        width: 12px;
        height: 12px;
    }}

    /* ===== LISTA SUSPENSA ===== */
    QComboBox QAbstractItemView {{
        background-color: white;
        border: 1px solid #B3B3B3;
        selection-background-color: #E6F0FF;
        selection-color: #000000;
        outline: 0;
    }}

    /* Hover do mouse */
    QComboBox QAbstractItemView::item:hover {{
        background-color: #F0F4FF;
    }}

    /* Item selecionado */
    QComboBox QAbstractItemView::item:selected {{
        background-color: #DCE8FF;
        color: #000000;
    }}
    """
