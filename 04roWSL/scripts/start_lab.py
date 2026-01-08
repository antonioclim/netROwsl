#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 4
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
Suportă atât modul Docker cât și modul nativ (fără Docker).

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
Accesați Portainer la: http://localhost:9000 (credențiale: stud / studstudstud)
"""

import subprocess
import sys
import time
import argparse
import signal
import socket
from pathlib import Path
from typing import Optional

# Adaugă rădăcina proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("start_lab")

# Definiția serviciilor
# NOTĂ: Portainer NU este inclus - rulează global pe portul 9000
SERVICII = {
    "text": {
        "container": "saptamana4-text",
        "port": 5400,
        "protocol": "tcp",
        "descriere": "Server Protocol TEXT",
        "script": "src/apps/text_proto_server.py",
        "timp_pornire": 3
    },
    "binar": {
        "container": "saptamana4-binar",
        "port": 5401,
        "protocol": "tcp",
        "descriere": "Server Protocol BINAR",
        "script": "src/apps/binary_proto_server.py",
        "timp_pornire": 3
    },
    "udp": {
        "container": "saptamana4-senzor",
        "port": 5402,
        "protocol": "udp",
        "descriere": "Server Senzor UDP",
        "script": "src/apps/udp_sensor_server.py",
        "timp_pornire": 2
    }
}

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"

# Procese native pentru mod fără Docker
procese_native = []


def oprire_procese_native(signum=None, frame=None):
    """Oprește procesele native la întrerupere."""
    global procese_native
    for proces in procese_native:
        try:
            proces.terminate()
            proces.wait(timeout=2)
        except Exception:
            try:
                proces.kill()
            except Exception:
                pass
    procese_native = []
    if signum:
        sys.exit(0)


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


def verifica_port(port: int, protocol: str = "tcp") -> bool:
    """Verifică dacă un serviciu răspunde pe port."""
    try:
        if protocol == "tcp":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                rezultat = s.connect_ex(('localhost', port))
                return rezultat == 0
        else:  # UDP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(2)
                s.sendto(b"test", ('localhost', port))
                return True
    except Exception:
        return False


def porneste_mod_nativ(serviciu: Optional[str] = None):
    """Pornește serverele în mod nativ (fără Docker)."""
    global procese_native
    
    logger.info("Pornire în mod nativ (fără Docker)...")
    
    # Configurează handler pentru Ctrl+C
    signal.signal(signal.SIGINT, oprire_procese_native)
    signal.signal(signal.SIGTERM, oprire_procese_native)
    
    servicii_de_pornit = [serviciu] if serviciu else ["text", "binar", "udp"]
    
    for nume_svc in servicii_de_pornit:
        if nume_svc not in SERVICII:
            logger.error(f"Serviciu necunoscut: {nume_svc}")
            continue
            
        svc = SERVICII[nume_svc]
        if "script" not in svc:
            continue
            
        cale_script = RADACINA_PROIECT / svc["script"]
        if not cale_script.exists():
            logger.error(f"Script negăsit: {cale_script}")
            continue
        
        logger.info(f"Pornire {svc['descriere']} pe port {svc['port']}...")
        
        try:
            proces = subprocess.Popen(
                [sys.executable, str(cale_script)],
                cwd=str(RADACINA_PROIECT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            procese_native.append(proces)
            time.sleep(svc["timp_pornire"])
            
            if verifica_port(svc["port"], svc["protocol"]):
                logger.info(f"  ✓ {svc['descriere']} activ pe port {svc['port']}")
            else:
                logger.warning(f"  ⚠ {svc['descriere']} - portul nu răspunde încă")
                
        except Exception as e:
            logger.error(f"Eroare la pornirea {nume_svc}: {e}")
    
    if procese_native:
        logger.info("")
        logger.info("=" * 50)
        logger.info("Servere active în mod nativ!")
        logger.info("Apăsați Ctrl+C pentru oprire.")
        logger.info("=" * 50)
        
        # Așteaptă până la întrerupere
        try:
            while True:
                time.sleep(1)
                # Verifică dacă procesele mai rulează
                for p in procese_native:
                    if p.poll() is not None:
                        logger.warning("Un proces s-a oprit neașteptat")
        except KeyboardInterrupt:
            oprire_procese_native()


def porneste_mod_docker(rebuild: bool = False, serviciu: Optional[str] = None):
    """Pornește laboratorul în mod Docker."""
    
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
    
    # Verifică status Portainer (doar avertisment, nu oprește execuția)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    logger.info("=" * 60)
    logger.info("Pornire Mediu Laborator Săptămâna 4")
    logger.info("Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    logger.info("=" * 60)
    
    try:
        # Construiește imaginile dacă e necesar
        if rebuild:
            logger.info("Reconstruire imagini Docker...")
            docker.compose_build()
        
        # Pornește containerele (fără Portainer - rulează global)
        logger.info("Pornire containere...")
        docker.compose_up(detach=True)
        
        # Așteaptă inițializarea
        logger.info("Așteptare inițializare servicii...")
        for i in range(5):
            time.sleep(1)
            sys.stdout.write(f"\r  Progres: {i + 1}/5 secunde...")
            sys.stdout.flush()
        print()
        
        # Verificare servicii
        toate_ok = True
        for nume, svc in SERVICII.items():
            if serviciu and nume != serviciu:
                continue
                
            logger.info(f"Verificare {svc['descriere']}...")
            
            for incercare in range(5):
                if verifica_port(svc["port"], svc.get("protocol", "tcp")):
                    logger.info(f"  ✓ {svc['descriere']} activ pe port {svc['port']}")
                    break
                time.sleep(1)
            else:
                logger.warning(f"  ⚠ {svc['descriere']} nu răspunde pe port {svc['port']}")
                toate_ok = False
        
        if toate_ok:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            
            # Afișează status Portainer
            if verifica_portainer_status():
                logger.info(f"  • Portainer:       {PORTAINER_URL}")
            else:
                logger.warning(f"  • Portainer:       NU RULEAZĂ (vezi instrucțiuni mai sus)")
            
            logger.info(f"  • Protocol TEXT:   localhost:5400")
            logger.info(f"  • Protocol BINAR:  localhost:5401")
            logger.info(f"  • Senzor UDP:      localhost:5402")
            logger.info("")
            logger.info("Pentru a opri laboratorul:")
            logger.info("  python3 scripts/stop_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Unele servicii nu au pornit. Verificați jurnalele.")
            logger.info("Rulați: docker logs saptamana4-text")
            return 1
            
    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        return 1


def afiseaza_stare():
    """Afișează starea curentă a serviciilor."""
    print("\n" + "=" * 60)
    print("STARE SERVICII LABORATOR SĂPTĂMÂNA 4")
    print("=" * 60 + "\n")
    
    # Servicii de laborator
    print("Servicii de laborator:")
    print("-" * 40)
    for nume, svc in SERVICII.items():
        port = svc["port"]
        protocol = svc.get("protocol", "tcp")
        stare = "✓ ACTIV" if verifica_port(port, protocol) else "✗ INACTIV"
        culoare = "\033[92m" if "ACTIV" in stare else "\033[91m"
        print(f"  {svc['descriere']:25} {culoare}{stare}\033[0m  (port {port})")
    
    # Portainer (global)
    print("\nServicii globale:")
    print("-" * 40)
    stare_portainer = "✓ ACTIV" if verifica_portainer_status() else "✗ INACTIV"
    culoare = "\033[92m" if "ACTIV" in stare_portainer else "\033[91m"
    print(f"  {'Portainer':25} {culoare}{stare_portainer}\033[0m  (port {PORTAINER_PORT})")
    
    print("\n" + "=" * 60)
    
    # Verificare containere Docker
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=saptamana4", "--format", "table {{.Names}}\t{{.Status}}"],
            capture_output=True,
            timeout=5
        )
        if rezultat.returncode == 0 and rezultat.stdout:
            print("\nContainere Docker laborator:")
            print(rezultat.stdout.decode())
    except Exception:
        pass


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Pornire Laborator Săptămâna 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python3 scripts/start_lab.py              # Pornire mod Docker
  python3 scripts/start_lab.py --native     # Pornire fără Docker
  python3 scripts/start_lab.py --service text  # Pornire doar server TEXT
  python3 scripts/start_lab.py --status     # Verificare stare

NOTĂ: Portainer rulează global pe portul 9000 și nu este gestionat de acest script.
      Accesați: http://localhost:9000 (stud / studstudstud)
        """
    )
    parser.add_argument("--status", action="store_true", 
                        help="Verifică doar starea serviciilor")
    parser.add_argument("--rebuild", action="store_true", 
                        help="Reconstruiește imaginile Docker")
    parser.add_argument("--native", action="store_true",
                        help="Rulează în mod nativ (fără Docker)")
    parser.add_argument("--service", "-s", choices=["text", "binar", "udp"],
                        help="Pornește doar un serviciu specific")
    parser.add_argument("--logs", action="store_true",
                        help="Afișează jurnalele containerului")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Afișează informații detaliate")
    
    args = parser.parse_args()
    
    if args.status:
        afiseaza_stare()
        return 0
    
    if args.logs:
        try:
            subprocess.run(["docker", "logs", "-f", "saptamana4-text"])
        except KeyboardInterrupt:
            pass
        return 0
    
    if args.native:
        porneste_mod_nativ(args.service)
        return 0
    
    return porneste_mod_docker(args.rebuild, args.service)


if __name__ == "__main__":
    sys.exit(main())
