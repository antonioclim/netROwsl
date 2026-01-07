#!/usr/bin/env python3
"""
Captură Trafic de Rețea - Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Instrument pentru capturarea traficului de rețea în fișiere PCAP.
"""

import subprocess
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime

RADACINA_PROIECT = Path(__file__).parent.parent

class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'

def afiseaza_info(mesaj): print(f"{Culori.CYAN}[INFO]{Culori.FINAL} {mesaj}")
def afiseaza_succes(mesaj): print(f"{Culori.VERDE}[OK]{Culori.FINAL} {mesaj}")
def afiseaza_eroare(mesaj): print(f"{Culori.ROSU}[EROARE]{Culori.FINAL} {mesaj}")

def gaseste_tshark():
    """Caută instalarea tshark."""
    cai = [
        Path(r"C:\Program Files\Wireshark\tshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\tshark.exe"),
    ]
    
    for cale in cai:
        if cale.exists():
            return str(cale)
    
    import shutil
    if shutil.which('tshark'):
        return 'tshark'
    
    return None

def genereaza_nume_fisier(prefix="captura"):
    """Generează un nume de fișier unic bazat pe timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.pcap"

def captura_cu_tshark(interfata, durata, fisier_iesire, filtru=None):
    """Capturează trafic folosind tshark."""
    tshark = gaseste_tshark()
    if not tshark:
        afiseaza_eroare("tshark nu a fost găsit. Instalați Wireshark.")
        return False
    
    cmd = [tshark, "-a", f"duration:{durata}", "-w", str(fisier_iesire)]
    
    if interfata:
        cmd.extend(["-i", interfata])
    
    if filtru:
        cmd.extend(["-f", filtru])
    
    afiseaza_info(f"Se pornește captura pentru {durata} secunde...")
    afiseaza_info(f"Fișier de ieșire: {fisier_iesire}")
    
    if filtru:
        afiseaza_info(f"Filtru: {filtru}")
    
    try:
        result = subprocess.run(cmd, timeout=durata + 10)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        afiseaza_eroare("Captura a expirat")
        return False
    except Exception as e:
        afiseaza_eroare(f"Eroare la captură: {e}")
        return False

def captura_din_container(container, durata, fisier_iesire, filtru=None):
    """Capturează trafic din interiorul unui container Docker."""
    afiseaza_info(f"Se capturează din containerul {container}...")
    
    cmd = ["docker", "exec", container, "tcpdump", "-w", f"/app/{Path(fisier_iesire).name}"]
    
    if filtru:
        cmd.extend(["-i", "any", filtru])
    else:
        cmd.extend(["-i", "any"])
    
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(durata)
        proc.terminate()
        
        # Copiază fișierul din container
        subprocess.run([
            "docker", "cp", 
            f"{container}:/app/{Path(fisier_iesire).name}", 
            str(fisier_iesire)
        ])
        
        return True
    except Exception as e:
        afiseaza_eroare(f"Eroare: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Captură Trafic de Rețea - Săptămâna 14",
        epilog="Laborator Rețele de Calculatoare - ASE | by Revolvix"
    )
    
    parser.add_argument("--durata", "-d", type=int, default=30, help="Durata capturii în secunde (implicit: 30)")
    parser.add_argument("--iesire", "-o", type=str, help="Fișier de ieșire (implicit: auto-generat)")
    parser.add_argument("--interfata", "-i", type=str, help="Interfața de rețea")
    parser.add_argument("--filtru", "-f", type=str, help="Filtru BPF (ex: 'port 8080')")
    parser.add_argument("--container", "-c", type=str, help="Capturează din containerul specificat")
    parser.add_argument("--lab", "-l", action="store_true", help="Filtru predefinit pentru porturile laboratorului")
    
    args = parser.parse_args()
    
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Captură Trafic de Rețea - Săptămâna 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Laborator Rețele de Calculatoare - ASE{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    # Determină fișierul de ieșire
    if args.iesire:
        fisier_iesire = Path(args.iesire)
    else:
        director_pcap = RADACINA_PROIECT / "pcap"
        director_pcap.mkdir(exist_ok=True)
        fisier_iesire = director_pcap / genereaza_nume_fisier()
    
    # Determină filtrul
    filtru = args.filtru
    if args.lab:
        filtru = "port 8080 or port 8001 or port 8002 or port 9000"
        afiseaza_info("Se folosește filtrul pentru porturile laboratorului")
    
    # Execută captura
    if args.container:
        succes = captura_din_container(args.container, args.durata, fisier_iesire, filtru)
    else:
        succes = captura_cu_tshark(args.interfata, args.durata, fisier_iesire, filtru)
    
    if succes and fisier_iesire.exists():
        dimensiune = fisier_iesire.stat().st_size
        afiseaza_succes(f"Captură salvată: {fisier_iesire}")
        afiseaza_info(f"Dimensiune: {dimensiune:,} bytes")
        print(f"\n{Culori.BOLD}Comenzi utile:{Culori.FINAL}")
        print(f"  Vizualizare: wireshark {fisier_iesire}")
        print(f"  Analiză HTTP: tshark -r {fisier_iesire} -Y http")
        print(f"  Statistici: tshark -r {fisier_iesire} -q -z conv,tcp")
        return 0
    else:
        afiseaza_eroare("Captura a eșuat")
        return 1

if __name__ == "__main__":
    sys.exit(main())
