DEFAULT = {
    "border-radius": "6px",
    "padding": "6px 6px",
    "font-weight": "500"
}

def input_style(color):
    """Retorna QSS padrão para botões"""
    return f"""
    QLineEdit {{
        border-radius: {color['border-radius']};
        padding: {color['padding']};
        font-weight: {color['font-weight']};
    }}
    """