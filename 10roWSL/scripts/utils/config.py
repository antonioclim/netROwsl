#!/usr/bin/env python3
"""
Configurație Centralizată pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Încarcă configurația din fișierul .env dacă există,
altfel folosește valorile implicite documentate.

Utilizare:
    from scripts.utils.config import config
    
    print(config.PORTAINER_URL)
    print(config.SSH_USER)
"""

import os
from pathlib import Path
from typing import Optional

# Încearcă să încarce python-dotenv dacă e disponibil
try:
    from dotenv import load_dotenv
    
    # Caută .env în rădăcina proiectului (10roWSL/)
    _radacina = Path(__file__).parent.parent.parent
    _env_path = _radacina / ".env"
    
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    # python-dotenv nu e instalat - folosim doar variabilele de mediu
    pass


class ConfigLab:
    """
    Configurație centralizată pentru laboratorul de rețele.
    
    Valorile pot fi suprascrise prin:
    1. Variabile de mediu (ex: export PORTAINER_PORT=9001)
    2. Fișier .env în rădăcina proiectului
    
    Attributes:
        PORTAINER_USER: Utilizator Portainer (implicit: stud)
        PORTAINER_PASS: Parolă Portainer (implicit: studstudstud)
        PORTAINER_PORT: Port Portainer (implicit: 9000)
        SSH_USER: Utilizator SSH laborator (implicit: labuser)
        SSH_PASS: Parolă SSH laborator (implicit: labpass)
        SSH_PORT: Port SSH laborator (implicit: 2222)
        FTP_USER: Utilizator FTP laborator (implicit: labftp)
        FTP_PASS: Parolă FTP laborator (implicit: labftp)
        FTP_PORT: Port FTP laborator (implicit: 2121)
        FTP_PASSIVE_START: Început interval porturi pasive FTP (implicit: 30000)
        FTP_PASSIVE_END: Sfârșit interval porturi pasive FTP (implicit: 30009)
        WEB_PORT: Port server web HTTP (implicit: 8000)
        DNS_PORT: Port server DNS (implicit: 5353)
        HTTPS_PORT: Port server HTTPS pentru exerciții (implicit: 4443)
        REST_PORT: Port server REST pentru exerciții (implicit: 5000)
        LAB_SUBNET: Subnet rețea laborator (implicit: 172.20.0.0/24)
        LAB_GATEWAY: Gateway rețea laborator (implicit: 172.20.0.1)
    """
    
    # ═══════════════════════════════════════════════════════════════
    # PORTAINER (Management Docker - rulează global)
    # ═══════════════════════════════════════════════════════════════
    PORTAINER_USER: str = os.getenv("PORTAINER_USER", "stud")
    PORTAINER_PASS: str = os.getenv("PORTAINER_PASS", "studstudstud")
    PORTAINER_PORT: int = int(os.getenv("PORTAINER_PORT", "9000"))
    
    # ═══════════════════════════════════════════════════════════════
    # SSH SERVER
    # ═══════════════════════════════════════════════════════════════
    SSH_USER: str = os.getenv("SSH_USER", "labuser")
    SSH_PASS: str = os.getenv("SSH_PASS", "labpass")
    SSH_PORT: int = int(os.getenv("SSH_PORT", "2222"))
    
    # ═══════════════════════════════════════════════════════════════
    # FTP SERVER
    # ═══════════════════════════════════════════════════════════════
    FTP_USER: str = os.getenv("FTP_USER", "labftp")
    FTP_PASS: str = os.getenv("FTP_PASS", "labftp")
    FTP_PORT: int = int(os.getenv("FTP_PORT", "2121"))
    FTP_PASSIVE_START: int = int(os.getenv("FTP_PASSIVE_START", "30000"))
    FTP_PASSIVE_END: int = int(os.getenv("FTP_PASSIVE_END", "30009"))
    
    # ═══════════════════════════════════════════════════════════════
    # SERVICII LABORATOR
    # ═══════════════════════════════════════════════════════════════
    WEB_PORT: int = int(os.getenv("WEB_PORT", "8000"))
    DNS_PORT: int = int(os.getenv("DNS_PORT", "5353"))
    HTTPS_PORT: int = int(os.getenv("HTTPS_PORT", "4443"))
    REST_PORT: int = int(os.getenv("REST_PORT", "5000"))
    
    # ═══════════════════════════════════════════════════════════════
    # REȚEA LABORATOR
    # ═══════════════════════════════════════════════════════════════
    LAB_SUBNET: str = os.getenv("LAB_SUBNET", "172.20.0.0/24")
    LAB_GATEWAY: str = os.getenv("LAB_GATEWAY", "172.20.0.1")
    LAB_NETWORK_NAME: str = os.getenv("LAB_NETWORK_NAME", "week10_labnet")
    
    # ═══════════════════════════════════════════════════════════════
    # IP-URI CONTAINERE
    # ═══════════════════════════════════════════════════════════════
    IP_WEB: str = os.getenv("IP_WEB", "172.20.0.10")
    IP_DNS: str = os.getenv("IP_DNS", "172.20.0.53")
    IP_SSH: str = os.getenv("IP_SSH", "172.20.0.22")
    IP_FTP: str = os.getenv("IP_FTP", "172.20.0.21")
    IP_DEBUG: str = os.getenv("IP_DEBUG", "172.20.0.200")
    IP_SSH_CLIENT: str = os.getenv("IP_SSH_CLIENT", "172.20.0.100")
    
    # ═══════════════════════════════════════════════════════════════
    # PROPRIETĂȚI DERIVATE
    # ═══════════════════════════════════════════════════════════════
    
    @classmethod
    def portainer_url(cls) -> str:
        """Returnează URL-ul complet pentru Portainer."""
        return f"http://localhost:{cls.PORTAINER_PORT}"
    
    @classmethod
    def web_url(cls) -> str:
        """Returnează URL-ul serverului web HTTP."""
        return f"http://localhost:{cls.WEB_PORT}"
    
    @classmethod
    def https_url(cls) -> str:
        """Returnează URL-ul serverului HTTPS."""
        return f"https://localhost:{cls.HTTPS_PORT}"
    
    @classmethod
    def rest_url(cls) -> str:
        """Returnează URL-ul serverului REST."""
        return f"http://localhost:{cls.REST_PORT}"
    
    @classmethod
    def ssh_connection_string(cls) -> str:
        """Returnează string-ul de conexiune SSH."""
        return f"{cls.SSH_USER}@localhost -p {cls.SSH_PORT}"
    
    @classmethod
    def ftp_passive_range(cls) -> str:
        """Returnează intervalul de porturi pasive FTP."""
        return f"{cls.FTP_PASSIVE_START}-{cls.FTP_PASSIVE_END}"
    
    @classmethod
    def to_dict(cls) -> dict:
        """Returnează configurația ca dicționar."""
        return {
            "portainer": {
                "user": cls.PORTAINER_USER,
                "port": cls.PORTAINER_PORT,
                "url": cls.portainer_url()
            },
            "ssh": {
                "user": cls.SSH_USER,
                "port": cls.SSH_PORT
            },
            "ftp": {
                "user": cls.FTP_USER,
                "port": cls.FTP_PORT,
                "passive_range": cls.ftp_passive_range()
            },
            "services": {
                "web_port": cls.WEB_PORT,
                "dns_port": cls.DNS_PORT,
                "https_port": cls.HTTPS_PORT,
                "rest_port": cls.REST_PORT
            },
            "network": {
                "subnet": cls.LAB_SUBNET,
                "gateway": cls.LAB_GATEWAY,
                "name": cls.LAB_NETWORK_NAME
            }
        }
    
    @classmethod
    def afiseaza_configuratie(cls):
        """Afișează configurația curentă în format tabelar."""
        print()
        print("=" * 50)
        print("  CONFIGURAȚIE LABORATOR SĂPTĂMÂNA 10")
        print("=" * 50)
        print()
        print("  Portainer:")
        print(f"    URL:        {cls.portainer_url()}")
        print(f"    Utilizator: {cls.PORTAINER_USER}")
        print()
        print("  SSH:")
        print(f"    Port:       {cls.SSH_PORT}")
        print(f"    Utilizator: {cls.SSH_USER}")
        print()
        print("  FTP:")
        print(f"    Port:       {cls.FTP_PORT}")
        print(f"    Utilizator: {cls.FTP_USER}")
        print(f"    Pasive:     {cls.ftp_passive_range()}")
        print()
        print("  Servicii:")
        print(f"    Web HTTP:   localhost:{cls.WEB_PORT}")
        print(f"    DNS:        localhost:{cls.DNS_PORT}/udp")
        print(f"    HTTPS:      localhost:{cls.HTTPS_PORT}")
        print(f"    REST:       localhost:{cls.REST_PORT}")
        print()
        print("  Rețea:")
        print(f"    Subnet:     {cls.LAB_SUBNET}")
        print(f"    Gateway:    {cls.LAB_GATEWAY}")
        print()
        print("=" * 50)


# Instanță globală pentru import ușor
config = ConfigLab()


# Permite rularea directă pentru verificare
if __name__ == "__main__":
    config.afiseaza_configuratie()
