from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
from scapy.layers.dns import DNS, DNSQR
from scapy.packet import Packet
from inventory import Inventory
from rule_engine import RuleEngine

class Packethandler:
    """Handles network packets: extraction, inventory update and alerts"""

    def __init__(self,logger=None):
        self.inventory = Inventory()
        self.logger = logger
        self.rule_engine = RuleEngine()

    def extract_packet_info(self,packet):
        mac = ip = dns_info = None

        if Ether in packet:
            mac = packet[Ether].src

        if IP in packet:
            ip = packet[IP].src

        if packet.haslayer(DNS) and packet.haslayer(DNSQR):
            query = packet[DNSQR].qname.decode("utf-8", errors="ignore")
            qtype = packet[DNSQR].qtype
            rcode = packet[DNS].rcode

            # Collect answers (if any)
            answers = []
            ttls = []
            if packet[DNS].ancount > 0:
                for i in range(packet[DNS].ancount):
                    ans = packet[DNS].an[i]
                    if isinstance(ans, DNSQR):
                        answers.append(ans.rdata if hasattr(ans, "rdata") else str(ans))
                        ttls.append(ans.ttl if hasattr(ans, "ttl") else None)

            dns_info = {
                "query": query,
                "qtype": qtype,
                "rcode": rcode,
                "answers": answers,
                "ttls": ttls,
            }

        return mac, ip, dns_info
    
    def _handle_inventory(self, mac: str, ip: str):
        device_info = None
        if self.inventory:
            device_info = self.inventory.update_device(mac, ip)

            if device_info.get("new", False):
                self.alert_manager.raise_alert(
                    mac=mac,
                    ip=ip,
                    alert_type="new_device",
                    description="A new device has joined the network",
                    recommendation="Verify ownership. If unknown, secure your Wi-Fi immediately.",
                    severity="medium",
                    evidence={"first_seen": device_info["first_seen"]},
                    hostname=device_info.get("hostname"),
                )
        return device_info

    # -------------------------------
    # DNS handler
    # -------------------------------
    def _handle_dns(self, mac: str, ip: str, dns_info: dict, device_info: dict):
        if self.inventory:
            self.inventory.add_dns_query(mac,ip, dns_info)
        self.rule_engine.apply_rules(mac, ip, dns_info)

    # -------------------------------
    # Main entry point
    # -------------------------------
    def handle_packet(self, packet: Packet):
        mac, ip, dns_info = self.extract_packet_info(packet)
        if not mac:
            return  # skip malformed packet

        device_info = self._handle_inventory(mac, ip)

        if dns_info:
            self._handle_dns(mac, ip, dns_info, device_info)
