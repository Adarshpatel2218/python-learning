import cv2
import numpy as np
from insightface.app import FaceAnalysis

# Model load only once
face_app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]   # GPU ho to CUDAExecutionProvider
)

face_app.prepare(
    ctx_id=-1,
    det_size=(640, 640)
)


def get_embedding(image_bytes):

    # Convert bytes -> numpy
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # Decode image
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return None

    # Large image resize
    h, w = img.shape[:2]

    if max(h, w) > 1280:
        scale = 1280 / max(h, w)
        img = cv2.resize(
            img,
            (int(w * scale), int(h * scale)),
            interpolation=cv2.INTER_AREA
        )

    faces = face_app.get(img)

    if not faces:
        return None

    # Highest confidence face
    face = max(faces, key=lambda x: x.det_score)

    return face.embedding.astype(np.float32).tolist()