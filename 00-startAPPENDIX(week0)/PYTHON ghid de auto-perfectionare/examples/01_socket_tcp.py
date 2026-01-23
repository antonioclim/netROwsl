#!/usr/bin/env python3
"""
Exemplu 1: Server și Client TCP de bază
=======================================
Demonstrează conceptele fundamentale ale socket programming.

Curs: Rețele de Calculatoare - ASE București, CSIE
Autor: ing. dr. Antonio Clim
Versiune: 2.1 — cu subgoal labels și comentarii extinse

💡 ANALOGIE: Socket-ul ca Telefon Fix
-------------------------------------
| Operație Socket | Echivalent Telefon                    |
|-----------------|---------------------------------------|
| socket()        | Cumperi un telefon nou                |
| bind()          | Îți aloci un număr de telefon (port)  |
| listen()        | Pui telefonul în priză, aștepți apel  |
| accept()        | Ridici receptorul când sună           |
| connect()       | Formezi numărul cuiva                 |
| send()/recv()   | Vorbești / Asculți                    |
| close()         | Închizi telefonul                     |

Obiective de învățare:
- Înțelegerea modelului client-server
- Gestionarea corectă a erorilor de rețea
- Pattern-ul context manager pentru resurse
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import sys
import logging
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE_LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: Logging-ul e preferat față de print() pentru debugging în producție
# deoarece poți controla nivelul (DEBUG/INFO/WARNING) și formatul
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_HOST: str = '0.0.0.0'  # Ascultă pe toate interfețele
DEFAULT_PORT: int = 8080
BUFFER_SIZE: int = 1024  # Dimensiune buffer recv()
SOCKET_TIMEOUT: float = 30.0  # Timeout în secunde
MAX_CONNECTIONS: int = 5  # Backlog pentru listen()


# ═══════════════════════════════════════════════════════════════════════════════
# IMPLEMENTARE_SERVER
# ═══════════════════════════════════════════════════════════════════════════════
def server(port: int = DEFAULT_PORT) -> None:
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
        
    Note:
        - Gestionează un singur client la un moment dat (pentru simplitate)
        - Pentru multi-client, vezi exemplele cu threading
        
    See Also:
        - client(): Funcția client complementară
        - https://docs.python.org/3/library/socket.html
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # ───────────────────────────────────────────────────────────
            # CONFIGURARE_SOCKET_OPTIONS
            # ───────────────────────────────────────────────────────────
            # HACK: SO_REUSEADDR permite rebind rapid după restart.
            # Fără asta, trebuie să aștepți ~60s (TIME_WAIT) după oprire.
            # WARNING: În producție, evaluează implicațiile de securitate!
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # ───────────────────────────────────────────────────────────
            # BIND_SI_LISTEN
            # ───────────────────────────────────────────────────────────
            # NOTE: 0.0.0.0 = ascultă pe TOATE interfețele (localhost + LAN)
            # Pentru doar local, schimbă cu 127.0.0.1
            s.bind((DEFAULT_HOST, port))
            s.listen(MAX_CONNECTIONS)
            
            logger.info(f"Server pornit pe portul {port}")
            print(f"[SERVER] Ascult pe portul {port}...")
            print(f"[SERVER] Oprire cu Ctrl+C")
            
            # ───────────────────────────────────────────────────────────
            # BUCLA_ACCEPT_CONEXIUNI
            # ───────────────────────────────────────────────────────────
            # TODO: Adaugă suport pentru multiple conexiuni simultane (threading)
            while True:
                try:
                    conn, addr = s.accept()
                    logger.info(f"Conexiune nouă de la {addr}")
                    print(f"[SERVER] Conexiune de la {addr}")
                    
                    with conn:
                        # HACK: Setăm timeout pentru a evita blocaj indefinit
                        # dacă clientul nu trimite date
                        conn.settimeout(SOCKET_TIMEOUT)
                        
                        try:
                            # ───────────────────────────────────────────
                            # PRIMIRE_DATE
                            # ───────────────────────────────────────────
                            data: bytes = conn.recv(BUFFER_SIZE)
                            
                            if not data:
                                # NOTE: Date goale = client a închis conexiunea
                                logger.warning(f"Client {addr} a trimis date goale")
                                continue
                            
                            # ───────────────────────────────────────────
                            # PROCESARE_MESAJ
                            # ───────────────────────────────────────────
                            # NOTE: errors='replace' înlocuiește caractere
                            # invalide cu � în loc să arunce excepție
                            mesaj_decodat: str = data.decode('utf-8', errors='replace')
                            print(f"[SERVER] Primit: {mesaj_decodat}")
                            logger.info(f"Primit de la {addr}: {mesaj_decodat[:50]}...")
                            
                            # ───────────────────────────────────────────
                            # TRIMITERE_RASPUNS
                            # ───────────────────────────────────────────
                            # NOTE: sendall() garantează trimiterea completă,
                            # spre deosebire de send() care poate trimite parțial
                            response: bytes = b"OK: " + data.upper()
                            conn.sendall(response)
                            print(f"[SERVER] Trimis: {response.decode('utf-8', errors='replace')}")
                            
                        except socket.timeout:
                            logger.warning(f"Timeout la citire de la {addr}")
                            print(f"[SERVER] Timeout - clientul {addr} nu a trimis date")
                            
                        except UnicodeDecodeError as e:
                            # NOTE: Se întâmplă rar cu errors='replace',
                            # dar păstrăm pentru siguranță
                            logger.error(f"Eroare decodare de la {addr}: {e}")
                            print(f"[SERVER] Eroare decodare: {e}")
                            conn.sendall(b"ERROR: Invalid encoding")
                            
                except ConnectionResetError:
                    # NOTE: Client a închis brusc conexiunea (ex: Ctrl+C)
                    logger.warning(f"Client deconectat brusc")
                    print("[SERVER] Client deconectat brusc (connection reset)")
                    
                except ConnectionAbortedError:
                    logger.warning("Conexiune anulată")
                    print("[SERVER] Conexiune anulată")
                    
    except OSError as e:
        # ───────────────────────────────────────────────────────────────
        # GESTIONARE_ERORI_STARTUP
        # ───────────────────────────────────────────────────────────────
        logger.error(f"Nu pot porni serverul: {e}")
        print(f"[EROARE] Nu pot porni serverul: {e}")
        
        # NOTE: Oferim soluții concrete pentru cea mai comună eroare
        if "Address already in use" in str(e):
            print("  → Portul este deja ocupat!")
            print("  → Soluții:")
            print("    1. Așteaptă ~60 secunde și încearcă din nou")
            print("    2. Folosește alt port: python script.py server 8081")
            print("    3. Verifică ce folosește portul: ss -tlnp | grep 8080")
        sys.exit(1)
        
    except KeyboardInterrupt:
        # NOTE: Ctrl+C e modul normal de oprire
        logger.info("Server oprit de utilizator")
        print("\n[SERVER] Oprire la cererea utilizatorului (Ctrl+C)")


# ═══════════════════════════════════════════════════════════════════════════════
# IMPLEMENTARE_CLIENT
# ═══════════════════════════════════════════════════════════════════════════════
def client(host: str = '127.0.0.1', port: int = DEFAULT_PORT, 
           message: str = 'Test') -> Optional[str]:
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
        Nu ridică excepții — le gestionează intern și returnează None
        
    Example:
        >>> response = client('127.0.0.1', 8080, 'Hello')
        >>> print(response)
        'OK: HELLO'
        
    Note:
        Funcția nu ridică excepții pentru a simplifica integrarea.
        Verifică dacă rezultatul e None pentru a detecta erori.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # ───────────────────────────────────────────────────────────
            # CONFIGURARE_TIMEOUT
            # ───────────────────────────────────────────────────────────
            # NOTE: Timeout pentru connect() — evită blocaj dacă serverul
            # nu răspunde (firewall, adresă greșită, etc.)
            s.settimeout(10.0)
            
            # ───────────────────────────────────────────────────────────
            # CONECTARE_LA_SERVER
            # ───────────────────────────────────────────────────────────
            logger.info(f"Conectare la {host}:{port}")
            s.connect((host, port))
            
            print(f"[CLIENT] Conectat la {host}:{port}")
            print(f"[CLIENT] Trimit: {message}")
            
            # ───────────────────────────────────────────────────────────
            # TRIMITERE_MESAJ
            # ───────────────────────────────────────────────────────────
            # NOTE: encode() convertește str → bytes (necesar pentru socket)
            s.sendall(message.encode('utf-8'))
            
            # ───────────────────────────────────────────────────────────
            # PRIMIRE_RASPUNS
            # ───────────────────────────────────────────────────────────
            response: bytes = s.recv(BUFFER_SIZE)
            
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
        # NOTE: gaierror = "getaddrinfo error" = problemă DNS
        logger.error(f"Eroare DNS pentru {host}: {e}")
        print(f"[EROARE] Nu pot rezolva adresa '{host}': {e}")
        return None
        
    except OSError as e:
        logger.error(f"Eroare rețea: {e}")
        print(f"[EROARE] Problemă de rețea: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# INTERFATA_UTILIZATOR
# ═══════════════════════════════════════════════════════════════════════════════
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
║                                                                       ║
║  DEBUGGING:                                                           ║
║    - Verifică portul: ss -tlnp | grep 8080                            ║
║    - Activează debug: export LOG_LEVEL=DEBUG                          ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Punct de intrare principal — parsează argumentele și execută.
    
    Returns:
        Exit code: 0 pentru succes, 1 pentru eroare
    """
    if len(sys.argv) < 2:
        print_usage()
        return 0
        
    if sys.argv[1] == 'server':
        port: int = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
        server(port)
        return 0
        
    elif sys.argv[1] == 'client':
        # Format: client [host] [port] [mesaj]
        host: str = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
        port: int = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_PORT
        msg: str = ' '.join(sys.argv[4:]) if len(sys.argv) > 4 else 'Hello'
        result = client(host, port, msg)
        return 0 if result else 1
        
    elif sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        return 0
        
    else:
        # Tratează argumentele ca mesaj pentru client
        message: str = ' '.join(sys.argv[1:])
        result = client(message=message)
        return 0 if result else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Întrerupt de utilizator")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Eroare fatală: {e}")
        sys.exit(1)
