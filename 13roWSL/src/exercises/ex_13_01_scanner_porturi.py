#!/usr/bin/env python3
"""
================================================================================
Exercițiul 1: Scanner TCP Avansat
================================================================================
S13 - IoT și Securitate în Rețelele de Calculatoare

OBIECTIVE PEDAGOGICE:
1. Înțelegerea funcționării socket-urilor TCP
2. Diferențierea între porturi deschise/închise/filtrate
3. Implementarea scanării concurente cu ThreadPoolExecutor
4. Exportul rezultatelor în format JSON structurat

AVERTISMENT ETIC:
- Acest instrument este destinat EXCLUSIV laboratorului controlat
- NU utilizați pe sisteme fără autorizare explicită
- Încălcarea acestei reguli constituie infracțiune conform legii

UTILIZARE:
    # Scanare de bază
    python3 ex_13_01_scanner_porturi.py --tinta 10.0.13.11 --porturi 1-1024
    
    # Scanare specifică cu export JSON
    python3 ex_13_01_scanner_porturi.py --tinta 10.0.13.11 --porturi 22,80,443,8080 --json-output scanare.json
    
    # Descoperire hosturi în rețea
    python3 ex_13_01_scanner_porturi.py --tinta 10.0.13.1-15 --mod descoperire
    
    # Scanare cu paralelism ridicat
    python3 ex_13_01_scanner_porturi.py --tinta 10.0.13.11 --porturi 1-65535 --workeri 200 --timeout 0.1

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
================================================================================
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ==============================================================================
# CONSTANTE ȘI CONFIGURARE
# ==============================================================================

# Porturi cunoscute și serviciile asociate (subset relevant)
PORTURI_CUNOSCUTE = {
    20: "FTP-Date",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1883: "MQTT",
    2121: "FTP-Alt",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6200: "Backdoor",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    8883: "MQTT-TLS",
    27017: "MongoDB",
}

# Culori ANSI pentru output
class Culori:
    ROSU = "\033[91m"
    VERDE = "\033[92m"
    GALBEN = "\033[93m"
    ALBASTRU = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# Dezactivează culorile când output-ul nu este TTY
try:
    if not sys.stdout.isatty():
        Culori.ROSU = ""
        Culori.VERDE = ""
        Culori.GALBEN = ""
        Culori.ALBASTRU = ""
        Culori.CYAN = ""
        Culori.RESET = ""
        Culori.BOLD = ""
except Exception:
    pass


# ==============================================================================
# STRUCTURI DE DATE
# ==============================================================================

@dataclass
class RezultatPort:
    """Rezultatul scanării unui port."""
    port: int
    stare: str  # 'deschis', 'inchis', 'filtrat'
    serviciu: str
    banner: Optional[str] = None
    timp_raspuns_ms: Optional[float] = None


@dataclass
class RezultatScanare:
    """Rezultatul complet al scanării."""
    tinta: str
    data_inceput: str
    data_sfarsit: str
    durata_secunde: float
    total_porturi: int
    porturi_deschise: int
    porturi_inchise: int
    porturi_filtrate: int
    rezultate: List[Dict]


# ==============================================================================
# FUNCȚII DE SCANARE
# ==============================================================================

def scaneaza_port(host: str, port: int, timeout: float = 1.0) -> RezultatPort:
    """
    Scanează un singur port folosind TCP connect.
    
    Procesul:
    1. Creează un socket TCP
    2. Încearcă să se conecteze la host:port
    3. Dacă reușește, portul este DESCHIS
    4. Dacă primește RST, portul este ÎNCHIS
    5. Dacă expiră timeout-ul, portul este FILTRAT
    
    Args:
        host: Adresa IP sau hostname țintă
        port: Numărul portului de scanat
        timeout: Timeout în secunde pentru conexiune
    
    Returns:
        RezultatPort cu informațiile colectate
    """
    serviciu = PORTURI_CUNOSCUTE.get(port, "necunoscut")
    banner = None
    timp_inceput = time.time()
    
    try:
        # Creează socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Încearcă conexiunea
        rezultat = sock.connect_ex((host, port))
        timp_raspuns = (time.time() - timp_inceput) * 1000  # în ms
        
        if rezultat == 0:
            # Port DESCHIS - încearcă să obții banner
            try:
                sock.settimeout(0.5)
                # Unele servicii trimit banner automat
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                if not banner:
                    # Încearcă cu request HTTP simplu
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').split('\n')[0].strip()
            except (socket.timeout, socket.error):
                pass
            
            return RezultatPort(
                port=port,
                stare="deschis",
                serviciu=serviciu,
                banner=banner[:100] if banner else None,
                timp_raspuns_ms=round(timp_raspuns, 2)
            )
        else:
            # Port ÎNCHIS
            return RezultatPort(
                port=port,
                stare="inchis",
                serviciu=serviciu,
                timp_raspuns_ms=round(timp_raspuns, 2)
            )
            
    except socket.timeout:
        # Port FILTRAT (niciun răspuns)
        return RezultatPort(
            port=port,
            stare="filtrat",
            serviciu=serviciu
        )
    except socket.error as e:
        # Eroare de conexiune - considerăm filtrat
        return RezultatPort(
            port=port,
            stare="filtrat",
            serviciu=serviciu
        )
    finally:
        try:
            sock.close()
        except Exception:
            pass


def parseaza_porturi(spec_porturi: str) -> List[int]:
    """
    Parsează specificația de porturi în listă de numere.
    
    Formate acceptate:
    - "80" -> [80]
    - "80,443,8080" -> [80, 443, 8080]
    - "1-100" -> [1, 2, ..., 100]
    - "22,80-85,443" -> [22, 80, 81, 82, 83, 84, 85, 443]
    
    Args:
        spec_porturi: Șir cu specificația porturilor
    
    Returns:
        Listă de numere de porturi
    """
    porturi = set()
    
    for parte in spec_porturi.split(','):
        parte = parte.strip()
        if '-' in parte:
            try:
                inceput, sfarsit = parte.split('-')
                for p in range(int(inceput), int(sfarsit) + 1):
                    if 1 <= p <= 65535:
                        porturi.add(p)
            except ValueError:
                print(f"[ATENȚIE] Format invalid interval: {parte}")
        else:
            try:
                p = int(parte)
                if 1 <= p <= 65535:
                    porturi.add(p)
            except ValueError:
                print(f"[ATENȚIE] Port invalid: {parte}")
    
    return sorted(porturi)


def parseaza_tinte(spec_tinta: str) -> List[str]:
    """
    Parsează specificația țintei în listă de adrese IP.
    
    Formate acceptate:
    - "192.168.1.1" -> ["192.168.1.1"]
    - "192.168.1.0/24" -> [toate IP-urile din subnet]
    - "192.168.1.1-10" -> ["192.168.1.1", ..., "192.168.1.10"]
    
    Args:
        spec_tinta: Șir cu specificația țintei
    
    Returns:
        Listă de adrese IP
    """
    tinte = []
    
    try:
        # Încearcă ca subnet CIDR
        retea = ipaddress.ip_network(spec_tinta, strict=False)
        for ip in retea.hosts():
            tinte.append(str(ip))
    except ValueError:
        # Încearcă ca interval (ex: 192.168.1.1-10)
        if '-' in spec_tinta:
            try:
                baza, interval = spec_tinta.rsplit('.', 1)
                parti_interval = interval.split('-')
                if len(parti_interval) == 2:
                    for i in range(int(parti_interval[0]), int(parti_interval[1]) + 1):
                        tinte.append(f"{baza}.{i}")
                else:
                    tinte.append(spec_tinta)
            except (ValueError, IndexError):
                tinte.append(spec_tinta)
        else:
            # Adresă simplă sau hostname
            tinte.append(spec_tinta)
    
    return tinte


def scaneaza_tinta(host: str, porturi: List[int], workeri: int = 50, 
                   timeout: float = 1.0, verbose: bool = True) -> RezultatScanare:
    """
    Scanează o țintă pe mai multe porturi concurent.
    
    Args:
        host: Adresa IP sau hostname țintă
        porturi: Lista de porturi de scanat
        workeri: Numărul de thread-uri concurente
        timeout: Timeout per port
        verbose: Afișează progresul în timp real
    
    Returns:
        RezultatScanare cu toate informațiile
    """
    data_inceput = datetime.now()
    rezultate = []
    
    deschise = 0
    inchise = 0
    filtrate = 0
    
    if verbose:
        print(f"\n{Culori.CYAN}[SCANARE]{Culori.RESET} Țintă: {host}")
        print(f"{Culori.CYAN}[SCANARE]{Culori.RESET} Porturi: {len(porturi)}")
        print(f"{Culori.CYAN}[SCANARE]{Culori.RESET} Workeri: {workeri}")
        print("-" * 50)
    
    with ThreadPoolExecutor(max_workers=workeri) as executor:
        # Trimite toate task-urile
        futures = {
            executor.submit(scaneaza_port, host, port, timeout): port
            for port in porturi
        }
        
        # Colectează rezultatele
        for future in as_completed(futures):
            rezultat = future.result()
            rezultate.append(asdict(rezultat))
            
            if rezultat.stare == "deschis":
                deschise += 1
                if verbose:
                    banner_info = f" - {rezultat.banner[:40]}..." if rezultat.banner else ""
                    print(f"{Culori.VERDE}[DESCHIS]{Culori.RESET} Port {rezultat.port:5} "
                          f"({rezultat.serviciu}){banner_info}")
            elif rezultat.stare == "inchis":
                inchise += 1
            else:
                filtrate += 1
    
    data_sfarsit = datetime.now()
    durata = (data_sfarsit - data_inceput).total_seconds()
    
    return RezultatScanare(
        tinta=host,
        data_inceput=data_inceput.isoformat(),
        data_sfarsit=data_sfarsit.isoformat(),
        durata_secunde=round(durata, 2),
        total_porturi=len(porturi),
        porturi_deschise=deschise,
        porturi_inchise=inchise,
        porturi_filtrate=filtrate,
        rezultate=sorted(rezultate, key=lambda x: x['port'])
    )


def afiseaza_sumar(rezultat: RezultatScanare):
    """Afișează sumarul scanării."""
    print("\n" + "=" * 50)
    print(f"{Culori.BOLD}SUMAR SCANARE{Culori.RESET}")
    print("=" * 50)
    print(f"Țintă:           {rezultat.tinta}")
    print(f"Durată:          {rezultat.durata_secunde} secunde")
    print(f"Total porturi:   {rezultat.total_porturi}")
    print(f"  {Culori.VERDE}Deschise:{Culori.RESET}      {rezultat.porturi_deschise}")
    print(f"  {Culori.ROSU}Închise:{Culori.RESET}       {rezultat.porturi_inchise}")
    print(f"  {Culori.GALBEN}Filtrate:{Culori.RESET}      {rezultat.porturi_filtrate}")
    print("=" * 50)


def salveaza_json(rezultat: RezultatScanare, fisier: str):
    """Salvează rezultatele în format JSON."""
    with open(fisier, 'w', encoding='utf-8') as f:
        json.dump(asdict(rezultat), f, indent=2, ensure_ascii=False)
    print(f"\n{Culori.CYAN}[INFO]{Culori.RESET} Rezultate salvate în: {fisier}")


# ==============================================================================
# FUNCȚIA PRINCIPALĂ
# ==============================================================================

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Scanner TCP Avansat - Laborator IoT și Securitate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Scanare porturi specifice
  python ex_13_01_scanner_porturi.py --tinta localhost --porturi 1883,8883,8080,2121,6200
  
  # Scanare interval cu export JSON
  python ex_13_01_scanner_porturi.py --tinta 10.0.13.11 --porturi 1-1000 --output scanare.json
  
  # Scanare rapidă cu mai mulți workeri
  python ex_13_01_scanner_porturi.py --tinta localhost --porturi 1-10000 --workeri 100 --timeout 0.5

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
        """
    )
    
    parser.add_argument("--tinta", "-t", required=True,
                        help="Ținta de scanat (IP, hostname, interval sau CIDR)")
    parser.add_argument("--porturi", "-p", default="1-1024",
                        help="Porturi de scanat (ex: 80,443 sau 1-1000)")
    parser.add_argument("--workeri", "-w", type=int, default=50,
                        help="Număr de thread-uri concurente (implicit: 50)")
    parser.add_argument("--timeout", type=float, default=1.0,
                        help="Timeout per port în secunde (implicit: 1.0)")
    parser.add_argument("--output", "-o",
                        help="Fișier JSON pentru salvarea rezultatelor")
    parser.add_argument("--silentios", "-s", action="store_true",
                        help="Mod silențios (doar porturi deschise)")
    parser.add_argument("--mod", choices=["scanare", "descoperire"], default="scanare",
                        help="Mod de operare")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"{Culori.BOLD}SCANNER TCP - LABORATOR SĂPTĂMÂNA 13{Culori.RESET}")
    print("IoT și Securitate în Rețelele de Calculatoare")
    print("=" * 60)
    
    # Parsează țintele și porturile
    tinte = parseaza_tinte(args.tinta)
    porturi = parseaza_porturi(args.porturi)
    
    if not porturi:
        print(f"{Culori.ROSU}[EROARE]{Culori.RESET} Niciun port valid specificat!")
        return 1
    
    print(f"\n{Culori.GALBEN}⚠️  AVERTISMENT: Utilizați doar pe sisteme autorizate!{Culori.RESET}\n")
    
    toate_rezultatele = []
    
    for tinta in tinte:
        rezultat = scaneaza_tinta(
            host=tinta,
            porturi=porturi,
            workeri=args.workeri,
            timeout=args.timeout,
            verbose=not args.silentios
        )
        
        afiseaza_sumar(rezultat)
        toate_rezultatele.append(rezultat)
    
    # Salvează în JSON dacă este specificat
    if args.output:
        if len(toate_rezultatele) == 1:
            salveaza_json(toate_rezultatele[0], args.output)
        else:
            # Salvează toate rezultatele
            toate_dict = [asdict(r) for r in toate_rezultatele]
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(toate_dict, f, indent=2, ensure_ascii=False)
            print(f"\n{Culori.CYAN}[INFO]{Culori.RESET} Rezultate salvate în: {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
