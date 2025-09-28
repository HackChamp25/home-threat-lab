from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR/ "data"
LOG_DIR = BASE_DIR/ "logs"

INVENTORY_FILE = DATA_DIR/ "inventory.json"
ALERTS_FILE = DATA_DIR/ "alert.json"
LOG_FILE = LOG_DIR/ "sensor.log"


