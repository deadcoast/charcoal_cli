import re
import sys
from colorama import Fore, Style, init
import logging

# Initialize colorama
init()

# Set up logging to file
logging.basicConfig(filename='error_log.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_chat_logs(file_path):
    """
    Load the content of a chat log file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logging.error("Error loading chat logs", exc_info=True)
        return None

def extract_code_blocks(chat_logs):
    """
    Advanced regex pattern to extract Python code blocks.
    """
    code_pattern = re.compile(r'```python\n(.*?)```', re.DOTALL)
    try:
        code_blocks = [match.strip() for match in code_pattern.findall(chat_logs)]
        return code_blocks
    except Exception as e:
        logging.error("Error extracting code blocks", exc_info=True)
        return None

def interactive_menu():
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
            chat_logs = load_chat_logs(file_path)
            if chat_logs:
                code_blocks = extract_code_blocks(chat_logs)
                if code_blocks:
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

if __name__ == "__main__":
    try:
        interactive_menu()
    except Exception as e:
        logging.error("An unexpected error occurred", exc_info=True)
        sys.exit(1)