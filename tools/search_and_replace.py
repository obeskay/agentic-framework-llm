def search_and_replace(file_path: str, search: str, replace: str) -> None:
    """
    Searches for a string in the specified file and replaces it with another string.
    
    Args:
    file_path (str): The path to the file.
    search (str): The string to search for.
    replace (str): The string to replace the search string with.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return
    except IOError:
        print(f"Error: Unable to read the file {file_path}.")
        return
    
    try:
        content = content.replace(search, replace)
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError:
        print(f"Error: Unable to write to the file {file_path}.")
