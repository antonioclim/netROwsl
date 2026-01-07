#!/usr/bin/env python3
"""
Script de Configurare Docker Desktop
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă îndrumări pentru configurarea optimă a Docker Desktop pentru laborator.
"""

import subprocess
import sys
import json
from pathlib import Path


def afiseaza_banner():
    """Afișează bannerul de start."""
    print("=" * 60)
    print("Configurare Docker Desktop pentru Laborator")
    print("Laborator Rețele de Calculatoare - ASE, Informatică Economică")
    print("=" * 60)
    print()


def verifica_memorie_wsl():
    """Verifică și afișează configurația de memorie WSL2."""
    print("[1] Verificare configurație memorie WSL2...")
    
    # Verificăm fișierul .wslconfig
    wslconfig = Path.home() / ".wslconfig"
    
    if wslconfig.exists():
        print(f"    Fișier .wslconfig găsit: {wslconfig}")
        print("    Conținut actual:")
        with open(wslconfig, 'r') as f:
            for linie in f:
                print(f"      {linie.rstrip()}")
    else:
        print("    Nu există fișier .wslconfig")
        print()
        print("    RECOMANDARE: Creați fișierul %USERPROFILE%\\.wslconfig cu:")
        print("    ─" * 30)
        print("    [wsl2]")
        print("    memory=4GB")
        print("    processors=2")
        print("    swap=2GB")
        print("    ─" * 30)
    
    print()


def verifica_backend_docker():
    """Verifică dacă Docker folosește backend-ul WSL2."""
    print("[2] Verificare backend Docker...")
    
    try:
        rezultat = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if rezultat.returncode == 0:
            info = json.loads(rezultat.stdout)
            
            # Verificăm dacă folosește WSL2
            isolation = info.get("Isolation", "necunoscut")
            os_type = info.get("OSType", "necunoscut")
            
            print(f"    Tip SO: {os_type}")
            print(f"    Izolare: {isolation}")
            
            if "wsl" in str(info).lower():
                print("    ✓ Docker folosește backend-ul WSL2")
            else:
                print("    ⚠ Verificați în Docker Desktop > Settings > General")
                print("      că opțiunea 'Use the WSL 2 based engine' este activată")
    except Exception as e:
        print(f"    ✗ Nu s-a putut verifica: {e}")
    
    print()


def afiseaza_setari_retea():
    """Afișează informații despre configurația de rețea Docker."""
    print("[3] Configurație rețea Docker...")
    
    try:
        # Listăm rețelele Docker
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}\t{{.Driver}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if rezultat.returncode == 0:
            print("    Rețele Docker existente:")
            for linie in rezultat.stdout.strip().split('\n'):
                if linie:
                    print(f"      {linie}")
        
        print()
        print("    NOTĂ: Laboratorul va crea rețeaua 'week10_labnet' (172.20.0.0/24)")
        
    except Exception as e:
        print(f"    ✗ Nu s-a putut verifica: {e}")
    
    print()


def afiseaza_resurse_docker():
    """Afișează utilizarea resurselor Docker."""
    print("[4] Utilizare resurse Docker...")
    
    try:
        rezultat = subprocess.run(
            ["docker", "system", "df"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if rezultat.returncode == 0:
            print("    " + rezultat.stdout.replace('\n', '\n    '))
        
    except Exception as e:
        print(f"    ✗ Nu s-a putut verifica: {e}")
    
    print()


def afiseaza_recomandari():
    """Afișează recomandări pentru configurarea optimă."""
    print("[5] Recomandări de configurare...")
    print()
    print("    SETĂRI DOCKER DESKTOP RECOMANDATE:")
    print("    ─" * 30)
    print("    Settings > General:")
    print("      ☑ Use the WSL 2 based engine")
    print("      ☑ Start Docker Desktop when you sign in")
    print()
    print("    Settings > Resources > WSL Integration:")
    print("      ☑ Enable integration with my default WSL distro")
    print()
    print("    Settings > Docker Engine (docker daemon.json):")
    print('      {')
    print('        "log-driver": "json-file",')
    print('        "log-opts": {')
    print('          "max-size": "10m",')
    print('          "max-file": "3"')
    print('        }')
    print('      }')
    print("    ─" * 30)
    print()


def verifica_porturi():
    """Verifică porturile necesare pentru laborator."""
    print("[6] Verificare porturi necesare...")
    
    import socket
    
    porturi = {
        8000: "Server Web HTTP",
        5353: "Server DNS (UDP)",
        2222: "Server SSH",
        2121: "Server FTP",
        9443: "Portainer UI",
    }
    
    for port, descriere in porturi.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.bind(("0.0.0.0", port))
                print(f"    ✓ Port {port} ({descriere}) - disponibil")
        except OSError:
            print(f"    ✗ Port {port} ({descriere}) - OCUPAT")
            print(f"        Identificați procesul: netstat -ano | findstr :{port}")
    
    print()


def main():
    """Funcția principală."""
    afiseaza_banner()
    
    verifica_memorie_wsl()
    verifica_backend_docker()
    afiseaza_setari_retea()
    afiseaza_resurse_docker()
    afiseaza_recomandari()
    verifica_porturi()
    
    print("=" * 60)
    print("Configurare verificată!")
    print()
    print("Dacă toate verificările sunt în regulă, puteți rula:")
    print("  python scripts/porneste_lab.py")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
