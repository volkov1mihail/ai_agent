import os
from functions.get_filepaths import get_filepaths, FunctionPurpose
from config import MAX_PERMISSION_LOOPS, MAX_LEN_DISPLAYED_CONTENT

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Asks for a permission to open and writea the given content to the file with a given file_path, relative to the working directory. If the permission is given, writes to file",
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

    print(status_message + "\n")
    for i in range(MAX_PERMISSION_LOOPS):
        permission = input(f'Write to "{file_path}"?\n0 - decline\n1 - allow\n2 - show the content prepared for writing\n')
        match int(permission):
            case 0:
                return f'Error: Declined the permission to write to "{file_path}"'
            case 1:
                break
            case 2:
                print_prepared_content(content)
            case _:
                pass

    output: str = ""
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

def print_next_part() -> bool:
    while True:
        print_part = input("0 - stop printing\n1 - show more content\n")
        match print_part:
            case 0:
                return False
            case 1:
                return True
            case _:
                pass

def print_prepared_content(content: str) -> None:
    if len(content) <= MAX_LEN_DISPLAYED_CONTENT:
        print(content)
    else:
        counter = 0
        print_next = True
        while(print_next and len(content) >= MAX_LEN_DISPLAYED_CONTENT * counter):
            if len(content) >= MAX_LEN_DISPLAYED_CONTENT * (counter + 1):
                print(content[MAX_LEN_DISPLAYED_CONTENT * counter : MAX_LEN_DISPLAYED_CONTENT * (counter + 1)])
                print_next = print_next_part()
            else:
                print(content[MAX_LEN_DISPLAYED_CONTENT * counter : len(content)])
            counter += 1
    return