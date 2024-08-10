import os
import logging

logging.basicConfig(level=logging.INFO)

def write_file(file_path: str, content: str) -> tuple:
    """
    Writes the given content to the specified file.
    
    Args:
    file_path (str): The path to the file.
    content (str): The content to write to the file.
    
    Returns:
    tuple: (bool, str) - (True if successful, message) or (False if failed, error message)
    """
    if not content:
        return False, "No content provided to write"

    try:
        # Check if the directory exists, and create it if it doesn't
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, mode=0o755, exist_ok=True)
        
        with open(file_path, 'w') as file:
            file.write(content)
        logging.info(f"Successfully wrote to file {file_path}.")
        return True, "File written successfully"
    except IOError as e:
        error_msg = f"Unable to write to the file {file_path}. Details: {e}"
        logging.error(f"Error: {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error occurred while writing to {file_path}: {e}"
        logging.error(error_msg)
        return False, error_msg
