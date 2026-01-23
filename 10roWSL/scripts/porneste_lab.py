#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 10
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

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

# Adaugă rădăcina proiectului la calea Python

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

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

# Configurația serviciilor laboratorului (FĂRĂ Portainer - rulează global)
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
}



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

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


def afiseaza_banner():
    """Afișează bannerul de pornire."""
    print()
    print("=" * 60)
    print("  LABORATOR SĂPTĂMÂNA 10 - Servicii de Rețea")
    print("  HTTP/S, REST, DNS, SSH, FTP în containere Docker")
    print("  Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()


def afiseaza_puncte_acces():
    """Afișează punctele de acces pentru servicii."""
    print()
    print("─" * 60)
    print("  PUNCTE DE ACCES SERVICII")
    print("─" * 60)
    print()
    
    # Status Portainer
    if verifica_portainer_status():
        print(f"  Portainer (Management Docker): ✓ ACTIV")
        print(f"    → {PORTAINER_URL}")
    else:
        print("  Portainer (Management Docker): ✗ INACTIV")
        print("    → Vezi instrucțiunile de mai sus pentru pornire")
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



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

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
    args = parser.parse_args()

    afiseaza_banner()

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
        docker = ManagerDocker(RADACINA_PROIECT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Eroare: {e}")
        logger.error("Asigurați-vă că rulați scriptul din directorul 10roWSL")
        return 1

    if args.stare:
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
            logger.info("")
            logger.info("Pentru oprire: python3 scripts/opreste_lab.py")
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



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
