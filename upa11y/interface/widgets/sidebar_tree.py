from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QBrush
from PyQt6.QtWidgets import QLabel, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
import qtawesome as qta


class SidebarTreeWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebarRoot")

        self.title = QLabel("Conjunto ativo")
        self.title.setObjectName("sidebarTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.tree = QTreeWidget(self)
        self.tree.setObjectName("sidebarTree")
        self.tree.setHeaderHidden(True)
        self.tree.setUniformRowHeights(True)
        self.tree.setIndentation(18)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(self.title)
        layout.addWidget(self.tree)

    def set_data(self, tree_data: Mapping[str, Any]) -> None:
        self.tree.clear()
        root_label, root_value = next(iter(tree_data.items()))
        self.title.setText(f"Conjunto ativo: {root_label}")
        self._populate_roots(root_value)

    def _populate_roots(self, tree_data: Mapping[str, Any]) -> None:
        for root_label, root_value in tree_data.items():
            root_item = QTreeWidgetItem([str(root_label)])
            self._style_item(root_item, depth=0)
            self.tree.addTopLevelItem(root_item)
            self._populate_item(root_item, root_value, depth=1)

        self.tree.expandToDepth(2)

    def _populate_item(self, parent: QTreeWidgetItem, node_value: Any, *, depth: int) -> None:
        if isinstance(node_value, Mapping):
            for label, child in node_value.items():
                child_item = QTreeWidgetItem([str(label)])
                self._style_item(child_item, depth=depth)
                parent.addChild(child_item)
                self._populate_item(child_item, child, depth=depth + 1)
            return

        if node_value is not None:
            leaf_item = QTreeWidgetItem([str(node_value)])
            self._style_item(leaf_item, depth=depth)
            parent.addChild(leaf_item)

    def _style_item(self, item: QTreeWidgetItem, *, depth: int) -> None:
        if depth == 0:
            font = QFont()
            font.setBold(True)
            font.setPointSize(11)
            item.setFont(0, font)
            item.setForeground(0, QBrush(QColor("#f3f5f4")))
            self._make_checkable_when_numbered(item)
            return

        label = item.text(0)
        if depth == 1 and label == "teste.py":
            item.setIcon(0, qta.icon("fa5s.file-code", color="#f3f5f4"))

        if depth == 1 and label == "refatoracoes":
            item.setIcon(0, qta.icon("fa5s.code-branch", color="#f3f5f4"))

        if depth == 2:
            self._make_checkable_when_numbered(item)

        item.setForeground(0, QBrush(QColor("#d7ddda")))

    @staticmethod
    def _make_checkable_when_numbered(item: QTreeWidgetItem) -> None:
        number = item.text(0).split(".", 1)[0]
        if not number.isdigit():
            return

        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(0, Qt.CheckState.Checked)
