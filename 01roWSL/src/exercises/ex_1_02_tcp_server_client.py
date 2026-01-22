#!/usr/bin/env python3
"""
Exercițiul 1.02: Server și Client TCP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu demonstrează comunicarea TCP folosind socket-uri Python.
Rulează atât serverul cât și clientul pentru a arăta handshake-ul TCP.

Concepte cheie:
- Socket TCP (SOCK_STREAM) - conexiune orientată
- Handshake în 3 pași (SYN, SYN-ACK, ACK)
- Stări socket: LISTEN, ESTABLISHED, TIME_WAIT
- Comunicare bidirecțională
"""

from __future__ import annotations

import socket
import threading
import time
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

# Culori pentru output - diferențiem vizual SERVER de CLIENT
VERDE = "\033[92m"      # SERVER
ALBASTRU = "\033[94m"   # CLIENT
GALBEN = "\033[93m"     # INFO
CYAN = "\033[96m"       # STĂRI
ROSU = "\033[91m"       # ERORI
RESET = "\033[0m"
BOLD = "\033[1m"

# Configurare
HOST = '127.0.0.1'
PORT = 9095  # Port diferit de cel standard pentru a evita conflicte


# ═══════════════════════════════════════════════════════════════════════════════
# AFISARE_STARI_SOCKET
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_stari_socket() -> None:
    """Afișează un tabel explicativ cu stările socket-ului TCP.
    
    Ajută la înțelegerea ce se întâmplă în spatele scenei.
    """
    print()
    print(f"{CYAN}┌{'─' * 60}┐{RESET}")
    print(f"{CYAN}│{BOLD}  STĂRI SOCKET TCP - CE ÎNSEAMNĂ FIECARE                     {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}├{'─' * 60}┤{RESET}")
    print(f"{CYAN}│  LISTEN      │ Server: Așteaptă conexiuni pe port           │{RESET}")
    print(f"{CYAN}│  SYN_SENT    │ Client: A trimis SYN, așteaptă SYN-ACK       │{RESET}")
    print(f"{CYAN}│  SYN_RECV    │ Server: A primit SYN, a trimis SYN-ACK       │{RESET}")
    print(f"{CYAN}│  ESTABLISHED │ Conexiune activă - se pot trimite date       │{RESET}")
    print(f"{CYAN}│  FIN_WAIT_1  │ A trimis FIN, așteaptă ACK                   │{RESET}")
    print(f"{CYAN}│  TIME_WAIT   │ Așteaptă pachete întârziate (~60s)           │{RESET}")
    print(f"{CYAN}│  CLOSE_WAIT  │ A primit FIN, așteaptă close() local         │{RESET}")
    print(f"{CYAN}│  CLOSED      │ Conexiune închisă complet                    │{RESET}")
    print(f"{CYAN}└{'─' * 60}┘{RESET}")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def ruleaza_server() -> None:
    """Rulează serverul TCP.
    
    Pașii serverului:
    1. socket() - creează socket
    2. bind() - asociază cu adresă și port
    3. listen() - începe să asculte
    4. accept() - acceptă conexiune (blochează până vine client)
    5. recv()/send() - primește/trimite date
    6. close() - închide conexiunea
    """
    print(f"{VERDE}[SERVER]{RESET} Se creează socket-ul TCP...")
    
    # Creează socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR permite refolosirea portului imediat după închidere
    # Fără asta, ai primi "Address already in use" dacă rulezi din nou rapid
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    print(f"{VERDE}[SERVER]{RESET} Se face bind() pe {HOST}:{PORT}...")
    server_socket.bind((HOST, PORT))
    
    print(f"{VERDE}[SERVER]{RESET} Se apelează listen() - serverul așteaptă conexiuni")
    print(f"{VERDE}[SERVER]{RESET} {CYAN}>>> Stare: LISTEN <<<{RESET}")
    server_socket.listen(1)  # Coada de 1 conexiune
    
    print(f"{VERDE}[SERVER]{RESET} Se așteaptă conexiune... (accept() blochează)")
    
    # accept() blochează până vine un client
    client_conn, client_addr = server_socket.accept()
    
    print(f"{VERDE}[SERVER]{RESET} ✓ Conexiune acceptată de la {client_addr}")
    print(f"{VERDE}[SERVER]{RESET} {CYAN}>>> Stare: ESTABLISHED <<<{RESET}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TRANSFER_DATE_SERVER
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Primește date de la client
    print(f"{VERDE}[SERVER]{RESET} Se așteaptă date de la client...")
    data = client_conn.recv(1024)
    
    if data:
        mesaj_primit = data.decode('utf-8')
        print(f"{VERDE}[SERVER]{RESET} Primit: '{mesaj_primit}'")
        
        # Trimite răspuns
        raspuns = f"Server a primit: {mesaj_primit}"
        client_conn.send(raspuns.encode('utf-8'))
        print(f"{VERDE}[SERVER]{RESET} Trimis răspuns: '{raspuns}'")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INCHIDERE_CONEXIUNE_SERVER
    # ═══════════════════════════════════════════════════════════════════════════
    
    print(f"{VERDE}[SERVER]{RESET} Se închide conexiunea cu clientul...")
    client_conn.close()
    
    print(f"{VERDE}[SERVER]{RESET} Se închide socket-ul server...")
    server_socket.close()
    
    print(f"{VERDE}[SERVER]{RESET} ✓ Server oprit")


# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_CLIENT
# ═══════════════════════════════════════════════════════════════════════════════

def ruleaza_client() -> None:
    """Rulează clientul TCP.
    
    Pașii clientului:
    1. socket() - creează socket
    2. connect() - conectare la server (declanșează handshake)
    3. send()/recv() - trimite/primește date
    4. close() - închide conexiunea
    """
    # Așteaptă puțin să pornească serverul
    time.sleep(0.5)
    
    print(f"{ALBASTRU}[CLIENT]{RESET} Se creează socket-ul TCP...")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print(f"{ALBASTRU}[CLIENT]{RESET} Se conectează la {HOST}:{PORT}...")
    print(f"{ALBASTRU}[CLIENT]{RESET} {CYAN}>>> Trimite SYN (handshake pas 1) <<<{RESET}")
    
    try:
        client_socket.connect((HOST, PORT))
        print(f"{ALBASTRU}[CLIENT]{RESET} {CYAN}>>> Primit SYN-ACK, trimis ACK (handshake complet) <<<{RESET}")
        print(f"{ALBASTRU}[CLIENT]{RESET} {CYAN}>>> Stare: ESTABLISHED <<<{RESET}")
        print(f"{ALBASTRU}[CLIENT]{RESET} ✓ Conectat la server!")
        
        # ═══════════════════════════════════════════════════════════════════════
        # TRANSFER_DATE_CLIENT
        # ═══════════════════════════════════════════════════════════════════════
        
        # Trimite mesaj
        mesaj = "Salut de la client TCP!"
        print(f"{ALBASTRU}[CLIENT]{RESET} Se trimite: '{mesaj}'")
        client_socket.send(mesaj.encode('utf-8'))
        
        # Primește răspuns
        print(f"{ALBASTRU}[CLIENT]{RESET} Se așteaptă răspuns...")
        raspuns = client_socket.recv(1024)
        
        if raspuns:
            print(f"{ALBASTRU}[CLIENT]{RESET} Primit: '{raspuns.decode('utf-8')}'")
        
        # ═══════════════════════════════════════════════════════════════════════
        # INCHIDERE_CONEXIUNE_CLIENT
        # ═══════════════════════════════════════════════════════════════════════
        
        print(f"{ALBASTRU}[CLIENT]{RESET} Se închide conexiunea...")
        print(f"{ALBASTRU}[CLIENT]{RESET} {CYAN}>>> Trimite FIN (începe închiderea) <<<{RESET}")
        client_socket.close()
        print(f"{ALBASTRU}[CLIENT]{RESET} {CYAN}>>> Stare: TIME_WAIT (așteaptă ~60s) <<<{RESET}")
        print(f"{ALBASTRU}[CLIENT]{RESET} ✓ Client oprit")
        
    except ConnectionRefusedError:
        print(f"{ROSU}[CLIENT] EROARE: Conexiune refuzată - serverul nu rulează?{RESET}")
    except Exception as e:
        print(f"{ROSU}[CLIENT] EROARE: {e}{RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Funcția principală - rulează demonstrația server-client."""
    print()
    print(f"{BOLD}╔{'═' * 58}╗{RESET}")
    print(f"{BOLD}║  EXERCIȚIUL 1.02: SERVER ȘI CLIENT TCP                   ║{RESET}")
    print(f"{BOLD}╚{'═' * 58}╝{RESET}")
    
    # Afișează explicația stărilor
    afiseaza_stari_socket()
    
    print(f"{GALBEN}Se pornește demonstrația...{RESET}")
    print(f"{GALBEN}(Serverul și clientul rulează în paralel){RESET}")
    print()
    print("=" * 60)
    print()
    
    # Pornește serverul într-un thread separat
    thread_server = threading.Thread(target=ruleaza_server)
    thread_server.start()
    
    # Pornește clientul (așteaptă puțin ca serverul să fie gata)
    ruleaza_client()
    
    # Așteaptă terminarea serverului
    thread_server.join(timeout=5)
    
    print()
    print("=" * 60)
    print()
    
    # Explicație handshake
    print(f"{BOLD}HANDSHAKE TCP ÎN 3 PAȘI (ce s-a întâmplat):{RESET}")
    print()
    print(f"  Client                              Server")
    print(f"     │                                   │")
    print(f"     │  ─────── SYN (seq=x) ──────────►  │  Pas 1: Vreau să mă conectez")
    print(f"     │                                   │")
    print(f"     │  ◄──── SYN-ACK (ack=x+1) ───────  │  Pas 2: OK, și eu vreau")
    print(f"     │                                   │")
    print(f"     │  ─────── ACK (ack=y+1) ────────►  │  Pas 3: Confirmat!")
    print(f"     │                                   │")
    print(f"     │     CONEXIUNE STABILITĂ           │")
    print()
    
    print(f"{VERDE}✓ Exercițiu completat!{RESET}")
    print()
    print(f"{GALBEN}TIP: Rulează `ss -tn state time-wait` pentru a vedea socket-uri în TIME_WAIT{RESET}")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
