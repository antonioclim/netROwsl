#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 11
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
Accesați Portainer la: http://localhost:9000 (credențiale: stud / studstudstud)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path
from typing import Optional

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("start_lab")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE_CONSTANTE
# ═══════════════════════════════════════════════════════════════════════════════

# Timeout-uri (în secunde)
TIMEOUT_DOCKER_INFO = 10
TIMEOUT_DOCKER_START = 30
TIMEOUT_PORT_WAIT = 30
TIMEOUT_SOCKET = 2
TIMEOUT_HTTP_REQUEST = 5

# Pauze (în secunde)
SLEEP_AFTER_DOCKER_START = 2
SLEEP_AFTER_COMPOSE_UP = 5
SLEEP_PORT_CHECK_INTERVAL = 0.5

# Configurări test
NUM_REQUESTS_TEST_DISTRIBUTION = 6

# Credențiale Portainer
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"

# Definirea serviciilor și configurațiilor lor (FĂRĂ Portainer - rulează global)
SERVICII: dict[str, dict] = {
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


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICARE_DOCKER
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_docker_disponibil() -> bool:
    """
    Verifică dacă Docker este disponibil și rulează.
    
    Returns:
        True dacă daemon-ul Docker răspunde, False altfel.
    
    Example:
        >>> verifica_docker_disponibil()
        True
    """
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=TIMEOUT_DOCKER_INFO
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except FileNotFoundError:
        return False
    except Exception:
        return False


def porneste_docker_service() -> bool:
    """
    Încearcă să pornească serviciul Docker în WSL.
    
    Returns:
        True dacă Docker a pornit cu succes, False altfel.
    
    Raises:
        Nu ridică excepții — toate sunt gestionate intern.
    """
    logger.info("Se încearcă pornirea serviciului Docker...")
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_DOCKER_START
        )
        if result.returncode == 0:
            time.sleep(SLEEP_AFTER_DOCKER_START)
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


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICARE_PORTAINER
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_portainer_status() -> bool:
    """
    Verifică dacă Portainer rulează pe portul 9000.
    
    Returns:
        True dacă Portainer este accesibil, False altfel.
    """
    try:
        # Verifică prin docker ps
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_DOCKER_INFO
        )
        if result.returncode == 0 and "Up" in result.stdout:
            return True
        
        # Verifică prin socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT_SOCKET)
            result_connect = sock.connect_ex(('localhost', PORTAINER_PORT))
            sock.close()
            return result_connect == 0
        except Exception:
            return False
            
    except Exception:
        return False


def afiseaza_avertisment_portainer() -> None:
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


# ═══════════════════════════════════════════════════════════════════════════════
# AȘTEPTARE_SERVICII
# ═══════════════════════════════════════════════════════════════════════════════

def asteapta_port(host: str, port: int, timeout: int = TIMEOUT_PORT_WAIT) -> bool:
    """
    Așteaptă ca un port să devină disponibil.
    
    Args:
        host: Adresa gazdei (ex: 'localhost', '192.168.1.1')
        port: Numărul portului (1-65535)
        timeout: Timpul maxim de așteptare în secunde
    
    Returns:
        True dacă portul este disponibil, False dacă timeout expiră.
    
    Raises:
        ValueError: Dacă portul nu e în intervalul valid (1-65535).
    
    Example:
        >>> asteapta_port('localhost', 8080, timeout=10)
        True
    """
    if not (1 <= port <= 65535):
        raise ValueError(f"Port invalid: {port}. Trebuie să fie între 1 și 65535.")
    
    timp_start = time.time()
    while time.time() - timp_start < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((host, port))
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(SLEEP_PORT_CHECK_INTERVAL)
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# TESTARE_ECHILIBROR
# ═══════════════════════════════════════════════════════════════════════════════

def testeaza_echilibror() -> dict[str, int]:
    """
    Testează distribuția echilibrului de sarcină.
    
    Trimite mai multe cereri către echilibror și contorizează
    răspunsurile de la fiecare backend.
    
    Returns:
        Dicționar cu statistici de distribuție {backend_id: count}.
    
    Example:
        >>> testeaza_echilibror()
        {'backend_1': 2, 'backend_2': 2, 'backend_3': 2}
    """
    try:
        import requests
    except ImportError:
        logger.warning("Modulul requests nu este disponibil pentru testare")
        return {}
    
    distributie: dict[str, int] = {}
    
    try:
        for _ in range(NUM_REQUESTS_TEST_DISTRIBUTION):
            resp = requests.get("http://localhost:8080/", timeout=TIMEOUT_HTTP_REQUEST)
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


# ═══════════════════════════════════════════════════════════════════════════════
# AFIȘARE_STARE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_stare(docker: ManagerDocker) -> None:
    """
    Afișează starea curentă a containerelor.
    
    Args:
        docker: Instanță ManagerDocker pentru interogarea containerelor.
    """
    print("\nStare containere:")
    print("-" * 50)
    
    containere = docker.obtine_containere_rulare()
    
    for nume, config in SERVICII.items():
        nume_container = config["container"]
        ruleaza = nume_container in containere
        stare = "✓ RULEAZĂ" if ruleaza else "✗ OPRIT"
        print(f"  {config['descriere']}: {stare}")
    
    # Afișează status Portainer
    print()
    print("Servicii Globale:")
    print("-" * 50)
    if verifica_portainer_status():
        print(f"  Portainer (port {PORTAINER_PORT}): \033[92m● ACTIV\033[0m")
    else:
        print(f"  Portainer (port {PORTAINER_PORT}): \033[91m○ INACTIV\033[0m")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ORCHESTRARE
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """
    Funcția principală care orchestrează pornirea laboratorului.
    
    Returns:
        Cod de ieșire: 0 pentru succes, 1 pentru eroare.
    """
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

    logger.info("=" * 60)
    logger.info("Pornire Mediu Laborator Săptămâna 11")
    logger.info("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    logger.info("=" * 60)

    # ═══════════════════════════════════════════════════════════════════════════
    # VERIFICARE_PREREQUISITE
    # ═══════════════════════════════════════════════════════════════════════════
    
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

    if args.status:
        afiseaza_stare(docker)
        return 0

    # ═══════════════════════════════════════════════════════════════════════════
    # PORNIRE_CONTAINERE
    # ═══════════════════════════════════════════════════════════════════════════
    
    try:
        # Construiește și pornește containerele
        if args.rebuild:
            logger.info("Reconstruire imagini Docker...")
            docker.compose_build()
        
        logger.info("Pornire containere...")
        docker.compose_up(detach=args.detach)

        # Așteaptă inițializarea serviciilor
        logger.info("Se așteaptă inițializarea serviciilor...")
        time.sleep(SLEEP_AFTER_COMPOSE_UP)

        # ═══════════════════════════════════════════════════════════════════════
        # VERIFICARE_SERVICII
        # ═══════════════════════════════════════════════════════════════════════
        
        # Verifică dacă portul principal este accesibil
        if asteapta_port("localhost", 8080, timeout=TIMEOUT_PORT_WAIT):
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

        # ═══════════════════════════════════════════════════════════════════════
        # LOGHEAZA_REZULTATE
        # ═══════════════════════════════════════════════════════════════════════
        
        if toate_sanatoase:
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
            
            logger.info("  Echilibror de sarcină:  http://localhost:8080")
            logger.info("  Verificare stare:       http://localhost:8080/health")
            logger.info("  Status Nginx:           http://localhost:8080/nginx_status")
            logger.info("")
            logger.info("Pentru a opri: python3 scripts/stop_lab.py")
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
