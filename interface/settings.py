from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ColorPalette:
    background: str = "#2b2f30"
    background_gradient: str = "#242728"
    surface: str = "#353a3c"
    surface_hover: str = "#41474a"
    text_primary: str = "#f3f5f4"
    text_secondary: str = "#b9c1bc"
    accent: str = "#115c22"
    accent_hover: str = "#14722a"
    accent_pressed: str = "#0d481b"
    border: str = "#4b5255"


@dataclass(frozen=True, slots=True)
class AppPreferences:
    app_name: str = "UpA11y Interface"
    organization_name: str = "UpA11y"
    default_width: int = 1280
    default_height: int = 800
    base_font_family: str = "Noto Sans"
    base_font_size: int = 11


def build_global_stylesheet(colors: ColorPalette) -> str:
    return f"""
    QMainWindow {{
        background-color: {colors.background};
    }}
    QWidget#homeRoot {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 {colors.background},
            stop: 1 {colors.background_gradient}
        );
    }}
    QLabel#brandLabel {{
        color: {colors.text_primary};
        font-size: 64px;
        font-weight: 800;
        letter-spacing: 1px;
    }}
    QLabel#accentLabel {{
        color: {colors.accent};
        font-size: 64px;
        font-weight: 800;
    }}
    QLabel#taglineLabel {{
        color: {colors.text_secondary};
        font-size: 15px;
        font-weight: 500;
    }}
    QPushButton#menuButton {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: 12px;
        padding: 14px 20px;
        text-align: left;
        font-size: 15px;
        font-weight: 600;
    }}
    QPushButton#menuButton:hover {{
        background-color: {colors.surface_hover};
    }}
    QPushButton#menuButton:pressed {{
        background-color: {colors.background_gradient};
    }}
    QPushButton#menuButton[variant="accent"] {{
        background-color: {colors.accent};
        border-color: {colors.accent};
    }}
    QPushButton#menuButton[variant="accent"]:hover {{
        background-color: {colors.accent_hover};
        border-color: {colors.accent_hover};
    }}
    QPushButton#menuButton[variant="accent"]:pressed {{
        background-color: {colors.accent_pressed};
        border-color: {colors.accent_pressed};
    }}
    QWidget#topBar {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: 14px;
    }}
    QLabel#topBarTitle {{
        color: {colors.text_primary};
        font-size: 16px;
        font-weight: 700;
    }}
    QPushButton#topBarButton {{
        background-color: transparent;
        color: {colors.text_secondary};
        border: 1px solid transparent;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 13px;
        font-weight: 600;
    }}
    QPushButton#topBarButton:hover {{
        color: {colors.text_primary};
        background-color: {colors.surface_hover};
        border-color: {colors.border};
    }}
    QPushButton#topBarButton[active="true"] {{
        color: {colors.text_primary};
        background-color: {colors.accent};
        border-color: {colors.accent};
    }}
    QPushButton#topBarButton[active="true"]:hover {{
        background-color: {colors.accent_hover};
        border-color: {colors.accent_hover};
    }}
    QWidget#sidebarRoot {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: 12px;
    }}
    QTreeWidget#sidebarTree {{
        background-color: transparent;
        color: {colors.text_primary};
        border: none;
        padding: 8px;
        outline: none;
    }}
    QTreeWidget#sidebarTree::item {{
        min-height: 26px;
        border-radius: 8px;
        padding: 2px 6px;
    }}
    QTreeWidget#sidebarTree::item:selected {{
        background-color: {colors.accent_pressed};
        color: {colors.text_primary};
    }}
    QWidget#mainShellRoot {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 {colors.background},
            stop: 1 {colors.background_gradient}
        );
    }}
    QStackedWidget#contentStack {{
        background-color: transparent;
        border: none;
    }}
    QWidget#contentPage {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: 12px;
    }}
    QLabel#contentTitle {{
        color: {colors.text_primary};
        font-size: 26px;
        font-weight: 700;
    }}
    QLabel#contentDescription {{
        color: {colors.text_secondary};
        font-size: 14px;
        font-weight: 500;
    }}
    """