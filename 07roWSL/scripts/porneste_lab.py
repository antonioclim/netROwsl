#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
Accesați Portainer la: http://localhost:9000 (credențiale: stud / studstudstud)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
import socket
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.network_utils import UtilitareRetea
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Definire servicii și configurația lor
# NOTĂ: Portainer NU este inclus - rulează global pe portul 9000
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

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"


def verifica_docker_activ() -> bool:
    """Verifică dacă Docker este activ și funcțional."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def porneste_docker_service() -> bool:
    """Încearcă să pornească serviciul Docker în WSL."""
    logger.info("Se încearcă pornirea serviciului Docker...")
    try:
        rezultat = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if rezultat.returncode == 0:
            time.sleep(2)
            return verifica_docker_activ()
        else:
            logger.error(f"Eroare la pornirea Docker: {rezultat.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Timeout la pornirea serviciului Docker")
        return False
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return False


def verifica_portainer_status() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000."""
    try:
        # Verifică prin docker ps
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
            return True
        
        # Verifică prin socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', PORTAINER_PORT))
            sock.close()
            return result == 0
        except Exception:
            return False
            
    except Exception:
        return False


def afiseaza_avertisment_portainer() -> None:
    """Afișează avertisment dacă Portainer nu rulează."""
    logger.warning("")
    logger.warning("=" * 60)
    logger.warning("⚠️  AVERTISMENT: Portainer nu rulează!")
    logger.warning("")
    logger.warning("Portainer este instrumentul vizual pentru gestionarea Docker.")
    logger.warning("Pentru a-l porni, executați în terminal:")
    logger.warning("")
    logger.warning("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    logger.warning("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    logger.warning("    -v portainer_data:/data portainer/portainer-ce:latest")
    logger.warning("")
    logger.warning(f"După pornire, accesați: {PORTAINER_URL}")
    logger.warning(f"Credențiale: {PORTAINER_USER} / {PORTAINER_PASS}")
    logger.warning("=" * 60)
    logger.warning("")


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

    logger.info("=" * 60)
    logger.info("Laborator Săptămâna 7: Interceptarea și Filtrarea Pachetelor")
    logger.info("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    logger.info("=" * 60)

    # Verifică și pornește Docker dacă nu rulează
    if not verifica_docker_activ():
        logger.warning("Docker nu este activ. Se încearcă pornirea automată...")
        if not porneste_docker_service():
            logger.error("")
            logger.error("Nu s-a putut porni Docker!")
            logger.error("Încercați manual: sudo service docker start")
            logger.error("(Parolă: stud)")
            return 1
        logger.info("✓ Docker a fost pornit cu succes!")

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Modul status
    if args.status:
        logger.info("")
        logger.info("Verificare Status Laborator Săptămâna 7")
        logger.info("-" * 40)
        
        docker.afiseaza_status(SERVICII)
        
        logger.info("\nVerificare conectivitate servicii:")
        toate_servicii = dict(SERVICII)
        if args.proxy or args.demo:
            toate_servicii.update(SERVICII_OPTIONALE)
        
        verifica_servicii(toate_servicii)
        
        # Afișează status Portainer
        logger.info("\nServicii globale:")
        logger.info("-" * 40)
        if verifica_portainer_status():
            logger.info(f"  Portainer: ✓ ACTIV ({PORTAINER_URL})")
        else:
            logger.warning(f"  Portainer: ✗ INACTIV (port {PORTAINER_PORT})")
        
        return 0

    # Verifică status Portainer (doar avertisment, nu oprește execuția)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()

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
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            
            # Afișează status Portainer
            if verifica_portainer_status():
                logger.info(f"  Portainer: {PORTAINER_URL}")
            else:
                logger.info(f"  Portainer: NU RULEAZĂ (vezi instrucțiuni mai sus)")
            
            for nume, info in toate_servicii.items():
                port = info["port"]
                protocol = info["protocol"]
                descriere = info["descriere"]
                logger.info(f"  {descriere}: localhost:{port}/{protocol}")
            logger.info("")
            logger.info("Pentru oprire: python3 scripts/opreste_lab.py")
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
