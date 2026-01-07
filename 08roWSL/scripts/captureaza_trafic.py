#!/usr/bin/env python3
"""
Asistent Captură Trafic
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Ajută la capturarea traficului de rețea pentru analiză.

Utilizare:
    python scripts/captureaza_trafic.py --interfata eth0 --iesire pcap/captura.pcap
    python scripts/captureaza_trafic.py --lista-interfete
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

# Coduri culori
VERDE = "\033[92m"
ROSU = "\033[91m"
GALBEN = "\033[93m"
ALBASTRU = "\033[94m"
CYAN = "\033[96m"
RESETARE = "\033[0m"
BOLD = "\033[1m"

RADACINA_PROIECT = Path(__file__).parent.parent


def afiseaza_titlu(titlu: str):
    """Afișează un titlu formatat."""
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{titlu}{RESETARE}")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print()


def listeaza_interfete():
    """Listează interfețele de rețea disponibile."""
    afiseaza_titlu("Interfețe de Rețea Disponibile")
    
    # Încearcă ip link (Linux)
    try:
        result = subprocess.run(
            ["ip", "link", "show"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(result.stdout)
            return
    except FileNotFoundError:
        pass
    
    # Încearcă ipconfig (Windows)
    try:
        result = subprocess.run(
            ["ipconfig", "/all"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(result.stdout)
            return
    except FileNotFoundError:
        pass
    
    print(f"{GALBEN}Nu s-au putut lista interfețele.{RESETARE}")
    print("Încercați manual: ip link show (Linux) sau ipconfig (Windows)")


def verifica_tcpdump() -> bool:
    """Verifică dacă tcpdump este disponibil."""
    try:
        result = subprocess.run(
            ["tcpdump", "--version"],
            capture_output=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def captureaza_trafic(interfata: str, fisier_iesire: Path, durata: int, filtru: str = ""):
    """Capturează trafic folosind tcpdump."""
    afiseaza_titlu(f"Captură Trafic - {interfata}")
    
    if not verifica_tcpdump():
        print(f"{ROSU}tcpdump nu este instalat!{RESETARE}")
        print()
        print("Alternative:")
        print("  1. Instalați tcpdump: apt install tcpdump")
        print("  2. Folosiți Wireshark direct")
        print("  3. Capturați din container Docker")
        return False
    
    # Creează directorul dacă nu există
    fisier_iesire.parent.mkdir(parents=True, exist_ok=True)
    
    # Construiește comanda tcpdump
    cmd = [
        "tcpdump",
        "-i", interfata,
        "-w", str(fisier_iesire),
        "-c", "1000"  # Maxim 1000 pachete
    ]
    
    if filtru:
        cmd.extend(filtru.split())
    
    print(f"Interfață: {interfata}")
    print(f"Fișier ieșire: {fisier_iesire}")
    print(f"Durată maximă: {durata} secunde")
    if filtru:
        print(f"Filtru: {filtru}")
    print()
    print(f"{GALBEN}Captură în curs... Apăsați Ctrl+C pentru oprire{RESETARE}")
    print("-" * 50)
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        start = time.time()
        while time.time() - start < durata:
            if process.poll() is not None:
                break
            time.sleep(1)
            pachete = "..." # Ar necesita parsing complex
            print(f"  Timp: {int(time.time() - start)}s", end="\r")
        
        process.terminate()
        process.wait(timeout=5)
        
    except KeyboardInterrupt:
        print()
        print(f"{GALBEN}Captură oprită de utilizator{RESETARE}")
        process.terminate()
    
    print()
    if fisier_iesire.exists():
        dimensiune = fisier_iesire.stat().st_size
        print(f"{VERDE}Captură salvată: {fisier_iesire}{RESETARE}")
        print(f"Dimensiune: {dimensiune / 1024:.1f} KB")
        print()
        print("Pentru analiză, deschideți fișierul în Wireshark:")
        print(f"  wireshark {fisier_iesire}")
        return True
    else:
        print(f"{ROSU}Nu s-a creat fișierul de captură.{RESETARE}")
        return False


def afiseaza_instructiuni_wireshark():
    """Afișează instrucțiuni pentru Wireshark."""
    afiseaza_titlu("Instrucțiuni Captură cu Wireshark")
    
    print("""
{BOLD}Capturare trafic localhost:{RESETARE}

1. Deschideți Wireshark
2. Selectați interfața "Loopback: lo" sau "Adapter for loopback"
3. Aplicați filtrul de captură: port 8080
4. Porniți captura (butonul albastru)
5. Efectuați cereri HTTP în alt terminal
6. Opriți captura și analizați

{BOLD}Filtre utile pentru afișare:{RESETARE}

  http                    - Doar trafic HTTP
  tcp.port == 8080        - Doar portul 8080
  tcp.flags.syn == 1      - Pachete SYN (începutul conexiunii)
  http.request            - Doar cereri HTTP
  http.response           - Doar răspunsuri HTTP
  ip.addr == 172.28.8.21  - Trafic către/de la un backend

{BOLD}Generare trafic pentru captură:{RESETARE}

  curl http://localhost:8080/
  curl -i http://localhost:8080/nginx-health
  for i in {{1..10}}; do curl -s http://localhost:8080/ >/dev/null; done

{BOLD}Analiză handshake TCP:{RESETARE}

  1. Filtru: tcp.flags.syn == 1
  2. Identificați pachetul SYN (client → server)
  3. Click dreapta → Follow → TCP Stream
  4. Observați secvența: SYN → SYN-ACK → ACK

""".format(BOLD=BOLD, RESETARE=RESETARE))


def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Asistent Captură Trafic - Laborator Săptămâna 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python captureaza_trafic.py --lista-interfete
  python captureaza_trafic.py -i lo -o pcap/test.pcap
  python captureaza_trafic.py --wireshark
        """
    )
    parser.add_argument(
        "--interfata", "-i",
        help="Interfața de rețea pentru captură"
    )
    parser.add_argument(
        "--iesire", "-o",
        type=Path,
        default=RADACINA_PROIECT / "pcap" / "captura.pcap",
        help="Fișierul de ieșire pentru captură"
    )
    parser.add_argument(
        "--durata", "-d",
        type=int,
        default=60,
        help="Durata maximă a capturii în secunde (implicit: 60)"
    )
    parser.add_argument(
        "--filtru", "-f",
        default="port 8080",
        help="Filtru tcpdump (implicit: port 8080)"
    )
    parser.add_argument(
        "--lista-interfete", "-l",
        action="store_true",
        help="Listează interfețele de rețea disponibile"
    )
    parser.add_argument(
        "--wireshark", "-w",
        action="store_true",
        help="Afișează instrucțiuni pentru Wireshark"
    )
    
    args = parser.parse_args()
    
    if args.lista_interfete:
        listeaza_interfete()
        return 0
    
    if args.wireshark:
        afiseaza_instructiuni_wireshark()
        return 0
    
    if not args.interfata:
        print(f"{GALBEN}Specificați o interfață cu --interfata{RESETARE}")
        print()
        print("Pentru a vedea interfețele disponibile:")
        print("  python captureaza_trafic.py --lista-interfete")
        print()
        print("Pentru instrucțiuni Wireshark:")
        print("  python captureaza_trafic.py --wireshark")
        return 1
    
    succes = captureaza_trafic(
        args.interfata,
        args.iesire,
        args.durata,
        args.filtru
    )
    
    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
