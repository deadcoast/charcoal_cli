import logging
import os
import re
import sys
from typing import List, Optional

from colorama import Fore, Style, init

from modules.cli_menu_handler import coarse_sand_cli_menu, cli_menu
from scripts.trove_classifier import pep508_identifier, python_identifier, pep517_backend_reference

# Initialize colorama for colored CLI output
init(autoreset=True)

# Initialize colorama
init()

# Setup logger for error logging
logging.basicConfig(filename='charcoal_error.log',
                    level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Set up logging to file
logging.basicConfig(filename='error_log.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# Advanced Regex patterns for Python code extraction resembling a multi-layered charcoal filtering process
PARSER_ONE = r'(?:```python)(.*?)(?:```)'  # Coarse Sand - captures basic fenced code blocks
PARSER_TWO = r'(?<=```python\n)([\s\S]+?)(?=\n```)'  # Fine Sand - more precise, includes newlines surrounding code
# blocks
PARSER_THREE = r'(?<!\\)`{3}python\n(.*?\n)`{3}'  # Pebbles - excludes escaped backticks
PARSER_FOUR = r'(?<!`)```python\s+(.*?)\s+```(?!`)'  # Charcoal - final filter, excludes surrounding single backticks


def _chain(module_parts: List[str], param: List[str]) -> List[str]:
    """
    Chains the module parts and parameters together.
    
    Args:
        module_parts (List[str]): The list of module parts.
        param (List[str]): The list of parameters.
    
    Returns:
        List[str]: The chained list of module parts and parameters.
    """
    if not module_parts and not param:
        return []

    if not isinstance(module_parts, list) or not isinstance(param, list):
        raise TypeError("Inputs must be lists.")

    if not module_parts:
        return []

    return module_parts + param if param else []


def python_entrypoint_reference(value: str) -> bool:
    module_match = re.match(r"([^:]+):(.+)", value)
    if not module_match:
        return False

    module = module_match[1]
    rest = module_match[2]

    if "[" in rest:
        obj_match = re.match(r"([^[]+)\[(.+)]", rest)
        if not obj_match:
            return False

        obj = obj_match[1]
        extras_ = obj_match[2]

        if not extras_.endswith("]"):
            return False

        extras = (x.strip() for x in re.split(r",", extras_.strip("[]")))

        if any(not pep508_identifier(x) for x in extras):
            return False

        python_entrypoint_reference.logger.warn(f"`{value}` - using extras for entry points is not recommended")
    else:
        obj = rest

    module_parts = re.split(r"\.", module)
    identifiers = module_parts + re.split(r"\.", obj) if rest else module_parts

    return all(python_identifier(i) for i in identifiers)

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
    except re.error as py:
        logger.error(f'Regex error: {py}')
        raise ExtractionError(
            'Failed to extract code blocks due to a regex issue.'
        ) from py


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


def interactive_menu():
    pass


def main():
    """Main execution function."""
    quick_display_menu()
    coarse_sand_cli_menu()
    choice = input("Choose an option: ")
    if choice == '1':
        file_path = input("Enter path to the chat log file: ")
        try:
            code_blocks = extract_code_from_file(file_path)
            save_code_blocks_to_files(code_blocks)
        except ImportError:
            logger.error(f'Unexpected error occurred: {e}')
    elif choice == '2':
        print(f"{Fore.BLUE}Goodbye!{Style.RESET_ALL}")
        sys.exit()


if __name__ == '__main__':
    try:
        interactive_menu()
        main()
        sys.exit(0)
    except (KeyboardInterrupt, EOFError):
        print(f"{Fore.RED}Exiting the program. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        logging.error("An unexpected error occurred", exc_info=True)
        coarse_sand_cli_menu()
        interactive_menu()
        main()
        sys.exit(0)
    except (KeyboardInterrupt, EOFError):
        print(f"{Fore.RED}Exiting the program. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    try:
        pep508_identifier()

        pep517_backend_reference()

        python_entrypoint_reference = pep517_backend_reference(  # type: ignore
            "module:obj[extra1, extra2]")

        python_identifier()
    except ImportError:
        logger.error('Unexpected error occurred')
