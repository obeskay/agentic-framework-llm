import base64
from pdf2image import convert_from_path
import pytesseract

class ImageProcessing:
    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

    @staticmethod
    def analyze_pdf(pdf_path):
        images = convert_from_path(pdf_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
