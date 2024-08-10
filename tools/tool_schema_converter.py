def convert_tools_to_openai_schema():
    """
    Converts the tools defined in the tools directory to the OpenAI schema.
    
    Returns:
    list: A list of tools formatted according to the OpenAI schema.
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Writes content to a specified file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file."
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file."
                        }
                    },
                    "required": ["file_path", "content"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Reads content from a specified file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file."
                        }
                    },
                    "required": ["file_path"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_and_replace",
                "description": "Searches for a string in a specified file and replaces it with another string.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file."
                        },
                        "search": {
                            "type": "string",
                            "description": "The string to search for."
                        },
                        "replace": {
                            "type": "string",
                            "description": "The string to replace the search string with."
                        }
                    },
                    "required": ["file_path", "search", "replace"],
                    "additionalProperties": False
                }
            }
        }
    ]
    return tools
