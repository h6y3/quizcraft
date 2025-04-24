"""
OCR functionality for scanned PDF documents
"""

import io

import PIL.Image
from typing import Union

try:
    import pytesseract

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class OCRProcessor:
    """Handles OCR processing for scanned documents"""

    def __init__(self):
        """Initialize the OCR processor"""
        if not OCR_AVAILABLE:
            print(
                "Warning: pytesseract not installed\
                    . OCR functionality will be limited."
            )

    def process_image(self, image: Union[str, bytes, PIL.Image.Image]) -> str:
        """
        Process an image using OCR

        Args:
            image: Path to image, bytes, or PIL Image object

        Returns:
            Extracted text from the image
        """
        if not OCR_AVAILABLE:
            return ""

        try:
            # Convert to PIL Image if needed
            if isinstance(image, str):
                img = PIL.Image.open(image)
            elif isinstance(image, bytes):
                img = PIL.Image.open(io.BytesIO(image))
            else:
                img = image

            # Apply preprocessing for better OCR results
            img = self._preprocess_image(img)

            # Perform OCR
            text = pytesseract.image_to_string(img)
            return text

        except Exception as e:
            print(f"OCR error: {str(e)}")
            return ""

    def _preprocess_image(self, image: PIL.Image.Image) -> PIL.Image.Image:
        """
        Preprocess image for better OCR results

        Args:
            image: PIL Image to preprocess

        Returns:
            Preprocessed PIL Image
        """
        # Convert to grayscale
        if image.mode != "L":
            image = image.convert("L")

        # In a real implementation, we might apply more preprocessing:
        # - Noise reduction
        # - Contrast enhancement
        # - Deskewing
        # etc.

        return image


def extract_text_from_page_image(page_image: PIL.Image.Image) -> str:
    """
    Extract text from a PDF page image

    Args:
        page_image: PIL Image of a PDF page

    Returns:
        Extracted text from the page
    """
    processor = OCRProcessor()
    return processor.process_image(page_image)
