#!/usr/bin/env python3
"""
Utilitare de Testare a Rețelei
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Oferă funcții pentru testarea conectivității și diagnosticarea rețelei.
"""

from __future__ import annotations

import subprocess
import socket
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .logger import configureaza_logger


@dataclass
class RezultatPing:
    """Rezultatul unei operațiuni ping."""
    reusit: bool
    gazda: str
    pachete_trimise: int
    pachete_primite: int
    pierdere_procent: float
    rtt_min: Optional[float] = None
    rtt_medie: Optional[float] = None
    rtt_max: Optional[float] = None
    mesaj_eroare: Optional[str] = None


@dataclass
class RezultatVerificarePort:
    """Rezultatul verificării unui port."""
    deschis: bool
    gazda: str
    port: int
    protocol: str
    timp_raspuns_ms: Optional[float] = None
    mesaj_eroare: Optional[str] = None


class TesterRetea:
    """Clasă pentru testarea conectivității de rețea."""
    
    def __init__(self) -> None:
        """Inițializează testerul de rețea."""
        self.logger = configureaza_logger("retea")

    def ping(
        self,
        gazda: str,
        numar_pachete: int = 4,
        timeout: int = 5
    ) -> RezultatPing:
        """Execută ping către o gazdă.
        
        Args:
            gazda: Adresa IP sau hostname-ul țintă
            numar_pachete: Numărul de pachete de trimis
            timeout: Timeout per pachet în secunde
            
        Returns:
            Rezultatul operațiunii ping
        """
        self.logger.debug(f"Ping către {gazda} cu {numar_pachete} pachete")
        
        try:
            rezultat = subprocess.run(
                ["ping", "-c", str(numar_pachete), "-W", str(timeout), gazda],
                capture_output=True,
                text=True,
                timeout=timeout * numar_pachete + 10
            )
            
            if rezultat.returncode == 0:
                # Parsează ieșirea pentru statistici
                linii = rezultat.stdout.strip().split("\n")
                
                # Caută linia cu statisticile de pierdere
                pierdere = 0.0
                trimise = numar_pachete
                primite = numar_pachete
                rtt_min = rtt_medie = rtt_max = None
                
                for linie in linii:
                    if "packet loss" in linie or "pierdute" in linie:
                        parti = linie.split(",")
                        for parte in parti:
                            if "received" in parte or "primite" in parte:
                                primite = int("".join(filter(str.isdigit, parte.split()[0])))
                            elif "loss" in parte or "pierdere" in parte:
                                pierdere = float(parte.split("%")[0].split()[-1])
                    
                    elif "rtt" in linie.lower() or "min/avg/max" in linie:
                        # Format: rtt min/avg/max/mdev = 0.123/0.456/0.789/0.012 ms
                        parti = linie.split("=")
                        if len(parti) >= 2:
                            valori = parti[1].strip().split("/")
                            if len(valori) >= 3:
                                rtt_min = float(valori[0])
                                rtt_medie = float(valori[1])
                                rtt_max = float(valori[2])
                
                return RezultatPing(
                    reusit=True,
                    gazda=gazda,
                    pachete_trimise=trimise,
                    pachete_primite=primite,
                    pierdere_procent=pierdere,
                    rtt_min=rtt_min,
                    rtt_medie=rtt_medie,
                    rtt_max=rtt_max
                )
            else:
                return RezultatPing(
                    reusit=False,
                    gazda=gazda,
                    pachete_trimise=numar_pachete,
                    pachete_primite=0,
                    pierdere_procent=100.0,
                    mesaj_eroare=rezultat.stderr or "Ping eșuat"
                )
                
        except subprocess.TimeoutExpired:
            return RezultatPing(
                reusit=False,
                gazda=gazda,
                pachete_trimise=numar_pachete,
                pachete_primite=0,
                pierdere_procent=100.0,
                mesaj_eroare="Timeout expirat"
            )
        except Exception as e:
            return RezultatPing(
                reusit=False,
                gazda=gazda,
                pachete_trimise=numar_pachete,
                pachete_primite=0,
                pierdere_procent=100.0,
                mesaj_eroare=str(e)
            )

    def verifica_port_tcp(
        self,
        gazda: str,
        port: int,
        timeout: float = 5.0
    ) -> RezultatVerificarePort:
        """Verifică dacă un port TCP este deschis.
        
        Args:
            gazda: Adresa IP sau hostname-ul
            port: Numărul portului
            timeout: Timeout în secunde
            
        Returns:
            Rezultatul verificării
        """
        self.logger.debug(f"Verificare port TCP {gazda}:{port}")
        
        timp_start = time.time()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                rezultat = s.connect_ex((gazda, port))
                timp_raspuns = (time.time() - timp_start) * 1000
                
                if rezultat == 0:
                    return RezultatVerificarePort(
                        deschis=True,
                        gazda=gazda,
                        port=port,
                        protocol="TCP",
                        timp_raspuns_ms=timp_raspuns
                    )
                else:
                    return RezultatVerificarePort(
                        deschis=False,
                        gazda=gazda,
                        port=port,
                        protocol="TCP",
                        mesaj_eroare=f"Conexiune refuzată (cod: {rezultat})"
                    )
                    
        except socket.timeout:
            return RezultatVerificarePort(
                deschis=False,
                gazda=gazda,
                port=port,
                protocol="TCP",
                mesaj_eroare="Timeout la conectare"
            )
        except Exception as e:
            return RezultatVerificarePort(
                deschis=False,
                gazda=gazda,
                port=port,
                protocol="TCP",
                mesaj_eroare=str(e)
            )

    def verifica_port_udp(
        self,
        gazda: str,
        port: int,
        timeout: float = 5.0
    ) -> RezultatVerificarePort:
        """Verifică dacă un port UDP răspunde.
        
        Args:
            gazda: Adresa IP sau hostname-ul
            port: Numărul portului
            timeout: Timeout în secunde
            
        Returns:
            Rezultatul verificării
        
        Notă: UDP este fără conexiune, deci verificarea este aproximativă.
        """
        self.logger.debug(f"Verificare port UDP {gazda}:{port}")
        
        timp_start = time.time()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)
                s.sendto(b"test", (gazda, port))
                
                try:
                    s.recvfrom(1024)
                    timp_raspuns = (time.time() - timp_start) * 1000
                    return RezultatVerificarePort(
                        deschis=True,
                        gazda=gazda,
                        port=port,
                        protocol="UDP",
                        timp_raspuns_ms=timp_raspuns
                    )
                except socket.timeout:
                    # Pentru UDP, timeout nu înseamnă neapărat port închis
                    return RezultatVerificarePort(
                        deschis=True,  # Presupunem deschis dacă nu primim ICMP unreachable
                        gazda=gazda,
                        port=port,
                        protocol="UDP",
                        mesaj_eroare="Fără răspuns (normal pentru UDP)"
                    )
                    
        except Exception as e:
            return RezultatVerificarePort(
                deschis=False,
                gazda=gazda,
                port=port,
                protocol="UDP",
                mesaj_eroare=str(e)
            )

    def obtine_interfete_locale(self) -> List[Tuple[str, str]]:
        """Obține lista interfețelor de rețea locale.
        
        Returns:
            Lista de tuple (nume_interfață, adresă_ip)
        """
        interfete = []
        
        try:
            rezultat = subprocess.run(
                ["ip", "-br", "addr", "show"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if rezultat.returncode == 0:
                for linie in rezultat.stdout.strip().split("\n"):
                    parti = linie.split()
                    if len(parti) >= 3:
                        nume = parti[0]
                        # Extrage prima adresă IP (fără CIDR)
                        for parte in parti[2:]:
                            if "/" in parte:
                                ip = parte.split("/")[0]
                                interfete.append((nume, ip))
                                break
                                
        except Exception as e:
            self.logger.error(f"Eroare la obținerea interfețelor: {e}")
        
        return interfete

    def obtine_gateway_implicit(self) -> Optional[str]:
        """Obține adresa gateway-ului implicit.
        
        Returns:
            Adresa IP a gateway-ului sau None
        """
        try:
            rezultat = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if rezultat.returncode == 0:
                parti = rezultat.stdout.strip().split()
                if "via" in parti:
                    idx = parti.index("via")
                    if idx + 1 < len(parti):
                        return parti[idx + 1]
                        
        except Exception as e:
            self.logger.error(f"Eroare la obținerea gateway-ului: {e}")
        
        return None

    def ruleaza_test_conectivitate(self) -> None:
        """Rulează un test de conectivitate complet și afișează rezultatele."""
        print("\n" + "=" * 60)
        print("  TEST DE CONECTIVITATE")
        print("=" * 60 + "\n")
        
        # Interfețe locale
        print("INTERFEȚE LOCALE:")
        interfete = self.obtine_interfete_locale()
        for nume, ip in interfete:
            print(f"  • {nume}: {ip}")
        
        # Gateway implicit
        gateway = self.obtine_gateway_implicit()
        print(f"\nGATEWAY IMPLICIT: {gateway or 'nedisponibil'}")
        
        # Test ping loopback
        print("\nTEST LOOPBACK:")
        rez = self.ping("127.0.0.1", numar_pachete=2)
        if rez.reusit:
            print(f"  ✓ Loopback funcțional (RTT: {rez.rtt_medie:.2f} ms)")
        else:
            print(f"  ✗ Loopback eșuat: {rez.mesaj_eroare}")
        
        # Test ping gateway
        if gateway:
            print("\nTEST GATEWAY:")
            rez = self.ping(gateway, numar_pachete=2)
            if rez.reusit:
                print(f"  ✓ Gateway accesibil (RTT: {rez.rtt_medie:.2f} ms)")
            else:
                print(f"  ✗ Gateway inaccesibil: {rez.mesaj_eroare}")
        
        print("\n" + "=" * 60 + "\n")


# Exemplu de utilizare
if __name__ == "__main__":
    tester = TesterRetea()
    tester.ruleaza_test_conectivitate()
