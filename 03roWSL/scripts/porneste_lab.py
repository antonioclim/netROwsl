#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 3
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
Accesați Portainer la: http://localhost:9000 (credențiale: stud / studstudstud)

Utilizare:
    python3 scripts/porneste_lab.py [--status] [--rebuild] [--broadcast]
"""

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path

# Adaugă rădăcina proiectului în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Configurația serviciilor
# NOTĂ: Portainer NU este inclus - rulează global pe portul 9000
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
    }
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
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
            return True
        
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
    
    # Status Portainer (global)
    print("\nServicii globale:")
    print("-" * 40)
    if verifica_portainer_status():
        print(f"  portainer    ✓ Activ      Interfață Web Management:9000 (global)")
    else:
        print(f"  portainer    ✗ Inactiv    Interfață Web Management:9000 (global)")
    
    print("\n" + "=" * 60)


def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Pornește Laboratorul Săptămânii 3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python3 porneste_lab.py              # Pornire normală
  python3 porneste_lab.py --status     # Verificare stare
  python3 porneste_lab.py --broadcast  # Pornește și receiver
  python3 porneste_lab.py --rebuild    # Reconstruire imagini

NOTĂ: Portainer rulează global pe portul 9000 și nu este gestionat de acest script.
      Accesați: http://localhost:9000 (stud / studstudstud)
        """
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
        "-d", "--detach",
        action="store_true",
        default=True,
        help="Rulează în mod detașat (implicit)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Afișează informații detaliate"
    )
    args = parser.parse_args()

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

    # Construiește lista de profiluri
    profiluri = []
    if args.broadcast:
        profiluri.append("broadcast")

    # Verifică status Portainer (doar avertisment, nu oprește execuția)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()

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

        # Pornește containerele (fără Portainer - rulează global)
        logger.info("Pornire containere...")
        docker.compose_up(detach=True, profiluri=profiluri)

        # Așteaptă serviciile
        timp_asteptare = max(s["timp_pornire"] for s in SERVICII.values())
        if "broadcast" in profiluri:
            timp_asteptare = max(timp_asteptare, SERVICII_OPTIONALE["receiver"]["timp_pornire"])
        
        logger.info(f"Așteptare inițializare servicii ({timp_asteptare}s)...")
        for i in range(timp_asteptare):
            time.sleep(1)
            sys.stdout.write(f"\r  Progres: {i + 1}/{timp_asteptare} secunde...")
            sys.stdout.flush()
        print()

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

        if toate_ok:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            
            # Afișează status Portainer
            if verifica_portainer_status():
                logger.info(f"  • Portainer:      {PORTAINER_URL}")
            else:
                logger.warning(f"  • Portainer:      NU RULEAZĂ (vezi instrucțiuni mai sus)")
            
            logger.info(f"  • Server Echo:    localhost:8080")
            logger.info(f"  • Tunel TCP:      localhost:9090")
            if "broadcast" in profiluri:
                logger.info(f"  • Receiver UDP:   172.20.0.101:5007/5008")
            logger.info("")
            logger.info("Container interactiv:")
            logger.info("  docker exec -it week3_client bash")
            logger.info("")
            logger.info("Pentru a opri laboratorul:")
            logger.info("  python3 scripts/opreste_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Unele servicii nu au pornit corect.")
            logger.error("Verificați log-urile: docker logs week3_<serviciu>")
            return 1

    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
