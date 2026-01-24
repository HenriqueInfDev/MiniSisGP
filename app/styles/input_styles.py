DEFAULTINPUT = {
    "border-radius": "6px",
    "padding": "6px 6px",
    "font-weight": "500"
}

def input_style(color):
    """Retorna QSS padrão para botões"""
    return f"""
    QLineEdit, QTextEdit {{
        border-radius: {color['border-radius']};
        padding: {color['padding']};
        font-weight: {color['font-weight']};
    }}
    """

def doublespinbox_style(color):
    return f"""
    QDoubleSpinBox {{
        border-radius: {color['border-radius']};
        padding: {color['padding']};
        font-weight: {color['font-weight']};
        padding-right: 20px; /* espaço para os botões */
    }}

    /* Caixa dos botões */
    QDoubleSpinBox::up-button,
    QDoubleSpinBox::down-button {{
        background: transparent;
        border: none;
        width: 16px;
    }}

    /* Botão de subir */
    QDoubleSpinBox::up-button {{
        subcontrol-origin: border;
        subcontrol-position: top right;
    }}

    /* Botão de descer */
    QDoubleSpinBox::down-button {{
        subcontrol-origin: border;
        subcontrol-position: bottom right;
    }}

    /* Seta de subir */
    QDoubleSpinBox::up-arrow {{
        image: url(app/styles/images/icons/doublespin-up-arrow.svg);
        width: 10px;
        height: 10px;
    }}

    /* Seta de descer */
    QDoubleSpinBox::down-arrow {{
        image: url(app/styles/images/icons/doublespin-down-arrow.svg);
        width: 10px;
        height: 10px;
    }}

    /* Hover opcional */
    QDoubleSpinBox::up-button:hover,
    QDoubleSpinBox::down-button:hover {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    """
