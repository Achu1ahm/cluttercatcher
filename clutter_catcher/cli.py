import click
from clutter_catcher.analyzer import FileAnalyzer
from clutter_catcher.utils import validate_project_path

@click.command()
@click.argument("project_path", callback=validate_project_path)
def main(project_path):
    analyzer = FileAnalyzer(project_path)

    print("Scanning Files...")
    unused_files = analyzer.find_unused_files()

    if unused_files:
        print("Unused files detected")
        for file in unused_files:
            print(f"- {file}")
    else:
        print("No unused files detected.")

if __name__ == "__main__":
    main()