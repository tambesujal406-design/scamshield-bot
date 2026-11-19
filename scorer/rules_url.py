import re
from urllib.parse import urlparse

from .patterns import (BRANDS, KNOWN_TLDS, RISKY_TLDS, SECOND_LEVEL, SHORTENERS,
                       SUSPICIOUS_URL_WORDS)

_TLD_ALT = "|".join(sorted(KNOWN_TLDS, key=len, reverse=True))
URL_RE = re.compile(
    r"(?:https?://|www\.)[^\s<>\"']+"
    rf"|\b(?:[a-z0-9-]+\.)+(?:{_TLD_ALT})\b(?:/[^\s<>\"']*)?",
    re.IGNORECASE,
)
_IP_RE = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}")
_ALL_OFFICIAL = {d for _, domains in BRANDS.values() for d in domains}


def registered_domain(host: str) -> str:
    parts = host.split(".")
    if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in SECOND_LEVEL:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def _check_one(raw: str) -> list[tuple[str, int]]:
    raw = raw.rstrip(".,;:!?)]}'\"")
    parsed = urlparse(raw if "://" in raw else "//" + raw)
    host = (parsed.hostname or "").lower()
    if not host:
        return []

    out = []
    reg = registered_domain(host)
    tld = host.rsplit(".", 1)[-1]
    tokens = re.split(r"[.\-_]", host)

    if _IP_RE.fullmatch(host):
        out.append(("Link uses a raw IP address", 25))
    if "xn--" in host:
        out.append(("Link uses look-alike characters (punycode)", 25))
    if "@" in parsed.netloc:
        out.append(("Link hides its real address with an @", 15))
    if reg in SHORTENERS or host in SHORTENERS:
        out.append(("Shortened link hides the real destination", 15))
    if tld in RISKY_TLDS:
        out.append((f"Link ends in .{tld}, common on throwaway scam sites", 12))

    on_official = reg in _ALL_OFFICIAL
    for brand, (name, official) in BRANDS.items():
        if brand in tokens and reg not in official:
            out.append((f"Link imitates {name}", 30))
            break

    if not on_official:
        target = (host + parsed.path).lower()
        if any(w in target for w in SUSPICIOUS_URL_WORDS):
            out.append(("Link asks you to log in, verify or claim something", 8))
    if raw.lower().startswith("http://"):
        out.append(("Link isn't encrypted (http)", 5))
    if host.count("-") >= 3:
        out.append(("Domain is stuffed with hyphens", 8))
    if len(host.split(".")) >= 5:
        out.append(("Unusually long chain of subdomains", 8))
    return out


def check_urls(text: str) -> list[tuple[str, int]]:
    """Return (reason, points) for link problems. Each reason counts once per message."""
    seen: dict[str, int] = {}
    for match in URL_RE.finditer(text):
        for reason, points in _check_one(match.group(0)):
            seen.setdefault(reason, points)
    return list(seen.items())
