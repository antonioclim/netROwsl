#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 8
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

# Adaugă rădăcina proiectului la calea Python
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

# Coduri ANSI pentru culori
VERDE = "\033[92m"
ROSU = "\033[91m"
GALBEN = "\033[93m"
ALBASTRU = "\033[94m"
CYAN = "\033[96m"
RESETARE = "\033[0m"
BOLD = "\033[1m"


# Configurația serviciilor
SERVICII = {
    "nginx": {
        "container": "week8-nginx-1",
        "port": 8080,
        "verificare_sanatate": "/nginx-health",
        "timp_pornire": 5
    },
    "backend1": {
        "container": "week8-backend1-1",
        "port": None,  # Port intern
        "verificare_sanatate": None,
        "timp_pornire": 3
    },
    "backend2": {
        "container": "week8-backend2-1",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 3
    },
    "backend3": {
        "container": "week8-backend3-1",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 3
    },
    "portainer": {
        "container": "week8-portainer-1",
        "port": 9443,
        "verificare_sanatate": None,
        "timp_pornire": 5
    }
}


def afiseaza_banner():
    """Afișează banner-ul de pornire."""
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{CYAN}   Laborator Săptămâna 8 - Nivel Transport{RESETARE}")
    print(f"{CYAN}   Server HTTP și Proxy Invers{RESETARE}")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print()


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


def verifica_port_deschis(port: int, timeout: float = 1.0) -> bool:
    """Verifică dacă un port este deschis."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex(("127.0.0.1", port))
            return result == 0
    except Exception:
        return False


def verifica_sanatate_http(url: str, timeout: float = 5.0) -> bool:
    """Verifică dacă un endpoint HTTP răspunde."""
    try:
        with urlopen(url, timeout=timeout) as response:
            return 200 <= response.status < 300
    except Exception:
        return False


def asteapta_port(port: int, timeout: float = 30.0) -> bool:
    """Așteaptă ca un port să devină disponibil."""
    start = time.time()
    while time.time() - start < timeout:
        if verifica_port_deschis(port):
            return True
        time.sleep(0.5)
    return False


def ruleaza_compose(comanda: list, cwd: Path) -> tuple:
    """Rulează o comandă docker compose."""
    cmd = ["docker", "compose"] + comanda
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout la executarea comenzii"
    except Exception as e:
        return False, "", str(e)


def afiseaza_status_servicii():
    """Afișează starea serviciilor."""
    print(f"\n{ALBASTRU}Stare Servicii:{RESETARE}")
    print("-" * 50)
    
    for nume, config in SERVICII.items():
        port = config.get("port")
        if port:
            activ = verifica_port_deschis(port)
            status = f"{VERDE}● ACTIV{RESETARE}" if activ else f"{ROSU}○ INACTIV{RESETARE}"
            print(f"  {nume:15} port {port:5} {status}")
        else:
            # Pentru servicii fără port expus, verificăm containerul
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={config['container']}", "--format", "{{.Status}}"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                print(f"  {nume:15} {'intern':5} {VERDE}● ACTIV{RESETARE}")
            else:
                print(f"  {nume:15} {'intern':5} {ROSU}○ INACTIV{RESETARE}")


def porneste_laborator(reconstruieste: bool = False, verbose: bool = False):
    """Pornește mediul de laborator."""
    afiseaza_banner()
    
    # Verifică Docker
    print(f"{ALBASTRU}[INFO]{RESETARE} Verificare disponibilitate Docker...")
    if not verifica_docker_disponibil():
        print(f"{ROSU}[EROARE]{RESETARE} Docker nu este disponibil!")
        print("         Porniți Docker Desktop și încercați din nou.")
        return False
    print(f"{VERDE}[OK]{RESETARE} Daemon-ul Docker rulează")
    
    cale_docker = RADACINA_PROIECT / "docker"
    
    # Construiește imaginile dacă este necesar
    if reconstruieste:
        print(f"\n{ALBASTRU}[INFO]{RESETARE} Reconstruire imagini Docker...")
        succes, stdout, stderr = ruleaza_compose(["build", "--no-cache"], cale_docker)
        if not succes:
            print(f"{ROSU}[EROARE]{RESETARE} Construirea imaginilor a eșuat!")
            if verbose:
                print(stderr)
            return False
        print(f"{VERDE}[OK]{RESETARE} Imagini construite cu succes")
    
    # Pornește containerele
    print(f"\n{ALBASTRU}[INFO]{RESETARE} Pornire containere...")
    succes, stdout, stderr = ruleaza_compose(["up", "-d"], cale_docker)
    if not succes:
        print(f"{ROSU}[EROARE]{RESETARE} Pornirea containerelor a eșuat!")
        if verbose:
            print(stderr)
        return False
    print(f"{VERDE}[OK]{RESETARE} Containere pornite")
    
    # Așteaptă inițializarea
    print(f"\n{ALBASTRU}[INFO]{RESETARE} Așteptare inițializare servicii...")
    time.sleep(3)
    
    # Verifică nginx
    print(f"{ALBASTRU}[INFO]{RESETARE} Verificare sănătate nginx...")
    if asteapta_port(8080, timeout=30):
        print(f"{VERDE}[OK]{RESETARE} nginx răspunde pe portul 8080")
        
        # Verifică endpoint-ul de sănătate
        if verifica_sanatate_http("http://localhost:8080/nginx-health"):
            print(f"{VERDE}[OK]{RESETARE} Verificare sănătate nginx trecută")
        else:
            print(f"{GALBEN}[ATENȚIE]{RESETARE} Endpoint-ul de sănătate nu răspunde")
    else:
        print(f"{ROSU}[EROARE]{RESETARE} nginx nu răspunde!")
        return False
    
    # Verifică Portainer
    print(f"{ALBASTRU}[INFO]{RESETARE} Verificare Portainer...")
    if asteapta_port(9443, timeout=15):
        print(f"{VERDE}[OK]{RESETARE} Portainer disponibil pe portul 9443")
    else:
        print(f"{GALBEN}[ATENȚIE]{RESETARE} Portainer nu răspunde (opțional)")
    
    # Afișează informațiile de acces
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{VERDE}Mediul de laborator este pregătit!{RESETARE}")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print()
    print(f"{BOLD}Puncte de Acces:{RESETARE}")
    print(f"  Portainer:    {CYAN}https://localhost:9443{RESETARE}")
    print(f"  Proxy HTTP:   {CYAN}http://localhost:8080{RESETARE}")
    print(f"  Proxy HTTPS:  {CYAN}https://localhost:8443{RESETARE}")
    print()
    print(f"{BOLD}Test Rapid:{RESETARE}")
    print(f"  curl http://localhost:8080/")
    print(f"  curl -i http://localhost:8080/nginx-health")
    print()
    print(f"{BOLD}Observare Echilibrare Round-Robin:{RESETARE}")
    print(f"  for i in {{1..6}}; do curl -s http://localhost:8080/ | grep Backend; done")
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    
    return True


def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Pornire Laborator Săptămâna 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python porneste_laborator.py              # Pornire normală
  python porneste_laborator.py --status     # Doar verificare stare
  python porneste_laborator.py --reconstruieste  # Reconstruire imagini
        """
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Afișează doar starea serviciilor"
    )
    parser.add_argument(
        "--reconstruieste", "-r",
        action="store_true",
        help="Reconstruiește imaginile Docker înainte de pornire"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează ieșirea detaliată"
    )
    parser.add_argument(
        "--portainer",
        action="store_true",
        help="Deschide Portainer în browser după pornire"
    )
    
    args = parser.parse_args()
    
    if args.status:
        afiseaza_banner()
        afiseaza_status_servicii()
        return 0
    
    succes = porneste_laborator(
        reconstruieste=args.reconstruieste,
        verbose=args.verbose
    )
    
    if succes and args.portainer:
        import webbrowser
        webbrowser.open("https://localhost:9443")
    
    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
