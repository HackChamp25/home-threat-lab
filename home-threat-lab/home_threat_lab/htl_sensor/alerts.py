import json
import time
import uuid
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import config
from utils.file_utils import load_json, save_json

class AlertManager:
    """
    Simple alerts managere:
        - saves alerts to a JSON file (append to list)
        - supressed duplicate alerts for same (device, type) within suppression_seconds
        - logs alerts via logging module
    """

    def __init__(self, alerts_file: Path | str=None, suppression_seconds: int=10, logger: Optional[logging.Logger]=None):
        self.alerts_file = Path(alerts_file) if alerts_file else Path(config.ALERTS_FILE)
        self.suppression_seconds = suppression_seconds
        self._logger = logger or logging.getLogger("htl_sensor.alerts")
        loaded_alerts = load_json(self.alerts_file, default=[])
        if isinstance(loaded_alerts, dict):
            self._alerts = []
        else:
            self._alerts = loaded_alerts
        self._last_alert_time: dict[tuple, float] = {}   # (device, type) --> timestamp

        self.alerts_file.parent.mkdir(parents=True, exist_ok=True)

    def _save_alerts(self):
        try:
            save_json(self.alerts_file, self._alerts)
        except Exception as e:
            self._logger.exception("Failed to save alerts to disk: %s", e)

    def _should_suppress(self, device: str, alert_type: str) -> bool:
        key = (device, alert_type)
        now = time.time()
        last = self._last_alert_time.get(key)
        if last and (now - last) < self.suppression_seconds:
            return True
        self._last_alert_time[key] = now
        return False
    
    def raise_alert(
            self, device: str, alert_type: str, mac: str,
            description: str, recommendation: str, ip: Optional[str], 
            severity: str = "medium", evidence: Optional[dict] = None, hostname : Optional[str]=None
    ):
        """Create and persist an alert, unless suppressed."""
        if self._should_suppress(device, alert_type):
            self._logger.debug("Suppressed duplicate alert %s for %s", alert_type, device)
            return

        alert = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat() + "z",
            "mac": mac,
            "ip": ip,
            "device": device,
            "type": alert_type,
            "severity": severity,
            "description": description,
            "recommendation": recommendation,
            "evidence": evidence or {}
        }

        #Log with appropriate level
        if severity.lower() in ("critical", "high"):
            self._logger.error("ALERT %s %s: %s", alert_type, device, description)
        elif severity.lower() == "medium":
            self._logger.warning("ALERT %s %s: %s", alert_type, device, description)
        else:
            self._logger.info("ALERT %s %s: %s", alert_type, device, description)
            
        self._alerts.append(alert)
        self._save_alerts()
    
    def get_alerts(self):
        return self._alerts

    def notify_via_telegram(self, *args, **kwargs):
        self._logger.debug("Notify via telegram is yet to be completed")

        