#!/usr/bin/env python3
"""
Exemplu 1: Server și Client TCP de bază
=======================================
Demonstrează conceptele fundamentale ale socket programming.

Curs: Rețele de Calculatoare - ASE București, CSIE
Autor: ing. dr. Antonio Clim

Obiective de învățare:
- Înțelegerea modelului client-server
- Folosirea socket-urilor TCP în Python
- Gestionarea corectă a erorilor de rețea
"""
import socket
import sys
import logging
from typing import Optional

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def server(port: int = 8080) -> None:
    """Pornește un server TCP simplu care face echo la mesaje.
    
    Serverul ascultă pe toate interfețele (0.0.0.0) și răspunde
    cu versiunea uppercase a mesajului primit.
    
    Args:
        port: Portul pe care ascultă serverul (implicit 8080)
        
    Returns:
        None. Rulează indefinit până la Ctrl+C.
        
    Raises:
        OSError: Dacă portul este deja ocupat sau indisponibil
        
    Example:
        >>> server(8080)
        [SERVER] Ascult pe portul 8080...
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # HACK: SO_REUSEADDR permite rebind rapid după restart
            # Fără asta, trebuie să aștepți ~60s după oprire
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', port))
            s.listen(5)
            logger.info(f"Server pornit pe portul {port}")
            print(f"[SERVER] Ascult pe portul {port}...")
            print(f"[SERVER] Oprire cu Ctrl+C")
            
            while True:
                try:
                    conn, addr = s.accept()
                    logger.info(f"Conexiune nouă de la {addr}")
                    print(f"[SERVER] Conexiune de la {addr}")
                    
                    with conn:
                        # Setăm timeout pentru a evita blocaj indefinit
                        conn.settimeout(30.0)
                        
                        try:
                            data: bytes = conn.recv(1024)
                            
                            if not data:
                                logger.warning(f"Client {addr} a trimis date goale")
                                continue
                                
                            # Decodare cu fallback pentru caractere invalide
                            mesaj_decodat: str = data.decode('utf-8', errors='replace')
                            print(f"[SERVER] Primit: {mesaj_decodat}")
                            logger.info(f"Primit de la {addr}: {mesaj_decodat[:50]}...")
                            
                            response: bytes = b"OK: " + data.upper()
                            conn.sendall(response)
                            print(f"[SERVER] Trimis: {response.decode('utf-8', errors='replace')}")
                            
                        except socket.timeout:
                            logger.warning(f"Timeout la citire de la {addr}")
                            print(f"[SERVER] Timeout - clientul {addr} nu a trimis date")
                            
                        except UnicodeDecodeError as e:
                            logger.error(f"Eroare decodare de la {addr}: {e}")
                            print(f"[SERVER] Eroare decodare: {e}")
                            conn.sendall(b"ERROR: Invalid encoding")
                            
                except ConnectionResetError:
                    logger.warning(f"Client deconectat brusc")
                    print("[SERVER] Client deconectat brusc (connection reset)")
                    
                except ConnectionAbortedError:
                    logger.warning("Conexiune anulată")
                    print("[SERVER] Conexiune anulată")
                    
    except OSError as e:
        logger.error(f"Nu pot porni serverul: {e}")
        print(f"[EROARE] Nu pot porni serverul: {e}")
        
        if "Address already in use" in str(e):
            print("  → Portul este deja ocupat!")
            print("  → Soluții:")
            print("    1. Așteaptă ~60 secunde și încearcă din nou")
            print("    2. Folosește alt port: python script.py server 8081")
            print("    3. Verifică ce folosește portul: ss -tlnp | grep 8080")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Server oprit de utilizator")
        print("\n[SERVER] Oprire la cererea utilizatorului (Ctrl+C)")


def client(host: str = '127.0.0.1', port: int = 8080, message: str = 'Test') -> Optional[str]:
    """Trimite un mesaj la server și returnează răspunsul.
    
    Creează o conexiune TCP, trimite mesajul, așteaptă răspuns,
    apoi închide conexiunea.
    
    Args:
        host: Adresa IP sau hostname-ul serverului
        port: Portul serverului (implicit 8080)
        message: Mesajul de trimis (implicit 'Test')
        
    Returns:
        Răspunsul serverului ca string, sau None dacă a eșuat
        
    Raises:
        Nu ridică excepții - le gestionează intern și returnează None
        
    Example:
        >>> response = client('127.0.0.1', 8080, 'Hello')
        >>> print(response)
        'OK: HELLO'
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Timeout pentru conectare
            s.settimeout(10.0)
            
            logger.info(f"Conectare la {host}:{port}")
            s.connect((host, port))
            
            print(f"[CLIENT] Conectat la {host}:{port}")
            print(f"[CLIENT] Trimit: {message}")
            
            # Trimitere mesaj
            s.sendall(message.encode('utf-8'))
            
            # Așteptare răspuns
            response: bytes = s.recv(1024)
            
            if not response:
                logger.warning("Server a închis conexiunea fără răspuns")
                print("[CLIENT] Server nu a trimis răspuns")
                return None
                
            response_str: str = response.decode('utf-8', errors='replace')
            print(f"[CLIENT] Răspuns: {response_str}")
            logger.info(f"Răspuns primit: {response_str[:50]}...")
            
            return response_str
            
    except socket.timeout:
        logger.error(f"Timeout la conectare către {host}:{port}")
        print(f"[EROARE] Timeout - serverul nu răspunde în 10 secunde")
        print("  → Verifică dacă serverul rulează")
        return None
        
    except ConnectionRefusedError:
        logger.error(f"Conexiune refuzată de {host}:{port}")
        print(f"[EROARE] Conexiune refuzată de {host}:{port}")
        print("  → Serverul nu rulează sau portul e greșit")
        print("  → Pornește serverul: python 01_socket_tcp.py server")
        return None
        
    except socket.gaierror as e:
        logger.error(f"Eroare DNS pentru {host}: {e}")
        print(f"[EROARE] Nu pot rezolva adresa '{host}': {e}")
        return None
        
    except OSError as e:
        logger.error(f"Eroare rețea: {e}")
        print(f"[EROARE] Problemă de rețea: {e}")
        return None


def print_usage() -> None:
    """Afișează instrucțiunile de utilizare."""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║  01_socket_tcp.py - Exemplu Server/Client TCP                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║  UTILIZARE:                                                           ║
║    Server:  python 01_socket_tcp.py server [port]                     ║
║    Client:  python 01_socket_tcp.py [mesaj]                           ║
║    Client:  python 01_socket_tcp.py client [host] [port] [mesaj]      ║
║                                                                       ║
║  EXEMPLE:                                                             ║
║    python 01_socket_tcp.py server              # Server pe 8080       ║
║    python 01_socket_tcp.py server 9000         # Server pe 9000       ║
║    python 01_socket_tcp.py "Salut lume"        # Client către 8080    ║
║    python 01_socket_tcp.py client 192.168.1.5 8080 "Test"             ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)
        
    if sys.argv[1] == 'server':
        port: int = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
        server(port)
        
    elif sys.argv[1] == 'client':
        # Format: client [host] [port] [mesaj]
        host: str = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
        port: int = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        msg: str = ' '.join(sys.argv[4:]) if len(sys.argv) > 4 else 'Hello'
        client(host, port, msg)
        
    elif sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        
    else:
        # Tratează argumentele ca mesaj pentru client
        message: str = ' '.join(sys.argv[1:])
        client(message=message)
