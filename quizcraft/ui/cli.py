"""
Command-line interface for QuizCraft
"""
import argparse
import sys
import json
from typing import List, Dict, Any, Optional

from ..pdf.extractor import PDFExtractor, segment_text


def create_parser() -> argparse.ArgumentParser:
    """
    Create command-line argument parser
    
    Returns:
        Configured argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="QuizCraft - Extract and generate quiz questions from PDFs"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract text from PDF")
    extract_parser.add_argument("pdf_path", help="Path to the PDF file")
    extract_parser.add_argument(
        "--disable-ocr", 
        action="store_true", 
        help="Disable OCR fallback for scanned documents"
    )
    extract_parser.add_argument(
        "--segment", 
        action="store_true", 
        help="Segment extracted text into logical sections"
    )
    extract_parser.add_argument(
        "--output", 
        help="Output file path (default: stdout)"
    )
    
    return parser


def handle_extract_command(args: argparse.Namespace) -> int:
    """
    Handle the extract command
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    try:
        # Initialize extractor
        extractor = PDFExtractor(use_ocr_fallback=not args.disable_ocr)
        
        # Extract text from PDF
        print(f"Extracting text from {args.pdf_path}...")
        segments = extractor.extract_text(args.pdf_path)
        
        # Segment text if requested
        if args.segment and segments:
            print("Segmenting text...")
            segments = segment_text(segments)
        
        # Output results
        if args.output:
            with open(args.output, "w") as f:
                json.dump(segments, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(segments, indent=2))
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


def main() -> int:
    """
    Main entry point for the CLI
    
    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 1
    
    if args.command == "extract":
        return handle_extract_command(args)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())