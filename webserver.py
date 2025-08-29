from flask import Flask, send_from_directory
import os

app = Flask(__name__)
OUTPUT_DIR = "/app/output"

@app.route("/")
def list_files():
    files = os.listdir(OUTPUT_DIR)
    return "<br>".join([f"<a href='/files/{f}'>{f}</a>" for f in files])

@app.route("/files/<path:filename>")
def serve_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
