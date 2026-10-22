from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the DevOps Flask REST API Microservice",
        "container_hostname": socket.gethostname(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "UP",
        "service": "flask-api",
        "code": 200
    }), 200


@app.route('/api/info', methods=['GET'])
def info():
    return jsonify({
        "module": "DevOps Day-02",
        "version": "1.0.0",
        "author": "CDAC Student",
        "endpoints": [
            "/",
            "/api/health",
            "/api/info"
        ]
    })


if __name__ == '__main__':
    # Listen on all container interfaces on port 5000
    app.run(host='0.0.0.0', port=5000)
