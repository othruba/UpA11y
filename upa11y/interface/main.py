from __future__ import annotations

import sys

from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget

from upa11y.interface.settings import AppPreferences, ColorPalette, build_global_stylesheet
from upa11y.interface.views.home_page import HomePage
from upa11y.interface.views.main_window_shell import MainWindowShell


class UpA11yWindow(QMainWindow):
    def __init__(self, preferences: AppPreferences) -> None:
        super().__init__()
        self.preferences = preferences
        self.stack = QStackedWidget(self)
        self.home = HomePage(self.stack)
        self.shell = MainWindowShell(self.stack)

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.shell)
        self.setCentralWidget(self.stack)

        self.setWindowTitle(preferences.app_name)
        self.resize(preferences.default_width, preferences.default_height)
        self._connect_pages()
        self._create_menu()
        self.open_home()

    def _connect_pages(self) -> None:
        self.home.import_requested.connect(self.import_orientacoes)
        self.home.new_requested.connect(self.new_conjunto)
        self.home.about_requested.connect(self.show_about)
        self.shell.home_requested.connect(self.open_home)

    def _create_menu(self) -> None:
        menu = self.menuBar().addMenu("Telas")
        pages = (
            ("home", "Início", "Ctrl+1"),
            ("utils", "Utils", "Ctrl+2"),
            ("testes", "Testes", "Ctrl+3"),
            ("refatoracoes", "Refatorações", "Ctrl+4"),
            ("processar", "Processar", "Ctrl+5"),
            ("resultados", "Resultados", "Ctrl+6"),
        )

        for page, label, shortcut in pages:
            action = QAction(label, self)
            action.setShortcut(shortcut)
            action.triggered.connect(
                lambda _checked=False, page=page, label=label: self.open_page(page, label)
            )
            menu.addAction(action)

    def open_home(self) -> None:
        self.stack.setCurrentWidget(self.home)
        self.setWindowTitle(f"{self.preferences.app_name} - Início")

    def open_page(self, page: str, label: str) -> None:
        if page == "home":
            self.open_home()
            return

        self.stack.setCurrentWidget(self.shell)
        self.shell.show_page(page)
        self.setWindowTitle(f"{self.preferences.app_name} - {label}")

    def import_orientacoes(self) -> None:
        if self.shell._import_orientacoes():
            self.open_page("utils", "Utils")

    def new_conjunto(self) -> None:
        self.shell._new_conjunto()
        self.open_page("utils", "Utils")

    def show_about(self) -> None:
        QMessageBox.information(self, "Sobre", "[texto]")


class UpA11yApplication:
    def __init__(
        self,
        preferences: AppPreferences | None = None,
        palette: ColorPalette | None = None,
    ) -> None:
        self.preferences = preferences or AppPreferences()
        self.palette = palette or ColorPalette()
        self.qt_app = QApplication(sys.argv)
        self.window = UpA11yWindow(self.preferences)
        self._configure_application()

    def _configure_application(self) -> None:
        self.qt_app.setApplicationName(self.preferences.app_name)
        self.qt_app.setOrganizationName(self.preferences.organization_name)
        self.qt_app.setFont(QFont(self.preferences.base_font_family, self.preferences.base_font_size))
        self.qt_app.setStyleSheet(build_global_stylesheet(self.palette))

    def run(self) -> int:
        self.window.show()
        return self.qt_app.exec()


def main() -> int:
    app = UpA11yApplication()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
