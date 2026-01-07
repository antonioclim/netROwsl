#!/usr/bin/env python3
"""
Utilități de Rețea pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă funcții helper pentru testarea conectivității de rețea.
"""

import socket
import subprocess
from typing import Tuple, Optional, Dict, Any
from urllib.request import urlopen
from urllib.error import URLError

from .logger import configureaza_logger

logger = configureaza_logger("network_utils")


class TesterRetea:
    """Clasă pentru testarea conectivității de rețea."""
    
    def __init__(self, timeout: int = 5):
        """
        Inițializează testerul de rețea.
        
        Args:
            timeout: Timeout implicit pentru conexiuni în secunde
        """
        self.timeout = timeout
    
    def testeaza_port_tcp(
        self,
        gazda: str,
        port: int,
        timeout: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Testează dacă un port TCP este accesibil.
        
        Args:
            gazda: Adresa gazdei
            port: Numărul portului
            timeout: Timeout opțional
        
        Returns:
            Tuple (succes, mesaj)
        """
        timeout = timeout or self.timeout
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((gazda, port))
                return True, f"Port {port} accesibil pe {gazda}"
        except socket.timeout:
            return False, f"Timeout la conectare la {gazda}:{port}"
        except ConnectionRefusedError:
            return False, f"Conexiune refuzată la {gazda}:{port}"
        except socket.gaierror as e:
            return False, f"Eroare rezoluție DNS pentru {gazda}: {e}"
        except Exception as e:
            return False, f"Eroare neașteptată: {e}"
    
    def testeaza_port_udp(
        self,
        gazda: str,
        port: int,
        date_test: bytes = b"test"
    ) -> Tuple[bool, str]:
        """
        Testează dacă un serviciu UDP răspunde.
        
        Args:
            gazda: Adresa gazdei
            port: Numărul portului
            date_test: Date de trimis pentru test
        
        Returns:
            Tuple (succes, mesaj)
        
        Note:
            UDP este fără conexiune, deci testul poate fi imprecis.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(self.timeout)
                s.sendto(date_test, (gazda, port))
                # Încercăm să primim un răspuns
                try:
                    s.recvfrom(1024)
                    return True, f"Serviciu UDP activ pe {gazda}:{port}"
                except socket.timeout:
                    # Fără răspuns nu înseamnă neapărat că nu funcționează
                    return True, f"Pachet trimis la {gazda}:{port} (fără răspuns)"
        except Exception as e:
            return False, f"Eroare UDP: {e}"
    
    def testeaza_http(
        self,
        url: str,
        timeout: Optional[int] = None
    ) -> Tuple[bool, str, int]:
        """
        Testează dacă un endpoint HTTP răspunde.
        
        Args:
            url: URL-ul de testat
            timeout: Timeout opțional
        
        Returns:
            Tuple (succes, mesaj, cod_stare)
        """
        timeout = timeout or self.timeout
        
        try:
            with urlopen(url, timeout=timeout) as raspuns:
                cod = raspuns.getcode()
                return True, f"HTTP {cod} de la {url}", cod
        except URLError as e:
            return False, f"Eroare HTTP: {e.reason}", 0
        except Exception as e:
            return False, f"Eroare neașteptată: {e}", 0
    
    def testeaza_dns(
        self,
        domeniu: str,
        server_dns: str = "localhost",
        port_dns: int = 5353
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Testează rezoluția DNS folosind serverul specificat.
        
        Args:
            domeniu: Domeniul de rezolvat
            server_dns: Adresa serverului DNS
            port_dns: Portul DNS
        
        Returns:
            Tuple (succes, mesaj, adresa_ip)
        """
        try:
            rezultat = subprocess.run(
                ["dig", f"@{server_dns}", "-p", str(port_dns), domeniu, "+short"],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if rezultat.returncode == 0 and rezultat.stdout.strip():
                ip = rezultat.stdout.strip().split('\n')[0]
                return True, f"{domeniu} -> {ip}", ip
            else:
                return False, f"Nu s-a rezolvat {domeniu}", None
        except FileNotFoundError:
            return False, "Comanda 'dig' nu este disponibilă", None
        except Exception as e:
            return False, f"Eroare DNS: {e}", None
    
    def testeaza_ssh(
        self,
        gazda: str,
        port: int = 22
    ) -> Tuple[bool, str]:
        """
        Testează dacă un server SSH răspunde.
        
        Args:
            gazda: Adresa serverului
            port: Portul SSH
        
        Returns:
            Tuple (succes, mesaj)
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((gazda, port))
                
                # Citim banner-ul SSH
                banner = s.recv(1024).decode('utf-8', errors='ignore')
                if banner.startswith('SSH-'):
                    return True, f"Server SSH: {banner.strip()}"
                else:
                    return True, f"Port SSH deschis pe {gazda}:{port}"
        except Exception as e:
            return False, f"Eroare SSH: {e}"
    
    def testeaza_ftp(
        self,
        gazda: str,
        port: int = 21
    ) -> Tuple[bool, str]:
        """
        Testează dacă un server FTP răspunde.
        
        Args:
            gazda: Adresa serverului
            port: Portul FTP
        
        Returns:
            Tuple (succes, mesaj)
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((gazda, port))
                
                # Citim banner-ul FTP (codul 220)
                banner = s.recv(1024).decode('utf-8', errors='ignore')
                if '220' in banner:
                    return True, f"Server FTP: {banner.strip()}"
                else:
                    return True, f"Port FTP deschis pe {gazda}:{port}"
        except Exception as e:
            return False, f"Eroare FTP: {e}"
    
    def ruleaza_suite_teste(
        self,
        servicii: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Tuple[bool, str]]:
        """
        Rulează o suită de teste pentru serviciile specificate.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        
        Returns:
            Dicționar cu rezultatele testelor
        """
        rezultate = {}
        
        for nume, config in servicii.items():
            port = config.get("port")
            verificare = config.get("verificare_sanatate")
            
            if verificare and verificare.startswith("http"):
                succes, mesaj, _ = self.testeaza_http(verificare)
            elif port:
                succes, mesaj = self.testeaza_port_tcp("localhost", port)
            else:
                succes, mesaj = False, "Configurație incompletă"
            
            rezultate[nume] = (succes, mesaj)
            
            simbol = "✓" if succes else "✗"
            logger.info(f"  {simbol} {nume}: {mesaj}")
        
        return rezultate


def obtine_adresa_ip_locala() -> str:
    """
    Obține adresa IP locală a mașinii.
    
    Returns:
        Adresa IP ca string
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
