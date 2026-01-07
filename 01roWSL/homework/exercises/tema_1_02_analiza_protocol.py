#!/usr/bin/env python3
"""
Tema 1.2: Analiza Protocoalelor TCP/UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script ajută la generarea traficului TCP și UDP pentru captură și analiză.
"""

from __future__ import annotations

import subprocess
import sys
import socket
import threading
import time
import argparse
from pathlib import Path
from typing import Optional


def creeaza_trafic_tcp(port: int = 9090, mesaje: int = 5) -> None:
    """Creează trafic TCP pentru captură.
    
    Args:
        port: Portul pentru comunicare
        mesaje: Numărul de mesaje de trimis
    """
    print(f"\n[TCP] Pornire server pe portul {port}...")
    
    def server():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.settimeout(30)
                s.bind(("0.0.0.0", port))
                s.listen(1)
                print(f"[TCP Server] Ascult pe portul {port}")
                
                conn, addr = s.accept()
                print(f"[TCP Server] Conexiune de la {addr}")
                
                with conn:
                    for i in range(mesaje):
                        data = conn.recv(1024)
                        if not data:
                            break
                        print(f"[TCP Server] Primit: {data.decode()}")
                        conn.send(f"Confirmare {i+1}".encode())
        except socket.timeout:
            print("[TCP Server] Timeout - niciun client conectat")
        except Exception as e:
            print(f"[TCP Server] Eroare: {e}")
    
    def client():
        time.sleep(1)  # Așteaptă pornirea serverului
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect(("127.0.0.1", port))
                print("[TCP Client] Conectat la server")
                
                for i in range(mesaje):
                    mesaj = f"Mesaj TCP #{i+1}"
                    s.send(mesaj.encode())
                    print(f"[TCP Client] Trimis: {mesaj}")
                    raspuns = s.recv(1024)
                    print(f"[TCP Client] Răspuns: {raspuns.decode()}")
                    time.sleep(0.5)
        except Exception as e:
            print(f"[TCP Client] Eroare: {e}")
    
    # Pornește server și client în threaduri separate
    thread_server = threading.Thread(target=server)
    thread_client = threading.Thread(target=client)
    
    thread_server.start()
    thread_client.start()
    
    thread_client.join()
    thread_server.join(timeout=5)
    
    print("[TCP] Comunicare finalizată\n")


def creeaza_trafic_udp(port: int = 9091, mesaje: int = 5) -> None:
    """Creează trafic UDP pentru captură.
    
    Args:
        port: Portul pentru comunicare
        mesaje: Numărul de mesaje de trimis
    """
    print(f"\n[UDP] Pornire receptor pe portul {port}...")
    
    oprire = threading.Event()
    
    def receptor():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(1)
                s.bind(("0.0.0.0", port))
                print(f"[UDP Receptor] Ascult pe portul {port}")
                
                mesaje_primite = 0
                while not oprire.is_set() and mesaje_primite < mesaje:
                    try:
                        data, addr = s.recvfrom(1024)
                        print(f"[UDP Receptor] De la {addr}: {data.decode()}")
                        # Trimite răspuns
                        s.sendto(f"ACK {mesaje_primite+1}".encode(), addr)
                        mesaje_primite += 1
                    except socket.timeout:
                        continue
        except Exception as e:
            print(f"[UDP Receptor] Eroare: {e}")
    
    def emitator():
        time.sleep(0.5)  # Așteaptă pornirea receptorului
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(5)
                
                for i in range(mesaje):
                    mesaj = f"Datagram UDP #{i+1}"
                    s.sendto(mesaj.encode(), ("127.0.0.1", port))
                    print(f"[UDP Emițător] Trimis: {mesaj}")
                    
                    try:
                        raspuns, addr = s.recvfrom(1024)
                        print(f"[UDP Emițător] Răspuns: {raspuns.decode()}")
                    except socket.timeout:
                        print("[UDP Emițător] Fără răspuns (normal pentru UDP)")
                    
                    time.sleep(0.3)
                
                oprire.set()
        except Exception as e:
            print(f"[UDP Emițător] Eroare: {e}")
    
    thread_receptor = threading.Thread(target=receptor)
    thread_emitator = threading.Thread(target=emitator)
    
    thread_receptor.start()
    thread_emitator.start()
    
    thread_emitator.join()
    oprire.set()
    thread_receptor.join(timeout=3)
    
    print("[UDP] Comunicare finalizată\n")


def porneste_captura(interfata: str, port: int, fisier: Path, durata: int = 15) -> Optional[subprocess.Popen]:
    """Pornește captura de trafic în fundal.
    
    Args:
        interfata: Interfața de rețea
        port: Portul de filtrat
        fisier: Fișierul PCAP de ieșire
        durata: Durata maximă în secunde
        
    Returns:
        Procesul de captură sau None
    """
    try:
        cmd = [
            "tcpdump",
            "-i", interfata,
            "-w", str(fisier),
            f"port {port}",
            "-c", "100"  # Maximum 100 de pachete
        ]
        
        proces = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print(f"Captură pornită: {fisier}")
        return proces
        
    except FileNotFoundError:
        print("Eroare: tcpdump nu este instalat")
        print("Rulați manual în container: tcpdump -i lo -w <fisier.pcap> port <port>")
        return None
    except Exception as e:
        print(f"Eroare la pornirea capturii: {e}")
        return None


def opreste_captura(proces: subprocess.Popen) -> None:
    """Oprește procesul de captură.
    
    Args:
        proces: Procesul de oprit
    """
    if proces:
        proces.terminate()
        try:
            proces.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proces.kill()


def analizeaza_pcap(fisier: Path) -> None:
    """Analizează un fișier PCAP cu tshark.
    
    Args:
        fisier: Calea către fișierul PCAP
    """
    if not fisier.exists():
        print(f"Fișierul {fisier} nu există")
        return
    
    print(f"\n{'═' * 60}")
    print(f"ANALIZĂ: {fisier.name}")
    print('═' * 60)
    
    # Rezumat pachete
    print("\n--- Primele 10 pachete ---")
    subprocess.run(
        ["tshark", "-r", str(fisier), "-c", "10"],
        timeout=30
    )
    
    # Statistici protocol
    print("\n--- Ierarhie protocoale ---")
    subprocess.run(
        ["tshark", "-r", str(fisier), "-q", "-z", "io,phs"],
        timeout=30
    )
    
    # Flag-uri TCP (doar pentru TCP)
    if "tcp" in fisier.name.lower():
        print("\n--- Flag-uri TCP ---")
        subprocess.run(
            ["tshark", "-r", str(fisier), "-Y", "tcp", "-T", "fields",
             "-e", "frame.number", "-e", "tcp.flags.str", "-e", "tcp.seq", "-e", "tcp.ack"],
            timeout=30
        )


def genereaza_sablon_raport() -> str:
    """Generează șablonul pentru raportul de analiză."""
    return """# Raport Analiză Protocoale TCP/UDP

> Curs REȚELE DE CALCULATOARE - ASE, Informatică

## 1. Analiza Traficului TCP

### 1.1 Handshake-ul în Trei Pași

Identificați în captura `tcp_analiza.pcap`:

| Pas | Pachet # | Flag-uri | Seq | Ack |
|-----|----------|----------|-----|-----|
| SYN | | | | |
| SYN-ACK | | | | |
| ACK | | | | |

### 1.2 Overhead TCP

- Număr total pachete: ___
- Dimensiune totală date: ___ bytes
- Overhead antet TCP: ___ bytes per pachet

### TODO: Explicați de ce TCP are nevoie de handshake

[Răspunsul dvs. aici]

---

## 2. Analiza Traficului UDP

### 2.1 Caracteristici UDP

- Număr datagrame trimise: ___
- Număr datagrame primite: ___
- Dimensiune antet UDP: ___ bytes

### TODO: Ce observați diferit față de TCP?

[Răspunsul dvs. aici]

---

## 3. Comparație TCP vs UDP

| Aspect | TCP | UDP |
|--------|-----|-----|
| Pachete pentru 5 mesaje | | |
| Overhead total | | |
| Fiabilitate | | |
| Viteză relativă | | |

### TODO: Când ați folosi TCP și când UDP?

[Răspunsul dvs. aici]

---

## 4. Concluzii

[Scrieți 3-5 concluzii din această analiză]

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
"""


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Asistent pentru analiza protocoalelor TCP/UDP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Moduri de utilizare:
  python tema_1_02_analiza_protocol.py --mod tcp     # Generează trafic TCP
  python tema_1_02_analiza_protocol.py --mod udp     # Generează trafic UDP
  python tema_1_02_analiza_protocol.py --mod ambele  # TCP și UDP
  python tema_1_02_analiza_protocol.py --analiza tcp_analiza.pcap  # Analizează PCAP
  python tema_1_02_analiza_protocol.py --sablon      # Generează șablon raport
        """
    )
    parser.add_argument(
        "--mod",
        choices=["tcp", "udp", "ambele"],
        help="Modul de generare trafic"
    )
    parser.add_argument(
        "--port-tcp",
        type=int,
        default=9090,
        help="Portul pentru TCP (implicit: 9090)"
    )
    parser.add_argument(
        "--port-udp",
        type=int,
        default=9091,
        help="Portul pentru UDP (implicit: 9091)"
    )
    parser.add_argument(
        "--analiza",
        type=Path,
        help="Analizează un fișier PCAP"
    )
    parser.add_argument(
        "--sablon",
        action="store_true",
        help="Generează șablonul pentru raport"
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  TEMA 1.2: ANALIZA PROTOCOALE TCP/UDP".center(58) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE, Informatică".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    try:
        if args.sablon:
            cale_raport = Path("analiza_protocol.md")
            with open(cale_raport, "w", encoding="utf-8") as f:
                f.write(genereaza_sablon_raport())
            print(f"✓ Șablon raport generat: {cale_raport}")
            return 0
        
        if args.analiza:
            analizeaza_pcap(args.analiza)
            return 0
        
        if args.mod:
            print("ATENȚIE: Porniți captura ÎNAINTE de a rula acest script!")
            print()
            print("Într-un alt terminal, rulați:")
            if args.mod in ["tcp", "ambele"]:
                print(f"  tcpdump -i lo -w tcp_analiza.pcap port {args.port_tcp}")
            if args.mod in ["udp", "ambele"]:
                print(f"  tcpdump -i lo -w udp_analiza.pcap port {args.port_udp}")
            print()
            
            raspuns = input("Ați pornit captura? (d/n): ").strip().lower()
            if raspuns != "d":
                print("Porniți captura și rulați din nou scriptul.")
                return 0
            
            if args.mod in ["tcp", "ambele"]:
                creeaza_trafic_tcp(args.port_tcp)
            
            if args.mod in ["udp", "ambele"]:
                creeaza_trafic_udp(args.port_udp)
            
            print("\n" + "═" * 60)
            print("Trafic generat cu succes!")
            print("Opriți captura (Ctrl+C) și analizați fișierele PCAP.")
            print("═" * 60)
            return 0
        
        # Dacă nu s-a specificat nicio opțiune
        parser.print_help()
        return 0

    except KeyboardInterrupt:
        print("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        print(f"Eroare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
