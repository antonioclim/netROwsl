#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_laborator")

# Definirea serviciilor și configurațiile lor
SERVICII = {
    "python": {
        "container": "week5_python",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 5,
        "descriere": "Container principal Python pentru exerciții"
    },
    "server-udp": {
        "container": "week5_udp-server",
        "port": 9999,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Server UDP Echo pentru demonstrații"
    },
    "client-udp": {
        "container": "week5_udp-client",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Client UDP pentru testare"
    }
}


def afiseaza_banner():
    """Afișează bannerul de pornire."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║           SĂPTĂMÂNA 5 - LABORATOR REȚELE DE CALCULATOARE        ║
║                                                                  ║
║         Nivelul Rețea: Adresare IPv4/IPv6 și Subnetare          ║
║                                                                  ║
║              ASE Bucuresti - Informatică Economică               ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(
        description="Pornește mediul de laborator pentru Săptămâna 5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python porneste_laborator.py          # Pornește toate serviciile
  python porneste_laborator.py --status # Verifică starea serviciilor
  python porneste_laborator.py --reconstruieste  # Reconstruiește imaginile
        """
    )
    parser.add_argument(
        "--status", 
        action="store_true", 
        help="Doar verifică starea serviciilor"
    )
    parser.add_argument(
        "--reconstruieste", 
        action="store_true", 
        help="Forțează reconstruirea imaginilor Docker"
    )
    parser.add_argument(
        "--detasat", "-d", 
        action="store_true", 
        default=True,
        help="Rulează în modul detașat (implicit)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate"
    )
    args = parser.parse_args()

    afiseaza_banner()
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Doar verifică starea dacă este cerut
    if args.status:
        logger.info("Verificare stare servicii...")
        docker.afiseaza_status(SERVICII)
        return 0

    logger.info("=" * 60)
    logger.info("Pornire mediu de laborator Săptămâna 5")
    logger.info("=" * 60)

    try:
        # Construiește și pornește containerele
        if args.reconstruieste:
            logger.info("Reconstruire imagini Docker...")
            docker.compose_build()
        
        logger.info("Pornire containere...")
        docker.compose_up(detasat=args.detasat)

        # Așteaptă inițializarea serviciilor
        logger.info("Așteptare inițializare servicii...")
        time.sleep(5)

        # Verificări de sănătate
        logger.info("Verificare sănătate servicii...")
        toate_sanatoase = docker.verifica_servicii(SERVICII)

        if toate_sanatoase:
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info("  • Portainer: https://localhost:9443")
            logger.info("")
            logger.info("Containere active:")
            for nume, svc in SERVICII.items():
                port_info = f":{svc['port']}" if svc['port'] else ""
                logger.info(f"  • {svc['container']}{port_info} - {svc['descriere']}")
            logger.info("")
            logger.info("Rețea Docker: week5_labnet (10.5.0.0/24)")
            logger.info("=" * 60)
            logger.info("")
            logger.info("Pentru a rula exercițiile:")
            logger.info("  python src/exercises/ex_5_01_cidr_flsm.py 192.168.10.14/26")
            logger.info("")
            return 0
        else:
            logger.error("Unele servicii nu au pornit. Verificați jurnalele de mai sus.")
            logger.info("Încercați: docker compose -f docker/docker-compose.yml logs")
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
