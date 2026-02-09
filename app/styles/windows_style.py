# ======================================================
# PALETA – TEMA CLARO
# ======================================================

LIGHT = {
    "background": "#F2F2F2",
    "background-menu": "#EBEBEB",
    "surface": "#FFFFFF",
    "border": "#B3B3B3",
    "text-color": "#1F1F1F",
    "text-muted": "#5F6368",
    "hover": "#E6E6E6",
    "focus": "#B0B0B0",
}


# ======================================================
# WINDOW STYLE
# ======================================================

def window_style(color):
    return f"""
    /* ==================================================
       BASE
       ================================================== */

    QWidget {{
        background-color: {color['background']};
        color: {color['text-color']};
        font-family: "Segoe UI", "Inter", "Arial";
    }}

    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QDateEdit,
    QDateTimeEdit,
    QTextEdit,
    QTableWidget,
    QTableView,
    QMenuBar,
    QMenu,
    QGroupBox,
    QTabBar::tab,
    QHeaderView::section {{
        font-size: 14px;
    }}

    /* ==================================================
       MAIN WINDOW
       ================================================== */

    QMainWindow {{
        background-color: {color['background']};
    }}

    /* ==================================================
       LABELS
       ================================================== */

    QLabel {{
        color: {color['text-color']};
        font-weight: 700;
        background-color: transparent;
    }}

    /* ==================================================
       MENU BAR / MENU
       ================================================== */

    QMenuBar {{
        background-color: {color['background-menu']};
        color: {color['text-color']};
    }}

    QMenuBar::item:selected {{
        background-color: {color['hover']};
    }}

    QMenu {{
        background-color: {color['surface']};
        color: {color['text-color']};
        border: 1px solid {color['border']};
    }}

    QMenu::item {{
        padding: 3px 20px 3px 10px;
    }}

    QMenu::item:selected {{
        background-color: {color['hover']};
    }}

    /* ==================================================
       GROUP BOX
       ================================================== */

    QGroupBox {{
        border: 1px solid {color['border']};
        border-radius: 6px;
        margin-top: 12px;
        padding: 10px;
        background-color: {color['surface']};
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        color: {color['text-color']};
        font-weight: 500;
    }}

    /* ==================================================
       INPUTS
       ================================================== */

    QLineEdit,
    QDoubleSpinBox,
    QTextEdit,
    QDateEdit,
    QDateTimeEdit {{
        background-color: {color['surface']};
        border: 1px solid {color['border']};
        border-radius: 4px;
    }}

    QLineEdit:focus,
    QDoubleSpinBox:focus,
    QTextEdit:focus,
    QDateEdit:focus,
    QDateTimeEdit:focus {{
        border-color: {color['focus']};
    }}

    QFormLayout QLabel {{
        padding-right: 8px;
        color: {color['text-muted']};
    }}

    /* ==================================================
       TABS
       ================================================== */

    QTabWidget::pane {{
        border: 1px solid {color['border']};
        background: {color['surface']};
    }}

    QTabWidget::pane QWidget {{
        background-color: #FFFFFF;
    }}

    QTabBar::tab {{
        background: {color['background-menu']};
        padding: 6px 14px;
        border: 1px solid {color['border']};
        border-bottom: none;
    }}

    QTabBar::tab:selected {{
        background: {color['surface']};
        font-weight: 500;
    }}

    QTabBar::tab:!selected {{
        margin-top: 2px;
    }}

    /* ==================================================
       TABLES (QTableView / QTableWidget)
       ================================================== */

    QTableView,
    QTableWidget {{
        background-color: {color['surface']};
        alternate-background-color: {color['background']};
        border: 1px solid {color['border']};
        gridline-color: {color['border']};
        outline: 0;
    }}

    /* Itens (inclui borda esquerda) */
    QTableView::item,
    QTableWidget::item {{
        border-left: 1px solid {color['border']};
        border-bottom: 1px solid {color['border']};
        padding: 4px 6px;
        color: {color['text-color']};
    }}

    /* Remove hover azul padrão */
    QTableView::item:hover,
    QTableWidget::item:hover {{
        background-color: transparent;
    }}

    /* Seleção */
    QTableView::item:selected,
    QTableWidget::item:selected {{
        background-color: #D6D6D6;
        color: {color['text-color']};
    }}

    /* Seleção sem foco */
    QTableView::item:selected:!active,
    QTableWidget::item:selected:!active {{
        background-color: #D6D6D6;
    }}

    /* Cabeçalho */
    QHeaderView::section {{
        background-color: {color['background-menu']};
        padding: 4px 6px;
        border: 1px solid {color['border']};
        font-weight: 500;
    }}

    /* Canto superior esquerdo da tabela */
    QTableCornerButton::section {{
        background-color: {color['background-menu']};
        border: 1px solid {color['border']};
    }}
    """
