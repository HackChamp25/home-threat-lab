import logging
from scapy.all import sniff
from scapy.all import Packet
from packet_handler import Packethandler

class HomeThreatLabSensor:
    def __init__(self, alerts_file=None, logger=None):
        self.logger = logger or logging.getLogger("htl_sensor.sensor")
        self.packetHandler = Packethandler(logger=self.logger)
    
    def packet_handler(self, packet):
        self.packetHandler.handle_packet(packet)
    
    def run(self, iface=None):
        self.logger.info("Starting capture on %s", iface or "default interface")
        sniff(prn=self.packet_handler, store=False, iface=iface)