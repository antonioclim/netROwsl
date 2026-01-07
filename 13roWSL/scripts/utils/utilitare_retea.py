#!/usr/bin/env python3
"""
Utilitare Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Furnizează funcții pentru testarea conectivității și analiza rețelei.
"""

import socket
import subprocess
import platform
from typing import Optional, Tuple, List


def verifica_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Verifică dacă un port este deschis pe un host.
    
    Args:
        host: Adresa IP sau hostname
        port: Numărul portului
        timeout: Timeout în secunde
    
    Returns:
        True dacă portul este deschis și accesibil
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            rezultat = sock.connect_ex((host, port))
            return rezultat == 0
    except (socket.error, socket.timeout):
        return False


def obtine_banner(host: str, port: int, timeout: float = 3.0) -> Optional[str]:
    """
    Încearcă să obțină banner-ul de la un serviciu.
    
    Args:
        host: Adresa IP sau hostname
        port: Numărul portului
        timeout: Timeout în secunde
    
    Returns:
        Banner-ul serviciului sau None dacă nu s-a putut obține
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Unele servicii trimit banner automat, altele așteaptă input
            sock.settimeout(1.0)
            try:
                banner = sock.recv(1024)
                return banner.decode('utf-8', errors='ignore').strip()
            except socket.timeout:
                # Încearcă cu un request HTTP simplu pentru servicii web
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                try:
                    raspuns = sock.recv(1024)
                    return raspuns.decode('utf-8', errors='ignore').split('\n')[0].strip()
                except socket.timeout:
                    return None
    except Exception:
        return None


def rezolva_hostname(hostname: str) -> Optional[str]:
    """
    Rezolvă un hostname la adresa IP.
    
    Args:
        hostname: Numele de domeniu de rezolvat
    
    Returns:
        Adresa IP sau None dacă nu s-a putut rezolva
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def scaneaza_porturi(host: str, porturi: List[int], timeout: float = 1.0) -> List[Tuple[int, bool, Optional[str]]]:
    """
    Scanează o listă de porturi pe un host.
    
    Args:
        host: Adresa IP sau hostname
        porturi: Lista de porturi de scanat
        timeout: Timeout per port
    
    Returns:
        Listă de tupluri (port, deschis, banner)
    """
    rezultate = []
    
    for port in porturi:
        deschis = verifica_port(host, port, timeout)
        banner = obtine_banner(host, port, timeout) if deschis else None
        rezultate.append((port, deschis, banner))
    
    return rezultate


def ping_host(host: str, count: int = 1) -> bool:
    """
    Verifică dacă un host răspunde la ping.
    
    Args:
        host: Adresa IP sau hostname
        count: Numărul de pachete ICMP
    
    Returns:
        True dacă host-ul răspunde
    """
    # Detectează sistemul de operare pentru parametrul count
    parametru = "-n" if platform.system().lower() == "windows" else "-c"
    
    try:
        rezultat = subprocess.run(
            ["ping", parametru, str(count), host],
            capture_output=True,
            timeout=5
        )
        return rezultat.returncode == 0
    except Exception:
        return False


class VerificatorServicii:
    """
    Verificator pentru serviciile laboratorului.
    
    Verifică disponibilitatea și starea serviciilor configurate.
    """
    
    def __init__(self):
        self.servicii = {
            "mqtt": (1883, "MQTT Broker (text clar)"),
            "mqtt_tls": (8883, "MQTT Broker (TLS)"),
            "dvwa": (8080, "DVWA (HTTP)"),
            "ftp": (2121, "vsftpd (FTP)"),
            "backdoor": (6200, "Backdoor simulat")
        }
    
    def verifica_toate(self, host: str = "localhost") -> dict:
        """
        Verifică toate serviciile laboratorului.
        
        Args:
            host: Host-ul de verificat
        
        Returns:
            Dicționar cu starea fiecărui serviciu
        """
        rezultate = {}
        
        for nume, (port, descriere) in self.servicii.items():
            deschis = verifica_port(host, port)
            banner = obtine_banner(host, port) if deschis else None
            
            rezultate[nume] = {
                "port": port,
                "descriere": descriere,
                "disponibil": deschis,
                "banner": banner
            }
        
        return rezultate
    
    def afiseaza_stare(self, host: str = "localhost"):
        """
        Afișează starea serviciilor într-un format vizual.
        
        Args:
            host: Host-ul de verificat
        """
        rezultate = self.verifica_toate(host)
        
        print("\n" + "=" * 60)
        print("STARE SERVICII LABORATOR")
        print("=" * 60)
        
        for nume, info in rezultate.items():
            stare = "✓ DISPONIBIL" if info["disponibil"] else "✗ INDISPONIBIL"
            print(f"  {info['descriere']:30} Port {info['port']:5} {stare}")
            if info["banner"]:
                banner_scurt = info["banner"][:50] + "..." if len(info["banner"]) > 50 else info["banner"]
                print(f"    Banner: {banner_scurt}")
        
        print("=" * 60)


# Alias pentru compatibilitate
check_port = verifica_port
grab_banner = obtine_banner
resolve_hostname = rezolva_hostname
scan_port_range = scaneaza_porturi
ping_host = ping_host
ServiceChecker = VerificatorServicii
