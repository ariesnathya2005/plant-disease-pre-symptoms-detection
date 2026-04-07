from flask import Flask, render_template, request
import os
import numpy as np
import cv2
import tensorflow as tf

app = Flask(__name__)

UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ✅ Load model and class names
model = tf.keras.models.load_model("plant_disease_model_fixed.keras")
class_names = np.load("class_names.npy")

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Upload + Prediction
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if file and file.filename != "":
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # ✅ Image preprocessing
        img = cv2.imread(filepath)
        img = cv2.resize(img, (128, 128))
        img = img / 255.0
        img = np.reshape(img, (1, 128, 128, 3))

        # ✅ Prediction
        pred = model.predict(img)
        predicted_class = np.argmax(pred)
        result = class_names[predicted_class]

        return render_template("index.html", filename=file.filename, prediction=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)