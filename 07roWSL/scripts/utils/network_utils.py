#!/usr/bin/env python3
"""
Utilitare de Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Funcții pentru testarea conectivității și operațiuni de rețea.
"""

from __future__ import annotations

import socket
import time
from typing import Literal

from .logger import configureaza_logger

logger = configureaza_logger('network_utils')


class UtilitareRetea:
    """Clasă cu utilitare pentru operațiuni de rețea."""
    
    @staticmethod
    def verifica_port_deschis(
        host: str,
        port: int,
        timeout: float = 3.0,
        protocol: Literal["tcp", "udp"] = "tcp"
    ) -> bool:
        """
        Verifică dacă un port este deschis.
        
        Args:
            host: Adresa gazdă
            port: Numărul portului
            timeout: Timeout în secunde
            protocol: Protocolul de verificat (tcp sau udp)
        
        Returns:
            True dacă portul este deschis (pentru TCP)
            True dacă se poate trimite (pentru UDP - nu garantează recepție)
        """
        if protocol == "tcp":
            tip_socket = socket.SOCK_STREAM
        else:
            tip_socket = socket.SOCK_DGRAM
        
        try:
            sock = socket.socket(socket.AF_INET, tip_socket)
            sock.settimeout(timeout)
            
            if protocol == "tcp":
                rezultat = sock.connect_ex((host, port))
                sock.close()
                return rezultat == 0
            else:
                # Pentru UDP, doar verificăm că putem trimite
                sock.sendto(b"test", (host, port))
                sock.close()
                return True
                
        except socket.timeout:
            return False
        except Exception as e:
            logger.debug(f"Eroare la verificare port {host}:{port}: {e}")
            return False
    
    @staticmethod
    def asteapta_port(
        host: str,
        port: int,
        timeout: float = 30.0,
        interval: float = 1.0
    ) -> bool:
        """
        Așteaptă până când un port devine disponibil.
        
        Args:
            host: Adresa gazdă
            port: Numărul portului
            timeout: Timeout total în secunde
            interval: Interval între încercări
        
        Returns:
            True dacă portul a devenit disponibil
        """
        timp_start = time.time()
        
        while time.time() - timp_start < timeout:
            if UtilitareRetea.verifica_port_deschis(host, port, timeout=2.0):
                return True
            time.sleep(interval)
        
        return False
    
    @staticmethod
    def test_echo_tcp(
        host: str,
        port: int,
        mesaj: str = "test_echo",
        timeout: float = 5.0
    ) -> tuple[bool, str]:
        """
        Testează un server TCP echo.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
            mesaj: Mesajul de trimis
            timeout: Timeout în secunde
        
        Returns:
            Tuplu (succes, răspuns sau mesaj eroare)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            sock.sendall(mesaj.encode())
            raspuns = sock.recv(4096).decode()
            sock.close()
            
            if raspuns.strip() == mesaj:
                return True, raspuns
            else:
                return False, f"Răspuns neașteptat: {raspuns}"
                
        except socket.timeout:
            return False, "Timeout la așteptarea răspunsului"
        except ConnectionRefusedError:
            return False, "Conexiune refuzată"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def test_trimitere_udp(
        host: str,
        port: int,
        mesaj: str = "test_udp",
        timeout: float = 3.0,
        asteapta_raspuns: bool = False
    ) -> tuple[bool, str]:
        """
        Trimite o datagramă UDP.
        
        Args:
            host: Adresa destinație
            port: Portul destinație
            mesaj: Mesajul de trimis
            timeout: Timeout în secunde
            asteapta_raspuns: Dacă să aștepte răspuns
        
        Returns:
            Tuplu (succes, mesaj informativ)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            
            sock.sendto(mesaj.encode(), (host, port))
            
            if asteapta_raspuns:
                try:
                    raspuns, adresa = sock.recvfrom(4096)
                    sock.close()
                    return True, f"Răspuns primit: {raspuns.decode()}"
                except socket.timeout:
                    sock.close()
                    return False, "Niciun răspuns primit (posibil DROP)"
            else:
                sock.close()
                return True, "Datagramă trimisă"
                
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def sondeaza_porturi(
        host: str,
        interval_porturi: tuple[int, int],
        timeout_per_port: float = 1.0
    ) -> dict[int, str]:
        """
        Sondează un interval de porturi TCP.
        
        Args:
            host: Adresa gazdă
            interval_porturi: Tuplu (port_start, port_final)
            timeout_per_port: Timeout per port
        
        Returns:
            Dicționar {port: status} unde status este 'deschis', 'închis', 'filtrat'
        """
        rezultate = {}
        port_start, port_final = interval_porturi
        
        logger.info(f"Sondare porturi {port_start}-{port_final} pe {host}")
        
        for port in range(port_start, port_final + 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout_per_port)
                
                timp_start = time.time()
                rezultat = sock.connect_ex((host, port))
                timp_scurs = time.time() - timp_start
                sock.close()
                
                if rezultat == 0:
                    rezultate[port] = "deschis"
                    logger.info(f"  Port {port}: DESCHIS")
                elif timp_scurs >= timeout_per_port * 0.9:
                    # Timeout apropiat - probabil filtrat (DROP)
                    rezultate[port] = "filtrat"
                    logger.debug(f"  Port {port}: FILTRAT")
                else:
                    # Răspuns rapid negativ - închis
                    rezultate[port] = "închis"
                    logger.debug(f"  Port {port}: închis")
                    
            except socket.timeout:
                rezultate[port] = "filtrat"
                logger.debug(f"  Port {port}: FILTRAT (timeout)")
            except Exception as e:
                rezultate[port] = f"eroare: {e}"
        
        # Sumar
        deschise = sum(1 for s in rezultate.values() if s == "deschis")
        filtrate = sum(1 for s in rezultate.values() if s == "filtrat")
        inchise = sum(1 for s in rezultate.values() if s == "închis")
        
        logger.info(f"Rezultate: {deschise} deschise, {inchise} închise, {filtrate} filtrate")
        
        return rezultate
    
    @staticmethod
    def obtine_ip_local() -> str:
        """
        Obține adresa IP locală.
        
        Returns:
            Adresa IP locală sau '127.0.0.1' în caz de eroare
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except Exception:
            return "127.0.0.1"
