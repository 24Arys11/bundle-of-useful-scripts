"""wizard.py — PySide6 WizardApp (QMainWindow) entry point.

Module responsibilities:
  wizard_state.py   — WizardState dataclass + constants          (unchanged)
  wizard_prompt.py  — Prompt assembly + export helpers           (unchanged)
  wizard_widgets.py — PromptSidebar, CognitiveWidget
  wizard_screens.py — All QWizardPage classes + PromptWizard
  wizard.py         — WizardApp (QMainWindow), dark QSS, entry point
"""
from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from wizard_state import WizardState
from wizard_screens import PromptWizard
from wizard_widgets import PromptSidebar

# Resolve the checkmark SVG absolute path (forward slashes for QSS url())
_CHECK_SVG = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "check.svg"
).replace("\\", "/")


# ─────────────────────────────────────────────────────────────────────────────
# Dark stylesheet  (VS Code-inspired)
# ─────────────────────────────────────────────────────────────────────────────

_DARK_QSS = """
/* ── Base ────────────────────────────────────────────────────── */

QMainWindow, QWidget, QWizard, QWizardPage {
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: "Segoe UI", "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}

QLabel {
    color: #d4d4d4;
}

QLabel#hint {
    color: #9d9d9d;
    font-size: 12px;
}

QLabel#error-label {
    color: #f44747;
    font-size: 12px;
}

QLabel#section-label {
    color: #569cd6;
    font-weight: bold;
}

QLabel#tick-label {
    color: #888;
    font-size: 11px;
}

QLabel#sidebar-title {
    color: #569cd6;
    font-weight: bold;
    font-size: 13px;
}

QLabel#welcome-body {
    color: #cccccc;
    font-size: 13px;
    line-height: 1.6;
}

/* ── Input widgets ───────────────────────────────────────────── */

QLineEdit, QPlainTextEdit, QTextEdit {
    background-color: #2d2d30;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 4px 6px;
    color: #d4d4d4;
    selection-background-color: #094771;
}

QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus {
    border-color: #569cd6;
}

QTextBrowser {
    background-color: #2d2d30;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 4px;
    color: #d4d4d4;
}

QTextBrowser#sidebar-browser {
    background-color: transparent;
    border: none;
}

QTextBrowser#cognitive-example {
    background-color: #2a2a2e;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 6px;
    color: #c5c5c5;
    font-style: italic;
}

/* ── Buttons ─────────────────────────────────────────────────── */

QPushButton {
    background-color: #3c3c3c;
    color: #d4d4d4;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 5px 16px;
    min-height: 26px;
}

QPushButton:hover {
    background-color: #4a4a4f;
    border-color: #569cd6;
}

QPushButton:pressed {
    background-color: #094771;
}

QPushButton#primary-btn {
    background-color: #0e639c;
    border-color: #0e639c;
    color: #ffffff;
    font-weight: bold;
}

QPushButton#primary-btn:hover {
    background-color: #1177bb;
}

QPushButton#skip-btn {
    color: #888;
    background-color: transparent;
    border-color: #555;
}

QPushButton#exit-btn {
    background-color: #922424;
    border-color: #922424;
    color: #ffffff;
}

QPushButton#exit-btn:hover {
    background-color: #b02c2c;
    border-color: #b02c2c;
}

QPushButton#start-over-btn {
    background-color: #7a5a18;
    border-color: #7a5a18;
    color: #ffffff;
}

QPushButton#start-over-btn:hover {
    background-color: #9a7020;
    border-color: #9a7020;
}

QPushButton#qt_wizard_commit_button2 {
    color: #888;
    background-color: transparent;
    border: 1px solid #555;
    padding: 3px 10px;
    min-height: 22px;
    font-size: 11px;
}

/* ── Lists ───────────────────────────────────────────────────── */

QListWidget#checklist {
    background-color: #252526;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
}

QListWidget#checklist::item {
    padding: 5px 4px;
    border-radius: 3px;
}

QListWidget#checklist::item:hover {
    background-color: #2a2d2e;
}

QListWidget#checklist::item:selected {
    background-color: transparent;
    color: #d4d4d4;
    outline: none;
}

QListWidget#checklist:focus {
    outline: none;
}

QListWidget#checklist::item:focus {
    outline: none;
    border: none;
}

/* ── Radio / Checkbox ────────────────────────────────────────── */

QRadioButton, QCheckBox {
    spacing: 8px;
    color: #d4d4d4;
    padding: 3px 0;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #888;
    background: #2d2d30;
}

QRadioButton::indicator:checked {
    background: #569cd6;
    border-color: #569cd6;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 2px solid #888;
    background: #2d2d30;
}

QCheckBox::indicator:checked {
    background: #569cd6;
    border-color: #569cd6;
    image: url({check_svg});
}

/* ── QListWidget checkboxes ──────────────────────────────────── */

QListWidget#checklist::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 2px solid #888;
    background-color: #2d2d30;
}

QListWidget#checklist::indicator:unchecked {
    border: 2px solid #888;
    background-color: #2d2d30;
}

QListWidget#checklist::indicator:checked {
    background-color: #569cd6;
    border: 2px solid #569cd6;
    image: url({check_svg});
}

/* ── GroupBox ────────────────────────────────────────────────── */

QGroupBox {
    border: 1px solid #3c3c3c;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 6px;
    color: #9d9d9d;
    font-size: 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    top: -1px;
    color: #9d9d9d;
}

/* ── Sliders ─────────────────────────────────────────────────── */

QSlider::groove:horizontal {
    height: 6px;
    background: #3c3c3c;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 18px;
    height: 18px;
    background: #569cd6;
    border-radius: 9px;
    margin: -6px 0;
}

QSlider::handle:horizontal:hover {
    background: #6baedd;
}

QSlider::sub-page:horizontal {
    background: #1177bb;
    border-radius: 3px;
}

/* ── Scrollbars ──────────────────────────────────────────────── */

QScrollBar:vertical {
    width: 10px;
    background: #1e1e1e;
    border: none;
}

QScrollBar::handle:vertical {
    background: #4a4a4f;
    border-radius: 5px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #6a6a6f;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    height: 10px;
    background: #1e1e1e;
    border: none;
}

QScrollBar::handle:horizontal {
    background: #4a4a4f;
    border-radius: 5px;
    min-width: 24px;
}

/* ── Sidebar panel ───────────────────────────────────────────── */

QFrame#sidebar-sep {
    color: #3c3c3c;
}

/* ── Wizard header area ──────────────────────────────────────── */

QWizard QLabel {
    color: #d4d4d4;
}

/* ── Dialog ──────────────────────────────────────────────────── */

QDialog {
    background-color: #252526;
}

QMessageBox {
    background-color: #252526;
}

/* ── Theme toggle button ─────────────────────────────────────── */

QToolButton#theme-toggle {
    background-color: transparent;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    color: #d4d4d4;
    padding: 5px 16px;
    min-height: 26px;
}

QToolButton#theme-toggle:hover {
    background-color: #2d2d30;
    border-color: #569cd6;
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Light stylesheet
# ─────────────────────────────────────────────────────────────────────────────

_LIGHT_QSS = """
QMainWindow, QWidget, QWizard, QWizardPage {
    background-color: #f5f5f5;
    color: #1e1e1e;
    font-family: "Segoe UI", "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}

QLabel { color: #1e1e1e; }
QLabel#hint { color: #666666; font-size: 12px; }
QLabel#error-label { color: #cc0000; font-size: 12px; }
QLabel#section-label { color: #0070c0; font-weight: bold; }
QLabel#tick-label { color: #888; font-size: 11px; }
QLabel#sidebar-title { color: #0070c0; font-weight: bold; font-size: 13px; }
QLabel#welcome-body { color: #333333; font-size: 13px; }

QLineEdit, QPlainTextEdit, QTextEdit {
    background-color: #ffffff;
    border: 1px solid #c8c8c8;
    border-radius: 4px;
    padding: 4px 6px;
    color: #1e1e1e;
    selection-background-color: #add6ff;
}
QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus {
    border-color: #0078d4;
}

QTextBrowser {
    background-color: #ffffff;
    border: 1px solid #c8c8c8;
    border-radius: 4px;
    padding: 4px;
    color: #1e1e1e;
}
QTextBrowser#sidebar-browser { background-color: transparent; border: none; }
QTextBrowser#cognitive-example {
    background-color: #ebebeb;
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 6px;
    color: #333;
    font-style: italic;
}

QPushButton {
    background-color: #e5e5e5;
    color: #1e1e1e;
    border: 1px solid #b8b8b8;
    border-radius: 4px;
    padding: 5px 16px;
    min-height: 26px;
}
QPushButton:hover { background-color: #d0e4f7; border-color: #0078d4; }
QPushButton:pressed { background-color: #add6ff; }
QPushButton#primary-btn {
    background-color: #0078d4;
    border-color: #0078d4;
    color: #ffffff;
    font-weight: bold;
}
QPushButton#primary-btn:hover { background-color: #106ebe; }
QPushButton#skip-btn { color: #888; background-color: transparent; border-color: #b8b8b8; }

QPushButton#exit-btn {
    background-color: #b02c2c;
    border-color: #b02c2c;
    color: #ffffff;
}
QPushButton#exit-btn:hover {
    background-color: #922424;
    border-color: #922424;
}

QPushButton#start-over-btn {
    background-color: #9a7020;
    border-color: #9a7020;
    color: #ffffff;
}
QPushButton#start-over-btn:hover {
    background-color: #7a5a18;
    border-color: #7a5a18;
}

QPushButton#qt_wizard_commit_button2 {
    color: #888;
    background-color: transparent;
    border: 1px solid #b8b8b8;
    padding: 3px 10px;
    min-height: 22px;
    font-size: 11px;
}

QListWidget#checklist {
    background-color: #ffffff;
    border: 1px solid #c8c8c8;
    border-radius: 4px;
}
QListWidget#checklist::item { padding: 5px 4px; border-radius: 3px; }
QListWidget#checklist::item:hover { background-color: #e8f0fe; }
QListWidget#checklist::item:selected { background-color: transparent; color: #1e1e1e; outline: none; }
QListWidget#checklist:focus { outline: none; }
QListWidget#checklist::item:focus { outline: none; border: none; }

QListWidget#checklist::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 2px solid #888;
    background-color: #ffffff;
}
QListWidget#checklist::indicator:unchecked {
    border: 2px solid #888;
    background-color: #ffffff;
}
QListWidget#checklist::indicator:checked {
    background-color: #0078d4;
    border: 2px solid #0078d4;
    image: url({check_svg});
}

QRadioButton, QCheckBox { spacing: 8px; color: #1e1e1e; padding: 3px 0; }
QRadioButton::indicator {
    width: 16px; height: 16px;
    border-radius: 8px; border: 2px solid #888; background: #ffffff;
}
QRadioButton::indicator:checked { background: #0078d4; border-color: #0078d4; }
QCheckBox::indicator {
    width: 16px; height: 16px;
    border-radius: 3px; border: 2px solid #888; background: #ffffff;
}
QCheckBox::indicator:checked { background: #0078d4; border-color: #0078d4; image: url({check_svg}); }

QGroupBox {
    border: 1px solid #c8c8c8;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 6px;
    color: #666;
    font-size: 12px;
}
QGroupBox::title { subcontrol-origin: margin; left: 8px; top: -1px; color: #666; }

QSlider::groove:horizontal { height: 6px; background: #d0d0d0; border-radius: 3px; }
QSlider::handle:horizontal {
    width: 18px; height: 18px;
    background: #0078d4; border-radius: 9px; margin: -6px 0;
}
QSlider::handle:horizontal:hover { background: #106ebe; }
QSlider::sub-page:horizontal { background: #add6ff; border-radius: 3px; }

QScrollBar:vertical { width: 10px; background: #f5f5f5; border: none; }
QScrollBar::handle:vertical { background: #c0c0c0; border-radius: 5px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #a0a0a0; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { height: 10px; background: #f5f5f5; border: none; }
QScrollBar::handle:horizontal { background: #c0c0c0; border-radius: 5px; min-width: 24px; }

QFrame#sidebar-sep { color: #d0d0d0; }
QWizard QLabel { color: #1e1e1e; }
QDialog { background-color: #ffffff; }
QMessageBox { background-color: #f5f5f5; }

QToolButton#theme-toggle {
    background-color: transparent;
    border: 1px solid #c8c8c8;
    border-radius: 4px;
    color: #1e1e1e;
    padding: 5px 16px;
    min-height: 26px;
}
QToolButton#theme-toggle:hover {
    background-color: #d0e4f7;
    border-color: #0078d4;
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# QSS builder — interpolate the checkmark SVG path into the templates
# ─────────────────────────────────────────────────────────────────────────────

def _build_dark_qss() -> str:
    return _DARK_QSS.replace("{check_svg}", _CHECK_SVG)

def _build_light_qss() -> str:
    return _LIGHT_QSS.replace("{check_svg}", _CHECK_SVG)


# ─────────────────────────────────────────────────────────────────────────────
# Main window
# ─────────────────────────────────────────────────────────────────────────────

class WizardApp(QMainWindow):
    """Main window: QWizard (with theme toggle) on the left, live prompt sidebar on the right."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sys Prompt Wizard")
        self.resize(1100, 680)
        self._dark_mode = True

        self._state = WizardState()

        # ── Central layout ───────────────────────────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)
        outer = QHBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Left column: wizard (theme toggle overlaid) ──────────────────────
        left_col = QWidget()
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # Wizard
        self._wizard = PromptWizard(self._state, self)
        left_layout.addWidget(self._wizard, 1)

        outer.addWidget(left_col, 1)

        # ── Sidebar ──────────────────────────────────────────────────────────
        self._sidebar = PromptSidebar(self)
        self._sidebar.setStyleSheet("PromptSidebar { border-left: 1px solid #3c3c3c; }")
        self._wizard.sidebar = self._sidebar
        outer.addWidget(self._sidebar)

        # ── Theme toggle — floating over wizard top-right ────────────────────
        self._theme_btn = QToolButton(self._wizard)
        self._theme_btn.setObjectName("theme-toggle")
        self._theme_btn.setText("☀  Light theme")
        self._theme_btn.setToolTip("Switch to light theme")
        self._theme_btn.clicked.connect(self._toggle_theme)
        self._theme_btn.adjustSize()
        self._theme_btn.raise_()

        # Install event filter on wizard to reposition button on resize
        self._wizard.installEventFilter(self)

        # Initial sidebar state
        self._sidebar.refresh_content(self._state)

        # Close the main window when the wizard emits finished
        self._wizard.finished.connect(self._on_wizard_finished)

    def eventFilter(self, obj, event) -> bool:
        """Reposition theme toggle when the wizard resizes."""
        from PySide6.QtCore import QEvent
        if obj is self._wizard and event.type() == QEvent.Resize:
            self._reposition_theme_btn()
        return super().eventFilter(obj, event)

    def _reposition_theme_btn(self) -> None:
        """Place the theme button at top-right of the wizard, aligned with the title."""
        btn = self._theme_btn
        btn.adjustSize()
        x = self._wizard.width() - btn.width() - 14
        y = 10  # Vertically align with the page title line
        btn.move(x, y)
        btn.raise_()

    def _toggle_theme(self) -> None:
        self._dark_mode = not self._dark_mode
        if self._dark_mode:
            QApplication.instance().setStyleSheet(_build_dark_qss())
            self._theme_btn.setText("☀  Light theme")
            self._theme_btn.setToolTip("Switch to light theme")
            self._sidebar.setStyleSheet("PromptSidebar { border-left: 1px solid #3c3c3c; }")
        else:
            QApplication.instance().setStyleSheet(_build_light_qss())
            self._theme_btn.setText("🌙  Dark theme")
            self._theme_btn.setToolTip("Switch to dark theme")
            self._sidebar.setStyleSheet("PromptSidebar { border-left: 1px solid #d0d0d0; }")

    def _on_wizard_finished(self, result: int) -> None:
        self.close()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        # Position theme toggle once the window is laid out
        self._reposition_theme_btn()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")            # consistent cross-platform baseline
    app.setStyleSheet(_build_dark_qss())
    window = WizardApp()
    window.show()
    sys.exit(app.exec())
