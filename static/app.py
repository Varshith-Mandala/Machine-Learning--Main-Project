from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load your pre-trained model once (replace 'brain_tumor_model.h5' with your model path)
model = load_model('D:\brain-tumour-detection\Brain_Tumor_Model.h5')

DATABASE = 'tumor_records.db'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create SQLite table if not exists
def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            filename TEXT,
            tumor_detected INTEGER,
            confidence REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def preprocess_img(img_path):
    img = image.load_img(img_path, target_size=(225, 225))  # Adjust to your model's input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('mri_image')
    name = request.form.get('name')
    age = request.form.get('age')

    if not file or not name or not age:
        return jsonify({'error': 'Missing data in request'}), 400

    # Save uploaded file
    unique_id = str(uuid.uuid4())
    filename = f"{unique_id}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Preprocess for model
    img_array = preprocess_img(filepath)

    # Predict
    prediction = model.predict(img_array)
    tumor_prob = prediction[0][0]  # Adjust this as per your model's output

    tumor_detected = int(tumor_prob > 0.5)

    # Store record in DB
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO records (id, name, age, filename, tumor_detected, confidence) VALUES (?, ?, ?, ?, ?, ?)',
        (unique_id, name, int(age), filename, tumor_detected, float(tumor_prob))
    )
    conn.commit()
    conn.close()

    # Return JSON result
    return jsonify({
        'tumor': bool(tumor_detected),
        'confidence': float(tumor_prob)
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
