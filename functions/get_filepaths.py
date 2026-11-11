import os

def get_filepaths(working_directory: str, target_path: str, is_dir: bool) -> tuple[str, str, str]:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
    except Exception as e:
        return (f'Error: could not get the absolute path of "{working_directory}"\n' + str(e),
                "", "")
    
    try:
        target_path_abs: str = os.path.normpath(os.path.join(working_dir_abs, target_path))
    except Exception as e:
        return (f'Error: could not get the absolut path of "{target_path}"\n' + str(e),
                "", "")
    
    try:
        is_file = not is_dir
        is_dir_error = (f'Error: "{target_path}" is not a directory' if is_dir else
                        f'Error: File not found or is not a regular file: "{target_path}"')
        if (is_dir and not os.path.isdir(target_path_abs)
            or is_file and not os.path.isfile(target_path_abs)):
            return (is_dir_error, "", "")
    except Exception as e:
        return (f'Error: could not verify if "{target_path}" is a {'directory' if is_dir else 'file'}\n' + str(e),
                "", "")

    try:
        valid_target_path: bool = os.path.commonpath([working_dir_abs, target_path_abs]) == working_dir_abs
        if not valid_target_path:
            return (f'Error: Cannot {'list' if is_dir else 'read'} "{target_path}" as it is outside the permitted working directory',
                    "", "")
    except Exception as e:
        return (f'Error: could not calculate the common path of "{working_directory}" and "{target_path}"\n' + str(e),
                "", "")

    return (f'Success: "{target_path}" is within the working directory',
            working_dir_abs, target_path_abs)