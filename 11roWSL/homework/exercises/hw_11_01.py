#!/usr/bin/env python3
"""
Tema 11.01: Echilibror de Sarcină Extins cu Verificări Active de Stare
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest fișier conține scheletul pentru tema 1.
Implementați funcțiile marcate cu TODO.

Punctaj:
- Verificări active de stare: 40 puncte
- Weighted Round Robin: 30 puncte
- Endpoint de statistici: 20 puncte
- Degradare grațioasă: 10 puncte
"""

import argparse
import json
import socket
import threading
import time
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Backend:
    """Reprezintă un server backend."""
    host: str
    port: int
    weight: int = 1
    sanatos: bool = True
    esecuri_consecutive: int = 0
    succese_consecutive: int = 0
    total_cereri: int = 0
    conexiuni_active: int = 0
    
    @property
    def adresa(self) -> tuple[str, int]:
        return (self.host, self.port)


class VerificatorStare:
    """
    Thread pentru verificări active de stare.
    
    TODO: Implementați verificările periodice HTTP.
    """
    
    def __init__(
        self,
        backend_uri: list[Backend],
        interval: float = 5.0,
        prag_nesanatos: int = 3,
        prag_sanatos: int = 2
    ):
        """
        Inițializează verificatorul de stare.
        
        Args:
            backend_uri: Lista de backend-uri de verificat
            interval: Interval între verificări în secunde
            prag_nesanatos: Număr de eșecuri pentru a marca ca nesănătos
            prag_sanatos: Număr de succese pentru a marca ca sănătos
        """
        self.backend_uri = backend_uri
        self.interval = interval
        self.prag_nesanatos = prag_nesanatos
        self.prag_sanatos = prag_sanatos
        self._opreste = threading.Event()
        self._thread: Optional[threading.Thread] = None
    
    def porneste(self):
        """Pornește thread-ul de verificare."""
        # TODO: Implementați pornirea thread-ului
        # Sfat: Creați un thread daemon care rulează self._bucla_verificare
        pass
    
    def opreste(self):
        """Oprește thread-ul de verificare."""
        # TODO: Implementați oprirea grațioasă
        pass
    
    def _bucla_verificare(self):
        """Bucla principală de verificare."""
        # TODO: Implementați bucla care verifică periodic fiecare backend
        # Sfat: Folosiți self._opreste.wait(self.interval) pentru pauze
        pass
    
    def _verifica_backend(self, backend: Backend) -> bool:
        """
        Verifică starea unui backend.
        
        Args:
            backend: Backend-ul de verificat
        
        Returns:
            True dacă backend-ul răspunde corect
        """
        # TODO: Implementați verificarea HTTP
        # Sfat: Trimiteți GET /health și verificați status 200
        # Sfat: Actualizați esecuri_consecutive/succese_consecutive
        # Sfat: Marcați backend.sanatos conform pragurilor
        pass


class EchilibrorPonderat:
    """
    Echilibror de sarcină cu weighted round-robin și health checks.
    
    TODO: Implementați logica de echilibrare ponderată.
    """
    
    def __init__(
        self,
        backend_uri: list[tuple[str, int]],
        ponderi: list[int],
        interval_verificare: float = 5.0
    ):
        """
        Inițializează echiliborul ponderat.
        
        Args:
            backend_uri: Lista de (host, port)
            ponderi: Lista de ponderi pentru fiecare backend
            interval_verificare: Interval pentru health checks
        """
        self.timp_pornire = datetime.now()
        self.total_cereri = 0
        
        # Creează obiectele Backend cu ponderi
        self.backend_uri = [
            Backend(host, port, weight)
            for (host, port), weight in zip(backend_uri, ponderi)
        ]
        
        # Creează verificatorul de stare
        self.verificator = VerificatorStare(
            self.backend_uri,
            interval=interval_verificare
        )
        
        # TODO: Inițializați variabilele pentru weighted round-robin
        # Sfat: Aveți nevoie de un index curent și poate o listă expandată
        self._lock = threading.Lock()
    
    def selecteaza_backend(self) -> Optional[Backend]:
        """
        Selectează un backend folosind weighted round-robin.
        
        Returns:
            Backend selectat sau None dacă niciunul nu e disponibil
        """
        # TODO: Implementați weighted round-robin
        # Sfat: O abordare simplă este să expandați lista conform ponderilor
        # Exemplu: ponderi [3,2,1] -> [B1,B1,B1,B2,B2,B3]
        # Sfat: Săriți peste backend-urile nesănătoase
        pass
    
    def obtine_statistici(self) -> dict:
        """
        Returnează statisticile curente.
        
        Returns:
            Dicționar cu statisticile echilibrului
        """
        # TODO: Implementați colectarea statisticilor
        # Sfat: Calculați uptime, total cereri, stats per backend
        return {
            "uptime_seconds": 0,
            "total_requests": 0,
            "backends": []
        }
    
    def gestioneaza_cerere(self, sock_client: socket.socket, adresa: tuple):
        """
        Gestionează o cerere de la client.
        
        Args:
            sock_client: Socket-ul clientului
            adresa: Adresa clientului
        """
        try:
            # Primește cererea
            sock_client.settimeout(5.0)
            cerere = sock_client.recv(8192)
            
            if not cerere:
                return
            
            cerere_text = cerere.decode('utf-8', errors='ignore')
            
            # Verifică dacă e cerere de statistici
            if "GET /stats" in cerere_text:
                self._raspunde_statistici(sock_client)
                return
            
            # Selectează un backend
            backend = self.selecteaza_backend()
            
            if backend is None:
                # TODO: Implementați degradare grațioasă (503)
                self._raspunde_serviciu_indisponibil(sock_client)
                return
            
            # TODO: Redirecționați cererea către backend
            # Sfat: Incrementați total_cereri și backend.total_cereri
            # Sfat: Gestionați conexiuni_active pentru least_conn (opțional)
            
        except Exception as e:
            print(f"[Eroare] {e}")
        finally:
            sock_client.close()
    
    def _raspunde_statistici(self, sock_client: socket.socket):
        """Trimite răspunsul JSON cu statisticile."""
        stats = self.obtine_statistici()
        body = json.dumps(stats, indent=2)
        
        raspuns = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
            f"{body}"
        )
        sock_client.sendall(raspuns.encode())
    
    def _raspunde_serviciu_indisponibil(self, sock_client: socket.socket):
        """Trimite răspuns 503 Service Unavailable."""
        body = "Serviciu temporar indisponibil. Toate backend-urile sunt nesănătoase."
        
        raspuns = (
            "HTTP/1.1 503 Service Unavailable\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "\r\n"
            f"{body}"
        )
        sock_client.sendall(raspuns.encode())
    
    def ruleaza(self, host: str = "0.0.0.0", port: int = 8080):
        """
        Pornește echiliborul de sarcină.
        
        Args:
            host: Adresa pe care să asculte
            port: Portul pe care să asculte
        """
        # Pornește verificatorul de stare
        self.verificator.porneste()
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server.bind((host, port))
            server.listen(128)
            
            ponderi_str = ", ".join(f"{b.host}:{b.port}(w={b.weight})" for b in self.backend_uri)
            print(f"[ES] Ascultă pe {host}:{port}")
            print(f"[ES] Backend-uri: [{ponderi_str}]")
            print(f"[ES] Health checks la fiecare {self.verificator.interval}s")
            print(f"[ES] Statistici disponibile la /stats")
            print()
            
            while True:
                sock_client, adresa = server.accept()
                thread = threading.Thread(
                    target=self.gestioneaza_cerere,
                    args=(sock_client, adresa)
                )
                thread.daemon = True
                thread.start()
                
        except KeyboardInterrupt:
            print("\n[ES] Oprire...")
        finally:
            self.verificator.opreste()
            server.close()


def parseaza_backend_uri(backend_str: str) -> list[tuple[str, int]]:
    """Parsează șirul de backend-uri."""
    rezultat = []
    for parte in backend_str.split(','):
        host, port = parte.strip().split(':')
        rezultat.append((host, int(port)))
    return rezultat


def parseaza_ponderi(ponderi_str: str, numar_backends: int) -> list[int]:
    """Parsează șirul de ponderi."""
    if not ponderi_str:
        return [1] * numar_backends
    
    ponderi = [int(p.strip()) for p in ponderi_str.split(',')]
    
    if len(ponderi) != numar_backends:
        raise ValueError(
            f"Numărul de ponderi ({len(ponderi)}) nu corespunde "
            f"cu numărul de backend-uri ({numar_backends})"
        )
    
    return ponderi


def main():
    parser = argparse.ArgumentParser(
        description="Echilibror de sarcină extins cu health checks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python hw_11_01.py --backends localhost:8081,localhost:8082 --weights 3,2
  python hw_11_01.py --backends localhost:8081,localhost:8082,localhost:8083 --health-interval 10
        """
    )
    
    parser.add_argument(
        '--backends', '-b',
        required=True,
        help='Backend-uri (format: host:port,host:port,...)'
    )
    parser.add_argument(
        '--weights', '--ponderi', '-w',
        default='',
        help='Ponderi pentru fiecare backend (format: 3,2,1)'
    )
    parser.add_argument(
        '--listen', '-l',
        default='0.0.0.0:8080',
        help='Adresa de ascultare (implicit: 0.0.0.0:8080)'
    )
    parser.add_argument(
        '--health-interval', '--interval',
        type=float,
        default=5.0,
        help='Interval health check în secunde (implicit: 5)'
    )
    
    args = parser.parse_args()
    
    backend_uri = parseaza_backend_uri(args.backends)
    ponderi = parseaza_ponderi(args.weights, len(backend_uri))
    host, port = args.listen.split(':')
    
    echilibror = EchilibrorPonderat(
        backend_uri,
        ponderi,
        interval_verificare=args.health_interval
    )
    echilibror.ruleaza(host, int(port))


if __name__ == '__main__':
    main()
