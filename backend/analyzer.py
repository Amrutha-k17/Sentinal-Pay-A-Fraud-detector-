"""
Fraud Analyzer — Main analysis engine
Combines parser output + DB lookups + heuristic scoring → structured report.
"""

import re
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

from parser import ParsedTransaction, parse_message
import fraud_db as db

# ── Risk Flag ──────────────────────────────────────────────────────────────────

SEVERITY_WEIGHT = {"CRITICAL": 0.40, "HIGH": 0.25, "MEDIUM": 0.12, "LOW": 0.05}
VERDICT_THRESHOLDS = {
    "DANGEROUS":   0.65,
    "SUSPICIOUS":  0.35,
    "CAUTION":     0.15,
    "LIKELY_SAFE": 0.0,
}

SCAM_ADVICE = {
    "KYC Fraud":        "Banks never ask you to send money for KYC. Visit the nearest branch instead.",
    "Lottery Fraud":    "You cannot win a lottery you didn't enter. All prize fees are scams.",
    "Investment Fraud": "SEBI prohibits guaranteed return promises. Report to cybercrime.gov.in.",
    "Job Fraud":        "Legitimate employers never ask for deposits. Verify the company first.",
    "OLX Fraud":        "Never pay advance for items from strangers online. Inspect before payment.",
    "OLX/Military Fraud":"Military personnel selling goods online is a well-known scam pattern.",
    "Fake Support":     "Contact the company directly via their official website, not via UPI.",
    "Loan Fraud":       "Legitimate lenders never ask for upfront fees. Check RBI's NBFC list.",
    "Fake Charity":     "Verify charities on ngodarpan.niti.gov.in before donating.",
    "Extortion":        "Do not pay. Block the contact and report to cybercrime.gov.in immediately.",
    "Money Mule":       "This account has been flagged for receiving fraud proceeds.",
    "Phishing":         "Do not share OTPs, PINs, or passwords with anyone.",
    "Vishing":          "Banks never ask for sensitive info over phone calls.",
}

GENERAL_TIPS = [
    "Report fraud at cybercrime.gov.in or call 1930 (National Cyber Crime Helpline).",
    "Never share OTP, UPI PIN, or bank passwords with anyone.",
    "Banks never contact you asking to send money for any reason.",
]

# ── Report Structure ───────────────────────────────────────────────────────────

@dataclass
class RiskFlag:
    code: str
    severity: str
    title: str
    detail: str

@dataclass
class FraudReport:
    report_id: str
    timestamp: str
    input_type: str           # "text" | "image"
    ocr_method: Optional[str] # "claude_vision" | "tesseract" | None
    parse_confidence: float
    extracted: dict
    risk_flags: list
    db_match: dict
    risk_score: float
    verdict: str
    verdict_color: str
    recommendation: str
    advice: list
    safe_to_pay: bool

    def to_dict(self):
        return asdict(self)


# ── Analysis ───────────────────────────────────────────────────────────────────

def _score_to_verdict(score: float) -> tuple[str, str]:
    if score >= VERDICT_THRESHOLDS["DANGEROUS"]:
        return "DANGEROUS", "#ff3860"
    if score >= VERDICT_THRESHOLDS["SUSPICIOUS"]:
        return "SUSPICIOUS", "#ffaa00"
    if score >= VERDICT_THRESHOLDS["CAUTION"]:
        return "CAUTION", "#00bcd4"
    return "LIKELY SAFE", "#00e676"


def analyze(txn: ParsedTransaction, input_type: str = "text",
            ocr_method: str = None) -> FraudReport:
    flags: list[RiskFlag] = []
    db_match = {"found": False, "entries": [], "fraud_type": None, "severity": None}

    # ── DB: UPI lookup ──────────────────────────────────────────────────────
    if txn.receiver_upi:
        hit = db.lookup_upi(txn.receiver_upi)
        if hit:
            db_match["found"] = True
            db_match["entries"].append(hit)
            db_match["fraud_type"] = hit["fraud_type"]
            db_match["severity"] = hit["severity"]
            flags.append(RiskFlag(
                code="BLACKLISTED_UPI",
                severity=hit["severity"],
                title="UPI ID in Fraud Database",
                detail=f"'{txn.receiver_upi}' reported {hit['report_count']} times for {hit['fraud_type']} since {hit.get('first_reported','unknown')}"
            ))

    # ── DB: Phone lookup ────────────────────────────────────────────────────
    if txn.receiver_phone:
        hit = db.lookup_phone(txn.receiver_phone)
        if hit:
            db_match["found"] = True
            db_match["entries"].append(hit)
            flags.append(RiskFlag(
                code="BLACKLISTED_PHONE",
                severity=hit["severity"],
                title="Phone Number in Fraud Database",
                detail=f"+91-{txn.receiver_phone} reported {hit['report_count']} times for {hit['fraud_type']}"
            ))

    # ── DB: Account lookup ──────────────────────────────────────────────────
    if txn.receiver_account:
        hit = db.lookup_account(txn.receiver_account)
        if hit:
            db_match["found"] = True
            db_match["entries"].append(hit)
            flags.append(RiskFlag(
                code="BLACKLISTED_ACCOUNT",
                severity=hit["severity"],
                title="Bank Account in Fraud Database",
                detail=f"Account {txn.receiver_account} ({hit.get('bank','unknown')}) flagged for {hit['fraud_type']}"
            ))

    # ── DB: Keyword scan ────────────────────────────────────────────────────
    keyword_hits = db.check_keywords(txn.raw_text)
    seen_keywords = set()
    for kw in keyword_hits:
        if kw["keyword"] not in seen_keywords:
            seen_keywords.add(kw["keyword"])
            flags.append(RiskFlag(
                code=f"SCAM_KEYWORD_{kw['keyword'].upper().replace(' ','_')}",
                severity=kw["severity"],
                title=f"Scam Keyword: '{kw['keyword']}'",
                detail=kw["explanation"]
            ))

    # ── Heuristic: Payment request check ───────────────────────────────────
    if txn.is_payment_request and txn.txn_type == "REQUEST":
        flags.append(RiskFlag(
            code="PAYMENT_REQUEST",
            severity="MEDIUM",
            title="Incoming Payment Request",
            detail="You are being asked to send money. Verify the receiver's identity before paying."
        ))

    # ── Heuristic: Very small amount (₹1 trick) ─────────────────────────────
    if txn.amount is not None and 0 < txn.amount <= 2:
        flags.append(RiskFlag(
            code="MICRO_AMOUNT_TRICK",
            severity="CRITICAL",
            title="₹1 Verification Trick",
            detail="Sending ₹1 for 'account verification' is a scam. No legitimate service requires this."
        ))

    # ── Heuristic: Large unusual amount ────────────────────────────────────
    if txn.amount is not None and txn.amount > 50000:
        flags.append(RiskFlag(
            code="HIGH_AMOUNT",
            severity="MEDIUM",
            title=f"Large Amount: ₹{txn.amount:,.0f}",
            detail="Verify the payee identity and purpose carefully before transferring large sums."
        ))

    # ── Heuristic: Suspicious UPI patterns ─────────────────────────────────
    if txn.receiver_upi:
        upi_lower = txn.receiver_upi.lower()
        suspicious_words = ["kyc","verify","bank","support","help","winner","prize",
                           "lottery","loan","reward","govt","gov","pm","cbi","police"]
        matched = [w for w in suspicious_words if w in upi_lower.split("@")[0]]
        if matched:
            flags.append(RiskFlag(
                code="SUSPICIOUS_UPI_PATTERN",
                severity="HIGH",
                title="Suspicious UPI Handle",
                detail=f"UPI ID contains suspicious word(s): {', '.join(matched)}. Legitimate services use simple identifiers."
            ))

    # ── Heuristic: Known safe merchant ─────────────────────────────────────
    is_safe_merchant = db.is_safe_merchant(txn.receiver_name or "") or \
                       db.is_safe_merchant(txn.merchant_name or "")
    if is_safe_merchant and not db_match["found"] and not keyword_hits:
        flags.append(RiskFlag(
            code="KNOWN_MERCHANT",
            severity="LOW",
            title="Recognized Merchant",
            detail="Receiver appears to be a known legitimate merchant. Still verify the exact UPI ID."
        ))

    # ── Heuristic: No UPI/phone at all ─────────────────────────────────────
    if not txn.receiver_upi and not txn.receiver_phone and not txn.receiver_account:
        flags.append(RiskFlag(
            code="NO_IDENTIFIER",
            severity="MEDIUM",
            title="No Receiver Identifier Found",
            detail="Could not extract UPI ID, phone, or account number. Manually verify receiver details."
        ))

    # ── Score computation ───────────────────────────────────────────────────
    raw_score = sum(SEVERITY_WEIGHT.get(f.severity, 0) for f in flags)
    # Reduce score if known safe merchant with no fraud signals
    if is_safe_merchant and not db_match["found"] and not keyword_hits:
        raw_score *= 0.3
    risk_score = min(raw_score, 1.0)

    verdict, verdict_color = _score_to_verdict(risk_score)

    # ── Recommendation ──────────────────────────────────────────────────────
    fraud_type = db_match.get("fraud_type")
    if verdict == "DANGEROUS":
        if fraud_type and fraud_type in SCAM_ADVICE:
            recommendation = f"DO NOT PAY. {SCAM_ADVICE[fraud_type]}"
        else:
            recommendation = "DO NOT PAY. Multiple high-severity fraud indicators detected. Report to cybercrime.gov.in or call 1930."
    elif verdict == "SUSPICIOUS":
        recommendation = "PROCEED WITH EXTREME CAUTION. Independently verify the receiver before any payment. Do not act under pressure."
    elif verdict == "CAUTION":
        recommendation = "Double-check the receiver's UPI ID and purpose. Ensure you initiated this transaction."
    else:
        recommendation = "Appears legitimate. Always verify receiver UPI ID character by character before paying."

    advice = GENERAL_TIPS.copy()
    if fraud_type and fraud_type in SCAM_ADVICE:
        advice.insert(0, SCAM_ADVICE[fraud_type])

    # ── Finalize ────────────────────────────────────────────────────────────
    import uuid
    report = FraudReport(
        report_id=str(uuid.uuid4())[:8].upper(),
        timestamp=datetime.now().isoformat(),
        input_type=input_type,
        ocr_method=ocr_method,
        parse_confidence=txn.confidence,
        extracted={
            "receiver_name":    txn.receiver_name,
            "receiver_upi":     txn.receiver_upi,
            "receiver_phone":   txn.receiver_phone,
            "receiver_account": txn.receiver_account,
            "receiver_ifsc":    txn.receiver_ifsc,
            "amount":           txn.amount,
            "bank_name":        txn.bank_name,
            "purpose":          txn.purpose,
            "source_app":       txn.source_app,
            "txn_type":         txn.txn_type,
            "is_payment_request": txn.is_payment_request,
            "ref_number":       txn.ref_number,
        },
        risk_flags=[{"code": f.code, "severity": f.severity,
                     "title": f.title, "detail": f.detail} for f in flags],
        db_match=db_match,
        risk_score=round(risk_score, 3),
        verdict=verdict,
        verdict_color=verdict_color,
        recommendation=recommendation,
        advice=advice[:3],
        safe_to_pay=(verdict == "LIKELY SAFE"),
    )

    db.log_analysis(input_type, report.extracted, verdict, risk_score)
    return report


def analyze_text(text: str) -> FraudReport:
    txn = parse_message(text)
    return analyze(txn, input_type="text")


def analyze_image_result(ocr_result: dict) -> FraudReport:
    """Analyze result from OCR service."""
    extracted = ocr_result.get("extracted")
    text = ocr_result.get("text", "")
    method = ocr_result.get("method", "unknown")

    if extracted:
        # Claude Vision gave structured output — map directly
        txn = parse_message(extracted.get("full_extracted_text", text) or text)
        # Override with Claude's structured data (more accurate)
        if extracted.get("receiver_upi"):     txn.receiver_upi = extracted["receiver_upi"]
        if extracted.get("receiver_phone"):   txn.receiver_phone = extracted["receiver_phone"]
        if extracted.get("receiver_name"):    txn.receiver_name = extracted["receiver_name"]
        if extracted.get("receiver_account"): txn.receiver_account = extracted["receiver_account"]
        if extracted.get("amount"):           txn.amount = float(extracted["amount"])
        if extracted.get("purpose"):          txn.purpose = extracted["purpose"]
        if extracted.get("bank_name"):        txn.bank_name = extracted["bank_name"]
        if extracted.get("source_app"):       txn.source_app = extracted["source_app"]
        if extracted.get("is_payment_request") is not None:
            txn.is_payment_request = bool(extracted["is_payment_request"])
        if extracted.get("txn_type"):         txn.txn_type = extracted["txn_type"]
        txn.confidence = min(txn.confidence + 0.2, 1.0)
    else:
        # Tesseract raw text — use parser
        txn = parse_message(text)

    return analyze(txn, input_type="image", ocr_method=method)
