#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

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

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_laborator")

# Definirea serviciilor și configurațiile lor
# NOTĂ: Portainer NU este inclus - rulează global pe portul 9000
SERVICII = {
    "python": {
        "container": "week5_python",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 5,
        "descriere": "Container principal Python pentru exerciții"
    },
    "server-udp": {
        "container": "week5_udp-server",
        "port": 9999,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Server UDP Echo pentru demonstrații"
    },
    "client-udp": {
        "container": "week5_udp-client",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Client UDP pentru testare"
    }
}

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"


def afiseaza_banner():
    """Afișează bannerul de pornire."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║           SĂPTĂMÂNA 5 - LABORATOR REȚELE DE CALCULATOARE        ║
║                                                                  ║
║         Nivelul Rețea: Adresare IPv4/IPv6 și Subnetare          ║
║                                                                  ║
║              ASE București - Informatică Economică               ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


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


def main():
    parser = argparse.ArgumentParser(
        description="Pornește mediul de laborator pentru Săptămâna 5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python3 porneste_laborator.py          # Pornește toate serviciile
  python3 porneste_laborator.py --status # Verifică starea serviciilor
  python3 porneste_laborator.py --reconstruieste  # Reconstruiește imaginile

NOTĂ: Portainer rulează global pe portul 9000 și nu este gestionat de acest script.
      Accesați: http://localhost:9000 (stud / studstudstud)
        """
    )
    parser.add_argument(
        "--status", 
        action="store_true", 
        help="Doar verifică starea serviciilor"
    )
    parser.add_argument(
        "--reconstruieste", 
        action="store_true", 
        help="Forțează reconstruirea imaginilor Docker"
    )
    parser.add_argument(
        "--detasat", "-d", 
        action="store_true", 
        default=True,
        help="Rulează în modul detașat (implicit)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate"
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

    # Doar verifică starea dacă este cerut
    if args.status:
        logger.info("Verificare stare servicii...")
        docker.afiseaza_status(SERVICII)
        
        # Afișează și status Portainer
        print("\nServicii globale:")
        print("-" * 40)
        stare_portainer = "✓ ACTIV" if verifica_portainer_status() else "✗ INACTIV"
        print(f"  Portainer (global): {stare_portainer} (port {PORTAINER_PORT})")
        
        return 0

    # Verifică status Portainer (doar avertisment, nu oprește execuția)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()

    logger.info("=" * 60)
    logger.info("Pornire mediu de laborator Săptămâna 5")
    logger.info("=" * 60)

    try:
        # Construiește și pornește containerele
        if args.reconstruieste:
            logger.info("Reconstruire imagini Docker...")
            docker.compose_build()
        
        logger.info("Pornire containere...")
        docker.compose_up(detasat=args.detasat)

        # Așteaptă inițializarea serviciilor
        logger.info("Așteptare inițializare servicii...")
        for i in range(5):
            time.sleep(1)
            sys.stdout.write(f"\r  Progres: {i + 1}/5 secunde...")
            sys.stdout.flush()
        print()

        # Verificări de sănătate
        logger.info("Verificare sănătate servicii...")
        toate_sanatoase = docker.verifica_servicii(SERVICII)

        if toate_sanatoase:
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            
            # Afișează status Portainer
            if verifica_portainer_status():
                logger.info(f"  • Portainer: {PORTAINER_URL}")
            else:
                logger.warning(f"  • Portainer: NU RULEAZĂ (vezi instrucțiuni mai sus)")
            
            logger.info("")
            logger.info("Containere active:")
            for nume, svc in SERVICII.items():
                port_info = f":{svc['port']}" if svc['port'] else ""
                logger.info(f"  • {svc['container']}{port_info} - {svc['descriere']}")
            logger.info("")
            logger.info("Rețea Docker: week5_labnet (10.5.0.0/24)")
            logger.info("=" * 60)
            logger.info("")
            logger.info("Pentru a rula exercițiile:")
            logger.info("  python3 src/exercises/ex_5_01_cidr_flsm.py 192.168.10.14/26")
            logger.info("")
            logger.info("Pentru a opri laboratorul:")
            logger.info("  python3 scripts/opreste_laborator.py")
            logger.info("")
            return 0
        else:
            logger.error("Unele servicii nu au pornit. Verificați jurnalele de mai sus.")
            logger.info("Încercați: docker compose -f docker/docker-compose.yml logs")
            return 1

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
