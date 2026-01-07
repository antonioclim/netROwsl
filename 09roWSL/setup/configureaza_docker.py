#!/usr/bin/env python3
"""
Script Configurare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verifică și ajută la configurarea Docker Desktop pentru laborator.
"""

import subprocess
import sys
import json
from pathlib import Path


def afiseaza_titlu(titlu: str) -> None:
    """Afișează un titlu formatat."""
    print()
    print("=" * 50)
    print(titlu.center(50))
    print("=" * 50)
    print()


def verifica_docker_ruleaza() -> bool:
    """Verifică dacă Docker daemon rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def obtine_info_docker() -> dict:
    """Obține informații despre instalarea Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            return json.loads(rezultat.stdout)
    except Exception:
        pass
    return {}


def verifica_retea_docker() -> bool:
    """Verifică dacă pot fi create rețele Docker."""
    try:
        # Încearcă să creeze o rețea de test
        rezultat = subprocess.run(
            ["docker", "network", "create", "--driver", "bridge", "test_week9_net"],
            capture_output=True,
            timeout=10
        )
        
        if rezultat.returncode == 0:
            # Șterge rețeaua de test
            subprocess.run(
                ["docker", "network", "rm", "test_week9_net"],
                capture_output=True
            )
            return True
    except Exception:
        pass
    return False


def verifica_port(port: int) -> bool:
    """Verifică dacă un port este disponibil."""
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            rezultat = s.connect_ex(("localhost", port))
            # Dacă nu se poate conecta, portul e liber
            return rezultat != 0
    except Exception:
        return True


def verifica_porturi_necesare() -> dict:
    """Verifică disponibilitatea porturilor necesare."""
    porturi = {
        2121: "FTP Control",
        9443: "Portainer",
    }
    
    # Adaugă porturile passive
    for port in range(60000, 60011):
        porturi[port] = f"FTP Passiv"
    
    rezultate = {}
    for port, descriere in porturi.items():
        disponibil = verifica_port(port)
        rezultate[port] = {
            "descriere": descriere,
            "disponibil": disponibil
        }
    
    return rezultate


def afiseaza_stare(ok: bool, mesaj: str) -> None:
    """Afișează starea cu iconițe colorate."""
    if ok:
        print(f"  \033[92m✓\033[0m {mesaj}")
    else:
        print(f"  \033[91m✗\033[0m {mesaj}")


def main():
    """Funcția principală."""
    afiseaza_titlu("Configurare Docker")
    
    erori = 0
    
    # Verifică dacă Docker rulează
    print("Verificare Docker Daemon:")
    docker_ok = verifica_docker_ruleaza()
    afiseaza_stare(docker_ok, "Docker daemon activ")
    
    if not docker_ok:
        print("\n  Docker nu rulează. Vă rugăm să:")
        print("  1. Deschideți Docker Desktop")
        print("  2. Așteptați până când apare 'Docker is running'")
        print("  3. Rulați din nou acest script")
        return 1
    
    # Obține informații Docker
    print("\nInformații Docker:")
    info = obtine_info_docker()
    
    if info:
        print(f"  Versiune Server: {info.get('ServerVersion', 'necunoscut')}")
        print(f"  Sistem de Operare: {info.get('OperatingSystem', 'necunoscut')}")
        print(f"  Arhitectură: {info.get('Architecture', 'necunoscut')}")
        print(f"  CPU-uri: {info.get('NCPU', 'necunoscut')}")
        
        memorie_gb = info.get('MemTotal', 0) / (1024**3)
        print(f"  Memorie: {memorie_gb:.1f} GB")
        
        if memorie_gb < 4:
            print("\n  \033[93m⚠ Atenție: Se recomandă cel puțin 4GB RAM pentru Docker\033[0m")
    
    # Verifică rețeaua Docker
    print("\nVerificare Rețea Docker:")
    retea_ok = verifica_retea_docker()
    afiseaza_stare(retea_ok, "Creare rețele bridge")
    
    if not retea_ok:
        erori += 1
        print("  Nu se pot crea rețele Docker. Verificați:")
        print("  - Permisiunile Docker")
        print("  - Configurarea WSL2")
    
    # Verifică porturile
    print("\nVerificare Porturi:")
    porturi = verifica_porturi_necesare()
    
    porturi_ocupate = []
    for port, info in porturi.items():
        if not info["disponibil"]:
            porturi_ocupate.append(port)
    
    if not porturi_ocupate:
        afiseaza_stare(True, "Toate porturile necesare sunt disponibile")
    else:
        afiseaza_stare(False, f"Porturi ocupate: {porturi_ocupate[:5]}...")
        erori += 1
        print("\n  Porturile următoare sunt ocupate:")
        for port in porturi_ocupate[:10]:
            print(f"    - {port}: {porturi[port]['descriere']}")
        
        if len(porturi_ocupate) > 10:
            print(f"    ... și încă {len(porturi_ocupate) - 10} porturi")
        
        print("\n  Pentru a elibera porturile:")
        print("  1. Verificați ce le folosește: netstat -ano | findstr :<port>")
        print("  2. Opriți procesul sau schimbați portul în docker-compose.yml")
    
    # Sumar
    afiseaza_titlu("Rezultat")
    
    if erori == 0:
        print("  \033[92m✓ Docker este configurat corect!\033[0m")
        print()
        print("  Puteți porni laboratorul cu:")
        print("    python scripts/porneste_lab.py")
        return 0
    else:
        print(f"  \033[91m✗ {erori} probleme detectate\033[0m")
        print()
        print("  Vă rugăm să remediați problemele de mai sus.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
