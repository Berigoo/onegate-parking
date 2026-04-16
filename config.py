import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback if python-dotenv not installed
    pass

OPI_ZERO = os.getenv('OPI_ZERO', 'false').lower() in ('true', '1', 'yes')
RASPI = os.getenv('RASPI', 'false').lower() in ('true', '1', 'yes')

# If running under pytest, prefer the OPi Zero GPIO mock path to allow tests
# to run without hardware access.
import os as _os
if _os.environ.get('PYTEST_CURRENT_TEST') is not None:
    OPI_ZERO = True
    RASPI = False
