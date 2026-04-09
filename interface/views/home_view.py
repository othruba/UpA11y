from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget

try:
    from interface.widgets.menu_button import MenuButton
except ModuleNotFoundError:
    from widgets.menu_button import MenuButton


class HomeView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("homeRoot")
        self._build_ui()

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(48, 48, 48, 48)

        root_layout.addStretch(1)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_layout.setSpacing(22)

        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(0)
        brand_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        brand_main = QLabel("Up")
        brand_main.setObjectName("brandLabel")
        brand_accent = QLabel("A11y")
        brand_accent.setObjectName("accentLabel")

        brand_layout.addWidget(brand_main)
        brand_layout.addWidget(brand_accent)

        tagline = QLabel("Refatoração de interfaces para acessibilidade")
        tagline.setObjectName("taglineLabel")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_container = QVBoxLayout()
        button_container.setSpacing(12)
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        new_set_button = MenuButton("Novo Conjunto", variant="accent", icon_name="fa5s.plus-circle")
        load_set_button = MenuButton("Carregar Conjunto", icon_name="fa5s.folder-open")
        about_button = MenuButton("Sobre", icon_name="fa5s.info-circle")

        new_set_button.setFixedWidth(340)
        load_set_button.setFixedWidth(340)
        about_button.setFixedWidth(340)

        button_container.addWidget(new_set_button)
        button_container.addWidget(load_set_button)
        button_container.addWidget(about_button)

        center_layout.addLayout(brand_layout)
        center_layout.addWidget(tagline)
        center_layout.addSpacing(8)
        center_layout.addLayout(button_container)

        root_layout.addLayout(center_layout)
        root_layout.addStretch(1)