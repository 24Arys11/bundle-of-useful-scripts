# Wizard UX Flow

Decision-tree survey design for the PySide6 prompt wizard (`wizard.py`).  
Each page is a `QWizardPage` subclass. The user answers questions â€” the wizard maps answers to roles, presets, and instructions behind the scenes.

**Target audience:** Anyone who wants a tailored system prompt without prompt engineering knowledge.  
**Developer control panel:** `gui.py` (launched via `launcher.bat`) remains for power users who want full manual control.

---

## Architecture Overview

| File | Responsibility |
|---|---|
| `wizard_state.py` | `WizardState` dataclass + all constants (enum lists, preset options) |
| `wizard_prompt.py` | `build_prompt_from_state()` â€” maps state â†’ PromptBuilder calls |
| `wizard_widgets.py` | `PromptSidebar`, `CognitiveWidget`, `NoWheelSlider` |
| `wizard_screens.py` | All `QWizardPage` classes + `PromptWizard` + `ExportDialog` |
| `wizard.py` | `WizardApp` (QMainWindow), QSS themes, entry point |

`PromptWizard` is a `QWizard` (ModernStyle) embedded in `WizardApp` alongside a live `PromptSidebar`. The sidebar is injected into the wizard and refreshed after each page commit.

---

## Full Flow

```
Welcome
  â””â”€â–º Use Case (multi-select, â‰¥1 required)
        â”‚
        â”œâ”€â–º [Software Development selected]
        â”‚     A1  What kind of help?        (multi-select, all pre-selected)
        â”‚     A2  Technologies              (multi-select)          [skippable]
        â”‚     A3  Project type             (script / hobby / production)
        â”‚     A4  Project information      (free text + file import) [skippable]
        â”‚    [A5  Production guardrails]   (only if Production in A3) [skippable]
        â”‚
        â”œâ”€â–º [Learning & Teaching selected]
        â”‚     B1  Teaching style + technologies
        â”‚
        â”œâ”€â–º [Coaching & Growth selected]
        â”‚     C1  Coach expertise
        â”‚
        â”œâ”€â–º [Research & Analysis selected]
        â”‚     (silent â€” Researcher role added, no page shown)
        â”‚
        â”œâ”€â–º [Creative Work selected]
        â”‚     E1  Creative type
        â”‚
        â””â”€â–º [Professional / Business selected]
              F1  Business domain
                    â”‚
                    â–¼  (all branches converge â€” always shown)
              S1  Thinking & Communication Style
              S3  Protocols                   (optional) [skippable]
              S4  Custom Instructions         (optional) [skippable]
              S5  Preview + Export
```

> **Note:** S2 and S6 from earlier designs are removed. S1 absorbs communication/behavioral content; export is handled by a dialog popup on S5.

---

## Persistent Sidebar (all pages)

A 290px fixed-width panel on the right shows a live HTML summary:

```
â”Œâ”€â”€â”€ Prompt Summary â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Use cases:                  â”‚
â”‚   â€¢ Software Dev            â”‚
â”‚   â€¢ Research                â”‚
â”‚                             â”‚
â”‚ Roles:                      â”‚
â”‚   â€¢ Software Engineer       â”‚
â”‚   â€¢ System Architect        â”‚
â”‚   â€¢ Researcher              â”‚
â”‚                             â”‚
â”‚ Technologies:               â”‚
â”‚   Python, TypeScript        â”‚
â”‚                             â”‚
â”‚ Project type: Production    â”‚
â”‚ Analytical: High            â”‚
â”‚ Creative: Medium            â”‚
â”‚ Interaction: High           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Refreshes after every page commit and on Back navigation.

---

## Global Controls

| Button | Location | Action |
|---|---|---|
| `â†º Start Over` | far left | Resets `WizardState` to defaults; restarts from Welcome |
| `Skip â†’` | right of Back | Advances without committing state (skippable pages only) |
| `â† Back` | standard | Returns to previous page |
| `Next â†’` | standard | Commits state and advances |
| `âœ“ Export` | final page only | Opens `ExportDialog` |
| `Exit` | far left | Closes the application |
| `â˜€ Light theme` / `ðŸŒ™ Dark theme` | top-right overlay | Toggles QSS theme |

Skippable pages: A2, A4, A5, S3, S4.

---

## Page 0 â€” Welcome

No selections. Orients the user with a brief description of what the wizard produces.

---

## Page 1 â€” Use Case Selection

**Widget:** `QListWidget` (checkboxes, multi-select)  
**Validation:** At least one required.

| Use Case | Branch | Roles silently added |
|---|---|---|
| Software Development | A1 â†’ A2 â†’ A3 â†’ A4 â†’ [A5] | depends on A1 |
| Learning & Teaching | B1 | Teacher (+ Socratic Guide if style = Socratic) |
| Coaching & Growth | C1 | depends on C1 |
| Research & Analysis | *(none)* | Researcher |
| Creative Work | E1 | depends on E1 |
| Professional / Business | F1 | depends on F1 |

---

## Branch A â€” Software Development

### A1 â€” What kind of help?

All items pre-checked by default. Deselect anything that doesn't apply.

| Selection | Role added |
|---|---|
| Write / implement code | `Software Engineer` |
| Design the architecture | `Software System Architect` |
| Research docs, repos, APIs | `Researcher` |
| Teach me while we build | `Teacher` |
| Review and critique my code | `Software Engineer` |

### A2 â€” Technologies *(skippable)*

`QListWidget` with all available technology presets from `TECH_OPTIONS`. Each checked item appends `presets/technologies/<lang>.txt`.

### A3 â€” Project Type

`QButtonGroup` (radio). Drives engineering rigour.

| Value | Instruction injected |
|---|---|
| `script` | Pragmatic, minimal â€” no test boilerplate unless asked |
| `hobby` | Encourage structure and tests, no strict coverage |
| `production` | Full rigour: tests required, incremental changes, alignment before deviating â€” **unlocks A5** |

### A4 â€” Project Information *(skippable)*

`ProjectInfoEdit` â€” a drag-and-drop `QPlainTextEdit` that accepts `.txt`/`.md` file drops. Buttons for file import and an **Inspection Helper** dialog.

**Inspection Helper** generates a ready-to-paste IDE agent prompt:
> *"Analyze this project very thoroughly, sample a significant number of files to figure out patterns and produce a concise, technical description covering: purpose, stack, architecture, modules, conventions, dependencies, design decisions, and common patterns. (about 500 words)"*

**Output in prompt:** Content renders as a dedicated `Project context:` section (not a list entry).

### A5 â€” Production Guardrails *(production only, skippable)*

All items pre-checked by default. Each checked item adds a guardrail instruction.

| Guardrail | Key |
|---|---|
| Confirm before destructive changes | `confirm_destructive` |
| Prefer reversible operations | `prefer_reversible` |
| Flag design deviations | `flag_deviations` |
| Never guess requirements | `no_guessing` |
| Propose test strategy alongside every implementation | `propose_tests` |

A free-text `QLineEdit` allows adding a custom guardrail.

---

## Branch B â€” Learning & Teaching

### B1 â€” Teaching Style

`QButtonGroup` (radio) + technology checklist (same as A2).

| Style | Roles added |
|---|---|
| Direct explanation | `Teacher` |
| Socratic | `Teacher` + `Socratic Guide` |
| Example-driven | `Teacher` |

---

## Branch C â€” Coaching & Growth

### C1 â€” Coach Expertise

`QListWidget` (multi-select). At least one required.

| Expertise | Role |
|---|---|
| Career & professional development | `Growth & Accountability Coach` |
| Fitness & physical health | `Fitness Coach` |
| Mental wellness & emotional support | `Mental Wellness Advisor` |
| Accountability & habit building | `Growth & Accountability Coach` |

---

## Branch E â€” Creative Work

### E1 â€” Creative Type

`QButtonGroup` â†’ one of: Storytelling/Fiction, Poetry, Screenwriting, World-building, Copywriting.

---

## Branch F â€” Professional / Business

### F1 â€” Business Domain

`QButtonGroup` â†’ one of: Business strategy, Finance & investment, Legal, Marketing & brand.

---

## Shared Pages

---

### S1 â€” Thinking & Communication Style

Single merged page (scrollable) covering cognitive profile, response length, user alignment, advice style, and behavioral policies.

#### Cognitive Profile

Two `NoWheelSlider` instances (0â€“4 range, tick labels, click/drag only â€” no mouse wheel).

| Slider | Labels | Default |
|---|---|---|
| Analytical depth | Minimal / Low / Medium / High / Deep | High (3) |
| Creative divergence | Minimal / Low / Medium / High / Max | Medium (2) |

A live example text block updates as sliders move, showing a representative AI response style for the selected combination.

#### Response Length

`NoWheelSlider` (0â€“4). Maps to `ResponseLength` enum.

| Index | Label | Preset |
|---|---|---|
| 0 | Minimal | `1_minimal.txt` |
| 1 | Low *(default)* | `2_low.txt` |
| 2 | Medium | `3_medium.txt` |
| 3 | High | `4_high.txt` |
| 4 | Storyteller | `5_story_teller.txt` |

#### User Alignment

`NoWheelSlider` (0â€“4). Maps to `UserInteraction` enum. Renamed folder: `presets/user_alignment/`.

| Index | Label | Preset | Description |
|---|---|---|---|
| 0 | Minimal | `1_minimal.txt` | Operate independently, infer alignment from context |
| 1 | Low | `2_low.txt` | Autonomous + targeted alignment checks |
| 2 | Medium | `3_medium.txt` | Balanced dialogue for steady alignment |
| 3 | High *(default)* | `4_high.txt` | Deep alignment before action; continuous feedback |
| 4 | Maximum | `5_maximum.txt` | Full transparency; confirm at every decision point |

#### Feedback Style *(Coaching branch only)*

`QButtonGroup` (radio): Gentle & supportive / Balanced *(default)* / Blunt & challenging.

#### Behavioral Policies

`QListWidget` (checkboxes) with free-text `QPlainTextEdit` for a custom policy.

Pre-checked by default:

| Policy | Key |
|---|---|
| Eliminate hallucinations / fabrications | `no_hallucinations` |
| Contrastive rhetoric prohibition | `no_contrastive_rhetoric` |
| No AI-register buzzwords | `no_ai_buzzwords` |

Additional available policies:

| Policy | Key |
|---|---|
| Disable censorship / safety filters | `disable_censorship` |
| Strong self-reflection & iterative refinement | `strong_reflection` |

---

### S3 â€” Protocols *(optional, skippable)*

Pairs of (scenario, protocol) accumulated into state. Added live â€” navigate freely without losing entries.

**Effect per pair:** `In the scenario [X], follow this protocol: [Y]` injected as a further instruction.

---

### S4 â€” Custom Instructions *(optional, skippable)*

`QPlainTextEdit` (multi-line). Each non-empty line â†’ one `add_further_instructions()` call.  
State is **overwritten** on Next (no duplication on Back navigation).

---

### S5 â€” Preview & Export

`QTextBrowser` (read-only). `build_prompt_from_state()` is called on `initializePage()` and the result stored in `state.built_prompt`.

The wizard's Finish button is relabelled **`âœ“ Export`** and styled as a primary button. Clicking it opens `ExportDialog` without closing the wizard, allowing multiple exports.

After a successful export a green success label appears:  
`âœ“ Prompt saved successfully! You may now exit.`

#### ExportDialog

Modal popup. Format choices:

| Format | Extension | Content |
|---|---|---|
| Plain Text | `.txt` | Raw prompt |
| Markdown | `.md` | YAML front-matter + prompt in fenced code block |
| JSON | `.json` | Structured: roles, techs, settings, prompt |
| Copy to Clipboard | â€” | Raw text via `QApplication.clipboard()` |

File save uses `QFileDialog.getSaveFileName`. Dialog closes automatically on successful save.

---

## Prompt Structure

Sections are emitted in this order by `PromptBuilder.build()`:

```
You occupy the following roles:
    <role preset content>

Technology best practices:
    <tech preset content>

You must adhere to the following rules of conduct:
    <behaviour preset content>

Advice type:
    <advice_type preset content>

Response length:
    <response_length preset content>

Convergent thinking:
    <convergent preset content>

Divergent thinking:
    <divergent preset content>

User interaction:
    <user_alignment preset content>

Project context:
    <project_info free text>

Further instructions:
    - <guardrail instructions>
    - <custom guardrail>
    - <protocol instructions>
    - <extra instructions>
    - <language restriction>
    - <behavioral policy instructions>
    - <custom policy>
```

---

## State Model

`WizardState` is a `@dataclass` in `wizard_state.py`. All computed values (roles list, tech list) are derived at build time in `wizard_prompt.build_prompt_from_state()` â€” the Back button can never cause stale or duplicated data.

```python
@dataclass
class WizardState:
    # Branch A
    use_cases:           list[str]       # e.g. ["software_dev", "research"]
    help_types:          list[str]       # A1 raw selections
    a2_techs:            list            # A2 enum values
    project_type:        str             # "script" | "hobby" | "production"
    project_info:        str             # free text
    guardrail_keys:      list[str]       # A5 keys
    custom_guardrail:    str

    # Branch B
    teaching_style:      str             # "direct" | "socratic" | "examples"
    b1_techs:            list

    # Branch C
    coach_types:         list[str]

    # Branch E / F
    creative_type:       str
    business_domain:     str

    # S1 â€” Cognitive
    convergent_level:    int             # 0â€“4 index into CONV_LEVELS
    divergent_level:     int             # 0â€“4 index into DIV_LEVELS

    # S1 â€” Communication
    interaction:         str             # UserInteraction enum name  (default: "HIGH")
    response_length:     str             # ResponseLength enum name   (default: "LOW")
    advice:              str             # AdviceType enum name        (default: "BALLANCED")
    language_restriction: str
    behavioral_policies: list[str]       # selected policy keys
    custom_policy:       str

    # S3 / S4
    protocols:           list[tuple[str, str]]
    extra_instructions:  list[str]

    # Output
    built_prompt:        str
```
