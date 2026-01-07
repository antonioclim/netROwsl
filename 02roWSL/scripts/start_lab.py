#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, Any

# Adăugare rădăcină proiect la cale
RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configurează_logger

logger = configurează_logger("start_lab")

# Definire servicii și configurația lor
SERVICII: Dict[str, Dict[str, Any]] = {
    "week2_lab": {
        "container": "week2_lab",
        "port_tcp": 9090,
        "port_udp": 9091,
        "verificare_stare": None,
        "timp_pornire": 5,
        "descriere": "Container principal (servere TCP/UDP)"
    },
    "portainer": {
        "container": "week2_portainer",
        "port_tcp": 9443,
        "verificare_stare": "/api/status",
        "timp_pornire": 10,
        "descriere": "Interfață web Docker"
    }
}


def afișează_stare(manager: ManagerDocker) -> None:
    """Afișează starea curentă a serviciilor."""
    logger.info("=" * 60)
    logger.info("Starea Serviciilor")
    logger.info("=" * 60)
    
    for nume, config in SERVICII.items():
        container = config["container"]
        rulează = manager.container_rulează(container)
        stare = "🟢 Activ" if rulează else "🔴 Oprit"
        logger.info(f"  {nume}: {stare}")
        
        if rulează and "port_tcp" in config:
            logger.info(f"      Port TCP: {config['port_tcp']}")
        if rulează and "port_udp" in config:
            logger.info(f"      Port UDP: {config['port_udp']}")


def verifică_servicii(manager: ManagerDocker) -> bool:
    """
    Verifică dacă toate serviciile sunt funcționale.
    
    Returns:
        True dacă toate serviciile sunt sănătoase
    """
    toate_sănătoase = True
    
    for nume, config in SERVICII.items():
        container = config["container"]
        
        if not manager.container_rulează(container):
            logger.error(f"  ✗ {nume}: Containerul nu rulează")
            toate_sănătoase = False
            continue
        
        # Verificare port TCP
        if "port_tcp" in config:
            port = config["port_tcp"]
            if manager.verifică_port("localhost", port):
                logger.info(f"  ✓ {nume}: Port TCP {port} accesibil")
            else:
                logger.warning(f"  ⚠ {nume}: Port TCP {port} nu răspunde încă")
        
        # Verificare port UDP (mai greu de testat)
        if "port_udp" in config:
            logger.info(f"  ℹ {nume}: Port UDP {config['port_udp']} configurat")
    
    return toate_sănătoase


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Pornire Laborator Săptămâna 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python start_lab.py              # Pornire normală
  python start_lab.py --status     # Verificare stare
  python start_lab.py --rebuild    # Reconstruire imagini
        """
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Doar verifică starea (nu pornește nimic)"
    )
    parser.add_argument(
        "--rebuild", "-r",
        action="store_true",
        help="Forțează reconstruirea imaginilor Docker"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=True,
        help="Rulează în fundal (implicit: da)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate"
    )
    
    args = parser.parse_args()

    # Inițializare manager Docker
    cale_docker = RĂDĂCINĂ_PROIECT / "docker"
    manager = ManagerDocker(cale_docker)

    # Doar afișare stare
    if args.status:
        afișează_stare(manager)
        return 0

    # Pornire laborator
    logger.info("=" * 60)
    logger.info("Pornire Mediu de Laborator - Săptămâna 2")
    logger.info("Rețele de Calculatoare - ASE, Informatică Economică")
    logger.info("=" * 60)

    try:
        # Construire imagini dacă este necesar
        if args.rebuild:
            logger.info("Reconstruire imagini Docker...")
            manager.compose_build()
        
        # Pornire containere
        logger.info("Pornire containere...")
        manager.compose_up(detach=args.detach)

        # Așteptare inițializare servicii
        logger.info("Așteptare inițializare servicii...")
        timp_maxim = max(s.get("timp_pornire", 5) for s in SERVICII.values())
        
        for i in range(timp_maxim):
            time.sleep(1)
            sys.stdout.write(f"\r  Progres: {i + 1}/{timp_maxim} secunde...")
            sys.stdout.flush()
        print()

        # Verificare servicii
        logger.info("Verificare servicii...")
        toate_funcționale = verifică_servicii(manager)

        if toate_funcționale:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info(f"  • Portainer:  https://localhost:9443")
            logger.info(f"  • Server TCP: localhost:9090")
            logger.info(f"  • Server UDP: localhost:9091")
            logger.info("")
            logger.info("Pentru a porni un server TCP:")
            logger.info("  docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server")
            logger.info("")
            logger.info("Pentru a porni un server UDP:")
            logger.info("  docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py server")
            logger.info("=" * 60)
            return 0
        else:
            logger.warning("Unele servicii nu au pornit complet.")
            logger.info("Încercați să așteptați câteva secunde și rulați:")
            logger.info("  python scripts/start_lab.py --status")
            return 1

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
