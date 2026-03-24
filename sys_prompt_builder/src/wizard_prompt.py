"""wizard_prompt.py — Prompt assembly and export helpers.

All role/technology resolution happens here from raw WizardState fields.
No role or technology accumulation occurs in the state itself.
"""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

from data import Roles, Thinking, UserInteraction, AdviceType, ResponseLength
from prompt_builder import PromptBuilder
from wizard_state import (
    WizardState,
    GUARDRAIL_INSTRUCTION,
    BEHAVIORAL_POLICY_INSTRUCTION,
    COACH_ROLE_MAP,
    CREATIVE_ROLE_MAP,
    BUSINESS_ROLE_MAP,
    RESPONSE_KEYS,
)


# ─────────────────────────────────────────────────────────────────────────────
# Role resolution
# ─────────────────────────────────────────────────────────────────────────────

def _resolve_roles(state: WizardState) -> list:
    """Compute roles from raw state fields.  Order: dev → teaching → coaching → creative → business → research."""
    roles: list = []

    def _add(role):
        if role not in roles:
            roles.append(role)

    # Software dev branch
    if "software_dev" in state.use_cases:
        if "engineer" in state.help_types or "reviewer" in state.help_types:
            _add(Roles.TechScience.SOFTWARE_ENGINEER)
        if "architect" in state.help_types and state.project_type != "script":
            _add(Roles.TechScience.SOFTWARE_SYSTEM_ARCHITECT)
        if "researcher" in state.help_types:
            _add(Roles.GeneralGuidance.RESEARCHER)
        if "teacher" in state.help_types:
            _add(Roles.GeneralGuidance.TEACHER)

    # Learning branch
    if "learning" in state.use_cases:
        _add(Roles.GeneralGuidance.TEACHER)
        if state.teaching_style == "socratic":
            _add(Roles.GeneralGuidance.SOCRATIC_GUIDE)

    # Coaching branch
    if "coaching" in state.use_cases:
        for coach_type in state.coach_types:
            role = COACH_ROLE_MAP.get(coach_type)
            if role:
                _add(role)

    # Creative branch
    if "creative" in state.use_cases:
        role = CREATIVE_ROLE_MAP.get(state.creative_type)
        if role:
            _add(role)

    # Business branch
    if "business" in state.use_cases:
        role = BUSINESS_ROLE_MAP.get(state.business_domain)
        if role:
            _add(role)

    # Research branch (silent)
    if "research" in state.use_cases:
        _add(Roles.GeneralGuidance.RESEARCHER)

    return roles


def _resolve_techs(state: WizardState) -> list:
    """Merge A2 and B1 tech selections, deduplicated, preserving order."""
    seen: set = set()
    techs: list = []
    for tech in list(state.a2_techs) + list(state.b1_techs):
        if tech not in seen:
            seen.add(tech)
            techs.append(tech)
    return techs


# ─────────────────────────────────────────────────────────────────────────────
# Prompt assembly
# ─────────────────────────────────────────────────────────────────────────────

def build_prompt_from_state(state: WizardState) -> str:
    """Assemble the full prompt from a WizardState using PromptBuilder."""
    builder = PromptBuilder()

    for role in _resolve_roles(state):
        builder.add_role(role)

    for tech in _resolve_techs(state):
        builder.add_technology(tech)

    builder.set_convergent_thinking(state.convergent())
    builder.set_divergent_thinking(state.divergent())
    builder.set_user_interaction(state.user_interaction_enum())
    builder.set_response_length(state.response_length_enum())

    if state.coaching_selected:
        builder.set_advice_type(state.advice_type_enum())

    # Project type → instruction
    if state.project_type == "script":
        builder.add_further_instructions(
            "Keep solutions pragmatic and minimal. Do not add test boilerplate unless asked."
        )
    elif state.project_type == "hobby":
        builder.add_further_instructions(
            "Encourage good structure and tests, but without strict coverage requirements."
        )
    elif state.project_type == "production":
        builder.add_further_instructions(
            "Apply full engineering rigour: tests required, careful incremental changes, "
            "seek alignment before deviating from the agreed design."
        )

    if state.project_info.strip():
        builder.set_project_context(state.project_info.strip())

    for key in state.guardrail_keys:
        instr = GUARDRAIL_INSTRUCTION.get(key, "")
        if instr:
            builder.add_further_instructions(instr)

    if state.custom_guardrail.strip():
        builder.add_further_instructions(state.custom_guardrail.strip())

    for scenario, protocol in state.protocols:
        builder.add_further_instructions(
            f"In the scenario [{scenario}], follow this protocol: [{protocol}]"
        )

    for instr in state.extra_instructions:
        builder.add_further_instructions(instr)

    if state.language_restriction.strip():
        builder.add_further_instructions(state.language_restriction.strip())

    # Behavioral policies
    for key in state.behavioral_policies:
        policy_text = BEHAVIORAL_POLICY_INSTRUCTION.get(key, "")
        if policy_text:
            builder.add_further_instructions(policy_text)

    if state.custom_policy.strip():
        builder.add_further_instructions(state.custom_policy.strip())

    with contextlib.redirect_stdout(io.StringIO()):
        prompt = builder.build()

    return prompt


# ─────────────────────────────────────────────────────────────────────────────
# Export helpers
# ─────────────────────────────────────────────────────────────────────────────

def export_prompt(state: WizardState, formats: list[str], filename: str) -> list[str]:
    """
    Write the built prompt in the requested formats.
    Returns a list of destination strings (paths or "clipboard").
    """
    prompt = state.built_prompt
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    done: list[str] = []

    if "txt" in formats:
        path = output_dir / f"{filename}.txt"
        path.write_text(prompt, encoding="utf-8")
        done.append(str(path))

    if "md" in formats:
        path = output_dir / f"{filename}.md"
        meta = _build_md_meta(state)
        path.write_text(f"{meta}\n```\n{prompt}\n```\n", encoding="utf-8")
        done.append(str(path))

    if "json" in formats:
        path = output_dir / f"{filename}.json"
        data = _build_json_data(state, prompt)
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        done.append(str(path))

    if "clipboard" in formats:
        _copy_to_clipboard(prompt)
        done.append("clipboard")

    return done


def _build_md_meta(state: WizardState) -> str:
    roles = [r.name for r in _resolve_roles(state)]
    techs = [t.name for t in _resolve_techs(state)]
    lines = [
        "---",
        f"use_cases: {state.use_cases}",
        f"roles: {roles}",
        f"technologies: {techs}",
        f"project_type: {state.project_type}",
        f"convergent: {state.convergent().name}",
        f"divergent: {state.divergent().name}",
        "---",
    ]
    return "\n".join(lines)


def _build_json_data(state: WizardState, prompt: str) -> dict:
    return {
        "use_cases": state.use_cases,
        "roles": [r.name for r in _resolve_roles(state)],
        "technologies": [t.name for t in _resolve_techs(state)],
        "project_type": state.project_type,
        "project_info": state.project_info,
        "convergent_thinking": state.convergent().name,
        "divergent_thinking": state.divergent().name,
        "user_interaction": state.interaction,
        "advice_type": state.advice if state.coaching_selected else None,
        "language_restriction": state.language_restriction,
        "behavioral_policies": state.behavioral_policies,
        "custom_policy": state.custom_policy,
        "guardrail_keys": state.guardrail_keys,
        "protocols": [{"scenario": s, "protocol": p} for s, p in state.protocols],
        "extra_instructions": state.extra_instructions,
        "prompt": prompt,
    }


def _copy_to_clipboard(text: str) -> None:
    try:
        if sys.platform == "win32":
            subprocess.run(["clip"], input=text.encode("utf-16"), check=True)
        elif sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        else:
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
    except Exception:
        pass
