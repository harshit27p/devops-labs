import os
from flask import Flask, abort, jsonify, request
from signature import verify_github_signature
from github_events import should_create_ticket

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

@app.post("/webhooks/github")
def github_webhook():
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    if not secret:
        abort(503)
    raw_body = request.get_data(cache=True)
    signature = request.headers.get("X-Hub-Signature-256", "")
    if not verify_github_signature(secret, raw_body, signature):
        abort(401)

    event = request.headers.get("X-GitHub-Event", "")
    delivery_id = request.headers.get("X-GitHub-Delivery", "")
    payload = request.get_json(silent=True)
    if not delivery_id or not isinstance(payload, dict):
        abort(400)

    allowed_repo = os.environ.get("GITHUB_ALLOWED_REPOSITORY", "")
    if not should_create_ticket(event, payload, allowed_repo):
        return jsonify(accepted=True, action="ignored"), 202

    # TODO: persist delivery_id with a unique constraint, then enqueue/process.
    return jsonify(accepted=True, action="queued-placeholder",
                   delivery_id=delivery_id), 202

if __name__ == "__main__":
    # Local development only; use a production WSGI server when deployed.
    app.run(host="127.0.0.1", port=5000, debug=True)
