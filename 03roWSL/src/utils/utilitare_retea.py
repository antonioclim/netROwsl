#!/usr/bin/env python3
"""
Utilitare de Rețea pentru Exerciții
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Funcții helper utilizate în exercițiile de laborator.
"""

import socket
import struct
from typing import Optional, Tuple


def creeaza_socket_broadcast(port: int) -> socket.socket:
    """
    Creează un socket UDP configurat pentru broadcast.
    
    Args:
        port: Portul pe care să asculte
        
    Returns:
        Socket configurat pentru broadcast
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('0.0.0.0', port))
    return sock


def creeaza_socket_multicast(grup: str, port: int) -> socket.socket:
    """
    Creează un socket UDP configurat pentru multicast.
    
    Args:
        grup: Adresa grupului multicast
        port: Portul pe care să asculte
        
    Returns:
        Socket înscris în grupul multicast
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    
    # Înscrie în grup
    mreq = struct.pack(
        '4s4s',
        socket.inet_aton(grup),
        socket.inet_aton('0.0.0.0')
    )
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    return sock


def trimite_broadcast(mesaj: str, port: int, adresa: str = '255.255.255.255') -> bool:
    """
    Trimite un mesaj broadcast.
    
    Args:
        mesaj: Mesajul de trimis
        port: Portul destinație
        adresa: Adresa de broadcast
        
    Returns:
        True dacă a reușit
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(mesaj.encode(), (adresa, port))
        sock.close()
        return True
    except Exception:
        return False


def trimite_multicast(mesaj: str, grup: str, port: int, ttl: int = 1) -> bool:
    """
    Trimite un mesaj multicast.
    
    Args:
        mesaj: Mesajul de trimis
        grup: Adresa grupului multicast
        port: Portul destinație
        ttl: Time To Live
        
    Returns:
        True dacă a reușit
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        sock.sendto(mesaj.encode(), (grup, port))
        sock.close()
        return True
    except Exception:
        return False


def verifica_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Verifică dacă un port TCP este deschis.
    
    Args:
        host: Adresa IP sau hostname
        port: Numărul portului
        timeout: Timeout în secunde
        
    Returns:
        True dacă portul este deschis
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        rezultat = sock.connect_ex((host, port))
        sock.close()
        return rezultat == 0
    except Exception:
        return False


def obtine_ip_local() -> str:
    """
    Obține adresa IP locală.
    
    Returns:
        Adresa IP locală
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return '127.0.0.1'
