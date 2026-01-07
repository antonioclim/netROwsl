#!/usr/bin/env python3
"""
Utilitare de Rețea
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Oferă funcții pentru testarea conectivității și validarea configurațiilor de rețea.
"""

import socket
import subprocess
import re
from typing import Optional, Tuple, List
from ipaddress import ip_address, ip_network, IPv4Network, IPv4Address


def verifica_port(gazda: str, port: int, timeout: float = 2.0) -> bool:
    """
    Verifică dacă un port este deschis pe o gazdă.
    
    Args:
        gazda: Adresa IP sau hostname-ul gazdei
        port: Numărul portului de verificat
        timeout: Timpul de așteptare în secunde
    
    Returns:
        True dacă portul este deschis și răspunde
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            rezultat = sock.connect_ex((gazda, port))
            return rezultat == 0
    except (socket.error, socket.timeout):
        return False


def ping(gazda: str, numar: int = 1, timeout: int = 2) -> Tuple[bool, float]:
    """
    Efectuează un ping către o gazdă.
    
    Args:
        gazda: Adresa IP sau hostname-ul de ping-uit
        numar: Numărul de pachete ICMP de trimis
        timeout: Timeout pentru fiecare pachet în secunde
    
    Returns:
        Tuple de (succes, latență_medie_ms)
    """
    try:
        # Comandă ping diferită pentru Windows vs Linux
        import platform
        
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", str(numar), "-w", str(timeout * 1000), gazda]
            pattern_timp = r"Medie = (\d+)ms|Average = (\d+)ms"
        else:
            cmd = ["ping", "-c", str(numar), "-W", str(timeout), gazda]
            pattern_timp = r"avg[^=]*=\s*[\d.]+/([\d.]+)"
        
        rezultat = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * numar + 5)
        
        if rezultat.returncode == 0:
            # Încearcă să extragă latența
            match = re.search(pattern_timp, rezultat.stdout)
            if match:
                latenta = float(match.group(1) or match.group(2))
                return True, latenta
            return True, 0.0
        
        return False, 0.0
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return False, 0.0


def rezolva_dns(hostname: str) -> Optional[str]:
    """
    Rezolvă un hostname la o adresă IP.
    
    Args:
        hostname: Numele de domeniu de rezolvat
    
    Returns:
        Adresa IP sau None dacă rezoluția eșuează
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def valideaza_cidr(cidr: str) -> bool:
    """
    Validează o notație CIDR.
    
    Args:
        cidr: Șirul de validat (ex: "192.168.1.0/24")
    
    Returns:
        True dacă notația CIDR este validă
    """
    try:
        ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False


def valideaza_ip(adresa: str) -> bool:
    """
    Validează o adresă IP (IPv4 sau IPv6).
    
    Args:
        adresa: Adresa de validat
    
    Returns:
        True dacă adresa este validă
    """
    try:
        ip_address(adresa)
        return True
    except ValueError:
        return False


def calculeaza_info_retea(cidr: str) -> dict:
    """
    Calculează informații despre o rețea din notația CIDR.
    
    Args:
        cidr: Notația CIDR (ex: "192.168.1.0/24")
    
    Returns:
        Dicționar cu informații despre rețea
    """
    retea = ip_network(cidr, strict=False)
    
    return {
        "adresa_retea": str(retea.network_address),
        "adresa_broadcast": str(retea.broadcast_address),
        "masca": str(retea.netmask),
        "prefix": retea.prefixlen,
        "numar_total_adrese": retea.num_addresses,
        "numar_gazde_utilizabile": max(0, retea.num_addresses - 2),
        "prima_gazda": str(list(retea.hosts())[0]) if retea.num_addresses > 2 else None,
        "ultima_gazda": str(list(retea.hosts())[-1]) if retea.num_addresses > 2 else None,
        "este_privata": retea.is_private,
    }


def obtine_adresa_locala() -> Optional[str]:
    """
    Obține adresa IP locală a mașinii.
    
    Returns:
        Adresa IP locală sau None
    """
    try:
        # Creează un socket și conectează-te la un server extern
        # pentru a determina adresa locală
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except socket.error:
        return None


def scaneaza_porturi(
    gazda: str,
    port_start: int,
    port_sfarsit: int,
    timeout: float = 0.5
) -> List[int]:
    """
    Scanează o gamă de porturi pe o gazdă.
    
    Args:
        gazda: Adresa IP sau hostname-ul
        port_start: Primul port din gamă
        port_sfarsit: Ultimul port din gamă
        timeout: Timeout pentru fiecare verificare
    
    Returns:
        Lista de porturi deschise
    """
    porturi_deschise = []
    
    for port in range(port_start, port_sfarsit + 1):
        if verifica_port(gazda, port, timeout):
            porturi_deschise.append(port)
    
    return porturi_deschise


def formateaza_bytes(numar_bytes: int) -> str:
    """
    Formatează un număr de bytes într-un format citibil.
    
    Args:
        numar_bytes: Numărul de bytes
    
    Returns:
        Șir formatat (ex: "1.5 MB")
    """
    unitati = ['B', 'KB', 'MB', 'GB', 'TB']
    
    for unitate in unitati:
        if numar_bytes < 1024:
            return f"{numar_bytes:.1f} {unitate}"
        numar_bytes /= 1024
    
    return f"{numar_bytes:.1f} PB"


def calculeaza_prefix_pentru_gazde(numar_gazde: int) -> int:
    """
    Calculează prefixul minim pentru a acomoda un număr de gazde.
    
    Args:
        numar_gazde: Numărul de gazde necesare
    
    Returns:
        Lungimea prefixului CIDR
    """
    import math
    
    # Adaugă 2 pentru adresa de rețea și broadcast
    adrese_necesare = numar_gazde + 2
    
    # Calculează puterea de 2 necesară
    putere = math.ceil(math.log2(adrese_necesare))
    
    # Prefixul este 32 minus puterea
    return 32 - putere


# Alias-uri pentru compatibilitate cu versiunea în limba engleză
check_port = verifica_port
validate_cidr = valideaza_cidr
validate_ip = valideaza_ip
get_local_address = obtine_adresa_locala
calculate_network_info = calculeaza_info_retea
prefix_for_hosts = calculeaza_prefix_pentru_gazde
