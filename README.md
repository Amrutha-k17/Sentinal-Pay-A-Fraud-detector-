<div align="center">

```
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     ██████╗  █████╗ ██╗   ██╗
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ██╔══██╗██╔══██╗╚██╗ ██╔╝
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ██████╔╝███████║ ╚████╔╝
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██╔═══╝ ██╔══██║  ╚██╔╝
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗██║     ██║  ██║   ██║
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝   ╚═╝
```

### 🛡️ **INDIA** — Real-Time UPI Fraud Detection System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Made for India](https://img.shields.io/badge/Made%20for-🇮🇳%20India-FF9933?style=flat-square)](https://cybercrime.gov.in)

> **Paste a UPI message or upload a screenshot — get an instant fraud risk report in seconds.**
> Built specifically for Indian payment ecosystems: UPI, BHIM, PhonePe, Google Pay, Paytm, and bank SMS.

---

</div>

## 🚨 The Problem

India processes **12+ billion UPI transactions** monthly. Cybercrime helpline **1930** receives thousands of fraud complaints every day — KYC scams, lottery fraud, fake investment schemes, OLX military scams. Most victims only realise they've been scammed after the money is gone.

**SentinelPay lets anyone — in seconds, for free — verify whether a payment request is safe before hitting Send.**

---

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 📝 **Text Analysis** | Paste any UPI request, bank SMS, WhatsApp message |
| 📸 **Screenshot OCR** | Upload PhonePe/GPay/Paytm screenshots — auto-extracts all details |
| 🔍 **UPI Blacklist** | Checks against 38+ known fraudulent UPI IDs |
| 📞 **Phone Lookup** | Flags known vishing/SIM-swap numbers |
| 🔑 **Keyword Scanner** | 40+ scam keyword patterns with contextual explanations |
| 📊 **Risk Scoring** | Multi-signal weighted score → DANGEROUS / SUSPICIOUS / CAUTION / SAFE |
| 🏦 **Bank Intelligence** | Understands all Indian UPI handles (`@oksbi`, `@ybl`, `@paytm`…) |
| 🕵️ **Pattern Detection** | ₹1 trick, fake urgency, suspicious UPI handle patterns |
| 📋 **Audit Log** | Every analysis logged locally for review |
| ⚡ **< 200ms** | Inference under 200ms — real-time at the payment screen |

---

## 🖥️ Dashboard Preview

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🛡️  SENTINELPAY INDIA                       UPI Fraud Analyzer  ● Online│
├────────────────────────┬────────────────────────────────────────────────┤
│  ANALYZE TRANSACTION   │  🚨 VERDICT: DANGEROUS              Risk: 100% │
│  ─────────────────     │  ──────────────────────────────────────────────│
│  ✏️ Paste Message       │  🚫 DO NOT PAY. Banks never ask for KYC fees.  │
│  📸 Screenshot         │                                                │
│                        │  EXTRACTED DETAILS                             │
│  ┌──────────────────┐  │  UPI ID    kyc.update@ybl                      │
│  │ Pay ₹1 to        │  │  Amount    ₹1.00                               │
│  │ kyc.update@ybl   │  │  Bank      Yes Bank / PhonePe                  │
│  │ for KYC or your  │  │                                                │
│  │ account will be  │  │  RISK FLAGS (4 found)                          │
│  │ blocked...       │  │  ████ CRITICAL  UPI ID in Fraud Database       │
│  └──────────────────┘  │  ████ CRITICAL  ₹1 Verification Trick          │
│                        │  ███░ HIGH      Scam Keyword: 'kyc'            │
│  QUICK TEST SAMPLES    │  ███░ HIGH      Suspicious UPI Handle          │
│  [FRAUD] KYC Scam      │                                                │
│  [FRAUD] Lottery Fraud │  ⚠ DATABASE MATCH                              │
│  [FRAUD] Fake Support  │  KYC Fraud · 234 reports · Since 2024-01-10   │
│  [SAFE]  Zomato Order  │                                                │
│  [FRAUD] Investment    │  📞 Helpline: 1930 · cybercrime.gov.in        │
│                        │                                                │
│  [🔍 ANALYZE MESSAGE]  │  RECENT ANALYSES                               │
│                        │  🚨 DANGEROUS  kyc.update@ybl      ₹1         │
└────────────────────────┴────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────┐
                    │         User Interface           │
                    │     Vite + React  :3000          │
                    │                                  │
                    │  ┌──────────┐  ┌──────────────┐ │
                    │  │  Text    │  │  Screenshot  │ │
                    │  │  Input   │  │   Upload     │ │
                    │  └────┬─────┘  └──────┬───────┘ │
                    └───────┼───────────────┼─────────┘
                            │  /api proxy   │
                    ┌───────▼───────────────▼─────────┐
                    │       Flask API  :5000           │
                    │  POST /analyze/text              │
                    │  POST /analyze/image             │
                    │  GET  /health  GET  /stats       │
                    └───────┬──────────────┬───────────┘
                            │              │
               ┌────────────▼──┐    ┌──────▼──────────┐
               │  Text Parser  │    │   OCR Service    │
               │  (regex.py)   │    │                  │
               │               │    │  1. Claude Vision│
               │  • UPI ID     │    │     (accurate)   │
               │  • Amount ₹   │    │  2. Tesseract    │
               │  • Phone No.  │    │     (fallback)   │
               │  • IFSC Code  │    └──────────────────┘
               │  • App Source │
               └───────┬───────┘
                       │
               ┌───────▼────────────────────────────────┐
               │           Analyzer Engine              │
               │                                        │
               │  ① SQLite DB lookups                   │
               │     flagged_upi · flagged_phone         │
               │     flagged_account · keywords          │
               │                                        │
               │  ② Heuristic rules                     │
               │     ₹1 trick · urgency · UPI patterns  │
               │     high amount · no identifier        │
               │                                        │
               │  ③ Risk Score → Verdict → Report       │
               └────────────────────────────────────────┘
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Tesseract OCR

```bash
# macOS
brew install tesseract

# Ubuntu / Debian
sudo apt install tesseract-ocr

# Windows — download installer from:
# https://github.com/UB-Mannheim/tesseract/wiki
```

### Option A — One Command ✨

```bash
git clone https://github.com/yourname/sentinelpay-india
cd sentinelpay-india
chmod +x start.sh && ./start.sh
```

Open **http://localhost:3000** — done.

### Option B — Manual (Two Terminals)

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python app.py
# ✓ Flask running on http://localhost:5000

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
# ✓ Vite running on http://localhost:3000
```

### Option C — With Claude Vision OCR (Best Screenshot Accuracy)

```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
cd backend && python app.py
```

Get a free key at [console.anthropic.com](https://console.anthropic.com)

> Without the key, Tesseract handles screenshots locally — no API call, no cost.

---

## 📡 API Reference

### `POST /analyze/text`

```bash
curl -X POST http://localhost:5000/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Pay ₹1 to kyc.update@ybl for KYC verification or your account will be blocked"}'
```

**Response**
```json
{
  "report_id": "A3F9C1B2",
  "verdict": "DANGEROUS",
  "risk_score": 1.0,
  "safe_to_pay": false,
  "recommendation": "DO NOT PAY. Banks never ask you to send money for KYC.",

  "extracted": {
    "receiver_upi": "kyc.update@ybl",
    "amount": 1.0,
    "bank_name": "Yes Bank / PhonePe",
    "is_payment_request": true
  },

  "risk_flags": [
    { "severity": "CRITICAL", "title": "UPI ID in Fraud Database",
      "detail": "Reported 234 times for KYC Fraud since 2024-01-10" },
    { "severity": "CRITICAL", "title": "₹1 Verification Trick",
      "detail": "No legitimate service requires sending money to verify an account." }
  ],

  "db_match": {
    "found": true,
    "fraud_type": "KYC Fraud",
    "severity": "CRITICAL"
  }
}
```

### `POST /analyze/image`

```bash
curl -X POST http://localhost:5000/analyze/image \
  -F "image=@/path/to/screenshot.png"
```

### All Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | API + service status |
| `GET` | `/stats` | DB counts + recent analyses |
| `POST` | `/analyze/text` | Analyze pasted message |
| `POST` | `/analyze/image` | Analyze screenshot (multipart) |
| `POST` | `/db/lookup` | Quick UPI/phone check `{"upi":"..."}` |

---

## 🗄️ Fraud Intelligence Database

Seeded with patterns modeled from RBI advisories, CERT-In alerts, and I4C reports.

### Flagged UPI IDs — 38 entries

| Fraud Type | Sample IDs | Reports |
|---|---|---|
| 🔴 KYC Fraud | `kyc.update@ybl`, `sbi.kyc@oksbi`, `kycverify@paytm` | 234, 189, 312 |
| 🔴 Lottery / Prize | `lotteryindia@ybl`, `ipl.winner@paytm`, `amazon.lucky@apl` | 421, 512, 445 |
| 🔴 Investment Fraud | `trading.profit@ybl`, `crypto.india@paytm`, `forex.earn@ybl` | 678, 543, 789 |
| 🟠 Fake Support | `sbi.helpdesk@oksbi`, `google.pay.help@oksbi` | 567, 178 |
| 🟠 Job Fraud | `jobwork.india@ybl`, `workfromhome@paytm` | 321, 267 |
| 🟠 OLX / Military | `army.sale@oksbi` | 445 |
| 🟠 Loan Fraud | `easyloan@paytm`, `loan.approve@ybl` | 234, 189 |
| 🟠 Fake Charity | `pmcare@paytm`, `flood.relief@ybl` | 678, 234 |

### Scam Keywords — 40 entries

| Category | Keywords |
|---|---|
| KYC / Verification | `kyc`, `kyc update`, `aadhar link`, `pan update`, `account block` |
| Lottery / Prize | `lottery`, `lucky draw`, `prize winner`, `bumper prize`, `registration fee` |
| Investment | `guaranteed return`, `double money`, `crypto profit`, `stock tips` |
| Urgency / Fear | `urgent`, `immediately`, `account suspended`, `legal action`, `arrested` |
| Tricks | `send ₹1`, `send re 1`, `verify account`, `test payment` |

---

## 📊 Risk Scoring Model

```
Risk Score = Σ (weight per flag)    [capped at 1.0]

  CRITICAL flag  →  +0.40
  HIGH flag      →  +0.25
  MEDIUM flag    →  +0.12
  LOW flag       →  +0.05

  Known safe merchant (Zomato, Amazon…)  →  score × 0.3
```

### Verdict Scale

| Score | Verdict | Meaning |
|---|---|---|
| ≥ 65% | 🚨 **DANGEROUS** | High confidence fraud — do NOT pay |
| ≥ 35% | ⚠️ **SUSPICIOUS** | Multiple red flags — verify first |
| ≥ 15% | 🔍 **CAUTION** | Minor concerns — double-check |
| < 15% | ✅ **LIKELY SAFE** | No fraud signals detected |

---

## 📁 Project Structure

```
sentinelpay-india/
│
├── 🚀 start.sh                     # One-command launcher (Flask + Vite)
│
├── backend/
│   ├── app.py                      # Flask API — routes, CORS, error handling
│   ├── analyzer.py                 # Core engine → FraudReport dataclass
│   ├── parser.py                   # Indian UPI/SMS/bank regex parser
│   ├── fraud_db.py                 # SQLite: seed, lookup, audit log
│   ├── ocr.py                      # Claude Vision + Tesseract fallback
│   ├── requirements.txt
│   └── model/
│       └── fraud_india.db          # SQLite fraud intelligence database
│
└── frontend/
    ├── index.html
    ├── vite.config.js              # Dev proxy :3000 → :5000, offline handler
    └── src/
        ├── App.jsx                 # Root: health poll, offline banner, history
        ├── components/
        │   ├── AnalyzeInput.jsx    # Text/image toggle + 6 sample messages
        │   └── FraudReport.jsx     # Report: verdict, flags, DB match, advice
        ├── utils/api.js            # Fetch wrapper with robust error mapping
        └── styles/index.css        # Dark terminal aesthetic (CSS variables)
```

---

## 🧠 Detection Pipeline

```
  User Input
      │
      ├── Text message ──────────────────────────┐
      │                                           │
      └── Screenshot ──► OCR Engine              │
                           ├─ Claude Vision API  │
                           └─ Tesseract (local)  │
                                    │             │
                                    └─────────────▼
                                           │
                                    ┌──────▼──────────────┐
                                    │    Regex Parser      │
                                    │  UPI · ₹ · Phone    │
                                    │  IFSC · Purpose      │
                                    └──────┬───────────────┘
                                           │
                          ┌────────────────▼──────────────────┐
                          │          Fraud Analyzer            │
                          │                                    │
                          │  ① UPI blacklist  (38 entries)    │
                          │  ② Phone lookup   (18 entries)    │
                          │  ③ Account check  ( 8 entries)    │
                          │  ④ Keyword scan   (40 patterns)   │
                          │  ⑤ ₹1 micro-amount trick          │
                          │  ⑥ UPI handle pattern check       │
                          │  ⑦ High-value amount flag         │
                          │  ⑧ Safe merchant recognition      │
                          │                                    │
                          └────────────────┬──────────────────┘
                                           │
                                    ┌──────▼──────────────┐
                                    │  Risk Score + Verdict│
                                    │  + Flags + Advice    │
                                    │  → Logged to SQLite  │
                                    └──────┬───────────────┘
                                           │
                                    ┌──────▼──────────────┐
                                    │   Report Card UI     │
                                    │ Verdict · DB Match   │
                                    │ Flags · Helpline     │
                                    └─────────────────────┘
```

---

## 🛡️ Fraud Types Covered

<table>
<tr>
<td width="50%" valign="top">

**🔴 CRITICAL THREATS**
- KYC verification fraud
- ₹1 account verification trick
- Blacklisted UPI IDs (verified)
- Lottery / prize claim scams
- Fake PM / government schemes

</td>
<td width="50%" valign="top">

**🟠 HIGH RISK**
- Investment / trading scams
- OLX military seller fraud
- Fake customer support impersonation
- Pre-approved loan fraud
- Account suspension threats

</td>
</tr>
<tr>
<td valign="top">

**🟡 MEDIUM CAUTION**
- Unverified incoming payment requests
- Work-from-home job scams
- Suspicious UPI handle patterns
- High-value transfers (>₹50,000)
- No identifier found in message

</td>
<td valign="top">

**🟢 LIKELY SAFE**
- Known merchants (Zomato, Swiggy, Amazon…)
- Standard bank credit / debit alerts
- Clean UPI IDs with no database match
- Normal everyday transaction amounts

</td>
</tr>
</table>

---

## 🔐 Privacy & Security

- ✅ **100% local** — fraud database lives on your machine, no cloud sync
- ✅ **No PII transmitted** — messages stay on device (unless Claude Vision OCR is used for screenshots)
- ✅ **Audit log** — all analyses stored in local SQLite only, no third-party logging
- ✅ **Open source** — every rule, weight, and keyword is readable and auditable

---

## 🆘 Indian Cybercrime Resources

| Resource | Details |
|---|---|
| 📞 **National Helpline** | **1930** — 24×7, free, handles all cybercrime |
| 🌐 **Report Online** | [cybercrime.gov.in](https://cybercrime.gov.in) |
| 🏦 **RBI Complaint** | [cms.rbi.org.in](https://cms.rbi.org.in) — banking fraud |
| 🔍 **SEBI Investor** | [scores.sebi.gov.in](https://scores.sebi.gov.in) — investment fraud |
| 🏛️ **I4C** | [i4c.mha.gov.in](https://i4c.mha.gov.in) — Cybercrime Coordination Centre |
| 📲 **TRAI DND** | [trai.gov.in](https://trai.gov.in) — block spam calls |

---

## 🗺️ Roadmap

- [ ] WhatsApp message share-sheet integration
- [ ] Crowdsourced fraud reporting (submit new flagged UPI IDs)
- [ ] Hindi / regional language scam message support
- [ ] Browser extension for real-time UPI page scanning
- [ ] Live NPCI / Razorpay IFSC API for bank validation
- [ ] PWA for offline mobile use
- [ ] Exportable PDF report for police complaint filing

---

## 🤝 Contributing

Most welcome — especially:

- 🆕 **New fraud UPI IDs / phones** — open an issue with evidence source
- 📩 **Scam message samples** — help expand keyword detection
- 🌐 **Regional language patterns** — Hindi, Tamil, Telugu UPI scam messages

```bash
# Dev setup
git clone https://github.com/yourname/sentinelpay-india
cd sentinelpay-india/backend
pip install -r requirements.txt
python -c "from fraud_db import init_db; init_db()"
python app.py
```

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ for 🇮🇳 India**

*Protecting Indian UPI users from cyber fraud — one transaction at a time.*

---

### 📞 Cybercrime Helpline: **1930**
### 🌐 [cybercrime.gov.in](https://cybercrime.gov.in)

---

*SentinelPay is an independent open-source tool.*
*Not affiliated with NPCI, RBI, PhonePe, Google Pay, or Paytm.*

</div>
