#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.network_utils import UtilitareRetea
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Definire servicii și configurația lor
SERVICII = {
    "server_tcp": {
        "container": "week7_server_tcp",
        "port": 9090,
        "protocol": "tcp",
        "timp_pornire": 5,
        "descriere": "Server TCP Echo"
    },
    "receptor_udp": {
        "container": "week7_receptor_udp",
        "port": 9091,
        "protocol": "udp",
        "timp_pornire": 3,
        "descriere": "Receptor UDP"
    },
}

SERVICII_OPTIONALE = {
    "filtru_pachete": {
        "container": "week7_filtru_pachete",
        "port": 8888,
        "protocol": "tcp",
        "timp_pornire": 3,
        "descriere": "Filtru Pachete (Proxy)"
    },
}


def verifica_servicii(servicii: dict) -> bool:
    """Verifică că serviciile sunt funcționale."""
    toate_ok = True
    
    for nume, info in servicii.items():
        port = info["port"]
        protocol = info["protocol"]
        descriere = info["descriere"]
        
        logger.info(f"  Verificare {descriere} (port {port}/{protocol})...")
        
        if protocol == "tcp":
            ok = UtilitareRetea.verifica_port_deschis("localhost", port, timeout=3.0)
        else:
            # Pentru UDP, doar verificăm că putem trimite
            ok, _ = UtilitareRetea.test_trimitere_udp("localhost", port)
        
        if ok:
            logger.info(f"    [OK] {descriere} funcțional")
        else:
            logger.error(f"    [EROARE] {descriere} nu răspunde")
            toate_ok = False
    
    return toate_ok


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Pornește mediul de laborator pentru Săptămâna 7"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Verifică doar statusul, nu pornește serviciile"
    )
    parser.add_argument(
        "--reconstruieste",
        action="store_true",
        help="Reconstruiește imaginile Docker"
    )
    parser.add_argument(
        "--proxy",
        action="store_true",
        help="Include serviciul de filtrare la nivel aplicație"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Pornește în modul demo (toate serviciile)"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Modul status
    if args.status:
        logger.info("=" * 60)
        logger.info("Verificare Status Laborator Săptămâna 7")
        logger.info("=" * 60)
        
        docker.afiseaza_status(SERVICII)
        
        logger.info("\nVerificare conectivitate servicii:")
        toate_servicii = dict(SERVICII)
        if args.proxy or args.demo:
            toate_servicii.update(SERVICII_OPTIONALE)
        
        verifica_servicii(toate_servicii)
        return 0

    # Pornire normală
    logger.info("=" * 60)
    logger.info("Pornire Mediu Laborator Săptămâna 7")
    logger.info("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    logger.info("=" * 60)

    try:
        # Determinare profil
        if args.demo:
            profil = "demo"
            toate_servicii = dict(SERVICII)
            toate_servicii.update(SERVICII_OPTIONALE)
        elif args.proxy:
            profil = "proxy"
            toate_servicii = dict(SERVICII)
            toate_servicii.update(SERVICII_OPTIONALE)
        else:
            profil = None
            toate_servicii = SERVICII

        # Reconstruire dacă este cerută
        if args.reconstruieste:
            logger.info("Reconstruire imagini Docker...")
            docker.compose_build()

        # Pornire containere
        logger.info("Pornire containere Docker...")
        ok = docker.compose_up(detach=True, profile=profil)
        
        if not ok:
            logger.error("Eroare la pornirea containerelor")
            return 1

        # Așteptare inițializare
        timp_asteptare = max(s["timp_pornire"] for s in toate_servicii.values())
        logger.info(f"Așteptare {timp_asteptare} secunde pentru inițializarea serviciilor...")
        time.sleep(timp_asteptare)

        # Verificare servicii
        logger.info("Verificare servicii...")
        toate_ok = verifica_servicii(toate_servicii)

        if toate_ok:
            logger.info("")
            logger.info("=" * 60)
            logger.info("Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info("  Portainer: https://localhost:9443")
            for nume, info in toate_servicii.items():
                port = info["port"]
                protocol = info["protocol"]
                descriere = info["descriere"]
                logger.info(f"  {descriere}: localhost:{port}/{protocol}")
            logger.info("")
            logger.info("Pentru oprire: python scripts/opreste_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("")
            logger.error("Unele servicii nu au pornit corect.")
            logger.error("Verificați logurile: docker compose -f docker/docker-compose.yml logs")
            return 1

    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
