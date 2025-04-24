# PDF Quiz Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python CLI application that processes educational PDFs to extract existing questions and generate new ones using Claude, optimized for token efficiency and cost-effectiveness.

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
- [Support](#support)

## Overview

PDF Quiz Generator helps educators, students, and learners work with educational content more effectively. It solves the problem of manually creating quizzes from educational materials by automating the extraction and generation of high-quality questions from PDF documents.

## Features

- **PDF Text Extraction**: Extract text from PDFs with OCR support for scanned documents
- **Question Identification**: Automatically identify and extract existing questions
- **AI-Powered Generation**: Generate new questions based on document content
- **Interactive Quizzing**: Test knowledge with an interactive quiz mode
- **Token Optimization**: Efficiently use AI tokens to minimize costs
- **Caching System**: Store results to avoid redundant API calls

## Installation

### Option 1: PyPI Installation (Coming Soon)

```bash
pip install pdf-quiz-generator
```

### Option 2: Development Setup

```bash
# Clone the repository
git clone https://github.com/hanyuan-nlp/pdf-quiz-generator.git
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

- **Python**: 3.8+
- **Tesseract OCR**: (Optional, for processing scanned documents)
  - macOS: `brew install tesseract`
  - Ubuntu/Debian: `apt-get install tesseract-ocr`
  - Windows: [Installer available here](https://github.com/UB-Mannheim/tesseract/wiki)
- **Dependencies**: Listed in requirements.txt

## Usage

### Extract Text from a PDF

```bash
# Basic extraction
pdf-quiz-generator extract path/to/file.pdf

# Extract with text segmentation and save to file
pdf-quiz-generator extract path/to/file.pdf --segment --output extracted_text.json

# Extract without OCR fallback
pdf-quiz-generator extract path/to/file.pdf --disable-ocr
```

### Generate Questions from a PDF

```bash
# Generate 5 questions with default difficulty
pdf-quiz-generator generate path/to/file.pdf --num-questions 5

# Generate questions with specified difficulty
pdf-quiz-generator generate path/to/file.pdf --difficulty easy|medium|hard

# Generate questions about specific topic
pdf-quiz-generator generate path/to/file.pdf --topic "photosynthesis"
```

### Interactive Quiz Mode

```bash
# Start an interactive quiz with questions from the PDF
pdf-quiz-generator quiz path/to/file.pdf

# Use existing questions extracted from the PDF
pdf-quiz-generator quiz path/to/file.pdf --use-existing

# Save quiz results to a file
pdf-quiz-generator quiz path/to/file.pdf --save-results results.json
```

## Examples

### Example: Extracting Text from a PDF

```bash
$ pdf-quiz-generator extract samples/sample.pdf --segment
✓ Processing samples/sample.pdf
✓ Text extraction complete
✓ Segmentation complete - identified 15 text segments
✓ Results saved to samples/sample_extracted.json
```

### Example: Generating Questions

```bash
$ pdf-quiz-generator generate samples/sample.pdf --num-questions 3
✓ Processing samples/sample.pdf
✓ Text extraction complete
✓ Generating questions...
✓ Created 3 questions about the main concepts
✓ Results saved to samples/sample_questions.json
```

## Project Structure

```
pdf-quiz-generator/
├── pdf_quiz_generator/       # Main package
│   ├── pdf/                  # PDF text extraction and processing
│   │   ├── extractor.py      # Core PDF text extraction
│   │   └── ocr.py            # OCR functionality for scanned PDFs
│   ├── ai/                   # Claude API integration
│   │   ├── client.py         # API client with error handling
│   │   └── tokens.py         # Token estimation and management
│   ├── questions/            # Question processing
│   │   ├── extractor.py      # Existing question extraction
│   │   └── generator.py      # New question generation
│   ├── storage/              # Data persistence
│   │   └── cache.py          # Caching functionality
│   ├── utils/                # Utility functions
│   │   └── text.py           # Text processing utilities
│   └── ui/                   # User interfaces
│       └── cli.py            # Command-line interface
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please check out our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## Testing

Run the unit tests with:

```bash
python -m unittest discover tests
```

For more comprehensive testing:

```bash
# Run tests with coverage report
pytest --cov=pdf_quiz_generator tests/

# Run only fast tests
pytest -k "not slow" tests/
```

## Security

- API keys and credentials are stored in `.env` files which are not committed to git
- Use `.env.example` as a template for required environment variables
- Never commit sensitive information to the repository
- Regular dependency updates to address security vulnerabilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Please report bugs via the GitHub issue tracker
- **Questions**: Open a discussion in the GitHub repository or contact the maintainer
- **Email**: [your-email@example.com](mailto:your-email@example.com) (for private inquiries)
- **Twitter**: [@your_handle](https://twitter.com/your_handle)

---

Created by Han Yuan ([@hanyuan-nlp](https://github.com/hanyuan-nlp))