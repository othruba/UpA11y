from __future__ import annotations

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QPushButton
import qtawesome as qta



class MenuButton(QPushButton):
    def __init__(
        self,
        label: str,
        *,
        variant: str = "default",
        icon_name: str | None = None,
        parent=None,
    ) -> None:
        super().__init__(label, parent)
        self.setObjectName("menuButton")
        self.setProperty("variant", variant)
        self.setMinimumHeight(56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if icon_name and qta:
            self.setIcon(qta.icon(icon_name, color="#f3f5f4"))
            self.setIconSize(QSize(18, 18))