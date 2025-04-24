# PDF Quiz Generator

A Python CLI application that processes educational PDFs to extract existing questions and generate new ones using Claude, optimized for token efficiency and cost-effectiveness.

## Overview

This tool helps educators and students work with educational content by:

1. Extracting text from PDF documents with OCR support for scanned content
2. Identifying and extracting existing questions
3. Generating new questions based on the content
4. Creating interactive quizzes

## Installation

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd pdf-quiz-generator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

### API Credentials

This application uses the Anthropic Claude API for AI features. You'll need to set up your credentials:

1. Get an API key from [Anthropic](https://console.anthropic.com/)
2. Copy `.env.example` to `.env` and add your API key:

```bash
cp .env.example .env
# Edit .env with your text editor and add your API key
```

### Requirements

- Python 3.8+
- Tesseract OCR (optional, for processing scanned documents)
- Dependencies listed in requirements.txt

## Usage

### Extract text from a PDF

```bash
# Basic extraction
pdf-quiz-generator extract path/to/file.pdf

# Extract with text segmentation and save to file
pdf-quiz-generator extract path/to/file.pdf --segment --output extracted_text.json

# Extract without OCR fallback
pdf-quiz-generator extract path/to/file.pdf --disable-ocr
```

## Project Structure

```
pdf-quiz-generator/
├── pdf_quiz_generator/       # Main package
│   ├── pdf/                  # PDF processing
│   ├── ai/                   # Claude integration
│   ├── questions/            # Question handling (future)
│   ├── storage/              # Caching & persistence
│   ├── utils/                # Utilities
│   └── ui/                   # CLI interface
├── tests/                    # Unit tests
└── samples/                  # Sample data
```

## Development Roadmap

This project is being developed in milestones:

1. **Project Setup & PDF Processing** ✅
   - Basic PDF text extraction with PyMuPDF
   - OCR fallback with pytesseract for scanned documents
   - Text segmentation with content type classification
   - Command-line interface for extraction

2. **Claude API Integration & Caching** (Current)
   - API client with error handling
   - Token estimation
   - Caching system with SQLite
   - Secure credential management

3. **Question Extraction & Validation** (Planned)
   - Pattern matching
   - Question validation
   - Claude-based extraction

4. **Question Generation** (Planned)
   - Generation by concept
   - Difficulty customization
   - Question validation

5. **CLI Interface & Quiz Mode** (Planned)
   - Interactive quiz functionality
   - Reporting and statistics

## Testing

Run the unit tests with:

```bash
python -m unittest discover tests
```

## Security

- API keys and credentials are stored in `.env` files which are not committed to git
- Use `.env.example` as a template for required environment variables
- Never commit sensitive information to the repository