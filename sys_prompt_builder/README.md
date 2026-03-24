
# Sys Prompt Builder

A prompt builder for generating high-quality AI system prompts — either via a guided wizard or a developer control panel.

## Documentation

- [Wizard UX Flow](docs/wizard_flow.md)
- [Implementation Roadmap & Decisions Log](docs/wizard_impl_roadmap.md)

## Recommendations

While the `.vscode` folder is ignored by default, it is recommended to enable word wrap inside `.txt` files. You can do so by adding this to your `.vscode/settings.json` file:

```json
{
  "editor.wordWrap": "on",
  "files.associations": {
    "*.txt": "plaintext"
  }
}
```

## Wizard (Recommended — beginners)

A fully guided PySide6 wizard that builds a tailored system prompt step by step.
No prompt engineering knowledge needed.

**Launch:** double-click `launcher_wizard.bat` (Windows), or:
```
cd src && python wizard.py
```

**What it covers:**
- Use-case branching (software dev, learning, coaching, creative, business, research)
- Role and technology preset injection
- Cognitive profile — analytical depth + creative divergence sliders
- Response length and user alignment (interaction) sliders
- Behavioral policies (e.g. eliminate hallucinations, contrastive rhetoric prohibition, AI buzzword ban)
- Production guardrails when working on production-grade projects
- Custom scenario→protocol rules and extra instructions
- Live prompt sidebar that updates as you navigate
- Dark / Light theme toggle
- Export to `.txt`, `.md`, `.json`, or clipboard

## GUI Usage (Developer Control Panel)

Launch `gui.py` with Python, or double-click `launcher.bat` (Windows).
Full manual control over all preset combinations.

## CLI Usage

#### Simple:

Modify `cli.py` with the options you like and run it. Save output with `python cli.py > output.txt`.

#### Intermediate:

1. Add `.txt` files in the `presets/` folder. Use sub-folders to organise.
2. Add enum entries in `data.py`.
3. Extend `prompt_builder.py` (add field, method, and an `if` block in `build()`).
4. Set options in `cli.py` and run it.

#### Advanced:

There is no advanced. It's a simple Python script that produces powerful results.


## Credits

1. The `behaviours/chaos_orb_dynamic` preset is inspired by [ThePrimeTime](https://www.youtube.com/@ThePrimeTimeagen) in [this video](https://youtu.be/rzZXGlmWveo?t=560).
