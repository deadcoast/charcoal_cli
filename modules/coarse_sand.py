import re
import os


def load_chat_logs(file_path):
    """
    Load the content of a chat log file.
    """
    with open(file_path, 'r') as file:
        return file.read()


def extract_code_blocks(chat_logs):
    """
    Extract Python code blocks enclosed within triple backticks.
    """
    code_pattern = re.compile(r'```python\n(.*?)```', re.DOTALL)
    return [match.strip() for match in code_pattern.findall(chat_logs)]


def save_extracted_code(code_blocks, directory='extracted_code', single_file=False):
    """
    Save the code blocks to .py files in the specified directory.
    """
    os.makedirs(directory, exist_ok=True)
    if single_file:
        with open(os.path.join(directory, 'combined_code.py'), 'w') as combined_file:
            for index, code in enumerate(code_blocks, start=1):
                combined_file.write(f'# Code block {index}\n{code}\n\n')
    else:
        for index, code in enumerate(code_blocks, start=1):
            file_path = os.path.join(directory, f'code_block_{index}.py')
            with open(file_path, 'w') as file:
                file.write(code)


def main(log_file_path):
    """
    Main function to load chat logs, extract Python code, and save them.
    """
    chat_logs = load_chat_logs(log_file_path)
    code_blocks = extract_code_blocks(chat_logs)
    save_extracted_code(code_blocks)


# Call the main function with the path to your chat log
main('path_to_your_chat_log.txt')
