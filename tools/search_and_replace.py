def search_and_replace(file_path: str, search: str, replace: str) -> bool:
    """
    Searches for a string in the specified file and replaces it with another string.
    
    Args:
    file_path (str): The path to the file.
    search (str): The string to search for.
    replace (str): The string to replace the search string with.
    
    Returns:
    bool: True if the operation was successful, False otherwise.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError as e:
        print(f"Error: The file {file_path} does not exist. Details: {e}")
        return False
    except IOError as e:
        print(f"Error: Unable to read the file {file_path}. Details: {e}")
        return False
    
    try:
        content = content.replace(search, replace)
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Successfully replaced '{search}' with '{replace}' in file {file_path}.")
        return True
    except IOError as e:
        print(f"Error: Unable to write to the file {file_path}. Details: {e}")
        return False
