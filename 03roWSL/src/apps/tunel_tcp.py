#!/usr/bin/env python3
"""
Tunel TCP pentru Servicii
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Aplicație de tunelare TCP care redirecționează conexiuni către un server țintă.
Versiune de producție pentru containerul router.

Utilizare:
    python tunel_tcp.py --port-ascultare 9090 --host-tinta 172.20.0.10 --port-tinta 8080
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
TIMEOUT_CONECTARE = 10


class TunelTCPServicii:
    """
    Tunel TCP pentru redirecționarea transparentă a conexiunilor.
    
    Funcționează ca un proxy simplu, acceptând conexiuni pe un port
    și redirecționându-le către serverul țintă.
    """
    
    def __init__(
        self,
        port_ascultare: int,
        host_tinta: str,
        port_tinta: int
    ):
        """
        Inițializează tunelul.
        
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
        self.conexiuni_active = 0
        self.lock = threading.Lock()
    
    def log(self, mesaj: str, id_conn: Optional[int] = None) -> None:
        """Afișează mesaj cu timestamp."""
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        prefix = f"[{id_conn:03d}]" if id_conn else "[tunel]"
        print(f"[{ts}] {prefix} {mesaj}", flush=True)
    
    def relay(
        self,
        sursa: socket.socket,
        dest: socket.socket,
        directie: str,
        id_conn: int
    ) -> int:
        """
        Relayează date între două socket-uri.
        
        Args:
            sursa: Socket sursă
            dest: Socket destinație
            directie: Descriere pentru log
            id_conn: ID conexiune
            
        Returns:
            Numărul total de bytes transferați
        """
        total = 0
        try:
            while self.activ:
                date = sursa.recv(DIMENSIUNE_BUFFER)
                if not date:
                    break
                dest.sendall(date)
                total += len(date)
        except Exception:
            pass
        finally:
            try:
                sursa.shutdown(socket.SHUT_RD)
            except Exception:
                pass
            try:
                dest.shutdown(socket.SHUT_WR)
            except Exception:
                pass
        return total
    
    def gestioneaza_conexiune(
        self,
        sock_client: socket.socket,
        addr_client: tuple,
        id_conn: int
    ) -> None:
        """
        Gestionează o conexiune client.
        
        Args:
            sock_client: Socket-ul clientului
            addr_client: Adresa clientului
            id_conn: ID-ul conexiunii
        """
        ip, port = addr_client
        
        with self.lock:
            self.conexiuni_active += 1
        
        self.log(f"Conexiune de la {ip}:{port}", id_conn)
        
        sock_tinta = None
        bytes_trimise = 0
        bytes_primite = 0
        
        try:
            # Conectare la țintă
            sock_tinta = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_tinta.settimeout(TIMEOUT_CONECTARE)
            sock_tinta.connect((self.host_tinta, self.port_tinta))
            sock_tinta.settimeout(None)
            
            self.log(f"Conectat la {self.host_tinta}:{self.port_tinta}", id_conn)
            
            # Relay bidirecțional
            rezultate = [0, 0]
            
            def relay_cu_rezultat(sursa, dest, idx):
                rezultate[idx] = self.relay(sursa, dest, "", id_conn)
            
            t1 = threading.Thread(
                target=relay_cu_rezultat,
                args=(sock_client, sock_tinta, 0)
            )
            t2 = threading.Thread(
                target=relay_cu_rezultat,
                args=(sock_tinta, sock_client, 1)
            )
            
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            
            bytes_trimise = rezultate[0]
            bytes_primite = rezultate[1]
            
        except ConnectionRefusedError:
            self.log(f"Conexiune refuzată de țintă", id_conn)
        except socket.timeout:
            self.log(f"Timeout la conectare", id_conn)
        except Exception as e:
            self.log(f"Eroare: {e}", id_conn)
        finally:
            try:
                sock_client.close()
            except Exception:
                pass
            if sock_tinta:
                try:
                    sock_tinta.close()
                except Exception:
                    pass
            
            with self.lock:
                self.conexiuni_active -= 1
            
            self.log(
                f"Închis: ↑{bytes_trimise}B ↓{bytes_primite}B (active: {self.conexiuni_active})",
                id_conn
            )
    
    def porneste(self) -> None:
        """Pornește tunelul."""
        print("=" * 60)
        print("TUNEL TCP - SERVICIU")
        print("=" * 60)
        print(f"Ascultare: 0.0.0.0:{self.port_ascultare}")
        print(f"Țintă: {self.host_tinta}:{self.port_tinta}")
        print("-" * 60)
        
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(('0.0.0.0', self.port_ascultare))
        self.socket_server.listen(10)
        
        self.activ = True
        self.log("Tunel activ")
        
        try:
            while self.activ:
                try:
                    self.socket_server.settimeout(1.0)
                    sock_client, addr_client = self.socket_server.accept()
                    
                    with self.lock:
                        self.contor_conexiuni += 1
                        id_conn = self.contor_conexiuni
                    
                    thread = threading.Thread(
                        target=self.gestioneaza_conexiune,
                        args=(sock_client, addr_client, id_conn),
                        daemon=True
                    )
                    thread.start()
                    
                except socket.timeout:
                    continue
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.opreste()
    
    def opreste(self) -> None:
        """Oprește tunelul."""
        self.activ = False
        if self.socket_server:
            try:
                self.socket_server.close()
            except Exception:
                pass
        self.log(f"Oprit. Total conexiuni: {self.contor_conexiuni}")


def main():
    """Punct de intrare."""
    parser = argparse.ArgumentParser(description='Tunel TCP Serviciu')
    parser.add_argument('--port-ascultare', '-l', type=int, default=PORT_ASCULTARE)
    parser.add_argument('--host-tinta', '-H', type=str, default=HOST_TINTA)
    parser.add_argument('--port-tinta', '-P', type=int, default=PORT_TINTA)
    args = parser.parse_args()
    
    tunel = TunelTCPServicii(
        port_ascultare=args.port_ascultare,
        host_tinta=args.host_tinta,
        port_tinta=args.port_tinta
    )
    tunel.porneste()


if __name__ == '__main__':
    main()
