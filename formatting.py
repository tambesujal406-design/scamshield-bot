"""Turns a scorer Result into the Telegram message text (HTML parse mode)."""
import html

from scorer import Result

EMOJI = {"low": "🟢", "medium": "🟡", "high": "🔴"}
LABEL = {"low": "Low risk", "medium": "Medium risk", "high": "High risk"}
ADVICE = {
    "high": "Don't click any link or share any OTP, PIN or password. "
            "Report it at cybercrime.gov.in or call 1930.",
    "medium": "Be careful. Don't click links or pay anything until you've confirmed "
              "with the real company through its official app or website.",
    "low": "Nothing alarming found, but that's not a guarantee. "
           "Never share an OTP with anyone.",
}
BAR_LEN = 10
MAX_REASONS = 4


def risk_bar(score: int) -> str:
    filled = round(score / 100 * BAR_LEN)
    return "▰" * filled + "▱" * (BAR_LEN - filled)


def format_reply(result: Result) -> str:
    lines = [
        f"{EMOJI[result.level]} <b>Risk: {result.score}/100 ({LABEL[result.level]})</b>",
        risk_bar(result.score),
        "",
    ]
    if result.reasons:
        lines.append("<b>Why</b>")
        for reason, points in result.reasons[:MAX_REASONS]:
            # reasons can contain text copied from the user's message, so escape it
            lines.append(f"• {html.escape(reason)} (+{points})")
    else:
        lines.append("No scam signals found in this message.")
    lines += ["", f"<b>What to do</b>\n{ADVICE[result.level]}", "",
              "<i>Automated check, not a guarantee.</i>"]
    return "\n".join(lines)
