def write_file(file_path: str, content: str) -> None:
    """
    Writes the given content to the specified file.
    
    Args:
    file_path (str): The path to the file.
    content (str): The content to write to the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError:
        print(f"Error: Unable to write to the file {file_path}.")
