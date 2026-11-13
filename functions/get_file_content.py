from functions.get_filepaths import get_filepaths, FunctionPurpose
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Opens and reads the file with a given file_path, relative to the working directory. Provides a string of file's contents and only read first MAX_CHARS number of characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "A path to the file picked for reading, relative to the working directory",
                },
            },
        },
        "required": ["file_path"],
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    status_message, working_dir_abs, file_path_abs = get_filepaths(
        working_directory, file_path, FunctionPurpose.READ_FILE)
    if "Error" in status_message:
        return status_message

    output: str = status_message + "\n"
    try:
        f = open(file_path_abs, "r")
        output += f.read(MAX_CHARS)
    except Exception as e:
        return output + f'Error: could not open or read the "{file_path}"\n' + str(e)

    try:
        if f.read(1):
            output += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        output += f'...Could not verify if "{file_path}" was truncated or not\n' + str(e)

    return output