from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ColorPalette:
    background: str = "#2b2f30"
    surface: str = "#353a3c"
    surface_hover: str = "#41474a"
    text_primary: str = "#f3f5f4"
    text_secondary: str = "#b9c1bc"
    accent: str = "#115c22"
    accent_hover: str = "#14722a"
    accent_pressed: str = "#0d481b"
    border: str = "#4b5255"


@dataclass
class AppPreferences:
    app_name: str = "UpA11y Interface"
    organization_name: str = "UpA11y"
    default_width: int = 1280
    default_height: int = 800
    base_font_family: str = "Noto Sans"
    base_font_size: int = 11


def build_global_stylesheet(colors: ColorPalette) -> str:
    return f"""
    QMainWindow,
    QWidget#mainShellRoot {{
        background-color: {colors.background};
    }}
    QWidget#topBar,
    QWidget#sidebarRoot,
    QWidget#summaryCard,
    QLabel#statusLabel {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: 8px;
    }}
    QLabel {{
        color: {colors.text_primary};
    }}
    QLabel#topBarTitle {{
        font-size: 16px;
        font-weight: 700;
    }}
    QLabel#homeLogo {{
        font-size: 72px;
        font-weight: 800;
    }}
    QLabel#sidebarTitle {{
        background-color: {colors.text_primary};
        color: #101312;
        border-radius: 6px;
        padding: 8px 10px;
        font-weight: 700;
    }}
    QLabel#contentTitle {{
        font-size: 26px;
        font-weight: 700;
    }}
    QLabel#contentDescription {{
        color: {colors.text_secondary};
        font-size: 14px;
    }}
    QLabel#sectionTitle {{
        font-size: 19px;
        font-weight: 800;
    }}
    QLabel#fieldLabel {{
        font-size: 16px;
        font-weight: 800;
    }}
    QLabel#statusLabel {{
        padding: 10px 12px;
        font-size: 14px;
        font-weight: 600;
    }}
    QStackedWidget#contentStack,
    QScrollArea#contentScroll,
    QScrollArea#contentScroll > QWidget > QWidget,
    QWidget#workspacePage {{
        background-color: transparent;
        border: none;
    }}
    QTreeWidget#sidebarTree {{
        background-color: transparent;
        color: {colors.text_primary};
        border: none;
        outline: none;
    }}
    QTreeWidget#sidebarTree::item {{
        min-height: 30px;
        border-radius: 8px;
        padding: 2px 6px;
    }}
    QTreeWidget#sidebarTree::item:selected {{
        background-color: {colors.accent_pressed};
    }}
    QLineEdit#formInput {{
        background-color: {colors.text_primary};
        color: #101312;
        border: 1px solid {colors.text_primary};
        border-radius: 6px;
        padding: 9px 10px;
        font-size: 15px;
    }}
    QPushButton#topBarButton,
    QPushButton#inlineButton,
    QPushButton#actionTile {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: 8px;
        font-weight: 700;
    }}
    QPushButton#topBarButton {{
        color: {colors.text_secondary};
        padding: 10px 14px;
        font-size: 13px;
    }}
    QPushButton#topBarButton[active="true"] {{
        color: {colors.text_primary};
        background-color: {colors.accent};
        border-color: {colors.accent};
    }}
    QPushButton#inlineButton {{
        padding: 9px 12px;
        font-size: 14px;
    }}
    QPushButton#actionTile {{
        padding: 18px 20px;
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {colors.surface_hover};
        border-color: {colors.accent};
    }}
    QPushButton#topBarButton[active="true"]:hover {{
        background-color: {colors.accent_hover};
    }}
    QPushButton:disabled {{
        color: {colors.text_secondary};
    }}
    QTableWidget#resultsTable {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: 8px;
        gridline-color: {colors.border};
        selection-background-color: {colors.accent_pressed};
    }}
    QTableWidget#resultsTable::item {{
        padding: 6px;
    }}
    QHeaderView::section {{
        background-color: {colors.background};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        padding: 8px;
        font-weight: 800;
    }}
    """
