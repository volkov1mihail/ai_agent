import os
from functions.get_filepaths import get_filepaths, FunctionPurpose

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Opens and writes the given content to the file with a given file_path, relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "A path to the file to write to. The path is relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the chosen file",
                }
            },
        },
        "required": ["file_path", "content"],
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    status_message, working_dir_abs, file_path_abs = get_filepaths(working_directory, file_path, FunctionPurpose.WRITE_TO_FILE)
    if "Error" in status_message:
        return status_message

    output: str = status_message + "\n"
    try:
        dir_path = file_path_abs.split("/")
        os.makedirs("/".join(dir_path[:-1]), exist_ok=True)
    except Exception as e:
        return output + f'Error: Could not verify the existence of parent directories of "{file_path}"\n' + str(e)

    try:
        with open(file_path_abs, "w") as f:
            f.write(content)
    except Exception as e:
        return output + f'Error: Could not open or write to "{file_path}"\n' + str(e)

    return output + f'Successfully wrote to "{file_path}" ({len(content)} characters written)'