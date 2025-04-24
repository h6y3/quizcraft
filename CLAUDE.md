# QuizCraft Development Guide

## Project Overview

QuizCraft is a Python CLI application that processes educational PDFs to extract
existing questions and generate new ones using Claude AI. The application focuses
on token efficiency and cost-effectiveness.

### Current Status

We are currently at **Milestone 2: Claude API Integration & Caching**. The PDF
extraction functionality is complete, and we're working on integrating the Claude
API with proper error handling and efficient caching mechanisms.

### Core Features

1. PDF processing with text extraction and OCR
2. Intelligent question extraction and generation via Claude API
3. Token optimization for cost efficiency
4. Local caching system for reduced API calls
5. Customizable question generation by difficulty and topic
6. Command-line interface with interactive quiz mode

## Development Workflow

### Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package in development mode
pip install -e .

# Running tests
python -m unittest discover tests

# Using the CLI
quizcraft extract path/to/file.pdf
```

### Development Process

1. Create a branch for each feature or bug fix
2. Write tests before implementation where possible
3. Run tests and linters locally before submitting PRs
4. Document all public functions, classes, and modules
5. Update this document as needed when architecture changes

## Project Structure

```text
quizcraft/
├── quizcraft/       # Main package
│   ├── __init__.py
│   ├── main.py               # Entry point
│   ├── config.py             # Configuration
│   ├── pdf/                  # PDF processing modules
│   │   ├── extractor.py      # PDF text extraction
│   │   └── ocr.py            # OCR functionality
│   ├── ai/                   # Claude API integration
│   │   ├── client.py         # API client
│   │   ├── service.py        # AI service logic
│   │   ├── credentials.py    # API key management
│   │   ├── prompts.py        # Prompt templates
│   │   └── tokens.py         # Token counting
│   ├── questions/            # Question handling
│   ├── storage/              # Caching & persistence
│   │   └── cache.py          # Cache implementation
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

## Coding Standards and Principles

Following principles from "Code Complete" and our experience with this project,
we've established these guidelines.

### Code Quality

#### Documentation and Comments

- Include docstrings on all public classes and methods
- Document parameters, return values, and raised exceptions
- Keep comments focused on explaining "why", not "what"
- Use type hints consistently

#### Error Handling

- Use appropriate exception handling with specific exception types
- Validate input parameters and fail early
- Include helpful error messages that guide the user
- Log errors with sufficient context for debugging

#### Testing

- Write unit tests for all service classes
- Mock external dependencies in tests
- Test both success and failure paths
- Validate edge cases and boundary conditions
- Mirror the application's package structure in the test directory

#### Validation and Linting

- Use a markdown linter for documentation files (e.g., pymarkdown)
- Run type checking with mypy
- Format code with black
- Use flake8 for code quality enforcement
- Ensure all files end with a single newline

##### Markdown Style Guide

We use the `pymarkdown` linter to enforce markdown styling rules. Run:

```bash
pymarkdown scan /path/to/file.md
```

Common markdown rules to follow:

1. **Line Length**: Keep lines under 80 characters
2. **Trailing Spaces**: Never leave trailing spaces at end of lines
3. **Code Blocks**:
   - Always specify a language for fenced code blocks
   - Always surround code blocks with blank lines
   - Example: \```python instead of just \```
4. **Headers**:
   - Always surround headers with blank lines (before and after)
   - Use a single H1 (#) at the top of the document
   - No duplicate headers with identical text
   - Use proper header hierarchy (don't skip levels)
5. **Emphasis**: Don't use emphasis (bold, italic) instead of proper headers
6. **Lists**: Maintain consistent indentation in nested lists
7. **End of File**: Ensure files end with exactly one newline (not zero, not multiple)
8. **Line Breaks**: Use blank lines to separate paragraphs, not trailing spaces
9. **HTML**: Avoid raw HTML in markdown files when possible

### Architecture and Design

#### Service-Oriented Architecture

- Use service classes to encapsulate business logic
- Create clear separation between data access, business logic, and presentation
- Define explicit interfaces between system components

#### Separation of Concerns

- Each module should have a single, well-defined responsibility
- PDF handling, AI integration, and UI should be isolated from each other
- Configuration should be separate from business logic

#### Information Hiding

- Implementation details should be hidden behind well-defined interfaces
- Classes should expose only what is necessary for their use
- Internal state should be protected from direct external manipulation

### Code Organization

#### Modular Structure

- Group related functionality into cohesive modules
- Maintain clean package hierarchy with logical organization
- Use __init__.py files to define public interfaces for each module

#### Class and Function Design

- Methods should have a single responsibility
- Keep method length under 25 lines where reasonable
- Functions should operate at a single level of abstraction
- Classes should implement a single, clear abstraction

#### Dependency Management

- Use dependency injection to allow for testing and flexibility
- Minimize dependencies between modules
- Explicitly import only what is needed

#### DRY (Don't Repeat Yourself)

- Extract common logic into shared functions or base classes
- Use inheritance or composition to reuse code appropriately
- Create utilities for frequently used operations

### Performance and Efficiency

#### Token Optimization

- Intelligently reduce prompt size to stay within limits
- Cache API responses to avoid redundant calls
- Implement token counting for better cost control

#### Resource Management

- Use context managers for resource cleanup
- Properly close files, database connections, and other resources
- Implement timeouts for external API calls

## Development Roadmap

### Milestone 1: Project Setup & PDF Processing ✅

- ✅ Setup project structure and dependencies
- ✅ Implement PDF text extraction with PyMuPDF
- ✅ Add OCR fallback for scanned documents
- ✅ Basic text segmentation for context preservation

### Milestone 2: Claude API Integration & Caching 🔄

- Implement Claude API client with error handling
- Add token estimation functionality
- Create caching system with SQLite backend
- Implement MD5 hashing for prompt deduplication

### Milestone 3: Question Extraction & Validation

- Develop pattern matching for existing questions
- Implement question structure validation
- Create Claude-based fallback extraction
- Store extracted questions in database

### Milestone 4: Question Generation

- Implement question generation by concept
- Add difficulty level customization
- Create validation for generated questions
- Optimize token usage with targeted context

### Milestone 5: CLI Interface & Quiz Mode

- Build command-line interface with arguments
- Implement interactive quiz functionality
- Add reporting and statistics
- Integrate all components with proper error handling

## Implementation Strategies

### PDF Processing

- Use PyMuPDF with OCR fallback (pytesseract) for scanned documents
- Intelligent text segmentation for context preservation
- Extract metadata to enhance question generation

### Claude API Integration

- Implement caching with MD5 hashing of prompts
- Add retry logic with exponential backoff
- Validate and repair malformed JSON responses

### Question Generation

- Extract questions using pattern matching first, then Claude API as fallback
- Validate question quality (structure, options, answer correctness)
- Generate questions by concept for better coverage

### Caching System

- Size-limited cache with automatic pruning of older entries
- Persistent storage with SQLite for reuse across sessions
- Cache invalidation based on age

### CLI Commands

```bash
# Extract questions from PDF
python -m quizcraft extract path/to/file.pdf --save

# Generate new questions
python -m quizcraft generate path/to/file.pdf --difficulty medium \
  --num-questions 5

# Run interactive quiz
python -m quizcraft quiz path/to/file.pdf --use-existing
```

## Dependencies

```text
anthropic>=0.18.0
PyMuPDF>=1.23.5
pytesseract>=0.3.10
Pillow>=10.0.0
```
