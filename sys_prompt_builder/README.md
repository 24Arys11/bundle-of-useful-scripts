
# Project Title

A prompt builder for generating high quality system prompts with ease.

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

## GUI Usage (Recommended)

Launch the `gui.py` with python `python gui.py`, or just double-click `launcher.bat` (on windows).

## CLI Usage

#### Simple:

Modify the `cli.py` with the options you like and run it. You may save the out in a file using this command `python cli.py > output.txt`. This would serve as your system propt for your favourite LLM.

#### Intermediare:

1. Add `.txt` files in the `presets` folder. Use sub-folders to organize your folder structure however you wish.
2. Add the options for your newly added prompts within the enums inside the `data.py` (or just modify my prompts)
3. Extend the `prompt_builder.py` to handle the new options (it's easy, just add your new variable, copy-paste a 3-line method and addapt it, then add another `if` in the `build` method)
4. Set the options in `cli.py` and run it. Use `python cli.py > output.txt` to save the output in `output.txt` file.

#### Advanced:

There is no advanced. It's really just a simple python script made in one evening. But it's very powerful if you need to create good system prompts quickly !


## Credits

1. The `behaviours/chaos_orb_dynamic` is inspired from [ThePrimeTime](https://www.youtube.com/@ThePrimeTimeagen) youtube channel in [this video](https://youtu.be/rzZXGlmWveo?t=560).
