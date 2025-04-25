"""
Command-line interface for QuizCraft
"""

import argparse

import sys
import json

import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_parser():
    """
    Create command-line argument parser

    Returns:
        Configured argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="QuizCraft - Extract and generate quiz questions from PDFs"
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Command to execute"
    )

    # Extract command
    extract_parser = subparsers.add_parser(
        "extract", help="Extract text from PDF"
    )
    extract_parser.add_argument("pdf_path", help="Path to the PDF file")
    extract_parser.add_argument(
        "--disable-ocr",
        action="store_true",
        help="Disable OCR fallback for scanned documents",
    )
    extract_parser.add_argument(
        "--segment",
        action="store_true",
        help="Segment extracted text into logical sections",
    )
    extract_parser.add_argument(
        "--output", help="Output file path (default: stdout)"
    )

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate questions from PDF"
    )
    generate_parser.add_argument("pdf_path", help="Path to the PDF file")
    generate_parser.add_argument(
        "--num-questions",
        "-n",
        type=int,
        default=5,
        help="Number of questions to generate",
    )
    generate_parser.add_argument(
        "--difficulty",
        "-d",
        choices=["easy", "medium", "hard"],
        default="medium",
        help="Difficulty level of the questions",
    )
    generate_parser.add_argument(
        "--topic", "-t", help="Focus on a specific topic (optional)"
    )
    generate_parser.add_argument(
        "--disable-ocr",
        action="store_true",
        help="Disable OCR fallback for scanned documents",
    )
    generate_parser.add_argument(
        "--output", "-o", help="Output file path (default: stdout)"
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
        # Initialize the PDF service
        from ..pdf import PDFService

        pdf_service = PDFService(use_ocr=not args.disable_ocr)

        # Validate the PDF path
        if not os.path.exists(args.pdf_path):
            logger.error(f"PDF file not found: {args.pdf_path}")
            print(
                f"Error: PDF file not found: {args.pdf_path}", file=sys.stderr
            )
            return 1

        if not os.path.isfile(args.pdf_path):
            logger.error(f"Not a file: {args.pdf_path}")
            print(f"Error: Not a file: {args.pdf_path}", file=sys.stderr)
            return 1

        # Extract text from PDF
        try:
            result = pdf_service.extract_text(
                args.pdf_path, segment=args.segment
            )
        except ValueError as e:
            logger.error(f"Extraction error: {str(e)}")
            print(f"Extraction error: {str(e)}", file=sys.stderr)
            return 1

        if not result["success"]:
            error_reason = result.get("reason", "Unknown reason")
            logger.error(f"Failed to extract text: {error_reason}")
            print(
                f"Error: Failed to extract text from {args.pdf_path}: "
                f"{error_reason}",
                file=sys.stderr,
            )
            return 1

        # Output results
        if args.output:
            try:
                output_dir = os.path.dirname(args.output)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"Results saved to {args.output}")
            except IOError as e:
                logger.error(f"Failed to write output file: {str(e)}")
                print(
                    f"Error: Failed to write output file: {str(e)}",
                    file=sys.stderr,
                )
                return 1
        else:
            # Print a summary instead of the full JSON for better terminal out
            # put
            if args.segment:
                print(f"Segmented into {len(result['segments'])} segments")
                for i, seg in enumerate(
                    result["segments"][:3]
                ):  # Show the first 3 segments
                    preview = seg["text"][:100].replace("\n", " ")
                    print(
                        f"Segment {i + 1} ({seg.get('type', 'unknown')}): "
                        f"{preview}..."
                    )
                if len(result["segments"]) > 3:
                    print(
                        f"... and {len(result['segments']) - 3} more segments"
                    )
            else:
                text_preview = result["text"][:200].replace("\n", " ")
                print(
                    f"Extracted text ({len(
                        result['text'])} characters): {text_preview}..."
                )

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        print(f"Error: File not found: {str(e)}", file=sys.stderr)
        return 1
    except PermissionError as e:
        logger.error(f"Permission denied: {str(e)}")
        print(f"Error: Permission denied: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


def handle_generate_command(args: argparse.Namespace) -> int:
    """
    Handle the generate command

    Args:
        args: Command-line arguments

    Returns:
        Exit code
    """
    try:
        # Initialize services
        from ..pdf import PDFService
        from ..ai import AIService

        pdf_service = PDFService(use_ocr=not args.disable_ocr)
        ai_service = AIService()

        # Get the appropriate context
        if args.topic:
            # Extract topic-specific content
            context_result = pdf_service.extract_topic_context(
                args.pdf_path, args.topic
            )
            if not context_result["success"]:
                print(
                    f"Error: Failed to extract text from {args.pdf_path}",
                    file=sys.stderr,
                )
                return 1
            context = context_result["text"]
        else:
            # Extract the full text
            extraction_result = pdf_service.extract_text(args.pdf_path)
            if not extraction_result["success"]:
                print(
                    f"Error: Failed to extract text from {args.pdf_path}",
                    file=sys.stderr,
                )
                return 1
            context = extraction_result["text"]

        # Generate questions
        print(
            f"Generating {args.num_questions} questions at "
            f"{args.difficulty} difficulty..."
        )
        generation_result = ai_service.generate_questions(
            context=context,
            num_questions=args.num_questions,
            difficulty=args.difficulty,
            cache_key_prefix=args.pdf_path,
        )

        # Output the results
        questions = generation_result["questions"]
        if args.output:
            with open(args.output, "w") as f:
                json.dump(questions, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(questions, indent=2))

        # Display summary
        print(f"Generated {len(questions['questions'])} questions")

        # Show token usage
        token_usage = generation_result["token_usage"]
        print(
            f"Token usage: {token_usage['input_tokens']} input, "
            f"{token_usage['output_tokens']} output"
        )

        # Mention if from cache
        if generation_result.get("from_cache", False):
            print("Note: Results retrieved from cache")

        return 0

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


def main():
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
    elif args.command == "generate":
        return handle_generate_command(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
