import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LOG_DIR, LOG_FILE


def setup_logging(level=logging.INFO, logfile: Path | str = None):
    """
    Configure logging: console + rotating file.
    Call this once at program start.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logfile = Path(logfile) if logfile else LOG_FILE
    logfile.parent.mkdir(parents=True, exist_ok=True)

    fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    formatter = logging.Formatter(fmt)

    root = logging.getLogger()
    root.setLevel(level)

    #console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    #return a module logger convenience
    return logging.getLogger('htl_sensor')
