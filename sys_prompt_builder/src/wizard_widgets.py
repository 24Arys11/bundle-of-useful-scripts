"""wizard_widgets.py — PySide6 custom widgets for the prompt wizard.

Contains:
  PromptSidebar   — live summary panel (right column, injected by WizardApp)
  CognitiveWidget — two real QSliders + live example text block
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from wizard_state import COGNITIVE_EXAMPLES, CONV_NAMES, DIV_NAMES


# ─────────────────────────────────────────────────────────────────────────────
# Wheel-deaf slider  (click/drag only — wheel scroll is ignored)
# ─────────────────────────────────────────────────────────────────────────────

class NoWheelSlider(QSlider):
    """QSlider that ignores mouse-wheel events so scrolling a page doesn't
    accidentally change a setting."""

    def wheelEvent(self, event: QWheelEvent) -> None:  # type: ignore[override]
        event.ignore()


# ─────────────────────────────────────────────────────────────────────────────
# Prompt Sidebar
# ─────────────────────────────────────────────────────────────────────────────

class PromptSidebar(QWidget):
    """Live summary panel — updated whenever the wizard advances or goes back."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(290)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(4)

        title = QLabel("Prompt Summary")
        title.setObjectName("sidebar-title")
        root.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("sidebar-sep")
        root.addWidget(sep)

        self._browser = QTextBrowser()
        self._browser.setObjectName("sidebar-browser")
        self._browser.setOpenExternalLinks(False)
        self._browser.setReadOnly(True)
        root.addWidget(self._browser, 1)

    # ── Public API ──────────────────────────────────────────────────────────

    def refresh_content(self, state) -> None:
        """Rebuild the HTML summary from the current WizardState."""
        from wizard_prompt import _resolve_roles, _resolve_techs  # local import avoids cycle

        roles = _resolve_roles(state)
        techs = _resolve_techs(state)

        uc_label = {
            "software_dev": "Software Dev",
            "learning":     "Learning",
            "coaching":     "Coaching",
            "research":     "Research",
            "creative":     "Creative",
            "business":     "Professional",
        }

        h: list[str] = []

        if state.use_cases:
            h.append("<b>Use cases</b>")
            for uc in state.use_cases:
                h.append(f"&nbsp;• {uc_label.get(uc, uc)}")
            h.append("")

        if roles:
            h.append("<b>Roles</b>")
            for r in roles:
                raw = str(r)
                name = raw.split(".")[-1].replace("_", " ").title() if "." in raw else raw
                h.append(f"&nbsp;• {name}")
            h.append("")

        if techs:
            h.append("<b>Technologies</b>")
            names = []
            for t in techs:
                n = t.name if hasattr(t, "name") else str(t)
                names.append(n.replace("_", " ").title())
            h.append("&nbsp;" + ", ".join(names))
            h.append("")

        if state.project_type and "software_dev" in state.use_cases:
            h.append(f"<b>Project type</b>: {state.project_type.title()}")
            h.append("")

        h.append("<b>Thinking</b>")
        h.append(f"&nbsp;Analytical: {CONV_NAMES[state.convergent_level]}")
        h.append(f"&nbsp;Creative: {DIV_NAMES[state.divergent_level]}")
        h.append("")

        h.append(f"<b>Alignment</b>: {state.alignment.capitalize()}")

        if state.protocols:
            h.append("")
            h.append(f"<b>Protocols</b>: {len(state.protocols)} defined")

        self._browser.setHtml("<br>".join(h))


# ─────────────────────────────────────────────────────────────────────────────
# Cognitive Widget
# ─────────────────────────────────────────────────────────────────────────────

class CognitiveWidget(QWidget):
    """Two labelled QSliders for analytical depth + creative divergence.

    A live example block updates as the sliders move.
    """

    def __init__(
        self,
        conv_initial: int = 2,
        div_initial: int = 2,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setSpacing(8)

        # ── Analytical depth ────────────────────────────────────────────────
        root.addWidget(self._section_label("Analytical depth"))
        root.addLayout(self._tick_labels(CONV_NAMES))
        self._conv_slider = self._make_slider(conv_initial)
        root.addWidget(self._conv_slider)

        # ── Creative divergence ──────────────────────────────────────────────
        root.addWidget(self._section_label("Creative divergence"))
        root.addLayout(self._tick_labels(DIV_NAMES))
        self._div_slider = self._make_slider(div_initial)
        root.addWidget(self._div_slider)

        # ── Example block ────────────────────────────────────────────────────
        example_lbl = QLabel("Example AI response style at these settings:")
        example_lbl.setObjectName("hint")
        root.addWidget(example_lbl)

        self._example = QTextBrowser()
        self._example.setObjectName("cognitive-example")
        self._example.setFixedHeight(70)
        self._example.setReadOnly(True)
        root.addWidget(self._example)

        # Wire signals
        self._conv_slider.valueChanged.connect(self._update_example)
        self._div_slider.valueChanged.connect(self._update_example)
        self._update_example()

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def conv_level(self) -> int:
        return self._conv_slider.value()

    @property
    def div_level(self) -> int:
        return self._div_slider.value()

    def restore(self, conv: int, div: int) -> None:
        self._conv_slider.setValue(conv)
        self._div_slider.setValue(div)

    # ── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _section_label(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("section-label")
        return lbl

    @staticmethod
    def _make_slider(initial: int) -> NoWheelSlider:
        s = NoWheelSlider(Qt.Horizontal)
        s.setRange(0, 4)
        s.setValue(initial)
        s.setTickInterval(1)
        s.setTickPosition(QSlider.TicksBelow)
        s.setSingleStep(1)
        s.setPageStep(1)
        return s

    @staticmethod
    def _tick_labels(names: list[str]) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        for name in names:
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setObjectName("tick-label")
            row.addWidget(lbl, 1)
        return row

    def _update_example(self) -> None:
        text = COGNITIVE_EXAMPLES[self._div_slider.value()][self._conv_slider.value()]
        self._example.setPlainText(text)
