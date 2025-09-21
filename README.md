# 🛡️ Home Threat Lab (HTL) – Network Sensor

HTL is a lightweight Python-based project to passively monitor your **home network**.  
It captures packets, builds a device inventory, and (soon) will generate alerts with plain-language explanations.  

This project is designed as a **learning tool** — small scope, but strong fundamentals: networking, packet analysis, detection logic, and logging.


## 🚀 How It Works

1. **Start Capture**
   ```bash
   python capture.py --iface "Wi-Fi"
   

flowchart TD
    A[Run capture.py] --> B[Parse CLI args (--iface)]
    B --> C[Setup logging (logger_config.py)]
    C --> D[Load inventory.json]
    D --> E[Start packet sniffing (Scapy)]
    E --> F[packet_handler()]
    F --> G[Update inventory.json]
    F --> H[Alert Manager (future)]
    H --> I[alerts.json]
