from enum import Enum

class Roles:
    class BusinessFinance(Enum):
        FINANCIAL_ANALYST = "presets/roles/business_finance/financial_analyst.txt"
        LEGAL_ADVISOR = "presets/roles/business_finance/legal_advisor.txt"
        # Add more roles as needed

    class StrategyAndBusiness(Enum):
        BUSINESS_STRATEGIST = "presets/roles/strategy_business/business_strategist.txt"
        SYSTEMIC_STRATEGIST = "presets/roles/strategy_business/systemic_strategist.txt"
        # Add more roles as needed

    class CreativeContent(Enum):
        COPYWRITER_MARKETER = "presets/roles/creative_content/copywriter_marketer.txt"
        POET_LYRICIST = "presets/roles/creative_content/poet_lyricist.txt"
        SCREENWRITER = "presets/roles/creative_content/screenwriter.txt"
        STORYTELLER_NARRATOR = "presets/roles/creative_content/storyteller_narrator.txt"
        UX_DESIGNER = "presets/roles/creative_content/ux_designer.txt"
        # Add more roles as needed

    class GeneralGuidance(Enum):
        CONSULTANT = "presets/roles/general_guidance/consultant.txt"
        DEBATE_OPPONENT = "presets/roles/general_guidance/debate_opponent.txt"
        RESEARCHER = "presets/roles/general_guidance/researcher.txt"
        SOCRATIC_GUIDE = "presets/roles/general_guidance/socratic_guide.txt"
        TEACHER = "presets/roles/general_guidance/teacher.txt"
        GROWTH_ACCOUNTABILITY_COACH = "presets/roles/general_guidance/growth_n_accountability_coach.txt"
        # Add more roles as needed

    class HealthWellbeing(Enum):
        FITNESS_COACH = "presets/roles/health_wellbeing/fitness_coach.txt"
        MENTAL_WELLNESS_ADVISOR = "presets/roles/health_wellbeing/mental_wellness_advisor.txt"
        # Add more roles as needed

    class SpecializedUnique(Enum):
        COMEDIAN = "presets/roles/specialized_unique/comedian.txt"
        DUNGEON_MASTER = "presets/roles/specialized_unique/dungeon_master.txt"
        HISTORIAN = "presets/roles/specialized_unique/historian.txt"
        RPG_BLCKSMITH_NPC = "presets/roles/specialized_unique/rpg_blacksmith_npc.txt"
        SCIENCE_FICTION_WORLD_BUILDER = "presets/roles/specialized_unique/science_fiction_world_builder.txt"
        # Add more roles as needed

    class TechScience(Enum):
        AI_EXPERT = "presets/roles/tech_science/ai_expert.txt"
        BLOCKCHAIN_EXPERT = "presets/roles/tech_science/blockchain_expert.txt"
        CYBERSECURITY_SPECIALIST = "presets/roles/tech_science/cybersecurity_specialist.txt"
        DATA_SCIENTIST = "presets/roles/tech_science/data_scientist.txt"
        SOFTWARE_ENGINEER = "presets/roles/tech_science/software_engineer.txt"
        # Add more roles as needed

class Behaviours(Enum):
    DISABLE_CENSORSHIP = "presets/behaviours/disable_censorship.txt"
    # Add more behaviours as needed

class ResponseLength(Enum):
    MINIMAL = "presets/response_length/1_minimal.txt"
    LOW = "presets/response_length/2_low.txt"
    MEDIUM = "presets/response_length/3_medium.txt"
    HIGH = "presets/response_length/4_high.txt"
    STORY_TELLER = "presets/response_length/5_story_teller.txt"

class AdviceType(Enum):
    SOFT = "presets/advice_type/1_soft.txt"
    BALLANCED = "presets/advice_type/2_ballanced.txt"
    HARSH = "presets/advice_type/3_harsh.txt"

class Thinking:
    class Divergent(Enum):
        MINIMAL = "presets/thinking/divergent/1_minimal.txt"
        LOW = "presets/thinking/divergent/2_low.txt"
        MEDIUM = "presets/thinking/divergent/3_medium.txt"
        HIGH = "presets/thinking/divergent/4_high.txt"
        CREATIVE = "presets/thinking/divergent/5_creative.txt"

    class Convergent(Enum):
        MINIMAL = "presets/thinking/convergent/1_minimal.txt"
        LOW = "presets/thinking/convergent/2_low.txt"
        MEDIUM = "presets/thinking/convergent/3_medium.txt"
        HIGH = "presets/thinking/convergent/4_high.txt"
        DEEP_ANALYSIS = "presets/thinking/convergent/5_deep_analysis.txt"

class UserInteraction(Enum):
    MINIMAL = "presets/user_interaction/1_minimal.txt"
    LOW = "presets/user_interaction/2_low.txt"
    MEDIUM = "presets/user_interaction/3_medium.txt"
    HIGH = "presets/user_interaction/4_high.txt"
    BABYSITTER = "presets/user_interaction/5_babysitter.txt"
