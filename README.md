<div align="center">

# 🛡️ SentinelPay India

**Real-Time UPI Fraud Detection — Paste a message, get an instant risk report.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![Made for India](https://img.shields.io/badge/Made%20for-🇮🇳%20India-FF9933?style=flat-square)](https://cybercrime.gov.in)

*Supports UPI · PhonePe · Google Pay · Paytm · Bank SMS · WhatsApp*

</div>

---

## What It Does

Paste any suspicious payment request or upload a screenshot — SentinelPay extracts the receiver's UPI ID, amount, and purpose, then cross-checks against a fraud database and returns a verdict in under 200ms.

```
Input (text or screenshot)
       ↓
  OCR / Parser  →  extracts UPI ID, ₹ amount, phone, bank
       ↓
  Fraud Analyzer →  DB blacklist + 40 keyword patterns + heuristics
       ↓
  Verdict: DANGEROUS / SUSPICIOUS / CAUTION / LIKELY SAFE
```

---

## Quick Start

```bash
# Clone & start everything
git clone https://github.com/yourname/sentinelpay-india
cd sentinelpay-india
chmod +x start.sh && ./start.sh
```

Or manually:

```bash
# Terminal 1 — Backend
cd backend && pip install -r requirements.txt && python app.py

# Terminal 2 — Frontend
cd frontend && npm install && npm run dev
```

Open **http://localhost:3000**

> **Optional:** Set `ANTHROPIC_API_KEY` for Claude Vision OCR (more accurate screenshot reading). Falls back to Tesseract locally without it.

---

## Features

| | |
|---|---|
| 📝 **Text & Screenshot** | Paste messages or upload PhonePe/GPay/Paytm screenshots |
| 🔍 **UPI Blacklist** | 38+ flagged UPI IDs from known fraud patterns |
| 📞 **Phone Lookup** | Flags reported vishing and SIM-swap numbers |
| 🔑 **Keyword Detection** | 40+ scam keywords with plain-English explanations |
| 🕵️ **Heuristics** | ₹1 trick, urgency language, suspicious UPI handles |
| 📊 **Risk Score** | Weighted multi-signal score with color-coded verdict |
| 📋 **Audit Log** | Every analysis stored locally in SQLite |

---

## API

```bash
# Analyze a message
curl -X POST http://localhost:5000/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Pay ₹1 to kyc.update@ybl or your SBI account will be blocked"}'

# Analyze a screenshot
curl -X POST http://localhost:5000/analyze/image -F "image=@screenshot.png"
```

```json
{
  "verdict": "DANGEROUS",
  "risk_score": 1.0,
  "recommendation": "DO NOT PAY. Banks never ask for KYC fees via UPI.",
  "extracted": { "receiver_upi": "kyc.update@ybl", "amount": 1.0 },
  "risk_flags": [
    { "severity": "CRITICAL", "title": "UPI ID in Fraud Database", "detail": "234 reports since 2024-01-10" },
    { "severity": "CRITICAL", "title": "₹1 Verification Trick",    "detail": "No legitimate service requires this." }
  ],
  "db_match": { "found": true, "fraud_type": "KYC Fraud" }
}
```

Other endpoints: `GET /health` · `GET /stats` · `POST /db/lookup`

---

## Project Structure

```
sentinelpay-india/
├── start.sh                  # One-command launcher
├── backend/
│   ├── app.py                # Flask API
│   ├── analyzer.py           # Risk scoring engine
│   ├── parser.py             # Indian UPI/SMS regex parser
│   ├── fraud_db.py           # SQLite: seed data, lookups, audit log
│   ├── ocr.py                # Claude Vision + Tesseract fallback
│   └── model/fraud_india.db  # Fraud intelligence database
└── frontend/
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── AnalyzeInput.jsx   # Text/image input + sample messages
        │   └── FraudReport.jsx    # Verdict card, flags, DB match
        └── utils/api.js
```

---

## Fraud Database

Seeded from RBI advisories and CERT-In fraud alerts.

| Type | Entries | Examples |
|---|---|---|
| Flagged UPI IDs | 38 | KYC, lottery, investment, fake support |
| Flagged Phones | 18 | Vishing, SIM-swap numbers |
| Scam Keywords | 40 | `kyc`, `lucky draw`, `guaranteed return`, `send ₹1` |

**Verdict thresholds:** ≥65% → 🚨 DANGEROUS · ≥35% → ⚠️ SUSPICIOUS · ≥15% → 🔍 CAUTION · <15% → ✅ SAFE

---

## Privacy

All data stays on your machine. No cloud sync, no PII logging, no third-party calls (unless Claude Vision OCR is enabled for screenshots).

---

## 🆘 Helpline: 1930 &nbsp;|&nbsp; [cybercrime.gov.in](https://cybercrime.gov.in)

<div align="center">

*Built for 🇮🇳 India · MIT License · Not affiliated with NPCI, RBI, or any payment provider*

</div>
