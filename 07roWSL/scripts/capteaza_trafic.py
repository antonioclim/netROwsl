#!/usr/bin/env python3
"""
Instrument de Captură Trafic
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Script pentru capturarea traficului de rețea folosind tcpdump sau tshark.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# Adaugă rădăcina proiectului în path

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("capteaza_trafic")



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_instrument(nume: str) -> bool:
    """Verifică dacă un instrument este disponibil."""
    try:
        rezultat = subprocess.run(
            ["which", nume] if sys.platform != "win32" else ["where", nume],
            capture_output=True,
            timeout=5
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def capteaza_cu_tcpdump(
    interfata: str,
    fisier_iesire: Path,
    durata: int,
    filtru_bpf: str | None = None
) -> bool:
    """
    Capturează trafic folosind tcpdump.
    
    Args:
        interfata: Interfața de rețea
        fisier_iesire: Calea către fișierul de ieșire
        durata: Durata capturii în secunde
        filtru_bpf: Filtru BPF opțional
    
    Returns:
        True dacă captura a reușit
    """
    comanda = [
        "tcpdump",
        "-i", interfata,
        "-w", str(fisier_iesire),
        "-c", "10000",  # Număr maxim de pachete
    ]
    
    if filtru_bpf:
        comanda.extend(filtru_bpf.split())
    
    logger.info(f"Pornire captură pe interfața {interfata}")
    logger.info(f"Fișier de ieșire: {fisier_iesire}")
    logger.info(f"Durată: {durata} secunde")
    if filtru_bpf:
        logger.info(f"Filtru BPF: {filtru_bpf}")
    
    logger.info("")
    logger.info("Apăsați Ctrl+C pentru a opri captura mai devreme")
    logger.info("")
    
    try:
        proces = subprocess.Popen(
            comanda,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        timp_start = time.time()
        while time.time() - timp_start < durata:
            if proces.poll() is not None:
                break
            time.sleep(1)
            secunde_ramase = int(durata - (time.time() - timp_start))
            print(f"\r  Captură în curs... {secunde_ramase}s rămase  ", end="", flush=True)
        
        proces.terminate()
        print()
        
        logger.info(f"Captură salvată în: {fisier_iesire}")
        return True
        
    except KeyboardInterrupt:
        proces.terminate()
        print()
        logger.info("Captură oprită de utilizator")
        return True
    except Exception as e:
        logger.error(f"Eroare la captură: {e}")
        return False


def capteaza_cu_tshark(
    interfata: str,
    fisier_iesire: Path,
    durata: int,
    filtru_display: str | None = None
) -> bool:
    """
    Capturează trafic folosind tshark.
    
    Args:
        interfata: Interfața de rețea
        fisier_iesire: Calea către fișierul de ieșire
        durata: Durata capturii în secunde
        filtru_display: Filtru de afișare opțional
    
    Returns:
        True dacă captura a reușit
    """
    comanda = [
        "tshark",
        "-i", interfata,
        "-w", str(fisier_iesire),
        "-a", f"duration:{durata}",
    ]
    
    if filtru_display:
        comanda.extend(["-Y", filtru_display])
    
    logger.info(f"Pornire captură tshark pe interfața {interfata}")
    logger.info(f"Fișier de ieșire: {fisier_iesire}")
    logger.info(f"Durată: {durata} secunde")
    
    try:
        rezultat = subprocess.run(
            comanda,
            capture_output=True,
            timeout=durata + 10
        )
        
        if rezultat.returncode == 0:
            logger.info(f"Captură salvată în: {fisier_iesire}")
            return True
        else:
            logger.error(f"Eroare tshark: {rezultat.stderr.decode()}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.info(f"Captură finalizată (timeout)")
        return True
    except Exception as e:
        logger.error(f"Eroare la captură: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Capturează trafic de rețea pentru laboratorul Săptămânii 7"
    )
    parser.add_argument(
        "--interfata", "-i",
        default="eth0",
        help="Interfața de rețea (implicit: eth0)"
    )
    parser.add_argument(
        "--iesire", "-o",
        type=Path,
        help="Calea către fișierul de ieșire (implicit: pcap/captura_TIMESTAMP.pcap)"
    )
    parser.add_argument(
        "--durata", "-d",
        type=int,
        default=60,
        help="Durata capturii în secunde (implicit: 60)"
    )
    parser.add_argument(
        "--filtru", "-f",
        help="Filtru BPF (pentru tcpdump) sau filtru de afișare (pentru tshark)"
    )
    parser.add_argument(
        "--instrument",
        choices=["tcpdump", "tshark", "auto"],
        default="auto",
        help="Instrumentul de folosit (implicit: auto)"
    )
    parser.add_argument(
        "--listeaza-interfete",
        action="store_true",
        help="Listează interfețele de rețea disponibile"
    )
    args = parser.parse_args()

    # Listare interfețe
    if args.listeaza_interfete:
        logger.info("Interfețe de rețea disponibile:")
        try:
            if verifica_instrument("tshark"):
                subprocess.run(["tshark", "-D"])
            elif verifica_instrument("tcpdump"):
                subprocess.run(["tcpdump", "--list-interfaces"])
            else:
                logger.error("Niciun instrument de captură disponibil")
        except Exception as e:
            logger.error(f"Eroare: {e}")
        return 0

    # Determinare fișier de ieșire
    if args.iesire:
        fisier_iesire = args.iesire
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_pcap = RADACINA_PROIECT / "pcap"
        dir_pcap.mkdir(exist_ok=True)
        fisier_iesire = dir_pcap / f"captura_{timestamp}.pcap"

    # Determinare instrument
    instrument = args.instrument
    if instrument == "auto":
        if verifica_instrument("tcpdump"):
            instrument = "tcpdump"
        elif verifica_instrument("tshark"):
            instrument = "tshark"
        else:
            logger.error("Niciun instrument de captură disponibil!")
            logger.error("Instalați tcpdump sau Wireshark (tshark)")
            return 1

    logger.info("=" * 60)
    logger.info("Captură Trafic Săptămâna 7")
    logger.info("=" * 60)

    # Executare captură
    if instrument == "tcpdump":
        ok = capteaza_cu_tcpdump(
            args.interfata,
            fisier_iesire,
            args.durata,
            args.filtru
        )
    else:
        ok = capteaza_cu_tshark(
            args.interfata,
            fisier_iesire,
            args.durata,
            args.filtru
        )

    if ok:
        logger.info("")
        logger.info("=" * 60)
        logger.info("Captură finalizată cu succes!")
        logger.info(f"Deschideți în Wireshark: {fisier_iesire}")
        logger.info("=" * 60)
        return 0
    else:
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
