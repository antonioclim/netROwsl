#!/usr/bin/env python3
"""
Script de Instalare Cerințe Preliminare
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Ghidează utilizatorul prin procesul de instalare a tuturor dependențelor necesare.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def afiseaza_banner():
    """Afișează banner-ul de început."""
    print("=" * 70)
    print("   Asistent Instalare - Laborator Săptămâna 13")
    print("   IoT și Securitate în Rețelele de Calculatoare")
    print("   Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 70)
    print()


def verifica_sistem_operare():
    """Verifică sistemul de operare și returnează informații."""
    sistem = platform.system()
    versiune = platform.version()
    print(f"[INFO] Sistem de operare detectat: {sistem}")
    print(f"[INFO] Versiune: {versiune}")
    
    if sistem != "Windows":
        print("[ATENȚIE] Acest kit este optimizat pentru Windows 10/11 cu WSL2.")
        print("          Unele funcționalități pot să nu fie disponibile.")
    
    return sistem


def instaleaza_pachete_python():
    """Instalează pachetele Python necesare."""
    print("\n" + "-" * 50)
    print("Instalare Pachete Python")
    print("-" * 50)
    
    pachete = [
        "docker>=6.0.0",
        "requests>=2.28.0",
        "pyyaml>=6.0",
        "paho-mqtt>=1.6.0",
        "scapy>=2.5.0"
    ]
    
    print("\nPachete care vor fi instalate:")
    for pachet in pachete:
        print(f"  • {pachet}")
    
    raspuns = input("\nDoriți să continuați? [D/n]: ").strip().lower()
    if raspuns in ['n', 'nu', 'no']:
        print("[INFO] Instalare anulată de utilizator.")
        return False
    
    print("\n[INFO] Se instalează pachetele Python...")
    
    for pachet in pachete:
        print(f"\n[INSTALARE] {pachet}...")
        try:
            rezultat = subprocess.run(
                [sys.executable, "-m", "pip", "install", pachet, "--break-system-packages"],
                capture_output=True,
                text=True
            )
            if rezultat.returncode == 0:
                print(f"[SUCCES] {pachet} instalat cu succes")
            else:
                # Încearcă fără --break-system-packages
                rezultat = subprocess.run(
                    [sys.executable, "-m", "pip", "install", pachet],
                    capture_output=True,
                    text=True
                )
                if rezultat.returncode == 0:
                    print(f"[SUCCES] {pachet} instalat cu succes")
                else:
                    print(f"[EROARE] Nu s-a putut instala {pachet}")
                    print(f"         {rezultat.stderr}")
        except Exception as e:
            print(f"[EROARE] Excepție la instalarea {pachet}: {e}")
    
    return True


def verifica_docker_desktop():
    """Verifică și ghidează instalarea Docker Desktop."""
    print("\n" + "-" * 50)
    print("Verificare Docker Desktop")
    print("-" * 50)
    
    try:
        rezultat = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True
        )
        if rezultat.returncode == 0:
            print(f"[SUCCES] Docker găsit: {rezultat.stdout.strip()}")
            
            # Verifică dacă daemon-ul rulează
            rezultat_info = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            if rezultat_info.returncode == 0:
                print("[SUCCES] Docker daemon rulează")
                return True
            else:
                print("[ATENȚIE] Docker este instalat dar daemon-ul nu rulează")
                print("          Porniți Docker Desktop și încercați din nou")
                return False
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"[EROARE] {e}")
    
    print("[INFO] Docker Desktop nu a fost găsit.")
    print("\n        Pentru a instala Docker Desktop:")
    print("        1. Accesați https://www.docker.com/products/docker-desktop/")
    print("        2. Descărcați versiunea pentru Windows")
    print("        3. Rulați instalatorul și urmați instrucțiunile")
    print("        4. Asigurați-vă că selectați 'Use WSL 2 instead of Hyper-V'")
    print("        5. Reporniți calculatorul dacă este necesar")
    
    return False


def verifica_wsl2():
    """Verifică configurarea WSL2."""
    print("\n" + "-" * 50)
    print("Verificare WSL2")
    print("-" * 50)
    
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = rezultat.stdout + rezultat.stderr
        
        if "WSL 2" in output or "Default Version: 2" in output:
            print("[SUCCES] WSL2 este configurat corect")
            return True
        else:
            print("[ATENȚIE] WSL2 nu pare să fie versiunea implicită")
    except FileNotFoundError:
        print("[INFO] Comanda WSL nu a fost găsită")
    except Exception as e:
        print(f"[EROARE] {e}")
    
    print("\n        Pentru a configura WSL2:")
    print("        1. Deschideți PowerShell ca Administrator")
    print("        2. Rulați: wsl --install")
    print("        3. Rulați: wsl --set-default-version 2")
    print("        4. Reporniți calculatorul")
    
    return False


def verifica_wireshark():
    """Verifică instalarea Wireshark."""
    print("\n" + "-" * 50)
    print("Verificare Wireshark")
    print("-" * 50)
    
    cai_posibile = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for cale in cai_posibile:
        if cale.exists():
            print(f"[SUCCES] Wireshark găsit: {cale}")
            return True
    
    print("[INFO] Wireshark nu a fost găsit în locațiile standard.")
    print("\n        Pentru a instala Wireshark:")
    print("        1. Accesați https://www.wireshark.org/download.html")
    print("        2. Descărcați 'Windows x64 Installer'")
    print("        3. Rulați instalatorul")
    print("        4. La 'Install Npcap', selectați instalarea componentei")
    
    return False


def genereaza_certificate_tls():
    """Generează certificatele TLS pentru broker-ul MQTT."""
    print("\n" + "-" * 50)
    print("Generare Certificate TLS")
    print("-" * 50)
    
    radacina = Path(__file__).parent.parent
    director_certs = radacina / "docker" / "configs" / "certs"
    director_certs.mkdir(parents=True, exist_ok=True)
    
    ca_key = director_certs / "ca.key"
    ca_crt = director_certs / "ca.crt"
    server_key = director_certs / "server.key"
    server_crt = director_certs / "server.crt"
    
    # Verifică dacă certificatele există deja
    if ca_crt.exists() and server_crt.exists():
        print("[INFO] Certificatele TLS există deja.")
        raspuns = input("Doriți să le regenerați? [d/N]: ").strip().lower()
        if raspuns not in ['d', 'da', 'y', 'yes']:
            print("[INFO] Se păstrează certificatele existente.")
            return True
    
    print("\n[INFO] Se generează certificatele TLS...")
    
    try:
        # Generare cheie privată CA
        print("[GENERARE] Cheie privată CA...")
        subprocess.run([
            "openssl", "genrsa",
            "-out", str(ca_key),
            "2048"
        ], check=True, capture_output=True)
        
        # Generare certificat CA
        print("[GENERARE] Certificat CA...")
        subprocess.run([
            "openssl", "req", "-new", "-x509",
            "-days", "365",
            "-key", str(ca_key),
            "-out", str(ca_crt),
            "-subj", "/CN=MQTT-CA-ASE/O=ASE Informatica/C=RO"
        ], check=True, capture_output=True)
        
        # Generare cheie privată server
        print("[GENERARE] Cheie privată server...")
        subprocess.run([
            "openssl", "genrsa",
            "-out", str(server_key),
            "2048"
        ], check=True, capture_output=True)
        
        # Generare CSR server
        print("[GENERARE] Cerere de semnare certificat (CSR)...")
        server_csr = director_certs / "server.csr"
        subprocess.run([
            "openssl", "req", "-new",
            "-key", str(server_key),
            "-out", str(server_csr),
            "-subj", "/CN=localhost/O=ASE Informatica/C=RO"
        ], check=True, capture_output=True)
        
        # Semnare certificat server cu CA
        print("[GENERARE] Certificat server semnat...")
        subprocess.run([
            "openssl", "x509", "-req",
            "-days", "365",
            "-in", str(server_csr),
            "-CA", str(ca_crt),
            "-CAkey", str(ca_key),
            "-CAcreateserial",
            "-out", str(server_crt)
        ], check=True, capture_output=True)
        
        # Curățare fișiere temporare
        server_csr.unlink(missing_ok=True)
        (director_certs / "ca.srl").unlink(missing_ok=True)
        
        print("[SUCCES] Certificate TLS generate cu succes!")
        print(f"         Locație: {director_certs}")
        return True
        
    except FileNotFoundError:
        print("[EROARE] OpenSSL nu a fost găsit.")
        print("         Instalați OpenSSL sau Git for Windows (include OpenSSL)")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[EROARE] Eroare la generarea certificatelor: {e}")
        return False


def creeaza_fisier_env():
    """Creează fișierul .env cu configurația porturilor."""
    print("\n" + "-" * 50)
    print("Creare Fișier Configurare (.env)")
    print("-" * 50)
    
    radacina = Path(__file__).parent.parent
    fisier_env = radacina / ".env"
    
    if fisier_env.exists():
        print("[INFO] Fișierul .env există deja.")
        return True
    
    continut = """# Configurare porturi laborator Săptămâna 13
# Curs REȚELE DE CALCULATOARE - ASE, Informatică

# Porturi MQTT Mosquitto
MQTT_PLAIN_PORT=1883
MQTT_TLS_PORT=8883

# Port DVWA (aplicație web vulnerabilă)
DVWA_HOST_PORT=8080

# Porturi vsftpd
VSFTPD_HOST_PORT=2121
VSFTPD_BACKDOOR_HOST_PORT=6200

# Configurare rețea Docker
NETWORK_SUBNET=10.0.13.0/24
NETWORK_GATEWAY=10.0.13.1
"""
    
    fisier_env.write_text(continut, encoding='utf-8')
    print(f"[SUCCES] Fișier .env creat: {fisier_env}")
    return True


def afiseaza_sumar():
    """Afișează sumarul și pașii următori."""
    print("\n" + "=" * 70)
    print("   INSTALARE FINALIZATĂ")
    print("=" * 70)
    print("""
Pași următori:

1. Verificați mediul:
   python setup/verifica_mediu.py

2. Porniți laboratorul:
   python scripts/porneste_lab.py

3. Rulați testul de fum:
   python tests/test_fum.py

4. Începeți exercițiile din README.md

În caz de probleme, consultați:
- docs/depanare.md
- README.md secțiunea Depanare
""")
    print("=" * 70)


def main():
    """Funcția principală."""
    afiseaza_banner()
    
    sistem = verifica_sistem_operare()
    
    print("\nAcest script vă va ghida prin instalarea următoarelor componente:")
    print("  1. Pachete Python necesare")
    print("  2. Verificare Docker Desktop")
    print("  3. Verificare WSL2")
    print("  4. Verificare Wireshark")
    print("  5. Generare certificate TLS")
    print("  6. Creare fișier configurare (.env)")
    
    raspuns = input("\nDoriți să continuați? [D/n]: ").strip().lower()
    if raspuns in ['n', 'nu', 'no']:
        print("[INFO] Instalare anulată de utilizator.")
        return 0
    
    # Rulează toate verificările și instalările
    instaleaza_pachete_python()
    verifica_docker_desktop()
    verifica_wsl2()
    verifica_wireshark()
    genereaza_certificate_tls()
    creeaza_fisier_env()
    
    afiseaza_sumar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
