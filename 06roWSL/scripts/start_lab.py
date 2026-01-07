#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 6
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator
pentru exercițiile NAT/PAT și SDN.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, ProgressLogger

logger = setup_logger("start_lab")

# Definiții servicii pentru Săptămâna 6
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
SERVICII_OPTIONALE = {
    "sdn-controller": {
        "container": "week6_controller",
        "port": 6633,
        "health_check": None,
        "startup_time": 5,
        "description": "Controller SDN (OS-Ken)",
        "profile": "controller"
    },
    "portainer": {
        "container": "week6_portainer",
        "port": 9443,
        "health_check": None,
        "startup_time": 15,
        "description": "Panou de administrare containere",
        "profile": "management"
    },
}


def afiseaza_banner():
    """Afișează banner-ul de pornire."""
    print()
    print("=" * 60)
    print("  Săptămâna 6: NAT/PAT și Laborator SDN")
    print("  Disciplina REȚELE DE CALCULATOARE - ASE | de Revolvix")
    print("=" * 60)
    print()


def afiseaza_informatii_acces(servicii_pornite: dict):
    """Afișează informațiile de acces pentru serviciile pornite."""
    print()
    print("Puncte de acces:")
    print("-" * 60)
    
    if "week6-lab" in servicii_pornite:
        print("  Lab principal: docker exec -it week6_lab bash")
        print("                 (sau folosește docker compose run --rm week6-lab)")
    
    if "sdn-controller" in servicii_pornite:
        print("  Controller:    localhost:6633 (OpenFlow)")
    
    if "portainer" in servicii_pornite:
        print("  Portainer:     https://localhost:9443")
    
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
        "--portainer",
        action="store_true",
        help="Pornește și interfața de administrare Portainer"
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
    
    # Localizează docker-compose.yml
    director_docker = RADACINA_PROIECT / "docker"
    
    try:
        docker = DockerManager(director_docker)
    except FileNotFoundError as e:
        logger.error(f"Configurația Docker nu a fost găsită: {e}")
        return 1
    
    # Doar verificare stare
    if args.status:
        afiseaza_banner()
        toate_serviciile = {**SERVICII, **SERVICII_OPTIONALE}
        docker.show_status(toate_serviciile)
        return 0
    
    afiseaza_banner()
    
    # Determină ce profile să activeze
    profile = []
    servicii_de_pornit = dict(SERVICII)
    
    if args.controller:
        profile.append("controller")
        servicii_de_pornit["sdn-controller"] = SERVICII_OPTIONALE["sdn-controller"]
    
    if args.portainer:
        profile.append("management")
        servicii_de_pornit["portainer"] = SERVICII_OPTIONALE["portainer"]
    
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
