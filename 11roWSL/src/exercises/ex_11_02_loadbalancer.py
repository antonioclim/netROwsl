#!/usr/bin/env python3
"""
Exercițiul 11.02: Echilibror de Sarcină Python
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Implementare de echilibror de sarcină cu suport pentru:
- Round-robin: distribuție ciclică
- Least-connections: cel mai puțin încărcat
- IP hash: sesiuni persistente

Include și un generator de sarcină pentru testare.

Utilizare:
    # Pornește echiliborul
    python ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --algo rr
    
    # Generează sarcină
    python ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 100 --c 10
"""

import argparse
import hashlib
import socket
import threading
import time
from dataclasses import dataclass, field
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class Backend:
    """Reprezintă un server backend."""
    host: str
    port: int
    conexiuni_active: int = 0
    esecuri: int = 0
    indisponibil_pana: float = 0.0
    
    @property
    def adresa(self) -> tuple[str, int]:
        return (self.host, self.port)
    
    @property
    def disponibil(self) -> bool:
        return time.time() >= self.indisponibil_pana
    
    def marcheaza_esec(self, timeout_esec: float = 10.0):
        """Marchează un eșec și indisponibilizează temporar."""
        self.esecuri += 1
        self.indisponibil_pana = time.time() + timeout_esec
    
    def reseteaza(self):
        """Resetează starea de eșec."""
        self.esecuri = 0
        self.indisponibil_pana = 0.0


class EchilibrorSarcina:
    """
    Implementare echilibror de sarcină.
    
    Suportă algoritmii: round-robin (rr), least-connections (least_conn), ip_hash
    """
    
    def __init__(
        self,
        backend_uri: list[tuple[str, int]],
        algoritm: str = "rr",
        esecuri_pasive: int = 1,
        timeout_esec: float = 10.0,
        timeout_socket: float = 2.5
    ):
        """
        Inițializează echiliborul.
        
        Args:
            backend_uri: Lista de backend-uri (host, port)
            algoritm: Algoritmul de echilibrare (rr, least_conn, ip_hash)
            esecuri_pasive: Număr de eșecuri înainte de marcarea ca indisponibil
            timeout_esec: Timpul de așteptare după un eșec
            timeout_socket: Timeout pentru conexiuni
        """
        self.backend_uri = [Backend(h, p) for h, p in backend_uri]
        self.algoritm = algoritm
        self.esecuri_pasive = esecuri_pasive
        self.timeout_esec = timeout_esec
        self.timeout_socket = timeout_socket
        
        self._index_rr = 0
        self._lock = threading.Lock()
    
    def obtine_backend_uri_disponibile(self) -> list[Backend]:
        """Returnează lista backend-urilor disponibile."""
        return [b for b in self.backend_uri if b.disponibil]
    
    def selecteaza_backend(self, ip_client: str = "") -> Optional[Backend]:
        """
        Selectează un backend conform algoritmului configurat.
        
        Args:
            ip_client: Adresa IP a clientului (pentru ip_hash)
        
        Returns:
            Backend selectat sau None dacă niciunul nu e disponibil
        """
        disponibile = self.obtine_backend_uri_disponibile()
        
        if not disponibile:
            return None
        
        if self.algoritm == "rr":
            return self._selecteaza_round_robin(disponibile)
        elif self.algoritm == "least_conn":
            return self._selecteaza_least_connections(disponibile)
        elif self.algoritm == "ip_hash":
            return self._selecteaza_ip_hash(disponibile, ip_client)
        else:
            return self._selecteaza_round_robin(disponibile)
    
    def _selecteaza_round_robin(self, disponibile: list[Backend]) -> Backend:
        """Selectează backend-ul următor în ordine ciclică."""
        with self._lock:
            self._index_rr = self._index_rr % len(disponibile)
            backend = disponibile[self._index_rr]
            self._index_rr += 1
            return backend
    
    def _selecteaza_least_connections(self, disponibile: list[Backend]) -> Backend:
        """Selectează backend-ul cu cele mai puține conexiuni active."""
        return min(disponibile, key=lambda b: b.conexiuni_active)
    
    def _selecteaza_ip_hash(self, disponibile: list[Backend], ip_client: str) -> Backend:
        """Selectează backend-ul bazat pe hash-ul IP-ului clientului."""
        hash_val = int(hashlib.md5(ip_client.encode()).hexdigest(), 16)
        index = hash_val % len(disponibile)
        return disponibile[index]
    
    def redirectioneaza_cerere(
        self,
        sock_client: socket.socket,
        adresa_client: tuple,
        verbose: bool = False
    ) -> bool:
        """
        Redirecționează o cerere către un backend.
        
        Args:
            sock_client: Socket-ul clientului
            adresa_client: Adresa clientului
            verbose: Afișează mesaje detaliate
        
        Returns:
            True dacă redirecționarea a reușit
        """
        try:
            # Primește cererea
            sock_client.settimeout(self.timeout_socket)
            cerere = sock_client.recv(8192)
            
            if not cerere:
                return False
            
            # Selectează un backend
            ip_client = adresa_client[0]
            backend = self.selecteaza_backend(ip_client)
            
            if backend is None:
                # Niciun backend disponibil - trimite eroare
                raspuns_eroare = (
                    "HTTP/1.1 503 Service Unavailable\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: 20\r\n"
                    "\r\n"
                    "Serviciu indisponibil"
                )
                sock_client.sendall(raspuns_eroare.encode())
                return False
            
            # Redirecționează către backend
            backend.conexiuni_active += 1
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_backend:
                    sock_backend.settimeout(self.timeout_socket)
                    sock_backend.connect(backend.adresa)
                    sock_backend.sendall(cerere)
                    
                    # Primește și redirecționează răspunsul
                    while True:
                        date = sock_backend.recv(4096)
                        if not date:
                            break
                        sock_client.sendall(date)
                
                backend.reseteaza()
                
                if verbose:
                    print(f"[ES] {ip_client} → {backend.host}:{backend.port}")
                
                return True
                
            except Exception as e:
                backend.marcheaza_esec(self.timeout_esec)
                if verbose:
                    print(f"[ES] Eșec la {backend.host}:{backend.port}: {e}")
                return False
            finally:
                backend.conexiuni_active -= 1
                
        except Exception as e:
            if verbose:
                print(f"[ES] Eroare client: {e}")
            return False
    
    def ruleaza(self, host: str = "0.0.0.0", port: int = 8080, verbose: bool = False):
        """
        Pornește echiliborul de sarcină.
        
        Args:
            host: Adresa pe care să asculte
            port: Portul pe care să asculte
            verbose: Afișează mesaje detaliate
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server.bind((host, port))
            server.listen(128)
            
            backend_str = ", ".join(f"{b.host}:{b.port}" for b in self.backend_uri)
            print(f"[ES] Ascultă pe {host}:{port} | algo={self.algoritm}")
            print(f"[ES] Backend-uri: [{backend_str}]")
            print(f"[ES] esecuri_pasive={self.esecuri_pasive} timeout_esec={self.timeout_esec}s")
            print()
            
            while True:
                sock_client, adresa = server.accept()
                thread = threading.Thread(
                    target=self._gestioneaza_conexiune,
                    args=(sock_client, adresa, verbose)
                )
                thread.daemon = True
                thread.start()
                
        except KeyboardInterrupt:
            print("\n[ES] Oprire...")
        finally:
            server.close()
    
    def _gestioneaza_conexiune(
        self, 
        sock_client: socket.socket, 
        adresa: tuple, 
        verbose: bool
    ):
        """Gestionează o conexiune de client."""
        try:
            self.redirectioneaza_cerere(sock_client, adresa, verbose)
        finally:
            sock_client.close()


def http_get_simplu(url: str, timeout: float = 5.0) -> tuple[int, float]:
    """
    Execută o cerere HTTP GET simplă.
    
    Returns:
        Tuple (cod_status, latenta_ms)
    """
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 80
    path = parsed.path or "/"
    
    timp_start = time.time()
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            
            cerere = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            s.sendall(cerere.encode())
            
            raspuns = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                raspuns += chunk
            
            latenta = (time.time() - timp_start) * 1000
            
            # Extrage codul de stare
            prima_linie = raspuns.decode('utf-8', errors='ignore').split('\r\n')[0]
            status = int(prima_linie.split()[1])
            
            return (status, latenta)
            
    except Exception:
        return (0, 0.0)


def ruleaza_generator_sarcina(url: str, numar_cereri: int, concurenta: int):
    """
    Rulează generatorul de sarcină.
    
    Args:
        url: URL-ul de testat
        numar_cereri: Numărul total de cereri
        concurenta: Numărul de cereri simultane
    """
    print(f"[generator] url={url}")
    print(f"[generator] n={numar_cereri} c={concurenta}")
    
    latente = []
    statusuri = {}
    
    timp_start = time.time()
    
    with ThreadPoolExecutor(max_workers=concurenta) as executor:
        futures = [
            executor.submit(http_get_simplu, url)
            for _ in range(numar_cereri)
        ]
        
        for future in as_completed(futures):
            status, latenta = future.result()
            statusuri[status] = statusuri.get(status, 0) + 1
            if latenta > 0:
                latente.append(latenta)
    
    durata = time.time() - timp_start
    rps = numar_cereri / durata
    
    print(f"[generator] durata={durata:.3f}s rps={rps:.2f}")
    print(f"[generator] distribuție_statusuri={statusuri}")
    
    if latente:
        latente.sort()
        def percentila(p):
            idx = int(len(latente) * p / 100)
            return latente[min(idx, len(latente)-1)]
        
        print(f"[generator] latențe_ms: p50={percentila(50):.4f} p90={percentila(90):.4f} "
              f"p95={percentila(95):.4f} p99={percentila(99):.4f}")


def parseaza_backend_uri(backend_str: str) -> list[tuple[str, int]]:
    """Parsează șirul de backend-uri în liste de (host, port)."""
    rezultat = []
    for parte in backend_str.split(','):
        host, port = parte.strip().split(':')
        rezultat.append((host, int(port)))
    return rezultat


def main():
    parser = argparse.ArgumentParser(
        description="Echilibror de sarcină Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Pornește echiliborul cu round-robin
  python ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082 --algo rr
  
  # Pornește cu IP hash pentru sesiuni persistente
  python ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082 --algo ip_hash
  
  # Generează sarcină de test
  python ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 100 --c 10
        """
    )
    
    subparsers = parser.add_subparsers(dest='comanda')
    
    # Subcomandă pentru generator de sarcină
    parser_loadgen = subparsers.add_parser('loadgen', help='Generează sarcină de test')
    parser_loadgen.add_argument('--url', required=True, help='URL-ul de testat')
    parser_loadgen.add_argument('--n', type=int, default=100, help='Număr de cereri')
    parser_loadgen.add_argument('--c', type=int, default=10, help='Concurență')
    
    # Argumente pentru echilibor
    parser.add_argument(
        '--backends', '-b',
        help='Backend-uri (format: host:port,host:port,...)'
    )
    parser.add_argument(
        '--algo', '-a',
        choices=['rr', 'least_conn', 'ip_hash'],
        default='rr',
        help='Algoritm de echilibrare (implicit: rr)'
    )
    parser.add_argument(
        '--listen', '-l',
        default='0.0.0.0:8080',
        help='Adresa de ascultare (implicit: 0.0.0.0:8080)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Afișează mesaje detaliate'
    )
    
    args = parser.parse_args()
    
    if args.comanda == 'loadgen':
        ruleaza_generator_sarcina(args.url, args.n, args.c)
    else:
        if not args.backends:
            parser.error("--backends este obligatoriu pentru modul echilibror")
        
        backend_uri = parseaza_backend_uri(args.backends)
        host, port = args.listen.split(':')
        
        es = EchilibrorSarcina(backend_uri, algoritm=args.algo)
        es.ruleaza(host, int(port), args.verbose)


if __name__ == '__main__':
    main()
