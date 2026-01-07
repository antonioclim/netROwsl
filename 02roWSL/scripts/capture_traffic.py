#!/usr/bin/env python3
"""
Captură Trafic de Rețea - Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Wrapper pentru tcpdump/tshark cu opțiuni simplificate.
"""

import subprocess
import sys
import argparse
import signal
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Adăugare rădăcină proiect la cale
RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))

from scripts.utils.logger import configurează_logger

logger = configurează_logger("captura")

# Proces global pentru oprire grațioasă
proces_captură: Optional[subprocess.Popen] = None


def handler_semnal(sig, frame):
    """Handler pentru semnale de întrerupere."""
    global proces_captură
    if proces_captură:
        logger.info("\nOprire captură...")
        proces_captură.terminate()
    sys.exit(0)


def generează_nume_fișier(prefix: str = "week2") -> str:
    """
    Generează un nume de fișier unic bazat pe timestamp.
    
    Args:
        prefix: Prefix pentru numele fișierului
        
    Returns:
        Nume de fișier în format prefix_YYYYMMDD_HHMMSS.pcap
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.pcap"


def construiește_filtru_bpf(
    porturi: Optional[List[int]] = None,
    protocol: Optional[str] = None,
    host: Optional[str] = None
) -> str:
    """
    Construiește un filtru BPF (Berkeley Packet Filter).
    
    Args:
        porturi: Lista de porturi de capturat
        protocol: Protocol (tcp, udp, icmp)
        host: Adresă host de filtrat
        
    Returns:
        String cu filtrul BPF
    """
    părți = []
    
    if protocol:
        părți.append(protocol.lower())
    
    if host:
        părți.append(f"host {host}")
    
    if porturi:
        filtru_porturi = " or ".join(f"port {p}" for p in porturi)
        if len(porturi) > 1:
            filtru_porturi = f"({filtru_porturi})"
        părți.append(filtru_porturi)
    
    return " and ".join(părți) if părți else ""


def captură_tcpdump(
    interfață: str,
    fișier_ieșire: str,
    filtru: str = "",
    nr_pachete: int = 0,
    verbose: bool = False
) -> int:
    """
    Rulează tcpdump pentru captură de pachete.
    
    Args:
        interfață: Interfața de rețea
        fișier_ieșire: Calea către fișierul de ieșire
        filtru: Filtru BPF opțional
        nr_pachete: Număr de pachete de capturat (0 = infinit)
        verbose: Mod verbose
        
    Returns:
        Cod de ieșire
    """
    global proces_captură
    
    cmd = ["docker", "exec", "week2_lab", "tcpdump"]
    
    # Opțiuni de bază
    cmd.extend(["-i", interfață])
    cmd.extend(["-w", f"/app/pcap/{Path(fișier_ieșire).name}"])
    
    # Număr de pachete
    if nr_pachete > 0:
        cmd.extend(["-c", str(nr_pachete)])
    
    # Verbose
    if verbose:
        cmd.append("-v")
    
    # Filtru BPF
    if filtru:
        cmd.append(filtru)
    
    logger.info(f"Comandă: {' '.join(cmd)}")
    logger.info(f"Fișier ieșire: {fișier_ieșire}")
    logger.info("Apăsați Ctrl+C pentru a opri captura...")
    logger.info("")
    
    try:
        proces_captură = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Afișare output în timp real
        for linie in proces_captură.stdout:
            print(f"  {linie.rstrip()}")
        
        proces_captură.wait()
        return proces_captură.returncode
        
    except FileNotFoundError:
        logger.error("Docker sau tcpdump nu a fost găsit!")
        logger.info("Asigurați-vă că Docker rulează și containerul week2_lab este activ.")
        return 1


def captură_tshark(
    interfață: str,
    fișier_ieșire: str,
    filtru: str = "",
    nr_pachete: int = 0,
    verbose: bool = False
) -> int:
    """
    Rulează tshark pentru captură de pachete.
    
    Args:
        interfață: Interfața de rețea
        fișier_ieșire: Calea către fișierul de ieșire
        filtru: Filtru de captură
        nr_pachete: Număr de pachete de capturat (0 = infinit)
        verbose: Mod verbose
        
    Returns:
        Cod de ieșire
    """
    global proces_captură
    
    cmd = ["docker", "exec", "week2_lab", "tshark"]
    
    # Opțiuni de bază
    cmd.extend(["-i", interfață])
    cmd.extend(["-w", f"/app/pcap/{Path(fișier_ieșire).name}"])
    
    # Număr de pachete
    if nr_pachete > 0:
        cmd.extend(["-c", str(nr_pachete)])
    
    # Verbose
    if verbose:
        cmd.append("-V")
    
    # Filtru
    if filtru:
        cmd.extend(["-f", filtru])
    
    logger.info(f"Comandă: {' '.join(cmd)}")
    logger.info(f"Fișier ieșire: {fișier_ieșire}")
    logger.info("Apăsați Ctrl+C pentru a opri captura...")
    logger.info("")
    
    try:
        proces_captură = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        for linie in proces_captură.stdout:
            print(f"  {linie.rstrip()}")
        
        proces_captură.wait()
        return proces_captură.returncode
        
    except FileNotFoundError:
        logger.error("Docker sau tshark nu a fost găsit!")
        return 1


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Captură Trafic de Rețea - Săptămâna 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  # Captură tot traficul pe interfața any
  python capture_traffic.py -i any -o captura.pcap
  
  # Captură doar trafic TCP pe portul 9090
  python capture_traffic.py --filter "tcp port 9090"
  
  # Captură 100 de pachete și oprește
  python capture_traffic.py -n 100 -o test.pcap
  
  # Utilizare tshark în loc de tcpdump
  python capture_traffic.py --tool tshark -i eth0

Filtre BPF utile:
  tcp port 9090           - Trafic TCP pe portul 9090
  udp port 9091           - Trafic UDP pe portul 9091
  host 10.0.2.10          - Trafic către/de la o adresă
  tcp and port 9090       - Combinație protocol și port
        """
    )
    
    parser.add_argument(
        "--interface", "-i",
        default="any",
        help="Interfața de captură (implicit: any)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Fișier de ieșire (implicit: generare automată)"
    )
    parser.add_argument(
        "--filter", "-f",
        default="",
        help="Filtru BPF pentru captură"
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=0,
        help="Număr de pachete de capturat (0 = infinit)"
    )
    parser.add_argument(
        "--tool", "-t",
        choices=["tcpdump", "tshark"],
        default="tcpdump",
        help="Instrumentul de captură (implicit: tcpdump)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        action="append",
        help="Port de filtrat (poate fi specificat de mai multe ori)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mod verbose"
    )
    
    args = parser.parse_args()

    # Instalare handler semnal
    signal.signal(signal.SIGINT, handler_semnal)
    signal.signal(signal.SIGTERM, handler_semnal)

    # Generare nume fișier dacă nu este specificat
    if args.output:
        fișier_ieșire = args.output
    else:
        fișier_ieșire = generează_nume_fișier()
    
    # Asigurare că fișierul se află în directorul pcap
    cale_pcap = RĂDĂCINĂ_PROIECT / "pcap"
    cale_pcap.mkdir(exist_ok=True)
    
    if not fișier_ieșire.endswith(".pcap"):
        fișier_ieșire += ".pcap"
    
    cale_completă = cale_pcap / Path(fișier_ieșire).name

    # Construire filtru
    filtru = args.filter
    if args.port and not filtru:
        filtru = construiește_filtru_bpf(porturi=args.port)

    logger.info("=" * 60)
    logger.info("Captură Trafic de Rețea - Săptămâna 2")
    logger.info("=" * 60)
    logger.info(f"Instrument: {args.tool}")
    logger.info(f"Interfață: {args.interface}")
    logger.info(f"Filtru: {filtru if filtru else '(fără filtru)'}")
    logger.info(f"Pachete: {args.count if args.count > 0 else 'infinit'}")
    logger.info("")

    # Rulare captură
    if args.tool == "tcpdump":
        return captură_tcpdump(
            args.interface,
            str(cale_completă),
            filtru,
            args.count,
            args.verbose
        )
    else:
        return captură_tshark(
            args.interface,
            str(cale_completă),
            filtru,
            args.count,
            args.verbose
        )


if __name__ == "__main__":
    sys.exit(main())
