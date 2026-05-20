import { useState, useRef } from 'react'

const SAMPLES = [
  {
    tag: 'FRAUD', tagClass: 'danger',
    label: 'KYC Scam — SBI',
    text: 'URGENT: Your SBI account will be blocked in 24 hours. Complete KYC now. Send ₹1 to kyc.update@ybl to verify your account. Ref: KYC2024SBI',
  },
  {
    tag: 'FRAUD', tagClass: 'danger',
    label: 'Lottery Prize Fraud',
    text: 'Congratulations! You have won ₹50,000 in the India Lucky Draw 2024. To claim your prize, pay ₹500 processing fee to lotteryindia@ybl. Hurry! Offer expires in 2 hours.',
  },
  {
    tag: 'FRAUD', tagClass: 'danger',
    label: 'Fake Customer Support',
    text: '[PhonePe Alert] Your PhonePe account has been suspended. Contact our support team immediately. Pay ₹1 verification fee to google.pay.help@oksbi to reactivate.',
  },
  {
    tag: 'SAFE', tagClass: 'ok',
    label: 'Zomato Order',
    text: 'Zomato order #ZM789456 confirmed. Pay ₹349 to zomato@icici. Order: Butter Chicken + Naan from Punjabi Dhaba. Estimated delivery: 35 mins.',
  },
  {
    tag: 'FRAUD', tagClass: 'danger',
    label: 'Investment Scam',
    text: '[PhonePe] Trading.profit is requesting ₹25,000 from you. Note: Guaranteed 40% return in 7 days. SEBI registered scheme. Pay now to confirm your slot.',
  },
  {
    tag: 'FRAUD', tagClass: 'danger',
    label: 'OLX Army Scam',
    text: 'Hi, I am selling my Royal Enfield 350cc at ₹45,000. I am currently posted abroad with Indian Army. Pay advance of ₹5000 to army.sale@oksbi and I will ship via Army courier.',
  },
]

export default function AnalyzeInput({ onAnalyze, loading, online }) {
  const [mode, setMode] = useState('text')
  const [text, setText] = useState('')
  const [image, setImage] = useState(null)
  const [imageFile, setImageFile] = useState(null)
  const [drag, setDrag] = useState(false)
  const fileRef = useRef()

  const handleFile = (file) => {
    if (!file || !file.type.startsWith('image/')) return
    setImageFile(file)
    const reader = new FileReader()
    reader.onload = (e) => setImage(e.target.result)
    reader.readAsDataURL(file)
  }

  const onDrop = (e) => {
    e.preventDefault(); setDrag(false)
    handleFile(e.dataTransfer.files[0])
  }

  const isOffline = online === false
  const canSubmit = !isOffline && (mode === 'text' ? text.trim().length > 10 : !!imageFile)

  const submit = () => {
    if (!canSubmit || loading) return
    if (mode === 'text') onAnalyze({ type: 'text', text })
    else onAnalyze({ type: 'image', file: imageFile })
  }

  return (
    <>
      <div className="section-head">
        <span className="section-title">Analyze Transaction</span>
        <span className="section-tag">INR Only</span>
      </div>

      <div className="input-tabs">
        <button className={`input-tab${mode === 'text' ? ' active' : ''}`}
          onClick={() => setMode('text')}>✏️ Paste Message</button>
        <button className={`input-tab${mode === 'image' ? ' active' : ''}`}
          onClick={() => setMode('image')}>📸 Screenshot</button>
      </div>

      {mode === 'text' ? (
        <div className="text-input-wrap">
          <textarea
            className="msg-textarea"
            placeholder={`Paste any transaction message here:\n\n• UPI payment request\n• Bank SMS alert\n• PhonePe / GPay / Paytm message\n• WhatsApp payment request\n• Any suspicious message`}
            value={text}
            onChange={e => setText(e.target.value)}
            maxLength={5000}
          />
          <div className="char-count">{text.length} / 5000</div>

          <div className="samples-wrap">
            <div className="sample-label">Quick Test — Try a sample</div>
            {SAMPLES.map((s, i) => (
              <button key={i} className="sample-btn" onClick={() => { setText(s.text); setMode('text') }}>
                <span className={`sample-tag ${s.tagClass}`}>{s.tag}</span>
                {s.label}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <>
          {!image ? (
            <div
              className={`drop-zone${drag ? ' drag' : ''}`}
              onDragOver={e => { e.preventDefault(); setDrag(true) }}
              onDragLeave={() => setDrag(false)}
              onDrop={onDrop}
              onClick={() => fileRef.current?.click()}
            >
              <input ref={fileRef} type="file" accept="image/*"
                style={{ display: 'none' }}
                onChange={e => handleFile(e.target.files[0])} />
              <div className="drop-icon">📲</div>
              <div className="drop-label">Drop screenshot or tap to upload</div>
              <div className="drop-sub">PhonePe · GPay · Paytm · Bank SMS · WhatsApp</div>
              <div className="drop-sub">JPG, PNG, WebP — max 10MB</div>
            </div>
          ) : (
            <div className="img-preview">
              <img src={image} alt="Transaction screenshot" />
              <button className="img-remove" onClick={() => { setImage(null); setImageFile(null) }}>✕ Remove</button>
            </div>
          )}
          <div style={{ padding: '0 18px 8px', fontSize: 11, color: 'var(--muted)', lineHeight: 1.7 }}>
            <strong style={{ color: 'var(--text)' }}>Tips for best results:</strong><br/>
            • Crop tightly around the payment message<br/>
            • Ensure text is sharp and readable<br/>
            • Set <code style={{ color: 'var(--accent)', fontSize: 10 }}>ANTHROPIC_API_KEY</code> for Claude Vision (most accurate)
          </div>
        </>
      )}

      <button className="analyze-btn" onClick={submit} disabled={!canSubmit || loading}>
        {loading
          ? <><span className="spinner" />Analyzing…</>
          : isOffline
            ? '⚠ Backend Offline'
            : `🔍 Analyze ${mode === 'text' ? 'Message' : 'Screenshot'}`}
      </button>
    </>
  )
}
