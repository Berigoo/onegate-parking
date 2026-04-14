import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback if python-dotenv not installed
    pass

OPI_ZERO = os.getenv('OPI_ZERO', 'false').lower() in ('true', '1', 'yes')
