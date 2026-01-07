#!/usr/bin/env python3
"""
Script de Instalare a Cerințelor Preliminare
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Automatizează instalarea dependențelor necesare pentru laboratorul Săptămânii 12.
"""

import subprocess
import sys
import os
from pathlib import Path


def afiseaza_antet(mesaj: str):
    """Afișează un antet formatat."""
    print("\n" + "=" * 60)
    print(f"  {mesaj}")
    print("=" * 60)


def afiseaza_pas(numar: int, mesaj: str):
    """Afișează un pas numerotat."""
    print(f"\n[Pasul {numar}] {mesaj}")
    print("-" * 40)


def ruleaza_comanda(comanda: list, descriere: str) -> bool:
    """Rulează o comandă și afișează rezultatul."""
    print(f"  Executare: {' '.join(comanda)}")
    try:
        rezultat = subprocess.run(
            comanda,
            capture_output=True,
            text=True,
            timeout=300
        )
        if rezultat.returncode == 0:
            print(f"  ✓ {descriere} - SUCCES")
            return True
        else:
            print(f"  ✗ {descriere} - EȘUAT")
            if rezultat.stderr:
                print(f"    Eroare: {rezultat.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ {descriere} - TIMEOUT")
        return False
    except Exception as e:
        print(f"  ✗ {descriere} - EROARE: {e}")
        return False


def instaleaza_pachete_python():
    """Instalează pachetele Python necesare."""
    pachete = [
        "grpcio>=1.50.0",
        "grpcio-tools>=1.50.0",
        "protobuf>=4.21.0",
        "dnspython>=2.3.0",
        "pytest>=7.0.0",
        "colorama>=0.4.6",
        "docker>=6.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0"
    ]
    
    for pachet in pachete:
        ruleaza_comanda(
            [sys.executable, "-m", "pip", "install", pachet, "--break-system-packages", "-q"],
            f"Instalare {pachet.split('>=')[0]}"
        )


def creeaza_directoare():
    """Creează directoarele necesare pentru laborator."""
    radacina_proiect = Path(__file__).parent.parent
    
    directoare = [
        radacina_proiect / "pcap",
        radacina_proiect / "artifacts",
        radacina_proiect / "docker" / "volumes" / "spool",
        radacina_proiect / "homework" / "exercises",
        radacina_proiect / "homework" / "solutions"
    ]
    
    for director in directoare:
        director.mkdir(parents=True, exist_ok=True)
        gitkeep = director / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
        print(f"  ✓ Director creat: {director.relative_to(radacina_proiect)}")


def genereaza_stub_grpc():
    """Generează fișierele stub gRPC din fișierul proto."""
    radacina_proiect = Path(__file__).parent.parent
    director_grpc = radacina_proiect / "src" / "apps" / "rpc" / "grpc"
    fisier_proto = director_grpc / "calculator.proto"
    
    if not fisier_proto.exists():
        print("  ⚠ Fișierul calculator.proto nu a fost găsit, se omite generarea stub-urilor")
        return
    
    try:
        from grpc_tools import protoc
        
        rezultat = protoc.main([
            'grpc_tools.protoc',
            f'-I{director_grpc}',
            f'--python_out={director_grpc}',
            f'--grpc_python_out={director_grpc}',
            str(fisier_proto)
        ])
        
        if rezultat == 0:
            print("  ✓ Fișierele stub gRPC generate cu succes")
        else:
            print("  ✗ Generarea stub-urilor gRPC a eșuat")
    except ImportError:
        print("  ⚠ grpc_tools nu este disponibil, stub-urile trebuie generate manual")


def verifica_docker():
    """Verifică și oferă instrucțiuni pentru Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            print("  ✓ Docker Desktop rulează")
            return True
    except Exception:
        pass
    
    print("  ⚠ Docker Desktop nu rulează sau nu este instalat")
    print()
    print("  Pentru a instala Docker Desktop:")
    print("  1. Descărcați de la: https://www.docker.com/products/docker-desktop/")
    print("  2. Rulați installer-ul și urmați instrucțiunile")
    print("  3. Activați integrarea WSL2 din Setări > Resources > WSL Integration")
    print("  4. Reporniți calculatorul dacă este necesar")
    return False


def main():
    afiseaza_antet("Instalare Cerințe - Laboratorul Săptămânii 12")
    print("\nAcest script va configura mediul pentru laboratorul de SMTP și RPC.")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
    
    # Pasul 1: Verificare Python
    afiseaza_pas(1, "Verificare versiune Python")
    versiune = sys.version_info
    if versiune >= (3, 11):
        print(f"  ✓ Python {versiune.major}.{versiune.minor}.{versiune.micro} detectat")
    else:
        print(f"  ✗ Python {versiune.major}.{versiune.minor} este prea vechi")
        print("  Vă rugăm să instalați Python 3.11 sau mai nou de pe python.org")
        return 1
    
    # Pasul 2: Instalare pachete Python
    afiseaza_pas(2, "Instalare pachete Python")
    instaleaza_pachete_python()
    
    # Pasul 3: Creare directoare
    afiseaza_pas(3, "Creare structură directoare")
    creeaza_directoare()
    
    # Pasul 4: Generare stub-uri gRPC
    afiseaza_pas(4, "Generare fișiere stub gRPC")
    genereaza_stub_grpc()
    
    # Pasul 5: Verificare Docker
    afiseaza_pas(5, "Verificare Docker Desktop")
    docker_ok = verifica_docker()
    
    # Sumar
    afiseaza_antet("Instalare Completă")
    
    if docker_ok:
        print("\n✓ Toate cerințele sunt instalate și configurate!")
        print("\nPași următori:")
        print("  1. Navigați în directorul proiectului")
        print("  2. Rulați: python scripts/porneste_lab.py")
        print("  3. Accesați Portainer la: https://localhost:9443")
    else:
        print("\n⚠ Cerințele Python sunt instalate, dar Docker necesită atenție.")
        print("\nDupă configurarea Docker Desktop:")
        print("  1. Rulați: python setup/verifica_mediu.py")
        print("  2. Apoi: python scripts/porneste_lab.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
