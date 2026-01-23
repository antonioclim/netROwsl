#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Adaugă rădăcina proiectului în path

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("curata")

PREFIX_SAPTAMANA = "week7"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def curata_director(director: Path, extensii: list[str] | None = None):
    """
    Curăță fișierele dintr-un director.
    
    Args:
        director: Calea către director
        extensii: Lista de extensii de curățat (None = toate)
    """
    if not director.exists():
        return
    
    fisiere_sterse = 0
    
    for fisier in director.iterdir():
        if fisier.name.startswith('.'):
            continue
        
        if fisier.is_file():
            if extensii is None or fisier.suffix in extensii:
                fisier.unlink()
                fisiere_sterse += 1
    
    if fisiere_sterse > 0:
        logger.info(f"  Șterse {fisiere_sterse} fișiere din {director.name}/")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Curățare mediu laborator Săptămâna 7"
    )
    parser.add_argument(
        "--complet",
        action="store_true",
        help="Elimină volumele și toate datele (folosiți înainte de săptămâna următoare)"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Curăță și resursele Docker neutilizate din sistem"
    )
    parser.add_argument(
        "--simulare",
        action="store_true",
        help="Afișează ce s-ar șterge fără a face modificări"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Curățare Mediu Laborator Săptămâna 7")
    logger.info("=" * 60)

    if args.simulare:
        logger.info("[SIMULARE] Nicio modificare nu va fi efectuată")
        logger.info("")

    try:
        # Oprire containere
        logger.info("Oprire containere...")
        docker.compose_down(volumes=args.complet, dry_run=args.simulare)

        # Eliminare resurse cu prefix specific
        logger.info(f"\nEliminare resurse {PREFIX_SAPTAMANA}_*...")
        docker.elimina_dupa_prefix(PREFIX_SAPTAMANA, dry_run=args.simulare)

        # Curățare artefacte
        if args.complet and not args.simulare:
            logger.info("\nCurățare directoare de lucru...")
            
            # Curăță directorul artifacts
            dir_artefacte = RADACINA_PROIECT / "artifacts"
            curata_director(dir_artefacte)
            
            # Curăță capturile pcap
            dir_pcap = RADACINA_PROIECT / "pcap"
            curata_director(dir_pcap, extensii=[".pcap", ".pcapng"])
            
            logger.info("  Directoarele au fost curățate")

        # Curățare sistem Docker (opțional)
        if args.prune and not args.simulare:
            logger.info("\nCurățare resurse Docker neutilizate...")
            docker.system_prune()

        # Sumar
        logger.info("")
        logger.info("=" * 60)
        if args.simulare:
            logger.info("[SIMULARE] Curățare completă (nicio modificare efectuată)")
        else:
            logger.info("Curățare completă!")
            if args.complet:
                logger.info("Sistemul este pregătit pentru următoarea sesiune de laborator.")
            else:
                logger.info("Notă: Volumele Docker au fost păstrate.")
                logger.info("      Pentru curățare totală, folosiți: --complet")
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
