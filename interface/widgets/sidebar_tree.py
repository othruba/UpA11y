from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from PyQt6.QtGui import QColor, QFont, QBrush
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget


class SidebarTreeWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebarRoot")

        self.tree = QTreeWidget(self)
        self.tree.setObjectName("sidebarTree")
        self.tree.setHeaderHidden(True)
        self.tree.setUniformRowHeights(True)
        self.tree.setIndentation(18)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tree)

    def set_data(self, tree_data: Mapping[str, Any]) -> None:
        self.tree.clear()
        for root_label, root_value in tree_data.items():
            root_item = QTreeWidgetItem([root_label])
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
            item.setBackground(0, QBrush(QColor("#115c22")))
            return

        item.setForeground(0, QBrush(QColor("#d7ddda")))