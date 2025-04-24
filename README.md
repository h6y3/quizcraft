# QuizCraft

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python CLI application that processes educational PDFs to extract existing
questions and generate new ones using Claude, optimized for token efficiency.
Currently at **Milestone 2: Claude API Integration & Caching**.

## 📚 Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)
- [Testing](#testing)
- [Security](#security)
- [License](#license)

## Overview

QuizCraft helps educators, students, and learners work with educational content
more effectively. It automates the extraction and generation of high-quality
questions from PDF documents.

## Features

- **PDF Text Extraction**: Extract text from PDFs with OCR support
- **Question Identification**: Automatically identify existing questions
- **AI-Powered Generation**: Generate new questions based on document content
- **Interactive Quizzing**: Test knowledge with an interactive quiz mode
- **Token Optimization**: Efficiently use AI tokens to minimize costs
- **Caching System**: Store results to avoid redundant API calls

## Installation

### Development Setup

```bash
# Clone the repository
git clone https://github.com/hanyuan-nlp/quizcraft.git
cd quizcraft

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Install development dependencies
pip install flake8 mypy black pymarkdownlnt
```

> **Important:** This environment uses `python3` command instead of `python`.
> Always use `python3` when running commands.

**CRITICAL:** Always activate the virtual environment before running any commands.
The prompt should show `(venv)` when activated.

### API Credentials

This application uses the Anthropic Claude API for AI features.

1. Get an API key from [Anthropic](https://console.anthropic.com/)
2. Copy `.env.example` to `.env` and add your API key:

```bash
cp .env.example .env
# Edit .env with your text editor and add your API key
```

### Requirements

- **Python**: 3.8+
- **Tesseract OCR**: (Optional, for processing scanned documents)
  - macOS: `brew install tesseract`
  - Ubuntu/Debian: `apt-get install tesseract-ocr`
  - Windows: [Installer available here](https://github.com/UB-Mannheim/tesseract/wiki)
- **Dependencies**:

  ```text
  anthropic>=0.18.0
  PyMuPDF>=1.23.5
  pytesseract>=0.3.10
  Pillow>=10.0.0
  python-dotenv>=1.0.0
  flake8>=7.0.0
  black>=24.1.0
  mypy>=1.7.0
  pymarkdownlnt>=0.9.0
  ```

## Usage

### Extract Text from a PDF

```bash
# Basic extraction
python3 -m quizcraft extract path/to/file.pdf

# Extract with text segmentation and save to file
python3 -m quizcraft extract path/to/file.pdf --segment --output extracted_text.json

# Extract without OCR fallback
python3 -m quizcraft extract path/to/file.pdf --disable-ocr
```

### Generate Questions from a PDF

```bash
# Generate 5 questions with default difficulty
python3 -m quizcraft generate path/to/file.pdf --num-questions 5

# Generate questions with specified difficulty
python3 -m quizcraft generate path/to/file.pdf --difficulty easy|medium|hard

# Generate questions about specific topic
python3 -m quizcraft generate path/to/file.pdf --topic "photosynthesis"
```

### Interactive Quiz Mode

```bash
# Start an interactive quiz with questions from the PDF
python3 -m quizcraft quiz path/to/file.pdf

# Use existing questions extracted from the PDF
python3 -m quizcraft quiz path/to/file.pdf --use-existing

# Save quiz results to a file
python3 -m quizcraft quiz path/to/file.pdf --save-results results.json
```

## Examples

### Example: Extracting Text from a PDF

```bash
$ python3 -m quizcraft extract samples/sample.pdf --segment
✓ Processing samples/sample.pdf
✓ Text extraction complete
✓ Segmentation complete - identified 15 text segments
✓ Results saved to samples/sample_extracted.json
```

### Example: Generating Questions

```bash
$ python3 -m quizcraft generate samples/sample.pdf --num-questions 3
✓ Processing samples/sample.pdf
✓ Text extraction complete
✓ Generating questions...
✓ Created 3 questions about the main concepts
✓ Results saved to samples/sample_questions.json
```

## Project Structure

```python
quizcraft/
├── quizcraft/               # Main package
│   ├── __init__.py
│   ├── __main__.py          # Entry point for CLI
│   ├── main.py              # Application core
│   ├── config.py            # Configuration handling
│   ├── pdf/                 # PDF processing
│   │   ├── extractor.py     # PDF text extraction
│   │   ├── ocr.py           # OCR for scanned PDFs
│   │   └── service.py       # PDF service layer
│   ├── ai/                  # Claude API integration
│   │   ├── client.py        # API client
│   │   ├── credentials.py   # API key management
│   │   ├── prompts.py       # Prompt templates
│   │   ├── service.py       # AI service logic
│   │   └── tokens.py        # Token management
│   ├── questions/           # Question handling
│   ├── storage/             # Data persistence
│   │   └── cache.py         # Caching functionality
│   ├── utils/               # Utility functions
│   │   └── text.py          # Text processing utilities
│   └── ui/                  # User interfaces
│       └── cli.py           # Command-line interface
├── tests/                   # Unit tests
├── samples/                 # Sample data
└── scripts/                 # Utility scripts
```

## Development Roadmap

This project is being developed in milestones:

1. **Project Setup & PDF Processing** ✅
   - Basic PDF text extraction with PyMuPDF
   - OCR fallback with pytesseract for scanned documents
   - Text segmentation with content type classification
   - Command-line interface for extraction

2. **Claude API Integration & Caching** ✅
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please check out our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## Development

### Testing

Run the unit tests with:

```bash
python3 -m unittest discover tests
```

### Linting and Formatting

```bash
# Always activate the virtual environment first!
source venv/bin/activate

# Check for linting issues
python3 -m flake8 quizcraft/

# Run specific linting checks
python3 -m flake8 quizcraft/ --select=E501  # Check line length only
python3 -m flake8 quizcraft/ --select=F401  # Check unused imports only

# Fix line length issues with our script
python3 scripts/fix_line_length.py

# Auto-format code with black
python3 -m black --line-length 79 quizcraft/

# Run type checking
python3 -m mypy quizcraft/

# Lint markdown files
pymarkdownlnt scan *.md
```

For more detailed development guidelines, see [CLAUDE.md](CLAUDE.md).

## Security

- API keys and credentials are stored in `.env` files which are not committed
  to git
- Use `.env.example` as a template for required environment variables
- Never commit sensitive information to the repository
- Regular dependency updates to address security vulnerabilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE)
file for details.
