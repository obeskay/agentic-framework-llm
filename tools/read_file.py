def read_file(file_path):
    """
    Reads the content from the specified file.
    
    Args:
    file_path (str): The path to the file.
    
    Returns:
    str: The content of the file.
    """
    with open(file_path, 'r') as file:
        return file.read()
