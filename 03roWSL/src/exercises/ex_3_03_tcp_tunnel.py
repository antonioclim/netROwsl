#!/usr/bin/env python3
"""
Exercițiul 3.3: Tunel TCP Bidirecțional
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Demonstrează crearea unui tunel TCP pentru redirecționarea transparentă
a conexiunilor. Tunelul acceptă conexiuni pe un port și le redirecționează
către un server destinație, relayând datele bidirecțional.

Concepte cheie:
- Relay TCP bidirecțional
- Gestionarea conexiunilor cu threading
- Pattern-ul proxy/intermediar
- Tratarea elegantă a deconectărilor

Utilizare:
    python ex_3_03_tcp_tunnel.py --port-ascultare 9090 --host-tinta 172.20.0.10 --port-tinta 8080
"""

import socket
import sys
import threading
import argparse
import signal
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAȚIE
# ═══════════════════════════════════════════════════════════════════════════

PORT_ASCULTARE = 9090
HOST_TINTA = '172.20.0.10'
PORT_TINTA = 8080
DIMENSIUNE_BUFFER = 4096


# ═══════════════════════════════════════════════════════════════════════════
# RELAY DATE BIDIRECȚIONAL
# ═══════════════════════════════════════════════════════════════════════════

class TunelTCP:
    """
    Implementează un tunel TCP care redirecționează conexiuni.
    
    Arhitectura:
    
    Client ←→ Tunel ←→ Server
    
    1. Clientul se conectează la tunel
    2. Tunelul creează conexiune către server
    3. Datele sunt relayate bidirecțional între cele două conexiuni
    """
    
    def __init__(
        self,
        port_ascultare: int,
        host_tinta: str,
        port_tinta: int
    ):
        """
        Inițializează tunelul TCP.
        
        Args:
            port_ascultare: Portul pe care tunelul acceptă conexiuni
            host_tinta: Adresa serverului destinație
            port_tinta: Portul serverului destinație
        """
        self.port_ascultare = port_ascultare
        self.host_tinta = host_tinta
        self.port_tinta = port_tinta
        self.socket_server: Optional[socket.socket] = None
        self.activ = False
        self.contor_conexiuni = 0
        self.lock = threading.Lock()
    
    def log(self, mesaj: str, id_conexiune: Optional[int] = None) -> None:
        """Afișează un mesaj cu timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        prefix = f"[conn-{id_conexiune:03d}]" if id_conexiune else "[tunel]"
        print(f"[{timestamp}] {prefix} {mesaj}")
    
    def relay_date(
        self,
        sursa: socket.socket,
        destinatie: socket.socket,
        directie: str,
        id_conexiune: int
    ) -> None:
        """
        Relayează date de la sursă la destinație.
        
        Această funcție rulează într-un thread separat pentru fiecare
        direcție de comunicare (client→server și server→client).
        
        Args:
            sursa: Socket-ul de citire
            destinatie: Socket-ul de scriere
            directie: Descriere pentru logging
            id_conexiune: ID-ul conexiunii pentru logging
        """
        total_bytes = 0
        
        try:
            while self.activ:
                # Citește date de la sursă
                date = sursa.recv(DIMENSIUNE_BUFFER)
                
                if not date:
                    # Conexiune închisă de peer
                    self.log(f"{directie}: conexiune închisă de peer", id_conexiune)
                    break
                
                # Trimite date către destinație
                # sendall() asigură trimiterea completă
                destinatie.sendall(date)
                total_bytes += len(date)
                
        except socket.error as e:
            self.log(f"{directie}: eroare socket - {e}", id_conexiune)
        except Exception as e:
            self.log(f"{directie}: eroare - {e}", id_conexiune)
        finally:
            # Închide ambele socket-uri pentru a semnala celuilalt thread
            try:
                sursa.shutdown(socket.SHUT_RD)
            except Exception:
                pass
            try:
                destinatie.shutdown(socket.SHUT_WR)
            except Exception:
                pass
            
            self.log(f"{directie}: terminat, {total_bytes} bytes transferați", id_conexiune)
    
    def gestioneaza_conexiune(
        self,
        socket_client: socket.socket,
        adresa_client: tuple,
        id_conexiune: int
    ) -> None:
        """
        Gestionează o conexiune client individuală.
        
        Pași:
        1. Creează conexiune către serverul țintă
        2. Pornește două thread-uri pentru relay bidirecțional
        3. Așteaptă terminarea ambelor thread-uri
        4. Curăță resursele
        
        Args:
            socket_client: Socket-ul conexiunii client
            adresa_client: Tuplu (IP, port) al clientului
            id_conexiune: ID unic pentru această conexiune
        """
        ip_client, port_client = adresa_client
        self.log(f"Nouă conexiune de la {ip_client}:{port_client}", id_conexiune)
        
        socket_server = None
        
        try:
            # Creează conexiune către serverul țintă
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.settimeout(10)  # Timeout pentru conectare
            socket_server.connect((self.host_tinta, self.port_tinta))
            socket_server.settimeout(None)  # Elimină timeout după conectare
            
            self.log(f"Conectat la țintă {self.host_tinta}:{self.port_tinta}", id_conexiune)
            
            # Pornește thread-uri pentru relay bidirecțional
            thread_client_server = threading.Thread(
                target=self.relay_date,
                args=(socket_client, socket_server, "client→server", id_conexiune),
                daemon=True
            )
            
            thread_server_client = threading.Thread(
                target=self.relay_date,
                args=(socket_server, socket_client, "server→client", id_conexiune),
                daemon=True
            )
            
            thread_client_server.start()
            thread_server_client.start()
            
            # Așteaptă terminarea ambelor thread-uri
            thread_client_server.join()
            thread_server_client.join()
            
        except ConnectionRefusedError:
            self.log(f"Conexiune refuzată de {self.host_tinta}:{self.port_tinta}", id_conexiune)
        except socket.timeout:
            self.log(f"Timeout la conectarea către {self.host_tinta}:{self.port_tinta}", id_conexiune)
        except Exception as e:
            self.log(f"Eroare: {e}", id_conexiune)
        finally:
            # Curăță conexiunile
            try:
                socket_client.close()
            except Exception:
                pass
            
            if socket_server:
                try:
                    socket_server.close()
                except Exception:
                    pass
            
            self.log(f"Conexiune închisă", id_conexiune)
    
    def porneste(self) -> None:
        """
        Pornește tunelul TCP.
        
        Creează socket-ul de ascultare și acceptă conexiuni într-o buclă.
        Fiecare conexiune este gestionată într-un thread separat.
        """
        print("=" * 60)
        print("TUNEL TCP BIDIRECȚIONAL")
        print("=" * 60)
        print(f"Ascultare pe: 0.0.0.0:{self.port_ascultare}")
        print(f"Redirecționare către: {self.host_tinta}:{self.port_tinta}")
        print("Apăsați Ctrl+C pentru oprire")
        print("-" * 60)
        
        # Creează socket-ul de ascultare
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(('0.0.0.0', self.port_ascultare))
        self.socket_server.listen(5)
        
        self.activ = True
        self.log("Tunel pornit, așteptare conexiuni...")
        
        try:
            while self.activ:
                try:
                    # Acceptă conexiuni cu timeout pentru a permite oprirea
                    self.socket_server.settimeout(1.0)
                    socket_client, adresa_client = self.socket_server.accept()
                    
                    # Generează ID pentru conexiune
                    with self.lock:
                        self.contor_conexiuni += 1
                        id_conexiune = self.contor_conexiuni
                    
                    # Gestionează conexiunea într-un thread separat
                    thread = threading.Thread(
                        target=self.gestioneaza_conexiune,
                        args=(socket_client, adresa_client, id_conexiune),
                        daemon=True
                    )
                    thread.start()
                    
                except socket.timeout:
                    continue
                    
        except KeyboardInterrupt:
            self.log("Oprire inițiată de utilizator...")
        finally:
            self.opreste()
    
    def opreste(self) -> None:
        """Oprește tunelul și curăță resursele."""
        self.activ = False
        
        if self.socket_server:
            try:
                self.socket_server.close()
            except Exception:
                pass
        
        self.log(f"Tunel oprit. Total conexiuni gestionate: {self.contor_conexiuni}")


# ═══════════════════════════════════════════════════════════════════════════
# PUNCT DE INTRARE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Parsează argumentele și pornește tunelul."""
    parser = argparse.ArgumentParser(
        description='Tunel TCP Bidirecțional',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  Tunel simplu către server local:
    python ex_3_03_tcp_tunnel.py --port-ascultare 9090 --host-tinta localhost --port-tinta 8080
    
  Tunel către server în rețea:
    python ex_3_03_tcp_tunnel.py -l 9090 -H 172.20.0.10 -P 8080
    
Testare:
  # Terminal 1: Pornește tunelul
  python ex_3_03_tcp_tunnel.py -l 9090 -H 172.20.0.10 -P 8080
  
  # Terminal 2: Conectează-te prin tunel
  echo "Test" | nc localhost 9090
        """
    )
    
    parser.add_argument(
        '--port-ascultare', '-l',
        type=int,
        default=PORT_ASCULTARE,
        help=f'Portul pe care tunelul ascultă (implicit: {PORT_ASCULTARE})'
    )
    parser.add_argument(
        '--host-tinta', '-H',
        type=str,
        default=HOST_TINTA,
        help=f'Adresa serverului țintă (implicit: {HOST_TINTA})'
    )
    parser.add_argument(
        '--port-tinta', '-P',
        type=int,
        default=PORT_TINTA,
        help=f'Portul serverului țintă (implicit: {PORT_TINTA})'
    )
    
    args = parser.parse_args()
    
    tunel = TunelTCP(
        port_ascultare=args.port_ascultare,
        host_tinta=args.host_tinta,
        port_tinta=args.port_tinta
    )
    
    tunel.porneste()


if __name__ == '__main__':
    main()
