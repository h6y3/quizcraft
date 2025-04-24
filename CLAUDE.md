# QuizCraft Development Guidelines

## Project Organization

The project has been organized for better maintainability and clarity:

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

## Coding Standards and Principles

Following principles from "Code Complete" and our experience with this project, we've established these guidelines:

### Architecture and Design

1. **Service-Oriented Architecture**
   - Use service classes to encapsulate business logic
   - Create clear separation between data access, business logic, and presentation
   - Define explicit interfaces between system components

2. **Separation of Concerns**
   - Each module should have a single, well-defined responsibility
   - PDF handling, AI integration, and UI should be isolated from each other
   - Configuration should be separate from business logic

3. **Information Hiding**
   - Implementation details should be hidden behind well-defined interfaces
   - Classes should expose only what is necessary for their use
   - Internal state should be protected from direct external manipulation

### Code Organization

1. **Modular Structure**
   - Group related functionality into cohesive modules
   - Maintain clean package hierarchy with logical organization
   - Use __init__.py files to define public interfaces for each module

2. **Class and Function Design**
   - Methods should have a single responsibility
   - Keep method length under 25 lines where reasonable
   - Functions should operate at a single level of abstraction
   - Classes should implement a single, clear abstraction

3. **Dependency Management**
   - Use dependency injection to allow for testing and flexibility
   - Minimize dependencies between modules
   - Explicitly import only what is needed

### Code Quality

1. **Error Handling**
   - Use appropriate exception handling with specific exception types
   - Validate input parameters and fail early
   - Include helpful error messages that guide the user
   - Log errors with sufficient context for debugging

2. **Documentation**
   - Include docstrings on all public classes and methods
   - Document parameters, return values, and raised exceptions
   - Keep comments focused on explaining "why", not "what"
   - Use type hints consistently

3. **DRY (Don't Repeat Yourself)**
   - Extract common logic into shared functions or base classes
   - Use inheritance or composition to reuse code appropriately
   - Create utilities for frequently used operations

### Performance and Efficiency

1. **Token Optimization**
   - Intelligently reduce prompt size to stay within limits
   - Cache API responses to avoid redundant calls
   - Implement token counting for better cost control

2. **Resource Management**
   - Use context managers for resource cleanup
   - Properly close files, database connections, and other resources
   - Implement timeouts for external API calls

### Testing

1. **Test Coverage**
   - Write unit tests for all service classes
   - Mock external dependencies in tests
   - Test both success and failure paths
   - Validate edge cases and boundary conditions

2. **Test Organization**
   - Mirror the application's package structure in the test directory
   - Use consistent naming conventions for test methods
   - Separate unit tests from integration tests

### Continuous Improvement

1. **Code Reviews**
   - Conduct regular code reviews to maintain quality
   - Verify adherence to these standards
   - Look for opportunities to refactor and improve

2. **Refactoring**
   - Regularly refactor to improve code structure
   - Apply design patterns where appropriate
   - Eliminate code smells when identified

## Project Organization

```
quizcraft/
├── quizcraft/       # Main package
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
quizcraft extract path/to/file.pdf
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

# QuizCraft: Concise Specification

```markdown
# QuizCraft: Concise Specification

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
quizcraft/
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
python -m quizcraft extract path/to/file.pdf --save

# Generate new questions
python -m quizcraft generate path/to/file.pdf --difficulty medium --num-questions 5

# Run interactive quiz
python -m quizcraft quiz path/to/file.pdf --use-existing
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
