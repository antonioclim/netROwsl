"""
================================================================================
Exerciții de Laborator - Săptămâna 13
================================================================================
IoT și Securitate în Rețelele de Calculatoare

Exerciții disponibile:

    ex_13_01_scanner_porturi
        Scanner TCP pentru recunoașterea serviciilor de rețea.
        Funcționalități: scanare concurentă, banner grabbing, export JSON.
        Utilizare: python3 ex_13_01_scanner_porturi.py --tinta localhost --porturi 1-1024

    ex_13_02_client_mqtt
        Client MQTT cu suport pentru TLS și diferite niveluri QoS.
        Funcționalități: subscribe, publish, conexiuni securizate.
        Utilizare: python3 ex_13_02_client_mqtt.py --mod subscribe --topic "test/#"

    ex_13_03_sniffer_pachete
        Sniffer de pachete de rețea folosind biblioteca Scapy.
        Funcționalități: captură live, filtrare BPF, export PCAP.
        Utilizare: sudo python3 ex_13_03_sniffer_pachete.py --numar 20

    ex_13_04_verificator_vulnerabilitati
        Verificator de vulnerabilități pentru servicii de rețea.
        Funcționalități: audit FTP, MQTT, HTTP; raportare severități.
        Utilizare: python3 ex_13_04_verificator_vulnerabilitati.py --tinta localhost --toate

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
================================================================================
"""

__all__ = [
    "ex_13_01_scanner_porturi",
    "ex_13_02_client_mqtt",
    "ex_13_03_sniffer_pachete",
    "ex_13_04_verificator_vulnerabilitati",
]
