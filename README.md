# ScamShield Bot

A Telegram bot that checks a suspicious message and replies with a 0-100 risk score and the reasons behind it.
Forward or paste an SMS, WhatsApp or email text and get an explanation, not just a verdict.

\## Screenshots

| High risk | Medium risk | Low risk |

|---|---|---|

| !\[High](screenshots/high-risk.png) | !\[Medium](screenshots/medium-risk.png) | !\[Low](screenshots/low-risk.png) |How it works

Every message goes through two rule sets. Each rule that fires adds points and a plain-language reason.
The total is capped at 100 and shown with the four biggest reasons.

|Score|Level|
|-|-|
|0-30|Low risk|
|31-60|Medium risk|
|61-100|High risk|

* **Text rules** (`scorer/rules\_text.py`): OTP/PIN requests, fees and deposits, KYC threats, urgency, lottery claims, fake jobs, fake delivery and bill notices, "digital arrest" threats, guaranteed-returns pitches.
* **Link rules** (`scorer/rules\_url.py`): shorteners, raw IP addresses, punycode, risky TLDs, bank/brand imitation (including subdomain tricks like `sbi.co.in.evil.xyz`), login/verify/claim wording.
* All words, weights and brand domains live in `scorer/patterns.py`, so tuning needs no code changes.

## Run it

```bash
python -m venv .venv
.venv\\Scripts\\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env          # then paste your BotFather token into .env
python bot.py
```

Run the tests with `python -m unittest -v tests.test\_scorer`.

## Privacy

Message text is never stored or logged. Only the score, risk level and feedback button presses are logged.

## Limitations

This is a rule-based heuristic. It can miss new scam styles and can flag harmless messages.
A low score is not a guarantee of safety. Never share an OTP with anyone.

## Ideas for later

* Optional Google Safe Browsing / VirusTotal lookup for links
* Hindi and Marathi keyword lists
* Screenshot input (OCR)
* A browser extension that reuses `scorer/`

