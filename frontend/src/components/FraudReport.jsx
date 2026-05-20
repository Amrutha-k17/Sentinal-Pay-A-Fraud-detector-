const SEV_ORDER = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 }
const VERDICT_CLASS = (v) => v?.replace(' ', '-') ?? ''

const fmt_inr = (n) => n != null
  ? `₹${Number(n).toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`
  : null

const DetailItem = ({ label, value, cls = '' }) => (
  <div className="detail-item">
    <span className="detail-label">{label}</span>
    <span className={`detail-value ${cls} ${value == null ? 'null' : ''}`}>
      {value ?? '—'}
    </span>
  </div>
)

export default function FraudReport({ report }) {
  if (!report) return null

  const { verdict, risk_score, extracted, risk_flags, db_match,
          recommendation, advice, report_id, timestamp, parse_confidence,
          input_type, ocr_method } = report

  const vc = VERDICT_CLASS(verdict)
  const sortedFlags = [...(risk_flags || [])].sort(
    (a, b) => (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9)
  )

  const verdictIcon = {
    'DANGEROUS':   '🚨',
    'SUSPICIOUS':  '⚠️',
    'CAUTION':     '🔍',
    'LIKELY SAFE': '✅',
  }[verdict] ?? '❓'

  const recIcon = verdict === 'DANGEROUS' ? '🚫' :
                  verdict === 'SUSPICIOUS' ? '⚠️' :
                  verdict === 'CAUTION'    ? '🔍' : '✅'

  return (
    <div className="report-wrap">

      {/* ── Verdict Banner ──────────────────────────────────────────── */}
      <div className={`verdict-banner ${vc}`}>
        <div className="verdict-left">
          <div className="verdict-label">Risk Verdict · Report #{report_id}</div>
          <div className="verdict-text">{verdictIcon} {verdict}</div>
          <div className={`score-bar ${vc}`} style={{ width: 220 }}>
            <div className="score-fill" style={{ width: `${risk_score * 100}%` }} />
          </div>
        </div>
        <div className="verdict-right">
          <div className="risk-pct">{(risk_score * 100).toFixed(0)}%</div>
          <div className="risk-pct-sub">Risk Score</div>
        </div>
      </div>

      {/* ── Recommendation ──────────────────────────────────────────── */}
      <div className="rec-box">
        <div className="rec-icon">{recIcon}</div>
        <div className="rec-content">
          <div className="rec-title">Recommendation</div>
          <div className="rec-text">{recommendation}</div>
        </div>
      </div>

      {/* ── Extracted Details ────────────────────────────────────────── */}
      <div className="report-card">
        <div className="card-head">
          <span className="card-title">Extracted Transaction Details</span>
          <span className="card-badge" style={{ background: 'rgba(0,212,255,.1)', color: 'var(--accent)' }}>
            {input_type === 'image' ? `📸 ${ocr_method ?? 'OCR'}` : '✏️ Text'}
          </span>
        </div>
        <div className="card-body">
          <div className="details-grid">
            <DetailItem label="Receiver UPI"
              value={extracted.receiver_upi}
              cls={extracted.receiver_upi ? 'upi' : ''} />
            <DetailItem label="Amount (INR)"
              value={fmt_inr(extracted.amount)}
              cls={extracted.amount ? 'amount' : ''} />
            <DetailItem label="Receiver Name"
              value={extracted.receiver_name} />
            <DetailItem label="Bank"
              value={extracted.bank_name} />
            <DetailItem label="Phone Number"
              value={extracted.receiver_phone ? `+91 ${extracted.receiver_phone}` : null} />
            <DetailItem label="Source App"
              value={extracted.source_app} cls="app" />
            <DetailItem label="Purpose / Note"
              value={extracted.purpose} />
            <DetailItem label="Reference No."
              value={extracted.ref_number} />
          </div>
          {extracted.receiver_account && (
            <div style={{ marginTop: 10, paddingTop: 10, borderTop: '1px solid var(--border)' }}>
              <DetailItem label="Account Number" value={extracted.receiver_account} />
            </div>
          )}
          <div className="confidence-bar">
            <span className="conf-label">Parse confidence</span>
            <div className="conf-track">
              <div className="conf-fill" style={{ width: `${parse_confidence * 100}%` }} />
            </div>
            <span className="conf-val">{(parse_confidence * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* ── Risk Flags ────────────────────────────────────────────────── */}
      <div className="report-card">
        <div className="card-head">
          <span className="card-title">Risk Flags</span>
          <span className="card-badge"
            style={{
              background: sortedFlags.length ? 'var(--danger-bg)' : 'var(--ok-bg)',
              color: sortedFlags.length ? 'var(--danger)' : 'var(--ok)'
            }}>
            {sortedFlags.length} found
          </span>
        </div>
        <div className="card-body">
          {sortedFlags.length === 0 ? (
            <div className="no-flags">✓ No fraud indicators detected</div>
          ) : (
            <div className="flags-list">
              {sortedFlags.map((f, i) => (
                <div key={i} className={`flag-item ${f.severity}`}>
                  <span className={`flag-sev ${f.severity}`}>{f.severity}</span>
                  <div className="flag-content">
                    <div className="flag-title">{f.title}</div>
                    <div className="flag-detail">{f.detail}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ── Database Match ────────────────────────────────────────────── */}
      <div className="report-card">
        <div className="card-head">
          <span className="card-title">Fraud Database Match</span>
          <span className="card-badge"
            style={{
              background: db_match.found ? 'var(--danger-bg)' : 'var(--ok-bg)',
              color: db_match.found ? 'var(--danger)' : 'var(--ok)'
            }}>
            {db_match.found ? '⚠ MATCHED' : '✓ CLEAN'}
          </span>
        </div>
        <div className="card-body">
          {db_match.found ? (
            <div className="db-match-hit">
              {db_match.entries.map((entry, i) => (
                <div key={i} className="db-entry" style={{ marginBottom: i < db_match.entries.length - 1 ? 12 : 0 }}>
                  <div className="db-fraud-type">⚠ {entry.fraud_type}</div>
                  <div className="db-stats">
                    {entry.report_count && (
                      <div className="db-stat">Reports: <span>{entry.report_count}</span></div>
                    )}
                    {entry.severity && (
                      <div className="db-stat">Severity: <span>{entry.severity}</span></div>
                    )}
                    {entry.first_reported && (
                      <div className="db-stat">First reported: <span>{entry.first_reported?.slice(0,10)}</span></div>
                    )}
                    {entry.bank && (
                      <div className="db-stat">Bank: <span>{entry.bank}</span></div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="db-match-miss">
              ✓ No matches found in fraud database — not a known fraudulent identifier
            </div>
          )}
        </div>
      </div>

      {/* ── Safety Advice ─────────────────────────────────────────────── */}
      <div className="report-card">
        <div className="card-head">
          <span className="card-title">Safety Advice</span>
          <span className="card-badge" style={{ background: 'var(--ok-bg)', color: 'var(--ok)' }}>Helpline: 1930</span>
        </div>
        <div className="card-body">
          <div className="advice-list">
            {(advice || []).map((a, i) => (
              <div key={i} className="advice-item">
                <span className="advice-dot">›</span>
                <span>{a}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Report Meta ───────────────────────────────────────────────── */}
      <div className="report-meta">
        <div className="meta-item">ID: <span>#{report_id}</span></div>
        <div className="meta-item">Time: <span>{new Date(timestamp).toLocaleTimeString('en-IN')}</span></div>
        <div className="meta-item">Input: <span>{input_type}</span></div>
        {ocr_method && <div className="meta-item">OCR: <span>{ocr_method}</span></div>}
      </div>

    </div>
  )
}
