from __future__ import annotations

import re

NETWORK_PATTERNS = [r"\brequests\.", r"\bhttpx\.", r"\burllib\.", r"\bsocket\.", r"\bfetch\s*\(", r"\bHttpClient\b"]
WRITE_PATTERNS = [r"\.write\s*\(", r"\.write_text\s*\(", r"\bopen\s*\([^)]*['\"]w", r"\bFile\.Write", r"\bDirectory\.Create", r"\bINSERT\b", r"\bUPDATE\b", r"\bDELETE\b"]
READ_PATTERNS = [r"\.read\s*\(", r"\.read_text\s*\(", r"\bopen\s*\(", r"\bFile\.Read", r"\bDirectory\.GetFiles", r"\bSELECT\b"]
LOG_PATTERNS = [r"\bprint\s*\(", r"\blogger\.", r"\bconsole\.log\s*\(", r"\bConsole\.Write"]


def detect_effects(source: str) -> set[str]:
    effects: set[str] = set()
    if any(re.search(pattern, source, re.IGNORECASE) for pattern in NETWORK_PATTERNS):
        effects.add("network")
    if any(re.search(pattern, source, re.IGNORECASE) for pattern in WRITE_PATTERNS):
        effects.add("write")
    if any(re.search(pattern, source, re.IGNORECASE) for pattern in READ_PATTERNS):
        effects.add("read")
    if any(re.search(pattern, source, re.IGNORECASE) for pattern in LOG_PATTERNS):
        effects.add("log")
    return effects
