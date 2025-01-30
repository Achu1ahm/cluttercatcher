import os

def find_file(root_dir, filename):
    """Recursively search for a file in the project directory."""
    for dirpath, _, filenames in os.walk(root_dir):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None  # Return None if the file is not found

