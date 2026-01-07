#!/usr/bin/env python3
"""
Script de Configurare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Generează certificatele TLS și configurația Docker pentru laborator.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def genereaza_certificate(director_certs: Path, suprascrie: bool = False):
    """
    Generează certificatele TLS pentru broker-ul MQTT.
    
    Args:
        director_certs: Calea către directorul de certificate
        suprascrie: Dacă să suprascrie certificatele existente
    """
    director_certs.mkdir(parents=True, exist_ok=True)
    
    ca_key = director_certs / "ca.key"
    ca_crt = director_certs / "ca.crt"
    server_key = director_certs / "server.key"
    server_crt = director_certs / "server.crt"
    
    # Verifică existența certificatelor
    if ca_crt.exists() and server_crt.exists() and not suprascrie:
        print("[INFO] Certificatele există deja. Folosiți --regen-certs pentru regenerare.")
        return True
    
    print("[INFO] Se generează certificatele TLS...")
    
    try:
        # Cheie privată CA
        subprocess.run([
            "openssl", "genrsa",
            "-out", str(ca_key), "2048"
        ], check=True, capture_output=True)
        print("[OK] Cheie CA generată")
        
        # Certificat CA auto-semnat
        subprocess.run([
            "openssl", "req", "-new", "-x509",
            "-days", "365",
            "-key", str(ca_key),
            "-out", str(ca_crt),
            "-subj", "/CN=MQTT-CA-Laborator/O=ASE Informatica/C=RO"
        ], check=True, capture_output=True)
        print("[OK] Certificat CA generat")
        
        # Cheie privată server
        subprocess.run([
            "openssl", "genrsa",
            "-out", str(server_key), "2048"
        ], check=True, capture_output=True)
        print("[OK] Cheie server generată")
        
        # CSR pentru server
        server_csr = director_certs / "server.csr"
        subprocess.run([
            "openssl", "req", "-new",
            "-key", str(server_key),
            "-out", str(server_csr),
            "-subj", "/CN=localhost/O=ASE Informatica/C=RO"
        ], check=True, capture_output=True)
        
        # Semnare certificat server
        subprocess.run([
            "openssl", "x509", "-req",
            "-days", "365",
            "-in", str(server_csr),
            "-CA", str(ca_crt),
            "-CAkey", str(ca_key),
            "-CAcreateserial",
            "-out", str(server_crt)
        ], check=True, capture_output=True)
        print("[OK] Certificat server semnat")
        
        # Curățare temporare
        server_csr.unlink(missing_ok=True)
        (director_certs / "ca.srl").unlink(missing_ok=True)
        
        print(f"[SUCCES] Certificate generate în: {director_certs}")
        return True
        
    except FileNotFoundError:
        print("[EROARE] OpenSSL nu este instalat sau nu este în PATH")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[EROARE] Eroare OpenSSL: {e}")
        return False


def creeaza_env(fisier_env: Path, config: dict):
    """
    Creează sau actualizează fișierul .env.
    
    Args:
        fisier_env: Calea către fișierul .env
        config: Dicționar cu configurația porturilor
    """
    continut = f"""# Configurare Laborator Săptămâna 13
# Curs REȚELE DE CALCULATOARE - ASE, Informatică
# Generat automat - modificați după necesități

# Porturi MQTT
MQTT_PLAIN_PORT={config.get('mqtt_plain', 1883)}
MQTT_TLS_PORT={config.get('mqtt_tls', 8883)}

# Port DVWA
DVWA_HOST_PORT={config.get('dvwa', 8080)}

# Porturi FTP
VSFTPD_HOST_PORT={config.get('ftp', 2121)}
VSFTPD_BACKDOOR_HOST_PORT={config.get('backdoor', 6200)}

# Rețea Docker
NETWORK_SUBNET=10.0.13.0/24
NETWORK_GATEWAY=10.0.13.1
"""
    
    fisier_env.write_text(continut, encoding='utf-8')
    print(f"[SUCCES] Fișier .env creat: {fisier_env}")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Configurare Docker pentru Laborator Săptămâna 13",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python configureaza_docker.py
  python configureaza_docker.py --regen-certs
  python configureaza_docker.py --mqtt-plain-port 11883 --dvwa-port 18080
        """
    )
    
    parser.add_argument("--regen-certs", action="store_true",
                        help="Regenerează certificatele TLS")
    parser.add_argument("--mqtt-plain-port", type=int, default=1883,
                        help="Port MQTT text clar (implicit: 1883)")
    parser.add_argument("--mqtt-tls-port", type=int, default=8883,
                        help="Port MQTT TLS (implicit: 8883)")
    parser.add_argument("--dvwa-port", type=int, default=8080,
                        help="Port DVWA (implicit: 8080)")
    parser.add_argument("--ftp-port", type=int, default=2121,
                        help="Port FTP (implicit: 2121)")
    parser.add_argument("--backdoor-port", type=int, default=6200,
                        help="Port backdoor simulat (implicit: 6200)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Configurare Docker - Laborator Săptămâna 13")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    print()
    
    radacina = Path(__file__).parent.parent
    
    # Generare certificate
    director_certs = radacina / "docker" / "configs" / "certs"
    genereaza_certificate(director_certs, args.regen_certs)
    
    # Creare .env
    config = {
        'mqtt_plain': args.mqtt_plain_port,
        'mqtt_tls': args.mqtt_tls_port,
        'dvwa': args.dvwa_port,
        'ftp': args.ftp_port,
        'backdoor': args.backdoor_port
    }
    creeaza_env(radacina / ".env", config)
    
    print("\n" + "=" * 60)
    print("Configurare completă!")
    print("\nPorturi configurate:")
    print(f"  MQTT (text clar): {args.mqtt_plain_port}")
    print(f"  MQTT (TLS):       {args.mqtt_tls_port}")
    print(f"  DVWA:             {args.dvwa_port}")
    print(f"  FTP:              {args.ftp_port}")
    print(f"  Backdoor:         {args.backdoor_port}")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
