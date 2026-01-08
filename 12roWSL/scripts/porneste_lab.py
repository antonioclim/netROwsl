#!/usr/bin/env python3
"""
Script de Pornire a Laboratorului Săptămânii 12
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
Accesați Portainer la: http://localhost:9000 (credențiale: stud / studstudstud)
"""

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path

# Adăugare rădăcină proiect în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"

# Configurația serviciilor (FĂRĂ Portainer - rulează global)
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
}


def verifica_docker_disponibil() -> bool:
    """Verifică dacă Docker este disponibil și rulează."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def porneste_docker_service() -> bool:
    """Încearcă să pornească serviciul Docker în WSL."""
    logger.info("Se încearcă pornirea serviciului Docker...")
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            time.sleep(2)
            return verifica_docker_disponibil()
        else:
            logger.error(f"Eroare la pornirea Docker: {result.stderr}")
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
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and "Up" in result.stdout:
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


def afiseaza_avertisment_portainer():
    """Afișează avertisment dacă Portainer nu rulează."""
    print()
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
    print()


def verifica_port(port: int, timeout: float = 1.0) -> bool:
    """Verifică dacă un port răspunde."""
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
    
    # Afișează status Portainer
    print()
    print("Servicii Globale:")
    print("-" * 60)
    if verifica_portainer_status():
        print(f"  \033[92m✓ ACTIV\033[0m  Portainer (Management)     (port {PORTAINER_PORT})")
    else:
        print(f"  \033[91m✗ OPRIT\033[0m  Portainer (Management)     (port {PORTAINER_PORT})")
    
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

    logger.info("=" * 60)
    logger.info("Pornire Mediu de Laborator - Săptămâna 12")
    logger.info("SMTP, JSON-RPC, XML-RPC, gRPC")
    logger.info("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    logger.info("=" * 60)

    # Verifică Docker
    logger.info("Verificare disponibilitate Docker...")
    if not verifica_docker_disponibil():
        logger.warning("Docker nu este disponibil. Se încearcă pornirea automată...")
        if not porneste_docker_service():
            logger.error("Nu s-a putut porni Docker!")
            logger.error("Încercați manual: sudo service docker start")
            logger.error("(Parolă: stud)")
            return 1
        logger.info("Docker a fost pornit cu succes!")
    else:
        logger.info("Daemon-ul Docker rulează")

    # Verifică status Portainer (doar avertisment)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Doar afișare status
    if args.status:
        afiseaza_status(docker)
        return 0

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
        
        # Status Portainer
        if verifica_portainer_status():
            logger.info(f"  Portainer (Management): {PORTAINER_URL} ✓")
        else:
            logger.info(f"  Portainer (Management): {PORTAINER_URL} (INACTIV)")
        
        logger.info("  SMTP:       localhost:1025  (netcat/telnet)")
        logger.info("  JSON-RPC:   http://localhost:6200")
        logger.info("  XML-RPC:    http://localhost:6201")
        logger.info("  gRPC:       localhost:6251")
        logger.info("")
        logger.info("Pentru oprire: python3 scripts/opreste_lab.py")
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
