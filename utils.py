# utils.py
def safe_float(value, default=None):
    """Convert input to float safely."""
    try:
        return float(value)
    except:
        return default
