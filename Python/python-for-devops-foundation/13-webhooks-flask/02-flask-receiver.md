# Flask Webhook Receiver

Install Flask:
```bash
python -m pip install Flask
```

Local development skeleton:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/webhooks/github")
def github_webhook():
    event = request.headers.get("X-GitHub-Event", "")
    delivery = request.headers.get("X-GitHub-Delivery", "")
    if not delivery:
        return jsonify(error="missing delivery id"), 400
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="invalid JSON"), 400
    # Verify signature before trusting or processing the payload.
    return jsonify(accepted=True, event=event), 202

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
```

This is not production-ready. Add signature verification, request-size limits, persistent deduplication and production WSGI hosting before deployment.

Exercise with curl:
```bash
curl -X POST http://127.0.0.1:5000/webhooks/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Delivery: local-test-001" \
  -H "X-GitHub-Event: issue_comment" \
  -d '{"action":"created"}'
```
