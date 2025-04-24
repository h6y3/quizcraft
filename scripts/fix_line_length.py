#!/usr/bin/env python3
"""Script to fix line length issues in the codebase targeting specific files."""

import os
import re
import subprocess
import sys
from pathlib import Path


def check_line_length_issues(file_path):
    """
    Check if a file has line length issues using flake8.
    
    Args:
        file_path: Path to the Python file to check
    
    Returns:
        list: List of tuples with (line_number, line) for lines with issues
    """
    try:
        result = subprocess.run(
            ["flake8", str(file_path), "--select=E501"],
            check=False,
            capture_output=True,
            text=True
        )
        
        issues = []
        for line in result.stdout.splitlines():
            parts = line.split(':', 3)
            if len(parts) >= 3:
                try:
                    line_num = int(parts[1])
                    issues.append(line_num)
                except ValueError:
                    pass
        
        return issues
    except subprocess.SubprocessError:
        print(f"Error checking line length in {file_path}")
        return []


def manually_fix_line_length(file_path, line_length=79):
    """
    Apply manual fixes for line length issues in specific files.
    
    Args:
        file_path: Path to the Python file to fix
        line_length: Maximum line length (default: 79 characters)
        
    Returns:
        bool: True if changes were made, False otherwise
    """
    print(f"Applying manual line length fixes to {file_path}")
    
    # Get problematic line numbers
    problem_lines = check_line_length_issues(file_path)
    if not problem_lines:
        print(f"No line length issues found in {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    
    # Process each problematic line
    for line_num in problem_lines:
        if 1 <= line_num <= len(lines):
            # Get the line content (0-indexed in our list)
            line = lines[line_num - 1]
            
            if len(line.rstrip('\n')) > line_length:
                # Apply fix based on file type and content
                new_line = fix_line_for_specific_file(file_path, line, line_num)
                
                if new_line != line:
                    lines[line_num - 1] = new_line
                    modified = True
                    print(f"  Fixed line {line_num} in {file_path}")
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✓ Fixed line length issues in {file_path}")
        return True
    
    print(f"Could not automatically fix line length issues in {file_path}")
    return False


def fix_line_for_specific_file(file_path, line, line_num):
    """
    Apply file-specific fixes for long lines.
    
    Args:
        file_path: Path to the file being processed
        line: The problematic line
        line_num: Line number in the file
        
    Returns:
        str: The fixed line
    """
    filename = os.path.basename(file_path)
    indent = len(line) - len(line.lstrip())
    indentation = ' ' * indent
    continued_indent = ' ' * (indent + 4)  # PEP8 recommends 4 space continuation
    
    # Special case for specific files
    if "client.py" in file_path and "stop_sequences" in line and "Optional list of sequences" in line:
        # Line 66 in client.py
        parts = line.strip().split(' ', 3)
        if len(parts) >= 4:
            return f"{indentation}{parts[0]} {parts[1]} {parts[2]}\\\n{continued_indent}{parts[3]}"
            
    elif "prompts.py" in file_path and "questions that test both" in line:
        # Line 67 in prompts.py
        return f"{indentation}\"questions that test both factual recall and deeper \"\n{continued_indent}\"understanding. Each question should be challenging but fair.\""
        
    elif "service.py" in file_path and "api_key" in line:
        # Line 84 in service.py
        return line.replace(": ", ":\\\n" + continued_indent)
    
    elif "service.py" in file_path and "Failed to generate" in line:
        # Line 121 in service.py
        parts = line.split("Failed to")
        if len(parts) == 2:
            return f"{indentation}{parts[0]}Failed to\\\n{continued_indent}generate{parts[1]}"
    
    elif "tokens.py" in file_path and "number of tokens" in line:
        # Line 19 in tokens.py
        parts = line.split(" in ")
        if len(parts) == 2:
            return f"{indentation}{parts[0]}\\\n{continued_indent}in {parts[1]}"
    
    elif "ocr.py" in file_path and "Image.open" in line:
        # Line 25 in ocr.py
        parts = line.rsplit(" for ", 1)
        if len(parts) == 2:
            return f"{indentation}{parts[0]}\\\n{continued_indent}for {parts[1]}"
    
    elif "cache.py" in file_path and "key=" in line:
        # Line 72 in cache.py
        parts = line.split("key=")
        if len(parts) == 2:
            return f"{indentation}{parts[0]}\\\n{continued_indent}key={parts[1]}"
    
    # Generic fixes for other cases
    return apply_generic_fixes(line, indent)
    

def apply_generic_fixes(line, indent):
    """
    Apply generic fixes for long lines.
    
    Args:
        line: The line to fix
        indent: Current indentation level
        
    Returns:
        str: Fixed line
    """
    indentation = ' ' * indent
    continued_indent = ' ' * (indent + 4)  # PEP8 recommends 4 space continuation
    
    # Prioritized list of break points to try
    break_points = []
    
    # 1. Break at logical operators
    for op in [' and ', ' or ']:
        if op in line:
            pos = line.find(op)
            if 20 < pos < len(line) - 20:  # Ensure meaningful parts on both sides
                break_points.append((pos, f"{line[:pos]}\\\n{continued_indent}{line[pos:].lstrip()}"))
    
    # 2. Break at commas in parameter lists or arguments
    if ',' in line and ('(' in line or '[' in line or '{' in line):
        comma_positions = [m.start() for m in re.finditer(r',\s*', line)]
        for pos in sorted(comma_positions):
            if 20 < pos < len(line) - 10:  # Ensure meaningful parts on both sides
                break_points.append((pos + 1, f"{line[:pos + 1]}\n{continued_indent}{line[pos + 1:].lstrip()}"))
    
    # 3. Break at dots in method chains
    if '.' in line:
        dot_positions = [m.start() for m in re.finditer(r'\.', line)]
        for pos in sorted(dot_positions):
            if 20 < pos < len(line) - 10:  # Ensure meaningful parts on both sides
                break_points.append((pos, f"{line[:pos]}\\\n{continued_indent}{line[pos:]}"))
    
    # 4. Break at open parentheses
    if '(' in line:
        paren_positions = [pos for pos, char in enumerate(line) if char == '(']
        for pos in paren_positions:
            if 20 < pos < len(line) - 10:  # Ensure meaningful parts on both sides
                break_points.append((pos + 1, f"{line[:pos + 1]}\n{continued_indent}{line[pos + 1:]}"))
    
    # Try the break points in order of priority (distance from middle)
    if break_points:
        line_middle = len(line) // 2
        sorted_breaks = sorted(break_points, key=lambda bp: abs(bp[0] - line_middle))
        return sorted_breaks[0][1]  # Return the best break
    
    # If no good break point found, return original line
    return line


def format_with_black(file_path, line_length=79):
    """
    Format a file with Black.
    
    Args:
        file_path: Path to the file to format
        line_length: Maximum line length
        
    Returns:
        bool: True if formatting was successful
    """
    try:
        subprocess.run(
            ["black", "--line-length", str(line_length), file_path],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def fix_file(file_path, line_length=79):
    """
    Fix line length issues in a file.
    
    Args:
        file_path: Path to the file to fix
        line_length: Maximum line length
        
    Returns:
        bool: True if file was fixed
    """
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        print(f"Error: {file_path} is not a Python file")
        return False
    
    # First run black to format the file
    print(f"Formatting {file_path} with Black...")
    format_with_black(file_path, line_length)
    
    # Then check for remaining line length issues
    issues = check_line_length_issues(file_path)
    if not issues:
        print(f"✓ No line length issues in {file_path}")
        return True
    
    # Apply manual fixes
    print(f"Applying manual fixes to {file_path} for lines: {issues}")
    return manually_fix_line_length(file_path, line_length)


def main():
    """Main function to fix line length issues."""
    # Check dependencies
    try:
        for cmd in ["black", "flake8"]:
            subprocess.run([cmd, "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Error: Make sure you have Black and flake8 installed:")
        print("  pip install black flake8")
        return 1
    
    # Determine project root and paths
    root_dir = Path(__file__).parent.parent
    quizcraft_dir = root_dir / 'quizcraft'
    
    # Handle single file mode
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        
        # Handle absolute and relative paths
        if not os.path.isabs(target_path):
            full_path = os.path.join(str(quizcraft_dir), target_path)
            if not os.path.exists(full_path):
                full_path = os.path.join(os.getcwd(), target_path)
        else:
            full_path = target_path
        
        if os.path.exists(full_path):
            fix_file(full_path)
        else:
            print(f"Error: File not found: {target_path}")
        return 0
    
    # Find all Python files with line length issues
    result = subprocess.run(
        ["flake8", str(quizcraft_dir), "--select=E501"],
        check=False,
        capture_output=True,
        text=True
    )
    
    problematic_files = set()
    for line in result.stdout.splitlines():
        file_path = line.split(':', 1)[0]
        problematic_files.add(file_path)
    
    if not problematic_files:
        print("No line length issues found.")
        return 0
    
    print(f"Found {len(problematic_files)} files with line length issues:")
    for file_path in sorted(problematic_files):
        print(f"  - {file_path}")
    
    # Fix each file
    fixed_count = 0
    for file_path in sorted(problematic_files):
        if fix_file(file_path):
            fixed_count += 1
    
    # Final report
    print(f"\nSummary: Fixed {fixed_count} out of {len(problematic_files)} files")
    
    # Check for remaining issues
    result = subprocess.run(
        ["flake8", str(quizcraft_dir), "--select=E501"],
        check=False,
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        remaining = len(result.stdout.splitlines())
        print(f"There are still {remaining} line length issues. Manual fixes may be needed.")
    else:
        print("All line length issues have been fixed!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())