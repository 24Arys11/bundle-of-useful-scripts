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
        SOFTWARE_SYSTEM_ARCHITECT = "presets/roles/tech_science/software_system_architect.txt"
        # Add more roles as needed

    @staticmethod
    def get_all_roles():
        return {
            "BusinessFinance": list(Roles.BusinessFinance),
            "StrategyAndBusiness": list(Roles.StrategyAndBusiness),
            "CreativeContent": list(Roles.CreativeContent),
            "GeneralGuidance": list(Roles.GeneralGuidance),
            "HealthWellbeing": list(Roles.HealthWellbeing),
            "SpecializedUnique": list(Roles.SpecializedUnique),
            "TechScience": list(Roles.TechScience)
        }

class Behaviours(Enum):
    DISABLE_CENSORSHIP = "presets/behaviours/disable_censorship.txt"
    STRONG_REFLECTION = "presets/behaviours/strong_reflection.txt"
    REMOVE_HALLUCINATIONS = "presets/behaviours/remove_hallucinations.txt"
    CHAOS_ORB_DYNAMIC = "presets/behaviours/chaos_orb_dynamic.txt"
    # Add more behaviours as needed

    @staticmethod
    def get_all_behaviours():
        return list(Behaviours)

class ResponseLength(Enum):
    MINIMAL = "presets/response_length/1_minimal.txt"
    LOW = "presets/response_length/2_low.txt"
    MEDIUM = "presets/response_length/3_medium.txt"
    HIGH = "presets/response_length/4_high.txt"
    STORY_TELLER = "presets/response_length/5_story_teller.txt"

    @staticmethod
    def get_all_response_lengths():
        return list(ResponseLength)

class AdviceType(Enum):
    SOFT = "presets/advice_type/1_soft.txt"
    BALLANCED = "presets/advice_type/2_ballanced.txt"
    HARSH = "presets/advice_type/3_harsh.txt"

    @staticmethod
    def get_all_advice_types():
        return list(AdviceType)

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

    @staticmethod
    def get_all_thinking_types():
        return {
            "Divergent": list(Thinking.Divergent),
            "Convergent": list(Thinking.Convergent)
        }

class UserAlignment(Enum):
    MINIMAL = "presets/user_alignment/1_minimal.txt"
    LOW = "presets/user_alignment/2_low.txt"
    MEDIUM = "presets/user_alignment/3_medium.txt"
    HIGH = "presets/user_alignment/4_high.txt"
    MAXIMUM = "presets/user_alignment/5_maximum.txt"

    @staticmethod
    def get_all_user_alignments():
        return list(UserAlignment)

class Technologies:
    class Languages(Enum):
        PYTHON = "presets/technologies/languages/python.txt"
        C = "presets/technologies/languages/c.txt"
        CPP = "presets/technologies/languages/cpp.txt"
        CSHARP = "presets/technologies/languages/csharp.txt"
        JAVA = "presets/technologies/languages/java.txt"
        GO = "presets/technologies/languages/go.txt"
        RUST = "presets/technologies/languages/rust.txt"
        SWIFT = "presets/technologies/languages/swift.txt"
        KOTLIN = "presets/technologies/languages/kotlin.txt"
        TYPESCRIPT = "presets/technologies/languages/typescript.txt"
        PHP = "presets/technologies/languages/php.txt"
        JULIA = "presets/technologies/languages/julia.txt"
        R = "presets/technologies/languages/r.txt"
        MATLAB = "presets/technologies/languages/matlab.txt"
        LISP = "presets/technologies/languages/lisp.txt"

    class Frontend(Enum):
        REACT = "presets/technologies/frontend/react.txt"
        ANGULAR = "presets/technologies/frontend/angular.txt"
        VUE = "presets/technologies/frontend/vue.txt"
        NEXTJS = "presets/technologies/frontend/nextjs.txt"
        TAILWINDCSS = "presets/technologies/frontend/tailwindcss.txt"
        BOOTSTRAP = "presets/technologies/frontend/bootstrap.txt"

    class Backend(Enum):
        NODEJS = "presets/technologies/backend/nodejs.txt"
        DJANGO = "presets/technologies/backend/django.txt"
        SPRING_BOOT = "presets/technologies/backend/spring_boot.txt"

    class Databases(Enum):
        SQL = "presets/technologies/databases/sql.txt"
        MONGODB = "presets/technologies/databases/mongodb.txt"

    class Mobile(Enum):
        FLUTTER = "presets/technologies/mobile/flutter.txt"

    @staticmethod
    def get_all():
        return {
            "Languages": list(Technologies.Languages),
            "Frontend": list(Technologies.Frontend),
            "Backend": list(Technologies.Backend),
            "Databases": list(Technologies.Databases),
            "Mobile": list(Technologies.Mobile),
        }

class SpecialPrompts(Enum):
    REASONING_ENGINE = "presets/special_prompts/reasoning_engine.txt"
    FUTURE_VISION_GUIDE = "presets/special_prompts/future_vision_guide.txt"
    PROMPT_CREATOR = "presets/special_prompts/prompt_creator.txt"
    WRITING_ASSISTANT = "presets/special_prompts/writing_assistant.txt"
    ATOMIC_SENTENCE_DECOMPOSER = "presets/special_prompts/atomic_sentence_decomposer.txt"
    INTROSPECTION_INTERVIEWER = "presets/special_prompts/introspection_interviewer.txt"
    OPPORTUNITY_GAP_CARTOGRAPHER = "presets/special_prompts/opportunity_gap_cartographer.txt"
    # Add more special prompts as needed

    @staticmethod
    def get_all():
        return list(SpecialPrompts)
