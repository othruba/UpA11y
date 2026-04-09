from __future__ import annotations

import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow

try:
    from interface.settings import AppPreferences, ColorPalette, build_global_stylesheet
    from interface.views.main_window_shell import MainWindowShell
except ModuleNotFoundError:
    from settings import AppPreferences, ColorPalette, build_global_stylesheet
    from views.main_window_shell import MainWindowShell


class PrototypeWindow(QMainWindow):
    def __init__(self, preferences: AppPreferences) -> None:
        super().__init__()
        self._preferences = preferences
        self._setup_window()

    def _setup_window(self) -> None:
        self.setWindowTitle(self._preferences.app_name)
        self.resize(self._preferences.default_width, self._preferences.default_height)
        self.setCentralWidget(MainWindowShell(self))


class PrototypeApplication:
    def __init__(
        self,
        preferences: AppPreferences | None = None,
        palette: ColorPalette | None = None,
    ) -> None:
        self._preferences = preferences or AppPreferences()
        self._palette = palette or ColorPalette()
        self._qt_app = QApplication(sys.argv)
        self._window = PrototypeWindow(self._preferences)
        self._configure_application()

    def _configure_application(self) -> None:
        self._qt_app.setApplicationName(self._preferences.app_name)
        self._qt_app.setOrganizationName(self._preferences.organization_name)
        self._qt_app.setFont(QFont(self._preferences.base_font_family, self._preferences.base_font_size))
        self._qt_app.setStyleSheet(build_global_stylesheet(self._palette))

    def run(self) -> int:
        self._window.show()
        return self._qt_app.exec()


def main() -> int:
    app = PrototypeApplication()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())