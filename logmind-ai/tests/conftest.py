import sys
from pathlib import Path

# Add the logmind-ai directory to Python's import path.
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))