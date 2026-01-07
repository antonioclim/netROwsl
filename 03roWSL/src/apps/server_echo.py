#!/usr/bin/env python3
"""
Server Echo TCP
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Server simplu care returnează (echo) orice date primite de la client.
Folosit pentru testarea conectivității și demonstrații de tunelare.

Utilizare:
    python server_echo.py [--port PORT]
"""

import socket
import sys
import threading
import argparse
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAȚIE
# ═══════════════════════════════════════════════════════════════════════════

PORT_IMPLICIT = 8080
DIMENSIUNE_BUFFER = 4096


class ServerEcho:
    """
    Server TCP Echo simplu.
    
    Acceptă conexiuni și returnează datele primite înapoi clientului.
    Fiecare conexiune este gestionată într-un thread separat.
    """
    
    def __init__(self, port: int = PORT_IMPLICIT):
        """
        Inițializează serverul echo.
        
        Args:
            port: Portul pe care serverul ascultă
        """
        self.port = port
        self.socket_server: Optional[socket.socket] = None
        self.activ = False
        self.contor_conexiuni = 0
        self.lock = threading.Lock()
    
    def log(self, mesaj: str, id_conexiune: Optional[int] = None) -> None:
        """Afișează un mesaj cu timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        prefix = f"[conn-{id_conexiune:03d}]" if id_conexiune else "[server]"
        print(f"[{timestamp}] {prefix} {mesaj}")
    
    def gestioneaza_client(
        self,
        socket_client: socket.socket,
        adresa_client: tuple,
        id_conexiune: int
    ) -> None:
        """
        Gestionează o conexiune client.
        
        Citește date de la client și le trimite înapoi (echo).
        
        Args:
            socket_client: Socket-ul conexiunii
            adresa_client: Tuplu (IP, port) al clientului
            id_conexiune: ID unic pentru logging
        """
        ip_client, port_client = adresa_client
        self.log(f"Conexiune nouă de la {ip_client}:{port_client}", id_conexiune)
        
        total_bytes = 0
        
        try:
            while self.activ:
                # Primește date de la client
                date = socket_client.recv(DIMENSIUNE_BUFFER)
                
                if not date:
                    # Clientul a închis conexiunea
                    break
                
                # Trimite datele înapoi (echo)
                socket_client.sendall(date)
                total_bytes += len(date)
                
                # Log pentru debugging
                mesaj_previzualizare = date.decode('utf-8', errors='replace')[:50]
                if len(date) > 50:
                    mesaj_previzualizare += "..."
                self.log(f"Echo: {len(date)} bytes - '{mesaj_previzualizare}'", id_conexiune)
                
        except socket.error as e:
            self.log(f"Eroare socket: {e}", id_conexiune)
        except Exception as e:
            self.log(f"Eroare: {e}", id_conexiune)
        finally:
            try:
                socket_client.close()
            except Exception:
                pass
            self.log(f"Conexiune închisă, {total_bytes} bytes procesați", id_conexiune)
    
    def porneste(self) -> None:
        """Pornește serverul echo."""
        print("=" * 50)
        print("SERVER ECHO TCP")
        print("=" * 50)
        print(f"Ascultare pe: 0.0.0.0:{self.port}")
        print("Apăsați Ctrl+C pentru oprire")
        print("-" * 50)
        
        # Creează socket-ul de ascultare
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(('0.0.0.0', self.port))
        self.socket_server.listen(5)
        
        self.activ = True
        self.log("Server pornit, așteptare conexiuni...")
        
        try:
            while self.activ:
                try:
                    self.socket_server.settimeout(1.0)
                    socket_client, adresa_client = self.socket_server.accept()
                    
                    with self.lock:
                        self.contor_conexiuni += 1
                        id_conexiune = self.contor_conexiuni
                    
                    # Gestionează conexiunea într-un thread separat
                    thread = threading.Thread(
                        target=self.gestioneaza_client,
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
        """Oprește serverul."""
        self.activ = False
        
        if self.socket_server:
            try:
                self.socket_server.close()
            except Exception:
                pass
        
        self.log(f"Server oprit. Total conexiuni: {self.contor_conexiuni}")


def main():
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(description='Server Echo TCP')
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=PORT_IMPLICIT,
        help=f'Portul de ascultare (implicit: {PORT_IMPLICIT})'
    )
    args = parser.parse_args()
    
    server = ServerEcho(port=args.port)
    server.porneste()


if __name__ == '__main__':
    main()
