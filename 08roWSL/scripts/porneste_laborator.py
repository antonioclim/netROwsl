#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 8
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

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
from urllib.request import urlopen
from urllib.error import URLError

# Adaugă rădăcina proiectului la calea Python

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

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

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"

# Configurația serviciilor (FĂRĂ Portainer - rulează global)
SERVICII = {
    "nginx": {
        "container": "week8-nginx-proxy",
        "port": 8080,
        "verificare_sanatate": "/nginx-health",
        "timp_pornire": 5
    },
    "backend1": {
        "container": "week8-backend-1",
        "port": None,  # Port intern
        "verificare_sanatate": None,
        "timp_pornire": 3
    },
    "backend2": {
        "container": "week8-backend-2",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 3
    },
    "backend3": {
        "container": "week8-backend-3",
        "port": None,
        "verificare_sanatate": None,
        "timp_pornire": 3
    }
}



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_banner():
    """Afișează banner-ul de pornire."""
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{CYAN}   Laborator Săptămâna 8 - Nivel Transport{RESETARE}")
    print(f"{CYAN}   Server HTTP și Proxy Invers{RESETARE}")
    print(f"{CYAN}   Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer{RESETARE}")
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


def porneste_docker_service() -> bool:
    """Încearcă să pornească serviciul Docker în WSL."""
    print(f"{ALBASTRU}[INFO]{RESETARE} Se încearcă pornirea serviciului Docker...")
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
            print(f"{ROSU}[EROARE]{RESETARE} Eroare la pornirea Docker: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"{ROSU}[EROARE]{RESETARE} Timeout la pornirea serviciului Docker")
        return False
    except Exception as e:
        print(f"{ROSU}[EROARE]{RESETARE} Eroare neașteptată: {e}")
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
    print(f"{GALBEN}{'=' * 60}{RESETARE}")
    print(f"{GALBEN}⚠️  AVERTISMENT: Portainer nu rulează!{RESETARE}")
    print()
    print(f"Portainer este instrumentul vizual pentru gestionarea Docker.")
    print(f"Pentru a-l porni, executați în terminal:")
    print()
    print(f"  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    print(f"    -v /var/run/docker.sock:/var/run/docker.sock \\")
    print(f"    -v portainer_data:/data portainer/portainer-ce:latest")
    print()
    print(f"După pornire, accesați: {CYAN}{PORTAINER_URL}{RESETARE}")
    print(f"Credențiale: {PORTAINER_USER} / {PORTAINER_PASS}")
    print(f"{GALBEN}{'=' * 60}{RESETARE}")
    print()


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
    print(f"\n{ALBASTRU}Stare Servicii Laborator:{RESETARE}")
    print("-" * 50)
    
    for nume, config in SERVICII.items():
        port = config.get("port")
        container = config.get("container")
        if port:
            activ = verifica_port_deschis(port)
            status = f"{VERDE}● ACTIV{RESETARE}" if activ else f"{ROSU}○ INACTIV{RESETARE}"
            print(f"  {nume:15} port {port:5} {status}")
        else:
            # Pentru servicii fără port expus, verificăm containerul
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={container}", "--format", "{{.Status}}"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                print(f"  {nume:15} {'intern':5} {VERDE}● ACTIV{RESETARE}")
            else:
                print(f"  {nume:15} {'intern':5} {ROSU}○ INACTIV{RESETARE}")
    
    # Afișează status Portainer (serviciu global)
    print()
    print(f"{ALBASTRU}Servicii Globale:{RESETARE}")
    print("-" * 50)
    if verifica_portainer_status():
        print(f"  {'Portainer':15} port {PORTAINER_PORT:5} {VERDE}● ACTIV{RESETARE}")
    else:
        print(f"  {'Portainer':15} port {PORTAINER_PORT:5} {ROSU}○ INACTIV{RESETARE}")


def porneste_laborator(reconstruieste: bool = False, verbose: bool = False):
    """Pornește mediul de laborator."""
    afiseaza_banner()
    
    # Verifică Docker
    print(f"{ALBASTRU}[INFO]{RESETARE} Verificare disponibilitate Docker...")
    if not verifica_docker_disponibil():
        print(f"{GALBEN}[ATENȚIE]{RESETARE} Docker nu este disponibil. Se încearcă pornirea automată...")
        if not porneste_docker_service():
            print(f"{ROSU}[EROARE]{RESETARE} Nu s-a putut porni Docker!")
            print("         Încercați manual: sudo service docker start")
            print("         (Parolă: stud)")
            return False
        print(f"{VERDE}[OK]{RESETARE} Docker a fost pornit cu succes!")
    else:
        print(f"{VERDE}[OK]{RESETARE} Daemon-ul Docker rulează")
    
    # Verifică status Portainer (doar avertisment)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()
    
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
    
    # Afișează informațiile de acces
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{VERDE}✓ Mediul de laborator este pregătit!{RESETARE}")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print()
    print(f"{BOLD}Puncte de Acces:{RESETARE}")
    
    # Status Portainer
    if verifica_portainer_status():
        print(f"  Portainer:    {CYAN}{PORTAINER_URL}{RESETARE}")
    else:
        print(f"  Portainer:    {GALBEN}NU RULEAZĂ{RESETARE} (vezi instrucțiuni mai sus)")
    
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
    print(f"Pentru oprire: python3 scripts/opreste_laborator.py")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Pornire Laborator Săptămâna 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python3 porneste_laborator.py              # Pornire normală
  python3 porneste_laborator.py --status     # Doar verificare stare
  python3 porneste_laborator.py --reconstruieste  # Reconstruire imagini
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
    
    args = parser.parse_args()
    
    if args.status:
        afiseaza_banner()
        afiseaza_status_servicii()
        return 0
    
    succes = porneste_laborator(
        reconstruieste=args.reconstruieste,
        verbose=args.verbose
    )
    
    return 0 if succes else 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
