import re
import os

def find_file(root_dir, filename):
    """Recursively search for a file in the project directory."""
    for dirpath, _, filenames in os.walk(root_dir):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None  # Return None if the file is not found


def remove_comments(content: str, file_type: str ) -> str:

    if file_type == "py":
        content = re.sub(r'#.*', '', content)  # Remove single-line comments
        content = re.sub(r'""".*?"""|\'\'\'.*?\'\'\'', '', content, flags=re.DOTALL)  # Remove multi-line comments
    elif file_type == "html":
        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    elif file_type == "css":
        # Remove CSS comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    elif file_type == "js":
        # Remove JavaScript comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*', '', content)  # Remove single-line comments
    return content
