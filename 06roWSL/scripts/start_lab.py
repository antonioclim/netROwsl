#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 6
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator
pentru exercițiile NAT/PAT și SDN.

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

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, ProgressLogger

logger = setup_logger("start_lab")

# Definiții servicii pentru Săptămâna 6
# NOTĂ: Portainer NU este inclus - rulează global pe portul 9000
SERVICII = {
    "week6-lab": {
        "container": "week6_lab",
        "port": None,  # Fără port expus (folosește rețea host)
        "health_check": None,
        "startup_time": 10,
        "description": "Mediu principal de laborator cu Mininet"
    },
}

# Servicii opționale (activate cu profile)
# NOTĂ: Portainer a fost eliminat - rulează global pe portul 9000
SERVICII_OPTIONALE = {
    "sdn-controller": {
        "container": "week6_controller",
        "port": 6633,
        "health_check": None,
        "startup_time": 5,
        "description": "Controller SDN (OS-Ken)",
        "profile": "controller"
    },
}

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"


def afiseaza_banner():
    """Afișează banner-ul de pornire."""
    print()
    print("=" * 60)
    print("  Săptămâna 6: NAT/PAT și Laborator SDN")
    print("  Disciplina REȚELE DE CALCULATOARE - ASE | de Revolvix")
    print("=" * 60)
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


def afiseaza_informatii_acces(servicii_pornite: dict):
    """Afișează informațiile de acces pentru serviciile pornite."""
    print()
    print("Puncte de acces:")
    print("-" * 60)
    
    # Afișează status Portainer
    if verifica_portainer_status():
        print(f"  Portainer:     {PORTAINER_URL}")
    else:
        print(f"  Portainer:     NU RULEAZĂ (vezi instrucțiuni mai sus)")
    
    if "week6-lab" in servicii_pornite:
        print("  Lab principal: docker exec -it week6_lab bash")
        print("                 (sau folosește docker compose run --rm week6-lab)")
    
    if "sdn-controller" in servicii_pornite:
        print("  Controller:    localhost:6633 (OpenFlow)")
    
    print("-" * 60)
    print()
    print("Comenzi rapide (în interiorul containerului):")
    print("  make nat-demo    - Pornește topologia NAT")
    print("  make sdn-demo    - Pornește topologia SDN")
    print("  make check       - Verifică dependențele")
    print("  make clean       - Curăță Mininet")
    print()


def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Pornește mediul de laborator Săptămâna 6"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Verifică doar starea, nu pornește serviciile"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Forțează reconstruirea imaginilor Docker"
    )
    parser.add_argument(
        "--controller",
        action="store_true",
        help="Pornește și controller-ul SDN"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=False,
        help="Rulează containerele în modul detașat"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișare detaliată"
    )
    args = parser.parse_args()
    
    if args.verbose:
        from scripts.utils.logger import set_verbose
        set_verbose(logger, True)
    
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
    
    # Localizează docker-compose.yml
    director_docker = RADACINA_PROIECT / "docker"
    
    try:
        docker = DockerManager(director_docker)
    except FileNotFoundError as e:
        logger.error(f"Configurația Docker nu a fost găsită: {e}")
        return 1
    
    # Doar verificare stare
    if args.status:
        toate_serviciile = {**SERVICII, **SERVICII_OPTIONALE}
        docker.show_status(toate_serviciile)
        
        # Afișează și status Portainer
        print("\nServicii globale:")
        print("-" * 40)
        stare_portainer = "✓ ACTIV" if verifica_portainer_status() else "✗ INACTIV"
        print(f"  Portainer (global): {stare_portainer} (port {PORTAINER_PORT})")
        
        return 0
    
    # Verifică status Portainer (doar avertisment, nu oprește execuția)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()
    
    # Determină ce profile să activeze
    profile = []
    servicii_de_pornit = dict(SERVICII)
    
    if args.controller:
        profile.append("controller")
        servicii_de_pornit["sdn-controller"] = SERVICII_OPTIONALE["sdn-controller"]
    
    try:
        with ProgressLogger(logger, "Pornirea mediului de laborator", 4) as progress:
            # Pasul 1: Construiește imaginile
            if args.rebuild:
                progress.step("Construirea imaginilor Docker (--rebuild specificat)")
                if not docker.compose_build(no_cache=args.rebuild):
                    logger.error("Eșec la construirea imaginilor Docker")
                    return 1
            else:
                progress.step("Verificarea imaginilor Docker")
                docker.compose_build()  # Construiește dacă nu există
            
            # Pasul 2: Pornește serviciile
            progress.step("Pornirea containerelor Docker")
            if not docker.compose_up(detach=args.detach or True, profiles=profile if profile else None):
                logger.error("Eșec la pornirea serviciilor")
                return 1
            
            # Pasul 3: Așteaptă pornirea
            progress.step("Așteptarea inițializării serviciilor")
            time.sleep(5)
            
            # Pasul 4: Verifică serviciile
            progress.step("Verificarea serviciilor")
            toate_sanatoase = docker.verify_services(servicii_de_pornit)
        
        if toate_sanatoase:
            print()
            print("=" * 60)
            print("  ✓ Mediul de laborator este pregătit!")
            print("=" * 60)
            afiseaza_informatii_acces(servicii_de_pornit)
            
            if not args.detach:
                print("Notă: Rulează cu -d/--detach pentru a rula în fundal")
            
            print("Pentru a opri laboratorul:")
            print("  python3 scripts/stop_lab.py")
            print()
            
            return 0
        else:
            logger.warning("Unele servicii pot să nu fie complet pregătite")
            logger.info("Verifică logurile cu: docker compose -f docker/docker-compose.yml logs")
            return 1
    
    except KeyboardInterrupt:
        print("\nPornire întreruptă")
        return 130
    except Exception as e:
        logger.error(f"Eșec la pornirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
