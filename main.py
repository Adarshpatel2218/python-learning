from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import cv2
import numpy as np
import pytesseract
import re

from face_service import get_embedding

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- HOME ----------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ---------------- USER ----------------

class User(BaseModel):
    name: str
    email: str


@app.post("/user")
async def create_user(user: User):
    return {
        "status": True,
        "data": user
    }


# ---------------- FACE REGISTER ----------------

@app.post("/register-face")
async def register_face(file: UploadFile = File(...)):

    image_bytes = await file.read()

    embedding = get_embedding(image_bytes)

    if embedding is None:
        return {
            "status": False,
            "message": "No face detected"
        }

    return {
        "status": True,
        "message": "Face Registered Successfully",
        "embedding_length": len(embedding),
        "embedding": embedding
    }


# ---------------- DOCUMENT OCR ----------------

@app.post("/extract-document")
async def extract_document(file: UploadFile = File(...)):

    image_bytes = await file.read()

    np_arr = np.frombuffer(image_bytes, np.uint8)

    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return {
            "status": False,
            "message": "Invalid Image"
        }

    try:

        text = pytesseract.image_to_string(img)

        aadhaar_match = re.findall(
            r"\b\d{4}\s?\d{4}\s?\d{4}\b",
            text
        )

        pan_match = re.findall(
            r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
            text
        )

        document_type = None
        document_number = None

        if aadhaar_match:
            document_type = "AADHAAR"
            document_number = aadhaar_match[0]

        elif pan_match:
            document_type = "PAN"
            document_number = pan_match[0]

        return {
            "status": True,
            "document_type": document_type,
            "document_number": document_number,
            "aadhaar_number": aadhaar_match[0] if aadhaar_match else None,
            "pan_number": pan_match[0] if pan_match else None,
            "text": text
        }

    except Exception as e:

        return {
            "status": False,
            "message": str(e)
        }