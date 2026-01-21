DEFAULT = {
    "border-radius": "6px",
    "padding": "6px 6px",
    "font-weight": "500"
}

def search_field_style(color):
    return f"""
    QComboBox {{
        border-radius: {color['border-radius']};
        padding: {color['padding']};
        font-weight: {color['font-weight']};
    }}
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
    """