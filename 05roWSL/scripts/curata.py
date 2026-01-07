#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""

import subprocess
import sys
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("curata")

PREFIX_SAPTAMANA = "week5"


def confirma_actiune(mesaj: str) -> bool:
    """Cere confirmarea utilizatorului pentru acțiuni distructive."""
    while True:
        raspuns = input(f"{mesaj} (da/nu): ").lower().strip()
        if raspuns in ('da', 'd', 'yes', 'y'):
            return True
        elif raspuns in ('nu', 'n', 'no'):
            return False
        print("Vă rog răspundeți cu 'da' sau 'nu'.")


def main():
    parser = argparse.ArgumentParser(
        description="Curățare mediu de laborator Săptămâna 5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Niveluri de curățare:
  Implicit:     Oprește containerele, păstrează volumele
  --complet:    Elimină și volumele (folosiți înainte de săptămâna următoare)
  --curata-tot: Curăță și resursele Docker neutilizate (prune)

Exemple:
  python curata.py                    # Curățare de bază
  python curata.py --complet          # Curățare completă cu volume
  python curata.py --complet --fortat # Fără confirmare
  python curata.py --simulare         # Afișează ce s-ar șterge
        """
    )
    parser.add_argument(
        "--complet", 
        action="store_true",
        help="Elimină volumele și toate datele (folosiți înainte de săptămâna următoare)"
    )
    parser.add_argument(
        "--curata-tot", 
        action="store_true",
        help="Curăță și resursele Docker neutilizate (prune)"
    )
    parser.add_argument(
        "--simulare", 
        action="store_true",
        help="Afișează ce s-ar elimina fără a face modificări"
    )
    parser.add_argument(
        "--fortat", "-f",
        action="store_true",
        help="Nu cere confirmare pentru acțiuni distructive"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Curățare mediu de laborator Săptămâna 5")
    logger.info("=" * 60)

    if args.simulare:
        logger.info("[SIMULARE] Nu se vor face modificări")

    try:
        # Confirmă acțiunile distructive
        if args.complet and not args.fortat and not args.simulare:
            logger.warning("⚠ Curățarea completă va șterge toate datele!")
            if not confirma_actiune("Sigur doriți să continuați?"):
                logger.info("Operațiune anulată de utilizator.")
                return 0

        # Oprește și elimină containerele
        logger.info("Oprire containere...")
        docker.compose_down(volume=args.complet, simulare=args.simulare)

        # Elimină resursele specifice săptămânii
        logger.info(f"Eliminare resurse {PREFIX_SAPTAMANA}_*...")
        docker.elimina_dupa_prefix(PREFIX_SAPTAMANA, simulare=args.simulare)

        # Curăță artefactele generate
        if args.complet and not args.simulare:
            logger.info("Curățare director artefacte...")
            director_artefacte = RADACINA_PROIECT / "artifacts"
            fisiere_sterse = 0
            for f in director_artefacte.glob("*"):
                if f.name != ".gitkeep":
                    f.unlink()
                    fisiere_sterse += 1
            if fisiere_sterse:
                logger.info(f"  Șterse {fisiere_sterse} fișiere din artifacts/")

            logger.info("Curățare director pcap...")
            director_pcap = RADACINA_PROIECT / "pcap"
            capturi_sterse = 0
            for f in director_pcap.glob("*.pcap"):
                f.unlink()
                capturi_sterse += 1
            if capturi_sterse:
                logger.info(f"  Șterse {capturi_sterse} fișiere de captură")

        # Curățare sistem opțională
        if args.curata_tot and not args.simulare:
            logger.info("Curățare resurse Docker neutilizate...")
            docker.system_prune()

        logger.info("=" * 60)
        logger.info("✓ Curățare completă!")
        if args.complet:
            logger.info("Sistemul este pregătit pentru următoarea sesiune de laborator.")
        else:
            logger.info("Containerele au fost oprite. Volumele au fost păstrate.")
            logger.info("Pentru curățare completă: python scripts/curata.py --complet")
        logger.info("=" * 60)
        return 0

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Curățarea a eșuat: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
