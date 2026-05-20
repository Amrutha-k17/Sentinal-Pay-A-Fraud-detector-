"""
OCR Service
Primary: Claude Vision API (accurate, structured)
Fallback: pytesseract (local, no API key needed)
"""

import os
import base64
import json
import re
import logging
from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract

log = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── Image Preprocessing ────────────────────────────────────────────────────────

def preprocess_image(img: Image.Image) -> Image.Image:
    """Enhance image for better OCR accuracy."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Resize if too small
    w, h = img.size
    if w < 600:
        scale = 600 / w
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    # Enhance contrast + sharpness
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Sharpness(img).enhance(1.8)
    return img


def image_to_base64(img: Image.Image, fmt="JPEG") -> str:
    buf = BytesIO()
    img.save(buf, format=fmt, quality=95)
    return base64.b64encode(buf.getvalue()).decode()


# ── Claude Vision (Primary) ────────────────────────────────────────────────────

VISION_PROMPT = """You are analyzing a screenshot of a financial transaction message or payment request (Indian UPI/bank/payment app).

Extract ALL visible transaction details and return ONLY a valid JSON object with these fields (use null if not found):
{
  "receiver_name": "string or null",
  "receiver_upi": "string (UPI ID like name@handle) or null",
  "receiver_phone": "10-digit Indian mobile or null",
  "receiver_account": "bank account number or null",
  "receiver_ifsc": "IFSC code or null",
  "amount": number (in INR, no commas) or null,
  "purpose": "payment purpose/note or null",
  "sender_name": "string or null",
  "bank_name": "bank name or null",
  "source_app": "PhonePe/Google Pay/Paytm/BHIM/Bank SMS/WhatsApp/Other",
  "txn_type": "REQUEST/RECEIVED/SENT/ALERT/UNKNOWN",
  "is_payment_request": true or false,
  "ref_number": "reference/UTR number or null",
  "full_extracted_text": "complete text visible in screenshot"
}

Extract EXACTLY what is visible. Do not infer or hallucinate. Return only the JSON."""


def extract_via_claude(image_bytes: bytes, media_type: str = "image/jpeg") -> dict:
    """Use Claude Vision API to extract transaction details from screenshot."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    import urllib.request
    img_b64 = base64.b64encode(image_bytes).decode()

    payload = json.dumps({
        "model": "claude-opus-4-5",
        "max_tokens": 1024,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": img_b64
                }},
                {"type": "text", "text": VISION_PROMPT}
            ]
        }]
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    text = data["content"][0]["text"].strip()
    # Strip markdown fences if present
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text)


# ── Tesseract (Fallback) ───────────────────────────────────────────────────────

def extract_via_tesseract(image_bytes: bytes) -> str:
    img = Image.open(BytesIO(image_bytes))
    img = preprocess_image(img)
    # Try multiple PSM modes, pick best result
    configs = ["--psm 6", "--psm 4", "--psm 3"]
    results = []
    for cfg in configs:
        try:
            text = pytesseract.image_to_string(img, lang="eng", config=cfg)
            results.append(text)
        except Exception:
            pass
    # Pick the longest result (most extracted)
    return max(results, key=len) if results else ""


# ── Main Entry ─────────────────────────────────────────────────────────────────

def extract_from_image(image_bytes: bytes, media_type: str = "image/jpeg") -> dict:
    """
    Returns dict with:
      extracted: dict of parsed fields (from Claude) or None
      text: raw OCR text (from tesseract fallback)
      method: "claude_vision" | "tesseract"
      error: str or None
    """
    # Try Claude Vision first
    if ANTHROPIC_API_KEY:
        try:
            extracted = extract_via_claude(image_bytes, media_type)
            log.info("[OCR] Claude Vision extraction successful")
            return {
                "extracted": extracted,
                "text": extracted.get("full_extracted_text", ""),
                "method": "claude_vision",
                "error": None,
            }
        except Exception as e:
            log.warning(f"[OCR] Claude Vision failed: {e}, falling back to tesseract")

    # Fallback: tesseract
    try:
        text = extract_via_tesseract(image_bytes)
        log.info(f"[OCR] Tesseract extracted {len(text)} chars")
        return {
            "extracted": None,
            "text": text,
            "method": "tesseract",
            "error": None,
        }
    except Exception as e:
        log.error(f"[OCR] Tesseract failed: {e}")
        return {
            "extracted": None,
            "text": "",
            "method": "failed",
            "error": str(e),
        }
