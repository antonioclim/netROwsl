#!/usr/bin/env python3
"""
Utilitare comune pentru aplicații de rețea - Săptămâna 6

Acest modul consolidează funcționalitățile comune pentru a evita
duplicarea codului între diferite aplicații client-server.

Planul de porturi Săptămâna 6:
    TCP_APP_PORT = 9090
    UDP_APP_PORT = 9091
    WEEK_PORT_BASE = 5600 (pentru porturi personalizate)
    WEEK_PORT_RANGE = 5600..5699

Planul de IP-uri Săptămâna 6:
    SUBNET = 10.0.6.0/24
    GATEWAY = 10.0.6.1
    H1 = 10.0.6.11
    H2 = 10.0.6.12
    H3 = 10.0.6.13
    SERVER = 10.0.6.100

ing. dr. Antonio Clim | Licență MIT | ASE-CSIE 2025-2026
"""

from __future__ import annotations

import argparse
import logging
import socket
import sys
from dataclasses import dataclass
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_SAPTAMANA_6
# ═══════════════════════════════════════════════════════════════════════════════

SAPTAMANA = 6

# Plan IP
SUBRETEA = f"10.0.{SAPTAMANA}.0/24"
GATEWAY = f"10.0.{SAPTAMANA}.1"
H1_IP = f"10.0.{SAPTAMANA}.11"
H2_IP = f"10.0.{SAPTAMANA}.12"
H3_IP = f"10.0.{SAPTAMANA}.13"
SERVER_IP = f"10.0.{SAPTAMANA}.100"

# Plan porturi (evită privilegii root)
TCP_APP_PORT = 9090
UDP_APP_PORT = 9091
HTTP_PORT = 8080
PROXY_PORT = 8888
DNS_PORT = 5353
FTP_PORT = 2121
SSH_PORT = 2222
CONTROLLER_PORT = 6633

# Porturi personalizate pentru Săptămâna 6
WEEK_PORT_BASE = 5100 + 100 * (SAPTAMANA - 1)  # 5600
WEEK_PORT_RANGE = range(WEEK_PORT_BASE, WEEK_PORT_BASE + 100)

# Timeout-uri implicite
TIMEOUT_IMPLICIT = 5
DIMENSIUNE_BUFFER_IMPLICIT = 4096


# ═══════════════════════════════════════════════════════════════════════════════
# JURNALIZARE
# ═══════════════════════════════════════════════════════════════════════════════

def configureaza_logging(
    nume: str = "aplicatie_retea",
    nivel: int = logging.INFO,
    format_msg: str = "[%(asctime)s] %(levelname)s: %(message)s"
) -> logging.Logger:
    """
    Configurează jurnalizare consecventă pentru aplicații.
    
    Creează un logger cu handler pentru stdout și formatare standardizată.
    Dacă logger-ul are deja handlere, nu adaugă altele noi.
    
    Args:
        nume: Numele logger-ului (folosit pentru identificare în loguri)
        nivel: Nivelul de jurnalizare (implicit: INFO)
        format_msg: Formatul mesajului de log
    
    Returns:
        Logger configurat și gata de folosit
    
    Example:
        >>> logger = configureaza_logging("server_tcp")
        >>> logger.info("Serverul a pornit pe portul 9090")
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(format_msg, datefmt="%H:%M:%S"))
        logger.addHandler(handler)
    
    return logger


# ═══════════════════════════════════════════════════════════════════════════════
# AJUTOARE_SOCKET
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ConfigSocket:
    """
    Configurare pentru crearea socket-urilor.
    
    Attributes:
        host: Adresa de bind/conectare (implicit: 0.0.0.0 pentru toate interfețele)
        port: Portul de folosit (implicit: TCP_APP_PORT)
        timeout: Timeout pentru operații în secunde (0 = fără timeout)
        dimensiune_buffer: Dimensiunea buffer-ului de recepție în bytes
        refoloseste_adresa: Permite refolosirea imediată a adresei (SO_REUSEADDR)
    """
    host: str = "0.0.0.0"
    port: int = TCP_APP_PORT
    timeout: float = TIMEOUT_IMPLICIT
    dimensiune_buffer: int = DIMENSIUNE_BUFFER_IMPLICIT
    refoloseste_adresa: bool = True


def creeaza_socket_tcp(config: Optional[ConfigSocket] = None) -> socket.socket:
    """
    Creează un socket TCP configurat.
    
    Socket-ul este creat cu opțiunile specificate în config.
    Dacă config nu este furnizat, se folosesc valorile implicite.
    
    Args:
        config: Configurare socket (opțional, se folosesc implicit valorile din ConfigSocket)
    
    Returns:
        Socket TCP (SOCK_STREAM) configurat și gata de bind/connect
    
    Example:
        >>> sock = creeaza_socket_tcp()
        >>> sock.bind(("0.0.0.0", 9090))
        >>> sock.listen(5)
    """
    if config is None:
        config = ConfigSocket()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if config.refoloseste_adresa:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    if config.timeout > 0:
        sock.settimeout(config.timeout)
    
    return sock


def creeaza_socket_udp(config: Optional[ConfigSocket] = None) -> socket.socket:
    """
    Creează un socket UDP configurat.
    
    Socket-ul este creat cu opțiunile specificate în config.
    Portul implicit pentru UDP este UDP_APP_PORT (9091).
    
    Args:
        config: Configurare socket (opțional)
    
    Returns:
        Socket UDP (SOCK_DGRAM) configurat și gata de bind
    
    Example:
        >>> sock = creeaza_socket_udp()
        >>> sock.bind(("0.0.0.0", 9091))
        >>> data, addr = sock.recvfrom(4096)
    """
    if config is None:
        config = ConfigSocket(port=UDP_APP_PORT)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    if config.refoloseste_adresa:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    if config.timeout > 0:
        sock.settimeout(config.timeout)
    
    return sock


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDARE
# ═══════════════════════════════════════════════════════════════════════════════

def este_ip_valid(ip: str) -> bool:
    """
    Verifică dacă un string este o adresă IPv4 validă.
    
    Args:
        ip: String-ul de verificat (ex: "192.168.1.1")
    
    Returns:
        True dacă este o adresă IPv4 validă, False altfel
    """
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def este_port_valid(port: int) -> bool:
    """
    Verifică dacă un port este în intervalul valid (1-65535).
    
    Args:
        port: Numărul portului de verificat
    
    Returns:
        True dacă portul este valid, False altfel
    """
    return 1 <= port <= 65535


def este_port_saptamana(port: int) -> bool:
    """
    Verifică dacă portul este în intervalul personalizat al săptămânii.
    
    Pentru Săptămâna 6, intervalul este 5600-5699.
    
    Args:
        port: Numărul portului de verificat
    
    Returns:
        True dacă portul este în intervalul săptămânii, False altfel
    """
    return port in WEEK_PORT_RANGE


# ═══════════════════════════════════════════════════════════════════════════════
# AJUTOARE_ARGPARSE
# ═══════════════════════════════════════════════════════════════════════════════

def adauga_argumente_comune(
    parser: argparse.ArgumentParser,
    include_port: bool = True,
    include_host: bool = True
) -> None:
    """
    Adaugă argumente comune la un parser argparse.
    
    Args:
        parser: Instanță ArgumentParser la care se adaugă argumentele
        include_port: Include argumentul --port (implicit: True)
        include_host: Include argumentul --host/--bind (implicit: True)
    """
    if include_host:
        parser.add_argument(
            "--host", "--bind",
            default="0.0.0.0",
            help="Adresa de bind/conectare (implicit: 0.0.0.0)"
        )
    
    if include_port:
        parser.add_argument(
            "--port", "-p",
            type=int,
            default=TCP_APP_PORT,
            help=f"Port (implicit: {TCP_APP_PORT})"
        )
    
    parser.add_argument(
        "--timeout", "-t",
        type=float,
        default=TIMEOUT_IMPLICIT,
        help=f"Timeout în secunde (implicit: {TIMEOUT_IMPLICIT})"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Output detaliat"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# INFORMATII_SAPTAMANA
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_info_saptamana() -> None:
    """
    Afișează informații despre configurarea săptămânii curente.
    
    Afișează un banner formatat cu toate constantele relevante:
    planul de IP-uri și planul de porturi pentru Săptămâna 6.
    """
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  Săptămâna {SAPTAMANA}: SDN - Rețele definite prin software       ║
╠══════════════════════════════════════════════════════════╣
║  Plan IP:                                                ║
║    Subrețea: {SUBRETEA:<20}                       ║
║    Gateway:  {GATEWAY:<20}                       ║
║    h1:       {H1_IP:<20}                       ║
║    h2:       {H2_IP:<20}                       ║
║    h3:       {H3_IP:<20}                       ║
║    Server:   {SERVER_IP:<20}                       ║
╠══════════════════════════════════════════════════════════╣
║  Plan porturi:                                           ║
║    Aplicație TCP: {TCP_APP_PORT:<10}                          ║
║    Aplicație UDP: {UDP_APP_PORT:<10}                          ║
║    Controller:    {CONTROLLER_PORT:<10}                          ║
║    Bază săptămână:{WEEK_PORT_BASE:<10} (interval: {WEEK_PORT_BASE}-{WEEK_PORT_BASE+99})║
╚══════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    afiseaza_info_saptamana()
