import base64
from PIL import Image
import io
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from typing import List, Dict, Any

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def pdf_to_images(pdf_path: str) -> List[Image.Image]:
    return convert_from_path(pdf_path)

def analyze_package_image(image_path: str) -> Dict[str, Any]:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detección de bordes
    edges = cv2.Canny(gray, 50, 150)
    
    # Detección de contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Análisis de forma
    shapes = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            shapes.append("rectangular")
        elif len(approx) > 8:
            shapes.append("circular")
    
    # OCR para texto en la imagen
    text = pytesseract.image_to_string(Image.fromarray(image))
    
    # Detección de color dominante
    pixels = np.float32(image.reshape(-1, 3))
    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant_color = palette[np.argmax(counts)]
    
    return {
        "shapes": shapes,
        "text": text,
        "dominant_color": dominant_color.tolist(),
        "damage_detected": "damage" in text.lower() or "damaged" in text.lower()
    }

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def resize_image(image_path: str, output_path: str, size: tuple) -> None:
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(output_path)

def apply_filter(image_path: str, output_path: str, filter_type: str) -> None:
    image = Image.open(image_path)
    if filter_type == "grayscale":
        image = image.convert("L")
    elif filter_type == "sepia":
        sepia_filter = (1.35, 0.68, 0.46, 0, 1.31, 0.66, 0.45, 0, 1.14, 0.58, 0.39, 0)
        image = image.convert("RGB", sepia_filter)
    image.save(output_path)
