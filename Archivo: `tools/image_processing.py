import base64
from PIL import Image

class ImageProcessing:
    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

    @staticmethod
    def analyze_image(image_path):
        image = Image.open(image_path)
        # Procesar la imagen según sea necesario
        return image
