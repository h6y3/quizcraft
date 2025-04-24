"""
PDF text extraction module using PyMuPDF with OCR fallback
"""

import fitz  # PyMuPDF

import PIL.Image
import io

from .ocr import OCRProcessor

from typing import Dict, List, Any


class PDFExtractor:
    """Extracts text from PDF files with OCR fallback if needed"""

    def __init__(self, use_ocr_fallback: bool = True):
        """
        Initialize the PDF extractor

        Args:
            use_ocr_fallback: Whether to use OCR when regular extraction fails
        """
        self.use_ocr_fallback = use_ocr_fallback
        self.ocr_processor = OCRProcessor() if use_ocr_fallback else None

    def extract_text(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract text from PDF document

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of text segments with metadata
        """
        segments = []

        try:
            doc = fitz.open(pdf_path)

            for page_num, page in enumerate(doc):
                # Extract text using PyMuPDF
                text = page.get_text()

                # If page has little or no text and OCR is enabled, we would u
                # se OCR here
                if not text.strip() and self.use_ocr_fallback:
                    text = self._ocr_fallback(page)

                if text.strip():
                    segments.append(
                        {
                            "page": page_num + 1,
                            "text": text,
                            "metadata": {
                                "has_images": len(page.get_images()) > 0,
                                "has_tables": self._has_tables(page),
                            },
                        }
                    )

            doc.close()

        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")

        return segments

    def _ocr_fallback(self, page: fitz.Page) -> str:
        """
        OCR fallback for scanned documents

        Args:
            page: PDF page to process

        Returns:
            Extracted text from OCR
        """
        if not self.ocr_processor:
            return ""

        try:
            # Convert page to an image
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")
            img = PIL.Image.open(io.BytesIO(img_data))

            # Process with OCR
            text = self.ocr_processor.process_image(img)
            return text

        except Exception as e:
            print(f"OCR fallback error: {str(e)}")
            return ""

    def _has_tables(self, page: fitz.Page) -> bool:
        """
        Detect if page contains tables (placeholder)

        Args:
            page: PDF page to check

        Returns:
            True if tables are detected, False otherwise
        """
        # This would use a more sophisticated method in a real implementation
        # For now return False as a placeholder
        return False


def segment_text(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Segment text into logical sections

    Args:
        segments: List of raw text segments from PDF

    Returns:
        List of processed text segments with content type classification
    """
    processed_segments = []

    for segment in segments:
        text = segment["text"]

        # Basic segmentation by paragraphs
        paragraphs = [p for p in text.split("\n\n") if p.strip()]

        for paragraph in paragraphs:
            # Simple classification of content type
            content_type = _classify_content(paragraph)

            processed_segments.append(
                {
                    "page": segment["page"],
                    "text": paragraph,
                    "type": content_type,
                    "metadata": segment["metadata"],
                }
            )

    return processed_segments


def _classify_content(text: str) -> str:
    """
    Classify content type based on text characteristics

    Args:
        text: Text to classify

    Returns:
        Content type classification
    """
    text = text.strip()

    if not text:
        return "empty"

    # Check for heading
    if len(text) < 100 and text.endswith(":") or text.isupper():
        return "heading"

    # Check for potential question
    if "?" in text:
        return "potential_question"

    # Check for bullet points
    if text.startswith("•") or text.startswith("-") or text.startswith("*"):
        return "bullet_point"

    # Default to paragraph
    return "paragraph"
