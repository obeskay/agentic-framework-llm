def read_file(file_path: str) -> str:
    """
    Reads the content from the specified file.
    
    Args:
    file_path (str): The path to the file.
    
    Returns:
    str: The content of the file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return ""
    except IOError:
        print(f"Error: Unable to read the file {file_path}.")
        return ""
