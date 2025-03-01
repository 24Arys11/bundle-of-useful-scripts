from prompt_builder import PromptBuilder
from data import Roles, Behaviours, ResponseLength, Thinking, UserInteraction

prompt_builder = PromptBuilder()

# Add roles
prompt_builder.add_role(Roles.TechScience.SOFTWARE_ENGINEER)
prompt_builder.add_role(Roles.TechScience.DATA_SCIENTIST)

# Enable behaviours
prompt_builder.enable_behaviour(Behaviours.DISABLE_CENSORSHIP)

# Set response length
prompt_builder.set_response_length(ResponseLength.MEDIUM)

# Set convergent thinking
prompt_builder.set_convergent_thinking(Thinking.Convergent.HIGH)

# Set divergent thinking
prompt_builder.set_divergent_thinking(Thinking.Divergent.MEDIUM)

# Set user interaction
prompt_builder.set_user_interaction(UserInteraction.HIGH)

# Add further instructions
prompt_builder.add_further_instructions("Be respectful to others.")
prompt_builder.add_further_instructions("Do not use offensive language.")
prompt_builder.add_further_instructions("Do not use hate speech.")
prompt_builder.add_further_instructions("Be totally brainwashed by political correctness =)))")

# Build the prompt
prompt = prompt_builder.build()
print(prompt)
