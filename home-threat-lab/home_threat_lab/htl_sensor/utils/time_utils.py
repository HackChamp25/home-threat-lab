from datetime import  datetime

def current_time():
    """Return ISO formatted current time string"""
    return datetime.now().isoformat()

