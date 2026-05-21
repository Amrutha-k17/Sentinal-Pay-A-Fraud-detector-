<div align="center">

# 🛡️ SentinelPay
### *AI-Powered Payment Fraud Detection*

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Vercel-black?style=for-the-badge)](https://sentinal-pay-a-fraud-detector.vercel.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Amrutha-k17/Sentinal-Pay-A-Fraud-detector-)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **SentinelPay** is a full-stack fraud detection application that uses machine learning to analyze payment transactions in real time and flag suspicious activity with explainable results.

</div>

---

## ✨ Features

- 🔍 **Real-time fraud scoring** — instantly classify transactions as legitimate or fraudulent
- 📊 **Risk dashboard** — visual breakdown of fraud probability and contributing factors
- 🤖 **ML-powered backend** — trained model serves predictions via REST API
- 📈 **Transaction history** — track and review past analyzed transactions
- 📱 **Responsive UI** — clean, modern interface works across all devices

---

## 🖼️ Demo

🔗 **[sentinal-pay-a-fraud-detector.vercel.app](https://sentinal-pay-a-fraud-detector.vercel.app/)**

---

## 🗂️ Project Structure

```
Sentinal-Pay-A-Fraud-detector/
│
├── frontend/                  # React application (Vite)
│   ├── public/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Route-level pages
│   │   ├── services/          # API call handlers
│   │   └── App.jsx
│   ├── index.html
│   └── package.json
│
├── backend/                   # Python / Flask or FastAPI server
│   ├── model/                 # Trained ML model & scaler
│   │   ├── fraud_model.pkl
│   │   └── scaler.pkl
│   ├── app.py                 # API entry point
│   ├── predict.py             # Prediction logic
│   └── requirements.txt
│
└── README.md
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React, Vite, Tailwind CSS |
| **Backend** | Python, Flask / FastAPI |
| **ML Model** | Scikit-learn (Random Forest / XGBoost) |
| **Deployment** | Vercel (frontend), Render / Railway (backend) |
| **Data** | Synthetic / public payment fraud datasets |

---

## 🚀 Getting Started

### Prerequisites

- Node.js ≥ 18
- Python ≥ 3.9
- pip / virtualenv

### 1. Clone the repo

```bash
git clone https://github.com/Amrutha-k17/Sentinal-Pay-A-Fraud-detector-.git
cd Sentinal-Pay-A-Fraud-detector-
```

### 2. Start the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs at `http://localhost:5000`

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/predict` | Submit transaction for fraud analysis |
| `GET` | `/history` | Retrieve past transaction results |
| `GET` | `/health` | Server health check |

**Sample request:**
```json
POST /predict
{
  "amount": 4500.00,
  "transaction_type": "TRANSFER",
  "old_balance": 5000.00,
  "new_balance": 500.00
}
```

**Sample response:**
```json
{
  "is_fraud": true,
  "fraud_probability": 0.94,
  "risk_level": "HIGH"
}
```

---

## 🧠 How It Works

```
User Input  →  React Form  →  API Request  →  ML Model  →  Fraud Score  →  UI Result
```

1. User enters transaction details in the web UI
2. Frontend sends a POST request to the backend API
3. The ML model preprocesses and scores the transaction
4. Fraud probability and risk label are returned
5. Results are displayed with visual indicators

---

## 📦 Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:5000
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 👩‍💻 Author

**Amrutha K**
[![GitHub](https://img.shields.io/badge/GitHub-Amrutha--k17-181717?style=flat&logo=github)](https://github.com/Amrutha-k17)

---

<div align="center">

Made to keep payments safe

</div>
