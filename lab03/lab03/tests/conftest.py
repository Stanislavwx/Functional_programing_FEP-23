import sys
from pathlib import Path

# Ensure project root is importable when running pytest from inside tests/
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
