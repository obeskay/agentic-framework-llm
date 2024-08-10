def write_file(file_path, content):
    """
    Writes the given content to the specified file.
    
    Args:
    file_path (str): The path to the file.
    content (str): The content to write to the file.
    """
    with open(file_path, 'w') as file:
        file.write(content)
