#!/usr/bin/env python3
"""
Asistent Captură Trafic de Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script facilitează captura de pachete folosind tcpdump în containerul Docker.
"""

from __future__ import annotations

import subprocess
import sys
import signal
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("captura_trafic")

# Procesul de captură global pentru gestionarea semnalelor
proces_captura: Optional[subprocess.Popen] = None


def handler_semnal(sig: int, frame) -> None:
    """Gestionează întreruperea pentru oprire grațioasă."""
    global proces_captura
    
    logger.info("\nSe oprește captura...")
    if proces_captura:
        proces_captura.terminate()
        try:
            proces_captura.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proces_captura.kill()


def construieste_filtru_bpf(
    port: Optional[int] = None,
    gazda: Optional[str] = None,
    protocol: Optional[str] = None
) -> str:
    """Construiește un filtru BPF din parametrii dați.
    
    Args:
        port: Numărul portului de filtrat
        gazda: Adresa IP sau hostname de filtrat
        protocol: Protocolul de filtrat (tcp, udp, icmp)
        
    Returns:
        Șirul filtrului BPF
    """
    conditii = []
    
    if port:
        conditii.append(f"port {port}")
    
    if gazda:
        conditii.append(f"host {gazda}")
    
    if protocol:
        conditii.append(protocol.lower())
    
    return " and ".join(conditii) if conditii else ""


def porneste_captura(
    interfata: str,
    fisier_iesire: Path,
    filtru: str = "",
    numar_pachete: Optional[int] = None,
    durata: Optional[int] = None,
    container: str = "week1_lab"
) -> int:
    """Pornește captura de trafic în container.
    
    Args:
        interfata: Interfața de rețea pentru captură
        fisier_iesire: Calea fișierului PCAP de ieșire
        filtru: Filtru BPF opțional
        numar_pachete: Număr maxim de pachete de capturat
        durata: Durata maximă a capturii în secunde
        container: Numele containerului Docker
        
    Returns:
        Codul de ieșire
    """
    global proces_captura
    
    # Construiește comanda tcpdump
    cmd_tcpdump = [
        "tcpdump",
        "-i", interfata,
        "-w", f"/work/pcap/{fisier_iesire.name}",
        "-U",  # Scriere imediată în fișier
    ]
    
    if numar_pachete:
        cmd_tcpdump.extend(["-c", str(numar_pachete)])
    
    if filtru:
        cmd_tcpdump.append(filtru)
    
    # Construiește comanda Docker
    cmd_docker = [
        "docker", "exec",
        container
    ] + cmd_tcpdump
    
    logger.info("=" * 60)
    logger.info("Pornire Captură Trafic")
    logger.info("=" * 60)
    logger.info(f"  Interfață: {interfata}")
    logger.info(f"  Fișier:    {fisier_iesire}")
    if filtru:
        logger.info(f"  Filtru:    {filtru}")
    if numar_pachete:
        logger.info(f"  Pachete:   maxim {numar_pachete}")
    if durata:
        logger.info(f"  Durată:    maxim {durata} secunde")
    logger.info("")
    logger.info("Apăsați Ctrl+C pentru a opri captura...")
    logger.info("=" * 60)
    
    try:
        # Configurează handler-ul de semnal
        signal.signal(signal.SIGINT, handler_semnal)
        signal.signal(signal.SIGTERM, handler_semnal)
        
        # Pornește captura
        proces_captura = subprocess.Popen(
            cmd_docker,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Așteaptă terminarea sau timeout
        if durata:
            try:
                proces_captura.wait(timeout=durata)
            except subprocess.TimeoutExpired:
                logger.info(f"\nDurată maximă ({durata}s) atinsă")
                proces_captura.terminate()
                proces_captura.wait(timeout=5)
        else:
            proces_captura.wait()
        
        # Copiază fișierul din container în directorul local
        cale_locala = RADACINA_PROIECT / "pcap" / fisier_iesire.name
        rezultat = subprocess.run([
            "docker", "cp",
            f"{container}:/work/pcap/{fisier_iesire.name}",
            str(cale_locala)
        ], capture_output=True)
        
        logger.info("")
        logger.info("=" * 60)
        if cale_locala.exists():
            dimensiune = cale_locala.stat().st_size
            logger.info(f"✓ Captură salvată: {cale_locala}")
            logger.info(f"  Dimensiune: {dimensiune:,} octeți")
            logger.info("")
            logger.info("Pentru a analiza captura:")
            logger.info(f"  tshark -r {cale_locala}")
            logger.info(f"  wireshark {cale_locala}")
        else:
            logger.warning("⚠ Fișierul de captură nu a fost găsit")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Eroare la captură: {e}")
        return 1


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Asistent Captură Trafic de Rețea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Captură de bază pe loopback
  python captura_trafic.py -i lo -o captura.pcap
  
  # Captură filtrată pe port
  python captura_trafic.py -i any --port 9090 -o tcp_captura.pcap
  
  # Captură cu limită de pachete
  python captura_trafic.py -i lo -c 100 -o test.pcap
  
  # Captură cu durată maximă
  python captura_trafic.py -i any --durata 60 -o sesiune.pcap

Filtre BPF comune:
  port 80          - Trafic HTTP
  tcp port 9090    - Trafic TCP pe port specific
  udp              - Tot traficul UDP
  host 192.168.1.1 - Trafic de la/către o adresă
        """
    )
    parser.add_argument(
        "-i", "--interfata",
        default="any",
        help="Interfața de rețea (implicit: any)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Fișierul PCAP de ieșire"
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        help="Numărul maxim de pachete de capturat"
    )
    parser.add_argument(
        "--durata",
        type=int,
        help="Durata maximă a capturii în secunde"
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Filtrează după numărul portului"
    )
    parser.add_argument(
        "--gazda",
        help="Filtrează după adresa IP sau hostname"
    )
    parser.add_argument(
        "--protocol",
        choices=["tcp", "udp", "icmp"],
        help="Filtrează după protocol"
    )
    parser.add_argument(
        "--filtru",
        help="Filtru BPF personalizat (suprascrie alte filtre)"
    )
    parser.add_argument(
        "--container",
        default="week1_lab",
        help="Numele containerului Docker (implicit: week1_lab)"
    )
    args = parser.parse_args()

    # Generează numele fișierului dacă nu este specificat
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = Path(f"captura_{timestamp}.pcap")
    
    # Asigură extensia .pcap
    if args.output.suffix.lower() != ".pcap":
        args.output = args.output.with_suffix(".pcap")

    # Construiește filtrul
    if args.filtru:
        filtru = args.filtru
    else:
        filtru = construieste_filtru_bpf(args.port, args.gazda, args.protocol)

    return porneste_captura(
        interfata=args.interfata,
        fisier_iesire=args.output,
        filtru=filtru,
        numar_pachete=args.count,
        durata=args.durata,
        container=args.container
    )


if __name__ == "__main__":
    sys.exit(main())
