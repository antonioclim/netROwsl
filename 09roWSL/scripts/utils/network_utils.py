#!/usr/bin/env python3
"""
Utilitare de Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Funcții helper pentru testarea și diagnosticarea rețelei.
"""

import socket
import subprocess
import time
from typing import Optional, Tuple
from ftplib import FTP


def verifica_port(
    gazda: str,
    port: int,
    timeout: float = 2.0
) -> bool:
    """
    Verifică dacă un port este deschis pe o gazdă.
    
    Argumente:
        gazda: Adresa IP sau hostname
        port: Numărul portului
        timeout: Timpul de așteptare în secunde
        
    Returnează:
        True dacă portul este deschis, False altfel
        
    Exemplu:
        >>> verifica_port("localhost", 2121)
        True
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            rezultat = s.connect_ex((gazda, port))
            return rezultat == 0
    except socket.error:
        return False


def asteapta_port(
    gazda: str,
    port: int,
    timeout: float = 30.0,
    interval: float = 1.0
) -> bool:
    """
    Așteaptă până când un port devine disponibil.
    
    Argumente:
        gazda: Adresa IP sau hostname
        port: Numărul portului
        timeout: Timpul maxim de așteptare în secunde
        interval: Intervalul între verificări
        
    Returnează:
        True dacă portul a devenit disponibil, False altfel
        
    Exemplu:
        >>> asteapta_port("localhost", 2121, timeout=10)
        True
    """
    timp_start = time.time()
    
    while time.time() - timp_start < timeout:
        if verifica_port(gazda, port, timeout=1.0):
            return True
        time.sleep(interval)
    
    return False


def ping_gazda(
    gazda: str,
    numar: int = 3,
    timeout: float = 5.0
) -> Tuple[bool, float]:
    """
    Execută ping către o gazdă.
    
    Argumente:
        gazda: Adresa IP sau hostname
        numar: Numărul de pachete de trimis
        timeout: Timpul de așteptare în secunde
        
    Returnează:
        Tuple (succes, timp_mediu_ms)
        
    Exemplu:
        >>> succes, timp = ping_gazda("google.com")
        >>> print(f"Ping reușit: {succes}, timp: {timp:.2f}ms")
    """
    try:
        # Detectează sistemul de operare
        import platform
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        
        rezultat = subprocess.run(
            ["ping", param, str(numar), gazda],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if rezultat.returncode == 0:
            # Extrage timpul mediu din output
            output = rezultat.stdout
            
            if 'Average' in output or 'avg' in output:
                import re
                # Pattern pentru Windows sau Linux
                match = re.search(r'(?:Average|avg)[^\d]*(\d+(?:\.\d+)?)', output)
                if match:
                    return True, float(match.group(1))
            
            return True, 0.0
        
        return False, 0.0
    
    except subprocess.TimeoutExpired:
        return False, 0.0
    except Exception:
        return False, 0.0


def testeaza_conexiune_ftp(
    gazda: str,
    port: int = 21,
    utilizator: str = "anonymous",
    parola: str = "guest@",
    timeout: float = 10.0
) -> Tuple[bool, str]:
    """
    Testează o conexiune FTP.
    
    Argumente:
        gazda: Adresa serverului FTP
        port: Portul FTP (implicit 21)
        utilizator: Numele de utilizator
        parola: Parola
        timeout: Timpul de așteptare
        
    Returnează:
        Tuple (succes, mesaj)
        
    Exemplu:
        >>> succes, mesaj = testeaza_conexiune_ftp("localhost", 2121, "test", "12345")
        >>> print(mesaj)
        Conectat cu succes. Director curent: /
    """
    try:
        ftp = FTP()
        ftp.connect(gazda, port, timeout=timeout)
        
        # Mesaj de bun venit
        banner = ftp.getwelcome()
        
        # Autentificare
        ftp.login(utilizator, parola)
        
        # Obține directorul curent
        director = ftp.pwd()
        
        ftp.quit()
        
        return True, f"Conectat cu succes. Banner: {banner}. Director: {director}"
    
    except Exception as e:
        return False, f"Eroare: {str(e)}"


def obtine_ip_local() -> str:
    """
    Obține adresa IP locală a mașinii.
    
    Returnează:
        Adresa IP ca string
        
    Exemplu:
        >>> ip = obtine_ip_local()
        >>> print(ip)
        192.168.1.100
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Nu trimite efectiv date, doar determină ruta
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def rezolva_hostname(hostname: str) -> Optional[str]:
    """
    Rezolvă un hostname la adresa IP.
    
    Argumente:
        hostname: Numele de gazdă de rezolvat
        
    Returnează:
        Adresa IP sau None dacă nu poate fi rezolvat
        
    Exemplu:
        >>> ip = rezolva_hostname("localhost")
        >>> print(ip)
        127.0.0.1
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def scaneaza_porturi(
    gazda: str,
    port_start: int,
    port_sfarsit: int,
    timeout: float = 0.5
) -> list:
    """
    Scanează un interval de porturi.
    
    Argumente:
        gazda: Adresa de scanat
        port_start: Portul de început
        port_sfarsit: Portul de final
        timeout: Timpul de așteptare per port
        
    Returnează:
        Lista porturilor deschise
        
    Exemplu:
        >>> porturi = scaneaza_porturi("localhost", 2120, 2125)
        >>> print(porturi)
        [2121]
    """
    porturi_deschise = []
    
    for port in range(port_start, port_sfarsit + 1):
        if verifica_port(gazda, port, timeout):
            porturi_deschise.append(port)
    
    return porturi_deschise


def formateaza_dimensiune(octeti: int) -> str:
    """
    Formatează o dimensiune în octeți într-un format lizibil.
    
    Argumente:
        octeti: Numărul de octeți
        
    Returnează:
        Dimensiunea formatată (ex: "1.5 MB")
        
    Exemplu:
        >>> print(formateaza_dimensiune(1536))
        1.50 KB
    """
    for unitate in ['B', 'KB', 'MB', 'GB', 'TB']:
        if octeti < 1024.0:
            return f"{octeti:.2f} {unitate}"
        octeti /= 1024.0
    return f"{octeti:.2f} PB"


# Alias-uri pentru compatibilitate cu versiunea engleză
check_port = verifica_port
wait_for_port = asteapta_port
ping_host = ping_gazda
test_ftp_connection = testeaza_conexiune_ftp
get_local_ip = obtine_ip_local


if __name__ == "__main__":
    # Demonstrație
    print("=== Test Utilitare Rețea ===\n")
    
    # Test IP local
    ip_local = obtine_ip_local()
    print(f"IP local: {ip_local}")
    
    # Test port
    port_test = 2121
    if verifica_port("localhost", port_test):
        print(f"Portul {port_test} este deschis")
    else:
        print(f"Portul {port_test} este închis")
    
    # Test rezolvare DNS
    ip_localhost = rezolva_hostname("localhost")
    print(f"localhost -> {ip_localhost}")
    
    # Test formatare dimensiune
    print(f"\n1234567 octeți = {formateaza_dimensiune(1234567)}")
