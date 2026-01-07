#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 10
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului la calea Python
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Configurația serviciilor laboratorului
SERVICII = {
    "web": {
        "container": "week10_web",
        "port": 8000,
        "verificare_sanatate": "http://localhost:8000/",
        "timp_pornire": 5,
        "descriere": "Server HTTP Python"
    },
    "dns-server": {
        "container": "week10_dns",
        "port": 5353,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Server DNS personalizat (dnslib)"
    },
    "ssh-server": {
        "container": "week10_ssh",
        "port": 2222,
        "verificare_sanatate": None,
        "timp_pornire": 5,
        "descriere": "Server SSH (OpenSSH)"
    },
    "ftp-server": {
        "container": "week10_ftp",
        "port": 2121,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Server FTP (pyftpdlib)"
    },
    "debug": {
        "container": "week10_debug",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 2,
        "descriere": "Container utilitar (dig, curl, tcpdump)"
    },
    "portainer": {
        "container": "week10_portainer",
        "port": 9443,
        "verificare_sanatate": None,
        "timp_pornire": 10,
        "descriere": "Interfață web Docker"
    },
}


def afiseaza_banner():
    """Afișează bannerul de pornire."""
    print()
    print("=" * 60)
    print("  LABORATOR SĂPTĂMÂNA 10 - Servicii de Rețea")
    print("  HTTP/S, REST, DNS, SSH, FTP în containere Docker")
    print("=" * 60)
    print()


def afiseaza_puncte_acces():
    """Afișează punctele de acces pentru servicii."""
    print()
    print("─" * 60)
    print("  PUNCTE DE ACCES SERVICII")
    print("─" * 60)
    print()
    print("  Portainer (Management Docker):")
    print("    → https://localhost:9443")
    print()
    print("  Server Web HTTP:")
    print("    → http://localhost:8000")
    print()
    print("  Server DNS (din container debug):")
    print("    → dig @localhost -p 5353 web.lab.local")
    print()
    print("  Server SSH:")
    print("    → ssh -p 2222 labuser@localhost")
    print("    → Parolă: labpass")
    print()
    print("  Server FTP:")
    print("    → ftp localhost 2121")
    print("    → Utilizator: labftp / Parolă: labftp")
    print()
    print("  Container Debug (acces shell):")
    print("    → docker exec -it week10_debug /bin/sh")
    print()
    print("─" * 60)


def main():
    """Funcția principală de pornire."""
    parser = argparse.ArgumentParser(
        description="Pornește Laboratorul Săptămânii 10"
    )
    parser.add_argument(
        "--stare",
        action="store_true",
        help="Verifică doar starea serviciilor"
    )
    parser.add_argument(
        "--reconstruieste",
        action="store_true",
        help="Forțează reconstruirea imaginilor"
    )
    parser.add_argument(
        "--detasare", "-d",
        action="store_true",
        default=True,
        help="Rulează în fundal (implicit)"
    )
    parser.add_argument(
        "--fara-portainer",
        action="store_true",
        help="Nu porni Portainer"
    )
    args = parser.parse_args()

    afiseaza_banner()

    try:
        docker = ManagerDocker(RADACINA_PROIECT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Eroare: {e}")
        logger.error("Asigurați-vă că rulați scriptul din directorul WEEK10_WSLkit_RO")
        return 1

    if args.stare:
        docker.afiseaza_stare(SERVICII)
        return 0

    logger.info("Pornire containere Docker...")

    try:
        # Construire și pornire containere
        if args.reconstruieste:
            logger.info("Reconstruire imagini Docker...")
            docker.compose_build()
        
        succes = docker.compose_up(detasare=args.detasare)
        
        if not succes:
            logger.error("Pornirea containerelor a eșuat")
            return 1

        # Așteptare pentru inițializarea serviciilor
        timp_maxim = max(s["timp_pornire"] for s in SERVICII.values())
        logger.info(f"Așteptare {timp_maxim} secunde pentru inițializare...")
        
        for i in range(timp_maxim):
            print(f"\r  Inițializare... {timp_maxim - i}s rămase", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 40 + "\r", end="")

        # Verificare stare servicii
        logger.info("Verificare stare servicii:")
        toate_sanatoase = docker.verifica_servicii(SERVICII)

        if toate_sanatoase:
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            afiseaza_puncte_acces()
            logger.info("=" * 60)
            return 0
        else:
            logger.warning("Unele servicii nu sunt încă pregătite.")
            logger.warning("Așteptați câteva secunde și verificați din nou cu --stare")
            return 0

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
