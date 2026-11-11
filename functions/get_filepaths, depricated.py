import os

def get_directory_filepath(working_directory: str, directory: str = ".") -> tuple[str, str, str]:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
    except Exception as e:
        return (f'Error: could not get the absolute path of "{working_directory}"\n' + str(e),
                "", "")
    
    try:
        target_dir_abs: str = os.path.normpath(os.path.join(working_dir_abs, directory))
    except Exception as e:
        return (f'Error: could not get the relative path of "{directory}"\n' + str(e),
                "", "")
    
    try:
        if not os.path.isdir(target_dir_abs):
            return (f'Error: "{directory}" is not a directory',
                    "", "")
    except Exception as e:
        return (f'Error: could not verify if "{directory}" is a directory\n' + str(e),
                "", "")

    try:
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, target_dir_abs]) == working_dir_abs
        if not valid_target_dir:
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory',
                    "", "")
    except Exception as e:
        return (f'Error: could not calculate the common path of "{working_directory}" and "{directory}"\n' + str(e),
                "", "")

    return (f'Success: "{directory}" is within the working directory',
            working_dir_abs, target_dir_abs)

def get_file_filepath(working_directory: str, file_path: str) -> tuple[str, str, str]:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
    except Exception as e:
        return (f'Error: could not get the absolute path of "{working_directory}"\n' + str(e),
                "", "")
    
    try:
        file_path_abs: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
    except Exception as e:
        return (f'Error: could not get the relative path of "{file_path}"\n' + str(e),
                "", "")
    
    try:
        if os.path.isdir(file_path_abs):
            return (f'Error: File not found or is not a regular file: "{file_path}"',
                    "", "")
    except Exception as e:
        return (f'Error: could not verify if "{file_path}" is a file\n' + str(e),
                "", "")

    try:
        valid_file_path: bool = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        if not valid_file_path:
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory',
                    "", "")
    except Exception as e:
        return (f'Error: could not calculate the common path of "{working_directory}" and "{file_path}"\n' + str(e),
                "", "")

    return (f'Success: "{file_path}" is within the working directory',
            working_dir_abs, file_path_abs)