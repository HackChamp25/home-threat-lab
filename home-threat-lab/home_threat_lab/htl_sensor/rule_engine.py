from utils import rules
from alerts import AlertManager

class RuleEngine:
    def __init__(self,logger=None):
        self.alertmanager = AlertManager(logger=logger)
        self.logger = logger
        self.nxdomain_count = {}

    def apply_rules(self, mac, ip, dns_info):
        #Track NXDOMAIN counts
        if dns_info.get("rcode",0)!=0:
            self.nxdomain_count[mac] = self.nxdomain_count.get(mac,0)+1
        else:
            self.nxdomain_count[mac] = 0
        
        for rule in rules.RULES:
            try:
                if rule.__name__ == "excessive_nxdomain":
                    alert = rule(dns_info, dns_info.get("rcode",0),self.nxdomain_count.get(mac,0))
                else:
                    alert = rule(dns_info)
                if alert:
                    self.alertmanager.raise_alert(
                        mac=mac,
                        device=mac,
                        ip=ip,
                        alert_type=alert["type"],
                        description=alert["description"],
                        recommendation=alert["recommendation"],
                        severity=alert["severity"],
                        evidence=dns_info
                    )
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Rule {rule.__name__} failed: {e}")