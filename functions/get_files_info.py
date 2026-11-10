import os

def get_filepaths(working_directory: str, directory: str = ".") -> tuple[str, str, str]:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
    except Exception as e:
        return (f"Error: could not get the absolute path of {working_directory}\n" + str(e),
                "", "")
    
    try:
        target_dir_abs: str = os.path.normpath(os.path.join(working_dir_abs, directory))
    except Exception as e:
        return (f"Error: could not get the relative path of {directory}\n" + str(e),
                "", "")
    
    try:
        if not os.path.isdir(target_dir_abs):
            return (f'Error: "{directory}" is not a directory',
                    "", "")
    except Exception as e:
        return (f"Error: could not verify if {directory} is a real directory\n" + str(e),
                "", "")

    try:
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, target_dir_abs]) == working_dir_abs
        if not valid_target_dir:
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory',
                    "", "")
    except Exception as e:
        return (f"Error: could not calculate the common path of {working_directory} and {directory}\n" + str(e),
                "", "")

    return (f'Success: "{directory}" is within the working directory',
            working_dir_abs, target_dir_abs)

def get_file_info(filepath: str) -> tuple[int, bool, str]:
    try:
        file_size: int =  os.path.getsize(filepath)
    except Exception as e:
        return 0, False, f"Error: could not calculate the size of {filepath}\n" + str(e)

    try:
        is_dir: bool = os.path.isdir(filepath)
    except Exception as e:
        return file_size, False, f"Error: could not verify if {filepath} is a directory or not\n" + str(e)

    return file_size, is_dir, f"Success: acquired information about {filepath}"

def generate_file_info(filepath: str) -> str:
    file_size, is_dir, status_message = get_file_info(filepath)
    if "Error" in status_message:
        return status_message

    file_name: str = filepath.split("/")[-1]
    return f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"



def get_files_info(working_directory: str, directory: str = ".") -> str:
    status_message, working_dir_abs, target_dir_abs = get_filepaths(working_directory, directory)
    if "Error" in status_message:
        return status_message

    output: str = status_message + "\n"
    try:
        contents: list[str] = os.listdir(target_dir_abs)
    except Exception as e:
        return output + f"Error: could not get the contents of {directory}\n" + str(e)
    if len(contents) == 0:
        return output + f"The {directory} has no contents"

    directory_in_string = "current" if directory == "." else f"\"{directory}\""
    result = f"Result for {directory_in_string} directory:\n"
    files_info = map(lambda file: generate_file_info(target_dir_abs + "/" + file), contents)
    return result + "\n".join(files_info)
        
    