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
**Status:** ⬜ Not Started

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
**Status:** ⬜ Not Started

- [ ] Write `src/presets/roles/tech_science/software_system_architect.txt`
- [ ] Add `SOFTWARE_SYSTEM_ARCHITECT` entry to `Roles.TechScience` enum in `data.py`

**Alignment needed:** Review and approve the preset content before committing.

---

### Step 4 — Edit Researcher Role Prompt
**Status:** ⬜ Not Started

- [ ] Review current `presets/roles/general_guidance/researcher.txt`
- [ ] Refine prompt for clarity, scope, and quality
- [ ] Align on final content before committing

**Alignment needed:** Review and approve revised prompt content.

---

### Step 5 — Technology-Specific Best Practices Presets
**Status:** ⬜ Not Started

New preset category: `presets/technologies/` (or sub-folder of `roles/tech_science/`).
Each file contains language/framework-specific best practices to append to the prompt.

- [ ] Decide folder structure and naming convention
- [ ] Decide initial set of technologies to cover (e.g. Python, C++, TypeScript, ...)
- [ ] Write presets — one file per technology
- [ ] Add corresponding enum entries in `data.py` under a new `Technologies` class
- [ ] Extend `PromptBuilder` to handle technology selections

**Alignment needed:** Agree on tech list and folder structure before writing content.

---

### Step 6 — Wizard Implementation
**Status:** ⬜ Not Started

See `docs/wizard_flow.md` for the full UX design.

**Confirmed flow:**
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

- [ ] Install `textual` dependency — add to `requirements.txt`
- [ ] Implement `src/wizard.py` — multi-screen Textual app
- [ ] Implement `launcher_wizard.bat`

**Alignment needed:** ✅ `wizard_flow.md` finalised — ready to implement.

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
