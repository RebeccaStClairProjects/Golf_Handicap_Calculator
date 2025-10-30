# errorHandler.py
"""
Centralized error handling utilities for database and Flask operations.
"""

import logging
from mysql.connector import Error, InterfaceError, OperationalError, ProgrammingError

# Optional: configure logging once here
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def handleDbError(e):
    """
    Standardized MySQL error handler.
    Returns a dict describing the error so Flask routes can jsonify it.
    """
    errorType = type(e).__name__

    if isinstance(e, InterfaceError):
        msg = f"MySQL interface error: {e}"
    elif isinstance(e, OperationalError):
        msg = f"MySQL operational error: {e}"
    elif isinstance(e, ProgrammingError):
        msg = f"MySQL programming error: {e}"
    elif isinstance(e, Error):
        msg = f"MySQL general error: {e}"
    else:
        msg = f"Unexpected error: {e}"

    logging.error(msg)
    return {"error": msg, "error_type": errorType}
