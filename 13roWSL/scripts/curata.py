#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 13
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import argparse
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.utilitare_docker import ManagerDocker

logger = configureaza_logger("curata")

PREFIX_SAPTAMANA = "week13"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def curata_artefacte(simulare: bool = False):
    """Curăță directoarele de artefacte și capturi."""
    directoare = [
        RADACINA_PROIECT / "artifacts",
        RADACINA_PROIECT / "pcap",
    ]
    
    for director in directoare:
        if not director.exists():
            continue
        
        for fisier in director.iterdir():
            if fisier.name == ".gitkeep" or fisier.name == "README.md":
                continue
            
            if simulare:
                logger.info(f"  [SIMULARE] Ar șterge: {fisier}")
            else:
                try:
                    if fisier.is_file():
                        fisier.unlink()
                        logger.info(f"  [ȘTERS] {fisier.name}")
                    elif fisier.is_dir():
                        import shutil
                        shutil.rmtree(fisier)
                        logger.info(f"  [ȘTERS] {fisier.name}/")
                except Exception as e:
                    logger.warning(f"  [EROARE] Nu s-a putut șterge {fisier}: {e}")


def curata_pycache(simulare: bool = False):
    """Elimină directoarele __pycache__."""
    for pycache in RADACINA_PROIECT.rglob("__pycache__"):
        if simulare:
            logger.info(f"  [SIMULARE] Ar șterge: {pycache}")
        else:
            try:
                import shutil
                shutil.rmtree(pycache)
                logger.info(f"  [ȘTERS] {pycache.relative_to(RADACINA_PROIECT)}")
            except Exception as e:
                logger.warning(f"  [EROARE] {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 13",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python curata.py              # Oprește containerele, păstrează volumele
  python curata.py --complet    # Elimină totul, inclusiv volumele
  python curata.py --artefacte  # Curăță doar artefactele generate
  python curata.py --simulare   # Arată ce ar fi șters fără a șterge
        """
    )
    parser.add_argument("--complet", action="store_true",
                        help="Elimină volumele și toate datele (pentru săptămâna următoare)")
    parser.add_argument("--curatare-sistem", action="store_true",
                        help="Curăță și resursele Docker neutilizate (docker system prune)")
    parser.add_argument("--artefacte", action="store_true",
                        help="Curăță doar directoarele artifacts/ și pcap/")
    parser.add_argument("--simulare", action="store_true",
                        help="Afișează ce ar fi șters fără a șterge efectiv")
    args = parser.parse_args()
    
    print("=" * 60)
    print("CURĂȚARE LABORATOR SĂPTĂMÂNA 13")
    print("=" * 60)
    
    if args.simulare:
        print("[SIMULARE] Nicio modificare nu va fi efectuată\n")
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    try:
        # Doar artefacte
        if args.artefacte:
            logger.info("Se curăță artefactele...")
            curata_artefacte(args.simulare)
            curata_pycache(args.simulare)
            print("\n✓ Curățare artefacte completă")
            return 0
        
        # Oprire containere
        logger.info("Se opresc containerele...")
        if not args.simulare:
            docker.compose_down(volumes=args.complet)
        else:
            logger.info("  [SIMULARE] docker compose down" + 
                       (" -v" if args.complet else ""))
        
        # Eliminare resurse cu prefixul săptămânii
        logger.info(f"\nSe elimină resursele {PREFIX_SAPTAMANA}_*...")
        if not args.simulare:
            docker.elimina_dupa_prefix(PREFIX_SAPTAMANA)
        else:
            logger.info(f"  [SIMULARE] Ar elimina containerele/rețelele/volumele {PREFIX_SAPTAMANA}_*")
        
        # Curățare artefacte dacă este completă
        if args.complet:
            logger.info("\nSe curăță artefactele...")
            curata_artefacte(args.simulare)
            
            logger.info("\nSe curăță cache-ul Python...")
            curata_pycache(args.simulare)
        
        # Curățare sistem Docker
        if args.curatare_sistem and not args.simulare:
            logger.info("\nSe curăță resursele Docker neutilizate...")
            docker.curata_sistem()
        
        print("\n" + "=" * 60)
        print("✓ CURĂȚARE COMPLETĂ!")
        if args.complet:
            print("  Sistemul este pregătit pentru următoarea sesiune de laborator.")
        print("=" * 60)
        return 0
        
    except Exception as e:
        logger.error(f"Eroare la curățare: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
