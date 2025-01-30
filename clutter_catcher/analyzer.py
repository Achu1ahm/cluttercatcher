import os
import re
from typing import List, Set
from clutter_catcher.utils import find_file

EXCLUDED_DIRS = {'.git', 'node_modules', '.idea', '__pycache__', 'venv', 'dist', 'build','libs'}    
EXCLUDED_FILES = {'requirements.txt', '.gitignore', '.env', 'poetry.lock', 'package-lock.json', "LICENSE", "README.md", "Readme.md", "__init__.py" }
EXCLUDED_EXTENSIONS = ('.txt', '.gitignore', '.env', '.lock', '.json', ".md", ".doc", ".docx", ".xls", ".xlsx", ".pdf", ".ppt", ".pptx", ".svg", ".ttf", ".woff", ".woff2", ".otf", ".eot", ".ico", ".map", ".json", ".img", ".jpeg", ".jpg", ".webp", ".png")

class FileAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = os.path.abspath(project_path)
    
    def get_all_files(self, extensions: List[str] = None) -> Set[str]:
        """Recursively retrieves all project files with the given extensions."""
        all_files = set()
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for file in files:
                if file in EXCLUDED_FILES or file.endswith(EXCLUDED_EXTENSIONS):
                    continue
                if not extensions or any(file.lower().endswith(ext) for ext in extensions):
                    all_files.add(os.path.abspath(os.path.join(root, file)))
        return all_files

    def collect_references(self) -> Set[str]:
        """Finds all referenced files from Python, HTML, CSS, and JS."""
        referenced_files = set()
        python_files = self.get_all_files(['.py'])
        html_files = self.get_all_files(['.html'])
        css_files = self.get_all_files(['.css'])
        js_files = self.get_all_files(['.js'])
      
        # Python: Detect imports and template usage
        for file in python_files:
            with open(file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                matches = re.findall(r'from\s+(\S+)|import\s+(\S+)', content)
                modules = {m.replace('.', '/') + '.py' for tup in matches for m in tup if m}
                referenced_files.update(os.path.join(self.project_path, mod) for mod in modules)

                # flask
                flask_templates = re.findall(r'render_template\s*\(\s*["\']([^"\']+)["\']', content)
                for template in flask_templates:
                    template_path = find_file(self.project_path,template)
                    if template_path:
                        referenced_files.add(template_path)
                
                #django
                 # Extract templates from `render(request, "template.html")`
                django_templates = re.findall(r'render\s*\(\s*[^,]+,\s*["\']([^"\']+)["\']', content)
                 # Extract templates from `template_name = "template.html"`
                django_templates += re.findall(r'template_name\s*=\s*["\']([^"\']+)["\']', content)
                for template in django_templates:
                    template_path = find_file(self.project_path,template)
                    if template_path:
                        referenced_files.add(template_path)
        
        # HTML: Detect linked CSS and JS
        for file in html_files:
            print("file scanning",file)
            with open(file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                matches = re.findall(r'(?:<script.*?src|<link.*?href)=["\'](.*?)["\']', content)
                print("matches",matches)
                print("*"*15)
                referenced_files.update(os.path.abspath(os.path.join(self.project_path, m)) for m in matches)
        
        # CSS: Detect @import
        for file in css_files:
            with open(file, 'r', encoding='utf-8', errors='replace') as f:
                matches = re.findall(r'@import\s+["\'](.*?)["\']', f.read())
                referenced_files.update(os.path.abspath(os.path.join(self.project_path, m)) for m in matches)
        
        # JS: Detect imports and requires
        for file in js_files:
            with open(file, 'r', encoding='utf-8', errors='replace') as f:
                matches = re.findall(r'(?:import.*?from|require)\(["\'](.*?)["\']\)', f.read())
                referenced_files.update(os.path.abspath(os.path.join(self.project_path, m)) for m in matches)
        
        return referenced_files
    
    def find_unused_files(self) -> List[str]:
        """Finds all files that are not referenced anywhere in the project."""
        all_files = self.get_all_files()
        referenced_files = self.collect_references()
        unused_files = all_files - referenced_files
        return sorted(os.path.relpath(f, self.project_path) for f in unused_files)
