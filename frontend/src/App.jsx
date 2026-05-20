import { useState, useEffect, useRef } from 'react'
import AnalyzeInput from './components/AnalyzeInput'
import FraudReport from './components/FraudReport'
import { api } from './utils/api'
import './styles/index.css'

const VERDICT_CLASS = (v) => v?.replace(' ', '-') ?? ''

export default function App() {
  const [report, setReport]   = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)
  const [online, setOnline]   = useState(null)   // null = checking
  const pollRef               = useRef(null)

  // ── Health polling every 5 s ──────────────────────────────────────────
  const checkHealth = () =>
    api.health()
      .then(() => setOnline(true))
      .catch(() => setOnline(false))

  useEffect(() => {
    checkHealth()
    pollRef.current = setInterval(checkHealth, 5000)
    return () => clearInterval(pollRef.current)
  }, [])

  // ── Analyze ───────────────────────────────────────────────────────────
  const handleAnalyze = async ({ type, text, file }) => {
    if (!online) {
      setError('Backend is offline. Start Flask first: cd backend && python app.py')
      return
    }
    setLoading(true)
    setError(null)
    try {
      const result = type === 'text'
        ? await api.analyzeText(text)
        : await api.analyzeImage(file)
      setReport(result)
      setHistory(prev => [result, ...prev].slice(0, 20))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const statusLabel = online === null ? 'Connecting…' : online ? 'API Online' : 'API Offline'
  const statusClass = online === null ? '' : online ? '' : ' offline'

  return (
    <div className="app">
      {/* ── Header ──────────────────────────────────────────────────── */}
      <header className="header">
        <div className="brand">
          <span className="brand-icon">🛡️</span>
          SentinelPay India
        </div>
        <div className="header-meta">
          <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--muted)' }}>
            UPI Fraud Analyzer
          </span>
          <div className={`status-pill${statusClass}`}>
            <div className="status-dot" />
            {statusLabel}
          </div>
        </div>
      </header>

      {/* ── Offline banner ───────────────────────────────────────────── */}
      {online === false && (
        <div className="offline-banner">
          <span>⚠ Flask backend is not running.</span>
          <code>cd backend &amp;&amp; python app.py</code>
        </div>
      )}

      <div className="main">
        {/* ── Left panel ─────────────────────────────────────────────── */}
        <div className="left-panel">
          <AnalyzeInput onAnalyze={handleAnalyze} loading={loading} online={online} />

          {error && (
            <div className="error-box">
              <span className="error-icon">⚠</span>
              <span>{error}</span>
              <button className="error-dismiss" onClick={() => setError(null)}>✕</button>
            </div>
          )}

          {/* History */}
          {history.length > 0 && (
            <div className="history-strip">
              <div className="history-head">Recent Analyses ({history.length})</div>
              {history.map((h, i) => (
                <div key={i} className="history-item" onClick={() => setReport(h)}>
                  <span className={`hist-verdict ${VERDICT_CLASS(h.verdict)}`}>
                    {h.verdict?.split(' ')[0]}
                  </span>
                  <span className="hist-upi">
                    {h.extracted?.receiver_upi ||
                     h.extracted?.receiver_phone ||
                     h.extracted?.receiver_name ||
                     'Unknown receiver'}
                  </span>
                  <span className="hist-score">
                    {h.extracted?.amount != null
                      ? `₹${Number(h.extracted.amount).toLocaleString('en-IN')}`
                      : '—'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ── Right panel ─────────────────────────────────────────────── */}
        <div className="right-panel">
          {!report && !loading ? (
            <div className="empty-state">
              <div className="empty-icon">🔍</div>
              <div className="empty-title">No Analysis Yet</div>
              <div className="empty-sub">
                Paste a UPI payment request, bank SMS, or any suspicious
                transaction message — or upload a screenshot — to get an
                instant fraud report.
              </div>
              <div className="feature-list">
                {[
                  ['🚨', 'UPI ID blacklist check'],
                  ['🔑', 'Scam keyword detection'],
                  ['📊', 'Pattern-based risk scoring'],
                  ['📸', 'Screenshot OCR analysis'],
                  ['🏦', 'Indian bank & UPI formats'],
                  ['📞', 'Phone number lookup'],
                ].map(([icon, txt]) => (
                  <div key={txt} className="feature-item">
                    <span>{icon}</span><span>{txt}</span>
                  </div>
                ))}
              </div>
              {online === false && (
                <div className="empty-offline">
                  <strong>Start the backend first:</strong>
                  <code>cd backend &amp;&amp; python app.py</code>
                </div>
              )}
            </div>
          ) : loading ? (
            <div className="empty-state">
              <div style={{ fontSize: 40 }}>🔄</div>
              <div className="empty-title">Analyzing Transaction…</div>
              <div className="empty-sub">
                Checking fraud database · Scanning keywords · Computing risk score
              </div>
            </div>
          ) : (
            <FraudReport report={report} />
          )}
        </div>
      </div>
    </div>
  )
}
