# conftest.py
import sys
import pathlib

# insert src/ at the front of sys.path before any tests run
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))
