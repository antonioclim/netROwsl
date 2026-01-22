"""
Module utilitare pentru programarea socket-urilor.
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Funcții disponibile:
- Creare socket-uri TCP și UDP
- Parsare și formatare adrese
- Verificare porturi disponibile
- Măsurare RTT
- Funcții pentru protocol cu lungime prefixată
- Calcul și verificare checksum
"""

from src.utils.net_utils import (
    creează_socket_tcp,
    creează_socket_udp,
    parsează_adresă,
    formatează_adresă,
    port_disponibil,
    găsește_port_liber,
    măsoară_rtt_tcp,
    măsoară_rtt_udp,
    trimite_cu_lungime,
    primește_cu_lungime,
    calculează_checksum,
    verifică_checksum,
)

__all__ = [
    # Creare socket-uri
    "creează_socket_tcp",
    "creează_socket_udp",
    # Adrese
    "parsează_adresă",
    "formatează_adresă",
    # Porturi
    "port_disponibil",
    "găsește_port_liber",
    # Măsurători
    "măsoară_rtt_tcp",
    "măsoară_rtt_udp",
    # Protocol cu lungime
    "trimite_cu_lungime",
    "primește_cu_lungime",
    # Checksum
    "calculează_checksum",
    "verifică_checksum",
]
