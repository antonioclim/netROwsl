#!/usr/bin/env python3
"""
Script de Pornire a Laboratorului Săptămânii 12
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adăugare rădăcină proiect în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Configurația serviciilor
SERVICII = {
    "smtp": {
        "container": "week12_lab",
        "port": 1025,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Server SMTP"
    },
    "jsonrpc": {
        "container": "week12_lab",
        "port": 6200,
        "verificare_sanatate": "http://localhost:6200",
        "timp_pornire": 2,
        "descriere": "Server JSON-RPC"
    },
    "xmlrpc": {
        "container": "week12_lab",
        "port": 6201,
        "verificare_sanatate": "http://localhost:6201",
        "timp_pornire": 2,
        "descriere": "Server XML-RPC"
    },
    "grpc": {
        "container": "week12_lab",
        "port": 6251,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Server gRPC"
    },
    "portainer": {
        "container": "week12_portainer",
        "port": 9443,
        "verificare_sanatate": "https://localhost:9443",
        "timp_pornire": 5,
        "descriere": "Portainer CE"
    }
}


def verifica_port(port: int, timeout: float = 1.0) -> bool:
    """Verifică dacă un port răspunde."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            rezultat = s.connect_ex(('localhost', port))
            return rezultat == 0
    except Exception:
        return False


def asteapta_servicii(timeout: int = 60) -> bool:
    """Așteaptă ca toate serviciile să devină disponibile."""
    logger.info("Se așteaptă pornirea serviciilor...")
    
    timp_start = time.time()
    porturi_asteptate = {1025, 6200, 6201, 6251}
    
    while time.time() - timp_start < timeout:
        porturi_active = {p for p in porturi_asteptate if verifica_port(p)}
        
        if porturi_active == porturi_asteptate:
            logger.info("✓ Toate serviciile sunt active!")
            return True
        
        ramase = porturi_asteptate - porturi_active
        logger.debug(f"Se așteaptă porturile: {ramase}")
        time.sleep(2)
    
    logger.error(f"Timeout după {timeout} secunde")
    return False


def afiseaza_status(docker: ManagerDocker):
    """Afișează starea curentă a serviciilor."""
    print("\n" + "=" * 60)
    print("Starea Serviciilor Laboratorului Săptămânii 12")
    print("=" * 60)
    
    for nume, config in SERVICII.items():
        port = config["port"]
        activ = verifica_port(port)
        
        if activ:
            status = "✓ ACTIV"
            culoare = "\033[92m"  # Verde
        else:
            status = "✗ OPRIT"
            culoare = "\033[91m"  # Roșu
        
        reset = "\033[0m"
        print(f"  {culoare}{status}{reset}  {config['descriere']:20} (port {port})")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Pornire Laborator Săptămâna 12 - SMTP și RPC"
    )
    parser.add_argument(
        "--status", 
        action="store_true",
        help="Afișează doar starea serviciilor"
    )
    parser.add_argument(
        "--rebuild", 
        action="store_true",
        help="Forțează reconstruirea imaginilor"
    )
    parser.add_argument(
        "--serviciu",
        choices=["smtp", "jsonrpc", "xmlrpc", "grpc", "all"],
        default="all",
        help="Serviciul specific de pornit (implicit: all)"
    )
    parser.add_argument(
        "--fara-docker",
        action="store_true",
        help="Pornește serverele local fără Docker"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Doar afișare status
    if args.status:
        afiseaza_status(docker)
        return 0

    logger.info("=" * 60)
    logger.info("Pornire Mediu de Laborator - Săptămâna 12")
    logger.info("SMTP, JSON-RPC, XML-RPC, gRPC")
    logger.info("=" * 60)

    try:
        # Construire și pornire containere
        if args.rebuild:
            logger.info("Reconstruire imagini Docker...")
            docker.compune_build()
        
        logger.info("Pornire containere Docker...")
        docker.compune_up(detasat=True)

        # Așteptare și verificare servicii
        if not asteapta_servicii(timeout=60):
            logger.error("Unele servicii nu au pornit corect.")
            logger.info("Verificați jurnalele cu: docker compose logs")
            return 1

        # Mesaj de succes
        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Mediul de laborator este pregătit!")
        logger.info("")
        logger.info("Puncte de acces:")
        logger.info("  Portainer:  https://localhost:9443")
        logger.info("  SMTP:       localhost:1025  (netcat/telnet)")
        logger.info("  JSON-RPC:   http://localhost:6200")
        logger.info("  XML-RPC:    http://localhost:6201")
        logger.info("  gRPC:       localhost:6251")
        logger.info("")
        logger.info("Pentru oprire: python scripts/opreste_lab.py")
        logger.info("=" * 60)
        return 0

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
