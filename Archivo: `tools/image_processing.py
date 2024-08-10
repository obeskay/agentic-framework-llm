import base64
from PIL import Image
import io

class ImageProcessing:
    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

    @staticmethod
    def analyze_image(image_path):
        image = Image.open(image_path)
        # Aquí se puede implementar el análisis de la imagen
        return image

    @staticmethod
    def save_image(image, save_path):
        image.save(save_path)

    @staticmethod
    def convert_to_grayscale(image_path):
        image = Image.open(image_path).convert("L")
        return image
