from __future__ import annotations

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

import qtawesome as qta



class TopBar(QWidget):
    home_click = pyqtSignal()
    nova_orientacao_click = pyqtSignal()
    configurar_refatoracao_click = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("topBar")
        self._buttons: dict[str, QPushButton] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        title = QLabel("UpA11y")
        title.setObjectName("topBarTitle")

        home_button = self._create_button("Tela Inicial", icon_name="fa5s.home")
        nova_orientacao_button = self._create_button("Nova Orientação", icon_name="fa5s.plus")
        configurar_refatoracao_button = self._create_button("Configurar Refatoração", icon_name="fa5s.sliders-h",)

        self._buttons = {
            "home": home_button,
            "new_orientacao": nova_orientacao_button,
            "configurar_refatoracao": configurar_refatoracao_button,
        }

        home_button.clicked.connect(self.home_click.emit)
        nova_orientacao_button.clicked.connect(self.nova_orientacao_click.emit)
        configurar_refatoracao_button.clicked.connect(self.configurar_refatoracao_click.emit)

        layout.addWidget(title)
        layout.addSpacing(16)
        layout.addWidget(home_button)
        layout.addWidget(nova_orientacao_button)
        layout.addWidget(configurar_refatoracao_button)
        layout.addStretch(1)

        self.set_active("home")

    def _create_button(self, text: str, *, icon_name: str | None = None) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("topBarButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        if icon_name and qta:
            button.setIcon(qta.icon(icon_name, color="#b9c1bc"))
            button.setIconSize(QSize(14, 14))

        return button

    def set_active(self, key: str) -> None:
        for button_key, button in self._buttons.items():
            is_active = button_key == key
            button.setProperty("active", "true" if is_active else "false")
            if qta and not button.icon().isNull():
                icon_color = "#f3f5f4" if is_active else "#b9c1bc"
                icon_name = self._icon_name_for(button_key)
                if icon_name:
                    button.setIcon(qta.icon(icon_name, color=icon_color))
            button.style().unpolish(button)
            button.style().polish(button)

    @staticmethod
    def _icon_name_for(key: str) -> str | None:
        icon_map = {
            "home": "fa5s.home",
            "nova_orientacao": "fa5s.plus",
            "configurar_orientacao": "fa5s.sliders-h",
        }
        return icon_map.get(key)