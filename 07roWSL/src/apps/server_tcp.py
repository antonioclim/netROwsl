#!/usr/bin/env python3
"""
Server TCP Echo
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un server TCP simplu care returnează (echo) mesajele primite.
Folosit pentru demonstrarea conectivității TCP și a filtrării.

Comportament:
    1. Ascultă pe portul specificat (implicit: 9090)
    2. Acceptă conexiuni TCP de la clienți
    3. Pentru fiecare mesaj primit, îl trimite înapoi identic (echo)
    4. Închide conexiunea când clientul se deconectează

Exemplu de utilizare:
    python server_tcp.py --host 0.0.0.0 --port 9090
    
    # Test cu netcat:
    echo "Salut" | nc localhost 9090
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI — Module necesare pentru funcționalitatea serverului
# ═══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import socket
import sys
from datetime import datetime
from pathlib import Path

# Configurare cale pentru importul modulelor locale
RADACINA_PROIECT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

# Import logger unificat (cu fallback pentru rulare independentă)
try:
    from scripts.utils.logger import configureaza_logger
    logger = configureaza_logger("server_tcp")
except ImportError:
    # Fallback pentru rulare fără modulul logger
    import logging
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    logger = logging.getLogger("server_tcp")


# ═══════════════════════════════════════════════════════════════════════════════
# GESTIONARE_CLIENT — Procesarea unei conexiuni individuale
# ═══════════════════════════════════════════════════════════════════════════════

def gestioneaza_client(conn: socket.socket, adresa: tuple[str, int]):
    """
    Gestionează o conexiune de client în modul echo.
    
    Flux de procesare:
        1. Primește date de la client (max 4096 bytes per iterație)
        2. Decodează ca UTF-8 (cu fallback pentru caractere invalide)
        3. Trimite înapoi exact aceleași date (echo)
        4. Repetă până clientul închide conexiunea (recv returnează bytes gol)
    
    Comportament la erori:
        - ConnectionResetError: Clientul a închis brusc (RST) - normal pentru 
          clienți care nu fac graceful shutdown
        - Alte excepții: Logare și curățare
    
    NOTĂ PEDAGOGICĂ: Această funcție demonstrează pattern-ul clasic de 
    server TCP - bucla recv/send până la deconectare.
    
    Args:
        conn: Socket-ul conexiunii TCP stabilite (rezultat din accept())
        adresa: Tuplu (ip, port) al clientului
    """
    ip_client, port_client = adresa
    logger.info(f"Conexiune nouă de la {ip_client}:{port_client}")
    
    try:
        while True:
            # ───────────────────────────────────────────────────────────────────
            # PRIMIRE_DATE — recv() blochează până primește date sau conexiune închisă
            # ───────────────────────────────────────────────────────────────────
            # 4096 = dimensiune buffer standard, suficientă pentru majoritatea mesajelor
            date = conn.recv(4096)
            
            # Verificare deconectare - recv() returnează bytes gol când clientul închide
            if not date:
                logger.info(f"Client {ip_client}:{port_client} deconectat")
                break
            
            # Decodare cu toleranță la erori - 'replace' înlocuiește caracterele
            # invalide cu � în loc să arunce excepție
            mesaj = date.decode('utf-8', errors='replace')
            logger.info(f"Primit de la {ip_client}:{port_client}: {mesaj.strip()}")
            
            # ───────────────────────────────────────────────────────────────────
            # ECHO — Trimite înapoi exact datele primite
            # ───────────────────────────────────────────────────────────────────
            # sendall() garantează că TOT conținutul este trimis (spre deosebire de send())
            conn.sendall(date)
            logger.info(f"Trimis către {ip_client}:{port_client}: {mesaj.strip()}")
            
    except ConnectionResetError:
        # RST de la client - normal când clientul face Ctrl+C sau crash
        logger.warning(f"Conexiune resetată de {ip_client}:{port_client}")
    except Exception as e:
        # Alte erori neașteptate
        logger.error(f"Eroare cu {ip_client}:{port_client}: {e}")
    finally:
        # IMPORTANT: Întotdeauna închide socket-ul pentru a elibera resursele
        conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# PORNIRE_SERVER — Inițializare și bucla principală accept()
# ═══════════════════════════════════════════════════════════════════════════════

def porneste_server(host: str, port: int):
    """
    Pornește serverul TCP echo pe adresa și portul specificate.
    
    Secvența de inițializare:
        1. Creare socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
        2. Setare SO_REUSEADDR pentru rebind rapid după restart
        3. Bind pe adresa:port specificată
        4. Listen pentru a permite conexiuni în așteptare
        5. Bucla accept() pentru procesarea clienților
    
    NOTĂ: SO_REUSEADDR este ESENȚIAL pentru development - permite rebind 
    imediat după oprirea serverului, fără să așteptăm TIME_WAIT (~60s).
    
    Args:
        host: Adresa IP pe care să asculte ("0.0.0.0" = toate interfețele)
        port: Portul TCP (1-65535, >1024 nu necesită root)
    """
    # ───────────────────────────────────────────────────────────────────────────
    # CREARE_SOCKET — AF_INET = IPv4, SOCK_STREAM = TCP
    # ───────────────────────────────────────────────────────────────────────────
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR - permite rebind rapid după restart
    # Fără această opțiune, ar trebui să așteptăm ~60s (TIME_WAIT) după oprire
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # ───────────────────────────────────────────────────────────────────────
        # BIND_SI_LISTEN — Asociază socket-ul cu adresa și marchează-l ca server
        # ───────────────────────────────────────────────────────────────────────
        server_socket.bind((host, port))
        
        # listen(5) = maxim 5 conexiuni în coada de așteptare (pending)
        # Nu limitează conexiunile simultane, doar coada de conexiuni neacceptate încă
        server_socket.listen(5)
        
        logger.info(f"Server TCP Echo pornit pe {host}:{port}")
        logger.info("Așteptare conexiuni... (Ctrl+C pentru oprire)")
        
        # ───────────────────────────────────────────────────────────────────────
        # BUCLA_ACCEPT — Așteaptă și procesează conexiuni
        # ───────────────────────────────────────────────────────────────────────
        while True:
            try:
                # accept() blochează până vine o conexiune nouă
                # Returnează (socket_nou, (ip_client, port_client))
                conn, adresa = server_socket.accept()
                
                # NOTĂ: În producție, aici ar trebui threading sau asyncio
                # pentru a gestiona clienți multipli simultan
                gestioneaza_client(conn, adresa)
                
            except KeyboardInterrupt:
                logger.info("Server oprit de utilizator (Ctrl+C)")
                break
                
    except OSError as e:
        # Eroare la bind (port ocupat) sau alte erori de sistem
        logger.error(f"Eroare la pornirea serverului: {e}")
        sys.exit(1)
    finally:
        # Curățare - închide socket-ul serverului
        server_socket.close()
        logger.info("Socket server închis")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — Punct de intrare cu parsare argumente
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """
    Funcția principală - parsează argumentele și pornește serverul.
    
    Argumente linie de comandă:
        --host: Adresa pe care să asculte (implicit: 0.0.0.0 = toate)
        --port, -p: Portul TCP (implicit: 9090)
    """
    parser = argparse.ArgumentParser(
        description="Server TCP Echo pentru Laboratorul Săptămânii 7",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python server_tcp.py                    # Ascultă pe 0.0.0.0:9090
  python server_tcp.py --port 8080        # Ascultă pe 0.0.0.0:8080
  python server_tcp.py --host 127.0.0.1   # Doar localhost
        """
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Adresa pe care să asculte (implicit: 0.0.0.0 = toate interfețele)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=9090,
        help="Portul pe care să asculte (implicit: 9090)"
    )
    args = parser.parse_args()

    # Validare port
    if not 1 <= args.port <= 65535:
        logger.error(f"Port invalid: {args.port}. Trebuie să fie între 1 și 65535.")
        sys.exit(1)

    porneste_server(args.host, args.port)


if __name__ == "__main__":
    main()
