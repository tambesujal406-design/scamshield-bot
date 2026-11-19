"""All the data the scorer uses. Edit this file to tune or add rules.

Each text rule adds its weight ONCE per message (first matching pattern wins),
so repeating a word doesn't pile up points. Patterns are case-insensitive regexes.
"""

TEXT_RULES = [
    {
        "label": "Asks for an OTP, PIN or password",
        "weight": 40,
        "patterns": [
            # (?<!not )(?<!never ) stops "do not share your OTP" (a real bank warning) from matching
            r"(?<!not )(?<!never )(?<!n't )\b(?:share|send|give|tell|provide|enter|submit|forward|read out)\b[^.\n]{0,25}\b(?:otp|pin|cvv|password|passcode)\b",
        ],
    },
    {
        "label": "Asks for a fee or payment",
        "weight": 30,
        "patterns": [
            r"\b(?:registration|processing|security|refundable|delivery|customs|clearance|activation|joining)\s+(?:fee|fees|charge|charges|deposit|amount)\b",
            r"\bpay\b[^.\n]{0,30}\b(?:to (?:claim|receive|release|unlock|activate)|fee)\b",
            r"\bupi\b[^.\n]{0,20}\b(?:collect|request|approve)\b",
            r"\bsend (?:rs\.?|₹|inr)\s?\d+",
        ],
    },
    {
        "label": "KYC or account-block threat",
        "weight": 25,
        "patterns": [
            r"\bkyc\b",
            r"\b(?:update|verify|link|re-?verify)\s+(?:your\s+)?(?:pan|aadhaar|aadhar|bank account|account details)\b",
            r"\baccount\b[^.\n]{0,25}\b(?:blocked|suspended|frozen|deactivated|closed)\b",
        ],
    },
    {
        "label": "Pressure or urgency",
        "weight": 15,
        "patterns": [
            r"\b(?:urgent|urgently|immediately|right now|asap)\b",
            r"\b(?:blocked|suspended|disconnected|expire[sd]?)\b[^.\n]{0,15}\b(?:today|tonight|in \d+\s*(?:hours?|hrs?|minutes?|mins?))",
            r"\blast (?:chance|warning|reminder)\b",
            r"\bwithin \d+\s*(?:hours?|hrs?|minutes?|mins?)\b",
        ],
    },
    {
        "label": "Prize or lottery claim",
        "weight": 35,
        "patterns": [
            r"\byou(?:'ve| have)? won\b",
            r"\b(?:lucky draw|lottery|jackpot)\b",
            r"\bclaim your (?:prize|reward|gift|cashback)\b",
            r"\bcongratulations\b[^.\n]{0,30}\b(?:won|selected|winner)\b",
        ],
    },
    {
        "label": "Fake job or easy-money offer",
        "weight": 25,
        "patterns": [
            r"\bwork from home\b",
            r"\bearn\s+(?:rs\.?|₹|inr)?\s?\d[\d,]*\s*(?:/|per|a)?\s*(?:day|daily|week|weekly)\b",
            r"\bpart[- ]time (?:job|work)\b",
            r"\b(?:no experience|without experience)\b",
            r"\b(?:like|subscribe|rate)\b[^.\n]{0,25}\b(?:earn|paid|task|reward)\b",
            r"\bdaily (?:payout|payment|income)\b",
        ],
    },
    {
        "label": "Fake delivery or bill-disconnection notice",
        "weight": 20,
        "patterns": [
            r"\b(?:electricity|power|gas|water)\b[^.\n]{0,30}\b(?:bill|connection|supply)\b[^.\n]{0,40}\b(?:disconnect(?:ed|ion)?|cut|discontinued|suspended)\b",
            r"\bpower (?:will be )?(?:cut|disconnected)\b",
            r"\b(?:courier|parcel|package|shipment)\b[^.\n]{0,40}\b(?:on hold|held|stuck|returned|undelivered|failed|customs)\b",
        ],
    },
    {
        "label": "Threat from a fake authority",
        "weight": 50,
        "patterns": [
            r"\bdigital arrest\b",
            r"\barrest warrant\b",
            r"\b(?:cbi|ncb|narcotics|cyber ?crime)\b[^.\n]{0,40}\b(?:officer|case|notice|summons|complaint)\b",
        ],
    },
    {
        "label": "Tells you to keep it secret",
        "weight": 20,
        "patterns": [
            r"\b(?:do not|don't|dont) (?:tell|inform) (?:anyone|anybody|your family)\b",
            r"\bkeep (?:this|it) (?:a )?(?:secret|confidential)\b",
        ],
    },
    {
        "label": "Instant or pre-approved loan offer",
        "weight": 15,
        "patterns": [
            r"\b(?:instant|pre-?approved|quick) (?:personal )?loan\b",
            r"\bloan (?:approved|sanctioned)\b[^.\n]{0,30}\b(?:no (?:documents|cibil)|without)\b",
        ],
    },
    {
        "label": "Refund or reward you have to claim",
        "weight": 15,
        "patterns": [
            r"\brefund\b[^.\n]{0,40}\b(?:click|link|claim|process)\b",
        ],
    },
    {
        "label": "Guaranteed-returns investment pitch",
        "weight": 30,
        "patterns": [
            r"\b(?:guaranteed|assured)\s+(?:returns?|profit)\b",
            r"\b(?:double|triple)\s+your\s+(?:money|investment)\b",
            r"\b\d{2,3}\s?%\s*(?:daily|weekly|monthly)\s+(?:returns?|profit)\b",
            r"\b(?:crypto|bitcoin|usdt|forex|stock tips?)\b[^.\n]{0,30}\b(?:profit|returns?|signal|vip)\b",
        ],
    },
    {
        "label": "Pushes you to chat on WhatsApp or Telegram",
        "weight": 10,
        "patterns": [
            r"\b(?:whatsapp|telegram)\b[^.\n]{0,25}\b(?:us|me|number|group|channel|link|contact|message|msg|dm|join)\b",
            r"\b(?:t\.me|wa\.me|chat\.whatsapp\.com)/\S+",
            r"\bcontact\b[^.\n]{0,15}\b(?:whatsapp|telegram)\b",
        ],
    },
]

# ---- link rules ----------------------------------------------------------

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy",
    "shorturl.at", "tiny.cc", "ow.ly", "bit.do", "s.id", "rebrand.ly", "t.ly",
}

# TLDs that show up a lot in throwaway scam sites (a hint, not proof)
RISKY_TLDS = {
    "xyz", "top", "click", "icu", "buzz", "cfd", "sbs", "cyou", "tk", "ml",
    "ga", "cf", "gq", "pw", "vip", "rest", "fun", "work", "support", "online", "site",
}

# Used to spot bare domains like "sbi-kyc-update.xyz/login" that have no http://
KNOWN_TLDS = RISKY_TLDS | {
    "com", "in", "net", "org", "info", "co", "me", "ly", "app", "io", "gov",
    "edu", "ac", "biz", "store", "shop", "live", "club", "link", "page", "bank", "sbi",
}

# Brand keyword -> display name + the domains that really belong to it.
# CHECK THESE YOURSELF and extend the list; a wrong entry causes false alarms.
BRANDS = {
    "sbi": ("SBI", {"sbi.co.in", "onlinesbi.sbi", "onlinesbi.com", "sbicard.com", "sbilife.co.in", "sbi.bank.in"}),
    "hdfc": ("HDFC Bank", {"hdfcbank.com", "hdfc.com", "hdfcsec.com"}),
    "icici": ("ICICI Bank", {"icicibank.com", "icicibank.co.in", "icicidirect.com"}),
    "axis": ("Axis Bank", {"axisbank.com", "axisbank.co.in"}),
    "pnb": ("PNB", {"pnbindia.in", "netpnb.com"}),
    "paytm": ("Paytm", {"paytm.com", "paytmbank.com"}),
    "phonepe": ("PhonePe", {"phonepe.com"}),
    "amazon": ("Amazon", {"amazon.in", "amazon.com", "amazon.co.in"}),
    "flipkart": ("Flipkart", {"flipkart.com"}),
    "uidai": ("UIDAI (Aadhaar)", {"uidai.gov.in"}),
    "incometax": ("Income Tax Dept", {"incometax.gov.in", "incometaxindia.gov.in"}),
    "indiapost": ("India Post", {"indiapost.gov.in"}),
    "jio": ("Jio", {"jio.com"}),
    "airtel": ("Airtel", {"airtel.in", "airtel.com"}),
    "netflix": ("Netflix", {"netflix.com"}),
}

SUSPICIOUS_URL_WORDS = ("login", "verify", "kyc", "update", "secure", "claim", "reward", "bonus", "refund")
SECOND_LEVEL = {"co", "com", "gov", "org", "net", "ac", "nic", "edu"}
