import sys
import argparse
import logging
from sensor import HomeThreatLabSensor
from logging_config import setup_logging


def main():
    parser = argparse.ArgumentParser(description="Home Threat Lab sensor")
    parser.add_argument("--iface", help="Interface to listen on", default=None)
    parser.add_argument("--alerts", help="Alerts file path (optional)", default=None)
    parser.add_argument("--log-level", help="Log level", default="INFO")
    args = parser.parse_args()

    #iface = sys.argv[1] if len(sys.argv) > 1 else None
    level=getattr(__import__("logging"), args.log_level.upper(), logging.INFO) if args.log_level else logging.INFO
    logger = setup_logging(level=level)
    sensor = HomeThreatLabSensor(alerts_file=args.alerts, logger=logger)
    sensor.run(iface=args.iface)


if __name__ == "__main__":
    main()