const BASE = import.meta.env.VITE_API_URL || 'https://sentinal-pay-a-fraud-detector.onrender.com'

async function apiFetch(path, opts = {}) {
  let res
  try {
    res = await fetch(`${BASE}${path}`, opts)
  } catch (networkErr) {
    throw new Error('Cannot reach backend. Make sure Flask is running on port 5000.')
  }

  // Try JSON first; fall back to text so we never silently swallow HTML error pages
  const contentType = res.headers.get('content-type') || ''
  let body
  if (contentType.includes('application/json')) {
    body = await res.json()
  } else {
    const text = await res.text()
    // Proxy/nginx HTML error pages
    if (!res.ok) {
      const status = res.status
      if (status === 503 || status === 502 || status === 504)
        throw new Error('Backend offline — run: cd backend && python app.py')
      if (status === 403)
        throw new Error('Access denied (403). Check Flask CORS config.')
      throw new Error(`Server error ${status}: ${text.slice(0, 120)}`)
    }
    body = { raw: text }
  }

  if (!res.ok) {
    throw new Error(body?.error || body?.message || `Request failed (${res.status})`)
  }
  return body
}

export const api = {
  health: () => apiFetch('/health'),
  stats:  () => apiFetch('/stats'),

  analyzeText: (text) => apiFetch('/analyze/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  }),

  analyzeImage: (file) => {
    const fd = new FormData()
    fd.append('image', file)
    return apiFetch('/analyze/image', { method: 'POST', body: fd })
  },
}
