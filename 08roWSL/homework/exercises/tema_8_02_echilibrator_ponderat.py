#!/usr/bin/env python3
"""
Tema 2: Echilibrator de Încărcare cu Ponderi
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Implementați un echilibrator de încărcare weighted round-robin
cu verificare a stării de sănătate și failover automat.

Cerințe:
    1. Distribuție proporțională cu ponderile configurate
    2. Verificare periodică a sănătății backend-urilor
    3. Failover automat pentru backend-uri indisponibile
    4. Statistici de distribuție

Utilizare:
    # Porniți 3 backend-uri (în terminale separate)
    python -m http.server 8001 --directory www/
    python -m http.server 8002 --directory www/
    python -m http.server 8003 --directory www/
    
    # Porniți echilibratorul
    python tema_8_02_echilibrator_ponderat.py

Testare:
    for i in {1..18}; do curl -s http://localhost:8000/ >/dev/null; done
"""

import socket
import threading
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from urllib.request import urlopen
from urllib.error import URLError

# Configurație
PORT_ECHILIBRATOR = 8000
GAZDA_ECHILIBRATOR = "127.0.0.1"
DIMENSIUNE_BUFFER = 8192

# Interval verificare sănătate (secunde)
INTERVAL_VERIFICARE = 10
TIMEOUT_VERIFICARE = 2

# Configurație backend-uri cu ponderi
# Formatul: (gazda, port): {"pondere": N, "nume": "Nume"}
CONFIGURARE_BACKEND = {
    ("127.0.0.1", 8001): {"pondere": 5, "nume": "Primar"},
    ("127.0.0.1", 8002): {"pondere": 3, "nume": "Secundar"},
    ("127.0.0.1", 8003): {"pondere": 1, "nume": "Backup"},
}


@dataclass
class InfoBackend:
    """Informații despre un backend."""
    gazda: str
    port: int
    pondere: int
    nume: str
    sanatos: bool = True
    cereri_servite: int = 0
    erori: int = 0
    pondere_curenta: int = 0


class EchilibratorPonderat:
    """
    Echilibrator de încărcare cu algoritm weighted round-robin.
    
    Folosește algoritmul smooth weighted round-robin pentru
    distribuție mai uniformă.
    """
    
    def __init__(self, configurare: Dict):
        """
        Inițializează echilibratorul.
        
        Args:
            configurare: Dicționar cu configurația backend-urilor
        """
        self.backend_uri: List[InfoBackend] = []
        self.blocare = threading.Lock()
        self.oprire = threading.Event()
        
        for (gazda, port), config in configurare.items():
            backend = InfoBackend(
                gazda=gazda,
                port=port,
                pondere=config["pondere"],
                nume=config["nume"],
                pondere_curenta=0
            )
            self.backend_uri.append(backend)
    
    def selecteaza_backend(self) -> Optional[InfoBackend]:
        """
        TODO: Selectează următorul backend folosind smooth weighted round-robin.
        
        Algoritmul:
            1. Pentru fiecare backend sănătos:
               - pondere_curenta += pondere
            2. Selectează backend-ul cu pondere_curenta maximă
            3. Pentru backend-ul selectat:
               - pondere_curenta -= suma_ponderilor_sanatoase
            4. Returnează backend-ul selectat
        
        Returns:
            Backend-ul selectat sau None dacă niciunul nu e disponibil
        
        Indicii:
        - Folosiți blocarea pentru thread-safety
        - Ignorați backend-urile nesănătoase
        - Returnați None dacă nu există backend-uri sănătoase
        """
        # CODUL DUMNEAVOASTRĂ AICI
        with self.blocare:
            # Filtrează backend-urile sănătoase
            sanatoase = [b for b in self.backend_uri if b.sanatos]
            
            if not sanatoase:
                return None
            
            # Calculează suma ponderilor
            suma_ponderi = sum(b.pondere for b in sanatoase)
            
            # Adaugă ponderile la pondere_curenta
            for backend in sanatoase:
                backend.pondere_curenta += backend.pondere
            
            # Selectează backend-ul cu pondere_curenta maximă
            selectat = max(sanatoase, key=lambda b: b.pondere_curenta)
            
            # Scade suma ponderilor din backend-ul selectat
            selectat.pondere_curenta -= suma_ponderi
            
            # Actualizează statisticile
            selectat.cereri_servite += 1
            
            return selectat
    
    def verifica_sanatate(self, backend: InfoBackend) -> bool:
        """
        TODO: Verifică sănătatea unui backend.
        
        Args:
            backend: Backend-ul de verificat
        
        Returns:
            True dacă backend-ul este sănătos
        
        Indicii:
        - Încercați să deschideți o conexiune TCP
        - Sau trimiteți o cerere HTTP GET /
        - Folosiți timeout-ul TIMEOUT_VERIFICARE
        """
        # CODUL DUMNEAVOASTRĂ AICI
        try:
            url = f"http://{backend.gazda}:{backend.port}/"
            with urlopen(url, timeout=TIMEOUT_VERIFICARE):
                return True
        except (URLError, socket.timeout, ConnectionRefusedError):
            return False
        except Exception:
            return False
    
    def bucla_verificare_sanatate(self):
        """Verifică periodic sănătatea backend-urilor."""
        while not self.oprire.is_set():
            for backend in self.backend_uri:
                stare_veche = backend.sanatos
                backend.sanatos = self.verifica_sanatate(backend)
                
                if stare_veche != backend.sanatos:
                    stare = "SĂNĂTOS" if backend.sanatos else "NESĂNĂTOS"
                    print(f"[SĂNĂTATE] {backend.nume} ({backend.gazda}:{backend.port}): {stare}")
            
            self.oprire.wait(INTERVAL_VERIFICARE)
    
    def porneste_verificare_sanatate(self):
        """Pornește firul de verificare a sănătății."""
        fir = threading.Thread(target=self.bucla_verificare_sanatate, daemon=True)
        fir.start()
        return fir
    
    def redirectioneaza_cerere(
        self,
        cerere: bytes,
        backend: InfoBackend,
        ip_client: str
    ) -> bytes:
        """
        TODO: Redirecționează cererea către backend.
        
        Args:
            cerere: Cererea HTTP de la client
            backend: Backend-ul țintă
            ip_client: IP-ul clientului original
        
        Returns:
            Răspunsul de la backend
        
        Indicii:
        - Creați conexiune socket către backend
        - Adăugați antetul X-Forwarded-For
        - Gestionați erorile și returnați 502/503
        """
        # CODUL DUMNEAVOASTRĂ AICI
        try:
            # Creează socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            # Conectează
            sock.connect((backend.gazda, backend.port))
            
            # Adaugă antetul X-Forwarded-For
            cerere_str = cerere.decode('utf-8', errors='replace')
            linii = cerere_str.split('\r\n')
            linii.insert(1, f"X-Forwarded-For: {ip_client}")
            cerere_modificata = '\r\n'.join(linii).encode('utf-8')
            
            # Trimite cererea
            sock.sendall(cerere_modificata)
            
            # Primește răspunsul
            raspuns = b""
            while True:
                try:
                    bucata = sock.recv(DIMENSIUNE_BUFFER)
                    if not bucata:
                        break
                    raspuns += bucata
                except socket.timeout:
                    break
            
            sock.close()
            return raspuns
            
        except ConnectionRefusedError:
            backend.sanatos = False
            backend.erori += 1
            return self._raspuns_eroare(503, "Serviciu Indisponibil")
            
        except Exception as e:
            backend.erori += 1
            return self._raspuns_eroare(502, f"Bad Gateway: {e}")
    
    def _raspuns_eroare(self, cod: int, mesaj: str) -> bytes:
        """Construiește un răspuns de eroare."""
        corp = f"Eroare {cod}: {mesaj}"
        return (
            f"HTTP/1.1 {cod} {mesaj}\r\n"
            f"Content-Type: text/plain; charset=utf-8\r\n"
            f"Content-Length: {len(corp)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
            f"{corp}"
        ).encode('utf-8')
    
    def afiseaza_statistici(self):
        """Afișează statisticile de distribuție."""
        print("\n" + "=" * 50)
        print("Statistici Echilibrare")
        print("=" * 50)
        
        total = sum(b.cereri_servite for b in self.backend_uri)
        
        for backend in self.backend_uri:
            stare = "✓" if backend.sanatos else "✗"
            procent = (backend.cereri_servite / total * 100) if total > 0 else 0
            print(f"  {stare} {backend.nume} (:{backend.port})")
            print(f"    Pondere: {backend.pondere}")
            print(f"    Cereri:  {backend.cereri_servite} ({procent:.1f}%)")
            print(f"    Erori:   {backend.erori}")
        
        print("=" * 50)


def gestioneaza_client(
    socket_client: socket.socket,
    adresa: tuple,
    echilibrator: EchilibratorPonderat
):
    """Gestionează conexiunea unui client."""
    try:
        cerere = socket_client.recv(DIMENSIUNE_BUFFER)
        
        if not cerere:
            return
        
        # Selectează backend
        backend = echilibrator.selecteaza_backend()
        
        if backend is None:
            # Niciun backend disponibil
            raspuns = echilibrator._raspuns_eroare(503, "Toate backend-urile sunt indisponibile")
            socket_client.sendall(raspuns)
            print(f"[PROXY] {adresa[0]}:{adresa[1]} -> Niciun backend disponibil")
            return
        
        print(f"[PROXY] {adresa[0]}:{adresa[1]} -> {backend.nume} (:{backend.port})")
        
        # Redirecționează cererea
        raspuns = echilibrator.redirectioneaza_cerere(cerere, backend, adresa[0])
        socket_client.sendall(raspuns)
        
    except Exception as e:
        print(f"[EROARE] {adresa[0]}:{adresa[1]} - {e}")
    finally:
        socket_client.close()


def main():
    """Funcția principală."""
    print("=" * 60)
    print("Echilibrator de Încărcare cu Ponderi - Tema 2")
    print("Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 60)
    print()
    
    # Creează echilibratorul
    echilibrator = EchilibratorPonderat(CONFIGURARE_BACKEND)
    
    print("Backend-uri configurate:")
    for backend in echilibrator.backend_uri:
        print(f"  - {backend.nume}: {backend.gazda}:{backend.port} (pondere: {backend.pondere})")
    print()
    
    # Pornește verificarea sănătății
    echilibrator.porneste_verificare_sanatate()
    print(f"[INFO] Verificare sănătate pornită (interval: {INTERVAL_VERIFICARE}s)")
    
    # Creează socket-ul
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        socket_server.bind((GAZDA_ECHILIBRATOR, PORT_ECHILIBRATOR))
        socket_server.listen(100)
        
        print(f"[INFO] Echilibrator pornit pe http://{GAZDA_ECHILIBRATOR}:{PORT_ECHILIBRATOR}/")
        print()
        print("Apăsați Ctrl+C pentru a opri și a vedea statisticile")
        print("-" * 60)
        
        while True:
            socket_client, adresa = socket_server.accept()
            
            fir = threading.Thread(
                target=gestioneaza_client,
                args=(socket_client, adresa, echilibrator)
            )
            fir.start()
            
    except KeyboardInterrupt:
        print("\n[INFO] Oprire echilibrator...")
        echilibrator.oprire.set()
        echilibrator.afiseaza_statistici()
    finally:
        socket_server.close()
        print("[INFO] Echilibrator oprit")


if __name__ == "__main__":
    main()
