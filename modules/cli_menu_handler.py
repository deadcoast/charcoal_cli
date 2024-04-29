import os
import logging
from colorama import Fore, Style

from charcoal_cli.charcoal_cli.src.charcoal_cli_parser import load_chat_logs, extract_code_blocks, save_code_blocks_to_files
from charcoal_cli import get_paths_from_user, search_directories_for_files
from charcoal_cli import extract_with_filters
from charcoal_cli import PARSER_ONE, PARSER_TWO, PARSER_THREE, PARSER_FOUR


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
        choice = input("Enter your choice: ")
        if choice == '1':
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
        elif choice == '2':
            print(f"{Fore.BLUE}Exiting the program. Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")


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
                            f.write(f'\n\n# {file_path}\n')
                            f.write('\n\n'.join(content))
                            f.write('\n\n')
                            print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
                        # Save the extracted code to a single file

                        elif content := extract_with_filters(open(file_path).read(), [PARSER_ONE, PARSER_TWO, PARSER_THREE, PARSER_FOUR]):
                            # Save the extracted code to new files
                            save_code_blocks_to_files(content, export_path)
                            # Save the extracted code to a single file

                            with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
                                f.write(f'\n\n# {file_path}\n')
                                f.write('\n\n'.join(content))
                                f.write('\n\n')
                                print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
                            # Save the extracted code to a single file
                            with open(os.path.join(export_path, 'all_code.py'), 'a', encoding='utf-8') as f:
                                f.write('\n\n'.join(content))
                            print(f"{Fore.MAGENTA}Code extracted and saved to single file: all_code.py{Style.RESET_ALL}")
                        elif content := extract_with_filters(open(file_path).read(), [PARSER_ONE, PARSER_TWO, PARSER_THREE, PARSER_FOUR]):
                            # Save the extracted code to new files
                            save_code_blocks_to_files(content, export_path)
                            # Save the extracted code to a single file
                        # Save the extracted code to a single file
                        elif content := extract_with_filters(open(file_path).read(), [PARSER_ONE, PARSER_TWO, PARSER_THREE, PARSER_FOUR]):
                            # Save the extracted code to a single file
                            with open(os.path.join(export_path, 'all_code.py'), 'w', encoding='utf-8') as f:
                                f.write('\n\n'.join(content))
                            print(f"{Fore.MAGENTA}Code extracted and saved to single file: all_code.py{Style.RESET_ALL}")
                        elif content := extract_with_filters(open(file_path).read(), [PARSER_ONE, PARSER_TWO, PARSER_THREE, PARSER_FOUR]):
                            # Save the extracted code to a single file
                            with open(os.path.join(export_path, os.path.basename(file_path).replace('.log', '.py')), 'w', encoding='utf-8'),
                                      'w') as f:
                                f.write('\n\n'.join(content))
                            print(f"{Fore.MAGENTA}Code extracted and saved from {file_path}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.MAGENTA}No Python code found in {file_path}{Style.RESET_ALL}")
                except AttributeError:
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
