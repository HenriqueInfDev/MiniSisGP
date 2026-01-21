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
        padding-right: 26px;
        font-weight: {color['font-weight']};
    }}
    """