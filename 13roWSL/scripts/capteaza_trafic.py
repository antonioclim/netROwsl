#!/usr/bin/env python3
"""
Script Captură Trafic de Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Wrapper pentru tcpdump/tshark cu filtre preconfigurate pentru laborator.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import signal
import os
from pathlib import Path
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("capteaza_trafic")

# Filtru BPF implicit pentru serviciile laboratorului
FILTRU_IMPLICIT = "tcp port 1883 or tcp port 8883 or tcp port 8080 or tcp port 2121 or tcp port 6200"

# Proces global pentru gestionarea semnalelor
proces_captare = None



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def handler_semnal(signum, frame):
    """Gestionează întreruperea graceful a capturii."""
    global proces_captare
    if proces_captare:
        logger.info("\nSe oprește captura...")
        proces_captare.terminate()
        proces_captare.wait()
    sys.exit(0)


def gaseste_interfata() -> str:
    """
    Încearcă să găsească interfața de rețea potrivită.
    
    Returns:
        Numele interfeței sau 'any' ca fallback
    """
    interfete_prioritate = ['eth0', 'ens33', 'enp0s3', 'docker0', 'any']
    
    try:
        rezultat = subprocess.run(
            ["ip", "link", "show"],
            capture_output=True,
            text=True
        )
        
        for interfata in interfete_prioritate:
            if interfata in rezultat.stdout:
                return interfata
    except FileNotFoundError:
        pass
    
    return "any"


def listeaza_interfete():
    """Afișează interfețele de rețea disponibile."""
    print("\nInterfețe de rețea disponibile:")
    print("-" * 40)
    
    try:
        rezultat = subprocess.run(
            ["ip", "-o", "link", "show"],
            capture_output=True,
            text=True
        )
        
        for linie in rezultat.stdout.strip().split('\n'):
            parti = linie.split(': ')
            if len(parti) >= 2:
                nume = parti[1].split('@')[0]
                print(f"  • {nume}")
    except FileNotFoundError:
        # Fallback pentru Windows
        try:
            rezultat = subprocess.run(
                ["netsh", "interface", "show", "interface"],
                capture_output=True,
                text=True
            )
            print(rezultat.stdout)
        except Exception:
            print("  Nu s-au putut lista interfețele")
    
    print("-" * 40)


def porneste_captarea(interfata: str, filtru: str, fisier_output: Path, 
                      durata: int = 0, numar_pachete: int = 0):
    """
    Pornește captura de trafic.
    
    Args:
        interfata: Interfața de captură
        filtru: Filtru BPF
        fisier_output: Calea către fișierul de ieșire .pcap
        durata: Durata capturii în secunde (0 = nelimitat)
        numar_pachete: Numărul de pachete de capturat (0 = nelimitat)
    """
    global proces_captare
    
    # Construiește comanda tcpdump
    comanda = [
        "tcpdump",
        "-i", interfata,
        "-w", str(fisier_output),
        "-n",  # Nu rezolva adresele
    ]
    
    if filtru:
        comanda.extend(filtru.split())
    
    if numar_pachete > 0:
        comanda.extend(["-c", str(numar_pachete)])
    
    logger.info(f"Pornire captură pe interfața: {interfata}")
    logger.info(f"Filtru: {filtru or 'niciunul'}")
    logger.info(f"Fișier ieșire: {fisier_output}")
    
    if durata > 0:
        logger.info(f"Durată: {durata} secunde")
    else:
        logger.info("Durată: nelimitată (Ctrl+C pentru oprire)")
    
    print("\n" + "=" * 50)
    print("CAPTURĂ ÎN CURS...")
    print("Apăsați Ctrl+C pentru a opri")
    print("=" * 50 + "\n")
    
    try:
        if durata > 0:
            # Captură cu timeout
            proces_captare = subprocess.Popen(comanda)
            proces_captare.wait(timeout=durata)
        else:
            # Captură nelimitată
            proces_captare = subprocess.Popen(comanda)
            proces_captare.wait()
    except subprocess.TimeoutExpired:
        proces_captare.terminate()
        proces_captare.wait()
        logger.info("Captură oprită după expirarea duratei")
    except KeyboardInterrupt:
        if proces_captare:
            proces_captare.terminate()
            proces_captare.wait()
        logger.info("Captură oprită de utilizator")
    
    # Verifică dimensiunea fișierului
    if fisier_output.exists():
        dimensiune = fisier_output.stat().st_size
        logger.info(f"Captură salvată: {fisier_output} ({dimensiune} bytes)")
        print(f"\nPentru a analiza captura:")
        print(f"  wireshark {fisier_output}")
        print(f"  tshark -r {fisier_output}")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Captură Trafic Rețea - Laborator Săptămâna 13",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python capteaza_trafic.py --durata 60
  python capteaza_trafic.py --filtru "tcp port 1883" --output captura_mqtt.pcap
  python capteaza_trafic.py --pachete 100 --interfata eth0
  python capteaza_trafic.py --listeaza-interfete
        """
    )
    
    parser.add_argument("--interfata", "-i", type=str,
                        help="Interfața de rețea pentru captură")
    parser.add_argument("--filtru", "-f", type=str, default=FILTRU_IMPLICIT,
                        help=f"Filtru BPF (implicit: porturi laborator)")
    parser.add_argument("--output", "-o", type=str,
                        help="Fișierul de ieșire .pcap")
    parser.add_argument("--durata", "-d", type=int, default=0,
                        help="Durata capturii în secunde (0=nelimitat)")
    parser.add_argument("--pachete", "-c", type=int, default=0,
                        help="Numărul de pachete de capturat")
    parser.add_argument("--listeaza-interfete", action="store_true",
                        help="Listează interfețele disponibile și iese")
    
    args = parser.parse_args()
    
    # Listare interfețe
    if args.listeaza_interfete:
        listeaza_interfete()
        return 0
    
    # Configurare handler pentru semnale
    signal.signal(signal.SIGINT, handler_semnal)
    signal.signal(signal.SIGTERM, handler_semnal)
    
    # Determină interfața
    interfata = args.interfata or gaseste_interfata()
    
    # Determină fișierul de ieșire
    if args.output:
        fisier_output = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        director_pcap = RADACINA_PROIECT / "pcap"
        director_pcap.mkdir(exist_ok=True)
        fisier_output = director_pcap / f"captura_{timestamp}.pcap"
    
    # Asigură-te că directorul părinte există
    fisier_output.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        porneste_captarea(
            interfata=interfata,
            filtru=args.filtru,
            fisier_output=fisier_output,
            durata=args.durata,
            numar_pachete=args.pachete
        )
        return 0
    except FileNotFoundError:
        logger.error("tcpdump nu este instalat sau nu este în PATH")
        logger.error("Instalați cu: sudo apt install tcpdump")
        return 1
    except PermissionError:
        logger.error("Permisiuni insuficiente. Rulați cu sudo/Administrator")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
