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

- [x] 5-column layout for `left_frame`: Col 0 Roles | Col 1 Technologies | Col 2 Thinking | Col 3 Behaviours | Col 4 ResponseLength + UserInteraction + AdviceTypes
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

**Flow implemented:**
```
Welcome
  └─► Use Case (multi-select, ≥1 required)
        ↓ branch pages per selected use case, in order:
        ├─► [Software Dev]  A1 Help types → A2 Technologies → A3 Project type → A4 Project information → [A5 Guardrails]
        ├─► [Learning]      B1 Teaching style
        ├─► [Coaching]      C1 Coach expertise
        ├─► [Research]      (silent — Researcher role added, no page shown)
        ├─► [Creative]      E1 Creative type
        └─► [Professional]  F1 Business domain
              ↓ always:
        S1 Cognitive Profile (5×5 grid)
        S2 Communication Preferences
        S3 Protocols
        S4 Custom Instructions
        S5 Preview
        S6 Export
```

- [x] Install `textual>=8.1.1` — added to `requirements.txt`
- [x] Implement `src/wizard.py` — 17-screen Textual app (WizardApp + WizardState + CognitiveGrid widget + PromptSidebar + all screens)
- [x] `launcher_wizard.bat` already in place (`cd /d "%~dp0src"` → `pythonw.exe wizard.py`)

**Architecture notes:**
- `WizardApp` holds `WizardState` dataclass and a `deque` screen queue
- `build_screen_queue()` computes the ordered screen sequence from use-case selections
- `advance()` pops the next class from the queue and pushes it
- `A5GuardrailsScreen` auto-skips on mount if `project_type != "production"`
- `S6ExportScreen` supports `.txt`, `.md`, `.json`, and clipboard; outputs to `src/output/`
- `reset_wizard()` clears state and calls `switch_screen(WelcomeScreen())` to restart cleanly
- `build_prompt_from_state()` free function maps `WizardState` → `PromptBuilder` calls, redirecting stdout to suppress the builder's `print()`

---

### Step 7 — README Update
**Status:** ⬜ Not Started (partial — docs links added in Step 1)

- [ ] Add Wizard section to README
- [ ] Update GUI/CLI sections to reflect new `src/` paths
- [ ] Document save formats (`.txt`, `.md`, `.json`, clipboard)

---

## Implementation Notes

- `data.py` uses **relative paths** from CWD — wizard must be launched with CWD set to `src/`
- Textual's `Screen` push/pop model maps directly to wizard page navigation
- `PromptBuilder` is already fully stateful — wizard just calls its methods and renders `build()` output
- Personal presets currently live outside the enum system — wizard will offer them as a separate optional step
