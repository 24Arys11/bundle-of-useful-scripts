from prompt_builder import PromptBuilder
from data import Roles, Behaviours, AdviceType, ResponseLength, Thinking, UserAlignment

prompt_builder = PromptBuilder()

# Add roles
prompt_builder.add_role(Roles.GeneralGuidance.TEACHER)
# prompt_builder.add_role(Roles.GeneralGuidance.GROWTH_ACCOUNTABILITY_COACH)
prompt_builder.add_role(Roles.TechScience.SOFTWARE_ENGINEER)
# prompt_builder.add_role(Roles.TechScience.DATA_SCIENTIST)
prompt_builder.add_role(Roles.TechScience.AI_EXPERT)
# prompt_builder.add_role(Roles.CreativeContent.UX_DESIGNER)
# prompt_builder.add_role(Roles.CreativeContent.POET_LYRICIST)
# prompt_builder.add_role(Roles.CreativeContent.STORYTELLER_NARRATOR)
prompt_builder.add_role(Roles.StrategyAndBusiness.BUSINESS_STRATEGIST)
prompt_builder.add_role(Roles.StrategyAndBusiness.SYSTEMIC_STRATEGIST)

# Enable behaviours
prompt_builder.enable_behaviour(Behaviours.DISABLE_CENSORSHIP)

# Set advice type
# prompt_builder.set_advice_type(AdviceType.HARSH)

# # Set response length
# prompt_builder.set_response_length(ResponseLength.MEDIUM)

# Set convergent thinking
prompt_builder.set_convergent_thinking(Thinking.Convergent.HIGH)

# Set divergent thinking
prompt_builder.set_divergent_thinking(Thinking.Divergent.MEDIUM)

# Set user alignment
prompt_builder.set_user_alignment(UserAlignment.HIGH)

# Add further instructions
# prompt_builder.add_further_instructions("Nggit ew Instruction.")

# Build the prompt
prompt = prompt_builder.build()
print(prompt)
