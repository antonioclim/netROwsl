#!/usr/bin/env python3
"""
Script de Instalare a Cerințelor Preliminare
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Instalează și configurează toate dependențele necesare pentru laborator.
"""

import subprocess
import sys
import os
from pathlib import Path


def afiseaza_banner():
    """Afișează bannerul de start."""
    print("=" * 60)
    print("Instalare Cerințe pentru Laboratorul Săptămânii 10")
    print("Laborator Rețele de Calculatoare - ASE, Informatică Economică")
    print("=" * 60)
    print()


def ruleaza_comanda(comanda: list, descriere: str) -> bool:
    """Rulează o comandă și afișează rezultatul."""
    print(f"  → {descriere}...")
    try:
        rezultat = subprocess.run(
            comanda,
            capture_output=True,
            text=True,
            timeout=300
        )
        if rezultat.returncode == 0:
            print(f"    ✓ {descriere} - succes")
            return True
        else:
            print(f"    ✗ {descriere} - eșuat")
            if rezultat.stderr:
                print(f"      Eroare: {rezultat.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"    ✗ {descriere} - timeout")
        return False
    except Exception as e:
        print(f"    ✗ {descriere} - eroare: {e}")
        return False


def instaleaza_pachete_python():
    """Instalează pachetele Python necesare."""
    print("\n[1/5] Instalare pachete Python...")
    
    pachete = [
        "docker",
        "requests",
        "pyyaml",
        "flask",
        "paramiko",
        "dnslib",
        "pyftpdlib",
        "colorama",
    ]
    
    succes = True
    for pachet in pachete:
        if not ruleaza_comanda(
            [sys.executable, "-m", "pip", "install", "--quiet", pachet],
            f"Instalare {pachet}"
        ):
            succes = False
    
    return succes


def verifica_docker():
    """Verifică instalarea Docker."""
    print("\n[2/5] Verificare Docker...")
    
    # Verificare docker
    rezultat = subprocess.run(
        ["docker", "--version"],
        capture_output=True,
        text=True
    )
    if rezultat.returncode == 0:
        print(f"    ✓ Docker instalat: {rezultat.stdout.strip()}")
    else:
        print("    ✗ Docker nu este instalat")
        print("      Descărcați Docker Desktop de pe: https://www.docker.com/products/docker-desktop/")
        return False
    
    # Verificare docker compose
    rezultat = subprocess.run(
        ["docker", "compose", "version"],
        capture_output=True,
        text=True
    )
    if rezultat.returncode == 0:
        print(f"    ✓ Docker Compose disponibil: {rezultat.stdout.strip()}")
    else:
        print("    ✗ Docker Compose nu este disponibil")
        return False
    
    # Verificare daemon activ
    rezultat = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        text=True
    )
    if rezultat.returncode == 0:
        print("    ✓ Daemon Docker activ")
    else:
        print("    ✗ Daemon Docker nu rulează")
        print("      Porniți aplicația Docker Desktop")
        return False
    
    return True


def creeaza_directoare():
    """Creează directoarele necesare pentru artefacte."""
    print("\n[3/5] Creare directoare...")
    
    radacina = Path(__file__).parent.parent
    directoare = [
        radacina / "artifacts",
        radacina / "pcap",
        radacina / "docker" / "volumes",
    ]
    
    for director in directoare:
        director.mkdir(parents=True, exist_ok=True)
        gitkeep = director / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
        print(f"    ✓ {director.relative_to(radacina)}")
    
    return True


def genereaza_certificate_tls():
    """Generează certificate TLS auto-semnate pentru exerciții."""
    print("\n[4/5] Generare certificate TLS...")
    
    radacina = Path(__file__).parent.parent
    dir_cert = radacina / "artifacts" / "certs"
    dir_cert.mkdir(parents=True, exist_ok=True)
    
    fisier_cheie = dir_cert / "server.key"
    fisier_cert = dir_cert / "server.crt"
    
    if fisier_cheie.exists() and fisier_cert.exists():
        print("    ✓ Certificatele există deja")
        return True
    
    # Generare cu OpenSSL dacă este disponibil
    try:
        rezultat = subprocess.run(
            [
                "openssl", "req", "-x509", "-newkey", "rsa:2048",
                "-keyout", str(fisier_cheie),
                "-out", str(fisier_cert),
                "-days", "365",
                "-nodes",
                "-subj", "/C=RO/ST=Bucharest/L=Bucharest/O=ASE/OU=Informatica/CN=localhost"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        if rezultat.returncode == 0:
            print(f"    ✓ Certificate generate în {dir_cert.relative_to(radacina)}")
            return True
        else:
            print("    ⚠ OpenSSL nu a reușit generarea, se va face din Python")
    except FileNotFoundError:
        print("    ⚠ OpenSSL nu este disponibil, certificatele vor fi generate la rulare")
    
    return True


def construieste_imagini_docker():
    """Construiește imaginile Docker necesare."""
    print("\n[5/5] Construire imagini Docker...")
    
    radacina = Path(__file__).parent.parent
    dir_docker = radacina / "docker"
    
    if not (dir_docker / "docker-compose.yml").exists():
        print("    ⚠ docker-compose.yml nu există încă")
        return True
    
    os.chdir(dir_docker)
    
    rezultat = subprocess.run(
        ["docker", "compose", "build"],
        capture_output=True,
        text=True,
        timeout=600
    )
    
    if rezultat.returncode == 0:
        print("    ✓ Imagini Docker construite cu succes")
        return True
    else:
        print("    ⚠ Construirea imaginilor a eșuat (se va reîncerca la pornire)")
        if rezultat.stderr:
            print(f"      Detalii: {rezultat.stderr[:300]}")
        return True  # Nu blocăm instalarea


def afiseaza_sumar(succes: bool):
    """Afișează sumarul instalării."""
    print("\n" + "=" * 60)
    if succes:
        print("✓ Instalare completă!")
        print()
        print("Pași următori:")
        print("  1. Rulați: python scripts/porneste_lab.py")
        print("  2. Accesați Portainer: https://localhost:9443")
        print("  3. Consultați README.md pentru exerciții")
    else:
        print("✗ Instalarea a întâmpinat erori")
        print()
        print("Vă rugăm să:")
        print("  1. Verificați mesajele de eroare de mai sus")
        print("  2. Instalați manual componentele lipsă")
        print("  3. Rulați din nou acest script")
    print("=" * 60)


def main():
    """Funcția principală de instalare."""
    afiseaza_banner()
    
    rezultate = []
    
    rezultate.append(instaleaza_pachete_python())
    rezultate.append(verifica_docker())
    rezultate.append(creeaza_directoare())
    rezultate.append(genereaza_certificate_tls())
    rezultate.append(construieste_imagini_docker())
    
    succes_total = all(rezultate)
    afiseaza_sumar(succes_total)
    
    return 0 if succes_total else 1


if __name__ == "__main__":
    sys.exit(main())
