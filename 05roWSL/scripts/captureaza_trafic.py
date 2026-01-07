#!/usr/bin/env python3
"""
Captură Trafic de Rețea - Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Acest script facilitează captura de pachete folosind tcpdump în containerele Docker
sau deschide Wireshark pentru analiză în timp real.
"""

import subprocess
import sys
import argparse
import signal
from pathlib import Path
from datetime import datetime

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("captureaza_trafic")

# Filtre predefinite pentru această săptămână
FILTRE_PREDEFINITE = {
    "udp": "udp port 9999",
    "icmp": "icmp",
    "ipv4": "ip",
    "ipv6": "ip6",
    "toate": "",
    "arp": "arp",
    "tcp": "tcp",
}


def obtine_timestamp() -> str:
    """Generează un timestamp pentru numele fișierului."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def captureaza_in_container(
    container: str,
    interfata: str,
    fisier_iesire: str,
    filtru: str = "",
    numar_pachete: int = 0,
    verbose: bool = False
):
    """
    Execută tcpdump într-un container Docker.
    
    Args:
        container: Numele containerului Docker
        interfata: Interfața de rețea de monitorizat
        fisier_iesire: Calea fișierului de ieșire (.pcap)
        filtru: Filtru BPF pentru tcpdump
        numar_pachete: Numărul de pachete de capturat (0 = nelimitat)
        verbose: Afișează informații detaliate
    """
    # Construiește comanda tcpdump
    cmd_tcpdump = ["tcpdump", "-i", interfata, "-w", f"/tmp/{Path(fisier_iesire).name}"]
    
    if numar_pachete > 0:
        cmd_tcpdump.extend(["-c", str(numar_pachete)])
    
    if verbose:
        cmd_tcpdump.append("-v")
    
    if filtru:
        cmd_tcpdump.append(filtru)

    # Comanda Docker completă
    cmd = ["docker", "exec", "-it", container] + cmd_tcpdump

    logger.info(f"Pornire captură în containerul '{container}'...")
    logger.info(f"Interfață: {interfata}")
    logger.info(f"Fișier ieșire: {fisier_iesire}")
    if filtru:
        logger.info(f"Filtru: {filtru}")
    logger.info("")
    logger.info("Apăsați Ctrl+C pentru a opri captura.")
    logger.info("-" * 40)

    try:
        proces = subprocess.Popen(cmd)
        proces.wait()
    except KeyboardInterrupt:
        logger.info("\nOprire captură...")
        proces.terminate()
        proces.wait()

    # Copiază fișierul din container
    logger.info(f"Copiere fișier de captură...")
    Path(fisier_iesire).parent.mkdir(parents=True, exist_ok=True)
    
    cmd_copiere = [
        "docker", "cp",
        f"{container}:/tmp/{Path(fisier_iesire).name}",
        fisier_iesire
    ]
    subprocess.run(cmd_copiere, check=True)
    
    logger.info(f"✓ Captură salvată în: {fisier_iesire}")


def deschide_wireshark(fisier: str = None):
    """
    Deschide Wireshark, opțional cu un fișier de captură.
    
    Args:
        fisier: Calea către fișierul .pcap de deschis
    """
    cale_wireshark = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
    
    if not cale_wireshark.exists():
        logger.error("Wireshark nu a fost găsit la calea standard.")
        logger.info("Instalați Wireshark de la: https://www.wireshark.org/")
        return False

    cmd = [str(cale_wireshark)]
    if fisier and Path(fisier).exists():
        cmd.append(fisier)

    logger.info("Deschidere Wireshark...")
    subprocess.Popen(cmd, start_new_session=True)
    return True


def listeaza_interfete(container: str):
    """Listează interfețele disponibile într-un container."""
    cmd = ["docker", "exec", container, "ip", "link", "show"]
    rezultat = subprocess.run(cmd, capture_output=True, text=True)
    
    if rezultat.returncode == 0:
        logger.info(f"Interfețe disponibile în '{container}':")
        print(rezultat.stdout)
    else:
        logger.error(f"Eroare la listarea interfețelor: {rezultat.stderr}")


def main():
    parser = argparse.ArgumentParser(
        description="Captură trafic de rețea pentru analiza laboratorului",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Filtre predefinite disponibile:
  {', '.join(FILTRE_PREDEFINITE.keys())}

Exemple:
  python captureaza_trafic.py --container week5_python --filtru udp
  python captureaza_trafic.py --container week5_python --filtru-personalizat "port 9999"
  python captureaza_trafic.py --wireshark pcap/captura.pcap
  python captureaza_trafic.py --listeaza-interfete week5_python
        """
    )
    
    parser.add_argument(
        "--container", "-c",
        default="week5_python",
        help="Containerul Docker pentru captură (implicit: week5_python)"
    )
    parser.add_argument(
        "--interfata", "-i",
        default="eth0",
        help="Interfața de rețea (implicit: eth0)"
    )
    parser.add_argument(
        "--iesire", "-o",
        help="Fișierul de ieșire .pcap (implicit: pcap/captura_TIMESTAMP.pcap)"
    )
    parser.add_argument(
        "--filtru", "-f",
        choices=list(FILTRE_PREDEFINITE.keys()),
        default="toate",
        help="Filtru predefinit (implicit: toate)"
    )
    parser.add_argument(
        "--filtru-personalizat",
        help="Filtru BPF personalizat (suprascrie --filtru)"
    )
    parser.add_argument(
        "--numar", "-n",
        type=int,
        default=0,
        help="Numărul de pachete de capturat (implicit: nelimitat)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate despre pachete"
    )
    parser.add_argument(
        "--wireshark", "-w",
        nargs="?",
        const="",
        help="Deschide Wireshark (opțional cu un fișier .pcap)"
    )
    parser.add_argument(
        "--listeaza-interfete",
        metavar="CONTAINER",
        help="Listează interfețele disponibile într-un container"
    )

    args = parser.parse_args()

    # Listează interfețele dacă este cerut
    if args.listeaza_interfete:
        listeaza_interfete(args.listeaza_interfete)
        return 0

    # Deschide Wireshark dacă este cerut
    if args.wireshark is not None:
        fisier = args.wireshark if args.wireshark else None
        deschide_wireshark(fisier)
        return 0

    # Determină fișierul de ieșire
    if args.iesire:
        fisier_iesire = args.iesire
    else:
        fisier_iesire = str(RADACINA_PROIECT / f"pcap/captura_{obtine_timestamp()}.pcap")

    # Determină filtrul
    if args.filtru_personalizat:
        filtru = args.filtru_personalizat
    else:
        filtru = FILTRE_PREDEFINITE.get(args.filtru, "")

    # Execută captura
    try:
        captureaza_in_container(
            container=args.container,
            interfata=args.interfata,
            fisier_iesire=fisier_iesire,
            filtru=filtru,
            numar_pachete=args.numar,
            verbose=args.verbose
        )
        
        # Întreabă dacă să deschidă în Wireshark
        raspuns = input("\nDoriți să deschideți captura în Wireshark? (da/nu): ")
        if raspuns.lower() in ('da', 'd', 'yes', 'y'):
            deschide_wireshark(fisier_iesire)
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Eroare la executarea comenzii: {e}")
        return 1
    except FileNotFoundError:
        logger.error("Docker nu a fost găsit. Asigurați-vă că Docker Desktop rulează.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
