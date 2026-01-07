#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 11
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

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

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("start_lab")


# Definirea serviciilor și configurațiilor lor
SERVICII = {
    "nginx_lb": {
        "container": "s11_nginx_lb",
        "port": 8080,
        "verificare_stare": "/health",
        "timp_pornire": 5,
        "descriere": "Echilibror de sarcină Nginx"
    },
    "backend_1": {
        "container": "s11_backend_1",
        "port": None,  # Port intern
        "verificare_stare": None,
        "timp_pornire": 3,
        "descriere": "Server backend 1"
    },
    "backend_2": {
        "container": "s11_backend_2",
        "port": None,
        "verificare_stare": None,
        "timp_pornire": 3,
        "descriere": "Server backend 2"
    },
    "backend_3": {
        "container": "s11_backend_3",
        "port": None,
        "verificare_stare": None,
        "timp_pornire": 3,
        "descriere": "Server backend 3"
    },
}


def asteapta_port(host: str, port: int, timeout: int = 30) -> bool:
    """
    Așteaptă ca un port să devină disponibil.
    
    Args:
        host: Adresa gazdei
        port: Numărul portului
        timeout: Timpul maxim de așteptare în secunde
    
    Returns:
        True dacă portul este disponibil, False altfel
    """
    import socket
    
    timp_start = time.time()
    while time.time() - timp_start < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((host, port))
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(0.5)
    return False


def testeaza_echilibror() -> dict:
    """
    Testează distribuția echilibrului de sarcină.
    
    Returns:
        Dicționar cu statistici de distribuție
    """
    import requests
    
    distributie = {}
    
    try:
        for i in range(6):
            resp = requests.get("http://localhost:8080/", timeout=5)
            # Extrage identificatorul backend-ului din răspuns
            continut = resp.text.lower()
            for j in range(1, 4):
                if f"web{j}" in continut or f"backend {j}" in continut:
                    cheie = f"backend_{j}"
                    distributie[cheie] = distributie.get(cheie, 0) + 1
                    break
    except Exception as e:
        logger.warning(f"Nu s-a putut testa echiliborul: {e}")
    
    return distributie


def afiseaza_stare(docker: ManagerDocker):
    """Afișează starea curentă a containerelor."""
    print("\nStare containere:")
    print("-" * 50)
    
    containere = docker.obtine_containere_rulare()
    
    for nume, config in SERVICII.items():
        nume_container = config["container"]
        ruleaza = nume_container in containere
        stare = "✓ RULEAZĂ" if ruleaza else "✗ OPRIT"
        print(f"  {config['descriere']}: {stare}")


def main():
    parser = argparse.ArgumentParser(
        description="Pornește mediul de laborator pentru Săptămâna 11"
    )
    parser.add_argument(
        "--status", "--stare",
        action="store_true",
        help="Verifică doar starea (nu pornește serviciile)"
    )
    parser.add_argument(
        "--rebuild", "--reconstruieste",
        action="store_true",
        help="Forțează reconstruirea imaginilor"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=True,
        help="Rulează în mod detașat (implicit)"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    if args.status:
        afiseaza_stare(docker)
        return 0

    logger.info("=" * 60)
    logger.info("Pornire Mediu Laborator Săptămâna 11")
    logger.info("=" * 60)

    try:
        # Construiește și pornește containerele
        if args.rebuild:
            logger.info("Reconstruire imagini Docker...")
            docker.compose_build()
        
        logger.info("Pornire containere...")
        docker.compose_up(detach=args.detach)

        # Așteaptă inițializarea serviciilor
        logger.info("Se așteaptă inițializarea serviciilor...")
        time.sleep(5)

        # Verifică dacă portul principal este accesibil
        if asteapta_port("localhost", 8080, timeout=30):
            logger.info("✓ Echiliborul de sarcină este accesibil pe portul 8080")
        else:
            logger.error("✗ Echiliborul de sarcină nu răspunde pe portul 8080")
            return 1

        # Testează distribuția sarcinii
        logger.info("Testare distribuție sarcină...")
        distributie = testeaza_echilibror()
        if distributie:
            logger.info(f"  Distribuție: {distributie}")
        
        # Verificări de stare
        toate_sanatoase = docker.verifica_servicii(SERVICII)

        if toate_sanatoase:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info("  Echilibror de sarcină: http://localhost:8080")
            logger.info("  Verificare stare:      http://localhost:8080/health")
            logger.info("  Status Nginx:          http://localhost:8080/nginx_status")
            logger.info("  Portainer:             https://localhost:9443")
            logger.info("")
            logger.info("Pentru a opri: python scripts/stop_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Unele servicii nu au pornit corect. Verificați jurnalele.")
            logger.info("Jurnale: docker compose logs")
            return 1

    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
