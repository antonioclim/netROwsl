#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 9
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script pornește toate containerele Docker și verifică
mediul de laborator.

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
Accesați Portainer la: http://localhost:9000 (credențiale: stud / studstudstud)
"""

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger, afiseaza_banner

logger = configureaza_logger("porneste_lab")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"

# Definirea serviciilor pentru săptămâna 9 (FĂRĂ Portainer - rulează global)
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


def verifica_porturi_passive(gazda: str = "localhost") -> bool:
    """Verifică disponibilitatea porturilor passive FTP."""
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
        
        # Afișează status Portainer
        print()
        print("Servicii Globale:")
        print("-" * 50)
        if verifica_portainer_status():
            print(f"  Portainer (port {PORTAINER_PORT}): \033[92m● ACTIV\033[0m")
        else:
            print(f"  Portainer (port {PORTAINER_PORT}): \033[91m○ INACTIV\033[0m")
        
        return 0

    afiseaza_banner(
        "Pornire Mediu de Laborator",
        "Săptămâna 9 - Nivelul Sesiune și Prezentare",
        "Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer"
    )

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
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            
            # Status Portainer
            if verifica_portainer_status():
                logger.info(f"  Portainer:   {PORTAINER_URL}")
            else:
                logger.warning("  Portainer:   NU RULEAZĂ (vezi instrucțiuni mai sus)")
            
            logger.info("  Server FTP:  ftp://localhost:2121")
            logger.info("  Credențiale: test / 12345")
            logger.info("")
            logger.info("Comenzi utile:")
            logger.info("  python3 scripts/ruleaza_demo.py --lista")
            logger.info("  python3 scripts/captureaza_trafic.py --help")
            logger.info("")
            logger.info("Pentru oprire: python3 scripts/opreste_lab.py")
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
