def search_and_replace(file_path, search, replace):
    """
    Searches for a string in the specified file and replaces it with another string.
    
    Args:
    file_path (str): The path to the file.
    search (str): The string to search for.
    replace (str): The string to replace the search string with.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    
    content = content.replace(search, replace)
    
    with open(file_path, 'w') as file:
        file.write(content)
