"""Pytest configuration and fixtures"""

import sys
from pathlib import Path

# Add parent directory to path to ensure lama package can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))
