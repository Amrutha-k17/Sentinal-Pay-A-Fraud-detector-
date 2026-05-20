"""
SentinelPay India — Flask API
Routes: POST /analyze/text, POST /analyze/image, GET /stats, GET /health
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

import fraud_db as db
from analyzer import analyze_text, analyze_image_result
from ocr import extract_from_image

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
}})

# ── Init DB on startup ─────────────────────────────────────────────────────────
db.init_db()

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "SentinelPay India"})


@app.route("/stats")
def stats():
    try:
        return jsonify(db.get_stats())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze/text", methods=["POST"])
def analyze_text_route():
    body = request.get_json(silent=True)
    if not body or not body.get("text", "").strip():
        return jsonify({"error": "Field 'text' is required and must not be empty"}), 400

    text = body["text"].strip()
    if len(text) > 5000:
        return jsonify({"error": "Text too long (max 5000 chars)"}), 400

    try:
        report = analyze_text(text)
        log.info(f"[TEXT] verdict={report.verdict} score={report.risk_score} upi={report.extracted.get('receiver_upi')}")
        return jsonify(report.to_dict())
    except Exception as e:
        log.exception("analyze/text error")
        return jsonify({"error": str(e)}), 500


@app.route("/analyze/image", methods=["POST"])
def analyze_image_route():
    # Accept multipart/form-data OR JSON with base64
    img_bytes = None
    media_type = "image/jpeg"

    if request.content_type and "multipart" in request.content_type:
        if "image" not in request.files:
            return jsonify({"error": "No 'image' file in request"}), 400
        f = request.files["image"]
        img_bytes = f.read()
        media_type = f.content_type or "image/jpeg"
    else:
        body = request.get_json(silent=True)
        if not body or not body.get("image_base64"):
            return jsonify({"error": "Provide 'image' file (multipart) or 'image_base64' (JSON)"}), 400
        import base64
        try:
            img_bytes = base64.b64decode(body["image_base64"])
            media_type = body.get("media_type", "image/jpeg")
        except Exception:
            return jsonify({"error": "Invalid base64 image data"}), 400

    if len(img_bytes) > 10 * 1024 * 1024:
        return jsonify({"error": "Image too large (max 10MB)"}), 400

    try:
        ocr_result = extract_from_image(img_bytes, media_type)
        if ocr_result["error"] and not ocr_result["text"]:
            return jsonify({"error": f"OCR failed: {ocr_result['error']}"}), 500

        report = analyze_image_result(ocr_result)
        log.info(f"[IMAGE] method={ocr_result['method']} verdict={report.verdict} score={report.risk_score}")
        resp = report.to_dict()
        resp["ocr_text_preview"] = (ocr_result.get("text") or "")[:300]
        return jsonify(resp)
    except Exception as e:
        log.exception("analyze/image error")
        return jsonify({"error": str(e)}), 500


@app.route("/db/lookup", methods=["POST"])
def db_lookup():
    """Quick lookup endpoint for UPI/phone."""
    body = request.get_json(silent=True) or {}
    result = {}
    if body.get("upi"):
        result["upi"] = db.lookup_upi(body["upi"])
    if body.get("phone"):
        result["phone"] = db.lookup_phone(body["phone"])
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
