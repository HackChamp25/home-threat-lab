import json
import config
from utils import time_utils, file_utils

class Inventory:
    
    def __init__(self, filepath=config.INVENTORY_FILE):
        self.filepath=filepath
        self.devices = self._load_inventory()
    
    def _load_inventory(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save(self):
        self.filepath.parent.mkdir(exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self.devices, f, indent=4)
    
    def update_device(self, mac, ip=None, dns=None):
        if not mac:
            return None

        now = time_utils.current_time()
        device = self.devices.get(mac, {
            "ip": ip,
            "first_seen": now,
            "latest_seen": now,
            "dns_logs": []
        })

        # Always update IP if available
        if ip:
            device["ip"] = ip

        # Update timestamp
        device["latest_seen"] = now

        self.devices[mac] = device
        self.save()
        return device
    
    def add_dns_query(self, mac,ip=None, dns_info=None):
        """Add a DNS query to the device's dns_logs."""
        if not mac or not dns_info:
            return
        device = self.devices.get(mac)
        if not device:
            # If device not found, create a new entry
            now = time_utils.current_time()
            device = {
                "ip": None,
                "first_seen": now,
                "latest_seen": now,
                "dns_logs": []
            }
            self.devices[mac] = device
        # Append the query to dns_logs
        log_entry = {
            "ts": time_utils.current_time(),
            "src_ip": ip,
            "query": dns_info.get("query"),
            "qtype": dns_info.get("qtype"),
            "rcode": dns_info.get("rcode"),
            "answers": dns_info.get("answers", []),
            "ttls": dns_info.get("ttls", []),
        }
        device.setdefault("dns_logs", []).append(log_entry)
        device["last_seen"] = time_utils.current_time()
        self.save()