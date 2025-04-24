"""PDF processing service with topic extraction and segmentation."""

import logging

from .extractor import PDFExtractor, segment_text

from typing import Dict, Any

logger = logging.getLogger(__name__)


class PDFService:
    """Service layer for PDF processing operations."""

    def __init__(self, use_ocr: bool = True):
        """
        Initialize the PDF service.

        Args:
            use_ocr: Whether to use OCR for text extraction
        """
        self.extractor = PDFExtractor(use_ocr_fallback=use_ocr)

    def extract_text(
        self, pdf_path: str, segment: bool = False
    ) -> Dict[str, Any]:
        """
        Extract text from a PDF file with optional segmentation.

        Args:
            pdf_path: Path to the PDF file
            segment: Whether to segment the extracted text

        Returns:
            Dictionary with extracted text and metadata
        """
        logger.info(f"Extracting text from {pdf_path}")

        # Extract raw text
        raw_segments = self.extractor.extract_text(pdf_path)

        if not raw_segments:
            logger.warning(f"No text extracted from {pdf_path}")
            return {
                "pdf_path": pdf_path,
                "text": "",
                "segments": [],
                "success": False,
            }

        # Process according to requested format
        if segment:
            processed_segments = segment_text(raw_segments)
            logger.info(f"Segmented into {len(processed_segments)} segments")
            return {
                "pdf_path": pdf_path,
                "segments": processed_segments,
                "success": True,
            }
        else:
            # Combine all segments into one text
            full_text = " ".join([seg.get("text", "") for seg in raw_segments])
            logger.info(f"Extracted {len(full_text)} characters")
            return {
                "pdf_path": pdf_path,
                "text": full_text,
                "raw_segments": raw_segments,
                "success": True,
            }

    def extract_topic_context(
        self, pdf_path: str, topic: str
    ) -> Dict[str, Any]:
        """
        Extract text related to a specific topic from a PDF.

        Args:
            pdf_path: Path to the PDF file
            topic: Topic to extract content about

        Returns:
            Dictionary with topic-specific content and metadata
        """
        # Extract and segment text
        extraction_result = self.extract_text(pdf_path, segment=True)

        if not extraction_result["success"]:
            return {
                "pdf_path": pdf_path,
                "topic": topic,
                "text": "",
                "segments": [],
                "success": False,
                "reason": "Failed to extract text from PDF",
            }

        # Find segments that mention the topic
        segments = extraction_result["segments"]
        relevant_segments = []

        for segment in segments:
            if topic.lower() in segment.get("text", "").lower():
                relevant_segments.append(segment)

        # Prepare result
        if relevant_segments:
            logger.info(
                f"Found {len(relevant_segments)} segments mentioning '{topic}'"
            )
            combined_text = "\n\n".join(
                [seg.get("text", "") for seg in relevant_segments]
            )
            return {
                "pdf_path": pdf_path,
                "topic": topic,
                "text": combined_text,
                "segments": relevant_segments,
                "success": True,
            }
        else:
            logger.warning(
                f"No segments found containing '{topic}'. Using full text."
            )
            # Fall back to full text
            full_text = " ".join([seg.get("text", "") for seg in segments])
            return {
                "pdf_path": pdf_path,
                "topic": topic,
                "text": full_text,
                "segments": segments,
                "success": True,
                "topic_found": False,
            }
