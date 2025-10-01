from flask import Flask, jsonify, request, send_file
from utils import playwright_utils, dataset_utils
import uuid
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
UPLOAD_FOLDER = "screenshots"
DATASET_FOLDER = "dataset"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify(message="Welcome to my Flask API!")

@app.route("/api/screenshot", methods=["GET"])
def screenshot():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    
    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        playwright_utils.take_webpage_screenshot(url, filepath)

        return send_file(filepath, mimetype="image/png")

    except Exception as e:
        print("E:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/save_screenshot", methods=["POST"])
def save_screenshot():
    label = request.form.get("label")
    if not label:
        return jsonify({"error": "Missing label"}), 400
    
    file = request.files.get("screenshot")
    if not file:
        return jsonify({"error": "Missing screenshot file"}), 400
    
    dataset_utils.save_screenshot_to_dataset(label, file)

    return jsonify({
        "status": "success",
        "label": label,
    })

if __name__ == "__main__":
    app.run(debug=True)
