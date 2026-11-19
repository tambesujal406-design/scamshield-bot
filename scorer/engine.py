from dataclasses import dataclass, field

from .rules_text import check_text
from .rules_url import check_urls

MAX_CHARS = 5000  # ignore anything past this so huge pastes can't slow the bot down


@dataclass
class Result:
    score: int
    level: str  # "low" | "medium" | "high"
    reasons: list[tuple[str, int]] = field(default_factory=list)  # biggest first


def level_for(score: int) -> str:
    if score >= 61:
        return "high"
    if score >= 31:
        return "medium"
    return "low"


def analyze(message: str) -> Result:
    text = (message or "")[:MAX_CHARS]
    findings = check_text(text) + check_urls(text)
    findings.sort(key=lambda f: f[1], reverse=True)
    score = min(100, sum(points for _, points in findings))
    return Result(score=score, level=level_for(score), reasons=findings)
