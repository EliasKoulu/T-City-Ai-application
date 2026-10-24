import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ui import build_ui

def main() -> None:
    """Entry point script for launching the application."""
    demo = build_ui()
    demo.launch()
    
if __name__ == "__main__":
    main()
