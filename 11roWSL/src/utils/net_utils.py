#!/usr/bin/env python3
"""
Utilitare de Rețea pentru Exerciții
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Funcții helper pentru operațiuni de rețea la nivel de socket.
"""

import socket
from typing import Optional


def creeaza_socket_tcp(timeout: float = 5.0) -> socket.socket:
    """
    Creează un socket TCP configurat.
    
    Args:
        timeout: Timeout în secunde
    
    Returns:
        Socket TCP configurat
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    return sock


def creeaza_socket_udp(timeout: float = 5.0) -> socket.socket:
    """
    Creează un socket UDP configurat.
    
    Args:
        timeout: Timeout în secunde
    
    Returns:
        Socket UDP configurat
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    return sock


def verifica_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Verifică dacă un port este deschis.
    
    Args:
        host: Adresa gazdei
        port: Numărul portului
        timeout: Timeout în secunde
    
    Returns:
        True dacă portul răspunde
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def obtine_ip_local() -> str:
    """
    Obține adresa IP locală a mașinii.
    
    Returns:
        Adresa IP locală
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def rezolva_hostname(hostname: str) -> Optional[str]:
    """
    Rezolvă un hostname la adresa IP.
    
    Args:
        hostname: Numele de gazdă
    
    Returns:
        Adresa IP sau None dacă rezolvarea eșuează
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None
