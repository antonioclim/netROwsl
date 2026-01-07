#!/usr/bin/env python3
"""
Utilitare de Rețea
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Funcții helper pentru testarea și diagnosticarea rețelei.
"""

import socket
import time
import subprocess
from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class RezultatPing:
    """Rezultatul unui test ping."""
    succes: bool
    durată_ms: float
    răspuns: str = ""
    eroare: str = ""


@dataclass
class InfoPort:
    """Informații despre un port."""
    port: int
    protocol: str
    stare: str
    proces: str = ""


class UtilitareRețea:
    """Clasă cu utilitare pentru operațiuni de rețea."""
    
    @staticmethod
    def verifică_port_tcp(host: str, port: int, timeout: float = 2.0) -> bool:
        """
        Verifică dacă un port TCP este deschis.
        
        Args:
            host: Adresa host
            port: Numărul portului
            timeout: Timeout în secunde
            
        Returns:
            True dacă portul este deschis
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                rezultat = sock.connect_ex((host, port))
                return rezultat == 0
        except Exception:
            return False
    
    @staticmethod
    def verifică_port_udp(host: str, port: int, mesaj: bytes = b"ping", timeout: float = 2.0) -> bool:
        """
        Verifică dacă un port UDP răspunde.
        
        Args:
            host: Adresa host
            port: Numărul portului
            mesaj: Mesaj de test
            timeout: Timeout în secunde
            
        Returns:
            True dacă s-a primit răspuns
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)
                sock.sendto(mesaj, (host, port))
                sock.recvfrom(1024)
                return True
        except socket.timeout:
            return False
        except Exception:
            return False
    
    @staticmethod
    def testează_tcp(
        host: str,
        port: int,
        mesaj: str,
        timeout: float = 5.0
    ) -> RezultatPing:
        """
        Testează comunicarea TCP cu un server.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
            mesaj: Mesajul de trimis
            timeout: Timeout în secunde
            
        Returns:
            RezultatPing cu detalii
        """
        try:
            start = time.perf_counter()
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((host, port))
                sock.sendall(mesaj.encode())
                răspuns = sock.recv(4096).decode()
            
            durată = (time.perf_counter() - start) * 1000
            
            return RezultatPing(
                succes=True,
                durată_ms=durată,
                răspuns=răspuns.strip()
            )
        except socket.timeout:
            return RezultatPing(
                succes=False,
                durată_ms=0,
                eroare="Timeout - serverul nu a răspuns"
            )
        except ConnectionRefusedError:
            return RezultatPing(
                succes=False,
                durată_ms=0,
                eroare="Conexiune refuzată - serverul nu rulează"
            )
        except Exception as e:
            return RezultatPing(
                succes=False,
                durată_ms=0,
                eroare=str(e)
            )
    
    @staticmethod
    def testează_udp(
        host: str,
        port: int,
        mesaj: str,
        timeout: float = 2.0
    ) -> RezultatPing:
        """
        Testează comunicarea UDP cu un server.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
            mesaj: Mesajul de trimis
            timeout: Timeout în secunde
            
        Returns:
            RezultatPing cu detalii
        """
        try:
            start = time.perf_counter()
            
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)
                sock.sendto(mesaj.encode(), (host, port))
                răspuns, _ = sock.recvfrom(4096)
            
            durată = (time.perf_counter() - start) * 1000
            
            return RezultatPing(
                succes=True,
                durată_ms=durată,
                răspuns=răspuns.decode().strip()
            )
        except socket.timeout:
            return RezultatPing(
                succes=False,
                durată_ms=0,
                eroare="Timeout - fără răspuns UDP"
            )
        except Exception as e:
            return RezultatPing(
                succes=False,
                durată_ms=0,
                eroare=str(e)
            )
    
    @staticmethod
    def obține_ip_local() -> str:
        """
        Obține adresa IP locală folosită pentru conexiuni externe.
        
        Returns:
            Adresa IP locală
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def rezolvă_hostname(hostname: str) -> Optional[str]:
        """
        Rezolvă un hostname la adresă IP.
        
        Args:
            hostname: Numele de rezolvat
            
        Returns:
            Adresa IP sau None dacă eșuează
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None
    
    @staticmethod
    def scanează_porturi(
        host: str,
        porturi: List[int],
        timeout: float = 0.5
    ) -> List[InfoPort]:
        """
        Scanează o listă de porturi TCP.
        
        Args:
            host: Adresa de scanat
            porturi: Lista de porturi
            timeout: Timeout per port
            
        Returns:
            Lista cu informații despre porturile deschise
        """
        rezultate = []
        
        for port in porturi:
            deschis = UtilitareRețea.verifică_port_tcp(host, port, timeout)
            
            if deschis:
                rezultate.append(InfoPort(
                    port=port,
                    protocol="TCP",
                    stare="DESCHIS"
                ))
        
        return rezultate
    
    @staticmethod
    def măsoară_latență(
        host: str,
        port: int,
        nr_teste: int = 5,
        protocol: str = "TCP"
    ) -> Tuple[float, float, float]:
        """
        Măsoară latența către un server.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
            nr_teste: Număr de teste
            protocol: TCP sau UDP
            
        Returns:
            Tuple cu (min, medie, max) în milisecunde
        """
        durate = []
        
        for _ in range(nr_teste):
            if protocol.upper() == "TCP":
                rezultat = UtilitareRețea.testează_tcp(host, port, "ping")
            else:
                rezultat = UtilitareRețea.testează_udp(host, port, "ping")
            
            if rezultat.succes:
                durate.append(rezultat.durată_ms)
            
            time.sleep(0.1)
        
        if not durate:
            return (0.0, 0.0, 0.0)
        
        return (min(durate), sum(durate) / len(durate), max(durate))


def formatează_bytes(nr_bytes: int) -> str:
    """
    Formatează un număr de bytes într-un format lizibil.
    
    Args:
        nr_bytes: Numărul de bytes
        
    Returns:
        String formatat (ex: "1.5 KB", "2.3 MB")
    """
    for unitate in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(nr_bytes) < 1024.0:
            return f"{nr_bytes:.1f} {unitate}"
        nr_bytes /= 1024.0
    return f"{nr_bytes:.1f} PB"


def formatează_durată(milisecunde: float) -> str:
    """
    Formatează o durată în milisecunde.
    
    Args:
        milisecunde: Durata în milisecunde
        
    Returns:
        String formatat
    """
    if milisecunde < 1:
        return f"{milisecunde * 1000:.0f} µs"
    elif milisecunde < 1000:
        return f"{milisecunde:.2f} ms"
    else:
        return f"{milisecunde / 1000:.2f} s"


if __name__ == "__main__":
    # Test rapid
    print("Test Utilitare Rețea")
    print("=" * 40)
    
    utilități = UtilitareRețea()
    
    print(f"IP local: {utilități.obține_ip_local()}")
    print(f"Rezolvare google.com: {utilități.rezolvă_hostname('google.com')}")
    
    print("\nTest TCP localhost:9090...")
    rezultat = utilități.testează_tcp("localhost", 9090, "test")
    print(f"  Succes: {rezultat.succes}")
    if rezultat.succes:
        print(f"  Durată: {formatează_durată(rezultat.durată_ms)}")
        print(f"  Răspuns: {rezultat.răspuns}")
    else:
        print(f"  Eroare: {rezultat.eroare}")
