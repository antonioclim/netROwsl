#!/usr/bin/env python3
"""
Pornire Laborator Săptămâna 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
Accesați Portainer la: http://localhost:9000 (credențiale: stud / studstudstud)
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.network_utils import TesterRetea
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Configurația serviciilor
# NOTĂ: Portainer NU este inclus - rulează global pe portul 9000
SERVICII = {
    "lab": {
        "container": "week1_lab",
        "port": 9090,
        "descriere": "Container principal de laborator",
        "timp_pornire": 5
    }
}

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"


def afiseaza_banner() -> None:
    """Afișează banner-ul de pornire."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  LABORATOR SĂPTĂMÂNA 1 - FUNDAMENTELE REȚELELOR".center(58) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE, Informatică".center(58) + "║")
    print("║" + "  Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()


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
            # Așteaptă puțin pentru ca Docker să fie complet funcțional
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
        # Verifică dacă containerul Portainer rulează
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
            return True
        
        # Verifică alternativ dacă portul 9000 răspunde
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


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Pornește Laboratorul Săptămânii 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python3 porneste_lab.py              # Pornire normală
  python3 porneste_lab.py --status     # Verifică doar starea
  python3 porneste_lab.py --rebuild    # Reconstruiește imaginile
  python3 porneste_lab.py --shell      # Pornește și deschide shell-ul

NOTĂ: Portainer rulează global pe portul 9000 și nu este gestionat de acest script.
      Accesați: http://localhost:9000 (stud / studstudstud)
        """
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Verifică doar starea serviciilor"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Reconstruiește imaginile Docker"
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Deschide un shell în container după pornire"
    )
    parser.add_argument(
        "-d", "--detasat",
        action="store_true",
        default=True,
        help="Rulează în background (implicit)"
    )
    args = parser.parse_args()

    afiseaza_banner()

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

    # Verifică status Portainer (doar avertisment, nu oprește execuția)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()

    # Doar verificare stare
    if args.status:
        docker.afiseaza_stare(SERVICII)
        
        # Afișează și starea Portainer
        if verifica_portainer_status():
            logger.info(f"✓ Portainer rulează pe {PORTAINER_URL}")
        else:
            logger.warning(f"✗ Portainer nu rulează")
        
        return 0

    logger.info("=" * 60)
    logger.info("Pornirea Mediului de Laborator - Săptămâna 1")
    logger.info("=" * 60)

    try:
        # Reconstruiește dacă este cerut
        if args.rebuild:
            logger.info("Se reconstruiesc imaginile Docker...")
            if not docker.compose_build(fara_cache=True):
                logger.error("Eroare la construirea imaginilor")
                return 1

        # Pornește containerele (fără Portainer - rulează global)
        if not docker.compose_up(detasat=args.detasat, profiluri=None):
            logger.error("Eroare la pornirea containerelor")
            return 1

        # Așteaptă să fie gata
        logger.info("Se așteaptă inițializarea serviciilor...")
        time.sleep(3)

        # Verifică serviciile
        toate_ok = True
        for nume, config in SERVICII.items():
            if docker.asteapta_container(config["container"], timeout=30):
                logger.info(f"✓ {config['descriere']} este gata")
            else:
                logger.error(f"✗ {config['descriere']} nu a pornit")
                toate_ok = False

        if toate_ok:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info(f"  • Container Lab: docker exec -it week1_lab bash")
            logger.info(f"  • Port TCP:      localhost:9090")
            logger.info(f"  • Port UDP:      localhost:9091")
            
            # Afișează status Portainer
            if verifica_portainer_status():
                logger.info(f"  • Portainer:     {PORTAINER_URL}")
            else:
                logger.warning(f"  • Portainer:     NU RULEAZĂ (vezi instrucțiuni mai sus)")
            
            logger.info("")
            logger.info("Pentru a opri laboratorul:")
            logger.info("  python3 scripts/opreste_lab.py")
            logger.info("=" * 60)

            # Deschide shell dacă este cerut
            if args.shell:
                logger.info("")
                logger.info("Se deschide shell-ul în container...")
                subprocess.run(["docker", "exec", "-it", "week1_lab", "bash"])

            return 0
        else:
            logger.error("Unele servicii nu au pornit. Verificați log-urile.")
            logger.error("  docker compose logs")
            return 1

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
