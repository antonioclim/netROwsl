#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 11
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import signal
from pathlib import Path

# Adaugă rădăcina proiectului în path

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("cleanup")

PREFIX_SAPTAMANA = "s11"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def curata_artefacte():
    """Elimină fișierele din directorul artifacts/."""
    director_artefacte = RADACINA_PROIECT / "artifacts"
    
    if not director_artefacte.exists():
        return
    
    fisiere_eliminate = 0
    for fisier in director_artefacte.glob("*"):
        if fisier.name != ".gitkeep":
            fisier.unlink()
            fisiere_eliminate += 1
    
    if fisiere_eliminate > 0:
        logger.info(f"  ✓ {fisiere_eliminate} fișiere artefact eliminate")


def curata_pcap():
    """Elimină fișierele .pcap din directorul pcap/."""
    director_pcap = RADACINA_PROIECT / "pcap"
    
    if not director_pcap.exists():
        return
    
    fisiere_eliminate = 0
    for fisier in director_pcap.glob("*.pcap"):
        fisier.unlink()
        fisiere_eliminate += 1
    
    if fisiere_eliminate > 0:
        logger.info(f"  ✓ {fisiere_eliminate} fișiere pcap eliminate")


def opreste_procese_python():
    """Oprește procesele Python legate de exerciții."""
    import os
    
    try:
        # Pe Windows
        if sys.platform == "win32":
            # Găsește procesele care rulează scripturile de exerciții
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
                capture_output=True,
                text=True
            )
            # Avertizează utilizatorul
            logger.info("  ℹ Verificați manual procesele Python care rulează exercițiile")
        else:
            # Pe Linux/macOS
            subprocess.run(
                ["pkill", "-f", "ex_11_"],
                capture_output=True
            )
            logger.info("  ✓ Procese Python de exerciții oprite")
    except Exception as e:
        logger.warning(f"  ⚠ Nu s-au putut opri procesele Python: {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Curățare mediu laborator Săptămâna 11"
    )
    parser.add_argument(
        "--full", "--complet",
        action="store_true",
        help="Eliminare completă (inclusiv volume și date)"
    )
    parser.add_argument(
        "--prune", "--curata-sistem",
        action="store_true",
        help="Curăță și resursele Docker neutilizate"
    )
    parser.add_argument(
        "--dry-run", "--simulare",
        action="store_true",
        help="Arată ce ar fi eliminat fără a efectua operațiunile"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Curățare Mediu Laborator Săptămâna 11")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("[SIMULARE] Nu se vor efectua modificări")
        print()

    try:
        # Oprește containerele
        logger.info("\n[1/5] Oprire containere...")
        if not args.dry_run:
            docker.compose_down(volumes=args.full)
        logger.info("  ✓ Containere oprite")

        # Elimină resursele cu prefixul săptămânii
        logger.info(f"\n[2/5] Eliminare resurse {PREFIX_SAPTAMANA}_*...")
        if not args.dry_run:
            docker.elimina_dupa_prefix(PREFIX_SAPTAMANA)
        logger.info("  ✓ Resurse Docker eliminate")

        # Curăță artefactele
        logger.info("\n[3/5] Curățare directoare...")
        if args.full and not args.dry_run:
            curata_artefacte()
            curata_pcap()
        elif args.full:
            logger.info("  [SIMULARE] Ar fi eliminate fișierele din artifacts/ și pcap/")
        else:
            logger.info("  ℹ Omis (folosiți --full pentru curățare completă)")

        # Oprește procesele Python
        logger.info("\n[4/5] Oprire procese exerciții...")
        if not args.dry_run:
            opreste_procese_python()
        else:
            logger.info("  [SIMULARE] Ar fi oprite procesele ex_11_*")

        # Curățare sistem Docker opțională
        logger.info("\n[5/5] Curățare sistem Docker...")
        if args.prune and not args.dry_run:
            docker.curata_sistem()
            logger.info("  ✓ Resurse Docker neutilizate eliminate")
        elif args.prune:
            logger.info("  [SIMULARE] Ar fi curățate resursele neutilizate")
        else:
            logger.info("  ℹ Omis (folosiți --prune pentru curățare sistem)")

        # Afișează spațiul recuperat
        if not args.dry_run:
            logger.info("\nSpațiu disc Docker:")
            subprocess.run(["docker", "system", "df"])

        logger.info("")
        logger.info("=" * 60)
        logger.info("Curățare finalizată!")
        if args.full:
            logger.info("Sistemul este pregătit pentru următoarea sesiune de laborator.")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Eroare la curățare: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
