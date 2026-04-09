from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QStackedWidget, QVBoxLayout, QWidget

try:
    from interface.data import WCAG_BASIC_TREE
    from interface.widgets.sidebar_tree import SidebarTreeWidget
    from interface.widgets.top_bar import TopBar
except ModuleNotFoundError:
    from data import WCAG_BASIC_TREE
    from widgets.sidebar_tree import SidebarTreeWidget
    from widgets.top_bar import TopBar


class MainWindowShell(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainShellRoot")
        self._stack_pages: dict[str, int] = {}
        self._build_ui()
        self._connect_events()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.top_bar = TopBar(self)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)

        self.sidebar = SidebarTreeWidget(self)
        self.sidebar.setMinimumWidth(320)
        self.sidebar.setMaximumWidth(420)
        self.sidebar.set_data(WCAG_BASIC_TREE)

        self.content_stack = QStackedWidget(self)
        self.content_stack.setObjectName("contentStack")

        self._add_page(
            key="home",
            title="Tela Inicial",
            description="Tela Inicial",
        )
        self._add_page(
            key="nova_orientacao",
            title="Nova Orientação",
            description="Nova Orientação",
        )
        self._add_page(
            key="configurar_refatoracao",
            title="Configurar Refatoração",
            description="Configurar Refatoração",
        )

        content_layout.addWidget(self.sidebar, 3)
        content_layout.addWidget(self.content_stack, 7)

        layout.addWidget(self.top_bar)
        layout.addLayout(content_layout)

        self._show_page("home")

    def _connect_events(self) -> None:
        self.top_bar.home_click.connect(lambda: self._show_page("home"))
        self.top_bar.nova_orientacao_click.connect(lambda: self._show_page("nova_orientacao"))
        self.top_bar.configurar_refatoracao_click.connect(lambda: self._show_page("configurar_refatoracao"))

    def _add_page(self, *, key: str, title: str, description: str) -> None:
        page = QWidget(self)
        page.setObjectName("contentPage")

        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(28, 28, 28, 28)
        page_layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("contentTitle")

        description_label = QLabel(description)
        description_label.setObjectName("contentDescription")
        description_label.setWordWrap(True)

        page_layout.addWidget(title_label)
        page_layout.addWidget(description_label)
        page_layout.addStretch(1)
        page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        index = self.content_stack.addWidget(page)
        self._stack_pages[key] = index

    def _show_page(self, key: str) -> None:
        page_index = self._stack_pages.get(key)
        if page_index is None:
            return
        self.content_stack.setCurrentIndex(page_index)
        self.top_bar.set_active(key)