import os
import tempfile
from clutter_catcher.analyzer import FileAnalyzer

def test_get_all_files():
    # Setup a temporary directory with sample files
    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = os.path.join(temp_dir, "file1.py")
        file2 = os.path.join(temp_dir, "file2.txt")
        with open(file1, "w"), open(file2, "w"):
            pass

        analyzer = FileAnalyzer(temp_dir)
        all_files = analyzer.get_all_files()

        assert file1 in all_files
        assert file2 in all_files

def test_find_unused_files():
    # Setup a temporary directory with sample files
    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = os.path.join(temp_dir, "file1.py")
        file2 = os.path.join(temp_dir, "file2.txt")
        with open(file1, "w"), open(file2, "w"):
            pass

        analyzer = FileAnalyzer(temp_dir)
        unused_files = analyzer.find_unused_files()

        assert file2 in unused_files
        assert file1 not in unused_files
