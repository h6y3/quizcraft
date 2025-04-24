# QuizCraft Development Guide

## Project Overview

QuizCraft is a Python CLI application that processes educational PDFs to extract
existing questions and generate new ones using Claude AI. The application focuses
on token efficiency and cost-effectiveness.

### Current Status

We have completed **Milestone 2: Claude API Integration & Caching**. The PDF
extraction functionality is complete, and the Claude API integration with error
handling and efficient caching mechanisms has been implemented. We are now
preparing to start Milestone 3.

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

# Install development dependencies
pip install flake8 mypy black

# Running tests
python3 -m unittest discover tests

# Running linters
python3 -m flake8 quizcraft/
python3 -m mypy quizcraft/
python3 -m black quizcraft/

# Using the CLI
python3 -m quizcraft extract path/to/file.pdf
```

> **Important:** This environment uses `python3` command instead of `python`.
> Always use `python3` when running commands.

#### Virtual Environment Activation

**CRITICAL:** Always activate the virtual environment before running any commands:

```bash
source venv/bin/activate
```

Running commands without activating the virtual environment will:
- Use system-installed packages instead of project dependencies
- Cause "module not found" errors
- Lead to inconsistent behavior

You must activate the virtual environment in **each new terminal session**.
The prompt should show `(venv)` when activated.

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

### Common Coding Pitfalls to Avoid

These issues have caused significant debugging time in our project:

1. **Line Length Violations**: Keep all lines under 79 characters to comply
   with E501
   - Break long strings across multiple lines using parentheses
   - Use line continuation for long function calls/parameters
   - For docstrings, use multi-line format with proper indentation

2. **Import Management**:
   - Only import what you use (avoid F401 unused import errors)
   - Use explicit imports instead of wildcard imports (`from module import *`)
   - Group imports in standard order: stdlib, third-party, local

3. **Indentation Issues**:
   - Use consistent 4-space indentation
   - Be careful with line continuation indentation (typically add 4 more spaces)
   - When breaking function calls/parameters, align properly

4. **String Formatting**:
   - Prefer f-strings for formatting when possible
   - For multi-line strings, use consistent indentation
   - Watch string concatenation across lines carefully

5. **Path Handling**:
   - Always use absolute paths for file operations
   - Use `os.path.join()` to ensure cross-platform compatibility
   - Validate paths exist before operations

6. **Error Handling**:
   - Never use bare `except:` clauses
   - Catch specific exceptions and provide meaningful error messages
   - Use appropriate exception types when raising errors

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

- Use a markdown linter for documentation files (pymarkdownlnt)
- Run type checking with mypy
- Format code with black
- Use flake8 for code quality enforcement (see Common Flake8 Rules below)
- Ensure all files end with a single newline

##### Common Flake8 Rules

- E501: Line too long (keep under 79 characters)
- E302: Expected 2 blank lines between top-level functions/classes
- E301: Expected 1 blank line between methods in a class
- F401: Imported module not used
- W293: Blank line contains whitespace
- E122/E128: Indentation issues in continuation lines
- E226: Missing whitespace around arithmetic operator
- W504: Line break after binary operator
- W391: Blank line at end of file

##### Markdown Style Guide

We use the `pymarkdownlnt` linter to enforce markdown styling rules. Run:

```bash
# Install the markdown linter
pip install pymarkdownlnt

# Check markdown files for issues
pymarkdownlnt scan *.md

# Fix automatically fixable issues
pymarkdownlnt fix *.md
```

For more specific rule checking, you can enable or disable specific rules:

```bash
# Check only specific rules
pymarkdownlnt --enable-rules MD013,MD041 scan *.md

# Disable specific rules for a scan
pymarkdownlnt --disable-rules MD013 scan *.md
```

Common markdown linting rules we enforce:

1. **MD013**: Line length - Keep lines under 80 characters
2. **MD009**: Trailing spaces - Never leave trailing spaces at end of lines
3. **MD031/MD040**: Code blocks
   - Always specify a language for fenced code blocks
   - Always surround code blocks with blank lines
   - Example: \```python instead of just \```
4. **MD022/MD024/MD025/MD041**: Headers
   - Always surround headers with blank lines (before and after)
   - Use a single H1 (#) at the top of the document
   - No duplicate headers with identical text
   - Use proper header hierarchy (don't skip levels)
5. **MD036**: Emphasis - Don't use emphasis (bold, italic) instead of proper headers
6. **MD007**: Lists - Maintain consistent indentation in nested lists
7. **MD047**: End of File - Ensure files end with exactly one newline
8. **MD012**: Line Breaks - Use blank lines to separate paragraphs, not
   trailing spaces
9. **MD033**: HTML - Avoid raw HTML in markdown files when possible

You can create a `.pymarkdown` configuration file in the project root to
customize rule settings if needed.

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

### Milestone 2: Claude API Integration & Caching ✅

- ✅ Implement Claude API client with error handling
- ✅ Add token estimation functionality
- ✅ Create caching system with SQLite backend
- ✅ Implement MD5 hashing for prompt deduplication
- ✅ Fix docstring formatting and indentation
- ✅ Auto-format code with black

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
python3 -m quizcraft extract path/to/file.pdf --save

# Generate new questions
python3 -m quizcraft generate path/to/file.pdf --difficulty medium \
  --num-questions 5

# Run interactive quiz
python3 -m quizcraft quiz path/to/file.pdf --use-existing
```

### Linting and Automated Fixes

```bash
# Always activate the virtual environment first!
source venv/bin/activate

# Check for linting issues
python -m flake8 quizcraft/

# Run specific linting checks
python -m flake8 quizcraft/ --select=E501  # Check line length only
python -m flake8 quizcraft/ --select=F401  # Check unused imports only

# Fix line length issues with our script
python scripts/fix_line_length.py

# Auto-format code with black
python -m black --line-length 79 quizcraft/

# Run type checking
python -m mypy quizcraft/
```

Our `fix_line_length.py` script combines Black's formatting with custom fixes
for line length issues. Run it before committing to ensure code complies with
the 79-character limit.

## Dependencies

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
