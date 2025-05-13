import os
from pathlib import Path
from typing import Optional

ROOT_DIR = str(Path(__file__).parent.parent.parent)

def construct_path(relative_path: str) -> str:
    path_parts = relative_path.split("/")
    absolute_path = os.path.join(ROOT_DIR, *path_parts)
    return absolute_path

def file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)

def file_to_string(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    
def string_to_file(file_path: str, data: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)

# Returns a list of files in the given directory with a specific suffix
def files_in_directory(path: str, suffix: Optional[str] = None) -> list[str]:
    if not os.path.exists(path):
        raise ValueError(f"Directory {path} does not exist.")
    
    files = []
    for file in os.listdir(path):
        if suffix is not None:
            if suffix in file:
                files.append(file)
        else:
            files.append(file)
    return files