#!/usr/bin/env python3
"""
TEMA 2: Echilibrator de Încărcare cu Ponderi
============================================
Disciplina: Rețele de Calculatoare, Săptămâna 8
Nivel: Avansat
Timp estimat: 120-150 minute
Punctaj: 100 puncte

OBIECTIVE DE ÎNVĂȚARE:
- Implementarea algoritmului Smooth Weighted Round-Robin
- Gestionarea health check pentru backend-uri
- Implementarea failover automat

CERINȚE:
1. Algoritm weighted round-robin (35 puncte)
2. Verificare periodică sănătate (25 puncte)
3. Failover automat (20 puncte)
4. Statistici și logging (10 puncte)
5. Calitatea codului (10 puncte)

TESTARE:
    # Pornește 3 backend-uri simple
    python3 -m http.server 8001 --directory ../www/ &
    python3 -m http.server 8002 --directory ../www/ &
    python3 -m http.server 8003 --directory ../www/ &
    
    # Pornește echilibratorul
    python3 tema_8_02_echilibrator_ponderat.py
    
    # Testează distribuția
    for i in {1..18}; do curl -s http://localhost:8000/; done

© Revolvix & ASE-CSIE București
"""

import socket
import threading
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

# =============================================================================
# CONFIGURAȚIE
# =============================================================================

CONFIGURATIE_BACKEND = {
    ("127.0.0.1", 8001): {"weight": 5, "name": "Primary"},
    ("127.0.0.1", 8002): {"weight": 3, "name": "Secondary"},
    ("127.0.0.1", 8003): {"weight": 1, "name": "Backup"},
}

PORT_ECHILIBRATOR = 8000
GAZDA = "0.0.0.0"
DIMENSIUNE_BUFFER = 4096
TIMEOUT_CONEXIUNE = 5.0
INTERVAL_HEALTH_CHECK = 10  # secunde


# =============================================================================
# STRUCTURI DE DATE
# =============================================================================

@dataclass
class Backend:
    """
    Reprezentarea unui server backend cu statistici.
    
    🔮 PREDICȚIE: De ce avem nevoie de `current_weight` separat de `weight`?
       Hint: gândește-te la Smooth Weighted Round-Robin.
    """
    host: str
    port: int
    weight: int = 1                    # Ponderea configurată (nu se schimbă)
    name: str = "unnamed"
    
    # Stare dinamică
    healthy: bool = True
    current_weight: int = 0            # Ponderea curentă (se modifică la fiecare selecție)
    
    # Statistici
    cereri_totale: int = 0
    cereri_reușite: int = 0
    cereri_eșuate: int = 0
    timp_total_răspuns: float = 0.0
    ultima_verificare: float = field(default_factory=time.time)
    
    @property
    def address(self) -> Tuple[str, int]:
        return (self.host, self.port)
    
    @property
    def timp_mediu_răspuns(self) -> float:
        if self.cereri_reușite == 0:
            return 0.0
        return self.timp_total_răspuns / self.cereri_reușite
    
    @property
    def rată_succes(self) -> float:
        if self.cereri_totale == 0:
            return 100.0
        return (self.cereri_reușite / self.cereri_totale) * 100
    
    def __str__(self):
        status = "✓" if self.healthy else "✗"
        return f"{self.name}({self.host}:{self.port}) [{status}] w={self.weight}"


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ CLASĂ (35 puncte)
# =============================================================================

class SmoothWeightedRoundRobin:
    """
    Implementare Smooth Weighted Round-Robin.
    
    ALGORITMUL:
    ───────────
    La fiecare selecție:
    1. Pentru fiecare backend sănătos: current_weight += weight
    2. Selectează backend-ul cu current_weight maxim
    3. Scade total_weight din current_weight al backend-ului selectat
    
    EXEMPLU (ponderi 5:3:1, total=9):
    ─────────────────────────────────
    
    | Pas | Înainte (+weight)    | Selectat | După (-total)        |
    |-----|----------------------|----------|----------------------|
    |  1  | A=5, B=3, C=1        | A (max)  | A=-4, B=3, C=1       |
    |  2  | A=1, B=6, C=2        | B (max)  | A=1, B=-3, C=2       |
    |  3  | A=6, B=0, C=3        | A (max)  | A=-3, B=0, C=3       |
    |  4  | A=2, B=3, C=4        | C (max)  | A=2, B=3, C=-5       |
    |  5  | A=7, B=6, C=-4       | A (max)  | A=-2, B=6, C=-4      |
    |  6  | A=3, B=9, C=-3       | B (max)  | A=3, B=0, C=-3       |
    |  ...| ...                  | ...      | ...                  |
    
    Secvența pentru 9 cereri: A,B,A,C,A,B,A,B,A (5×A, 3×B, 1×C)
    
    🔮 PREDICȚIE: De ce acest algoritm e "smooth"? 
       Compară cu round-robin simplu: A,A,A,A,A,B,B,B,C
       Care distribuie mai uniform în timp?
    """
    
    def __init__(self, backends: List[Backend]):
        """
        Inițializează balancer-ul.
        
        PAȘI:
        1. Stochează lista de backend-uri
        2. Creează Lock pentru thread safety
        3. Inițializează current_weight la 0 pentru toate
        """
        # TODO: Implementează inițializarea
        # Scrie codul tău aici...
        
        raise NotImplementedError("TODO: Implementează __init__")
    
    @property
    def total_weight(self) -> int:
        """Calculează suma ponderilor backend-urilor sănătoase."""
        # TODO: Implementează
        raise NotImplementedError("TODO: Implementează total_weight")
    
    def next_backend(self) -> Optional[Backend]:
        """
        Selectează următorul backend folosind Smooth Weighted Round-Robin.
        
        Returns:
            Backend-ul selectat sau None dacă niciunul nu e sănătos
        
        🔮 PREDICȚIE: Dacă toate backend-urile au aceeași pondere,
           algoritmul se comportă exact ca round-robin simplu?
        
        PAȘI DE IMPLEMENTARE:
        ─────────────────────
        1. Obține lock-ul
           with self.lock:
        
        2. Filtrează backend-urile sănătoase
           healthy = [b for b in self.backends if b.healthy]
           if not healthy:
               return None
        
        3. Crește current_weight pentru toate
           for backend in healthy:
               backend.current_weight += backend.weight
        
        4. Găsește backend-ul cu current_weight maxim
           selected = max(healthy, key=lambda b: b.current_weight)
        
        5. Scade total_weight din selected.current_weight
           selected.current_weight -= total_weight
        
        6. Returnează backend-ul selectat
        """
        # TODO: Implementează selecția SWRR
        # Scrie codul tău aici...
        
        raise NotImplementedError("TODO: Implementează next_backend")
    
    def get_stats(self) -> Dict:
        """
        Returnează statistici complete despre backend-uri.
        
        Returns:
            Dict cu: total, healthy, unhealthy, backends details
        """
        # TODO: Implementează
        raise NotImplementedError("TODO: Implementează get_stats")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE (25 puncte)
# =============================================================================

def verifica_sanatate(backend: Backend) -> bool:
    """
    Verifică dacă un backend răspunde la cereri.
    
    Args:
        backend: Backend-ul de verificat
    
    Returns:
        True dacă răspunde, False altfel
    
    🔮 PREDICȚIE: De ce folosim HEAD în loc de GET pentru health check?
       Hint: gândește-te la bandwidth și overhead.
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Creează socket TCP
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    2. Setează timeout scurt (2 secunde e suficient)
       sock.settimeout(2.0)
    
    3. Încearcă conectarea
       try:
           sock.connect(backend.address)
       except (socket.timeout, ConnectionRefusedError, OSError):
           return False
    
    4. Trimite cererea HEAD
       cerere = f"HEAD /health HTTP/1.1\\r\\nHost: {backend.host}\\r\\n\\r\\n"
       sock.sendall(cerere.encode())
    
    5. Așteaptă răspuns (orice răspuns = sănătos)
       try:
           raspuns = sock.recv(1024)
           return len(raspuns) > 0
       except socket.timeout:
           return False
    
    6. Actualizează timestamp-ul verificării
       backend.ultima_verificare = time.time()
    
    7. Închide socket-ul în finally
    
    GREȘELI COMUNE:
    ───────────────
    ✗ Timeout prea lung (blochează alte verificări)
    ✗ Neînchiderea socket-ului în caz de eroare
    ✗ Neactualizarea timestamp-ului
    """
    
    # TODO: Implementează health check
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează verifica_sanatate")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE (20 puncte parțial)
# =============================================================================

def trimite_catre_backend(cerere: bytes, backend: Backend) -> Optional[bytes]:
    """
    Trimite cererea către un backend și returnează răspunsul.
    
    Args:
        cerere: Cererea HTTP în bytes
        backend: Backend-ul destinație
    
    Returns:
        Răspunsul de la backend sau None în caz de eroare
    
    🔮 PREDICȚIE: Ce se întâmplă dacă backend-ul răspunde foarte lent
       (peste timeout)? Cum afectează asta statisticile?
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Înregistrează timpul de start
       timp_start = time.time()
    
    2. Creează socket și setează timeout
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sock.settimeout(TIMEOUT_CONEXIUNE)
    
    3. Conectează-te la backend
    
    4. Trimite cererea
       sock.sendall(cerere)
    
    5. Citește răspunsul complet
       raspuns = b""
       while True:
           chunk = sock.recv(DIMENSIUNE_BUFFER)
           if not chunk:
               break
           raspuns += chunk
    
    6. Actualizează statisticile backend-ului
       backend.cereri_totale += 1
       if raspuns:
           backend.cereri_reușite += 1
           backend.timp_total_răspuns += time.time() - timp_start
       else:
           backend.cereri_eșuate += 1
    
    7. Returnează răspunsul
    
    GREȘELI COMUNE:
    ───────────────
    ✗ Neactualizarea statisticilor în cazul erorilor
    ✗ Citirea unui singur chunk în loc de tot răspunsul
    ✗ Timeout prea scurt pentru răspunsuri mari
    """
    
    # TODO: Implementează forwarding-ul
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează trimite_catre_backend")


# =============================================================================
# COD FURNIZAT - POȚI MODIFICA
# =============================================================================

class EchilibratorIncărcare:
    """
    Server principal de echilibrare a încărcării.
    
    Cod parțial furnizat.
    """
    
    def __init__(self, host: str, port: int, backends: List[Backend]):
        self.host = host
        self.port = port
        self.balancer = SmoothWeightedRoundRobin(backends)
        self.running = False
        self.socket_server = None
    
    def porneste_verificari_sanatate(self):
        """Pornește thread-ul de health check."""
        def bucla_verificare():
            while self.running:
                for backend in self.balancer.backends:
                    era_sanatos = backend.healthy
                    backend.healthy = verifica_sanatate(backend)
                    
                    # Loghează schimbările de stare
                    if era_sanatos and not backend.healthy:
                        print(f"[HEALTH] ⚠️  {backend.name} a devenit NESĂNĂTOS")
                    elif not era_sanatos and backend.healthy:
                        print(f"[HEALTH] ✅ {backend.name} a revenit SĂNĂTOS")
                
                time.sleep(INTERVAL_HEALTH_CHECK)
        
        thread = threading.Thread(target=bucla_verificare, daemon=True)
        thread.start()
    
    def gestioneaza_client(self, socket_client: socket.socket, adresa: Tuple[str, int]):
        """Procesează o conexiune client."""
        try:
            cerere = socket_client.recv(DIMENSIUNE_BUFFER)
            if not cerere:
                return
            
            # Selectează backend
            backend = self.balancer.next_backend()
            
            if backend is None:
                raspuns = (
                    b"HTTP/1.1 503 Service Unavailable\r\n"
                    b"Content-Type: text/plain\r\n"
                    b"Content-Length: 26\r\n\r\n"
                    b"Nu sunt backend-uri active"
                )
                socket_client.sendall(raspuns)
                return
            
            print(f"[PROXY] {adresa[0]} → {backend.name}")
            
            # Trimite către backend
            raspuns = trimite_catre_backend(cerere, backend)
            
            if raspuns:
                socket_client.sendall(raspuns)
            else:
                # Backend a eșuat - marchează ca nesănătos
                backend.healthy = False
                print(f"[EROARE] {backend.name} a eșuat, marcat ca nesănătos")
                
                raspuns = (
                    b"HTTP/1.1 502 Bad Gateway\r\n"
                    b"Content-Type: text/plain\r\n"
                    b"Content-Length: 15\r\n\r\n"
                    b"Backend eșuat"
                )
                socket_client.sendall(raspuns)
                
        except Exception as e:
            print(f"[EROARE] {e}")
        finally:
            socket_client.close()
    
    def afiseaza_statistici(self):
        """Afișează statistici periodic."""
        def bucla_statistici():
            while self.running:
                time.sleep(30)
                print("\n" + "=" * 50)
                print("STATISTICI BACKEND-URI")
                print("=" * 50)
                for backend in self.balancer.backends:
                    status = "✓" if backend.healthy else "✗"
                    print(f"  {backend.name} [{status}]")
                    print(f"    Cereri: {backend.cereri_totale}")
                    print(f"    Succes: {backend.rată_succes:.1f}%")
                    print(f"    Timp mediu: {backend.timp_mediu_răspuns*1000:.1f}ms")
                print("=" * 50 + "\n")
        
        thread = threading.Thread(target=bucla_statistici, daemon=True)
        thread.start()
    
    def run(self):
        """Pornește echilibratorul."""
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket_server.bind((self.host, self.port))
            self.socket_server.listen(100)
            self.running = True
            
            print("=" * 60)
            print("Echilibrator de Încărcare - Tema 2")
            print("=" * 60)
            print(f"Ascultă pe http://{self.host}:{self.port}/")
            print("Backend-uri configurate:")
            for backend in self.balancer.backends:
                print(f"  - {backend}")
            print("-" * 60)
            print("Apăsați Ctrl+C pentru oprire")
            print()
            
            # Pornește thread-urile auxiliare
            self.porneste_verificari_sanatate()
            self.afiseaza_statistici()
            
            while self.running:
                try:
                    socket_client, adresa = self.socket_server.accept()
                    thread = threading.Thread(
                        target=self.gestioneaza_client,
                        args=(socket_client, adresa),
                        daemon=True
                    )
                    thread.start()
                except socket.error:
                    break
                    
        except KeyboardInterrupt:
            print("\n[INFO] Oprire echilibrator...")
        finally:
            self.running = False
            if self.socket_server:
                self.socket_server.close()


# =============================================================================
# FUNCȚIA PRINCIPALĂ
# =============================================================================

def main():
    """Funcția principală."""
    # Creează lista de backend-uri din configurație
    backends = []
    for (host, port), config in CONFIGURATIE_BACKEND.items():
        backend = Backend(
            host=host,
            port=port,
            weight=config.get("weight", 1),
            name=config.get("name", f"{host}:{port}")
        )
        backends.append(backend)
    
    # Pornește echilibratorul
    echilibrator = EchilibratorIncărcare(GAZDA, PORT_ECHILIBRATOR, backends)
    echilibrator.run()


if __name__ == "__main__":
    main()
