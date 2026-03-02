🚀 Project Overview

Brain tumor detection from MRI scans is a critical medical imaging task.
Instead of training a CNN from scratch, this project leverages a pretrained model (transfer learning) to improve performance and reduce training time.

The workflow includes:

MRI image preprocessing using OpenCV

Transfer learning using a pretrained CNN model

Model fine-tuning on brain MRI dataset

Performance evaluation using validation metrics

Web application for prediction

MySQL database integration for storing patient records

📂 Dataset

Source: [https://www.kaggle.com/code/mahmoudmagdyelnahal/brain-mri-images-for-brain-tumor-detection]

Total Images: 200

Classes:

Tumor

No Tumor

Train/Test Split: 80/20

Preprocessing Steps:

Image resizing

Normalization

Data augmentation

Conversion to tensor format
