import subprocess
from functions.get_filepaths import get_filepaths, FunctionPurpose
from config import RUN_PYTHON_FILE_TIMEOUT

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Creates a subprocess inside which executes a python script in a file wth a given file_path, relative to the working directory. Provides the standart output and standart error returned by the executed script",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "A path to the file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "A list of additional commands to be passed to the subprocess",
                }
            },
        },
        "required": ["file_path"],
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    if file_path.split(".")[-1] != "py":
        return f'Error: "{file_path}" is not a Python file'
    
    status_message, working_dir_abs, file_path_abs = get_filepaths(
        working_directory, file_path, FunctionPurpose.EXECUTE_FILE)
    if "Error" in status_message:
        return status_message
    output: str = status_message + "\n"

    command = ["python", file_path_abs]
    if args:
        command.extend(args)
    process = subprocess.run(command, capture_output=True, text=True, timeout=RUN_PYTHON_FILE_TIMEOUT)

    if process.returncode != 0:
        output += f"Process exited with code {process.returncode}\n"
    if process.stdout:
        output += "STDOUT:\n" + process.stdout
    if process.stderr:
        output += "\nSTDERR:\n" + process.stderr
    if not(process.stdout and process.stderr):
        output += "No output produced"
    return output

