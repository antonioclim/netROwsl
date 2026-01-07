#!/usr/bin/env python3
"""
Exercițiul 2.02: Server UDP cu Protocol Personalizat
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest modul implementează un server UDP cu un protocol de aplicație personalizat
care suportă mai multe comenzi.

Protocol de Aplicație:
    Comenzi disponibile:
    - ping          : Verificare disponibilitate (răspuns: PONG)
    - upper:text    : Convertește textul la majuscule
    - lower:text    : Convertește textul la minuscule
    - reverse:text  : Inversează textul
    - echo:text     : Returnează textul neschimbat
    - time          : Returnează ora curentă a serverului
    - help          : Afișează comenzile disponibile

Caracteristici UDP demonstate:
    - Fără conexiune (connectionless)
    - Fără garanție de livrare
    - Fără ordine garantată
    - Overhead minim (header 8 bytes vs 20+ TCP)

Utilizare:
    # Pornire server
    python ex_2_02_udp.py server
    
    # Client - comandă singulară
    python ex_2_02_udp.py client --command "upper:salut"
    
    # Client - mod interactiv
    python ex_2_02_udp.py client --interactive
"""

import socket
import argparse
import sys
from datetime import datetime
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Callable


# ============================================================================
# Configurație
# ============================================================================

@dataclass
class ConfigurațieServer:
    """Configurația serverului UDP."""
    host: str = "0.0.0.0"
    port: int = 9091
    dimensiune_buffer: int = 1024


CONFIG = ConfigurațieServer()


# ============================================================================
# Protocol de Aplicație
# ============================================================================

class ProtocolUDP:
    """
    Implementare protocol de aplicație peste UDP.
    
    Formatul mesajelor:
        Cerere:  COMANDĂ sau COMANDĂ:ARGUMENT
        Răspuns: REZULTAT sau EROARE:MESAJ
    """
    
    def __init__(self):
        """Inițializează handlerii de comenzi."""
        self.comenzi: Dict[str, Callable[[str], str]] = {
            "ping": self._cmd_ping,
            "upper": self._cmd_upper,
            "lower": self._cmd_lower,
            "reverse": self._cmd_reverse,
            "echo": self._cmd_echo,
            "time": self._cmd_time,
            "help": self._cmd_help,
        }
    
    def procesează(self, mesaj: str) -> str:
        """
        Procesează un mesaj și returnează răspunsul.
        
        Args:
            mesaj: Mesajul primit de la client
            
        Returns:
            Răspunsul de trimis înapoi
        """
        mesaj = mesaj.strip()
        
        if not mesaj:
            return "EROARE:Mesaj gol"
        
        # Parsare comandă și argument
        if ":" in mesaj:
            părți = mesaj.split(":", 1)
            comandă = părți[0].lower()
            argument = părți[1] if len(părți) > 1 else ""
        else:
            comandă = mesaj.lower()
            argument = ""
        
        # Execuție comandă
        if comandă in self.comenzi:
            try:
                return self.comenzi[comandă](argument)
            except Exception as e:
                return f"EROARE:Eroare la procesare: {e}"
        else:
            return f"EROARE:Comandă necunoscută '{comandă}'. Folosiți 'help' pentru lista comenzilor."
    
    def _cmd_ping(self, _: str) -> str:
        """Verificare disponibilitate server."""
        return "PONG"
    
    def _cmd_upper(self, text: str) -> str:
        """Convertește textul la majuscule."""
        if not text:
            return "EROARE:Lipsește textul. Utilizare: upper:text"
        return text.upper()
    
    def _cmd_lower(self, text: str) -> str:
        """Convertește textul la minuscule."""
        if not text:
            return "EROARE:Lipsește textul. Utilizare: lower:text"
        return text.lower()
    
    def _cmd_reverse(self, text: str) -> str:
        """Inversează textul."""
        if not text:
            return "EROARE:Lipsește textul. Utilizare: reverse:text"
        return text[::-1]
    
    def _cmd_echo(self, text: str) -> str:
        """Returnează textul neschimbat."""
        if not text:
            return "EROARE:Lipsește textul. Utilizare: echo:text"
        return text
    
    def _cmd_time(self, _: str) -> str:
        """Returnează ora curentă a serverului."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _cmd_help(self, _: str) -> str:
        """Afișează comenzile disponibile."""
        return """Comenzi disponibile:
  ping        - Verifică disponibilitatea serverului
  upper:text  - Convertește textul la MAJUSCULE
  lower:text  - Convertește textul la minuscule
  reverse:text - Inversează textul
  echo:text   - Returnează textul neschimbat
  time        - Afișează ora serverului
  help        - Afișează acest mesaj"""


# ============================================================================
# Server UDP
# ============================================================================

class ServerUDP:
    """
    Server UDP pentru protocolul personalizat.
    
    Spre deosebire de TCP:
    - Nu există conexiune persistentă
    - Fiecare datagramă este independentă
    - Nu există handshake
    - Nu există garanție de livrare sau ordine
    """
    
    def __init__(self, config: ConfigurațieServer = CONFIG):
        """
        Inițializează serverul.
        
        Args:
            config: Configurația serverului
        """
        self.config = config
        self.socket_server: Optional[socket.socket] = None
        self.protocol = ProtocolUDP()
        self.rulează = False
        self.nr_cereri = 0
    
    def pornește(self) -> None:
        """Pornește serverul UDP."""
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket_server.bind((self.config.host, self.config.port))
            self.rulează = True
            
            print("=" * 60)
            print(f"Server UDP pornit pe {self.config.host}:{self.config.port}")
            print("Protocol: Comenzi text personalizate")
            print("Apăsați Ctrl+C pentru oprire")
            print("=" * 60)
            print()
            
            self._buclă_principală()
            
        except KeyboardInterrupt:
            print("\nOprire server...")
        finally:
            self.oprește()
    
    def _buclă_principală(self) -> None:
        """Buclă principală de procesare a datagramelor."""
        while self.rulează:
            try:
                self.socket_server.settimeout(1.0)
                date, adresă_client = self.socket_server.recvfrom(self.config.dimensiune_buffer)
                
                self.nr_cereri += 1
                mesaj = date.decode('utf-8')
                
                print(f"[{self.nr_cereri}] De la {adresă_client[0]}:{adresă_client[1]}: {mesaj.strip()}")
                
                # Procesare și răspuns
                răspuns = self.protocol.procesează(mesaj)
                self.socket_server.sendto(răspuns.encode('utf-8'), adresă_client)
                
                print(f"[{self.nr_cereri}] Răspuns: {răspuns[:50]}{'...' if len(răspuns) > 50 else ''}")
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.rulează:
                    print(f"Eroare: {e}")
    
    def oprește(self) -> None:
        """Oprește serverul."""
        self.rulează = False
        if self.socket_server:
            self.socket_server.close()
            print(f"Server oprit. Total cereri procesate: {self.nr_cereri}")


# ============================================================================
# Client UDP
# ============================================================================

class ClientUDP:
    """Client UDP pentru testarea serverului."""
    
    def __init__(self, host: str = "localhost", port: int = CONFIG.port):
        """
        Inițializează clientul.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
        """
        self.host = host
        self.port = port
        self.adresă_server = (host, port)
    
    def trimite_comandă(self, comandă: str, timeout: float = 2.0) -> Optional[str]:
        """
        Trimite o comandă și așteaptă răspuns.
        
        Args:
            comandă: Comanda de trimis
            timeout: Timeout în secunde
            
        Returns:
            Răspunsul serverului sau None la eroare/timeout
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)
                sock.sendto(comandă.encode('utf-8'), self.adresă_server)
                răspuns, _ = sock.recvfrom(4096)
                return răspuns.decode('utf-8')
        except socket.timeout:
            print("Timeout - serverul nu a răspuns")
            return None
        except Exception as e:
            print(f"Eroare: {e}")
            return None
    
    def sesiune_interactivă(self) -> None:
        """Pornește o sesiune interactivă cu serverul."""
        print(f"Client UDP conectat la {self.host}:{self.port}")
        print("Introduceți comenzi (quit pentru ieșire, help pentru ajutor)")
        print("-" * 40)
        
        while True:
            try:
                comandă = input("> ").strip()
                
                if not comandă:
                    continue
                
                if comandă.lower() in ("quit", "exit"):
                    print("La revedere!")
                    break
                
                răspuns = self.trimite_comandă(comandă)
                if răspuns:
                    print(răspuns)
                    
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nLa revedere!")
                break


# ============================================================================
# Teste Rapide
# ============================================================================

def rulează_teste_protocol() -> None:
    """Rulează teste pentru protocolul UDP."""
    print("=" * 60)
    print("Teste Protocol UDP")
    print("=" * 60)
    
    protocol = ProtocolUDP()
    
    teste = [
        ("ping", "PONG"),
        ("upper:salut", "SALUT"),
        ("lower:SALUT", "salut"),
        ("reverse:abc", "cba"),
        ("echo:test", "test"),
        ("time", None),  # Verificăm doar că nu e eroare
        ("comandă_inexistentă", None),  # Trebuie să fie eroare
    ]
    
    reușite = 0
    eșuate = 0
    
    for intrare, așteptat in teste:
        rezultat = protocol.procesează(intrare)
        
        if așteptat is None:
            # Doar verificăm că nu aruncă excepție
            print(f"  ✓ {intrare} → {rezultat[:40]}")
            reușite += 1
        elif rezultat == așteptat:
            print(f"  ✓ {intrare} → {rezultat}")
            reușite += 1
        else:
            print(f"  ✗ {intrare} → {rezultat} (așteptat: {așteptat})")
            eșuate += 1
    
    print()
    print(f"Rezultate: {reușite} reușite, {eșuate} eșuate")
    print("=" * 60)


# ============================================================================
# Punct de Intrare
# ============================================================================

def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Server și Client UDP - Exercițiul 2.02",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Pornire server
  python ex_2_02_udp.py server
  
  # Trimitere comandă
  python ex_2_02_udp.py client --command "ping"
  python ex_2_02_udp.py client --command "upper:salut lume"
  
  # Mod interactiv
  python ex_2_02_udp.py client --interactive
  
  # Rulare teste protocol
  python ex_2_02_udp.py test

Comenzi protocol:
  ping, upper:text, lower:text, reverse:text, echo:text, time, help
        """
    )
    
    subparsers = parser.add_subparsers(dest="comandă", help="Comandă de executat")
    
    # Subcomandă: server
    parser_server = subparsers.add_parser("server", help="Pornește serverul UDP")
    parser_server.add_argument(
        "--port", "-p",
        type=int,
        default=CONFIG.port,
        help=f"Port de ascultare (implicit: {CONFIG.port})"
    )
    
    # Subcomandă: client
    parser_client = subparsers.add_parser("client", help="Rulează clientul UDP")
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
        "--command", "-c",
        help="Comandă de trimis"
    )
    parser_client.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Mod interactiv"
    )
    
    # Subcomandă: test
    subparsers.add_parser("test", help="Rulează teste pentru protocol")
    
    args = parser.parse_args()
    
    if args.comandă == "server":
        config = ConfigurațieServer(port=args.port)
        server = ServerUDP(config)
        server.pornește()
        return 0
        
    elif args.comandă == "client":
        client = ClientUDP(args.host, args.port)
        
        if args.interactive:
            client.sesiune_interactivă()
        elif args.command:
            răspuns = client.trimite_comandă(args.command)
            if răspuns:
                print(răspuns)
                return 0
            return 1
        else:
            parser_client.print_help()
            return 1
        return 0
        
    elif args.comandă == "test":
        rulează_teste_protocol()
        return 0
        
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
