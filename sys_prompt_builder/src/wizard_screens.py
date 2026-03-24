"""wizard_screens.py — All PySide6 QWizardPage classes + PromptWizard.

Navigation contract:
  - Each page stores its state in validatePage() (called on Next click).
  - initializePage() restores UI from state (called on both forward and Back nav).
  - nextId() uses _next_id() helper which computes the correct next page from
    the CURRENT state — so A5 is automatically included only for production.
  - No manual queue management needed; QWizard handles the Back stack natively.
"""
from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
    QWizard,
    QWizardPage,
)

from wizard_state import (
    TECH_OPTIONS, GUARDRAIL_OPTIONS, BEHAVIORAL_POLICY_OPTIONS,
    ALIGNMENT_NAMES, ALIGNMENT_KEYS,
    RESPONSE_NAMES, RESPONSE_KEYS,
    WizardState,
)
from wizard_prompt import build_prompt_from_state, export_prompt
from wizard_widgets import CognitiveWidget, NoWheelSlider


def _read_text_with_fallback(path: Path) -> str:
    """Read a text file, trying multiple encodings before giving up."""
    for enc in ("utf-8", "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, ValueError):
            continue
    # latin-1 never raises UnicodeDecodeError, so we should never reach here,
    # but just in case:
    return path.read_text(encoding="latin-1", errors="replace")


# ─────────────────────────────────────────────────────────────────────────────
# Page ID constants
# ─────────────────────────────────────────────────────────────────────────────

PAGE_WELCOME  = 0
PAGE_USE_CASE = 1
PAGE_A1       = 2
PAGE_A2       = 3
PAGE_A3       = 4
PAGE_A4       = 5
PAGE_A5       = 6
PAGE_B1       = 7
PAGE_C1       = 8
PAGE_E1       = 9
PAGE_F1       = 10
PAGE_S1       = 11
PAGE_S2       = 12
PAGE_S3       = 13
PAGE_S4       = 14
PAGE_S5       = 15
PAGE_S6       = 16


# ─────────────────────────────────────────────────────────────────────────────
# Navigation helpers
# ─────────────────────────────────────────────────────────────────────────────

def _branch_pages(state: WizardState) -> list[int]:
    """Compute the ordered list of pages to visit based on current state."""
    pages = [PAGE_WELCOME, PAGE_USE_CASE]
    if "software_dev" in state.use_cases:
        pages.extend([PAGE_A1, PAGE_A2, PAGE_A3, PAGE_A4])
        if state.project_type == "production":
            pages.append(PAGE_A5)
    if "learning" in state.use_cases:
        pages.append(PAGE_B1)
    if "coaching" in state.use_cases:
        pages.append(PAGE_C1)
    if "creative" in state.use_cases:
        pages.append(PAGE_E1)
    if "business" in state.use_cases:
        pages.append(PAGE_F1)
    pages.extend([PAGE_S1, PAGE_S3, PAGE_S4, PAGE_S5])
    return pages


def _next_id(state: WizardState, current: int) -> int:
    pages = _branch_pages(state)
    try:
        idx = pages.index(current)
        return pages[idx + 1] if idx + 1 < len(pages) else -1
    except ValueError:
        return -1


# ─────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_checklist(items: list[tuple[str, object]], parent: QWidget | None = None) -> QListWidget:
    """Return a QListWidget where every item has a checkbox."""
    lw = QListWidget(parent)
    lw.setObjectName("checklist")
    lw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    for label, data in items:
        item = QListWidgetItem(label)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.Unchecked)
        item.setData(Qt.UserRole, data)
        lw.addItem(item)
    return lw


def _get_checked(lw: QListWidget) -> list:
    return [
        lw.item(i).data(Qt.UserRole)
        for i in range(lw.count())
        if lw.item(i).checkState() == Qt.Checked
    ]


def _set_checked(lw: QListWidget, values: list) -> None:
    for i in range(lw.count()):
        item = lw.item(i)
        item.setCheckState(Qt.Checked if item.data(Qt.UserRole) in values else Qt.Unchecked)


def _hint(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("hint")
    lbl.setWordWrap(True)
    return lbl


def _error_label() -> QLabel:
    lbl = QLabel("")
    lbl.setObjectName("error-label")
    lbl.setWordWrap(True)
    return lbl


# ─────────────────────────────────────────────────────────────────────────────
# Inspection helper dialog
# ─────────────────────────────────────────────────────────────────────────────

_INSPECTION_PROMPT = """\
Analyze this project very thoroughly, sample a significant number of files to \
figure out patterns and produce a concise, technical description covering:

1. Project purpose and primary goals
2. Technology stack and overall architecture
3. Key modules / components and their responsibilities
4. Coding conventions and patterns observed in the codebase
5. External dependencies and integrations
6. Non-obvious design decisions or constraints
7. Common patterns and idioms used across the codebase (e.g. error handling \
strategy, logging approach, dependency injection style, naming conventions)

Write the output as a dense, technical summary (about 500 words).
Assume the reader is a senior engineer who will use this as a
system-prompt context block for an AI coding assistant."""


class InspectionHelperDialog(QDialog):
    """Non-modal popup with a ready-to-paste IDE agent prompt."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Project Inspection Helper")
        self.setMinimumSize(640, 400)

        root = QVBoxLayout(self)

        root.addWidget(_hint(
            "Paste the prompt below into your IDE agent (GitHub Copilot, Cursor, Cline…) "
            "to get an AI-generated project description, then import the result using "
            "the 'Import from File' button or paste it directly into the text area."
        ))

        self._browser = QTextBrowser()
        self._browser.setPlainText(_INSPECTION_PROMPT)
        root.addWidget(self._browser, 1)

        btn_row = QHBoxLayout()
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.clicked.connect(self._copy)
        btn_row.addWidget(copy_btn)
        btn_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        root.addLayout(btn_row)

    def _copy(self) -> None:
        QApplication.clipboard().setText(_INSPECTION_PROMPT)


# ─────────────────────────────────────────────────────────────────────────────
# Drag-and-drop plain text editor  (used on A4)
# ─────────────────────────────────────────────────────────────────────────────

class ProjectInfoEdit(QPlainTextEdit):
    """QPlainTextEdit that accepts file drops (.txt / .md)."""

    ACCEPTED_SUFFIXES = {".txt", ".md", ".markdown", ".rst"}

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setPlaceholderText(
            "Describe your project — architecture, stack, patterns, constraints…\n\n"
            "You can also drag-and-drop a .txt or .md file here, "
            "or use the buttons below to import a file."
        )

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            path = Path(url.toLocalFile())
            if path.suffix.lower() in self.ACCEPTED_SUFFIXES and path.is_file():
                try:
                    self.setPlainText(_read_text_with_fallback(path))
                except Exception as exc:
                    QMessageBox.warning(self, "Import failed", str(exc))
            else:
                QMessageBox.information(
                    self,
                    "Unsupported file",
                    f"Only {', '.join(sorted(self.ACCEPTED_SUFFIXES))} files are supported.",
                )
            event.acceptProposedAction()
        else:
            super().dropEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
# Base page
# ─────────────────────────────────────────────────────────────────────────────

class BasePage(QWizardPage):
    """Base class for all wizard pages.

    Subclasses implement:
      _build_ui()      — called once in __init__, builds widgets
      _restore_ui()    — called in initializePage, populates from state
      _commit_state()  — called in validatePage, saves to state; return False to block
    """

    PAGE_ID: int = -1

    def __init__(self) -> None:
        super().__init__()
        self._err_lbl = _error_label()
        self._build_ui()

    # ── Subclass hooks ───────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Build and lay out all widgets. Called once by __init__."""

    def _restore_ui(self) -> None:
        """Restore widget values from state. Called by initializePage."""

    def _commit_state(self) -> bool:
        """Save widget values to state. Return False to block advance."""
        return True

    # ── QWizardPage overrides ────────────────────────────────────────────────

    def initializePage(self) -> None:
        self._err_lbl.clear()
        self._restore_ui()
        # Update the sidebar (if wizard has one attached)
        wiz = self.wizard()
        if wiz and hasattr(wiz, "sidebar"):
            wiz.sidebar.refresh_content(wiz.state)

    def validatePage(self) -> bool:
        ok = self._commit_state()
        if not ok:
            return False
        # Refresh sidebar after committing
        wiz = self.wizard()
        if wiz and hasattr(wiz, "sidebar"):
            wiz.sidebar.refresh_content(wiz.state)
        return True

    def nextId(self) -> int:
        return _next_id(self.wizard().state, self.PAGE_ID)

    # ── Convenience ──────────────────────────────────────────────────────────

    @property
    def state(self) -> WizardState:
        return self.wizard().state

    def _show_error(self, msg: str) -> None:
        self._err_lbl.setText(msg)


# ─────────────────────────────────────────────────────────────────────────────
# Page 0 — Welcome
# ─────────────────────────────────────────────────────────────────────────────

class WelcomePage(BasePage):
    PAGE_ID = PAGE_WELCOME

    def _build_ui(self) -> None:
        self.setTitle("Sys Prompt Wizard")
        self.setSubTitle(
            "Build a tailored AI system prompt by answering a few simple questions.\n"
            "No prompt engineering knowledge required — the wizard handles everything."
        )
        root = QVBoxLayout(self)
        root.setSpacing(12)
        root.addStretch()

        desc = QLabel(
            "The wizard guides you through:\n"
            "  • Your use-case (development, learning, coaching, creative…)\n"
            "  • Technologies and project context\n"
            "  • Thinking style and communication preferences\n"
            "  • Custom protocols and extra instructions\n\n"
            "At the end you get a fully assembled system prompt ready to paste into any AI tool."
        )
        desc.setWordWrap(True)
        desc.setObjectName("welcome-body")
        root.addWidget(desc)
        root.addStretch()

    def nextId(self) -> int:
        return PAGE_USE_CASE


# ─────────────────────────────────────────────────────────────────────────────
# Page 1 — Use Case
# ─────────────────────────────────────────────────────────────────────────────

class UseCasePage(BasePage):
    PAGE_ID = PAGE_USE_CASE

    def _build_ui(self) -> None:
        self.setTitle("What do you need help with?")
        self.setSubTitle("Select all that apply.  At least one is required.")
        root = QVBoxLayout(self)
        self._list = _make_checklist([
            ("Software Development — write, design, review or build code",        "software_dev"),
            ("Learning & Teaching — understand a topic or technology",             "learning"),
            ("Coaching & Growth — career, habits, accountability, wellbeing",      "coaching"),
            ("Research & Analysis — deep-dive into topics or documents",           "research"),
            ("Creative Work — writing, stories, scripts, ideas",                   "creative"),
            ("Professional / Business — strategy, finance, legal, marketing",      "business"),
        ])
        self._list.setMaximumHeight(220)
        root.addWidget(self._list)
        root.addWidget(self._err_lbl)

    def _restore_ui(self) -> None:
        _set_checked(self._list, self.state.use_cases)

    def _commit_state(self) -> bool:
        sel = _get_checked(self._list)
        if not sel:
            self._show_error("Please select at least one option.")
            return False
        self.state.use_cases = sel
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Branch A — Software Development
# ─────────────────────────────────────────────────────────────────────────────

class A1HelpTypePage(BasePage):
    PAGE_ID = PAGE_A1

    def _build_ui(self) -> None:
        self.setTitle("Software Development — What kind of help?")
        self.setSubTitle("Deselect anything that doesn't apply.")
        root = QVBoxLayout(self)
        self._list = _make_checklist([
            ("Write / implement code",        "engineer"),
            ("Design the architecture",       "architect"),
            ("Research docs, repos, APIs",    "researcher"),
            ("Teach me while we build",       "teacher"),
            ("Review and critique my code",   "reviewer"),
        ])
        self._list.setMaximumHeight(180)
        # Pre-check all by default when state is empty
        for i in range(self._list.count()):
            self._list.item(i).setCheckState(Qt.Checked)
        root.addWidget(self._list)

    def _restore_ui(self) -> None:
        if self.state.help_types:
            _set_checked(self._list, self.state.help_types)

    def _commit_state(self) -> bool:
        self.state.help_types = _get_checked(self._list)
        return True


class A2TechPage(BasePage):
    PAGE_ID = PAGE_A2

    def _build_ui(self) -> None:
        self.setTitle("Software Development — Technologies")
        self.setSubTitle("Which technologies are involved?  Select all that apply.")
        root = QVBoxLayout(self)
        self._list = _make_checklist([(label, value) for label, value in TECH_OPTIONS])
        root.addWidget(self._list)
        root.addWidget(_hint("Use Custom Instructions (later page) for anything not listed."))

    def _restore_ui(self) -> None:
        _set_checked(self._list, self.state.a2_techs)

    def _commit_state(self) -> bool:
        self.state.a2_techs = _get_checked(self._list)
        return True


class A3ProjectTypePage(BasePage):
    PAGE_ID = PAGE_A3

    _ID_MAP = {0: "script", 1: "hobby", 2: "production"}

    def _build_ui(self) -> None:
        self.setTitle("Software Development — Project Type")
        self.setSubTitle("What kind of project is this?")
        root = QVBoxLayout(self)
        self._grp = QButtonGroup(self)
        radios = [
            ("Quick script — pragmatic, no test boilerplate",
             "Minimal structure, skip testing boilerplate unless asked."),
            ("Hobby / Personal project — some structure, tests welcome",
             "Encourage good structure and tests without strict requirements."),
            ("Production grade — full rigour, tests required, extra guardrails page follows",
             "Full engineering standards: tests, error handling, security guardrails."),
        ]
        for i, (label, _tooltip) in enumerate(radios):
            rb = QRadioButton(label)
            rb.setToolTip(_tooltip)
            self._grp.addButton(rb, i)
            root.addWidget(rb)
        # Default: hobby
        self._grp.button(1).setChecked(True)
        # Immediately update state on change so nextId() is correct
        self._grp.idClicked.connect(self._on_changed)

    def _on_changed(self, btn_id: int) -> None:
        self.state.project_type = self._ID_MAP.get(btn_id, "hobby")

    def _restore_ui(self) -> None:
        rev = {v: k for k, v in self._ID_MAP.items()}
        btn_id = rev.get(self.state.project_type, 1)
        self._grp.button(btn_id).setChecked(True)

    def _commit_state(self) -> bool:
        self.state.project_type = self._ID_MAP.get(self._grp.checkedId(), "hobby")
        return True


class A4ProjectInfoPage(BasePage):
    PAGE_ID = PAGE_A4

    def _build_ui(self) -> None:
        self.setTitle("Software Development — Project Information")
        self.setSubTitle(
            "Describe your project (optional) — architecture, stack, patterns, constraints…\n"
            "Drag-and-drop a file onto the text area, import from disk, or type directly."
        )
        root = QVBoxLayout(self)

        self._edit = ProjectInfoEdit()
        root.addWidget(self._edit, 1)

        btn_row = QHBoxLayout()
        import_btn = QPushButton("📂  Import from File")
        import_btn.clicked.connect(self._import_file)
        btn_row.addWidget(import_btn)

        helper_btn = QPushButton("🔍  Inspection Helper")
        helper_btn.clicked.connect(self._open_helper)
        btn_row.addWidget(helper_btn)
        btn_row.addStretch()
        root.addLayout(btn_row)

    def _import_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Project Information",
            "",
            "Text / Markdown files (*.txt *.md *.markdown *.rst);;All files (*)",
        )
        if path:
            try:
                self._edit.setPlainText(_read_text_with_fallback(Path(path)))
            except Exception as exc:
                QMessageBox.warning(self, "Import failed", str(exc))

    def _open_helper(self) -> None:
        dlg = InspectionHelperDialog(self)
        dlg.exec()

    def _restore_ui(self) -> None:
        self._edit.setPlainText(self.state.project_info)

    def _commit_state(self) -> bool:
        self.state.project_info = self._edit.toPlainText().strip()
        return True


class A5GuardrailsPage(BasePage):
    PAGE_ID = PAGE_A5

    def _build_ui(self) -> None:
        self.setTitle("Software Development — Production Guardrails")
        self.setSubTitle("Additional safeguards for production work (optional).")
        root = QVBoxLayout(self)
        self._list = _make_checklist(
            [(label, key) for label, key, _ in GUARDRAIL_OPTIONS]
        )
        self._list.setMaximumHeight(180)
        # Pre-check all guardrails by default
        for i in range(self._list.count()):
            self._list.item(i).setCheckState(Qt.Checked)
        root.addWidget(self._list)
        root.addWidget(_hint("Custom guardrail:"))
        self._custom = QLineEdit()
        self._custom.setPlaceholderText(
            "e.g. Always check for race conditions before async suggestions"
        )
        root.addWidget(self._custom)

    def _restore_ui(self) -> None:
        if self.state.guardrail_keys:
            _set_checked(self._list, self.state.guardrail_keys)
        # else: keep the default all-checked state
        self._custom.setText(self.state.custom_guardrail)

    def _commit_state(self) -> bool:
        self.state.guardrail_keys   = _get_checked(self._list)
        self.state.custom_guardrail = self._custom.text().strip()
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Branch B — Learning & Teaching
# ─────────────────────────────────────────────────────────────────────────────

class B1TeachingPage(BasePage):
    PAGE_ID = PAGE_B1

    _ID_MAP = {0: "direct", 1: "socratic", 2: "examples"}

    def _build_ui(self) -> None:
        self.setTitle("Learning & Teaching — Teaching Style")
        self.setSubTitle("How should the AI explain things to you?")
        root = QVBoxLayout(self)

        self._style_grp = QButtonGroup(self)
        for i, (label, tooltip) in enumerate([
            ("Direct explanation — clear, complete explanations",
             "Full answers upfront, no guessing required."),
            ("Socratic — guide me to the answer with questions",
             "Uses questions to lead you to understand the concept yourself."),
            ("Example-driven — show me first, then explain",
             "Demonstrates with code or examples before theory."),
        ]):
            rb = QRadioButton(label)
            rb.setToolTip(tooltip)
            self._style_grp.addButton(rb, i)
            root.addWidget(rb)
        self._style_grp.button(0).setChecked(True)

        root.addWidget(_hint("Technologies you're learning (optional):"))
        self._tech_list = _make_checklist([(label, value) for label, value in TECH_OPTIONS])
        root.addWidget(self._tech_list)

    def _restore_ui(self) -> None:
        rev = {v: k for k, v in self._ID_MAP.items()}
        self._style_grp.button(rev.get(self.state.teaching_style, 0)).setChecked(True)
        _set_checked(self._tech_list, self.state.b1_techs)

    def _commit_state(self) -> bool:
        self.state.teaching_style = self._ID_MAP.get(self._style_grp.checkedId(), "direct")
        self.state.b1_techs       = _get_checked(self._tech_list)
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Branch C — Coaching & Growth
# ─────────────────────────────────────────────────────────────────────────────

class C1CoachPage(BasePage):
    PAGE_ID = PAGE_C1

    def _build_ui(self) -> None:
        self.setTitle("Coaching & Growth — Coach Expertise")
        self.setSubTitle("What expertise should your coach have?  Select all that apply.")
        root = QVBoxLayout(self)
        self._list = _make_checklist([
            ("Career & professional development",     "career"),
            ("Fitness & physical health",              "fitness"),
            ("Mental wellness & emotional support",    "mental"),
            ("Accountability & habit building",        "accountability"),
        ])
        self._list.setMaximumHeight(160)
        root.addWidget(self._list)
        root.addWidget(self._err_lbl)

    def _restore_ui(self) -> None:
        _set_checked(self._list, self.state.coach_types)

    def _commit_state(self) -> bool:
        sel = _get_checked(self._list)
        if not sel:
            self._show_error("Please select at least one coaching area.")
            return False
        self.state.coach_types = sel
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Branch E — Creative Work
# ─────────────────────────────────────────────────────────────────────────────

class E1CreativePage(BasePage):
    PAGE_ID = PAGE_E1

    _ID_MAP = {0: "fiction", 1: "poetry", 2: "screenwriting", 3: "worldbuilding", 4: "copywriting"}

    def _build_ui(self) -> None:
        self.setTitle("Creative Work — Creative Type")
        root = QVBoxLayout(self)
        self._grp = QButtonGroup(self)
        for i, label in enumerate([
            "Storytelling / Fiction",
            "Poetry",
            "Screenwriting",
            "World-building / Lore",
            "Copywriting / Marketing",
        ]):
            rb = QRadioButton(label)
            self._grp.addButton(rb, i)
            root.addWidget(rb)
        self._grp.button(0).setChecked(True)

    def _restore_ui(self) -> None:
        rev = {v: k for k, v in self._ID_MAP.items()}
        self._grp.button(rev.get(self.state.creative_type, 0)).setChecked(True)

    def _commit_state(self) -> bool:
        self.state.creative_type = self._ID_MAP.get(self._grp.checkedId(), "fiction")
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Branch F — Professional / Business
# ─────────────────────────────────────────────────────────────────────────────

class F1BusinessPage(BasePage):
    PAGE_ID = PAGE_F1

    _ID_MAP = {0: "strategy", 1: "finance", 2: "legal", 3: "marketing"}

    def _build_ui(self) -> None:
        self.setTitle("Professional / Business — Domain")
        root = QVBoxLayout(self)
        self._grp = QButtonGroup(self)
        for i, label in enumerate([
            "Business strategy",
            "Finance & investment",
            "Legal",
            "Marketing & brand",
        ]):
            rb = QRadioButton(label)
            self._grp.addButton(rb, i)
            root.addWidget(rb)
        self._grp.button(0).setChecked(True)

    def _restore_ui(self) -> None:
        rev = {v: k for k, v in self._ID_MAP.items()}
        self._grp.button(rev.get(self.state.business_domain, 0)).setChecked(True)

    def _commit_state(self) -> bool:
        self.state.business_domain = self._ID_MAP.get(self._grp.checkedId(), "strategy")
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Shared S1 — Thinking & Communication Style
# ─────────────────────────────────────────────────────────────────────────────

class S1CogCommPage(BasePage):
    """Merged page: cognitive sliders + alignment slider + advice + behavioral policies."""

    PAGE_ID = PAGE_S1

    _ADV_MAP = {0: "SOFT", 1: "BALLANCED", 2: "HARSH"}

    def _build_ui(self) -> None:
        self.setTitle("Thinking & Communication Style")
        self.setSubTitle(
            "Configure how the AI thinks and communicates with you."
        )
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        container = QWidget()
        root = QVBoxLayout(container)
        root.setSpacing(10)

        # ── Cognitive sliders ────────────────────────────────────────────────
        cog_group = QGroupBox("Cognitive Profile")
        cog_layout = QVBoxLayout(cog_group)
        self._cog_widget = CognitiveWidget(conv_initial=3, div_initial=2)
        cog_layout.addWidget(self._cog_widget)
        root.addWidget(cog_group)

        # ── Response length slider ───────────────────────────────────────────
        resp_group = QGroupBox("Response Length")
        resp_layout = QVBoxLayout(resp_group)
        resp_layout.addWidget(_hint("How verbose should the AI be?"))
        resp_layout.addLayout(self._tick_labels(RESPONSE_NAMES))
        self._resp_slider = NoWheelSlider(Qt.Horizontal)
        self._resp_slider.setRange(0, 4)
        self._resp_slider.setValue(1)  # Low (default)
        self._resp_slider.setTickInterval(1)
        self._resp_slider.setTickPosition(QSlider.TicksBelow)
        self._resp_slider.setSingleStep(1)
        self._resp_slider.setPageStep(1)
        resp_layout.addWidget(self._resp_slider)
        root.addWidget(resp_group)

        # ── alignment slider ───────────────────────────────────────────────
        int_group = QGroupBox("User Alignment Level")
        int_layout = QVBoxLayout(int_group)
        int_layout.addWidget(_hint("How interactive should the AI be?"))
        int_layout.addLayout(self._tick_labels(ALIGNMENT_NAMES))
        self._int_slider = NoWheelSlider(Qt.Horizontal)
        self._int_slider.setRange(0, 4)
        self._int_slider.setValue(3)  # High (default)
        self._int_slider.setTickInterval(1)
        self._int_slider.setTickPosition(QSlider.TicksBelow)
        self._int_slider.setSingleStep(1)
        self._int_slider.setPageStep(1)
        int_layout.addWidget(self._int_slider)
        root.addWidget(int_group)

        # ── Advice type (visible only when coaching selected) ────────────────
        self._advice_box = QGroupBox("Feedback Style")
        adv_layout = QVBoxLayout(self._advice_box)
        adv_layout.addWidget(_hint("How should feedback be delivered?"))
        self._adv_grp = QButtonGroup(self)
        for i, label in enumerate(["Gentle & supportive", "Balanced", "Blunt & challenging"]):
            rb = QRadioButton(label)
            self._adv_grp.addButton(rb, i)
            adv_layout.addWidget(rb)
        self._adv_grp.button(1).setChecked(True)
        root.addWidget(self._advice_box)

        # ── Behavioral policies ──────────────────────────────────────────────
        pol_group = QGroupBox("Behavioral Policies")
        pol_layout = QVBoxLayout(pol_group)
        pol_layout.addWidget(_hint(
            "Select behavioral policies to enforce.  Add your own below."
        ))
        self._policy_list = _make_checklist(
            [(label, key) for label, key, _ in BEHAVIORAL_POLICY_OPTIONS]
        )
        self._policy_list.setMaximumHeight(180)
        # Pre-check default policies
        _DEFAULT_POLICIES = {"no_hallucinations", "no_contrastive_rhetoric", "no_ai_buzzwords"}
        for i in range(self._policy_list.count()):
            item = self._policy_list.item(i)
            if item.data(Qt.UserRole) in _DEFAULT_POLICIES:
                item.setCheckState(Qt.Checked)
        pol_layout.addWidget(self._policy_list)
        pol_layout.addWidget(_hint("Custom policy (optional):"))
        self._custom_policy = QPlainTextEdit()
        self._custom_policy.setFixedHeight(60)
        self._custom_policy.setPlaceholderText(
            'e.g. "Always respond in formal English" or any additional behavioral constraint.'
        )
        pol_layout.addWidget(self._custom_policy)
        root.addWidget(pol_group)

        scroll.setWidget(container)
        page_layout = QVBoxLayout(self)
        page_layout.addWidget(scroll)

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

    def initializePage(self) -> None:
        self._advice_box.setVisible("coaching" in self.state.use_cases)
        super().initializePage()

    def _restore_ui(self) -> None:
        self._cog_widget.restore(self.state.convergent_level, self.state.divergent_level)
        # Response length slider
        rev_resp = {v: i for i, v in enumerate(RESPONSE_KEYS)}
        self._resp_slider.setValue(rev_resp.get(self.state.response_length, 1))
        # alignment slider
        rev_int = {v: i for i, v in enumerate(ALIGNMENT_KEYS)}
        self._int_slider.setValue(rev_int.get(self.state.alignment, 3))
        # Advice
        rev_adv = {v: k for k, v in self._ADV_MAP.items()}
        self._adv_grp.button(rev_adv.get(self.state.advice, 1)).setChecked(True)
        # Policies — only override if user has already committed (non-empty list means visited)
        if self.state.behavioral_policies:
            _set_checked(self._policy_list, self.state.behavioral_policies)
        self._custom_policy.setPlainText(self.state.custom_policy)

    def _commit_state(self) -> bool:
        self.state.convergent_level    = self._cog_widget.conv_level
        self.state.divergent_level     = self._cog_widget.div_level
        self.state.response_length     = RESPONSE_KEYS[self._resp_slider.value()]
        self.state.alignment         = ALIGNMENT_KEYS[self._int_slider.value()]
        self.state.advice              = self._ADV_MAP.get(self._adv_grp.checkedId(), "BALLANCED")
        self.state.behavioral_policies = _get_checked(self._policy_list)
        self.state.custom_policy       = self._custom_policy.toPlainText().strip()
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Shared S3 — Protocols
# ─────────────────────────────────────────────────────────────────────────────

class S3ProtocolsPage(BasePage):
    PAGE_ID = PAGE_S3

    def _build_ui(self) -> None:
        self.setTitle("Protocols  (optional)")
        self.setSubTitle(
            "Define how the AI should behave in specific situations.  "
            "Each pair is kept — navigate back and forward freely."
        )
        root = QVBoxLayout(self)

        root.addWidget(_hint("Scenario:"))
        self._scenario = QLineEdit()
        self._scenario.setPlaceholderText("e.g. When I paste a block of code")
        root.addWidget(self._scenario)

        root.addWidget(_hint("Protocol:"))
        self._protocol = QPlainTextEdit()
        self._protocol.setFixedHeight(80)
        self._protocol.setPlaceholderText("e.g. First identify the language, then review for bugs, then suggest improvements.")
        root.addWidget(self._protocol)

        add_btn = QPushButton("+ Add Protocol")
        add_btn.clicked.connect(self._add_protocol)
        root.addWidget(add_btn)

        root.addWidget(_hint("Added so far:"))
        self._display = QTextBrowser()
        self._display.setFixedHeight(120)
        root.addWidget(self._display)

        root.addWidget(_hint("Tip: this page is optional — click Next to skip."))

    def _restore_ui(self) -> None:
        self._refresh_display()

    def _add_protocol(self) -> None:
        scenario = self._scenario.text().strip()
        protocol = self._protocol.toPlainText().strip()
        if scenario and protocol:
            self.state.protocols.append((scenario, protocol))
            self._refresh_display()
            self._scenario.clear()
            self._protocol.clear()

    def _refresh_display(self) -> None:
        if not self.state.protocols:
            self._display.setPlainText("(none)")
        else:
            lines = [
                f"• [{s}] → {p[:60]}{'…' if len(p) > 60 else ''}"
                for s, p in self.state.protocols
            ]
            self._display.setPlainText("\n".join(lines))

    def _commit_state(self) -> bool:
        return True  # protocols already appended live


# ─────────────────────────────────────────────────────────────────────────────
# Shared S4 — Custom Instructions
# ─────────────────────────────────────────────────────────────────────────────

class S4CustomPage(BasePage):
    PAGE_ID = PAGE_S4

    def _build_ui(self) -> None:
        self.setTitle("Custom Instructions  (optional)")
        self.setSubTitle(
            "Anything else you want to tell the AI?  "
            "Each non-empty line becomes one instruction."
        )
        root = QVBoxLayout(self)
        self._edit = QPlainTextEdit()
        self._edit.setPlaceholderText(
            "e.g. Always prefer immutable data structures.\n"
            "Never use pandas; use polars instead."
        )
        root.addWidget(self._edit, 1)

    def _restore_ui(self) -> None:
        self._edit.setPlainText("\n".join(self.state.extra_instructions))

    def _commit_state(self) -> bool:
        lines = [ln.strip() for ln in self._edit.toPlainText().splitlines() if ln.strip()]
        self.state.extra_instructions = lines  # overwrite — no duplication on Back
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Export dialog  (replaces the old S6 page)
# ─────────────────────────────────────────────────────────────────────────────

class ExportDialog(QDialog):
    """Popup for choosing export format and save location."""

    _FORMAT_MAP = {
        "Plain Text (.txt)": "txt",
        "Markdown (.md)":    "md",
        "JSON (.json)":      "json",
        "Copy to Clipboard": "clipboard",
    }
    _FILTER_MAP = {
        "txt":  "Text files (*.txt)",
        "md":   "Markdown files (*.md)",
        "json": "JSON files (*.json)",
    }

    def __init__(self, state: WizardState, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Export Prompt")
        self.setMinimumWidth(400)
        self._state = state
        self.saved_path: str | None = None  # set on successful save

        root = QVBoxLayout(self)
        root.setSpacing(12)

        root.addWidget(_hint("Choose an export format:"))

        from PySide6.QtWidgets import QComboBox
        self._combo = QComboBox()
        for label in self._FORMAT_MAP:
            self._combo.addItem(label)
        root.addWidget(self._combo)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        save_btn = QPushButton("Save")
        save_btn.setObjectName("primary-btn")
        save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(save_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        root.addLayout(btn_row)

    def _on_save(self) -> None:
        label = self._combo.currentText()
        fmt = self._FORMAT_MAP[label]

        if fmt == "clipboard":
            done = export_prompt(self._state, ["clipboard"], "")
            if done:
                self.saved_path = "clipboard"
                self.accept()
            return

        file_filter = self._FILTER_MAP.get(fmt, "All files (*)")
        default_name = f"my_prompt.{fmt}"
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Prompt", default_name, file_filter,
        )
        if path:
            prompt = self._state.built_prompt
            try:
                if fmt == "json":
                    data = self._build_json(prompt)
                    Path(path).write_text(
                        json.dumps(data, indent=2, default=str), encoding="utf-8"
                    )
                elif fmt == "md":
                    meta = self._build_md_meta()
                    Path(path).write_text(
                        f"{meta}\n```\n{prompt}\n```\n", encoding="utf-8"
                    )
                else:
                    Path(path).write_text(prompt, encoding="utf-8")
                self.saved_path = path
                self.accept()
            except Exception as exc:
                QMessageBox.warning(self, "Export failed", str(exc))

    def _build_md_meta(self) -> str:
        from wizard_prompt import _resolve_roles, _resolve_techs
        roles = [r.name for r in _resolve_roles(self._state)]
        techs = [t.name for t in _resolve_techs(self._state)]
        lines = [
            "---",
            f"use_cases: {self._state.use_cases}",
            f"roles: {roles}",
            f"technologies: {techs}",
            f"project_type: {self._state.project_type}",
            f"convergent: {self._state.convergent().name}",
            f"divergent: {self._state.divergent().name}",
            "---",
        ]
        return "\n".join(lines)

    def _build_json(self, prompt: str) -> dict:
        from wizard_prompt import _resolve_roles, _resolve_techs
        return {
            "use_cases": self._state.use_cases,
            "roles": [r.name for r in _resolve_roles(self._state)],
            "technologies": [t.name for t in _resolve_techs(self._state)],
            "project_type": self._state.project_type,
            "project_info": self._state.project_info,
            "convergent_thinking": self._state.convergent().name,
            "divergent_thinking": self._state.divergent().name,
            "user_alignment": self._state.alignment,
            "advice_type": self._state.advice if self._state.coaching_selected else None,
            "behavioral_policies": self._state.behavioral_policies,
            "custom_policy": self._state.custom_policy,
            "guardrail_keys": self._state.guardrail_keys,
            "protocols": [{"scenario": s, "protocol": p} for s, p in self._state.protocols],
            "extra_instructions": self._state.extra_instructions,
            "prompt": prompt,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Shared S5 — Preview  (final page, with integrated export)
# ─────────────────────────────────────────────────────────────────────────────

class S5PreviewPage(BasePage):
    PAGE_ID = PAGE_S5

    def _build_ui(self) -> None:
        self.setTitle("Prompt Preview")
        self.setSubTitle("Review the assembled system prompt.  Go back to adjust anything.")
        self.setFinalPage(True)
        root = QVBoxLayout(self)
        self._browser = QTextBrowser()
        self._browser.setReadOnly(True)
        root.addWidget(self._browser, 1)

        # Success message — hidden until export completes
        self._success_lbl = QLabel("")
        self._success_lbl.setAlignment(Qt.AlignCenter)
        self._success_lbl.setStyleSheet(
            "color: #4ec9b0; font-weight: bold; padding: 6px 0;"
        )
        self._success_lbl.hide()
        root.addWidget(self._success_lbl)

    def initializePage(self) -> None:
        super().initializePage()
        self._success_lbl.hide()
        prompt = build_prompt_from_state(self.state)
        self.state.built_prompt = prompt
        self._browser.setPlainText(prompt)

        # Turn the wizard's Finish button into a blue Export button
        wiz = self.wizard()
        if wiz:
            finish_btn = wiz.button(QWizard.FinishButton)
            if finish_btn:
                finish_btn.setText("✓  Export")
                finish_btn.setObjectName("primary-btn")
                # Force re-apply style
                finish_btn.style().unpolish(finish_btn)
                finish_btn.style().polish(finish_btn)

    def validatePage(self) -> bool:
        """Instead of finishing, open the export dialog."""
        dlg = ExportDialog(self.state, self)
        if dlg.exec() and dlg.saved_path:
            if dlg.saved_path == "clipboard":
                msg = "✓  Prompt copied to clipboard! You may now exit."
            else:
                msg = "✓  Prompt saved successfully! You may now exit."
            self._success_lbl.setText(msg)
            self._success_lbl.show()
        return False  # Don't close the wizard — let user export multiple times

    def _commit_state(self) -> bool:
        return True

    def nextId(self) -> int:
        return -1  # Final page


# ─────────────────────────────────────────────────────────────────────────────
# PromptWizard  (QWizard container)
# ─────────────────────────────────────────────────────────────────────────────

class PromptWizard(QWizard):
    """QWizard containing all pages.  Shares a single WizardState instance."""

    def __init__(self, state: WizardState, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state   = state
        self.sidebar = None  # injected by WizardApp after construction

        self.setWizardStyle(QWizard.ModernStyle)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setOption(QWizard.HaveHelpButton, False)
        self.setOption(QWizard.HaveCustomButton1, True)
        self.setOption(QWizard.HaveCustomButton2, True)
        self.setButtonText(QWizard.CustomButton1, "↺  Start Over")
        self.setButtonText(QWizard.CustomButton2, "Skip  →")
        self.setButtonText(QWizard.CancelButton,  "Exit")
        self.setButtonText(QWizard.FinishButton,  "Export")
        self.setMinimumSize(720, 520)

        # Layout: [Exit] [Start Over]  ···stretch···  [Skip] [Back] [Next] [Finish]
        self.setButtonLayout([
            QWizard.CancelButton,     # Exit        — far left
            QWizard.CustomButton1,    # Start Over  — left
            QWizard.Stretch,
            QWizard.CustomButton2,    # Skip        — right, before Back
            QWizard.BackButton,       # Back        — right
            QWizard.NextButton,       # Next        — right
            QWizard.FinishButton,     # Finish      — right
        ])

        # Register all pages
        self.setPage(PAGE_WELCOME,  WelcomePage())
        self.setPage(PAGE_USE_CASE, UseCasePage())
        self.setPage(PAGE_A1,       A1HelpTypePage())
        self.setPage(PAGE_A2,       A2TechPage())
        self.setPage(PAGE_A3,       A3ProjectTypePage())
        self.setPage(PAGE_A4,       A4ProjectInfoPage())
        self.setPage(PAGE_A5,       A5GuardrailsPage())
        self.setPage(PAGE_B1,       B1TeachingPage())
        self.setPage(PAGE_C1,       C1CoachPage())
        self.setPage(PAGE_E1,       E1CreativePage())
        self.setPage(PAGE_F1,       F1BusinessPage())
        self.setPage(PAGE_S1,       S1CogCommPage())
        self.setPage(PAGE_S3,       S3ProtocolsPage())
        self.setPage(PAGE_S4,       S4CustomPage())
        self.setPage(PAGE_S5,       S5PreviewPage())
        self.setStartId(PAGE_WELCOME)

        self.currentIdChanged.connect(self._on_page_changed)

        # Connect custom buttons directly (more reliable than customButtonClicked signal)
        start_over_btn = self.button(QWizard.CustomButton1)
        if start_over_btn:
            start_over_btn.setObjectName("start-over-btn")
            start_over_btn.clicked.connect(self._on_start_over)
        skip_btn = self.button(QWizard.CustomButton2)
        if skip_btn:
            skip_btn.clicked.connect(self._on_skip)
        exit_btn = self.button(QWizard.CancelButton)
        if exit_btn:
            exit_btn.setObjectName("exit-btn")

    # ── Skippable pages ─────────────────────────────────────────────────────

    # Pages where the Skip button should be visible 
    _SKIPPABLE = {PAGE_A2, PAGE_A4, PAGE_A5, PAGE_S3, PAGE_S4}

    def _on_start_over(self) -> None:
        """Reset state and restart from the beginning."""
        self.state.__init__()  # reset to defaults
        self.restart()
        if self.sidebar:
            self.sidebar.refresh_content(self.state)

    def _on_skip(self) -> None:
        """Skip the current page without committing state."""
        self.next()

    def _on_page_changed(self, page_id: int) -> None:
        # Show/hide Skip button depending on whether page is skippable
        skip_btn = self.button(QWizard.CustomButton2)
        if skip_btn:
            skip_btn.setVisible(page_id in self._SKIPPABLE)
        if self.sidebar:
            self.sidebar.refresh_content(self.state)
