# Face Recognition API

A FastAPI project for **Face Embedding Generation** and **Document OCR** using InsightFace and Tesseract OCR.

## Features

- Face Embedding Generation (512 Dimensions)
- Face Recognition using InsightFace
- Aadhaar & PAN OCR
- FastAPI REST API
- No Image Storage (Processed in Memory)

---

## Tech Stack

- Python
- FastAPI
- InsightFace
- OpenCV
- Tesseract OCR

---

## Installation

Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

API Docs:

```
http://127.0.0.1:8000/docs
```

---

## Face Embedding Flow

```
Image
   ↓
InsightFace
   ↓
512-D Embedding
   ↓
Store in Database
```

For verification:

```
New Image
   ↓
Embedding
   ↓
Cosine Similarity
   ↓
Match / No Match
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home Page |
| POST | `/register-face` | Generate Face Embedding |
| POST | `/extract-document` | Extract Aadhaar/PAN Details |

---

## Author

**Adarsh Patel**

GitHub: https://github.com/Adarshpatel2218