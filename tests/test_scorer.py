import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from formatting import format_reply  # noqa: E402
from scorer import analyze  # noqa: E402

SCAMS = [
    "Dear customer, your SBI account will be blocked today. Update KYC now at sbi-kyc-update.xyz/login and share the OTP.",
    "Congratulations! You have won Rs 25 lakh in our lucky draw. Pay Rs 999 processing fee to claim your prize: bit.ly/claim-now",
    "Work from home! Earn Rs 5000 per day by liking videos. No experience needed. Message us on Telegram t.me/easyjobs. Small refundable deposit required.",
    "Your electricity bill is overdue and power will be disconnected tonight. Call immediately and pay at http://45.13.22.9/pay",
    "Your parcel is on hold at customs. Pay delivery fee Rs 49 at tinyurl.com/abc123 within 24 hours.",
    "This is CBI cyber crime branch. A case is registered against your Aadhaar. You are under digital arrest, do not tell anyone.",
]

MEDIUM = [
    "Congratulations, you won a lucky draw!",
    "Get a pre-approved loan today. Guaranteed returns if you invest with us.",
]

SAFE = [
    "Hey, are we still meeting at 5 near the library? Bring the notes.",
    "Your OTP is 482913 for login. Do not share it with anyone.",
    "Your Amazon order has shipped. Track it at https://www.amazon.in/gp/your-account/order-history",
    "Meeting moved to 3 PM, join here: https://meet.google.com/abc-defg-hij",
    "Please do not share your OTP or PIN with anyone, including bank staff.",
    "Can you work from home tomorrow? I'll send the notes over.",
    "",
]


class ScorerTests(unittest.TestCase):
    def test_scams_score_high(self):
        for msg in SCAMS:
            with self.subTest(msg=msg[:50]):
                r = analyze(msg)
                self.assertGreaterEqual(r.score, 61, r.reasons)
                self.assertEqual(r.level, "high")

    def test_medium_messages(self):
        for msg in MEDIUM:
            with self.subTest(msg=msg[:50]):
                r = analyze(msg)
                self.assertTrue(31 <= r.score <= 60, (r.score, r.reasons))

    def test_safe_messages_score_low(self):
        for msg in SAFE:
            with self.subTest(msg=msg[:50]):
                r = analyze(msg)
                self.assertLessEqual(r.score, 30, r.reasons)
                self.assertEqual(r.level, "low")

    def test_score_is_capped_at_100(self):
        self.assertLessEqual(analyze(SCAMS[0]).score, 100)

    def test_reasons_sorted_biggest_first(self):
        pts = [p for _, p in analyze(SCAMS[0]).reasons]
        self.assertEqual(pts, sorted(pts, reverse=True))

    def test_real_bank_domain_not_flagged_as_imitation(self):
        r = analyze("Log in at https://www.hdfcbank.com to see your statement")
        self.assertFalse(any("imitates" in reason for reason, _ in r.reasons))

    def test_subdomain_trick_is_flagged(self):
        r = analyze("Visit https://sbi.co.in.secure-login.xyz/verify now")
        self.assertTrue(any("imitates SBI" in reason for reason, _ in r.reasons))

    def test_reply_escapes_html_from_user_text(self):
        reply = format_reply(analyze("please share <b>your</b> OTP now"))
        self.assertNotIn("<b>your", reply)
        self.assertIn("&lt;", reply)

    def test_reply_shows_at_most_four_reasons(self):
        reply = format_reply(analyze(SCAMS[0]))
        self.assertLessEqual(reply.count("• "), 4)


if __name__ == "__main__":
    unittest.main()
