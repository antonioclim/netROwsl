#!/usr/bin/env python3
"""
Utilitare de Rețea
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă funcții helper pentru testarea conectivității și operațiuni de rețea.
"""

import socket
import subprocess
from typing import Optional, Tuple


def verifica_port_deschis(host: str, port: int, timeout: float = 2.0) -> bool:
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


def testeaza_echo_tcp(host: str, port: int, mesaj: str = "test", timeout: float = 5.0) -> Tuple[bool, str]:
    """
    Testează un serviciu echo TCP.
    
    Args:
        host: Adresa serverului
        port: Portul serverului
        mesaj: Mesajul de trimis
        timeout: Timeout în secunde
        
    Returns:
        Tuple (success, răspuns sau eroare)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        sock.sendall(mesaj.encode())
        raspuns = sock.recv(4096).decode()
        sock.close()
        
        return True, raspuns
    except socket.timeout:
        return False, "Timeout la conectare"
    except ConnectionRefusedError:
        return False, "Conexiune refuzată"
    except Exception as e:
        return False, str(e)


def trimite_udp(host: str, port: int, mesaj: str, broadcast: bool = False) -> bool:
    """
    Trimite un mesaj UDP.
    
    Args:
        host: Adresa destinație
        port: Portul destinație
        mesaj: Mesajul de trimis
        broadcast: True pentru transmisie broadcast
        
    Returns:
        True dacă a reușit
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        if broadcast:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        sock.sendto(mesaj.encode(), (host, port))
        sock.close()
        return True
    except Exception:
        return False


def ping(host: str, numar_pachete: int = 3, timeout: int = 5) -> Tuple[bool, str]:
    """
    Execută un ping către un host.
    
    Args:
        host: Adresa IP sau hostname
        numar_pachete: Numărul de pachete ICMP
        timeout: Timeout în secunde
        
    Returns:
        Tuple (success, output)
    """
    try:
        # Detectează sistemul de operare pentru parametrii corecți
        import platform
        param_numar = "-n" if platform.system().lower() == "windows" else "-c"
        
        rezultat = subprocess.run(
            ["ping", param_numar, str(numar_pachete), host],
            capture_output=True,
            timeout=timeout * numar_pachete + 5
        )
        
        output = rezultat.stdout.decode() + rezultat.stderr.decode()
        return rezultat.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Timeout expirat"
    except Exception as e:
        return False, str(e)


def rezolva_hostname(hostname: str) -> Optional[str]:
    """
    Rezolvă un hostname la adresa IP.
    
    Args:
        hostname: Numele de host
        
    Returns:
        Adresa IP sau None dacă nu s-a putut rezolva
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def obtine_adresa_locala() -> str:
    """
    Obține adresa IP locală a mașinii.
    
    Returns:
        Adresa IP locală
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        adresa = sock.getsockname()[0]
        sock.close()
        return adresa
    except Exception:
        return "127.0.0.1"


def verifica_multicast_support() -> bool:
    """
    Verifică dacă sistemul suportă multicast.
    
    Returns:
        True dacă multicast-ul este suportat
    """
    try:
        import struct
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Încearcă să se alăture unui grup multicast de test
        mreq = struct.pack(
            '4s4s',
            socket.inet_aton('224.0.0.1'),
            socket.inet_aton('0.0.0.0')
        )
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.close()
        return True
    except Exception:
        return False
