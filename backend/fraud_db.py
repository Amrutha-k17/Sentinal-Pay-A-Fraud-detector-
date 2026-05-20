"""
Indian Fraud Database — SQLite
Seeds comprehensive fraud intelligence: UPI IDs, phones, accounts, keywords.
Data modeled after RBI/CERT-In/I4C reported fraud patterns.
"""

import sqlite3
import os
import json
import hashlib
from datetime import datetime, timedelta
import random
from typing import Optional, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), "model", "fraud_india.db")

# ── Seed Data ─────────────────────────────────────────────────────────────────

FRAUD_UPI_IDS = [
    # KYC Fraud
    ("kyc.update@ybl",      "KYC Fraud",        "CRITICAL", 234, "2024-01-10"),
    ("kycverify@paytm",     "KYC Fraud",        "CRITICAL", 189, "2024-01-15"),
    ("sbi.kyc@oksbi",       "KYC Fraud",        "CRITICAL", 312, "2023-12-20"),
    ("hdfc.kyc@okaxis",     "KYC Fraud",        "CRITICAL", 98,  "2024-02-01"),
    ("kyc.renewal@ybl",     "KYC Fraud",        "CRITICAL", 167, "2024-01-22"),
    ("icici.kyc@okicici",   "KYC Fraud",        "CRITICAL", 203, "2024-02-10"),
    ("axis.kyc@axisbank",   "KYC Fraud",        "HIGH",     76,  "2024-03-01"),
    ("kychelp@paytm",       "KYC Fraud",        "HIGH",     143, "2024-01-05"),
    # Lottery/Prize Fraud
    ("lotteryindia@ybl",    "Lottery Fraud",    "CRITICAL", 421, "2023-11-10"),
    ("prizewinner@paytm",   "Lottery Fraud",    "CRITICAL", 356, "2023-10-22"),
    ("reward.india@okhdfcbank","Lottery Fraud", "CRITICAL", 289, "2024-01-03"),
    ("lucky.draw@ybl",      "Lottery Fraud",    "HIGH",     178, "2024-02-14"),
    ("ipl.winner@paytm",    "Lottery Fraud",    "CRITICAL", 512, "2024-03-20"),
    ("amazon.lucky@apl",    "Lottery Fraud",    "CRITICAL", 445, "2024-02-28"),
    ("jio.prize@ybl",       "Lottery Fraud",    "HIGH",     231, "2024-01-18"),
    # Investment Fraud
    ("trading.profit@ybl",  "Investment Fraud", "CRITICAL", 678, "2023-12-01"),
    ("crypto.india@paytm",  "Investment Fraud", "CRITICAL", 543, "2024-01-08"),
    ("stocktips@okhdfcbank","Investment Fraud", "HIGH",     234, "2024-02-20"),
    ("forex.earn@ybl",      "Investment Fraud", "CRITICAL", 789, "2023-11-25"),
    ("demat.help@oksbi",    "Investment Fraud", "HIGH",     156, "2024-03-05"),
    # Job/OLX Fraud
    ("jobwork.india@ybl",   "Job Fraud",        "HIGH",     321, "2024-01-12"),
    ("workfromhome@paytm",  "Job Fraud",        "HIGH",     267, "2024-02-08"),
    ("parttime.job@ybl",    "Job Fraud",        "MEDIUM",   143, "2024-03-10"),
    ("olx.seller@paytm",    "OLX Fraud",        "HIGH",     198, "2024-01-30"),
    ("army.sale@oksbi",     "OLX/Military Fraud","CRITICAL",445, "2023-12-15"),
    # Fake Customer Support
    ("sbi.helpdesk@oksbi",  "Fake Support",     "CRITICAL", 567, "2024-01-20"),
    ("paytm.care@paytm",    "Fake Support",     "CRITICAL", 489, "2024-02-05"),
    ("amazon.support@ybl",  "Fake Support",     "HIGH",     312, "2024-01-28"),
    ("flipkart.help@ybl",   "Fake Support",     "HIGH",     234, "2024-02-18"),
    ("google.pay.help@oksbi","Fake Support",    "CRITICAL", 178, "2024-03-08"),
    # Loan Fraud
    ("easyloan@paytm",      "Loan Fraud",       "HIGH",     234, "2024-02-12"),
    ("loan.approve@ybl",    "Loan Fraud",       "HIGH",     189, "2024-01-25"),
    ("instant.loan@oksbi",  "Loan Fraud",       "MEDIUM",   112, "2024-03-15"),
    # Fake Charity
    ("pmcare@paytm",        "Fake Charity",     "CRITICAL", 678, "2023-11-01"),
    ("flood.relief@ybl",    "Fake Charity",     "HIGH",     234, "2024-02-01"),
    ("helpindia@oksbi",     "Fake Charity",     "MEDIUM",   156, "2024-01-10"),
    # Sextortion/Blackmail
    ("verify.account@ybl",  "Extortion",        "CRITICAL", 89,  "2024-02-25"),
    ("unlock.id@paytm",     "Extortion",        "HIGH",     67,  "2024-03-12"),
]

FRAUD_PHONES = [
    ("9999999999", "Multiple Scam Reports",  "CRITICAL", 456),
    ("8888888888", "Lottery Fraud",          "CRITICAL", 312),
    ("7777777777", "KYC Fraud",              "HIGH",     234),
    ("9876543210", "Investment Fraud",       "HIGH",     178),
    ("9123456789", "Job Fraud",              "HIGH",     145),
    ("8123456789", "OLX Fraud",              "MEDIUM",   98),
    ("7123456789", "Fake Support",           "HIGH",     213),
    ("9988776655", "Loan Fraud",             "MEDIUM",   87),
    ("8877665544", "Fake Charity",           "HIGH",     134),
    ("7766554433", "Phishing",               "HIGH",     189),
    ("9911223344", "SIM Swap Fraud",         "CRITICAL", 67),
    ("8899001122", "Account Takeover",       "CRITICAL", 45),
    ("7788990011", "Vishing",                "MEDIUM",   112),
    ("9876512345", "UPI Fraud",              "HIGH",     234),
    ("8765123456", "ATM Fraud",              "HIGH",     89),
    ("9000000001", "Lottery Fraud",          "CRITICAL", 567),
    ("8000000001", "Investment Fraud",       "CRITICAL", 445),
    ("7000000001", "Job Fraud",              "HIGH",     321),
]

FRAUD_ACCOUNTS = [
    ("00000000001234", "SBIN", "Money Mule",      "CRITICAL", 12),
    ("00000000005678", "HDFC", "Fraud Proceeds",  "CRITICAL", 8),
    ("00000000009012", "ICICI","Lottery Fraud",   "HIGH",     15),
    ("00000000003456", "AXIS", "Investment Fraud","HIGH",     7),
    ("00000000007890", "PAYTM","KYC Fraud",       "CRITICAL", 23),
    ("11111111111111", "SBIN", "Money Mule",      "CRITICAL", 34),
    ("22222222222222", "HDFC", "Fraud Proceeds",  "CRITICAL", 19),
    ("33333333333333", "KOTAK","Job Fraud",       "HIGH",     11),
]

SCAM_KEYWORDS = [
    # KYC / Verification
    ("kyc", "HIGH", "KYC verification scams are the most common in India. Banks never request payment for KYC."),
    ("kyc update", "CRITICAL", "No bank sends payment requests for KYC updates."),
    ("kyc expiry", "CRITICAL", "Fake urgency tactic — KYC does not expire via UPI."),
    ("aadhar link", "HIGH", "Aadhaar linking is done free at bank branches, never via payment."),
    ("pan update", "HIGH", "PAN update never requires sending money."),
    ("account block", "HIGH", "Banks block accounts through official channels, not payment requests."),
    # Lottery / Prize
    ("lottery", "CRITICAL", "India's lottery laws prohibit cross-state lotteries. Most are scams."),
    ("lucky draw", "CRITICAL", "Prize notifications asking for upfront payment are always scams."),
    ("prize winner", "CRITICAL", "You cannot win a prize you did not enter."),
    ("ipl winner", "CRITICAL", "IPL does not award money to random viewers via UPI."),
    ("bumper prize", "CRITICAL", "Common lottery fraud terminology."),
    ("registration fee", "HIGH", "Legitimate prizes never charge registration fees."),
    ("processing fee", "HIGH", "Upfront fees for prize claims are a fraud tactic."),
    ("amazon winner", "CRITICAL", "Amazon does not send prizes via random UPI requests."),
    # Investment
    ("guaranteed return", "CRITICAL", "SEBI prohibits guaranteed return promises. Always a fraud."),
    ("double money", "CRITICAL", "No legitimate scheme doubles money."),
    ("crypto profit", "HIGH", "Unregulated crypto investment schemes are common scams."),
    ("trading tips", "HIGH", "Paid trading tips via UPI are frequently fraudulent."),
    ("stock tips", "HIGH", "SEBI-registered advisors don't collect fees via UPI."),
    # OLX / Military
    ("army", "MEDIUM", "Military personnel selling goods is a common OLX fraud pretext."),
    ("posted abroad", "HIGH", "Overseas posting combined with item sale is a fraud pattern."),
    ("advance payment", "HIGH", "Never pay advance before receiving goods from unknown sellers."),
    # Urgency / Fear
    ("urgent", "MEDIUM", "Urgency is a manipulation tactic in fraud messages."),
    ("immediately", "MEDIUM", "Pressure to act immediately is a red flag."),
    ("last chance", "HIGH", "Artificial scarcity tactic."),
    ("account suspended", "HIGH", "Fake threat to create panic and rushed payment."),
    ("legal action", "HIGH", "Threatening legal action via payment request is a scam."),
    ("arrested", "HIGH", "Police/CBI never demand money via UPI."),
    ("fine payment", "HIGH", "Government fines are paid through official portals, not UPI."),
    # Job Fraud
    ("work from home", "MEDIUM", "Many WFH job offers require upfront deposits — a fraud."),
    ("part time job", "MEDIUM", "Part-time job fraud often requests deposits or fees."),
    ("data entry job", "MEDIUM", "Data entry job scams are widespread in India."),
    ("task completion", "HIGH", "Task-based earning schemes are typically fraudulent."),
    # Small amount tricks
    ("send ₹1", "CRITICAL", "Sending ₹1 for 'verification' is a common UPI fraud pattern."),
    ("send re 1", "CRITICAL", "Never send money for identity verification."),
    ("verify account", "HIGH", "Account verification never requires sending money."),
    ("test payment", "HIGH", "Test payment requests are used to establish trust before larger fraud."),
    # Loan Fraud
    ("pre-approved loan", "HIGH", "Pre-approved loan offers via UPI are fraudulent."),
    ("instant loan", "HIGH", "Instant loan disbursement asking for security deposit is a scam."),
    ("loan approved", "HIGH", "Loan approval via payment request is always fraudulent."),
]

SAFE_UPI_SUFFIXES = [
    "@oksbi", "@okaxis", "@okicici", "@okhdfcbank",
    "@ybl", "@ibl", "@axl", "@axisbank",
    "@paytm", "@apl",  "@waicici",
    "@kotak", "@federal", "@rbl", "@sib",
    "@freecharge", "@airtel", "@jiomoney",
    "@upi", "@icici", "@hdfcbank"
]

LEGITIMATE_MERCHANTS = [
    "zomato", "swiggy", "amazon", "flipkart", "myntra", "nykaa",
    "bookmyshow", "irctc", "makemytrip", "goibibo", "oyo",
    "uber", "ola", "rapido", "dunzo", "blinkit", "bigbasket",
    "phonepe", "googlepay", "paytm", "airtel", "jio",
    "netflix", "hotstar", "zee5", "sonyliv",
    "hdfc", "sbi", "icici", "axis", "kotak",
]

# ── DB Init ───────────────────────────────────────────────────────────────────

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS flagged_upi (
        id INTEGER PRIMARY KEY,
        upi_id TEXT UNIQUE NOT NULL,
        fraud_type TEXT,
        severity TEXT,
        report_count INTEGER DEFAULT 1,
        first_reported TEXT,
        last_updated TEXT
    );
    CREATE TABLE IF NOT EXISTS flagged_phone (
        id INTEGER PRIMARY KEY,
        phone TEXT UNIQUE NOT NULL,
        fraud_type TEXT,
        severity TEXT,
        report_count INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS flagged_account (
        id INTEGER PRIMARY KEY,
        account_no TEXT UNIQUE NOT NULL,
        bank TEXT,
        fraud_type TEXT,
        severity TEXT,
        report_count INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS scam_keywords (
        id INTEGER PRIMARY KEY,
        keyword TEXT UNIQUE NOT NULL,
        severity TEXT,
        explanation TEXT
    );
    CREATE TABLE IF NOT EXISTS analysis_log (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        input_type TEXT,
        extracted_json TEXT,
        verdict TEXT,
        risk_score REAL
    );
    CREATE INDEX IF NOT EXISTS idx_upi ON flagged_upi(upi_id);
    CREATE INDEX IF NOT EXISTS idx_phone ON flagged_phone(phone);
    """)

    now = datetime.now().isoformat()

    for row in FRAUD_UPI_IDS:
        c.execute("""INSERT OR IGNORE INTO flagged_upi
            (upi_id, fraud_type, severity, report_count, first_reported, last_updated)
            VALUES (?,?,?,?,?,?)""", (*row, now))

    for row in FRAUD_PHONES:
        c.execute("""INSERT OR IGNORE INTO flagged_phone
            (phone, fraud_type, severity, report_count) VALUES (?,?,?,?)""", row)

    for row in FRAUD_ACCOUNTS:
        c.execute("""INSERT OR IGNORE INTO flagged_account
            (account_no, bank, fraud_type, severity, report_count) VALUES (?,?,?,?,?)""", row)

    for row in SCAM_KEYWORDS:
        c.execute("""INSERT OR IGNORE INTO scam_keywords
            (keyword, severity, explanation) VALUES (?,?,?)""", row)

    conn.commit()
    conn.close()
    print(f"[DB] Initialized: {DB_PATH}")


# ── Lookup Functions ──────────────────────────────────────────────────────────

def lookup_upi(upi_id: str) -> Optional[Dict]:
    if not upi_id:
        return None
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM flagged_upi WHERE LOWER(upi_id)=LOWER(?)", (upi_id.strip(),)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def lookup_phone(phone: str) -> Optional[Dict]:
    if not phone:
        return None
    clean = "".join(filter(str.isdigit, phone))[-10:]
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM flagged_phone WHERE phone=?", (clean,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def lookup_account(account_no: str) -> Optional[Dict]:
    if not account_no:
        return None
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM flagged_account WHERE account_no=?", (account_no.strip(),)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def check_keywords(text: str) -> list[dict]:
    if not text:
        return []
    text_lower = text.lower()
    conn = get_conn()
    rows = conn.execute("SELECT keyword, severity, explanation FROM scam_keywords").fetchall()
    conn.close()
    hits = []
    for row in rows:
        if row["keyword"] in text_lower:
            hits.append(dict(row))
    return hits


def is_safe_merchant(name: str) -> bool:
    if not name:
        return False
    name_lower = name.lower()
    return any(m in name_lower for m in LEGITIMATE_MERCHANTS)


def log_analysis(input_type: str, extracted: dict, verdict: str, risk_score: float):
    conn = get_conn()
    conn.execute("""INSERT INTO analysis_log
        (timestamp, input_type, extracted_json, verdict, risk_score)
        VALUES (?,?,?,?,?)""",
        (datetime.now().isoformat(), input_type, json.dumps(extracted), verdict, risk_score)
    )
    conn.commit()
    conn.close()


def get_stats() -> dict:
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM analysis_log").fetchone()[0]
    flagged = conn.execute("SELECT COUNT(*) FROM analysis_log WHERE verdict IN ('DANGEROUS','SUSPICIOUS')").fetchone()[0]
    db_upi = conn.execute("SELECT COUNT(*) FROM flagged_upi").fetchone()[0]
    db_phone = conn.execute("SELECT COUNT(*) FROM flagged_phone").fetchone()[0]
    recent = conn.execute("""SELECT verdict, risk_score, timestamp, extracted_json
        FROM analysis_log ORDER BY id DESC LIMIT 10""").fetchall()
    conn.close()
    return {
        "total_analyses": total,
        "flagged": flagged,
        "db_upi_entries": db_upi,
        "db_phone_entries": db_phone,
        "recent": [dict(r) for r in recent],
    }


if __name__ == "__main__":
    init_db()
    print("UPI lookup test:", lookup_upi("kyc.update@ybl"))
    print("Keyword check:", check_keywords("send ₹1 for kyc verification"))
