#!/usr/bin/env python3
"""
Utilitare de Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Funcții auxiliare pentru exercițiile de laborator.
"""

from __future__ import annotations

import socket
import subprocess
import time
from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class RezultatPing:
    """Rezultatul unei operațiuni ping."""
    reusit: bool
    gazda: str
    rtt_ms: Optional[float] = None
    mesaj: str = ""


@dataclass
class InfoSocket:
    """Informații despre un socket."""
    protocol: str
    adresa_locala: str
    port_local: int
    adresa_externa: str
    port_extern: int
    stare: str


def ping_gazda(gazda: str, timeout: int = 5) -> RezultatPing:
    """Trimite un singur pachet ICMP și măsoară RTT.
    
    Args:
        gazda: Adresa IP sau hostname
        timeout: Timeout în secunde
        
    Returns:
        Rezultatul operațiunii ping
    """
    try:
        timp_start = time.time()
        rezultat = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), gazda],
            capture_output=True,
            text=True,
            timeout=timeout + 2
        )
        timp_total = (time.time() - timp_start) * 1000
        
        if rezultat.returncode == 0:
            # Extrage RTT din ieșire
            for linie in rezultat.stdout.split("\n"):
                if "time=" in linie:
                    parti = linie.split("time=")
                    if len(parti) > 1:
                        rtt_str = parti[1].split()[0].replace("ms", "")
                        try:
                            rtt = float(rtt_str)
                            return RezultatPing(
                                reusit=True,
                                gazda=gazda,
                                rtt_ms=rtt,
                                mesaj="Răspuns primit"
                            )
                        except ValueError:
                            pass
            
            return RezultatPing(
                reusit=True,
                gazda=gazda,
                rtt_ms=timp_total,
                mesaj="Răspuns primit"
            )
        else:
            return RezultatPing(
                reusit=False,
                gazda=gazda,
                mesaj="Gazdă inaccesibilă"
            )
            
    except subprocess.TimeoutExpired:
        return RezultatPing(
            reusit=False,
            gazda=gazda,
            mesaj="Timeout expirat"
        )
    except Exception as e:
        return RezultatPing(
            reusit=False,
            gazda=gazda,
            mesaj=str(e)
        )


def verifica_port_tcp(gazda: str, port: int, timeout: float = 5.0) -> Tuple[bool, float]:
    """Verifică dacă un port TCP este deschis.
    
    Args:
        gazda: Adresa IP sau hostname
        port: Numărul portului
        timeout: Timeout în secunde
        
    Returns:
        Tuple (deschis, timp_conectare_ms)
    """
    timp_start = time.time()
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            rezultat = s.connect_ex((gazda, port))
            timp_conectare = (time.time() - timp_start) * 1000
            
            return rezultat == 0, timp_conectare
            
    except Exception:
        return False, 0.0


def obtine_adresa_locala() -> str:
    """Obține adresa IP locală a sistemului.
    
    Returns:
        Adresa IP locală sau '127.0.0.1' dacă nu poate fi determinată
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Nu trimite date, doar determină ruta
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def rezolva_hostname(hostname: str) -> Optional[str]:
    """Rezolvă un hostname la adresa IP.
    
    Args:
        hostname: Numele de domeniu
        
    Returns:
        Adresa IP sau None dacă nu poate fi rezolvat
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def obtine_hostname_local() -> str:
    """Obține hostname-ul local.
    
    Returns:
        Hostname-ul sistemului
    """
    return socket.gethostname()


def formateaza_dimensiune(octeti: int) -> str:
    """Formatează o dimensiune în octeți într-un format citibil.
    
    Args:
        octeti: Dimensiunea în octeți
        
    Returns:
        Șir formatat (ex: '1.5 KB', '2.3 MB')
    """
    for unitate in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(octeti) < 1024.0:
            return f"{octeti:.1f} {unitate}"
        octeti /= 1024.0
    return f"{octeti:.1f} PB"


def formateaza_durata(secunde: float) -> str:
    """Formatează o durată în secunde într-un format citibil.
    
    Args:
        secunde: Durata în secunde
        
    Returns:
        Șir formatat (ex: '1m 30s', '2h 15m')
    """
    if secunde < 60:
        return f"{secunde:.2f}s"
    elif secunde < 3600:
        minute = int(secunde // 60)
        sec = secunde % 60
        return f"{minute}m {sec:.0f}s"
    else:
        ore = int(secunde // 3600)
        minute = int((secunde % 3600) // 60)
        return f"{ore}h {minute}m"


def creeaza_socket_tcp() -> socket.socket:
    """Creează un socket TCP configurat.
    
    Returns:
        Socket TCP nou
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s


def creeaza_socket_udp() -> socket.socket:
    """Creează un socket UDP configurat.
    
    Returns:
        Socket UDP nou
    """
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def calculeaza_checksum(date: bytes) -> int:
    """Calculează un checksum simplu pentru date.
    
    Args:
        date: Datele pentru care se calculează checksum-ul
        
    Returns:
        Valoarea checksum-ului (16 biți)
    """
    suma = 0
    for i in range(0, len(date), 2):
        if i + 1 < len(date):
            cuvant = (date[i] << 8) + date[i + 1]
        else:
            cuvant = date[i] << 8
        suma += cuvant
    
    # Adaugă carry
    while suma >> 16:
        suma = (suma & 0xFFFF) + (suma >> 16)
    
    return ~suma & 0xFFFF


# Demonstrație
if __name__ == "__main__":
    print("Demonstrație Utilitare de Rețea")
    print("=" * 40)
    
    # Test ping
    print("\nTest ping localhost:")
    rez = ping_gazda("127.0.0.1")
    if rez.reusit:
        print(f"  ✓ RTT: {rez.rtt_ms:.2f} ms")
    else:
        print(f"  ✗ {rez.mesaj}")
    
    # Adresa locală
    print(f"\nAdresă IP locală: {obtine_adresa_locala()}")
    print(f"Hostname local: {obtine_hostname_local()}")
    
    # Test port
    print("\nTest port 80 pe localhost:")
    deschis, timp = verifica_port_tcp("127.0.0.1", 80, timeout=2)
    print(f"  {'✓ Deschis' if deschis else '✗ Închis'}")
