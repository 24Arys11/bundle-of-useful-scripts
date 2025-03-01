from data import Roles, Behaviours, ResponseLength, Thinking, UserInteraction

class PromptBuilder:
    def __init__(self):
        self.roles = []
        self.behaviours = []
        self.response_length = None
        self.divergent_thinking = None
        self.convergent_thinking = None
        self.user_interaction = None
        self.further_instructions = []
        self.prompt = ""

    def add_role(self, role: Roles):
        self.roles.append(role)
        return self

    def enable_behaviour(self, behaviour: Behaviours):
        self.behaviours.append(behaviour)
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

    def add_further_instructions(self, instruction: str):
        self.further_instructions.append(f"    - {instruction}")

    def build(self):
        self.prompt = ""
        if self.roles:
            self.prompt += "You occupy the following roles:\n"
            for role in self.roles:
                with open(role.value, "r") as file:
                    self.prompt += file.read() + "\n"
            self.prompt += "\n"
        
        if self.behaviours:
            self.prompt += "You must adhere to the following rules of conduct:\n"
            for behaviour in self.behaviours:
                with open(behaviour.value, "r") as file:
                    self.prompt += file.read() + "\n"
            self.prompt += "\n"
        
        if self.response_length:
            self.prompt += "Response length:\n"
            with open(self.response_length.value, "r") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.convergent_thinking:
            self.prompt += "Convergent thinking:\n"
            with open(self.convergent_thinking.value, "r") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.divergent_thinking:
            self.prompt += "Divergent thinking:\n"
            with open(self.divergent_thinking.value, "r") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.user_interaction:
            self.prompt += "User interaction:\n"
            with open(self.user_interaction.value, "r") as file:
                self.prompt += file.read() + "\n"
            self.prompt += "\n"

        if self.further_instructions:
            self.prompt += "Further instructions:\n"
            for instruction in self.further_instructions:
                self.prompt += instruction + "\n"
            self.prompt += "\n"

        self.prompt = self.prompt.rstrip("\n")
        return self.prompt
