from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContractBuilder:
    scope: str
    intent: str
    priority: int = 3
    domain: str = ""
    input: tuple[str, ...] = ()
    output: tuple[str, ...] = ()
    effect: tuple[str, ...] = ()
    forbid: tuple[str, ...] = ()
    require: tuple[str, ...] = ()
    validate: tuple[str, ...] = ()
    meaning: str = ""

    def to_inline(self, prefix: str = "#") -> str:
        parts = [
            "@intract.v1",
            f"scope:{self.scope}",
            f"intent:{self.intent}",
            f"priority:{self.priority}",
        ]
        if self.domain:
            parts.append(f"domain:{self.domain}")
        if self.input:
            parts.append("input:" + ",".join(self.input))
        if self.output:
            parts.append("output:" + ",".join(self.output))
        if self.effect:
            parts.append("effect:" + ",".join(self.effect))
        if self.forbid:
            parts.append("forbid:" + ",".join(self.forbid))
        if self.require:
            parts.append("require:" + ",".join(self.require))
        if self.validate:
            parts.append("validate:" + ",".join(self.validate))
        if self.meaning:
            parts.append(f'meaning:"{self.meaning}"')
        return f"{prefix} " + " ".join(parts)


def contract(**kwargs) -> ContractBuilder:
    return ContractBuilder(**kwargs)
