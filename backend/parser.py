"""
Indian Transaction Message Parser
Extracts structured data from UPI requests, bank SMS, PhonePe/GPay/Paytm messages.
"""

import re
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Data Model ─────────────────────────────────────────────────────────────────

@dataclass
class ParsedTransaction:
    raw_text: str = ""
    source_app: Optional[str] = None       # PhonePe, GPay, Paytm, Bank, Unknown
    txn_type: Optional[str] = None         # REQUEST, RECEIVED, SENT, ALERT
    amount: Optional[float] = None
    currency: str = "INR"
    receiver_name: Optional[str] = None
    receiver_upi: Optional[str] = None
    receiver_phone: Optional[str] = None
    receiver_account: Optional[str] = None
    receiver_ifsc: Optional[str] = None
    sender_name: Optional[str] = None
    purpose: Optional[str] = None
    merchant_name: Optional[str] = None
    bank_name: Optional[str] = None
    ref_number: Optional[str] = None
    is_payment_request: bool = False
    confidence: float = 0.0
    parse_notes: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


# ── Regex Patterns ─────────────────────────────────────────────────────────────

# Amount: ₹500, Rs.500, Rs 500, INR 500, 500.00
AMT_PAT = re.compile(
    r'(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d{1,2})?)'
    r'|(?:amount[:\s]+(?:₹|rs\.?|inr)?\s*)([\d,]+(?:\.\d{1,2})?)',
    re.IGNORECASE
)

# UPI ID: anything@handle
UPI_PAT = re.compile(
    r'\b([\w.\-+]+@(?:oksbi|okaxis|okicici|okhdfcbank|ybl|ibl|axl|axisbank|'
    r'paytm|apl|waicici|kotak|federal|rbl|sib|freecharge|airtel|jiomoney|'
    r'upi|icici|hdfcbank|indus|barodampay|centralbank|unionbank|pnb|bob|'
    r'[a-z]{2,15}))\b',
    re.IGNORECASE
)

# Phone numbers (Indian 10-digit)
PHONE_PAT = re.compile(r'\b([6-9]\d{9})\b')

# Account numbers (9-18 digits, context-aware)
ACCT_PAT = re.compile(
    r'(?:a/?c|account|acc)[:\s#.]*([xX*]{0,8}\d{4,6})'
    r'|(?:account\s+no\.?\s*)(\d{9,18})',
    re.IGNORECASE
)

# IFSC
IFSC_PAT = re.compile(r'\b([A-Z]{4}0[A-Z0-9]{6})\b')

# Ref / UTR numbers
REF_PAT = re.compile(
    r'(?:ref\.?|utr|txn\s*id|transaction\s*id|order)[:\s#]*([A-Z0-9]{8,22})',
    re.IGNORECASE
)

# Purpose / Note / Narration
PURPOSE_PAT = re.compile(
    r'(?:for|note|purpose|remark|narration|description)[:\s]+"?([^.\n"]{3,80})"?',
    re.IGNORECASE
)

# Name patterns (after "from", "to", "pay to")
RECEIVER_NAME_PAT = re.compile(
    r'(?:pay(?:ment)?\s+to|to\s+pay|send\s+to|paying\s+to)[:\s]+([A-Z][a-zA-Z\s]{2,35})(?=\s|$|,|\.|₹|Rs)',
    re.IGNORECASE
)
SENDER_NAME_PAT = re.compile(
    r'(?:from|received\s+from|sent\s+by)[:\s]+([A-Z][a-zA-Z\s]{2,35})(?=\s|$|,|\.|₹|Rs)',
    re.IGNORECASE
)

# App-specific source detection
SOURCE_PATTERNS = {
    "PhonePe":   re.compile(r'phonepe|phone pe', re.I),
    "Google Pay": re.compile(r'google\s*pay|gpay|tez', re.I),
    "Paytm":     re.compile(r'paytm', re.I),
    "BHIM":      re.compile(r'\bbhim\b', re.I),
    "Amazon Pay": re.compile(r'amazon\s*pay', re.I),
    "WhatsApp":  re.compile(r'whatsapp', re.I),
    "SMS/Bank":  re.compile(r'\b(sbi|hdfc|icici|axis|kotak|pnb|bob|canara|union|federal|idfc|yes\s*bank)\b', re.I),
}

TXN_TYPE_PATTERNS = {
    "REQUEST":  re.compile(r'request(?:ing|ed)?\s+(?:payment|money|₹|rs)|pay(?:ment)?\s+request|collect\s+request', re.I),
    "RECEIVED": re.compile(r'received|credited|cr\b|deposited|added\s+to', re.I),
    "SENT":     re.compile(r'sent|debited|dr\b|paid\s+to|transferred\s+to', re.I),
    "ALERT":    re.compile(r'alert|otp|verify|verification|blocked|suspended|expir', re.I),
}

BANK_NAMES = {
    "sbi": "State Bank of India", "hdfc": "HDFC Bank", "icici": "ICICI Bank",
    "axis": "Axis Bank", "kotak": "Kotak Mahindra Bank", "pnb": "Punjab National Bank",
    "bob": "Bank of Baroda", "canara": "Canara Bank", "union": "Union Bank",
    "federal": "Federal Bank", "idfc": "IDFC First Bank", "yes": "Yes Bank",
    "paytm": "Paytm Payments Bank", "airtel": "Airtel Payments Bank",
    "indusind": "IndusInd Bank", "rbl": "RBL Bank",
}

UPI_BANK_MAP = {
    "@oksbi": "State Bank of India", "@okaxis": "Axis Bank",
    "@okicici": "ICICI Bank", "@okhdfcbank": "HDFC Bank",
    "@ybl": "Yes Bank / PhonePe", "@ibl": "ICICI Bank",
    "@paytm": "Paytm Payments Bank", "@apl": "Amazon Pay",
    "@kotak": "Kotak Mahindra Bank", "@axisbank": "Axis Bank",
    "@freecharge": "Axis Bank / Freecharge", "@airtel": "Airtel Payments Bank",
    "@jiomoney": "Jio Money", "@axl": "Axis Bank",
}

# ── Parser ─────────────────────────────────────────────────────────────────────

def parse_message(text: str) -> ParsedTransaction:
    txn = ParsedTransaction(raw_text=text)
    text_clean = text.strip()
    notes = []

    # Source app
    for app, pat in SOURCE_PATTERNS.items():
        if pat.search(text_clean):
            txn.source_app = app
            break
    if not txn.source_app:
        txn.source_app = "Unknown"

    # Transaction type
    for typ, pat in TXN_TYPE_PATTERNS.items():
        if pat.search(text_clean):
            txn.txn_type = typ
            break

    # Payment request flag
    if txn.txn_type == "REQUEST" or re.search(
        r'(?:request|requesting|collect|wants?\s+to\s+collect)', text_clean, re.I
    ):
        txn.is_payment_request = True

    # Amount
    amounts = AMT_PAT.findall(text_clean)
    if amounts:
        raw_amt = next((a[0] or a[1] for a in amounts if a[0] or a[1]), None)
        if raw_amt:
            try:
                txn.amount = float(raw_amt.replace(",", ""))
            except ValueError:
                notes.append("Could not parse amount")

    # UPI IDs
    upis = UPI_PAT.findall(text_clean)
    if upis:
        txn.receiver_upi = upis[0].lower()
        # Derive bank from UPI suffix
        for suffix, bank in UPI_BANK_MAP.items():
            if txn.receiver_upi.endswith(suffix):
                txn.bank_name = bank
                break
        if len(upis) > 1:
            notes.append(f"Multiple UPI IDs: {upis}")

    # Phone
    phones = PHONE_PAT.findall(text_clean)
    if phones:
        txn.receiver_phone = phones[0]
        if len(phones) > 1:
            notes.append(f"Multiple phones found: {phones}")

    # Account
    acct_matches = ACCT_PAT.findall(text_clean)
    if acct_matches:
        txn.receiver_account = next((a[0] or a[1] for a in acct_matches if a[0] or a[1]), None)

    # IFSC
    ifsc = IFSC_PAT.search(text_clean)
    if ifsc:
        txn.receiver_ifsc = ifsc.group(1)
        prefix = ifsc.group(1)[:4].lower()
        for key, name in BANK_NAMES.items():
            if key in prefix:
                txn.bank_name = txn.bank_name or name

    # Reference
    ref = REF_PAT.search(text_clean)
    if ref:
        txn.ref_number = ref.group(1)

    # Purpose
    purpose = PURPOSE_PAT.search(text_clean)
    if purpose:
        txn.purpose = purpose.group(1).strip()

    # Receiver name
    recv_name = RECEIVER_NAME_PAT.search(text_clean)
    if recv_name:
        txn.receiver_name = recv_name.group(1).strip().title()

    # Sender name
    send_name = SENDER_NAME_PAT.search(text_clean)
    if send_name:
        txn.sender_name = send_name.group(1).strip().title()

    # Bank name fallback from text
    if not txn.bank_name:
        for key, name in BANK_NAMES.items():
            if re.search(rf'\b{key}\b', text_clean, re.I):
                txn.bank_name = name
                break

    # UPI handle → name fallback
    if txn.receiver_upi and not txn.receiver_name:
        handle = txn.receiver_upi.split("@")[0]
        handle_clean = re.sub(r'[._\-0-9]', ' ', handle).strip()
        if len(handle_clean) > 2:
            txn.receiver_name = handle_clean.title()

    # Confidence scoring
    score = 0.0
    if txn.receiver_upi:  score += 0.35
    if txn.amount:        score += 0.25
    if txn.receiver_name: score += 0.15
    if txn.receiver_phone:score += 0.10
    if txn.txn_type:      score += 0.10
    if txn.purpose:       score += 0.05
    txn.confidence = min(score, 1.0)

    txn.parse_notes = notes
    return txn


def parse_batch(texts: list[str]) -> list[ParsedTransaction]:
    return [parse_message(t) for t in texts]


# ── Test ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    samples = [
        "Pay ₹1 to kyc.update@ybl for KYC verification immediately or your account will be blocked",
        "[PhonePe] Rahul Sharma (rahul@ybl) is requesting ₹5,000 from you. Note: Investment return",
        "Dear Customer, Rs.2000 IMPS transfer request from A/c XX4321 to 9876543210. Ref: 123456789",
        "Congratulations! You won ₹50,000 in Lucky Draw. Pay ₹500 processing fee to lottery.india@paytm",
        "Send ₹1 to verify your SBI account. Account suspended if not done in 2 hours. sbi.helpdesk@oksbi",
        "Zomato order payment of ₹349 to zomato@icici. Order #ZM123456",
    ]
    for s in samples:
        p = parse_message(s)
        print(f"\nInput: {s[:60]}...")
        print(f"  UPI: {p.receiver_upi} | Amount: {p.amount} | Confidence: {p.confidence:.2f}")
        print(f"  Type: {p.txn_type} | Request: {p.is_payment_request} | App: {p.source_app}")
