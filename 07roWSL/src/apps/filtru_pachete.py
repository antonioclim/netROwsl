#!/usr/bin/env python3
"""
Filtru de Pachete la Nivel Aplicație
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un proxy simplu care demonstrează filtrarea la nivel aplicație,
blocând cereri care conțin anumite cuvinte cheie.
"""

from __future__ import annotations

import argparse
import json
import socket
import threading
from datetime import datetime
from pathlib import Path


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}", flush=True)


class FiltruPachete:
    """Proxy cu filtrare la nivel aplicație."""
    
    def __init__(self, host: str, port: int, cale_config: Path | None = None):
        self.host = host
        self.port = port
        self.cuvinte_blocate: list[str] = []
        self.cuvinte_permise: list[str] = []
        
        if cale_config and cale_config.exists():
            self._incarca_config(cale_config)
    
    def _incarca_config(self, cale: Path):
        """Încarcă configurația din fișier JSON."""
        try:
            with open(cale, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.cuvinte_blocate = config.get("cuvinte_cheie_blocate", [])
            self.cuvinte_permise = config.get("cuvinte_cheie_permise", [])
            
            logheaza(f"Configurație încărcată: {len(self.cuvinte_blocate)} cuvinte blocate")
            
        except Exception as e:
            logheaza(f"Eroare la încărcarea configurației: {e}")
    
    def verifica_continut(self, date: bytes) -> tuple[bool, str]:
        """
        Verifică dacă conținutul este permis.
        
        Args:
            date: Datele de verificat
        
        Returns:
            Tuplu (permis, motiv)
        """
        try:
            text = date.decode('utf-8', errors='replace').lower()
            
            for cuvant in self.cuvinte_blocate:
                if cuvant.lower() in text:
                    return False, f"Cuvânt blocat detectat: '{cuvant}'"
            
            return True, "Conținut permis"
            
        except Exception as e:
            return False, f"Eroare la verificare: {e}"
    
    def gestioneaza_client(self, conn: socket.socket, adresa: tuple[str, int]):
        """Gestionează o conexiune de client."""
        ip_client, port_client = adresa
        logheaza(f"Conexiune nouă de la {ip_client}:{port_client}")
        
        try:
            date = conn.recv(4096)
            
            if not date:
                conn.close()
                return
            
            mesaj = date.decode('utf-8', errors='replace')
            logheaza(f"Cerere de la {ip_client}:{port_client}: {mesaj[:50]}...")
            
            # Verificare conținut
            permis, motiv = self.verifica_continut(date)
            
            if permis:
                logheaza(f"  [PERMIS] {motiv}")
                raspuns = b"HTTP/1.0 200 OK\r\n\r\nCerere acceptata\n"
            else:
                logheaza(f"  [BLOCAT] {motiv}")
                raspuns = b"HTTP/1.0 403 Forbidden\r\n\r\nCerere blocata de filtru\n"
            
            conn.sendall(raspuns)
            
        except Exception as e:
            logheaza(f"Eroare cu {ip_client}:{port_client}: {e}")
        finally:
            conn.close()
    
    def porneste(self):
        """Pornește serverul proxy."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            logheaza(f"Filtru pachete pornit pe {self.host}:{self.port}")
            logheaza(f"Cuvinte blocate: {', '.join(self.cuvinte_blocate) or 'niciunul'}")
            
            while True:
                try:
                    conn, adresa = server_socket.accept()
                    thread = threading.Thread(
                        target=self.gestioneaza_client,
                        args=(conn, adresa)
                    )
                    thread.daemon = True
                    thread.start()
                except KeyboardInterrupt:
                    logheaza("Filtru oprit de utilizator")
                    break
                    
        except OSError as e:
            logheaza(f"Eroare la pornirea filtrului: {e}")
        finally:
            server_socket.close()


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Filtru de pachete la nivel aplicație"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Adresa pe care să asculte (implicit: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8888,
        help="Portul pe care să asculte (implicit: 8888)"
    )
    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=Path("configs/firewall_profiles.json"),
        help="Calea către fișierul de configurare"
    )
    args = parser.parse_args()

    filtru = FiltruPachete(args.host, args.port, args.config)
    filtru.porneste()


if __name__ == "__main__":
    main()
