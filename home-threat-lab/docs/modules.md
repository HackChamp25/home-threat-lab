::: home_threat_lab.foo

# Home Threat Lab Sensor Modules

This document provides detailed descriptions of all modules inside the `htl_sensor` folder, including their classes, methods, arguments, and functionality.

---

## 1. `alerts.py`

### `AlertManager`
Manages alert creation, suppression, persistence, and notification.

- **`__init__(self, alerts_file: Path | str = None, suppression_seconds: int = 10, logger: Optional[logging.Logger] = None)`**
  - Initializes the alert manager, loads alerts from file, sets up suppression logic, and logging.
  - Arguments:
    - `alerts_file`: Path to the alerts JSON file.
    - `suppression_seconds`: Time window to suppress duplicate alerts.
    - `logger`: Optional logger instance.
- **`_save_alerts(self)`**
  - Saves the current alerts list to disk.
- **`_should_suppress(self, device: str, alert_type: str) -> bool`**
  - Checks if an alert for a device/type should be suppressed based on time.
  - Arguments:
    - `device`: Device identifier (MAC or hostname).
    - `alert_type`: Type of alert.
  - Returns: `True` if suppressed, else `False`.
- **`raise_alert(self, device: str, alert_type: str, mac: str, description: str, recommendation: str, ip: Optional[str], severity: str = "medium", evidence: Optional[dict] = None, hostname: Optional[str] = None)`**
  - Creates and persists an alert unless suppressed. Logs with appropriate severity.
  - Arguments:
    - `device`, `alert_type`, `mac`, `description`, `recommendation`, `ip`, `severity`, `evidence`, `hostname`.
- **`get_alerts(self)`**
  - Returns the current list of alerts.
- **`notify_via_telegram(self, *args, **kwargs)`**
  - Placeholder for future Telegram notification integration.

---

## 2. `inventory.py`

### `Inventory`
Manages device inventory and DNS logs.

- **`__init__(self, filepath=config.INVENTORY_FILE)`**
  - Loads inventory from file.
  - Arguments:
    - `filepath`: Path to the inventory JSON file.
- **`_load_inventory(self)`**
  - Reads inventory JSON from disk. Returns a dictionary of devices.
- **`save(self)`**
  - Saves the current inventory to disk.
- **`update_device(self, mac, ip=None, dns=None)`**
  - Updates or creates a device entry with MAC, IP, and timestamps.
  - Arguments:
    - `mac`: Device MAC address.
    - `ip`: Device IP address (optional).
    - `dns`: DNS info (optional, now deprecated).
  - Returns: Updated device dictionary.
- **`add_dns_query(self, mac, ip=None, dns_info=None)`**
  - Adds a DNS query log to a device. Creates device entry if missing.
  - Arguments:
    - `mac`: Device MAC address.
    - `ip`: Source IP for DNS query.
    - `dns_info`: Dictionary with DNS query details (`query`, `qtype`, `rcode`, `answers`, `ttls`).

---

## 3. `packet_handler.py`

### `Packethandler`
Handles packet extraction, inventory updates, and rule application.

- **`__init__(self, logger=None)`**
  - Initializes inventory, logger, and rule engine.
- **`extract_packet_info(self, packet)`**
  - Extracts MAC, IP, and DNS info from a Scapy packet.
  - Arguments:
    - `packet`: Scapy packet object.
  - Returns: Tuple `(mac, ip, dns_info)`.
- **`_handle_inventory(self, mac: str, ip: str)`**
  - Updates inventory for a device and raises alert if new.
  - Arguments:
    - `mac`: Device MAC address.
    - `ip`: Device IP address.
  - Returns: Device info dictionary.
- **`_handle_dns(self, mac: str, ip: str, dns_info: dict, device_info: dict)`**
  - Adds DNS query to inventory and applies rules.
  - Arguments:
    - `mac`, `ip`, `dns_info`, `device_info`.
- **`handle_packet(self, packet: Packet)`**
  - Main entry point: extracts info, updates inventory, handles DNS.
  - Arguments:
    - `packet`: Scapy packet object.

---

## 4. `sensor.py`

### `HomeThreatLabSensor`
Main sensor class for packet capture and processing.

- **`__init__(self, alerts_file=None, logger=None)`**
  - Initializes logger and packet handler.
  - Arguments:
    - `alerts_file`: Path to alerts file (optional).
    - `logger`: Logger instance (optional).
- **`packet_handler(self, packet)`**
  - Passes packet to handler for processing.
  - Arguments:
    - `packet`: Scapy packet object.
- **`run(self, iface=None)`**
  - Starts packet sniffing on the specified interface.
  - Arguments:
    - `iface`: Network interface name (optional).

---

## 5. `capture.py`

- **`main()`**
  - Command-line entry point for running the sensor. Handles argument parsing, logging setup, and sensor startup.
  - Arguments: None (uses argparse for CLI options).

---

## 6. `logging_config.py`

- **`setup_logging(level=logging.INFO, logfile: Path | str = None)`**
  - Configures logging for console and rotating file. Returns a logger instance.
  - Arguments:
    - `level`: Logging level (default INFO).
    - `logfile`: Path to log file (optional).
  - Returns: Logger instance for the application.

---

## 7. `rule_engine.py`

### `RuleEngine`
Applies custom rules to DNS queries and raises alerts.

- **`__init__(self, logger=None)`**
  - Initializes alert manager, logger, and NXDOMAIN tracking.
  - Arguments:
    - `logger`: Logger instance (optional).
- **`apply_rules(self, mac, ip, dns_info)`**
  - Applies all rules to DNS info, tracks NXDOMAIN counts, and raises alerts if rules trigger.
  - Arguments:
    - `mac`: Device MAC address.
    - `ip`: Device IP address.
    - `dns_info`: Dictionary with DNS query details.

---

## 8. `config.py`

Defines configuration constants for file paths and directories. No classes or methods, just variables:
- `INVENTORY_FILE`: Path to inventory JSON file.
- `ALERTS_FILE`: Path to alerts JSON file.
- `LOG_FILE`: Path to log file.
- `DATA_DIR`, `LOG_DIR`, etc.

---

## 9. `utils/file_utils.py`

Provides utility functions for safe JSON file operations.

- **`load_json(filepath: str, default=None)`**
  - Safely loads a JSON file from disk.
  - Arguments:
    - `filepath`: Path to the JSON file.
    - `default`: Value to return if file does not exist or cannot be loaded (default is None).
  - Returns: Parsed JSON data (dict or list). If the file does not exist, returns `default` or an empty dict.
  - Details: Checks for file existence, opens and parses JSON, returns default if missing.

- **`save_json(filepath: str, data: dict)`**
  - Writes a dictionary to a JSON file with pretty formatting.
  - Arguments:
    - `filepath`: Path to the JSON file.
    - `data`: Dictionary to write.
  - Details: Overwrites the file, formats with indentation for readability.

---

## 10. `utils/time_utils.py`

Provides utility functions for time handling and formatting.

- **`current_time()`**
  - Returns the current time as an ISO formatted string.
  - Arguments: None.
  - Returns: String in ISO 8601 format (e.g., `2025-10-05T14:23:45.123456`).
  - Details: Uses Python's `datetime.now().isoformat()` for consistent timestamping across modules.

---

## 11. `utils/rules.py`

Defines detection rules for suspicious network and DNS activity. These rules are used by the RuleEngine to analyze packets and DNS queries for threats.

- **`suspecious_dns_length(dns_info, threshold=50)`**
  - Checks if a DNS query string is unusually long (possible DGA/malware).
  - Arguments:
    - `dns_info`: Dictionary with DNS query details.
    - `threshold`: Length above which a query is considered suspicious (default 50).
  - Returns: Alert dictionary if triggered, else None.

- **`excessive_nxdomain(dns_info, rcode, failure_count, threshold=5)`**
  - Detects excessive NXDOMAIN DNS failures (possible beaconing or misconfiguration).
  - Arguments:
    - `dns_info`: DNS info dictionary.
    - `rcode`: DNS response code.
    - `failure_count`: Number of consecutive failures.
    - `threshold`: Failure count to trigger alert (default 5).
  - Returns: Alert dictionary if triggered, else None.

- **`unusual_port(packet)`**
  - Flags traffic on uncommon ports (not 53, 80, 443).
  - Arguments:
    - `packet`: Scapy packet object.
  - Returns: Alert dictionary if triggered, else None.

- **`suspicious_evil_domain(dns_info)`**
  - Detects DNS queries ending with `.evil.` (example of suspicious domain).
  - Arguments:
    - `dns_info`: DNS info dictionary.
  - Returns: Alert dictionary if triggered, else None.

- **`RULES`**
  - List of all rule functions to be applied by the RuleEngine.

---

These rules are essential for automated threat detection in the Home Threat Lab system. They are designed to be extensible and can be customized for additional threat scenarios.

---

**Note:**
- Utility modules (e.g., `utils/file_utils.py`, `utils/time_utils.py`,`utils/rules.py`) provide helper functions for JSON, time handling and rules to detect/raise alerts.
- Each module is designed for extensibility and integration in the Home Threat Lab system.

---

For further details, see the source code or ask for specific docstring-style documentation for any method.
