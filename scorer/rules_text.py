import re

from .patterns import TEXT_RULES

_COMPILED = [
    (rule["label"], rule["weight"], [re.compile(p, re.IGNORECASE) for p in rule["patterns"]])
    for rule in TEXT_RULES
]


def check_text(text: str) -> list[tuple[str, int]]:
    """Return (reason, points) for every text rule that fires."""
    findings = []
    for label, weight, regexes in _COMPILED:
        for rx in regexes:
            m = rx.search(text)
            if m:
                snippet = " ".join(m.group(0).split())[:40]
                findings.append((f'{label}: "{snippet}"', weight))
                break  # one hit per rule is enough
    return findings
