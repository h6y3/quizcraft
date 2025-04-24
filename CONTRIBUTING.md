# Contributing to QuizCraft

Thank you for considering contributing to QuizCraft! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers understand your report, reproduce the behavior, and find related reports.

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots if possible
- Include details about your configuration and environment

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to demonstrate the steps
- Describe the current behavior and explain which behavior you expected to see instead
- Explain why this enhancement would be useful to most users

### Pull Requests

- Fill in the required template
- Follow the Python style guides
- Write meaningful commit messages
- Include appropriate tests
- Update documentation as needed
- End all files with a newline

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Testing

- Write tests for new features and bug fixes
- Run tests before submitting a PR:
  ```bash
  python -m unittest discover tests
  ```

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

### Python Styleguide

- Follow PEP 8
- Use 4 spaces for indentation
- Use snake_case for variable names and function names
- Use CamelCase for class names
- Add docstrings to all functions and classes

## Documentation

- Update the README.md if needed
- Add docstrings to your code
- Comment your code when necessary

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

* `bug` - Issues for bugs in the codebase
* `documentation` - Issues for improving or updating documentation
* `enhancement` - Issues for new features or improvements
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `invalid` - Issues that are invalid or non-actionable
* `question` - Further information is requested

## Your First Contribution

Not sure where to begin contributing? Look for issues with the labels `good first issue` or `help wanted`.

## Getting Help

If you need help, you can ask questions by opening an issue with the label `question`.

Thank you for contributing to QuizCraft!