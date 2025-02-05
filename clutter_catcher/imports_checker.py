import os
from glob import glob
from clutter_catcher.utils import find_file

def validate_project_path(ctx, param, value):
    if not os.path.exists(value):
        raise click.BadParameter(f"The path '{value}' does not exist.")
    return value

def resolve_file_path(project_path, current_file, referenced_path):
    """Resolve file path dynamically, searching entire project directory"""
    # Normalize all paths to absolute
    project_path = os.path.abspath(project_path)
    current_file = os.path.abspath(current_file)

    if referenced_path.startswith('/'):
        # Handle absolute paths (relative to project root)
        relative_path = referenced_path.lstrip('/').replace('/', os.path.sep)
        
        # Search pattern: project_path/**/relative_path
        search_pattern = os.path.join(project_path, "**", relative_path)
        matches = glob(search_pattern, recursive=True)
        
        if matches:
            # Return first match (prioritize shallowest directory)
            return os.path.abspath(matches[0])
    else:
        # Handle relative paths from current file's directory
        current_dir = os.path.dirname(current_file)
        resolved_path = os.path.join(current_dir, referenced_path)
        
        # Security check: ensure path stays within project
        if os.path.commonpath([project_path, resolved_path]) == project_path:
            if os.path.exists(resolved_path):
                return os.path.abspath(resolved_path)
    
    return None
