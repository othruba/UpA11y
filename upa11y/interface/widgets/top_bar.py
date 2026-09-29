from __future__ import annotations

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

import qtawesome as qta


class TopBar(QWidget):
    home_click = pyqtSignal()
    utils_click = pyqtSignal()
    testes_click = pyqtSignal()
    refatoracoes_click = pyqtSignal()
    processar_click = pyqtSignal()
    resultados_click = pyqtSignal()

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

        home_button = self._create_button("Início", icon_name="fa5s.home")
        utils_button = self._create_button("Utils", icon_name="fa5s.tools")
        testes_button = self._create_button("Testes", icon_name="fa5s.vial")
        refatoracoes_button = self._create_button("Refatorações", icon_name="fa5s.code-branch")
        processar_button = self._create_button("Processar", icon_name="fa5s.folder-open")
        resultados_button = self._create_button("Resultados", icon_name="fa5s.table")

        self._buttons = {
            "home": home_button,
            "utils": utils_button,
            "testes": testes_button,
            "refatoracoes": refatoracoes_button,
            "processar": processar_button,
            "resultados": resultados_button,
        }

        home_button.clicked.connect(self.home_click.emit)
        utils_button.clicked.connect(self.utils_click.emit)
        testes_button.clicked.connect(self.testes_click.emit)
        refatoracoes_button.clicked.connect(self.refatoracoes_click.emit)
        processar_button.clicked.connect(self.processar_click.emit)
        resultados_button.clicked.connect(self.resultados_click.emit)

        layout.addWidget(title)
        layout.addSpacing(16)
        layout.addWidget(home_button)
        layout.addWidget(utils_button)
        layout.addWidget(testes_button)
        layout.addWidget(refatoracoes_button)
        layout.addWidget(processar_button)
        layout.addWidget(resultados_button)
        layout.addStretch(1)

        self.set_active("home")

    def _create_button(self, text: str, *, icon_name: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("topBarButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setIcon(qta.icon(icon_name, color="#b9c1bc"))
        button.setIconSize(QSize(14, 14))
        return button

    def set_active(self, key: str) -> None:
        for button_key, button in self._buttons.items():
            is_active = button_key == key
            button.setProperty("active", "true" if is_active else "false")
            icon_color = "#f3f5f4" if is_active else "#b9c1bc"
            button.setIcon(qta.icon(self._icon_name_for(button_key), color=icon_color))
            button.style().unpolish(button)
            button.style().polish(button)

    @staticmethod
    def _icon_name_for(key: str) -> str:
        icon_map = {
            "home": "fa5s.home",
            "utils": "fa5s.tools",
            "testes": "fa5s.vial",
            "refatoracoes": "fa5s.code-branch",
            "processar": "fa5s.folder-open",
            "resultados": "fa5s.table",
        }
        return icon_map[key]
