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

Source: [https://storage.googleapis.com/kaggle-data-sets/165566/377107/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20251204%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20251204T100022Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=61fb7bcf3efd823a8ab15d453fbb3260732c2b2126240b41c05ccbd8f3dd2f6d159d069e0c1fbb7e2c69d48c2faf09819d16b455ed5b83b40021e278f3ba9f4b83b807fda85ec97745c69b6169050f7bc34283e0745483c31e007cad8bbeec32decb6b9e0c5e82936d8261cb9b02885f06eebf72739937d9a8bbf969dcb68cb338479f73ec7651db9609848794b3f5f2a9f4dee95a6efdb86f37da3626165e7fe7d0b69e72368878f09aadee8a2c6656750ea8bef05d66083bc1e75b50091e5ba5b111631addf94308931fbd94bb53ca84b2bc52e07aec68c1df1553d18e7657ee73f60b402bd3c3fd21d0a6d23b51fa68f4103f2f433af3993e05734c984c26]

Total Images: XXXX

Classes:

Tumor

No Tumor

Train/Test Split: 80/20

Preprocessing Steps:

Image resizing

Normalization

Data augmentation

Conversion to tensor format
