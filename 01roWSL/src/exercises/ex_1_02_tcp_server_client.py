#!/usr/bin/env python3
"""
Exercițiul 1.02: Server și Client TCP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu demonstrează comunicarea client-server folosind socket-uri TCP.
Veți învăța despre modelul conexiune-orientat și handshake-ul în trei pași.

Concepte cheie:
- Socket-uri TCP (SOCK_STREAM)
- Handshake în trei pași (SYN, SYN-ACK, ACK)
- Stările socket-urilor (LISTEN, ESTABLISHED, TIME_WAIT)
- Modelul client-server

Rulare:
    python ex_1_02_tcp_server_client.py
    python ex_1_02_tcp_server_client.py --port 9999
"""

from __future__ import annotations

import socket
import sys
import threading
import time
import argparse
from typing import Optional


# Culori pentru terminal
VERDE = "\033[92m"
ALBASTRU = "\033[94m"
GALBEN = "\033[93m"
RESET = "\033[0m"


def afiseaza_stari_socket() -> None:
    """Explică stările unui socket TCP."""
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                    STĂRILE SOCKET-URILOR TCP                    │
├─────────────────────────────────────────────────────────────────┤
│  CLOSED      │ Socket închis, nu există conexiune              │
│  LISTEN      │ Server așteaptă conexiuni                       │
│  SYN_SENT    │ Client a trimis SYN, așteaptă SYN-ACK           │
│  SYN_RCVD    │ Server a primit SYN, a trimis SYN-ACK           │
│  ESTABLISHED │ Conexiune stabilită, transfer de date activ     │
│  FIN_WAIT_1  │ S-a trimis FIN, se așteaptă ACK                 │
│  FIN_WAIT_2  │ ACK primit, se așteaptă FIN de la celălalt      │
│  TIME_WAIT   │ Așteaptă ca pachetele să expire                 │
│  CLOSE_WAIT  │ FIN primit, aplicația încă procesează           │
│  LAST_ACK    │ FIN trimis, se așteaptă ultimul ACK             │
└─────────────────────────────────────────────────────────────────┘
""")


def server_tcp(port: int, mesaje_de_primit: int = 3) -> None:
    """Funcția serverului TCP.
    
    Args:
        port: Portul pe care să asculte
        mesaje_de_primit: Numărul de mesaje de primit înainte de închidere
    """
    print(f"\n{VERDE}[SERVER]{RESET} Se inițializează serverul TCP...")
    
    # Crearea socket-ului
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permite reutilizarea adresei
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Legare la adresă și port
        server_socket.bind(('0.0.0.0', port))
        print(f"{VERDE}[SERVER]{RESET} Socket legat la 0.0.0.0:{port}")
        
        # Începe ascultarea
        server_socket.listen(5)
        print(f"{VERDE}[SERVER]{RESET} Serverul ascultă (backlog=5)")
        print(f"{VERDE}[SERVER]{RESET} Stare: LISTEN")
        print(f"{VERDE}[SERVER]{RESET} Se așteaptă conexiuni...")
        
        # Acceptă conexiunea
        client_socket, adresa_client = server_socket.accept()
        print(f"\n{VERDE}[SERVER]{RESET} ═══════════════════════════════════════")
        print(f"{VERDE}[SERVER]{RESET} ✓ Conexiune acceptată de la {adresa_client}")
        print(f"{VERDE}[SERVER]{RESET} Stare: ESTABLISHED")
        print(f"{VERDE}[SERVER]{RESET} ═══════════════════════════════════════")
        
        mesaje_primite = 0
        while mesaje_primite < mesaje_de_primit:
            # Primește date
            date = client_socket.recv(1024)
            
            if not date:
                print(f"{VERDE}[SERVER]{RESET} Clientul a închis conexiunea")
                break
            
            mesaj = date.decode('utf-8')
            mesaje_primite += 1
            print(f"{VERDE}[SERVER]{RESET} Primit [{mesaje_primite}]: \"{mesaj}\"")
            
            # Trimite răspuns
            raspuns = f"Confirmare: am primit mesajul #{mesaje_primite}"
            client_socket.send(raspuns.encode('utf-8'))
            print(f"{VERDE}[SERVER]{RESET} Trimis răspuns: \"{raspuns}\"")
        
        # Închide conexiunea cu clientul
        client_socket.close()
        print(f"\n{VERDE}[SERVER]{RESET} Conexiune cu clientul închisă")
        print(f"{VERDE}[SERVER]{RESET} Stare client socket: CLOSE_WAIT → CLOSED")
        
    except Exception as e:
        print(f"{VERDE}[SERVER]{RESET} ✗ Eroare: {e}")
    finally:
        server_socket.close()
        print(f"{VERDE}[SERVER]{RESET} Server oprit")


def client_tcp(gazda: str, port: int, mesaje: list[str]) -> None:
    """Funcția clientului TCP.
    
    Args:
        gazda: Adresa serverului
        port: Portul serverului
        mesaje: Lista de mesaje de trimis
    """
    # Mică întârziere pentru a lăsa serverul să pornească
    time.sleep(0.5)
    
    print(f"\n{ALBASTRU}[CLIENT]{RESET} Se inițializează clientul TCP...")
    
    # Crearea socket-ului
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conectare la server
        print(f"{ALBASTRU}[CLIENT]{RESET} Se conectează la {gazda}:{port}...")
        print(f"{ALBASTRU}[CLIENT]{RESET} Stare: SYN_SENT (se trimite SYN)")
        
        client_socket.connect((gazda, port))
        
        print(f"\n{ALBASTRU}[CLIENT]{RESET} ═══════════════════════════════════════")
        print(f"{ALBASTRU}[CLIENT]{RESET} ✓ Conectat la server!")
        print(f"{ALBASTRU}[CLIENT]{RESET} Handshake TCP completat:")
        print(f"{ALBASTRU}[CLIENT]{RESET}   1. Client → Server: SYN")
        print(f"{ALBASTRU}[CLIENT]{RESET}   2. Server → Client: SYN-ACK")
        print(f"{ALBASTRU}[CLIENT]{RESET}   3. Client → Server: ACK")
        print(f"{ALBASTRU}[CLIENT]{RESET} Stare: ESTABLISHED")
        print(f"{ALBASTRU}[CLIENT]{RESET} ═══════════════════════════════════════")
        
        # Trimite mesajele
        for i, mesaj in enumerate(mesaje, 1):
            print(f"\n{ALBASTRU}[CLIENT]{RESET} Trimit mesajul #{i}: \"{mesaj}\"")
            client_socket.send(mesaj.encode('utf-8'))
            
            # Așteaptă răspuns
            raspuns = client_socket.recv(1024).decode('utf-8')
            print(f"{ALBASTRU}[CLIENT]{RESET} Răspuns primit: \"{raspuns}\"")
            
            time.sleep(0.3)  # Pauză scurtă între mesaje
        
        # Închide conexiunea
        print(f"\n{ALBASTRU}[CLIENT]{RESET} Se închide conexiunea...")
        print(f"{ALBASTRU}[CLIENT]{RESET} Stare: FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT")
        
    except ConnectionRefusedError:
        print(f"{ALBASTRU}[CLIENT]{RESET} ✗ Conexiune refuzată - serverul nu rulează")
    except Exception as e:
        print(f"{ALBASTRU}[CLIENT]{RESET} ✗ Eroare: {e}")
    finally:
        client_socket.close()
        print(f"{ALBASTRU}[CLIENT]{RESET} Socket client închis")


def demonstratie_completa(port: int) -> None:
    """Rulează o demonstrație completă server-client.
    
    Args:
        port: Portul pentru comunicare
    """
    print("\n" + "=" * 60)
    print("  DEMONSTRAȚIE: COMUNICARE TCP CLIENT-SERVER")
    print("=" * 60)
    
    # Mesajele pe care clientul le va trimite
    mesaje_client = [
        "Salut, server!",
        "Acesta este un test TCP.",
        "La revedere!"
    ]
    
    # Pornește serverul într-un fir de execuție separat
    fir_server = threading.Thread(
        target=server_tcp,
        args=(port, len(mesaje_client))
    )
    fir_server.daemon = True
    fir_server.start()
    
    # Pornește clientul
    client_tcp("127.0.0.1", port, mesaje_client)
    
    # Așteaptă finalizarea serverului
    fir_server.join(timeout=5)
    
    print("\n" + "=" * 60)
    print("  DEMONSTRAȚIE FINALIZATĂ")
    print("=" * 60)


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Demonstrație Server-Client TCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python ex_1_02_tcp_server_client.py              # Demonstrație completă
  python ex_1_02_tcp_server_client.py --port 8080  # Alt port
  python ex_1_02_tcp_server_client.py --stari      # Afișează stările socket
        """
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=9999,
        help="Portul pentru comunicare (implicit: 9999)"
    )
    parser.add_argument(
        "--stari",
        action="store_true",
        help="Afișează explicația stărilor socket TCP"
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  EXERCIȚIUL 1.02: SERVER ȘI CLIENT TCP".center(58) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    if args.stari:
        afiseaza_stari_socket()
        return 0

    try:
        demonstratie_completa(args.port)
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠ Întrerupt de utilizator")
        return 130
    except Exception as e:
        print(f"\n✗ Eroare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
