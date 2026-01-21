# ===== PALETA =====

GREEN = {
    "default": "#198754",
    "hover": "#157347",
    "pressed": "#146c43",
    "disabled": "#8fd3b0",
    "text": "white"
}

BLUE = {
    "default": "#0d6efd",
    "hover": "#0b5ed7",
    "pressed": "#0a58ca",
    "disabled": "#9ec5fe",
    "text": "white"
}

GRAY = {
    "default": "#6c757d",
    "hover": "#5c636a",
    "pressed": "#565e64",
    "disabled": "#ced4da",
    "text": "white"
}

RED = {
    "default": "#dc3545",
    "hover": "#bb2d3b",
    "pressed": "#b02a37",
    "disabled": "#f1aeb5",
    "text": "white"
}

YELLOW = {
    "default": "#ffc107",
    "hover": "#e0a800",
    "pressed": "#d39e00",
    "disabled": "#ffe69c",
    "text": "#212529"   # 👈 TEXTO ESCURO
}

# ===== FUNÇÕES DE ESTILO =====

def button_style(color):
    """Retorna QSS padrão para botões"""
    return f"""
    QPushButton {{
        background-color: {color['default']};
        color: {color.get('text', 'white')};
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background-color: {color['hover']};
    }}

    QPushButton:pressed {{
        background-color: {color['pressed']};
    }}

    QPushButton:disabled {{
        background-color: {color['disabled']};
        color: #adb5bd;
    }}
    """
