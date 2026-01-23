#!/usr/bin/env python3
"""
Captură Trafic de Rețea
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Asistent pentru capturarea traficului de rețea din containere folosind tcpdump.

Utilizare:
    python scripts/captureaza_trafic.py --container server --durata 30
    python scripts/captureaza_trafic.py --container client --filtru "port 5007" --output captura.pcap
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import time
import shutil
from pathlib import Path
from datetime import datetime

# Adaugă rădăcina proiectului în PATH

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("captureaza_trafic")



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_container(nume: str) -> bool:
    """Verifică dacă containerul există și rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", f"week3_{nume}"],
            capture_output=True,
            timeout=10
        )
        return "true" in rezultat.stdout.decode().lower()
    except Exception:
        return False


def porneste_captura(container: str, interfata: str, filtru: str,
                     durata: int, fisier_output: str) -> bool:
    """
    Pornește captura tcpdump în container.
    
    Args:
        container: Numele containerului (fără prefix week3_)
        interfata: Interfața de rețea (implicit eth0)
        filtru: Filtru tcpdump (opțional)
        durata: Durata capturii în secunde
        fisier_output: Calea fișierului de ieșire
        
    Returns:
        True dacă captura a reușit
    """
    nume_container = f"week3_{container}"
    fisier_temporar = f"/tmp/captura_{container}.pcap"
    
    # Construiește comanda tcpdump
    cmd_tcpdump = ["tcpdump", "-i", interfata, "-w", fisier_temporar]
    
    if filtru:
        cmd_tcpdump.extend(filtru.split())
    
    # Adaugă limită de timp (aproximativă - tcpdump nu are timeout nativ)
    # Vom folosi timeout la nivel de subprocess
    
    logger.info(f"Pornire captură în {nume_container}...")
    logger.info(f"  Interfață: {interfata}")
    logger.info(f"  Filtru: {filtru or '(niciunul)'}")
    logger.info(f"  Durată: {durata} secunde")
    logger.info(f"  Fișier: {fisier_output}")
    logger.info("")
    logger.info("Captură în curs... (Ctrl+C pentru oprire manuală)")
    
    try:
        # Rulează tcpdump în container
        proces = subprocess.Popen(
            ["docker", "exec", nume_container] + cmd_tcpdump,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Așteaptă durata specificată
        try:
            proces.wait(timeout=durata)
        except subprocess.TimeoutExpired:
            # Oprește tcpdump
            subprocess.run(
                ["docker", "exec", nume_container, "pkill", "-SIGINT", "tcpdump"],
                capture_output=True
            )
            time.sleep(1)
            proces.terminate()
        
        # Copiază fișierul din container
        logger.info("\nCopiere fișier captură...")
        rezultat = subprocess.run(
            ["docker", "cp", f"{nume_container}:{fisier_temporar}", fisier_output],
            capture_output=True
        )
        
        if rezultat.returncode == 0:
            # Verifică dimensiunea fișierului
            cale = Path(fisier_output)
            if cale.exists():
                dimensiune = cale.stat().st_size
                logger.info(f"✓ Captură salvată: {fisier_output} ({dimensiune} bytes)")
                
                # Curăță fișierul temporar
                subprocess.run(
                    ["docker", "exec", nume_container, "rm", "-f", fisier_temporar],
                    capture_output=True
                )
                return True
            else:
                logger.error("Fișierul de captură nu a fost creat")
                return False
        else:
            logger.error(f"Eroare la copierea fișierului: {rezultat.stderr.decode()}")
            return False
            
    except KeyboardInterrupt:
        logger.info("\nCaptură oprită de utilizator")
        # Încearcă să oprească tcpdump și să salveze captura
        subprocess.run(
            ["docker", "exec", nume_container, "pkill", "-SIGINT", "tcpdump"],
            capture_output=True
        )
        time.sleep(1)
        subprocess.run(
            ["docker", "cp", f"{nume_container}:{fisier_temporar}", fisier_output],
            capture_output=True
        )
        return True
    except Exception as e:
        logger.error(f"Eroare la captură: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Captură trafic de rețea din containerele de laborator"
    )
    parser.add_argument(
        "--container", "-c",
        type=str,
        default="server",
        choices=["server", "router", "client", "receiver"],
        help="Containerul din care se capturează (implicit: server)"
    )
    parser.add_argument(
        "--interfata", "-i",
        type=str,
        default="eth0",
        help="Interfața de rețea (implicit: eth0)"
    )
    parser.add_argument(
        "--filtru", "-f",
        type=str,
        default="",
        help="Filtru tcpdump (ex: 'port 5007', 'udp', 'host 172.20.0.10')"
    )
    parser.add_argument(
        "--durata", "-d",
        type=int,
        default=30,
        help="Durata capturii în secunde (implicit: 30)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Calea fișierului de ieșire (implicit: pcap/week3_<container>_<timestamp>.pcap)"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Captură Trafic de Rețea - Săptămâna 3")
    logger.info("=" * 60)

    # Verifică containerul
    if not verifica_container(args.container):
        logger.error(f"Containerul week3_{args.container} nu rulează!")
        logger.error("Porniți laboratorul: python scripts/porneste_lab.py")
        return 1

    # Generează numele fișierului de ieșire dacă nu este specificat
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        director_pcap = RADACINA_PROIECT / "pcap"
        director_pcap.mkdir(exist_ok=True)
        args.output = str(director_pcap / f"week3_{args.container}_{timestamp}.pcap")

    # Asigură că directorul există
    cale_output = Path(args.output)
    cale_output.parent.mkdir(parents=True, exist_ok=True)

    # Pornește captura
    succes = porneste_captura(
        container=args.container,
        interfata=args.interfata,
        filtru=args.filtru,
        durata=args.durata,
        fisier_output=args.output
    )

    if succes:
        logger.info("")
        logger.info("Pentru a vizualiza captura:")
        logger.info(f"  1. Deschideți Wireshark")
        logger.info(f"  2. File → Open → {args.output}")
        return 0
    else:
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
