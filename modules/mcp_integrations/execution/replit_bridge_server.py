"""
Antigravity Bridge Server v2 🌉
Run this on your Replit App to give Antigravity remote access to FILES and DATABASE.

Usage:
1. Create a file named 'bridge.py'
2. Paste this code
3. Run: python bridge.py
"""

import os
import json
from flask import Flask, request, jsonify
from replit import db

app = Flask(__name__)

AUTH_TOKEN = os.environ.get("BRIDGE_TOKEN", "antigravity-secret-key-123")

def check_auth():
    if request.headers.get("X-Auth-Token") != AUTH_TOKEN:
        return False
    return True

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Antigravity Bridge Online 🚀", "cwd": os.getcwd()})

# === FILE SYSTEM ===
@app.route("/files/read", methods=["GET"])
def read_file():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    try:
        with open(request.args.get("path"), "r", encoding="utf-8") as f:
            return jsonify({"content": f.read()})
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/files/write", methods=["POST"])
def write_file():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    try:
        path = request.json.get("path")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(request.json.get("content"))
        return jsonify({"status": "success"})
    except Exception as e: return jsonify({"error": str(e)}), 500

# === DATABASE ===
@app.route("/db/get", methods=["GET"])
def get_db():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    try:
        key = request.args.get("key")
        val = db.get(key)
        return jsonify({"value": val})
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/db/set", methods=["POST"])
def set_db():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    try:
        key = request.json.get("key")
        val = request.json.get("value")
        db[key] = val
        return jsonify({"status": "success", "key": key})
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
