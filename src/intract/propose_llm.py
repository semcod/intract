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
    try:
        from litellm import completion
    except ImportError as exc:
        raise RuntimeError("litellm is required for LLM proposals: pip install 'intract[llm]'") from exc

    resolved_model = (
        model
        or os.environ.get("LLM_MODEL")
        or os.environ.get("INTRACT_LLM_MODEL")
        or "openrouter/google/gemini-3.1-flash-lite-preview"
    )
    resolved_key = api_key or os.environ.get("OPENROUTER_API_KEY") or os.environ.get("LLM_API_KEY")
    if not resolved_key:
        raise RuntimeError("Set OPENROUTER_API_KEY or LLM_API_KEY for LLM contract proposals")

    prompt = f"""You propose Intract intent contracts for this artifact.

Goal/context:
{goal or "none"}

Artifact ({fragment_name}):
```
{source[:12000]}
```

Return ONLY a JSON array of strings. Each string must be one complete @intract.v1 line, for example:
"@intract.v1 id:example.fn scope:function intent:validate:input priority:3 domain:security effect:read forbid:network validate:input_presence,no_forbidden_effect meaning:\\"validate input\\""

Rules:
- Use scope ui for HTML/UI elements, function for code functions.
- Include id, scope, intent, priority, domain, effect, forbid, validate, meaning.
- Propose 1-5 contracts that capture the artifact intent and constraints.
- No markdown fences, no commentary."""

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
    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part) for part in content
        )
    if not content:
        return []

    raw = str(content).strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw).strip()

    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            line_strings = [str(item).strip() for item in parsed if str(item).strip()]
            return _lines_to_proposals(line_strings)
    except json.JSONDecodeError:
        pass

    return _lines_to_proposals(_extract_intract_lines(raw))
