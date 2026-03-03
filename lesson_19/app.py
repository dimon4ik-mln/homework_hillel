import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# Створюємо папку uploads якщо її нема
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------------------
# POST /upload
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload_image():

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]
    filename = image.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    image.save(filepath)

    image_url = f"{request.host_url}uploads/{filename}"

    return jsonify({
        "image_url": image_url
    }), 201


# ---------------------------
# GET /uploads/<filename>
# ---------------------------
@app.route("/uploads/<filename>", methods=["GET"])
def serve_upload(filename):

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    return send_file(filepath)


# ---------------------------
# GET /image/<filename>
# ---------------------------
@app.route("/image/<filename>", methods=["GET"])
def get_image(filename):

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    # Якщо Content-Type = text → повертаємо JSON
    if request.headers.get("Content-Type") == "text":
        image_url = f"{request.host_url}uploads/{filename}"

        return jsonify({
            "image_url": image_url
        })

    return send_file(filepath)


# ---------------------------
# DELETE /delete/<filename>
# ---------------------------
@app.route("/delete/<filename>", methods=["DELETE"])
def delete_image(filename):

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    os.remove(filepath)

    image_url = f"{request.host_url}uploads/{filename}"

    return jsonify({
        "image_url": image_url
    })


# ---------------------------
# Запуск сервера
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)