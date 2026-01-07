#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 9
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script pornește toate containerele Docker și verifică
mediul de laborator.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger, afiseaza_banner

logger = configureaza_logger("porneste_lab")

# Definirea serviciilor pentru săptămâna 9
SERVICII = {
    "server-ftp": {
        "container": "s9_ftp-server",
        "port": 2121,
        "verificare_sanatate": None,
        "timp_pornire": 5
    },
    "client1": {
        "container": "s9_client1",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 2
    },
    "client2": {
        "container": "s9_client2",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 2
    }
}

# Porturile passive FTP
PORTURI_PASSIVE = range(60000, 60011)


def verifica_porturi_passive(gazda: str = "localhost") -> bool:
    """Verifică disponibilitatea porturilor passive FTP."""
    import socket
    
    for port in PORTURI_PASSIVE:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                rezultat = s.connect_ex((gazda, port))
                if rezultat == 0:
                    logger.debug(f"Port pasiv {port}: deschis")
        except Exception:
            pass
    
    return True


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Pornește mediul de laborator pentru Săptămâna 9"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Verifică doar starea serviciilor"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Forțează reconstruirea imaginilor"
    )
    parser.add_argument(
        "--detasat", "-d",
        action="store_true",
        default=True,
        help="Rulează în mod detașat (implicit)"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    if args.status:
        afiseaza_banner(
            "Starea Laboratorului",
            "Săptămâna 9 - Nivelul Sesiune și Prezentare"
        )
        docker.afiseaza_stare(SERVICII)
        return 0

    afiseaza_banner(
        "Pornire Mediu de Laborator",
        "Săptămâna 9 - Nivelul Sesiune și Prezentare"
    )

    try:
        # Construiește și pornește containerele
        if args.rebuild:
            logger.info("Se reconstruiesc imaginile Docker...")
            docker.compose_build()
        
        logger.info("Se pornesc serviciile...")
        docker.compose_up(detasat=args.detasat)

        # Așteaptă inițializarea serviciilor
        logger.info("Se așteaptă inițializarea serviciilor...")
        time.sleep(5)

        # Verificări de sănătate
        logger.info("Se verifică starea serviciilor...")
        toate_ok = docker.verifica_servicii(SERVICII)

        # Verifică porturile passive
        logger.info("Se verifică porturile passive FTP (60000-60010)...")
        verifica_porturi_passive()

        if toate_ok:
            print()
            logger.info("=" * 60)
            logger.info("Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info("  Portainer:   https://localhost:9443")
            logger.info("  Server FTP:  ftp://localhost:2121")
            logger.info("  Credențiale: test / 12345")
            logger.info("")
            logger.info("Comenzi utile:")
            logger.info("  python scripts/ruleaza_demo.py --lista")
            logger.info("  python scripts/captureaza_trafic.py --help")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Unele servicii nu au pornit corect.")
            logger.error("Verificați log-urile cu: docker logs s9_ftp-server")
            return 1

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
