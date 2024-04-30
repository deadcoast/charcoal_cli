import os
import re
from colorama import Fore, Style, init
import logging

from modules.charcoal_logger import ExtractionError

# Initialize colorama
init(autoreset=True)

# Setup logger for error logging
logging.basicConfig(filename='charcoal_error.log',
                    level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class CharcoalParserHandler:
    """Handler class for parsing and extracting python code blocks."""

    def __init__(self, chat_logs: str):
        self.chat_logs = chat_logs
        self.filters = [
            r'(?:```python)(.*?)(?:```)',
            r'(?<=```python\n)([\s\S]+?)(?=\n```)',
            r'(?<!\\)`{3}python\n(.*?\n)`{3}',
            r'(?<!`)```python\s+(.*?)\s+```(?!`)',
        ]

    def extract_code_blocks(self):
        """Extract Python code blocks using multiple filters."""
        for f in self.filters:
            try:
                return re.findall(f, self.chat_logs, re.DOTALL)
            except re.error as e:
                logging.error(f'Regex error: {e}')
                raise ExtractionError(
                    'Failed to extract code blocks due to a regex issue.'
                ) from e

        raise ExtractionError('Failed to extract code blocks due to no matches found.')


# Advanced Regex patterns for Python code extraction resembling a multi-layered charcoal filtering process
PARSER_ONE = r'(?:```python)(.*?)(?:```)'  # Coarse Sand - captures basic fenced code blocks
PARSER_TWO = r'(?<=```python\n)([\s\S]+?)(?=\n```)'  # Fine Sand - more precise, includes newlines surrounding code
# blocks
PARSER_THREE = r'(?<!\\)`{3}python\n(.*?\n)`{3}'  # Pebbles - excludes escaped backticks
PARSER_FOUR = r'(?<!`)```python\s+(.*?)\s+```(?!`)'  # Charcoal - final filter, excludes surrounding single backticks


def search_directories_for_files(directory, extension='.log'):
    """Recursive directory search for files with the given extension."""
    files_found = []
    for root, _, files in os.walk(directory):
        files_found.extend(
            os.path.join(root, file)
            for file in files
            if file.endswith(extension)
        )
    return files_found


def extract_with_filters(content, filters):
    """Use multiple regex filters sequentially for finer code block extraction."""
    for f in filters:
        content = '\n'.join(re.findall(f, content, re.DOTALL))
    return content.strip().split('\n')


def get_paths_from_user():
    """Get the import and export directory paths from the user."""
    import_path = input(f"{Fore.CYAN}Enter the directory to search for chat logs: {Style.RESET_ALL}")
    export_path = input(f"{Fore.CYAN}Enter the directory to save extracted code: {Style.RESET_ALL}")
    return import_path, export_path


def cli_menu():
    """Dynamic, interactive modular CLI menu for templating with color implementation."""
    menu = {
        '1': 'Extract Python code from chat logs',
        '2': 'Set import/export paths',
        '3': 'Show current import/export paths',
        '4': 'Exit'
    }
    import_path, export_path = '', ''
    while True:
        print(f"{Fore.YELLOW}Charcoal - Advanced Python Code Extractor{Style.RESET_ALL}")
        for key, value in menu.items():
            print(f"{Fore.GREEN}{key}. {value}{Style.RESET_ALL}")
        choice = input(f"{Fore.BLUE}Choose an option: {Style.RESET_ALL}")
        if choice == '1':
            if not import_path or not export_path:
                print(f"{Fore.RED}Import/export paths are not set. Please set them first.{Style.RESET_ALL}")
            else:
                try:
                    files_to_process = search_directories_for_files(import_path, '.log')
                    for file_path in files_to_process:
                        if content := extract_with_filters(
                                open(file_path).read(),
                                [
                                    PARSER_ONE,
                                    PARSER_TWO,
                                    PARSER_THREE,
                                    PARSER_FOUR,
                                ],
                        ):
                            with open(os.path.join(export_path, os.path.basename(file_path).replace('.log', '.py')),
                                      'w') as f:
                                f.write(content)
                            print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.MAGENTA}No Python code found in {file_path}{Style.RESET_ALL}")
                except Exception as e:
                    logging.error("An error occurred while extracting code.", exc_info=True)
                    print(f"{Fore.RED}An error occurred. Details have been logged.{Style.RESET_ALL}")
        elif choice == '2':
            import_path, export_path = get_paths_from_user()
        elif choice == '3':
            print(f"{Fore.CYAN}Current import path: {import_path}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Current export path: {export_path}{Style.RESET_ALL}")
        elif choice == '4':
            print(f"{Fore.BLUE}Exiting Charcoal. Thank you for using the tool!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid option, try again.{Style.RESET_ALL}")


if __name__ == '__main__':
    cli_menu()
