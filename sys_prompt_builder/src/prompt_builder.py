from data import Roles, Behaviours, AdviceType, ResponseLength, Thinking, UserInteraction, Technologies

class PromptBuilder:
    def __init__(self):
        self.roles = []
        self.technologies = []
        self.behaviours = []
        self.advice_type = None
        self.response_length = None
        self.divergent_thinking = None
        self.convergent_thinking = None
        self.user_interaction = None
        self.further_instructions = []
        self.project_context = ""
        self.prompt = ""

    def add_role(self, role: Roles):
        self.roles.append(role)
        return self

    def add_technology(self, technology) -> 'PromptBuilder':
        """Add a technology-specific best practices preset."""
        self.technologies.append(technology)
        return self

    def enable_behaviour(self, behaviour: Behaviours):
        self.behaviours.append(behaviour)
        return self

    def set_advice_type(self, advice_type: AdviceType):
        self.advice_type = advice_type
        return self

    def set_response_length(self, length: ResponseLength):
        self.response_length = length
        return self

    def set_divergent_thinking(self, thinking: Thinking.Divergent):
        self.divergent_thinking = thinking
        return self

    def set_convergent_thinking(self, thinking: Thinking.Convergent):
        self.convergent_thinking = thinking
        return self

    def set_user_interaction(self, interaction: UserInteraction):
        self.user_interaction = interaction
        return self

    def set_project_context(self, context: str):
        """Set the project context block (rendered as its own section)."""
        self.project_context = context
        return self

    def add_further_instructions(self, instruction: str):
        self.further_instructions.append(f"    - {instruction}")

    def build(self):
        self.prompt = ""
        if self.roles:
            self.prompt += "You occupy the following roles:\n"
            for role in self.roles:
                with open(role.value, "r", encoding="utf-8") as file:
                    self.prompt += file.read() + "\n"
            self.prompt += "\n"
        
        if self.technologies:
            self.prompt += "Technology best practices:\n"
            for tech in self.technologies:
                with open(tech.value, "r", encoding="utf-8") as file:
                    self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.behaviours:
            self.prompt += "You must adhere to the following rules of conduct:\n"
            for behaviour in self.behaviours:
                with open(behaviour.value, "r", encoding="utf-8") as file:
                    self.prompt += file.read() + "\n"
            self.prompt += "\n"
        
        if self.advice_type:
            self.prompt += "Advice type:\n"
            with open(self.advice_type.value, "r", encoding="utf-8") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"
        
        if self.response_length:
            self.prompt += "Response length:\n"
            with open(self.response_length.value, "r", encoding="utf-8") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.convergent_thinking:
            self.prompt += "Convergent thinking:\n"
            with open(self.convergent_thinking.value, "r", encoding="utf-8") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.divergent_thinking:
            self.prompt += "Divergent thinking:\n"
            with open(self.divergent_thinking.value, "r", encoding="utf-8") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.user_interaction:
            self.prompt += "User interaction:\n"
            with open(self.user_interaction.value, "r", encoding="utf-8") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.project_context:
            self.prompt += "Project context:\n"
            self.prompt += self.project_context + "\n\n"

        if self.further_instructions:
            self.prompt += "Further instructions:\n"
            for instruction in self.further_instructions:
                self.prompt += instruction + "\n"
            self.prompt += "\n"

        self.prompt = self.prompt.rstrip("\n")
        print(self.prompt)
        return self.prompt
