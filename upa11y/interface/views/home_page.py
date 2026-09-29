from __future__ import annotations

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
import qtawesome as qta


class HomePage(QWidget):
    import_requested = pyqtSignal()
    new_requested = pyqtSignal()
    about_requested = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("homePage")
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        layout.addStretch(1)

        logo = QLabel("UpA11y")
        logo.setObjectName("homeLogo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        actions = QHBoxLayout()
        actions.setSpacing(12)
        actions.addStretch(1)
        actions.addWidget(self._button("Importar orientações", "fa5s.file-import", self.import_requested.emit))
        actions.addWidget(self._button("Novo conjunto", "fa5s.plus", self.new_requested.emit))
        actions.addWidget(self._button("Sobre", "fa5s.info-circle", self.about_requested.emit))
        actions.addStretch(1)
        layout.addLayout(actions)

        layout.addStretch(1)

    def _button(self, text: str, icon_name: str, callback) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("actionTile")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setMinimumSize(190, 92)
        button.setIcon(qta.icon(icon_name, color="#f3f5f4"))
        button.setIconSize(QSize(24, 24))
        button.clicked.connect(callback)
        return button
