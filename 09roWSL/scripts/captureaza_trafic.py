#!/usr/bin/env python3
"""
Script Captură Trafic Săptămâna 9
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script facilitează capturarea traficului de rețea
pentru analiză cu Wireshark.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Adaugă directorul rădăcină la cale

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import (
    configureaza_logger,
    afiseaza_banner,
    afiseaza_succes,
    afiseaza_eroare,
    afiseaza_info,
    afiseaza_avertisment
)

logger = configureaza_logger("captureaza_trafic")

# Directorul pentru salvarea capturilor
DIRECTOR_CAPTURI = RADACINA_PROIECT / "pcap"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_instrumente() -> dict:
    """
    Verifică disponibilitatea instrumentelor de captură.
    
    Returnează:
        Dicționar cu starea fiecărui instrument
    """
    instrumente = {
        "tcpdump": shutil.which("tcpdump") is not None,
        "tshark": shutil.which("tshark") is not None,
        "wireshark": (
            shutil.which("wireshark") is not None or
            Path(r"C:\Program Files\Wireshark\Wireshark.exe").exists()
        ),
        "docker": shutil.which("docker") is not None
    }
    
    return instrumente


def captureaza_in_container(
    container: str,
    interfata: str,
    fisier_iesire: str,
    durata: int = 60,
    filtre: str = ""
) -> bool:
    """
    Pornește captura în interiorul unui container Docker.
    
    Argumente:
        container: Numele containerului
        interfata: Interfața de rețea
        fisier_iesire: Calea pentru fișierul de ieșire
        durata: Durata capturii în secunde
        filtre: Filtre tcpdump opționale
        
    Returnează:
        True dacă a reușit
    """
    logger.info(f"Se pornește captura în containerul {container}...")
    logger.info(f"Interfață: {interfata}")
    logger.info(f"Durată: {durata} secunde")
    
    # Construiește comanda tcpdump
    comanda_tcpdump = f"tcpdump -i {interfata} -w /tmp/captura.pcap"
    if filtre:
        comanda_tcpdump += f" {filtre}"
    
    try:
        # Rulează tcpdump în container
        proces = subprocess.Popen(
            ["docker", "exec", container, "bash", "-c", comanda_tcpdump],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        afiseaza_info(f"Captura a început. Se oprește în {durata} secunde...")
        afiseaza_info("Apăsați Ctrl+C pentru a opri mai devreme.")
        
        try:
            proces.wait(timeout=durata)
        except subprocess.TimeoutExpired:
            # Oprește tcpdump
            subprocess.run(
                ["docker", "exec", container, "pkill", "tcpdump"],
                capture_output=True
            )
            proces.wait()
        
        # Copiază fișierul din container
        subprocess.run(
            ["docker", "cp", f"{container}:/tmp/captura.pcap", fisier_iesire],
            check=True,
            capture_output=True
        )
        
        afiseaza_succes(f"Captură salvată în: {fisier_iesire}")
        return True
        
    except subprocess.CalledProcessError as e:
        afiseaza_eroare(f"Eroare la captură: {e}")
        return False
    except KeyboardInterrupt:
        # Oprește procesul la întrerupere
        subprocess.run(
            ["docker", "exec", container, "pkill", "tcpdump"],
            capture_output=True
        )
        afiseaza_avertisment("\nCaptură întreruptă de utilizator.")
        
        # Încearcă să copieze ce s-a capturat
        try:
            subprocess.run(
                ["docker", "cp", f"{container}:/tmp/captura.pcap", fisier_iesire],
                check=True,
                capture_output=True
            )
            afiseaza_info(f"Captură parțială salvată în: {fisier_iesire}")
        except Exception:
            pass
        
        return False


def afiseaza_instructiuni_wireshark():
    """Afișează instrucțiuni pentru captură cu Wireshark."""
    afiseaza_banner("Captură cu Wireshark", "Instrucțiuni")
    
    print("Pentru a captura traficul Docker cu Wireshark:\n")
    
    print("1. Deschideți Wireshark")
    print()
    
    print("2. Selectați interfața potrivită:")
    print(r"   • Windows: '\\.\pipe\docker_engine' sau 'vEthernet (WSL)'")
    print("   • Linux/macOS: 'docker0' sau 'br-*'")
    print()
    
    print("3. Aplicați filtrul de captură (opțional):")
    print("   • Pentru FTP: 'port 2121 or port 20'")
    print("   • Pentru porturi passive: 'portrange 60000-60010'")
    print()
    
    print("4. Filtre de afișare utile:")
    print("   • ftp              - Tot traficul FTP")
    print("   • ftp.request      - Doar comenzile")
    print("   • ftp.response     - Doar răspunsurile")
    print("   • ftp-data         - Transferuri de date")
    print()
    
    print("5. Salvați captura în directorul pcap/")
    print(f"   Cale: {DIRECTOR_CAPTURI}")


def afiseaza_instructiuni_tcpdump():
    """Afișează instrucțiuni pentru captură cu tcpdump."""
    afiseaza_banner("Captură cu tcpdump", "Instrucțiuni")
    
    print("Pentru a captura în containerul serverului FTP:\n")
    
    print("1. Intrați în container:")
    print("   docker exec -it s9_ftp-server /bin/bash")
    print()
    
    print("2. Porniți captura:")
    print("   tcpdump -i eth0 -w /tmp/captura.pcap port 21")
    print()
    
    print("3. Când ați terminat, ieșiți cu Ctrl+C")
    print()
    
    print("4. Copiați fișierul pe gazdă:")
    print("   docker cp s9_ftp-server:/tmp/captura.pcap ./pcap/")
    print()
    
    print("5. Deschideți cu Wireshark:")
    print("   wireshark ./pcap/captura.pcap")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Facilitează capturarea traficului de rețea pentru Săptămâna 9"
    )
    parser.add_argument(
        "--container",
        type=str,
        default="s9_ftp-server",
        help="Containerul în care să se execute captura"
    )
    parser.add_argument(
        "--interfata",
        type=str,
        default="eth0",
        help="Interfața de rețea pentru captură"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Fișierul de ieșire pentru captură"
    )
    parser.add_argument(
        "--durata",
        type=int,
        default=60,
        help="Durata capturii în secunde (implicit 60)"
    )
    parser.add_argument(
        "--filtre",
        type=str,
        default="port 21 or port 2121",
        help="Filtre tcpdump"
    )
    parser.add_argument(
        "--instructiuni",
        action="store_true",
        help="Afișează instrucțiuni pentru captură manuală"
    )
    parser.add_argument(
        "--verifica",
        action="store_true",
        help="Verifică disponibilitatea instrumentelor"
    )
    args = parser.parse_args()

    # Verificare instrumente
    if args.verifica:
        afiseaza_banner("Verificare Instrumente", "Disponibilitate")
        instrumente = verifica_instrumente()
        
        for nume, disponibil in instrumente.items():
            if disponibil:
                afiseaza_succes(f"{nume}: instalat")
            else:
                afiseaza_eroare(f"{nume}: nu este găsit")
        
        return 0

    # Afișare instrucțiuni
    if args.instructiuni:
        afiseaza_instructiuni_wireshark()
        print("\n" + "=" * 60 + "\n")
        afiseaza_instructiuni_tcpdump()
        return 0

    # Creează directorul de capturi dacă nu există
    DIRECTOR_CAPTURI.mkdir(exist_ok=True)

    # Generează numele fișierului de ieșire
    if args.output:
        fisier_iesire = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fisier_iesire = DIRECTOR_CAPTURI / f"saptamana9_{timestamp}.pcap"

    afiseaza_banner("Captură Trafic", "Săptămâna 9")

    # Verifică instrumentele
    instrumente = verifica_instrumente()
    
    if not instrumente["docker"]:
        afiseaza_eroare("Docker nu este instalat sau nu este în PATH.")
        return 1

    # Pornește captura
    succes = captureaza_in_container(
        container=args.container,
        interfata=args.interfata,
        fisier_iesire=str(fisier_iesire),
        durata=args.durata,
        filtre=args.filtre
    )

    if succes and instrumente["wireshark"]:
        print()
        afiseaza_info(f"Pentru a analiza: wireshark {fisier_iesire}")

    return 0 if succes else 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
