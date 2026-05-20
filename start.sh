#!/bin/bash
# SentinelPay India — One-command startup

echo "🛡️  SentinelPay India — Starting..."

# Backend
echo ""
echo "▶ Starting Flask backend on :5000"
cd "$(dirname "$0")/backend"
pip install -r requirements.txt -q --break-system-packages 2>/dev/null
python app.py &
FLASK_PID=$!
echo "  Flask PID: $FLASK_PID"

# Wait for Flask to be ready
echo "  Waiting for backend..."
for i in $(seq 1 15); do
  if curl -sf http://localhost:5000/health > /dev/null 2>&1; then
    echo "  ✓ Backend ready"
    break
  fi
  sleep 1
done

# Frontend
echo ""
echo "▶ Starting Vite frontend on :3000"
cd "$(dirname "$0")/frontend"
npm install -q 2>/dev/null
npm run dev &
VITE_PID=$!

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌐  http://localhost:3000"
echo "  🔌  API  http://localhost:5000/health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Press Ctrl+C to stop both servers"
echo ""

trap "echo 'Stopping...'; kill $FLASK_PID $VITE_PID 2>/dev/null; exit 0" INT TERM
wait
