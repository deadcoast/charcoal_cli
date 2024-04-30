import os
import re
import sys
import logging
from colorama import Fore, Style

from modules.charcoal_logger import ExtractionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Advanced Regex pattern for Python code block extraction
PYTHON_CODE_BLOCK_PATTERN = r'```python\s+(.*?)\s+```'


def read_file_content(file_path):
    """Read and return the content of the given file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f'File not found: {file_path}')
        raise
    except IOError:
        logger.error(f'Error reading file: {file_path}')
        raise


def extract_python_code(content):
    """Extract python code using regex pattern."""
    try:
        return re.findall(PYTHON_CODE_BLOCK_PATTERN, content, re.DOTALL)
    except re.error as e:
        logger.error(f'Regex error: {e}')
        raise ExtractionError(
            'Failed to extract code blocks due to a regex issue.'
        ) from e


def display_menu():
    """Interactive CLI menu for user to choose actions."""
    print(f"{Fore.YELLOW}Python Code Extractor Menu{Style.RESET_ALL}")
    options = ["Extract Python code from file", "Exit"]
    for i, option in enumerate(options, start=1):
        print(f"{Fore.GREEN}{i}. {option}{Style.RESET_ALL}")


def extract_code_from_file(file_path):
    """Handle the file reading and code extraction process."""
    content = read_file_content(file_path)
    return extract_python_code(content)


def save_code_blocks_to_files(code_blocks, dir_path='extracted_code'):
    """Save the extracted code blocks to separate files."""
    os.makedirs(dir_path, exist_ok=True)
    for i, block in enumerate(code_blocks, start=1):
        file_path = f'{dir_path}/code_block_{i}.py'
        with open(file_path, 'w') as file:
            file.write(block)
        print(f"{Fore.MAGENTA}Saved: {file_path}{Style.RESET_ALL}")


def main():
    """Main execution function."""
    display_menu()
    choice = input("Choose an option: ")
    if choice == '1':
        file_path = input("Enter path to the chat log file: ")
        try:
            code_blocks = extract_code_from_file(file_path)
            save_code_blocks_to_files(code_blocks)
        except Exception as e:
            logger.error(f'Unexpected error occurred: {e}')
    elif choice == '2':
        print(f"{Fore.BLUE}Goodbye!{Style.RESET_ALL}")
        sys.exit()


if __name__ == '__main__':
    main()
