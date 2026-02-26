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

    image_url = f"http://127.0.0.1:8080/uploads/{filename}"

    return jsonify({
        "image_url": image_url
    }), 201


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

        image_url = f"http://127.0.0.1:8080/uploads/{filename}"

        return jsonify({
            "image_url": image_url
        })

    # Інакше повертаємо саме зображення
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

    image_url = f"http://127.0.0.1:8080/uploads/{filename}"

    return jsonify({
        "image_url": image_url
    })


# ---------------------------
# Запуск сервера
# ---------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)