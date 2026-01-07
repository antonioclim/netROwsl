#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 3
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.

Utilizare:
    python scripts/porneste_lab.py [--status] [--rebuild] [--broadcast] [--portainer]
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Configurația serviciilor
SERVICII = {
    "server": {
        "container": "week3_server",
        "port": 8080,
        "verificare_sanatate": "tcp",
        "timp_pornire": 5,
        "descriere": "Server Echo TCP"
    },
    "router": {
        "container": "week3_router",
        "port": 9090,
        "verificare_sanatate": "tcp",
        "timp_pornire": 8,
        "descriere": "Tunel TCP"
    },
    "client": {
        "container": "week3_client",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Container Testare"
    }
}

SERVICII_OPTIONALE = {
    "receiver": {
        "container": "week3_receiver",
        "port": 5007,
        "verificare_sanatate": None,
        "timp_pornire": 3,
        "descriere": "Receptor Broadcast/Multicast",
        "profil": "broadcast"
    },
    "portainer": {
        "container": "week3_portainer",
        "port": 9443,
        "verificare_sanatate": "https",
        "timp_pornire": 10,
        "descriere": "Interfață Web Management",
        "profil": "management"
    }
}


def verifica_serviciu(container: str, port: int = None, tip: str = None) -> bool:
    """
    Verifică dacă un serviciu este funcțional.
    
    Args:
        container: Numele containerului
        port: Portul de verificat (opțional)
        tip: Tipul verificării ('tcp', 'https', None)
    
    Returns:
        True dacă serviciul funcționează
    """
    # Verifică dacă containerul rulează
    try:
        rezultat = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", container],
            capture_output=True,
            timeout=10
        )
        if "true" not in rezultat.stdout.decode().lower():
            return False
    except Exception:
        return False
    
    # Verificare port dacă este specificat
    if port and tip == "tcp":
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            rezultat = sock.connect_ex(("localhost", port))
            sock.close()
            return rezultat == 0
        except Exception:
            return False
    
    return True


def afiseaza_status(profiluri: list = None):
    """Afișează statusul tuturor serviciilor."""
    print("\n" + "=" * 60)
    print("STATUS LABORATOR SĂPTĂMÂNA 3")
    print("=" * 60)
    
    print("\nServicii principale:")
    print("-" * 40)
    for nume, config in SERVICII.items():
        stare = "✓ Activ" if verifica_serviciu(
            config["container"], 
            config["port"],
            config["verificare_sanatate"]
        ) else "✗ Inactiv"
        port_str = f":{config['port']}" if config['port'] else ""
        print(f"  {nume:12} {stare:12} {config['descriere']}{port_str}")
    
    print("\nServicii opționale:")
    print("-" * 40)
    for nume, config in SERVICII_OPTIONALE.items():
        stare = "✓ Activ" if verifica_serviciu(
            config["container"],
            config["port"],
            config["verificare_sanatate"]
        ) else "✗ Inactiv"
        port_str = f":{config['port']}" if config['port'] else ""
        profil_str = f"(profil: {config['profil']})"
        print(f"  {nume:12} {stare:12} {config['descriere']}{port_str} {profil_str}")
    
    print("\n" + "=" * 60)


def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Pornește Laboratorul Săptămânii 3"
    )
    parser.add_argument(
        "--status", 
        action="store_true",
        help="Afișează doar statusul serviciilor"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true", 
        help="Reconstruiește imaginile Docker"
    )
    parser.add_argument(
        "--broadcast",
        action="store_true",
        help="Pornește și containerul receiver pentru broadcast/multicast"
    )
    parser.add_argument(
        "--portainer",
        action="store_true",
        help="Pornește și interfața web Portainer"
    )
    parser.add_argument(
        "-d", "--detach",
        action="store_true",
        default=True,
        help="Rulează în mod detașat (implicit)"
    )
    args = parser.parse_args()

    # Construiește lista de profiluri
    profiluri = []
    if args.broadcast:
        profiluri.append("broadcast")
    if args.portainer:
        profiluri.append("management")

    if args.status:
        afiseaza_status(profiluri)
        return 0

    logger.info("=" * 60)
    logger.info("Pornire Laborator Săptămâna 3")
    logger.info("Rețele de Calculatoare - ASE, Informatică Economică")
    logger.info("=" * 60)

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    try:
        # Reconstruiește imaginile dacă este cerut
        if args.rebuild:
            logger.info("Reconstruire imagini Docker...")
            docker.compose_build()

        # Pornește containerele
        logger.info("Pornire containere...")
        docker.compose_up(detach=True, profiluri=profiluri)

        # Așteaptă serviciile
        timp_asteptare = max(s["timp_pornire"] for s in SERVICII.values())
        if profiluri:
            timp_asteptare = max(timp_asteptare, 
                max(SERVICII_OPTIONALE[p.replace("management", "portainer").replace("broadcast", "receiver")]["timp_pornire"] 
                    for p in profiluri if p in ["broadcast", "management"]))
        
        logger.info(f"Așteptare inițializare servicii ({timp_asteptare}s)...")
        time.sleep(timp_asteptare)

        # Verifică serviciile
        logger.info("Verificare stare servicii...")
        toate_ok = True
        
        for nume, config in SERVICII.items():
            if verifica_serviciu(config["container"], config["port"], config["verificare_sanatate"]):
                logger.info(f"  ✓ {nume}: funcțional")
            else:
                logger.error(f"  ✗ {nume}: nu răspunde")
                toate_ok = False

        if "broadcast" in profiluri:
            config = SERVICII_OPTIONALE["receiver"]
            if verifica_serviciu(config["container"]):
                logger.info(f"  ✓ receiver: funcțional")
            else:
                logger.warning(f"  ⚠ receiver: nu a pornit")

        if "management" in profiluri:
            config = SERVICII_OPTIONALE["portainer"]
            if verifica_serviciu(config["container"]):
                logger.info(f"  ✓ portainer: funcțional")
            else:
                logger.warning(f"  ⚠ portainer: nu a pornit")

        if toate_ok:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info("  Server Echo:  localhost:8080")
            logger.info("  Tunel TCP:    localhost:9090")
            if "management" in profiluri:
                logger.info("  Portainer:    https://localhost:9443")
            logger.info("")
            logger.info("Container interactiv:")
            logger.info("  docker exec -it week3_client bash")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Unele servicii nu au pornit corect.")
            logger.error("Verificați log-urile: docker logs week3_<serviciu>")
            return 1

    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
