import os
import logging
from colorama import Fore, Style, init
from testtools import content

from modules.charcoal_logger import ExtractionError
from modules.charcoal_parser import CharcoalParserHandler, get_paths_from_user, PARSER_TWO, PARSER_ONE, PARSER_THREE, \
    PARSER_FOUR, extract_with_filters, search_directories_for_files
from modules.pebbles import extract_python_code, read_file_content, save_code_blocks_to_files
from modules.coarse_sand import load_chat_logs, extract_code_blocks

# Initialize colorama for colored CLI output
init(autoreset=True)

# Setup logger for error logging
logging.basicConfig(filename='charcoal_logger.py.log',
                    level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Setup logger for info logging
logging.basicConfig(filename='charcoal_logging_info.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Setup a logger
# Setup logger for error logging
logging.basicConfig(filename='charcoal_error.log',
                    level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Setup logger for info logging
logging.basicConfig(filename='charcoal_info.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Setup logger
logger = logging.getLogger('charcoal_cli')


class CharcoalCLI:
    def __init__(self):
        self.import_path = ''
        self.export_path = ''


def coarse_sand_cli_menu():
    """
    Interative CLI menu with color.
    """
    while True:
        print(f"{Fore.YELLOW}Welcome to the Python Code Extractor{Style.RESET_ALL}")
        print("Please select an option:")
        print(f"{Fore.GREEN}1. Load and extract code from a chat log file.{Style.RESET_ALL}")
        print(f"{Fore.RED}2. Exit{Style.RESET_ALL}")
        user_selection = input("Enter your user_selection: ")
        if user_selection == '1':
            file_path = input("Enter the path to your chat log file: ")
            if chat_logs := load_chat_logs(file_path):
                if code_blocks := extract_code_blocks(chat_logs):
                    for index, code in enumerate(code_blocks, start=1):
                        print(f"{Fore.CYAN}> code_block_{index}.py{Style.RESET_ALL}")
                        print(f"{Fore.MAGENTA}{code}{Style.RESET_ALL}")
                        print()
                else:
                    print(f"{Fore.RED}No code blocks found or an error occurred.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Failed to load chat logs.{Style.RESET_ALL}")
        elif user_selection == '2':
            print(f"{Fore.BLUE}Exiting the program. Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid user_selection, please try again.{Style.RESET_ALL}")


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
                                {
                                    PARSER_ONE,
                                    PARSER_TWO,
                                    PARSER_THREE,
                                    PARSER_FOUR,
                                },
                        ):
                            # Save the extracted code to new files
                            save_code_blocks_to_files(content, export_path)
                            # Save the extracted code to a single file
                        with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
                            main_cli_parser(f, file_path, content)
                        # Save the extracted code to a single file
                        with open(os.path.join(export_path, 'all_code.py'), 'w', encoding='utf-8') as f:
                            f.write('\n\n'.join(content))
                            print(
                                f"{Fore.MAGENTA}Code extracted and saved to single file: all_code.py{Style.RESET_ALL}")

                except AttributeError:
                    logging.error("An error occurred while extracting code.", exc_info=True)
                    print(f"{Fore.RED}An error occurred. Details have been logged.{Style.RESET_ALL}")
        elif choice == '2':
            import_path = input("Enter the path to your import directory: ")
            export_path = input("Enter the path to your export directory: ")
        elif choice == '3':
            if import_path:
                print(f"Import path: {import_path}")
            if export_path:
                print(f"Export path: {export_path}")
            else:
                print(f"{Fore.RED}Export path is not set. Please set it first.{Style.RESET_ALL}")
        elif choice == '4':
            print(f"{Fore.BLUE}Exiting the program. Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid user_selection, please try again.{Style.RESET_ALL}")
            # Save the extracted code to new files
            save_code_blocks_to_files(content, export_path)
            # Save the extracted code to a single file

            with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
                main_cli_parser(f, file_path, content)
                if content:
                    print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.MAGENTA}No Python code found in {file_path}{Style.RESET_ALL}")
            print()


def file_path():
    """Extract Python code from chat logs and save to new files."""
    file_path = input("Enter the path to your chat log file: ")
    if chat_logs := load_chat_logs(file_path):
        if code_blocks := extract_code_blocks(chat_logs):
            for index, code in enumerate(code_blocks, start=1):
                file_name = f'code_block_{index}.py'
                with open(os.path.join(export_path, file_name), 'w', encoding='utf-8') as f:
                    f.write(code)
                    print(f"{Fore.MAGENTA}Code extracted and saved to {file_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No Python code found in {file_path}{Style.RESET_ALL}")
    file_path = input("Enter the path to your chat log file: ")
    if chat_logs := load_chat_logs(file_path):
        if code_blocks := extract_code_blocks(chat_logs):
            for index, code in enumerate(code_blocks, start=1):
                print(f"{Fore.CYAN}> code_block_{index}.py{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}{code}{Style.RESET_ALL}")
                print()


def export export_paths():
    """Extract Python code from chat logs and save to new files."""
    if import_path:
        print(f"Import path: {import_path}")
    if export_path:
        print(f"Export path: {export_path}")
    else:
        print(f"{Fore.RED}Export path is not set. Please set it first.{Style.RESET_ALL}")
    import_path = input("Enter the path to your import directory: ")
    export_path = input("Enter the path to your export directory: ")
    return import_path, export_path

    """Extract Python code from chat logs and save to new files."""
    if import_path:
        print(f"Import path: {import_path}")
    if export_path:
        print(f"Export path: {export_path}")
    else:
        print(f"{Fore.RED}Export path is not set. Please set it first.{Style.RESET_ALL}")
    import_path = input("Enter the path to your import directory: ")
    export_path = input("Enter the path to your export directory: ")

        return import_path, export_path




"""Extract Python code from chat logs and save to new files."""
if chat_logs := load_chat_logs(file_path):
    if code_blocks := extract_code_blocks(chat_logs):
        for index, code in enumerate(code_blocks, start=1):
            file_name = f'code_block_{index}.py'
            with open(os.path.join(export_path, file_name), 'w', encoding='utf-8') as f:
                f.write(code)
                print(f"{Fore.MAGENTA}Code extracted and saved to {file_name}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No Python code found in {file_path}{Style.RESET_ALL}")
file_path = input("Enter the path to your chat log file: ")
if chat_logs := load_chat_logs(file_path):
    if code_blocks := extract_code_blocks(chat_logs):
        for index, code in enumerate(code_blocks, start=1):
            print(f"{Fore.CYAN}> code_block_{index}.py{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{code}{Style.RESET_ALL}")
            print()


def set_paths(file_path=None, export_path=None):
    """Extract Python code from chat logs and save to new files."""
    if chat_logs := load_chat_logs(file_path):
        if code_blocks := extract_code_blocks(chat_logs):
            for index, code in enumerate(code_blocks, start=1):
                file_name = f'code_block_{index}.py'
                with open(os.path.join(export_path, file_name), 'w', encoding='utf-8') as f:
                    f.write(code)
                    print(f"{Fore.MAGENTA}Code extracted and saved to {file_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No Python code found in {file_path}{Style.RESET_ALL}")
    file_path = input("Enter the path to your chat log file: ")
    if chat_logs := load_chat_logs(file_path):
        if code_blocks := extract_code_blocks(chat_logs):
            for index, code in enumerate(code_blocks, start=1):
                print(f"{Fore.CYAN}> code_block_{index}.py{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}{code}{Style.RESET_ALL}")
                print()
    """Set import and export paths."""
    import_path = input("Enter the path to your import directory: ")
    export_path = input("Enter the path to your export directory: ")
    return import_path, export_path


def export_code(file_path=None):
    """Extract Python code from chat logs and save to new files."""
    if chat_logs := load_chat_logs(file_path):
        if code_blocks := extract_code_blocks(chat_logs):
            for index, code in enumerate(code_blocks, start=1):
                file_name = f'code_block_{index}.py'
                with open(os.path.join(export_path, file_name), 'w', encoding='utf-8') as f:
                    f.write(code)
                    print(f"{Fore.MAGENTA}Code extracted and saved to {file_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No Python code found in {file_path}{Style.RESET_ALL}")
    file_path = input("Enter the path to your chat log file: ")
    if chat_logs := load_chat_logs(file_path):
        if code_blocks := extract_code_blocks(chat_logs):
            for index, code in enumerate(code_blocks, start=1):
                print(f"{Fore.CYAN}> code_block_{index}.py{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}{code}{Style.RESET_ALL}")
                print()


# Save the extracted code to new files
save_code_blocks_to_files(content)

# Save the extracted code to a single file
with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
    f.write(f'\n\n# {file_path}\n')
    f.write('\n\n'.join(content))
    f.write('\n\n')
    print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
    else:
    print(f"{Fore.MAGENTA}No Python code found in {file_path}{Style.RESET_ALL}")
print()
except AttributeError:
logging.error("An error occurred while extracting code.", exc_info=True)
print(f"{Fore.RED}An error occurred. Details have been logged.{Style.RESET_ALL}")
elif choice == '2':
import_path = input("Enter the path to your import directory: ")
export_path = input("Enter the path to your export directory: ")
elif choice == '3':
if import_path:
    print(f"Import path: {import_path}")
if export_path:
    print(f"Export path: {export_path}")
else:
    print(f"{Fore.RED}Export path is not set. Please set it first.{Style.RESET_ALL}")
elif choice == '4':
print(f"{Fore.BLUE}Exiting the program. Goodbye!{Style.RESET_ALL}")
else:
print(f"{Fore.RED}Invalid user_selection, please try again.{Style.RESET_ALL}")
# Save the extracted code to new files
save_code_blocks_to_files(content, export_path)
# Save the extracted code to a single file

with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
    f.write(f'\n\n# {file_path}\n')
    f.write('\n\n'.join(content))
    f.write('\n\n')
    print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
    else:
    print(f"{Fore.MAGENTA}No Python code found in {file_path}{Style.RESET_ALL}")
print()


def cli_menu(x=print(f"{Fore.MAGENTA}Code extracted and saved to single file: all_code.py{Style.RESET_ALL}")):
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
                                {
                                    PARSER_ONE,
                                    PARSER_TWO,
                                    PARSER_THREE,
                                    PARSER_FOUR,
                                },
                        ): x = 1  # Save the extracted code to new files
                        save_code_blocks_to_files(content, export_path)
                        # Save the extracted code to a single file
                        with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
                            f.write(f'\n\n# {file_path}\n')
                            f.write('\n\n'.join(content))
                            f.write('\n\n')
                            print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
                        else:
                        print(f"{Fore.MAGENTA}No Python code found in {file_path}{Style.RESET_ALL}")
                    if content:
                        # Save the extracted code to a single file
                        with open(os.path.join(export_path, 'all_code.py'), 'w', encoding='utf-8') as f:
                            f.write('\n\n'.join(content))
                        # Save the extracted code to new files
                        save_code_blocks_to_files(content, export_path)

                        # Save the extracted code to a single file
                        with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
                            f.write('\n\n'.join(content))
                        # Save the extracted code to new files
                        save_code_blocks_to_files(content, export_path)

                        # Save the extracted code to a single file
                        with open(os.path.join(export_path, 'all_code.py'), 'w', encoding='utf-8') as f:
                            f.write('\n\n'.join(content))
                        # Save the extracted code to new files
                        save_code_blocks_to_files(content, export_path)
                        # Save the extracted code to a single file
                        with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
                            f.write('\n\n'.join(content))
                        with open(os.path.join(export_path, 'all_code.py'), 'w', encoding='utf-8') as f:
                            f.write('\n\n'.join(content))
                        # Save the extracted code to a single file
                        with open(os.path.join(export_path, os.path.basename(file_path).replace('.log', '.py')), 'w',
                                  encoding='utf-8'), open(os.path.join(export_path, 'all_code.py'), 'w') as f:
                            f.write('\n\n'.join(content))
                            print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
                            print(f"{Fore.MAGENTA}No Python code found in {file_path}{Style.RESET_ALL}")
                    logging.error("An error occurred while extracting code.", exc_info=True)
                    print(f"{Fore.RED}An error occurred. Details have been logged.{Style.RESET_ALL}")

            import_path = input("Enter the path to your import directory: ")
            export_path = input("Enter the path to your export directory: ")
            if not import_path or not export_path:
                print(f"{Fore.RED}Import/export paths are not set. Please set them first.{Style.RESET_ALL}")
            else:
                try:
                    files_to_process = search_directories_for_files(import_path, '.log')
                    for file_path in files_to_process:
                        if content := extract_with_filters(
                                open(file_path).read(),
                                {
                                    PARSER_ONE,
                                    PARSER_TWO,
                                    PARSER_THREE,
                                    PARSER_FOUR,
                                },
                        ):
                            # Save the extracted code to new files
                            save_code_blocks_to_files(content, export_path)
                            x
                            # Save the extracted code to new files
                            save_code_blocks_to_files(content, export_path)
                            x
                            # Save the extracted code to new files
                            save_code_blocks_to_files(content, export_path)
                            x
                            # Save the extracted code to a single file
                            with open(os.path.join(export_path, 'all_code.py'), 'w', encoding='utf-8') as f:
                                f.write('\n\n'.join(content))
                            x
                            # Save the extracted code to a single file
                            with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
                                f.write('\n\n'.join(content))
                            x
                            with open(os.path.join(export_path, os.path.basename(file_path).replace('.log', '.py')),
                                      'w', encoding='utf-8') as f:
                                f.write('\n\n'.join(content))
                                print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
                            import_path = input("Enter the path to your import directory: ")
                            export_path = input("Enter the path to your export directory: ")
                            if not import_path or not export_path:
                                print(
                                    f"{Fore.RED}Import/export paths are not set. Please set them first.{Style.RESET_ALL}")
                            else:
                                try:
                                    files_to_process = search_directories_for_files(import_path, '.log')
                                    for file_path in files_to_process:
                                        if content := extract_with_filters(
                                                open(file_path).read(),
                                                {
                                                    PARSER_ONE,
                                                    PARSER_TWO,
                                                    PARSER_THREE,
                                                    PARSER_FOUR,
                                                },
                                        ):
                                            # Save the extracted code to a single file
                                            with open(os.path.join(export_path, 'all_code.py'), 'w',
                                                      encoding='utf-8') as f:


def main():
