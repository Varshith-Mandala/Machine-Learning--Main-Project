from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import uuid
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


app = Flask(__name__)
CORS(app)

DATABASE = 'tumor_records.db'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)



print("Loading model...")
model = load_model("brain_tumor_mobilenetv2_model2.h5")
print("Model loaded successfully!")



def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            filename TEXT,
            tumor_detected INTEGER,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()



def preprocess_img(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array / 255.0



def is_mri(img):
    """
    Light-weight MRI validation:
    - Reject small images
    - Reject highly colored images
    """
    arr = np.array(img)


    if arr.shape[0] < 80 or arr.shape[1] < 80:
        return False

    
    if len(arr.shape) == 3:
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        color_diff = np.mean(np.abs(r - g)) + np.mean(np.abs(g - b))
        if color_diff > 25: 
            return False

    return True



@app.route('/records', methods=['GET'])
def get_records():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM records")
    rows = cur.fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append({
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "filename": row[3],
            "tumor_detected": row[4],
            "confidence": row[5]
        })

    return jsonify(records)



@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('mri_image')
    name = request.form.get('name')
    age = request.form.get('age')


    if not file or not name or not age:
        return jsonify({'error': 'Missing data in request'}), 400

    
    try:
        img_raw = Image.open(file).convert("RGB")
    except:
        return jsonify({'error': 'Invalid image file'}), 400

    # Validate MRI
    if not is_mri(img_raw):
        return jsonify({'error': 'Invalid MRI Image'}), 400

    # Save image
    unique_id = str(uuid.uuid4())
    filename = f"{unique_id}.jpg"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    img_raw.save(file_path)

    # Preprocess
    img = preprocess_img(file_path)

    # Predict
    prediction = model.predict(img)[0]

    # Case 1: sigmoid output [0.92]
    # Case 2: softmax output [0.05, 0.95]
    if len(prediction) == 2:
        tumor_detected = int(np.argmax(prediction))
        confidence = float(max(prediction))
    else:
        tumor_detected = int(prediction[0] > 0.5)
        confidence = float(prediction[0])

    # Save record
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO records (id, name, age, filename, tumor_detected, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (unique_id, name, age, filename, tumor_detected, confidence))
    conn.commit()
    conn.close()

    return jsonify({
        'id': unique_id,
        'tumor_detected': tumor_detected,
        'confidence': confidence
    })



if __name__ == "__main__":
    app.run(debug=True)
