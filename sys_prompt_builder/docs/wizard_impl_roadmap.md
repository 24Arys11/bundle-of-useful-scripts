# Sys Prompt Builder — Task Roadmap

Traceability document. Updated after every iteration. Defines what has been decided, what is in progress, and what remains.

---

## Decisions Log

| # | Decision | Rationale |
|---|---|---|
| 1 | Use **Textual** for the wizard UI | Full mouse support, modern TUI, Screen-based navigation maps naturally to wizard pages, no heavy GUI deps |
| 2 | Wizard lives in `sys_prompt_builder/src/wizard.py` | Reuses existing `PromptBuilder`, `data.py`, and all preset `.txt` files with zero duplication |
| 3 | Separate `launcher_wizard.bat` | Keeps launchers at root, clean entry points, no changes to existing `launcher.bat` |
| 4 | Refactor to `src/` subfolder | Keeps root clean — only launchers and docs-facing files at root level |
| 5 | Add `docs/` subfolder | Keeps markdown docs organized; README links into `docs/` |
| 6 | Add Software System Architect preset | New role needed for the tech/science category |
| 7 | Edit Researcher role prompt | Current researcher prompt needs refinement before it is surfaced in the wizard |
| 8 | Add technology-specific best practices presets | Enables per-language/framework guidance (C++, Python, etc.) as a new preset category |
| 9 | Wizard = survey/decision tree, not preset picker | Wizard targets beginners; existing GUI remains the developer control panel |
| 10 | Align on each step before implementing | Prevents drift; user validates each step |
| 11 | Wizard flow: Use Case (multi-select) → branch pages → shared pages | Use case drives which branch pages appear; shared pages (cognitive profile, communication, protocols, custom instructions, preview, export) always shown. No "custom/mixed" escape hatch — use the other launcher for that. |
| 12 | Dev branch includes A4 Project Information page | Allows user to describe architecture, tech stack, patterns — injected as context into the prompt. Precedes optional A5 Production Guardrails page. |
| 13 | Cognitive profile uses 5×5 clickable button grid | Each cell = (convergent level, divergent level) pair. Cell text shows a short example AI response at those settings. More visual and decisive than sliders. |
| 14 | Advice type only shown in Coaching branch | Advice types are designed for coaching; not relevant for dev or research. |
| 15 | GUI redesigned to 5-column layout | Technologies column was too long to stack under Behaviours; each major category gets its own column for scan-ability |
| 16 | Copy to Clipboard button placed in `right_frame` below textbox | Logical proximity — the button acts on the textbox content |
| 17 | Add "Build Special Prompt" feature | Some prompts are standalone and should not concatenate with checkbox selections; dedicated popup with radio select loads file directly |
| 18 | `presets/special_prompts/` directory for standalone prompts | Separates standalone prompts from composable presets; popup iterates `SpecialPrompts` enum dynamically |
| 19 | Writing assistant enhanced with PROSE STYLE + LANGUAGE RESTRICTIONS sections | Plain-English behavioral instructions derived from linguistic metric targets; ensures LLM output conforms to the intended prose register without seeing raw numbers |
| 20 | Replace **Textual** with **PySide6** for the wizard | Textual (GPL) was incompatible with potential relicensing; PySide6 (LGPL) is safe. Also yields a true desktop window with native OS controls, resizing, and drag-and-drop support |
| 21 | Merge S1 (Cognitive) + S2 (Communication) into a single `S1CogCommPage` | All thinking and communication settings are logically grouped; one page is simpler and faster for users |
| 22 | Replace S6 Export page with `ExportDialog` modal popup | Wizard state remains intact after export — user can export multiple times without restarting; cleaner flow |
| 23 | `project_info` renders as a dedicated `Project context:` section | Separates the user's project description from the further-instructions bullet list; cleaner rendered prompt |
| 24 | `NoWheelSlider` wrapper around `QSlider` | Mouse wheel on a slider inside a scroll area accidentally changes values; overriding `wheelEvent` → `ignore()` fixes accidental changes |
| 25 | Rename `presets/user_interaction/` → `presets/user_alignment/` and enum member `BABYSITTER` → `MAXIMUM` | "Alignment" better describes the intent (keeping AI and user in sync); "Maximum" is a clearer label than "Babysitter" |
| 26 | Floating `QToolButton` overlay for theme toggle | Embedding the toggle in a top-bar strip caused layout conflicts; a child widget of the wizard window repositioned on `Resize` events sits cleanly top-right without interfering with page layout |

---

## Roadmap

### Step 1 — Documentation & Planning
**Status:** ✅ Done

- [x] Create `docs/` folder
- [x] Create `docs/ROADMAP.md` (this file)
- [x] Create `docs/wizard_flow.md` — full wizard UX flow with page-by-page design
- [x] Update `README.md` to reference docs

---

### Step 2 — Folder Refactor
**Status:** ✅ Done

Move all source files into `src/` subfolder. Only launchers and top-level docs remain at root.

**Target structure:**
```
sys_prompt_builder/
├── launcher.bat
├── launcher_wizard.bat        ← new
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── ROADMAP.md
│   └── wizard_flow.md
└── src/
    ├── cli.py
    ├── config.json
    ├── data.py
    ├── gui.py
    ├── prompt_builder.py
    ├── test.py
    ├── output.txt
    ├── personal_presets/
    └── presets/
```

**Files to move:** `cli.py`, `config.json`, `data.py`, `gui.py`, `prompt_builder.py`, `test.py`, `output.txt`, `personal_presets/`, `presets/`

**Files to update after move:**
- `launcher.bat` → `cd src` before launching `gui.py`
- `launcher_wizard.bat` → `cd src` before launching `wizard.py`
- All relative preset paths in `data.py` remain valid (relative to `src/` CWD)

---

### Step 3 — Software System Architect Preset
**Status:** ✅ Done

- [x] Write `src/presets/roles/tech_science/software_system_architect.txt`
- [x] Add `SOFTWARE_SYSTEM_ARCHITECT` entry to `Roles.TechScience` enum in `data.py`

**Alignment needed:** Review and approve the preset content before committing.

---

### Step 4 — Edit Researcher Role Prompt
**Status:** ✅ Done

- [x] Review current `presets/roles/general_guidance/researcher.txt`
- [x] Refine prompt for agentic codebase + web research behavior

---

### Step 5 — Technology-Specific Best Practices Presets
**Status:** ✅ Done

New preset category: `presets/technologies/` with sub-folders by category.

- [x] Folder structure: `languages/`, `frontend/`, `backend/`, `databases/`, `mobile/`
- [x] 28 preset files written (15 languages, 6 frontend, 3 backend, 2 databases, 1 mobile)
- [x] `Technologies` class added to `data.py` with 5 nested Enum sub-classes and `get_all()`
- [x] `PromptBuilder.add_technology()` added; `build()` emits "Technology best practices:" section
- [x] `gui.py` updated — Technologies section rendered in column 1 below Behaviours with a spacer gap

---

### Step 5b — GUI Redesign
**Status:** ✅ Done

- [x] 5-column layout for `left_frame`: Col 0 Roles | Col 1 Technologies | Col 2 Thinking | Col 3 Behaviours | Col 4 ResponseLength + UserAlignment + AdviceTypes
- [x] `create_column4_buttons()` replaces three separate methods; stacks radio sections with spacers
- [x] "Copy to Clipboard" moved to `right_frame` row 1, `sticky="e"`
- [x] All three footer buttons standardised to `width=22`
- [x] Textbox height increased to 48
- [x] Theme toggle kept at `left_frame` col 0 row 100

---

### Step 5c — Special Prompts Feature
**Status:** ✅ Done

New `presets/special_prompts/` directory for standalone prompts that must not concatenate with checkbox selections.

- [x] `SpecialPrompts` enum added to `data.py` with `get_all()` and `get_path()`
- [x] "Build Special Prompt" button added to col 3 row 100 in `gui.py`
- [x] `open_special_prompt_popup()` — modal `tk.Toplevel`, theme-aware bg, radio buttons iterate enum, "Load Prompt" writes file content directly to textbox
- [x] 7 prompts written and wired: `reasoning_engine`, `future_vision_guide`, `prompt_creator`, `writing_assistant`, `sentence_decomposer`, `introspection_interviewer`, `opportunity_gap_cartographer`

---

### Step 5d — Writing Assistant Prompt Refinement
**Status:** ✅ Done

- [x] Added `# PROSE STYLE` section — 8 behavioral rules covering sentence rhythm, subordination preference, passive voice frequency, deliberate vocabulary repetition, thematic echo, metaphor discipline, alliteration pruning, paragraph cohesion
- [x] Added `# LANGUAGE RESTRICTIONS` section — prohibits AI buzzwords, hedging qualifiers, decorative punctuation, fabricated citations
- [x] Contrastive rhetoric rule strengthened with explicit raise-to-dismiss pattern diagnosis and full banned-phrase list including AI-specific reframe constructions ("This is not just about X, it's Y", etc.)

---

### Step 6 — Wizard Implementation
**Status:** ✅ Done

See `docs/wizard_flow.md` for the full UX design.

Initially prototyped with **Textual** (TUI), then fully migrated to **PySide6** (decision #20) as the production implementation.

**5-module architecture (`src/`):**

| File | Responsibility |
|---|---|
| `wizard_state.py` | `WizardState` dataclass, all constants, enum helpers |
| `wizard_prompt.py` | `build_prompt_from_state()` — maps state → PromptBuilder |
| `wizard_widgets.py` | `PromptSidebar`, `CognitiveWidget`, `NoWheelSlider` |
| `wizard_screens.py` | All `QWizardPage` subclasses + `PromptWizard` + `ExportDialog` |
| `wizard.py` | `WizardApp` (QMainWindow), QSS themes, entry point |

**Flow implemented:**
```
Welcome
  └─► Use Case (multi-select, ≥1 required)
        ├─► [Software Dev]  A1 → A2 → A3 → A4 → [A5 Guardrails]
        ├─► [Learning]      B1 Teaching style
        ├─► [Coaching]      C1 Coach expertise
        ├─► [Research]      (silent — Researcher role added)
        ├─► [Creative]      E1 Creative type
        └─► [Professional]  F1 Business domain
              ↓ (always shown)
        S1 Thinking & Communication Style  ← merged S1+S2 (decision #21)
        S3 Protocols                        (skippable)
        S4 Custom Instructions              (skippable)
        S5 Preview + Export dialog popup    ← no S6 page (decision #22)
```

- [x] `PySide6>=6.5` added to `requirements.txt`
- [x] `wizard_state.py` — `WizardState` dataclass with `response_length`, `interaction`, `behavioral_policies`, `custom_policy`, `convergent_level`, `divergent_level` fields
- [x] `wizard_widgets.py` — `CognitiveWidget` (live example preview), `NoWheelSlider` (decision #24), `PromptSidebar` (290px HTML live summary)
- [x] `wizard_screens.py` — all branch pages + `S1CogCommPage` (merged, decision #21) + `PromptWizard` + `ExportDialog` (decision #22)
- [x] `wizard.py` — `WizardApp` with QSS dark/light themes, floating theme toggle (decision #26), 1100×680 window
- [x] `wizard_prompt.py` — calls `set_project_context()` (decision #23), `set_response_length()`, maps all state fields
- [x] `prompt_builder.py` — `set_project_context()` method renders dedicated `Project context:` section
- [x] `launcher_wizard.bat` already in place (`cd /d "%~dp0src"` → `pythonw.exe wizard.py`)

**Key implementation notes:**
- Back navigation never duplicates state — all `initializePage()` calls are safe to call multiple times
- `S1CogCommPage`: 4 groups — Cognitive Profile sliders, Response Length slider (default LOW), User Alignment slider (default HIGH), Behavioral Policies checklist (3 pre-checked by default)
- `ExportDialog`: modal, formats txt/md/json/clipboard, closes automatically on successful save
- `PromptWizard.nextId()` overridden to implement dynamic page ordering based on use-case selections
- Button object names `exit-btn` / `start-over-btn` enable per-button QSS colour rules

---

### Step 7 — README Update
**Status:** ✅ Done

- [x] Add Wizard section to README (as the recommended entry point for beginners)
- [x] Rename "GUI Usage (Recommended)" → "GUI Usage (Developer Control Panel)"
- [x] Fix docs links to `wizard_flow.md` and `wizard_impl_roadmap.md`
- [x] Document export formats (`.txt`, `.md`, `.json`, clipboard) in wizard section
- [x] Fix CLI section typos

---

### Step 8 — Post-Launch Refinements
**Status:** ✅ Done

Iterative UX improvements made after the initial PySide6 wizard reached working state.

**Window & layout:**
- [x] Resize default window to 1100×680 (was 1300×760)
- [x] Set wizard minimum size to 720×520
- [x] Theme toggle made a floating `QToolButton` child of the wizard, repositioned via `eventFilter(Resize)` (decision #26)

**S1 page enhancements:**
- [x] Response Length added as a `NoWheelSlider` (0–4, default index 1 = LOW)
- [x] User Alignment renamed from User Interaction; slider default changed to index 3 = HIGH
- [x] Behavioral Policies group added; 3 policies pre-checked by default (`no_hallucinations`, `no_contrastive_rhetoric`, `no_ai_buzzwords`)
- [x] `INTERACTION_KEYS / INTERACTION_NAMES`: `"BABYSITTER"` → `"MAXIMUM"` (decision #25)

**Prompt structure:**
- [x] `project_info` rendered as dedicated `Project context:` section via `PromptBuilder.set_project_context()` (decision #23)
- [x] Response length now injected into prompt via `set_response_length(state.response_length_enum())`

**Button styles:**
- [x] Exit button: dark red fill (`#922424` dark / `#b02c2c` light), same shape as Export button (flat, no bold)
- [x] Start Over button: dark orange fill (`#7a5a18` dark / `#9a7020` light), same shape as Export button

**Preset files:**
- [x] Folder `presets/user_interaction/` renamed to `presets/user_alignment/`
- [x] File `5_babysitter.txt` renamed to `5_maximum.txt`
- [x] All 5 `user_alignment` presets rewritten with clearer language

**Inspection helper prompt:**
- [x] Updated to request thorough analysis, sample a significant number of files, list 7 aspects (added: common patterns/idioms), target ~500 words

---

## Implementation Notes

- `data.py` uses **relative paths** from CWD — wizard must be launched with CWD set to `src/`
- `PromptWizard.nextId()` drives dynamic page ordering; page IDs are registered at wizard construction and skipped pages just never appear in `nextId()` output
- `PromptBuilder` is fully stateful — wizard calls its methods once and renders `build()` on S5; Back navigation never duplicates state
- Personal presets (`personal_presets/`) live outside the enum system — they are available in the developer GUI (`gui.py`) but not yet surfaced in the wizard
