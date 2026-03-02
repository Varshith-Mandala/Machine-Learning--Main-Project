from tensorflow.keras.models import load_model

model = load_model("Brain_Tumor_Model.h5")
model.summary()
