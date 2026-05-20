# 🛡️ SentinelPay India — UPI Fraud Analyzer

Real-time Indian transaction fraud detection via text message or screenshot.

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
# Optional: set for Claude Vision OCR (best accuracy)
export ANTHROPIC_API_KEY=your_key_here
python app.py          # → http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm run dev            # → http://localhost:3000
```

## How It Works

1. **Input** — Paste a UPI payment message OR upload a screenshot (PhonePe, GPay, Paytm, bank SMS, WhatsApp)
2. **OCR** — Claude Vision API (primary) or Tesseract (fallback) extracts text from images
3. **Parse** — Regex engine extracts UPI ID, phone, amount, purpose, app source
4. **DB Check** — SQLite fraud database (~50 UPI IDs, ~18 phones, scam keywords)
5. **Score** — Multi-signal risk scoring (DB hits + keyword matches + heuristics)
6. **Report** — Verdict (DANGEROUS / SUSPICIOUS / CAUTION / LIKELY SAFE) + flags + advice

## API Endpoints

| Method | Path              | Description                    |
|--------|-------------------|--------------------------------|
| GET    | `/health`         | Service status                 |
| GET    | `/stats`          | DB stats + recent analyses     |
| POST   | `/analyze/text`   | Analyze pasted message         |
| POST   | `/analyze/image`  | Analyze screenshot (multipart) |
| POST   | `/db/lookup`      | Quick UPI/phone lookup         |

### POST /analyze/text
```json
{ "text": "Pay ₹1 to kyc.update@ybl for KYC verification" }
```

### POST /analyze/image
```
Content-Type: multipart/form-data
Field: image (file)
```

### Sample Response
```json
{
  "verdict": "DANGEROUS",
  "risk_score": 1.0,
  "recommendation": "DO NOT PAY. Banks never ask you to send money for KYC.",
  "extracted": {
    "receiver_upi": "kyc.update@ybl",
    "amount": 1.0,
    "bank_name": "Yes Bank / PhonePe"
  },
  "risk_flags": [
    { "severity": "CRITICAL", "title": "UPI ID in Fraud Database", "detail": "..." },
    { "severity": "CRITICAL", "title": "₹1 Verification Trick", "detail": "..." }
  ],
  "db_match": { "found": true, "fraud_type": "KYC Fraud", "report_count": 234 }
}
```

## Fraud Database (Seeded)

| Table              | Entries | Coverage                            |
|--------------------|---------|-------------------------------------|
| flagged_upi        | ~38     | KYC, Lottery, Investment, OLX scams |
| flagged_phone      | ~18     | Vishing, SIM swap, UPI fraud        |
| flagged_account    | ~8      | Money mule accounts                 |
| scam_keywords      | ~40     | KYC, lottery, investment keywords   |

## Helpline
🆘 Cybercrime Helpline: **1930** | Portal: **cybercrime.gov.in**
