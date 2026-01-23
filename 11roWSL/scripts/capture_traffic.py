#!/usr/bin/env python3
"""
Captură Trafic de Rețea
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest script ajută la capturarea traficului de rețea pentru analiză.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import signal
import shutil
from pathlib import Path
from datetime import datetime

# Adaugă rădăcina proiectului în path

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("capture_traffic")

# Variabilă globală pentru procesul de captură
proces_captura = None



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def handler_semnal(signum, frame):
    """Handler pentru oprirea grațioasă a capturii."""
    global proces_captura
    if proces_captura:
        logger.info("\nOprire captură...")
        proces_captura.terminate()
        proces_captura.wait()
    sys.exit(0)


def gaseste_instrument_captura() -> str | None:
    """
    Găsește instrumentul de captură disponibil.
    
    Returns:
        Numele instrumentului ('tshark', 'tcpdump') sau None
    """
    if shutil.which("tshark"):
        return "tshark"
    if shutil.which("tcpdump"):
        return "tcpdump"
    return None


def listeaza_interfete():
    """Listează interfețele de rețea disponibile."""
    instrument = gaseste_instrument_captura()
    
    if instrument == "tshark":
        subprocess.run(["tshark", "-D"])
    elif instrument == "tcpdump":
        subprocess.run(["tcpdump", "--list-interfaces"])
    else:
        logger.error("Nu s-a găsit niciun instrument de captură (tshark/tcpdump)")


def porneste_captura_tshark(
    interfata: str,
    fisier_output: Path,
    filtru: str | None = None,
    durata: int | None = None
) -> subprocess.Popen:
    """
    Pornește captura cu tshark.
    
    Args:
        interfata: Interfața de rețea
        fisier_output: Calea fișierului de ieșire
        filtru: Filtru de captură opțional
        durata: Durata în secunde (opțional)
    
    Returns:
        Procesul de captură
    """
    cmd = ["tshark", "-i", interfata, "-w", str(fisier_output)]
    
    if filtru:
        cmd.extend(["-f", filtru])
    
    if durata:
        cmd.extend(["-a", f"duration:{durata}"])
    
    logger.info(f"Comandă: {' '.join(cmd)}")
    return subprocess.Popen(cmd)


def porneste_captura_tcpdump(
    interfata: str,
    fisier_output: Path,
    filtru: str | None = None,
    durata: int | None = None
) -> subprocess.Popen:
    """
    Pornește captura cu tcpdump.
    
    Args:
        interfata: Interfața de rețea
        fisier_output: Calea fișierului de ieșire
        filtru: Filtru de captură opțional
        durata: Durata în secunde (nu este suportat direct)
    
    Returns:
        Procesul de captură
    """
    cmd = ["tcpdump", "-i", interfata, "-w", str(fisier_output)]
    
    if filtru:
        cmd.extend(filtru.split())
    
    logger.info(f"Comandă: {' '.join(cmd)}")
    
    if durata:
        logger.warning(f"tcpdump nu suportă durată; captura va rula până la Ctrl+C")
    
    return subprocess.Popen(cmd)


def analizeaza_captura(fisier_pcap: Path):
    """
    Analizează o captură existentă.
    
    Args:
        fisier_pcap: Calea către fișierul pcap
    """
    if not fisier_pcap.exists():
        logger.error(f"Fișierul nu există: {fisier_pcap}")
        return
    
    instrument = gaseste_instrument_captura()
    
    if instrument != "tshark":
        logger.error("tshark este necesar pentru analiză")
        return
    
    logger.info(f"\nAnalizăm {fisier_pcap}...")
    logger.info("=" * 60)
    
    # Numără pachetele
    result = subprocess.run(
        ["tshark", "-r", str(fisier_pcap), "-q", "-z", "io,stat,0"],
        capture_output=True,
        text=True
    )
    logger.info("Statistici generale:")
    logger.info(result.stdout)
    
    # Numără pachetele HTTP
    result = subprocess.run(
        ["tshark", "-r", str(fisier_pcap), "-Y", "http", "-q"],
        capture_output=True,
        text=True
    )
    pachete_http = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    logger.info(f"Pachete HTTP: {pachete_http}")
    
    # Numără pachetele DNS
    result = subprocess.run(
        ["tshark", "-r", str(fisier_pcap), "-Y", "dns", "-q"],
        capture_output=True,
        text=True
    )
    pachete_dns = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    logger.info(f"Pachete DNS: {pachete_dns}")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    global proces_captura
    
    parser = argparse.ArgumentParser(
        description="Captură trafic de rețea pentru laboratorul Săptămânii 11"
    )
    parser.add_argument(
        "--interface", "--interfata", "-i",
        default="any",
        help="Interfața de captură (implicit: any)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Fișierul de ieșire (implicit: pcap/week11_TIMESTAMP.pcap)"
    )
    parser.add_argument(
        "--filter", "--filtru", "-f",
        help="Filtru de captură (ex: 'tcp port 8080')"
    )
    parser.add_argument(
        "--duration", "--durata", "-d",
        type=int,
        help="Durata capturii în secunde"
    )
    parser.add_argument(
        "--list", "--listeaza",
        action="store_true",
        help="Listează interfețele disponibile"
    )
    parser.add_argument(
        "--analyze", "--analizeaza", "-a",
        help="Analizează un fișier pcap existent"
    )
    args = parser.parse_args()

    # Configurează handler pentru SIGINT
    signal.signal(signal.SIGINT, handler_semnal)

    # Listează interfețele
    if args.list:
        logger.info("Interfețe disponibile:")
        listeaza_interfete()
        return 0

    # Analizează fișier existent
    if args.analyze:
        analizeaza_captura(Path(args.analyze))
        return 0

    # Verifică dacă există instrument de captură
    instrument = gaseste_instrument_captura()
    if not instrument:
        logger.error("Nu s-a găsit niciun instrument de captură!")
        logger.error("Instalați Wireshark (pentru tshark) sau tcpdump")
        return 1

    logger.info(f"Folosim instrumentul: {instrument}")

    # Determină fișierul de ieșire
    if args.output:
        fisier_output = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        director_pcap = RADACINA_PROIECT / "pcap"
        director_pcap.mkdir(exist_ok=True)
        fisier_output = director_pcap / f"week11_{timestamp}.pcap"

    logger.info("=" * 60)
    logger.info("Captură Trafic de Rețea")
    logger.info("=" * 60)
    logger.info(f"Interfață: {args.interface}")
    logger.info(f"Fișier:    {fisier_output}")
    if args.filter:
        logger.info(f"Filtru:    {args.filter}")
    if args.duration:
        logger.info(f"Durată:    {args.duration} secunde")
    else:
        logger.info("Durată:    Până la Ctrl+C")
    logger.info("")
    logger.info("Pornire captură... (Ctrl+C pentru oprire)")
    logger.info("")

    try:
        # Pornește captura
        if instrument == "tshark":
            proces_captura = porneste_captura_tshark(
                args.interface, fisier_output, args.filter, args.duration
            )
        else:
            proces_captura = porneste_captura_tcpdump(
                args.interface, fisier_output, args.filter, args.duration
            )

        # Așteaptă finalizarea
        proces_captura.wait()

        logger.info("")
        logger.info(f"✓ Captură salvată: {fisier_output}")
        logger.info(f"  Dimensiune: {fisier_output.stat().st_size / 1024:.1f} KB")
        
        # Oferă să analizeze
        if instrument == "tshark":
            logger.info("")
            analizeaza_captura(fisier_output)

        return 0

    except Exception as e:
        logger.error(f"Eroare la captură: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
