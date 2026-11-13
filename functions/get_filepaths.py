import os
from enum import Enum

class FunctionPurpose(Enum):
    LIST_DICTIONARY = 1
    READ_FILE = 2
    WRITE_TO_FILE = 3

def get_filepaths(working_directory: str, target_path: str, purpose: FunctionPurpose) -> tuple[str, str, str]:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
    except Exception as e:
        return (f'Error: Could not get the absolute path of "{working_directory}"\n' + str(e),
                "", "")
    
    try:
        target_path_abs: str = os.path.normpath(os.path.join(working_dir_abs, target_path))
    except Exception as e:
        return (f'Error: Could not get the absolut path of "{target_path}"\n' + str(e),
                "", "")
    
    try:
        match purpose:
            case FunctionPurpose.LIST_DICTIONARY:
                if not os.path.isdir(target_path_abs):
                    return (f'Error: "{target_path}" is not a directory',
                            "", "")
            case FunctionPurpose.READ_FILE:
                if not os.path.isfile(target_path_abs):
                    return (f'Error: File not found or is not a regular file: "{target_path}"',
                            "", "")
            case FunctionPurpose.WRITE_TO_FILE:
                if os.path.isdir(target_path_abs):
                    return (f'Error: Cannot write to "{target_path}" as it is a directory',
                            "", "")
    except Exception as e:
        match purpose:
            case FunctionPurpose.LIST_DICTIONARY:
                return (f'Error: Could not verify if "{target_path}" is a directory\n' + str(e),
                        "", "")
            case FunctionPurpose.READ_FILE:
                return (f'Error: Could not verify if "{target_path}" is a file\n' + str(e),
                        "", "")
            case FunctionPurpose.WRITE_TO_FILE:
                return (f'Error: Could not verify if "{target_path}" is a directory or not\n' + str(e),
                        "", "")

    try:
        valid_target_path: bool = os.path.commonpath([working_dir_abs, target_path_abs]) == working_dir_abs
        if not valid_target_path:
            match purpose:
                case FunctionPurpose.LIST_DICTIONARY:
                    return (f'Error: Cannot list "{target_path}" as it is outside the permitted working directory',
                            "", "")
                case FunctionPurpose.READ_FILE:
                    return (f'Error: Cannot read "{target_path}" as it is outside the permitted working directory',
                            "", "")
                case FunctionPurpose.WRITE_TO_FILE:
                    return (f'Error: Cannot write to "{target_path}" as it is outside the permitted working directory',
                            "", "")
    except Exception as e:
        return (f'Error: Could not calculate the common path of "{working_directory}" and "{target_path}"\n' + str(e),
                "", "")

    return (f'Success: "{target_path}" is within the working directory',
            working_dir_abs, target_path_abs)