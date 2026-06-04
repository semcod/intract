"""LLM-assisted @intract.v1 contract proposals (optional litellm extra)."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from intract.proposals import ProposedContract


def _extract_intract_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if "@intract.v1" in stripped:
            if not stripped.startswith("@"):
                idx = stripped.find("@intract.v1")
                stripped = stripped[idx:]
            lines.append(stripped)
    return lines


def _lines_to_proposals(lines: list[str], *, source: str = "llm") -> list[ProposedContract]:
    proposals: list[ProposedContract] = []
    for index, line in enumerate(lines):
        match = re.search(r"\bid:([^\s]+)", line)
        contract_id = match.group(1) if match else f"llm.proposed.{index}"
        kind = "llm"
        if "remove:" in line or "ui:remove" in line:
            kind = "delete"
        elif "keep:" in line or "ui:keep" in line:
            kind = "keep"
        proposals.append(
            ProposedContract(
                id=contract_id,
                kind=kind,
                element=contract_id.split(".")[-1],
                line=line,
            )
        )
    return proposals


def _load_litellm_completion():
    try:
        from litellm import completion
    except ImportError as exc:
        message = "litellm is required for LLM proposals: pip install 'intract[llm]'"
        raise RuntimeError(message) from exc
    return completion


def _resolve_model(model: str | None) -> str:
    return (
        model
        or os.environ.get("LLM_MODEL")
        or os.environ.get("INTRACT_LLM_MODEL")
        or "openrouter/google/gemini-3.1-flash-lite-preview"
    )


def _resolve_api_key(api_key: str | None) -> str:
    resolved_key = api_key or os.environ.get("OPENROUTER_API_KEY") or os.environ.get("LLM_API_KEY")
    if not resolved_key:
        raise RuntimeError("Set OPENROUTER_API_KEY or LLM_API_KEY for LLM contract proposals")
    return resolved_key


def _build_prompt(source: str, *, goal: str, fragment_name: str) -> str:
    example = (
        '"@intract.v1 id:example.fn scope:function intent:validate:input priority:3 '
        'domain:security effect:read forbid:network '
        'validate:input_presence,no_forbidden_effect meaning:\\"validate input\\""'
    )
    return f"""You propose Intract intent contracts for this artifact.

Goal/context:
{goal or "none"}

Artifact ({fragment_name}):
```
{source[:12000]}
```

Return ONLY a JSON array of strings. Each string must be one complete @intract.v1 line, for example:
{example}

Rules:
- Use scope ui for HTML/UI elements, function for code functions.
- Include id, scope, intent, priority, domain, effect, forbid, validate, meaning.
- Propose 1-5 contracts that capture the artifact intent and constraints.
- No markdown fences, no commentary."""


def _message_content_to_text(content: Any) -> str:
    if isinstance(content, list):
        return "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    return str(content or "")


def _strip_markdown_fence(raw: str) -> str:
    if not raw.startswith("```"):
        return raw
    without_opening = re.sub(r"^```[a-z]*\n?", "", raw)
    return re.sub(r"\n?```$", "", without_opening).strip()


def _json_line_strings(raw: str) -> list[str] | None:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, list):
        return None
    return [str(item).strip() for item in parsed if str(item).strip()]


def propose_contracts_llm(
    source: str,
    *,
    goal: str = "",
    fragment_name: str = "artifact",
    model: str | None = None,
    api_key: str | None = None,
    temperature: float = 0.2,
) -> list[ProposedContract]:
    """
    Ask an LLM to emit @intract.v1 lines for a code/HTML artifact.

    Requires: pip install 'intract[llm]' (litellm) and OPENROUTER_API_KEY or LLM_API_KEY.
    """
    completion = _load_litellm_completion()
    resolved_model = _resolve_model(model)
    resolved_key = _resolve_api_key(api_key)
    prompt = _build_prompt(source, goal=goal, fragment_name=fragment_name)

    response = completion(
        model=resolved_model,
        messages=[
            {
                "role": "system",
                "content": "You emit only valid @intract.v1 contract lines as a JSON string array.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=2048,
        api_key=resolved_key,
        api_base=os.environ.get("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
    )

    content = response.choices[0].message.content
    raw = _strip_markdown_fence(_message_content_to_text(content).strip())
    if not raw:
        return []

    line_strings = _json_line_strings(raw)
    if line_strings is not None:
        return _lines_to_proposals(line_strings)

    return _lines_to_proposals(_extract_intract_lines(raw))
