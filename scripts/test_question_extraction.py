#!/usr/bin/env python3
"""
Test script for question extraction functionality
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from quizcraft.pdf.extractor import PDFExtractor, segment_text
from quizcraft.questions.service import QuestionService


def main():
    """Test the question extraction functionality"""
    # Get sample PDF path
    sample_pdf = os.path.join(project_root, "samples", "python_questions.pdf")
    
    # Create temporary database path
    tmp_db_path = os.path.join(project_root, "samples", "test_questions.db")
    
    # Extract text from PDF
    print(f"Extracting text from {sample_pdf}...")
    extractor = PDFExtractor(use_ocr_fallback=True)
    segments = extractor.extract_text(sample_pdf)
    
    # Segment text
    print("Segmenting text...")
    processed_segments = segment_text(segments)
    
    # Initialize question service
    print("Extracting questions...")
    service = QuestionService(db_path=tmp_db_path, use_ai_fallback=True)
    
    # Extract questions
    questions, stats = service.extract_questions_from_segments(
        processed_segments, source_file=sample_pdf
    )
    
    # Print stats
    print("\nExtraction Statistics:")
    print(f"  Total segments: {stats['total_segments']}")
    print(f"  Potential question segments: {stats['potential_question_segments']}")
    print(f"  Pattern-extracted questions: {stats['pattern_extracted']}")
    print(f"  AI-extracted questions: {stats['ai_extracted']}")
    print(f"  Invalid questions: {stats['invalid_questions']}")
    print(f"  Stored questions: {stats['stored_questions']}")
    
    # Print extracted questions
    print(f"\nExtracted {len(questions)} questions:")
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. {question.question_text}")
        for key, option in question.options.items():
            print(f"   {key}: {option}")
        print(f"   Correct answer: {question.correct_answer}")
        if question.explanation:
            print(f"   Explanation: {question.explanation}")
    
    # Save questions to JSON
    output_path = os.path.join(project_root, "samples", "extracted_questions.json")
    question_set = {
        "questions": [q.to_dict() for q in questions],
        "stats": stats
    }
    
    with open(output_path, "w") as f:
        json.dump(question_set, f, indent=2)
    
    print(f"\nSaved extracted questions to {output_path}")
    print(f"Questions stored in database at {tmp_db_path}")
    
    # Test retrieving questions from storage
    print("\nTesting question retrieval from storage...")
    stored_questions = service.get_questions(source_file=sample_pdf)
    print(f"Retrieved {len(stored_questions)} questions from storage")
    
    # Get question stats
    print("\nQuestion statistics:")
    stats = service.get_question_stats(source_file=sample_pdf)
    print(f"  Total questions: {stats['total_questions']}")
    if stats.get("by_difficulty"):
        print("  By difficulty:")
        for difficulty, count in stats["by_difficulty"].items():
            print(f"    {difficulty}: {count}")
    if stats.get("by_category"):
        print("  By category:")
        for category, count in stats["by_category"].items():
            print(f"    {category}: {count}")


if __name__ == "__main__":
    main()