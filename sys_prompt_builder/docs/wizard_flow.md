# Wizard UX Flow

Decision-tree survey design for the Textual-based prompt wizard (`wizard.py`).  
Each page maps to one Textual `Screen`. The user answers questions about their needs — the wizard maps answers to roles, presets and instructions behind the scenes.

**Target audience:** Beginners who want a tailored prompt without prompt engineering knowledge.  
**Developer control panel:** The existing `gui.py` (launched via `launcher.bat`) remains for power users.

---

## Full Flow

```
Welcome
  └─► Use Case (multi-select, ≥1 required)
        │
        ├─► [Software Development selected]
        │     A1  What kind of help?          (multi-select, all pre-selected)
        │     A2  Technologies                (multi-select from available presets)
        │     A3  Project type               (script / hobby / production)
        │     A4  Project information        (free text: architecture, stack, patterns)
        │    [A5  Production guardrails]      (only if Production selected in A3)
        │
        ├─► [Learning & Teaching selected]
        │     B1  Teaching style
        │
        ├─► [Coaching & Growth selected]
        │     C1  Coach expertise             (multi-select)
        │
        ├─► [Research & Analysis selected]
        │     (silent — Researcher role added, no page shown)
        │
        ├─► [Creative Work selected]
        │     E1  Creative type
        │
        └─► [Professional / Business selected]
              F1  Business domain
                    │
                    ▼  (all branches converge — always shown)
              S1  Cognitive Profile           (5×5 grid)
              S2  Communication Preferences
              S3  Protocols                   (optional)
              S4  Custom Instructions         (optional)
              S5  Preview
              S6  Export
```

---

## Persistent Sidebar (all pages)

A narrow right-hand panel shows a live summary of what has been collected so far:

```
┌─── Your Prompt So Far ──────┐
│ Use cases:                  │
│   • Software Development    │
│   • Research & Analysis     │
│                             │
│ Roles:                      │
│   • Software Engineer       │
│   • System Architect        │
│   • Researcher              │
│                             │
│ Technologies:               │
│   • Python, C++             │
│                             │
│ Project: Production         │
│ Cognitive: Med / High       │
│ Interaction: Medium         │
└─────────────────────────────┘
```

Updates reactively after every selection.

---

## Page 1 — Welcome

**Purpose:** Orient the user. No selections made here.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   Sys Prompt Wizard                                      │
│                                                          │
│   Build a tailored AI system prompt by answering a       │
│   few simple questions about what you need.              │
│                                                          │
│   You don't need any prompt engineering knowledge.       │
│   The wizard handles the rest.                           │
│                                                          │
│                      [  Start  ]                         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Footer:** `Ctrl+Q  Quit`

---

## Page 2 — Use Case Selection

**Purpose:** Determine which branch pages to show. At least one required.

```
┌──────────────── What do you need? ──────────────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  What do you want to use this AI assistant for? │  Use cases: (none)     │
│  Select all that apply.                         │                        │
│                                                 │                        │
│  ☐  Software Development                        │                        │
│     Write, design, review or learn code         │                        │
│                                                 │                        │
│  ☐  Learning & Teaching                         │                        │
│     Understand a topic or technology            │                        │
│                                                 │                        │
│  ☐  Coaching & Growth                           │                        │
│     Career, accountability, habits, wellbeing   │                        │
│                                                 │                        │
│  ☐  Research & Analysis                         │                        │
│     Deep-dive into topics or documents          │                        │
│                                                 │                        │
│  ☐  Creative Work                               │                        │
│     Writing, stories, scripts, ideas            │                        │
│                                                 │                        │
│  ☐  Professional / Business                     │                        │
│     Strategy, finance, legal, marketing         │                        │
│                                                 │                        │
│  [← Back]                          [Next →]     │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `SelectionList`  
**Validation:** At least one selection required. Shows inline warning if empty and Next is pressed.  
**Research & Analysis note:** No branch page is shown — the Researcher role is silently added to state.

| Use Case | Description | Branch pages |
| --- | --- | --- |
| Software Development | Write, design, review or learn code | A1 → A2 → A3 → A4 → [A5] |
| Learning & Teaching | Understand a topic or technology | B1 |
| Coaching & Growth | Career, accountability, habits, wellbeing | C1 |
| Research & Analysis | Deep-dive into topics or documents | *(silent — Researcher role added)* |
| Creative Work | Writing, stories, scripts, ideas | E1 |
| Professional / Business | Strategy, finance, legal, marketing | F1 |

---

## Branch A — Software Development

### Page A1 — What kind of help?

**Purpose:** Determine which roles to activate. All pre-selected by default.

```
┌──────── Software Development — Help Type ───────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  What do you need help with?                    │  Use cases:            │
│  Deselect anything that doesn't apply.          │   • Software Dev       │
│                                                 │                        │
│  ☑  Write / implement code                      │  Roles:                │
│  ☑  Design the architecture                     │   • Software Engineer  │
│  ☑  Research docs, repos, APIs                  │   • System Architect   │
│  ☑  Teach me while we build                     │   • Researcher         │
│  ☑  Review and critique my code                 │   • Teacher            │
│                                                 │                        │
│  [← Back]                          [Next →]     │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `SelectionList` (all items checked on mount)

| Selection | Role(s) added |
| --- | --- |
| Write / implement code | `Software Engineer` |
| Design the architecture | `Software System Architect` |
| Research docs, repos, APIs | `Researcher` |
| Teach me while we build | `Teacher` |
| Review and critique my code | `Software Engineer` *(if not already added)* |

---

### Page A2 — Technologies

**Purpose:** Add language/framework-specific best practice presets.

```
┌──────── Software Development — Technologies ────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  Which technologies are involved?               │  Technologies: (none)  │
│  Select all that apply.                         │                        │
│                                                 │                        │
│  ☐  Python                                      │                        │
│  ☐  C++                                         │                        │
│  ☐  TypeScript                                  │                        │
│  ☐  Go                                          │                        │
│  ☐  Rust                                        │                        │
│  ☐  Java                                        │                        │
│  ☐  C#                                          │                        │
│  ☐  SQL                                         │                        │
│                                                 │                        │
│  (Only technologies with available presets are  │                        │
│   shown. Use Custom Instructions for anything   │                        │
│   not listed.)                                  │                        │
│                                                 │                        │
│  [← Back]                   [Skip]  [Next →]    │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `SelectionList`  
**Skip:** Allowed.  
**Effect:** Each selected technology appends the corresponding `presets/technologies/<lang>.txt`.

| Technology | Preset file |
| --- | --- |
| Python | `presets/technologies/python.txt` |
| C++ | `presets/technologies/cpp.txt` |
| TypeScript | `presets/technologies/typescript.txt` |
| Go | `presets/technologies/go.txt` |
| Rust | `presets/technologies/rust.txt` |
| Java | `presets/technologies/java.txt` |
| C# | `presets/technologies/csharp.txt` |
| SQL | `presets/technologies/sql.txt` |

---

### Page A3 — Project Type

**Purpose:** Set overall engineering rigour. Drives test, review and caution instructions.

```
┌──────── Software Development — Project Type ────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  What kind of project is this?                  │  Project: (none)       │
│                                                 │                        │
│  ○  Quick script                                │                        │
│     Pragmatic. No test boilerplate.             │                        │
│     Get it working, keep it simple.             │                        │
│                                                 │                        │
│  ○  Hobby / Personal project                    │                        │
│     Some structure. Tests welcome               │                        │
│     but no strict coverage targets.             │                        │
│                                                 │                        │
│  ○  Production grade                            │                        │
│     Full rigour. Tests required.                │                        │
│     Small safe changes. Extra guardrails page   │                        │
│     follows.                                    │                        │
│                                                 │                        │
│  [← Back]                          [Next →]     │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `RadioSet`  
**Validation:** One option required.  
**Effect — Script:** Adds instruction: *"Keep solutions pragmatic and minimal. Do not add test boilerplate unless asked."*  
**Effect — Hobby:** Adds instruction: *"Encourage good structure and tests, but without strict coverage requirements."*  
**Effect — Production:** Adds instruction: *"Apply full engineering rigour: tests required, careful incremental changes, seek alignment before deviating from agreed design."* → unlocks Page A5.

---

### Page A4 — Project Information

**Purpose:** Inject context about the specific project into the prompt.

```
┌──────── Software Development — Project Info ────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  Describe your project (optional).              │                        │
│                                                 │                        │
│  Include anything relevant: architecture,       │                        │
│  tech stack, patterns, constraints, team        │                        │
│  conventions, coding standards, etc.            │                        │
│                                                 │                        │
│ ┌─────────────────────────────────────────────┐ │                        │
│ │ e.g. "FastAPI backend, PostgreSQL, layered  │ │                        │
│ │ architecture (domain / service / repo),     │ │                        │
│ │ async throughout, pytest for tests."        │ │                        │
│ │                                             │ │                        │
│ └─────────────────────────────────────────────┘ │                        │
│                                                 │                        │
│  [← Back]                   [Skip]  [Next →]    │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `TextArea` (multi-line, optional)  
**Effect:** Content appended under a `Project context:` heading in the prompt.

---

### Page A5 — Production Guardrails *(only if Production selected in A3)*

**Purpose:** Let the user opt into specific safety/process guardrails for production work.

```
┌──────── Software Development — Guardrails ──────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  Additional production guardrails (optional).   │                        │
│  Check those that apply to your project.        │                        │
│                                                 │                        │
│  ☐  Ask for confirmation before destructive     │                        │
│     changes (deletes, drops, rewrites)          │                        │
│                                                 │                        │
│  ☐  Prefer reversible operations where possible │                        │
│                                                 │                        │
│  ☐  Flag any deviation from the agreed design   │                        │
│     before implementing it                      │                        │
│                                                 │                        │
│  ☐  Never guess a requirement — ask instead     │                        │
│                                                 │                        │
│  ☐  Always propose a test strategy alongside    │                        │
│     each implementation                         │                        │
│                                                 │                        │
│  [ + Add a custom guardrail... ]                │                        │
│                                                 │                        │
│  [← Back]                   [Skip]  [Next →]    │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `SelectionList` + inline `Input` that appends to the list on confirm  
**Effect:** Each checked item becomes a protocol entry: `In the scenario [X], follow this protocol: [Y]`

| Guardrail | Scenario injected |
| --- | --- |
| Confirm before destructive changes | Before deletes, drops, or full rewrites |
| Prefer reversible operations | When multiple approaches are available |
| Flag design deviations | When about to deviate from the agreed design |
| Never guess requirements | When a requirement is ambiguous or missing |
| Propose test strategy | Alongside every new implementation |

---

## Branch B — Learning & Teaching

### Page B1 — Teaching Style

```
┌──────── Learning & Teaching ────────────────────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  How should the AI teach you?                   │  Roles: Teacher        │
│                                                 │                        │
│  ◉  Direct explanation                          │                        │
│     Clear, complete explanations of each topic  │                        │
│                                                 │                        │
│  ○  Socratic                                    │                        │
│     Guide me to the answer with questions       │                        │
│                                                 │                        │
│  ○  Example-driven                              │                        │
│     Show me first, then explain                 │                        │
│                                                 │                        │
│  Any specific technology you're learning?       │                        │
│  (same list as A2 — adds the same presets)      │                        │
│  ☐ Python  ☐ C++  ☐ TypeScript  ☐ ...          │                        │
│                                                 │                        │
│  [← Back]                          [Next →]     │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

| Teaching style | Role(s) added |
| --- | --- |
| Direct explanation | `Teacher` |
| Socratic | `Teacher` + `Socratic Guide` |
| Example-driven | `Teacher` |

---

## Branch C — Coaching & Growth

### Page C1 — Coach Expertise

```
┌──────── Coaching & Growth ──────────────────────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  What expertise should your coach have?         │  Roles: (none yet)     │
│  Select all that apply.                         │                        │
│                                                 │                        │
│  ☐  Career & professional development           │                        │
│  ☐  Fitness & physical health                   │                        │
│  ☐  Mental wellness & emotional support         │                        │
│  ☐  Accountability & habit building             │                        │
│                                                 │                        │
│  [← Back]                          [Next →]     │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `SelectionList`  
**Validation:** At least one required.

| Expertise | Role preset |
| --- | --- |
| Career & professional development | `Growth & Accountability Coach` |
| Fitness & physical health | `Fitness Coach` |
| Mental wellness & emotional support | `Mental Wellness Advisor` |
| Accountability & habit building | `Growth & Accountability Coach` |

---

## Branch E — Creative Work

### Page E1 — Creative Type

```
┌──────── Creative Work ──────────────────────────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  What kind of creative work?                    │                        │
│                                                 │                        │
│  ○  Storytelling / Fiction                      │                        │
│  ○  Poetry                                      │                        │
│  ○  Screenwriting                               │                        │
│  ○  World-building / Lore                       │                        │
│  ○  Copywriting / Marketing                     │                        │
│                                                 │                        │
│  [← Back]                          [Next →]     │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `RadioSet`

---

## Branch F — Professional / Business

### Page F1 — Business Domain

```
┌──────── Professional / Business ────────────────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  What domain?                                   │                        │
│                                                 │                        │
│  ○  Business strategy                           │                        │
│  ○  Finance & investment                        │                        │
│  ○  Legal                                       │                        │
│  ○  Marketing & brand                           │                        │
│                                                 │                        │
│  [← Back]                          [Next →]     │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `RadioSet`

---

## Shared Pages (always shown, regardless of use cases)

---

### Page S1 — Cognitive Profile

**Purpose:** Set both convergent (analytical depth) and divergent (creativity) thinking with a single click on an interactive grid.

```
┌──────── Cognitive Profile ──────────────────────────────────────────────┐
│                                                                         │
│  How should the AI think?                                               │
│  Click the cell that best matches the responses you want.               │
│                                                                         │
│  Example question: "How would you reduce latency in a                   │
│  distributed system?"                                                   │
│                                                                         │
│              ◄──────────── Analytical depth ────────────►              │
│              Minimal      Low      Medium     High      Max             │
│  ▲  Max    [ Imaginat. ][ Wild  ][ Vision- ][ Vision ][ Visionary]     │
│  C         [ leap     ][ ideas ][ ary+str ][+rigour ][+exhausti.]      │
│  r                                                                      │
│  e  High   [ Creative ][ Ideas ][ Innovat.][ Innov. ][ Innovat. ]      │
│  a         [ only     ][ +some ][ +struct][+deep   ][+thorough ]       │
│  t                                                                      │
│  i  Medium [ Simple   ][ Clear ][★ Balanc][Thorough][ Rigorous ]      │
│  v         [ take     ][ conci-][ ed ★   ][        ][ +grounded]      │
│  i         [          ][ se    ][        ][        ][          ]       │
│  t                                                                      │
│  y  Low    [ Blunt    ][ Terse ][ Solid  ][ Solid  ][ Precise  ]      │
│  │         [          ][       ][        ][ +refs  ][ +thorough]      │
│  │                                                                      │
│  ▼  Min    [ One word ][ Brief ][ Short  ][ Concise][ Dense    ]      │
│            [          ][       ][ factual][ +ref   ][ factual  ]      │
│                                                                         │
│  Selected: Medium creativity / Medium analytical depth  (★ default)    │
│                                                                         │
│  [← Back]                                        [Next →]              │
└─────────────────────────────────────────────────────────────────────────┘
```

**Widget:** 5×5 grid of `Button` widgets  
- **Columns** = Convergent levels: Minimal → Low → Medium → High → Deep Analysis  
- **Rows** = Divergent levels: Max → High → Medium → Low → Minimal (top row = most creative)  
- Each cell shows a 2–3 word label describing what the AI's response feels like at that combination  
- Clicking a cell selects it (highlighted); previous selection is cleared  
- Default: centre cell Medium/Medium (marked ★)  
- A plain-English summary line below the grid updates on every click  

**Effect:** Sets both `convergent_thinking` and `divergent_thinking` in `WizardState`.

| | Minimal | Low | Medium | High | Deep Analysis |
| --- | --- | --- | --- | --- | --- |
| **Max creativity** | Imaginative leap | Wild ideas | Visionary + structure | Vision + rigour | Visionary + exhaustive |
| **High creativity** | Creative only | Ideas + some | Innovative + struct | Innovative + deep | Innovative + thorough |
| **Medium creativity** | Simple take | Clear, concise | ★ **Balanced** | Thorough | Rigorous + grounded |
| **Low creativity** | Blunt | Terse | Solid | Solid + refs | Precise + thorough |
| **Minimal creativity** | One word | Brief | Short factual | Concise + ref | Dense factual |

---

### Page S2 — Communication Preferences

```
┌──────── Communication Preferences ──────────────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  How interactive should the AI be?              │                        │
│                                                 │                        │
│  ○  Minimal    — answers only, no questions     │                        │
│  ○  Low        — asks only when truly stuck     │                        │
│  ◉  Medium     — asks when genuinely uncertain  │                        │
│  ○  High       — actively checks understanding  │                        │
│  ○  Babysitter — guides every step              │                        │
│                                                 │                        │
│  ──────────────────────────────────────────     │                        │
│                                                 │                        │
│  [shown only if Coaching branch selected]       │                        │
│  How should feedback and advice be delivered?   │                        │
│                                                 │                        │
│  ○  Gentle & supportive                         │                        │
│  ◉  Balanced                                    │                        │
│  ○  Blunt & challenging                         │                        │
│                                                 │                        │
│  ──────────────────────────────────────────     │                        │
│                                                 │                        │
│  Language / style restrictions (optional):      │                        │
│  ┌─────────────────────────────────────────┐   │                        │
│  │ e.g. "Always respond in formal English" │   │                        │
│  └─────────────────────────────────────────┘   │                        │
│                                                 │                        │
│  [← Back]                   [Skip]  [Next →]    │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widgets:** `RadioSet` (interaction level), conditional `RadioSet` (advice type — Coaching branch only), `Input` (language restriction)

| Interaction level | Behaviour |
| --- | --- |
| Minimal | Answers only — never asks clarifying questions |
| Low | Asks only when truly stuck |
| Medium *(default)* | Asks when genuinely uncertain |
| High | Actively checks understanding throughout |
| Babysitter | Guides every step, checks in constantly |

*Advice delivery (Coaching branch only):*

| Advice style | Description |
| --- | --- |
| Gentle & supportive | Encouraging, positive framing |
| Balanced *(default)* | Honest and constructive |
| Blunt & challenging | Direct, pushes back, no sugar-coating |

---

### Page S3 — Protocols *(optional)*

**Purpose:** Define explicit scenario → behaviour rules.

```
┌──────── Protocols ──────────────────────────────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  Define how the AI should behave in specific    │  Protocols: (none)     │
│  situations. Leave empty to skip.               │                        │
│                                                 │                        │
│  Scenario:                                      │                        │
│  ┌─────────────────────────────────────────┐   │                        │
│  │ When I paste a block of code            │   │                        │
│  └─────────────────────────────────────────┘   │                        │
│                                                 │                        │
│  Protocol:                                      │                        │
│  ┌─────────────────────────────────────────┐   │                        │
│  │ Always identify bugs before suggesting  │   │                        │
│  │ improvements                            │   │                        │
│  └─────────────────────────────────────────┘   │                        │
│                                                 │                        │
│  [ + Add another protocol ]                     │                        │
│                                                 │                        │
│  Added so far:                                  │                        │
│  • When I paste code → identify bugs first      │                        │
│                                                 │                        │
│  [← Back]                   [Skip]  [Next →]    │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widgets:** `Input` (scenario) + `TextArea` (protocol) + `Button` (add) + `ListView` (summary)  
**Effect per pair:** `In the scenario [X], follow this protocol: [Y]` under a `Protocols:` section.

| Field | Description |
| --- | --- |
| Scenario | A short description of a situation (e.g. *"When I paste a block of code"*) |
| Protocol | What the AI should do in that situation (multi-line, as specific as needed) |
| Added list | Running list shown below the form; each entry can be removed before proceeding |

---

### Page S4 — Custom Instructions *(optional)*

```
┌──────── Custom Instructions ────────────────────┬── Your Prompt So Far ──┐
│                                                 │                        │
│  Anything else you want to tell the AI?         │                        │
│  Appended as-is. Leave empty to skip.           │                        │
│                                                 │                        │
│ ┌─────────────────────────────────────────────┐ │                        │
│ │                                             │ │                        │
│ │                                             │ │                        │
│ │                                             │ │                        │
│ └─────────────────────────────────────────────┘ │                        │
│                                                 │                        │
│  [← Back]                   [Skip]  [Next →]    │                        │
└─────────────────────────────────────────────────┴────────────────────────┘
```

**Widget:** `TextArea` (multi-line)  
**Effect:** Each non-empty line → one `add_further_instructions()` call.

---

### Page S5 — Preview

**Purpose:** Show the fully assembled prompt. Read-only before export.

```
┌──────── Preview ────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ You occupy the following roles:                                   │  │
│  │     - **Software Engineer**: As a professional software engineer  │  │
│  │       you specialize in...                                        │  │
│  │     - **Software System Architect**: ...                          │  │
│  │                                                                   │  │
│  │ Project context:                                                  │  │
│  │     FastAPI backend, PostgreSQL, layered architecture...          │  │
│  │                                                                   │  │
│  │ Protocols:                                                        │  │
│  │     In the scenario [I paste a block of code], follow this        │  │
│  │     protocol: [identify bugs before suggesting improvements]      │  │
│  │ ...                                                               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  [← Back]                                            [Export →]         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Widget:** `TextArea` (read-only, scrollable)  
**Source:** `PromptBuilder.build()` output

---

### Page S6 — Export

```
┌──────── Export ─────────────────────────────────────────────────────────┐
│                                                                         │
│  Choose export format(s):                                               │
│                                                                         │
│   ☑  Plain Text  (.txt)                                                 │
│   ☐  Markdown    (.md)                                                  │
│   ☐  JSON        (.json)   includes metadata: roles, settings, etc.    │
│   ☐  Clipboard                                                          │
│                                                                         │
│  Filename (without extension):                                          │
│  ┌────────────────────────────┐                                         │
│  │ my_prompt                  │                                         │
│  └────────────────────────────┘                                         │
│                                                                         │
│  Save location: src/output/                                             │
│                                                                         │
│  [← Back]    [✓ Export]    [Start Over]    [Quit]                       │
└─────────────────────────────────────────────────────────────────────────┘
```

**Export formats:**

| Format | Extension | Content |
| --- | --- | --- |
| Plain Text | `.txt` | Raw prompt text (identical to existing `output.txt`) |
| Markdown | `.md` | Metadata header + prompt in a fenced code block |
| JSON | `.json` | Structured: `{ "roles": [...], "technologies": [...], ..., "prompt": "..." }` |
| Clipboard | — | Raw text via platform shell (`clip` / `xclip` / `pbcopy`) — no extra dep |

**`Start Over`** resets all wizard state and returns to Page 1.

---

## Navigation & Global Controls

| Action | Keyboard | Mouse |
|---|---|---|
| Next page | `Tab` to button + `Enter` | Click `[Next →]` |
| Previous page | `Escape` | Click `[← Back]` |
| Skip page | — | Click `[Skip]` (where available) |
| Quit | `Ctrl+Q` | — |
| Key bindings help | `F1` | — |

**Footer** (persistent): shows current page label + available shortcuts.

---

## State Model

A single `WizardState` dataclass flows through all screens by reference:

```python
@dataclass
class WizardState:
    # Use case
    use_cases: list[str]                     # e.g. ["software_dev", "research"]

    # Roles (resolved from all branch answers)
    roles: list                              # Roles enum values

    # Technology presets
    technologies: list                       # Technologies enum values

    # Project (software dev branch)
    project_type: str | None                 # "script" | "hobby" | "production" | None
    project_info: str                        # free text

    # Cognitive
    convergent_thinking: Thinking.Convergent | None
    divergent_thinking: Thinking.Divergent | None

    # Communication
    user_interaction: UserInteraction | None
    advice_type: AdviceType | None           # only set if Coaching branch selected

    # Language restriction
    language_restriction: str               # free text, empty = no restriction

    # Protocols
    protocols: list[tuple[str, str]]         # [(scenario, protocol), ...]

    # Custom instructions
    extra_instructions: list[str]

    # Output
    built_prompt: str                        # populated on S5 Preview
```
