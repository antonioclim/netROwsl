#!/usr/bin/env python3
"""
Exercițiul 2.01: Server TCP Concurent
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest modul implementează un server TCP care poate opera în două moduri:
- Threaded (concurent): Gestionează mai mulți clienți simultan
- Iterativ (secvențial): Procesează clienții unul câte unul

Protocol:
- Clientul trimite un mesaj text
- Serverul răspunde cu textul convertit la majuscule, prefixat cu "OK: "
- Conexiunea rămâne deschisă pentru mesaje multiple
- Clientul trimite "exit" sau "quit" pentru a închide conexiunea

Utilizare:
    # Pornire server în modul threaded
    python ex_2_01_tcp.py server --mode threaded
    
    # Pornire server în modul iterativ
    python ex_2_01_tcp.py server --mode iterative
    
    # Conectare client
    python ex_2_01_tcp.py client --message "salut lume"
    
    # Test de încărcare cu mai mulți clienți
    python ex_2_01_tcp.py load --clients 10 --messages 5
"""

import socket
import threading
import argparse
import sys
import time
from dataclasses import dataclass
from typing import Tuple, Optional
from concurrent.futures import ThreadPoolExecutor


# ============================================================================
# Configurație
# ============================================================================

@dataclass
class ConfigurațieServer:
    """Configurația serverului TCP."""
    host: str = "0.0.0.0"
    port: int = 9090
    backlog: int = 5
    dimensiune_buffer: int = 1024
    timeout_client: float = 300.0  # 5 minute
    max_thread_uri: int = 10


CONFIG = ConfigurațieServer()


# ============================================================================
# Server TCP
# ============================================================================

class ServerTCP:
    """
    Server TCP cu suport pentru moduri concurent și iterativ.
    
    Protocolul de aplicație:
    - Primește text de la client
    - Returnează textul în majuscule cu prefix "OK: "
    - Comenzi speciale: "exit", "quit" pentru deconectare
    """
    
    def __init__(self, config: ConfigurațieServer = CONFIG, mod: str = "threaded"):
        """
        Inițializează serverul.
        
        Args:
            config: Configurația serverului
            mod: "threaded" pentru concurent, "iterative" pentru secvențial
        """
        self.config = config
        self.mod = mod
        self.socket_server: Optional[socket.socket] = None
        self.rulează = False
        self.nr_conexiuni = 0
        self.lock = threading.Lock()
    
    def _procesează_mesaj(self, mesaj: str) -> Tuple[str, bool]:
        """
        Procesează un mesaj de la client.
        
        Args:
            mesaj: Mesajul primit
            
        Returns:
            Tuple (răspuns, continuă) unde continuă=False înseamnă deconectare
        """
        mesaj = mesaj.strip()
        
        if mesaj.lower() in ("exit", "quit"):
            return "La revedere!\n", False
        
        if not mesaj:
            return "EROARE: Mesaj gol\n", True
        
        răspuns = f"OK: {mesaj.upper()}\n"
        return răspuns, True
    
    def _gestionează_client(self, socket_client: socket.socket, adresă: Tuple[str, int]) -> None:
        """
        Gestionează comunicarea cu un client individual.
        
        Args:
            socket_client: Socket-ul clientului
            adresă: Adresa clientului (ip, port)
        """
        with self.lock:
            self.nr_conexiuni += 1
            nr_curent = self.nr_conexiuni
        
        print(f"[{nr_curent}] Client conectat: {adresă[0]}:{adresă[1]}")
        
        try:
            socket_client.settimeout(self.config.timeout_client)
            
            while self.rulează:
                try:
                    date = socket_client.recv(self.config.dimensiune_buffer)
                    
                    if not date:
                        print(f"[{nr_curent}] Client deconectat: {adresă[0]}:{adresă[1]}")
                        break
                    
                    mesaj = date.decode('utf-8')
                    print(f"[{nr_curent}] Primit: {mesaj.strip()}")
                    
                    răspuns, continuă = self._procesează_mesaj(mesaj)
                    socket_client.sendall(răspuns.encode('utf-8'))
                    print(f"[{nr_curent}] Trimis: {răspuns.strip()}")
                    
                    if not continuă:
                        break
                        
                except socket.timeout:
                    print(f"[{nr_curent}] Timeout pentru {adresă[0]}:{adresă[1]}")
                    break
                except ConnectionResetError:
                    print(f"[{nr_curent}] Conexiune resetată de {adresă[0]}:{adresă[1]}")
                    break
                    
        except Exception as e:
            print(f"[{nr_curent}] Eroare: {e}")
        finally:
            socket_client.close()
            print(f"[{nr_curent}] Conexiune închisă: {adresă[0]}:{adresă[1]}")
    
    def pornește(self) -> None:
        """Pornește serverul și începe să asculte conexiuni."""
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket_server.bind((self.config.host, self.config.port))
            self.socket_server.listen(self.config.backlog)
            self.rulează = True
            
            print("=" * 60)
            print(f"Server TCP pornit pe {self.config.host}:{self.config.port}")
            print(f"Mod: {'CONCURENT (threaded)' if self.mod == 'threaded' else 'ITERATIV (secvențial)'}")
            print("Apăsați Ctrl+C pentru oprire")
            print("=" * 60)
            
            if self.mod == "threaded":
                self._buclă_concurentă()
            else:
                self._buclă_iterativă()
                
        except KeyboardInterrupt:
            print("\nOprire server...")
        finally:
            self.oprește()
    
    def _buclă_concurentă(self) -> None:
        """Buclă principală pentru modul threaded."""
        with ThreadPoolExecutor(max_workers=self.config.max_thread_uri) as executor:
            while self.rulează:
                try:
                    self.socket_server.settimeout(1.0)
                    socket_client, adresă = self.socket_server.accept()
                    executor.submit(self._gestionează_client, socket_client, adresă)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.rulează:
                        print(f"Eroare la acceptare conexiune: {e}")
    
    def _buclă_iterativă(self) -> None:
        """Buclă principală pentru modul iterativ (secvențial)."""
        while self.rulează:
            try:
                self.socket_server.settimeout(1.0)
                socket_client, adresă = self.socket_server.accept()
                # În modul iterativ, procesăm clientul complet înainte de a accepta altul
                self._gestionează_client(socket_client, adresă)
            except socket.timeout:
                continue
            except Exception as e:
                if self.rulează:
                    print(f"Eroare la acceptare conexiune: {e}")
    
    def oprește(self) -> None:
        """Oprește serverul."""
        self.rulează = False
        if self.socket_server:
            self.socket_server.close()
            print("Server oprit.")


# ============================================================================
# Client TCP
# ============================================================================

class ClientTCP:
    """Client TCP simplu pentru testare."""
    
    def __init__(self, host: str = "localhost", port: int = CONFIG.port):
        """
        Inițializează clientul.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
        """
        self.host = host
        self.port = port
    
    def trimite_mesaj(self, mesaj: str, timeout: float = 5.0) -> Optional[str]:
        """
        Trimite un mesaj și așteaptă răspuns.
        
        Args:
            mesaj: Mesajul de trimis
            timeout: Timeout în secunde
            
        Returns:
            Răspunsul serverului sau None la eroare
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((self.host, self.port))
                sock.sendall(mesaj.encode('utf-8'))
                răspuns = sock.recv(1024).decode('utf-8')
                return răspuns.strip()
        except Exception as e:
            print(f"Eroare: {e}")
            return None
    
    def sesiune_interactivă(self) -> None:
        """Pornește o sesiune interactivă cu serverul."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(30.0)
                sock.connect((self.host, self.port))
                print(f"Conectat la {self.host}:{self.port}")
                print("Introduceți mesaje (exit/quit pentru ieșire)")
                print("-" * 40)
                
                while True:
                    try:
                        mesaj = input("> ")
                        if not mesaj:
                            continue
                        
                        sock.sendall(mesaj.encode('utf-8'))
                        răspuns = sock.recv(1024).decode('utf-8')
                        print(f"< {răspuns.strip()}")
                        
                        if mesaj.lower() in ("exit", "quit"):
                            break
                            
                    except EOFError:
                        break
                        
        except ConnectionRefusedError:
            print(f"Nu s-a putut conecta la {self.host}:{self.port}")
            print("Asigurați-vă că serverul rulează.")
        except Exception as e:
            print(f"Eroare: {e}")


# ============================================================================
# Test de Încărcare
# ============================================================================

def test_încărcare(
    host: str,
    port: int,
    nr_clienți: int,
    nr_mesaje: int
) -> None:
    """
    Rulează un test de încărcare cu mai mulți clienți simultan.
    
    Args:
        host: Adresa serverului
        port: Portul serverului
        nr_clienți: Numărul de clienți simultani
        nr_mesaje: Numărul de mesaje per client
    """
    print("=" * 60)
    print(f"Test de Încărcare: {nr_clienți} clienți × {nr_mesaje} mesaje")
    print("=" * 60)
    
    rezultate = {"reușite": 0, "eșuate": 0, "durate": []}
    lock = threading.Lock()
    
    def client_worker(id_client: int) -> None:
        """Worker pentru un client individual."""
        client = ClientTCP(host, port)
        
        for i in range(nr_mesaje):
            mesaj = f"Client{id_client}_Mesaj{i}"
            start = time.perf_counter()
            răspuns = client.trimite_mesaj(mesaj)
            durată = (time.perf_counter() - start) * 1000
            
            with lock:
                if răspuns:
                    rezultate["reușite"] += 1
                    rezultate["durate"].append(durată)
                else:
                    rezultate["eșuate"] += 1
    
    # Pornire clienți simultani
    start_total = time.perf_counter()
    thread_uri = []
    
    for i in range(nr_clienți):
        t = threading.Thread(target=client_worker, args=(i,))
        thread_uri.append(t)
        t.start()
    
    # Așteptare finalizare
    for t in thread_uri:
        t.join()
    
    durată_totală = time.perf_counter() - start_total
    
    # Statistici
    print()
    print("Rezultate:")
    print(f"  Total cereri: {nr_clienți * nr_mesaje}")
    print(f"  Reușite: {rezultate['reușite']}")
    print(f"  Eșuate: {rezultate['eșuate']}")
    print(f"  Durată totală: {durată_totală:.2f}s")
    
    if rezultate["durate"]:
        durate = rezultate["durate"]
        print(f"  Latență medie: {sum(durate)/len(durate):.2f}ms")
        print(f"  Latență min: {min(durate):.2f}ms")
        print(f"  Latență max: {max(durate):.2f}ms")
        print(f"  Throughput: {len(durate)/durată_totală:.1f} req/s")
    
    print("=" * 60)


# ============================================================================
# Punct de Intrare
# ============================================================================

def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Server și Client TCP - Exercițiul 2.01",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Pornire server concurent
  python ex_2_01_tcp.py server --mode threaded
  
  # Pornire server iterativ
  python ex_2_01_tcp.py server --mode iterative
  
  # Trimitere mesaj
  python ex_2_01_tcp.py client --message "salut"
  
  # Sesiune interactivă
  python ex_2_01_tcp.py client --interactive
  
  # Test de încărcare
  python ex_2_01_tcp.py load --clients 10 --messages 100
        """
    )
    
    subparsers = parser.add_subparsers(dest="comandă", help="Comandă de executat")
    
    # Subcomandă: server
    parser_server = subparsers.add_parser("server", help="Pornește serverul TCP")
    parser_server.add_argument(
        "--mode", "-m",
        choices=["threaded", "iterative"],
        default="threaded",
        help="Modul de operare (implicit: threaded)"
    )
    parser_server.add_argument(
        "--port", "-p",
        type=int,
        default=CONFIG.port,
        help=f"Port de ascultare (implicit: {CONFIG.port})"
    )
    
    # Subcomandă: client
    parser_client = subparsers.add_parser("client", help="Rulează clientul TCP")
    parser_client.add_argument(
        "--host", "-H",
        default="localhost",
        help="Adresa serverului (implicit: localhost)"
    )
    parser_client.add_argument(
        "--port", "-p",
        type=int,
        default=CONFIG.port,
        help=f"Portul serverului (implicit: {CONFIG.port})"
    )
    parser_client.add_argument(
        "--message", "-m",
        help="Mesaj de trimis"
    )
    parser_client.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Mod interactiv"
    )
    
    # Subcomandă: load (test încărcare)
    parser_load = subparsers.add_parser("load", help="Rulează test de încărcare")
    parser_load.add_argument(
        "--host", "-H",
        default="localhost",
        help="Adresa serverului"
    )
    parser_load.add_argument(
        "--port", "-p",
        type=int,
        default=CONFIG.port,
        help="Portul serverului"
    )
    parser_load.add_argument(
        "--clients", "-c",
        type=int,
        default=5,
        help="Număr de clienți simultani (implicit: 5)"
    )
    parser_load.add_argument(
        "--messages", "-n",
        type=int,
        default=10,
        help="Mesaje per client (implicit: 10)"
    )
    
    args = parser.parse_args()
    
    if args.comandă == "server":
        config = ConfigurațieServer(port=args.port)
        server = ServerTCP(config, mod=args.mode)
        server.pornește()
        return 0
        
    elif args.comandă == "client":
        client = ClientTCP(args.host, args.port)
        
        if args.interactive:
            client.sesiune_interactivă()
        elif args.message:
            răspuns = client.trimite_mesaj(args.message)
            if răspuns:
                print(f"Răspuns: {răspuns}")
                return 0
            return 1
        else:
            parser_client.print_help()
            return 1
        return 0
        
    elif args.comandă == "load":
        test_încărcare(args.host, args.port, args.clients, args.messages)
        return 0
        
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
