# Project Structure and Development Plan

## Project Reorganization

The project has been reorganized for better maintainability and clarity:

1. Added proper project documentation:
   - Updated README.md with clearer installation and usage instructions
   - Added more detailed project structure in CLAUDE.md
   - Added development environment setup instructions

2. Added development tools:
   - Created a Makefile for common development tasks
   - Added a .gitignore file
   - Enhanced package docstrings

3. Improved project organization:
   - Ensured consistent naming and structure
   - Added version tracking in __init__.py
   - Structured documentation for each milestone

## Project Organization

```
pdf-quiz-generator/
├── pdf_quiz_generator/       # Main package
│   ├── __init__.py
│   ├── main.py               # Entry point
│   ├── config.py             # Configuration
│   ├── pdf/                  # PDF processing modules
│   │   ├── extractor.py      # PDF text extraction
│   │   └── ocr.py            # OCR functionality
│   ├── ai/                   # Claude API integration (future)
│   ├── questions/            # Question handling (future)
│   ├── storage/              # Caching & persistence (future)
│   ├── utils/                # Utility functions
│   │   └── text.py           # Text processing utilities
│   └── ui/                   # User interface
│       └── cli.py            # Command-line interface
├── tests/                    # Unit tests
├── samples/                  # Sample data
├── requirements.txt          # Package dependencies
├── setup.py                  # Package setup script
└── README.md                 # Project documentation
```

## Development Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package in development mode
pip install -e .

# Running tests
python -m unittest discover tests

# Using the CLI
pdf-quiz-generator extract path/to/file.pdf
```

## Development Milestones

### Milestone 1: Project Setup & PDF Processing ✅
- ✅ Setup project structure and dependencies
- ✅ Implement PDF text extraction with PyMuPDF
- ✅ Add OCR fallback for scanned documents
- ✅ Basic text segmentation for context preservation

**Completed Features:**
- Project structure with modular organization
- PDF extraction using PyMuPDF
- OCR fallback with pytesseract
- Text segmentation with content type classification
- Basic CLI for PDF extraction
- Unit tests for core functionality

## Milestone 2: Claude API Integration & Caching
- Implement Claude API client with error handling
- Add token estimation functionality
- Create caching system with SQLite backend
- Implement MD5 hashing for prompt deduplication

## Milestone 3: Question Extraction & Validation
- Develop pattern matching for existing questions
- Implement question structure validation
- Create Claude-based fallback extraction
- Store extracted questions in database

## Milestone 4: Question Generation
- Implement question generation by concept
- Add difficulty level customization
- Create validation for generated questions
- Optimize token usage with targeted context

## Milestone 5: CLI Interface & Quiz Mode
- Build command-line interface with arguments
- Implement interactive quiz functionality
- Add reporting and statistics
- Integrate all components with proper error handling

# PDF Quiz Generator: Concise Specification

```markdown
# PDF Quiz Generator: Concise Specification

## System Overview
A Python CLI application that processes educational PDFs to extract existing questions and generate new ones using Claude, optimized for token efficiency and cost-effectiveness.

## Core Requirements
1. Process PDFs with focus on minimizing API costs
2. CLI interface with separation from core logic
3. Customizable question generation (difficulty, focus area, question types)
4. Efficient caching to reduce API calls
5. Extensible architecture for future expansion

## Architecture

```
pdf_quiz_generator/
├── main.py                 # Entry point
├── config.py               # Configuration
├── pdf/                    # PDF processing
├── ai/                     # Claude integration
├── questions/              # Question handling
├── storage/                # Caching & persistence
├── utils/                  # Utilities
└── ui/                     # CLI interface
```

## Key Implementation Strategies

### 1. PDF Processing
- Use PyMuPDF with OCR fallback (pytesseract) for scanned documents
- Intelligent text segmentation for context preservation
- Extract metadata to enhance question generation

### 2. Token Optimization
- Estimate Claude tokens accurately to stay within limits
- Intelligently trim context to focus on relevant content
- Prioritize sections likely to contain important concepts

### 3. Claude API Integration
- Implement caching with MD5 hashing of prompts
- Add retry logic with exponential backoff
- Validate and repair malformed JSON responses

### 4. Question Generation
- Extract questions using pattern matching first, then Claude API as fallback
- Validate question quality (structure, options, answer correctness)
- Generate questions by concept for better coverage

### 5. Caching System
- Size-limited cache with automatic pruning of older entries
- Persistent storage with SQLite for reuse across sessions
- Cache invalidation based on age

### 6. Error Handling
- Centralized error management with logging
- Graceful degradation when API issues occur
- User-friendly error messages

## CLI Commands

```bash
# Extract questions from PDF
python -m pdf_quiz_generator extract path/to/file.pdf --save

# Generate new questions
python -m pdf_quiz_generator generate path/to/file.pdf --difficulty medium --num-questions 5

# Run interactive quiz
python -m pdf_quiz_generator quiz path/to/file.pdf --use-existing
```

## Token Efficiency Techniques

1. **Pattern Matching First**: Use regex to extract questions where possible, minimizing API calls
2. **Targeted Context**: Extract only relevant sections for each concept
3. **Intelligent Caching**: Cache all API responses to prevent redundant calls
4. **Concept-Based Generation**: Generate questions by concept to avoid duplication
5. **Batch Processing**: Create multiple questions per API call

## Extensibility Points

1. **New UI Layers**: Core functionality separated from presentation
2. **Additional Question Types**: Structure supports new formats beyond multiple-choice
3. **Analytics**: Database schema supports tracking user performance
4. **Multiple AI Providers**: Client abstraction allows adding other AI services
5. **Content Libraries**: Persistence layer supports building reusable question banks

## Dependencies

```
anthropic>=0.18.0
PyMuPDF>=1.23.5
pytesseract>=0.3.10
Pillow>=10.0.0
```
```

This more concise version reduces the character count significantly while preserving the key architectural decisions and unique aspects of the design. I've removed most code examples and focused on the high-level strategies instead of implementation details.

Would you like me to make it even more concise, or would you prefer to keep certain sections in more detail?
