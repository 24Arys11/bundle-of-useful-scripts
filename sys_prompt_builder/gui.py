# Generated with GitHub Copilot

import tkinter as tk
from tkinter import ttk
from prompt_builder import PromptBuilder
from data import Roles, Behaviours, AdviceType, ResponseLength, Thinking, UserInteraction
import json
import os

class PromptBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Prompt Builder")
        self.prompt_builder = PromptBuilder()
        self.selected_roles = []
        self.selected_behaviours = []
        self.selected_advice_type = None
        self.selected_response_length = None
        self.selected_divergent_thinking = None
        self.selected_convergent_thinking = None
        self.selected_user_interaction = None

        self.config_file = "config.json"
        self.theme = self.load_theme()
        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.left_frame = ttk.Frame(self.root, padding="10")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.output_text = tk.Text(self.right_frame, wrap="word", width=80, height=45)
        self.output_text.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.output_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=self.scrollbar.set)

        self.copy_button = ttk.Button(self.right_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=1, column=0, pady=10, sticky="e")

        self.create_role_buttons()
        self.create_behaviour_buttons()
        self.create_advice_type_buttons()
        self.create_response_length_buttons()
        self.create_thinking_buttons()
        self.create_user_interaction_buttons()

        self.build_button = ttk.Button(self.left_frame, text="Build Prompt", command=self.build_prompt)
        self.build_button.grid(row=100, column=5, pady=10, sticky="se")

        self.theme_button = ttk.Button(self.left_frame, text="Dark Theme" if self.theme == "light" else "Light Theme", command=self.toggle_theme)
        self.theme_button.grid(row=100, column=0, pady=10, sticky="sw")

    def create_role_buttons(self):
        roles = Roles.get_all_roles()
        row = 0
        label = ttk.Label(self.left_frame, text="Roles")
        label.grid(row=row, column=0, sticky="w", padx=5)  # Add padding between columns
        row += 1
        for category, role_list in roles.items():
            label = ttk.Label(self.left_frame, text=category)
            label.grid(row=row, column=0, sticky="w", padx=5)  # Add padding between columns
            row += 1
            for role in role_list:
                var = tk.BooleanVar(value=False)
                button = ttk.Checkbutton(self.left_frame, text=role.name, variable=var, command=lambda r=role: self.toggle_role(r))
                button.var = var
                button.grid(row=row, column=0, sticky="w", padx=5)  # Add padding between columns
                row += 1

    def create_behaviour_buttons(self):
        label = ttk.Label(self.left_frame, text="Behaviours")
        label.grid(row=0, column=1, sticky="w", padx=5)  # Add padding between columns
        row = 1
        for behaviour in Behaviours.get_all_behaviours():
            var = tk.BooleanVar(value=False)
            button = ttk.Checkbutton(self.left_frame, text=behaviour.name, variable=var, command=lambda b=behaviour: self.toggle_behaviour(b))
            button.var = var
            button.grid(row=row, column=1, sticky="w", padx=5)  # Add padding between columns
            row += 1

    def create_advice_type_buttons(self):
        label = ttk.Label(self.left_frame, text="Advice Types")
        label.grid(row=0, column=2, sticky="w", padx=5)  # Add padding between columns
        row = 1
        self.advice_var = tk.StringVar(value="no_change")
        button = ttk.Radiobutton(self.left_frame, text="UNPROMPTED", value="no_change", variable=self.advice_var, command=lambda: self.set_advice_type(None))
        button.grid(row=row, column=2, sticky="w", padx=5)  # Add padding between columns
        row += 1
        for advice_type in AdviceType.get_all_advice_types():
            button = ttk.Radiobutton(self.left_frame, text=advice_type.name, value=advice_type, variable=self.advice_var, command=lambda a=advice_type: self.set_advice_type(a))
            button.grid(row=row, column=2, sticky="w", padx=5)  # Add padding between columns
            row += 1

    def create_response_length_buttons(self):
        label = ttk.Label(self.left_frame, text="Response Lengths")
        label.grid(row=0, column=3, sticky="w", padx=5)  # Add padding between columns
        row = 1
        self.response_var = tk.StringVar(value="no_change")
        button = ttk.Radiobutton(self.left_frame, text="UNPROMPTED", value="no_change", variable=self.response_var, command=lambda: self.set_response_length(None))
        button.grid(row=row, column=3, sticky="w", padx=5)  # Add padding between columns
        row += 1
        for response_length in ResponseLength.get_all_response_lengths():
            button = ttk.Radiobutton(self.left_frame, text=response_length.name, value=response_length, variable=self.response_var, command=lambda r=response_length: self.set_response_length(r))
            button.grid(row=row, column=3, sticky="w", padx=5)  # Add padding between columns
            row += 1

    def create_thinking_buttons(self):
        thinking_types = Thinking.get_all_thinking_types()
        row = 0
        self.thinking_vars = []
        for category, thinking_list in thinking_types.items():
            label = ttk.Label(self.left_frame, text=category)
            label.grid(row=row, column=4, sticky="w", padx=5)  # Add padding between columns
            row += 1
            thinking_var = tk.StringVar(value="no_change")
            self.thinking_vars.append(thinking_var)
            button = ttk.Radiobutton(self.left_frame, text="UNPROMPTED", value="no_change", variable=thinking_var, command=lambda: self.set_thinking(None, category))
            button.grid(row=row, column=4, sticky="w", padx=5)  # Add padding between columns
            row += 1
            for thinking in thinking_list:
                button = ttk.Radiobutton(self.left_frame, text=thinking.name, value=thinking, variable=thinking_var, command=lambda t=thinking, c=category: self.set_thinking(t, c))
                button.grid(row=row, column=4, sticky="w", padx=5)  # Add padding between columns
                row += 1
            row += 1

    def create_user_interaction_buttons(self):
        label = ttk.Label(self.left_frame, text="User Interactions")
        label.grid(row=0, column=5, sticky="w", padx=5)  # Add padding between columns
        row = 1
        self.interaction_var = tk.StringVar(value="no_change")
        button = ttk.Radiobutton(self.left_frame, text="UNPROMPTED", value="no_change", variable=self.interaction_var, command=lambda: self.set_user_interaction(None))
        button.grid(row=row, column=5, sticky="w", padx=5)  # Add padding between columns
        row += 1
        for interaction in UserInteraction.get_all_user_interactions():
            button = ttk.Radiobutton(self.left_frame, text=interaction.name, value=interaction, variable=self.interaction_var, command=lambda i=interaction: self.set_user_interaction(i))
            button.grid(row=row, column=5, sticky="w", padx=5)  # Add padding between columns
            row += 1

    def toggle_role(self, role):
        if role in self.selected_roles:
            self.selected_roles.remove(role)
        else:
            self.selected_roles.append(role)

    def toggle_behaviour(self, behaviour):
        if behaviour in self.selected_behaviours:
            self.selected_behaviours.remove(behaviour)
        else:
            self.selected_behaviours.append(behaviour)

    def set_advice_type(self, advice_type):
        self.selected_advice_type = advice_type

    def set_response_length(self, response_length):
        self.selected_response_length = response_length

    def set_thinking(self, thinking, category):
        if category == "Divergent":
            self.selected_divergent_thinking = thinking
        elif category == "Convergent":
            self.selected_convergent_thinking = thinking

    def set_user_interaction(self, interaction):
        self.selected_user_interaction = interaction

    def build_prompt(self):
        self.prompt_builder.roles = self.selected_roles
        self.prompt_builder.behaviours = self.selected_behaviours
        self.prompt_builder.advice_type = self.selected_advice_type
        self.prompt_builder.response_length = self.selected_response_length
        self.prompt_builder.divergent_thinking = self.selected_divergent_thinking
        self.prompt_builder.convergent_thinking = self.selected_convergent_thinking
        self.prompt_builder.user_interaction = self.selected_user_interaction

        prompt = self.prompt_builder.build()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, prompt)

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get(1.0, tk.END).strip())
        self.root.update()  # now it stays on the clipboard after the window is closed

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()
        self.save_theme()

    def apply_theme(self):
        if self.theme == "light":
            self.root.style = ttk.Style()
            self.root.style.theme_use('clam')
            self.root.style.configure('TFrame', background='white')
            self.root.style.configure('TLabel', background='white', foreground='black')
            self.root.style.configure('TButton', background='lightgrey', foreground='black')
            self.root.style.configure('TRadiobutton', background='white', foreground='black')
            self.root.style.configure('TCheckbutton', background='white', foreground='black')
            self.output_text.config(bg='#f0f0f0', fg='black', insertbackground='black')
            self.theme_button.config(text="Dark Theme")
        else:
            self.root.style = ttk.Style()
            self.root.style.theme_use('clam')
            self.root.style.configure('TFrame', background='#2e2e2e')
            self.root.style.configure('TLabel', background='#2e2e2e', foreground='white')
            self.root.style.configure('TButton', background='#444444', foreground='white')
            self.root.style.configure('TRadiobutton', background='#2e2e2e', foreground='white')
            self.root.style.configure('TCheckbutton', background='#2e2e2e', foreground='white')
            self.output_text.config(bg='#3e3e3e', fg='white', insertbackground='white')
            self.theme_button.config(text="Light Theme")

    def save_theme(self):
        with open(self.config_file, 'w') as config:
            json.dump({"theme": self.theme}, config)

    def load_theme(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as config:
                return json.load(config).get("theme", "light")
        return "light"

if __name__ == "__main__":
    root = tk.Tk()
    app = PromptBuilderGUI(root)
    root.mainloop()
