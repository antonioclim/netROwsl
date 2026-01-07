#!/usr/bin/env python3
"""
Utilități de Rețea
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Oferă funcții helper pentru testarea și diagnosticarea rețelei.
"""

import socket
import subprocess
import time
from typing import Optional, Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError


def verifica_port_deschis(gazda: str, port: int, timeout: float = 2.0) -> bool:
    """
    Verifică dacă un port este deschis pe o gazdă.
    
    Args:
        gazda: Adresa gazdei
        port: Numărul portului
        timeout: Timeout în secunde
    
    Returns:
        True dacă portul este deschis
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((gazda, port))
            return result == 0
    except Exception:
        return False


def asteapta_port(
    gazda: str, 
    port: int, 
    timeout: float = 30.0,
    interval: float = 0.5
) -> bool:
    """
    Așteaptă ca un port să devină disponibil.
    
    Args:
        gazda: Adresa gazdei
        port: Numărul portului
        timeout: Timeout total în secunde
        interval: Interval între verificări
    
    Returns:
        True dacă portul a devenit disponibil în timp util
    """
    start = time.time()
    while time.time() - start < timeout:
        if verifica_port_deschis(gazda, port, timeout=1.0):
            return True
        time.sleep(interval)
    return False


def cerere_http_get(
    url: str, 
    timeout: float = 10.0,
    antete: Optional[dict] = None
) -> Tuple[int, dict, bytes]:
    """
    Efectuează o cerere HTTP GET.
    
    Args:
        url: URL-ul de accesat
        timeout: Timeout în secunde
        antete: Antete HTTP opționale
    
    Returns:
        Tuplu (cod_stare, antete, corp)
    
    Raises:
        URLError: Dacă cererea eșuează
    """
    cerere = Request(url)
    
    if antete:
        for cheie, valoare in antete.items():
            cerere.add_header(cheie, valoare)
    
    with urlopen(cerere, timeout=timeout) as raspuns:
        cod_stare = raspuns.status
        antete_raspuns = dict(raspuns.headers)
        corp = raspuns.read()
        
        return cod_stare, antete_raspuns, corp


def verifica_sanatate_http(url: str, timeout: float = 5.0) -> bool:
    """
    Verifică dacă un endpoint HTTP răspunde cu succes.
    
    Args:
        url: URL-ul de verificat
        timeout: Timeout în secunde
    
    Returns:
        True dacă răspunsul are cod 2xx
    """
    try:
        cod_stare, _, _ = cerere_http_get(url, timeout=timeout)
        return 200 <= cod_stare < 300
    except Exception:
        return False


def ping_gazda(gazda: str, numar: int = 3) -> Tuple[bool, str]:
    """
    Efectuează ping către o gazdă.
    
    Args:
        gazda: Adresa gazdei
        numar: Numărul de pachete
    
    Returns:
        Tuplu (succes, ieșire)
    """
    try:
        # Detectează sistemul de operare pentru sintaxa corectă
        import platform
        parametru = "-n" if platform.system().lower() == "windows" else "-c"
        
        result = subprocess.run(
            ["ping", parametru, str(numar), gazda],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)


def traceroute(gazda: str) -> Tuple[bool, str]:
    """
    Efectuează traceroute către o gazdă.
    
    Args:
        gazda: Adresa gazdei
    
    Returns:
        Tuplu (succes, ieșire)
    """
    try:
        import platform
        comanda = "tracert" if platform.system().lower() == "windows" else "traceroute"
        
        result = subprocess.run(
            [comanda, gazda],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)


def obtine_ip_local() -> str:
    """
    Obține adresa IP locală a mașinii.
    
    Returns:
        Adresa IP ca string
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Nu trebuie să fie accesibilă, doar folosită pentru a obține IP-ul
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def rezolva_dns(nume_gazda: str) -> Optional[str]:
    """
    Rezolvă un nume de gazdă la adresa IP.
    
    Args:
        nume_gazda: Numele de gazdă de rezolvat
    
    Returns:
        Adresa IP sau None dacă rezolvarea eșuează
    """
    try:
        return socket.gethostbyname(nume_gazda)
    except socket.gaierror:
        return None


def formateaza_dimensiune(octeti: int) -> str:
    """
    Formatează o dimensiune în octeți într-un format ușor de citit.
    
    Args:
        octeti: Numărul de octeți
    
    Returns:
        String formatat (ex: "1.5 MB")
    """
    for unitate in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(octeti) < 1024.0:
            return f"{octeti:.1f} {unitate}"
        octeti /= 1024.0
    return f"{octeti:.1f} PB"
