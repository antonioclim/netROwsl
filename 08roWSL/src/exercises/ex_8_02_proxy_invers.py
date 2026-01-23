#!/usr/bin/env python3
"""
EXERCIȚIUL 2: Proxy Invers cu Echilibrare Round-Robin
=====================================================
Disciplina: Rețele de Calculatoare, Săptămâna 8
Nivel: Avansat
Timp estimat: 45-60 minute

OBIECTIVE DE ÎNVĂȚARE:
- Înțelegerea conceptului de reverse proxy
- Implementarea redirecționării cererilor
- Adăugarea headers de proxy (X-Forwarded-For, Via)
- Implementarea health check pentru backend-uri

INSTRUCȚIUNI:
1. Completați funcțiile marcate cu TODO
2. Rulați testele: python3 -m pytest tests/test_ex02.py -v
3. Test manual:
   - Terminal 1: python3 -m http.server 8001 --directory www/
   - Terminal 2: python3 -m http.server 8002 --directory www/
   - Terminal 3: python3 ex_8_02_proxy_invers.py --port 8080 --backends localhost:8001,localhost:8002

EVALUARE:
- Forward corect: 30%
- Headers proxy: 30%
- Round Robin: 20%
- Health check: 20%

© Revolvix & ASE-CSIE București
"""

import socket
import argparse
import threading
import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

# =============================================================================
# CONSTANTE
# =============================================================================

CRLF = "\r\n"
DOUBLE_CRLF = "\r\n\r\n"
BUFFER_SIZE = 4096
CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 10.0


# =============================================================================
# STRUCTURI DE DATE
# =============================================================================

@dataclass
class Backend:
    """Reprezentarea unui server backend."""
    host: str
    port: int
    healthy: bool = True
    last_check: float = 0.0
    
    def __str__(self):
        status = "✓" if self.healthy else "✗"
        return f"{self.host}:{self.port} [{status}]"
    
    @property
    def address(self) -> Tuple[str, int]:
        return (self.host, self.port)


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ CLASĂ
# =============================================================================

class RoundRobinBalancer:
    """
    Load balancer cu algoritm Round Robin.
    
    FUNCȚIONARE:
    ────────────
    - Menține o listă de backend-uri
    - La fiecare apel next_backend(), returnează următorul backend sănătos
    - Ciclează prin backend-uri în ordine: 1→2→3→1→2→3...
    
    THREAD SAFETY:
    ──────────────
    - Trebuie să fie thread-safe (folosește Lock)
    - Mai multe thread-uri pot apela next_backend() simultan
    
    Exemple:
        >>> backends = [Backend("localhost", 8001), Backend("localhost", 8002)]
        >>> balancer = RoundRobinBalancer(backends)
        >>> balancer.next_backend().port
        8001
        >>> balancer.next_backend().port
        8002
        >>> balancer.next_backend().port  # revine la primul
        8001
    
    🔮 PREDICȚIE: Dacă ai 3 backend-uri și apelezi next_backend() de 7 ori,
       care va fi secvența de porturi returnate?
       Notează predicția ta înainte de implementare!
    """
    
    def __init__(self, backends: List[Backend]):
        """
        Inițializează balancer-ul cu lista de backend-uri.
        
        PAȘI DE IMPLEMENTARE:
        ─────────────────────
        1. Stochează lista de backend-uri
           self.backends = backends
        
        2. Inițializează indexul curent (începe de la 0)
           self.current_index = 0
        
        3. Creează un Lock pentru thread safety
           self.lock = threading.Lock()
        """
        # TODO: Implementează inițializarea
        # Scrie codul tău aici...
        
        raise NotImplementedError("TODO: Implementează __init__")
    
    def next_backend(self) -> Optional[Backend]:
        """
        Returnează următorul backend sănătos.
        
        Returns:
            Backend-ul selectat sau None dacă niciunul nu e sănătos
        
        PAȘI DE IMPLEMENTARE:
        ─────────────────────
        1. Obține lock-ul pentru thread safety
           with self.lock:
        
        2. Parcurge backend-urile începând de la indexul curent
           - Încearcă maximum len(backends) backend-uri
           - Caută primul care e healthy
        
        3. Dacă găsești unul healthy:
           - Actualizează indexul pentru următorul apel
           - Returnează backend-ul
        
        4. Dacă niciunul nu e healthy, returnează None
        
        ALGORITM ROUND-ROBIN:
        ─────────────────────
        ```
        tries = 0
        while tries < len(self.backends):
            backend = self.backends[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.backends)
            if backend.healthy:
                return backend
            tries += 1
        return None
        ```
        
        🔮 PREDICȚIE: Dacă backend-ul 2 din 3 e nesănătos, ce se întâmplă
           cu distribuția? (Hint: 1→3→1→3→...)
        """
        # TODO: Implementează selecția round robin
        # Scrie codul tău aici...
        
        raise NotImplementedError("TODO: Implementează next_backend")
    
    def mark_unhealthy(self, backend: Backend):
        """
        Marchează un backend ca nesănătos.
        
        Simplu: backend.healthy = False
        """
        # TODO: Implementează
        raise NotImplementedError("TODO: Implementează mark_unhealthy")
    
    def mark_healthy(self, backend: Backend):
        """
        Marchează un backend ca sănătos.
        
        Simplu: backend.healthy = True
        """
        # TODO: Implementează
        raise NotImplementedError("TODO: Implementează mark_healthy")
    
    def get_stats(self) -> Dict[str, any]:
        """
        Returnează statistici despre backend-uri.
        
        Returns:
            Dict cu: total, healthy, unhealthy, backends
        
        Exemplu return:
            {
                "total": 3,
                "healthy": 2,
                "unhealthy": 1,
                "backends": ["localhost:8001 [✓]", "localhost:8002 [✗]", ...]
            }
        """
        # TODO: Implementează statistici
        raise NotImplementedError("TODO: Implementează get_stats")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE
# =============================================================================

def add_proxy_headers(request_str: str, client_ip: str, proxy_name: str = "proxy") -> str:
    """
    Adaugă sau actualizează headers specifice proxy-ului.
    
    Args:
        request_str: Cererea HTTP ca string
        client_ip: IP-ul clientului original
        proxy_name: Numele proxy-ului pentru header Via
    
    Returns:
        Cererea modificată cu headers adăugate
    
    HEADERS DE ADĂUGAT:
    ───────────────────
    1. X-Forwarded-For: IP-ul clientului original
       - Dacă există deja, adaugă la sfârșitul listei: "ip1, ip2, ip3"
    
    2. X-Forwarded-Proto: "http" (presupunem HTTP)
    
    3. Via: "1.1 {proxy_name}"
       - Dacă există deja, adaugă la sfârșitul listei
    
    Exemple:
        >>> req = "GET / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n"
        >>> modified = add_proxy_headers(req, "192.168.1.100", "myproxy")
        >>> "X-Forwarded-For: 192.168.1.100" in modified
        True
        >>> "Via: 1.1 myproxy" in modified
        True
    
    🔮 PREDICȚIE: Dacă cererea originală are deja X-Forwarded-For: 10.0.0.1,
       cum va arăta header-ul după ce adaugi 192.168.1.100?
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Separă cererea în părți: headers vs body
       parts = request_str.split(DOUBLE_CRLF, 1)
       header_section = parts[0]
       body = parts[1] if len(parts) > 1 else ""
    
    2. Separă header_section pe linii
       lines = header_section.split(CRLF)
       request_line = lines[0]  # "GET / HTTP/1.1"
       header_lines = lines[1:]
    
    3. Parsează headers existente într-un dicționar
       headers = {}
       for line in header_lines:
           if ': ' in line:
               key, value = line.split(': ', 1)
               headers[key.lower()] = (key, value)  # păstrează case original
    
    4. Actualizează/adaugă X-Forwarded-For
       if 'x-forwarded-for' in headers:
           old_val = headers['x-forwarded-for'][1]
           new_val = f"{old_val}, {client_ip}"
       else:
           new_val = client_ip
       headers['x-forwarded-for'] = ('X-Forwarded-For', new_val)
    
    5. Similar pentru X-Forwarded-Proto și Via
    
    6. Reconstruiește cererea
    """
    
    # TODO: Implementează adăugarea headers
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează add_proxy_headers")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE
# =============================================================================

def forward_request(request: bytes, backend: Backend, client_ip: str) -> Optional[bytes]:
    """
    Trimite cererea către un backend și returnează răspunsul.
    
    Args:
        request: Cererea HTTP originală în bytes
        backend: Backend-ul țintă
        client_ip: IP-ul clientului original
    
    Returns:
        Răspunsul de la backend în bytes, sau None în caz de eroare
    
    🔮 PREDICȚIE: Ce se întâmplă dacă backend-ul nu răspunde în 5 secunde?
       Ce valoare va returna funcția?
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Decodifică cererea în string
       request_str = request.decode('utf-8', errors='replace')
    
    2. Modifică header-ul Host pentru backend
       - Găsește linia "Host: ..." și înlocuiește cu backend
       - Sau: parsează și reconstruiește
    
    3. Adaugă headers de proxy cu add_proxy_headers()
       modified_request = add_proxy_headers(request_str, client_ip)
    
    4. Creează socket TCP
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    5. Setează timeout pentru conectare și citire
       sock.settimeout(CONNECT_TIMEOUT)
    
    6. Conectează-te la backend
       sock.connect(backend.address)
    
    7. Trimite cererea modificată
       sock.sendall(modified_request.encode())
    
    8. Citește răspunsul complet (în buclă până primești tot)
       response = b""
       sock.settimeout(READ_TIMEOUT)
       while True:
           chunk = sock.recv(BUFFER_SIZE)
           if not chunk:
               break
           response += chunk
    
    9. Închide socket-ul și returnează răspunsul
    
    CAZURI DE EROARE:
    ─────────────────
    - socket.timeout → returnează None
    - ConnectionRefusedError → returnează None
    - Orice altă excepție → loghează și returnează None
    """
    
    # TODO: Implementează forwarding-ul
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează forward_request")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE
# =============================================================================

def check_backend_health(backend: Backend) -> bool:
    """
    Verifică dacă un backend este sănătos (răspunde la cereri).
    
    Args:
        backend: Backend-ul de verificat
    
    Returns:
        True dacă backend-ul răspunde, False altfel
    
    METODĂ:
    ───────
    - Trimite un request HEAD /
    - Dacă primește răspuns în timeout, e sănătos
    - Actualizează backend.last_check cu timestamp-ul curent
    
    🔮 PREDICȚIE: Dacă backend-ul e oprit, cât timp va dura funcția
       până returnează False? (Hint: verifică timeout-ul)
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Creează socket TCP
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    2. Setează timeout scurt (2 secunde)
       sock.settimeout(2.0)
    
    3. Încearcă să te conectezi la backend
       try:
           sock.connect(backend.address)
       except (socket.timeout, ConnectionRefusedError):
           return False
    
    4. Trimite cererea HEAD
       request = f"HEAD / HTTP/1.1\\r\\nHost: {backend.host}\\r\\n\\r\\n"
       sock.sendall(request.encode())
    
    5. Încearcă să citești răspuns (orice răspuns = sănătos)
       try:
           response = sock.recv(1024)
           return len(response) > 0
       except socket.timeout:
           return False
    
    6. Actualizează timestamp-ul
       backend.last_check = time.time()
    
    7. Închide socket-ul în finally block
    """
    
    # TODO: Implementează health check
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează check_backend_health")


# =============================================================================
# COD FURNIZAT - NU MODIFICA
# =============================================================================

class ReverseProxy:
    """
    Server reverse proxy.
    Cod parțial furnizat - trebuie să implementezi metodele TODO.
    """
    
    def __init__(self, host: str, port: int, backends: List[Backend]):
        self.host = host
        self.port = port
        self.balancer = RoundRobinBalancer(backends)
        self.running = False
        self.server_socket = None
        
        # Thread pentru health check
        self.health_check_interval = 30  # secunde
        self.health_thread = None
    
    def start_health_checks(self):
        """Pornește thread-ul de health check."""
        def health_loop():
            while self.running:
                for backend in self.balancer.backends:
                    is_healthy = check_backend_health(backend)
                    if is_healthy:
                        self.balancer.mark_healthy(backend)
                    else:
                        self.balancer.mark_unhealthy(backend)
                    print(f"[HEALTH] {backend}")
                time.sleep(self.health_check_interval)
        
        self.health_thread = threading.Thread(target=health_loop, daemon=True)
        self.health_thread.start()
    
    def handle_client(self, client_socket: socket.socket, client_addr: Tuple[str, int]):
        """Procesează o conexiune client."""
        client_ip = client_addr[0]
        
        try:
            request = client_socket.recv(BUFFER_SIZE)
            if not request:
                return
            
            # Selectăm backend
            backend = self.balancer.next_backend()
            if not backend:
                error_response = (
                    b"HTTP/1.1 503 Service Unavailable\r\n"
                    b"Content-Type: text/plain\r\n"
                    b"Content-Length: 23\r\n\r\n"
                    b"No backends available"
                )
                client_socket.sendall(error_response)
                return
            
            print(f"[PROXY] {client_ip} -> {backend}")
            
            # Forward request
            response = forward_request(request, backend, client_ip)
            
            if response:
                client_socket.sendall(response)
            else:
                # Backend a eșuat
                self.balancer.mark_unhealthy(backend)
                error_response = (
                    b"HTTP/1.1 502 Bad Gateway\r\n"
                    b"Content-Type: text/plain\r\n"
                    b"Content-Length: 15\r\n\r\n"
                    b"Backend failed"
                )
                client_socket.sendall(error_response)
                
        except Exception as e:
            print(f"[EROARE] {e}")
        finally:
            client_socket.close()
    
    def run(self):
        """Pornește serverul proxy."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(100)
            self.running = True
            
            print(f"[INFO] Reverse proxy pornit pe http://{self.host}:{self.port}/")
            print(f"[INFO] Backend-uri: {[str(b) for b in self.balancer.backends]}")
            print("[INFO] Apasă Ctrl+C pentru oprire")
            
            # Pornește health checks
            self.start_health_checks()
            
            while self.running:
                try:
                    client_socket, client_addr = self.server_socket.accept()
                    # Handle în thread separat
                    thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_addr),
                        daemon=True
                    )
                    thread.start()
                except socket.error:
                    break
                    
        except KeyboardInterrupt:
            print("\n[INFO] Proxy oprit de utilizator")
        finally:
            self.running = False
            if self.server_socket:
                self.server_socket.close()


def parse_backends(backends_str: str) -> List[Backend]:
    """Parsează string-ul de backend-uri."""
    backends = []
    for backend_str in backends_str.split(","):
        host, port = backend_str.strip().split(":")
        backends.append(Backend(host=host, port=int(port)))
    return backends


def main():
    parser = argparse.ArgumentParser(description="Reverse Proxy")
    parser.add_argument("--host", default="0.0.0.0", help="Adresa de bind")
    parser.add_argument("--port", type=int, default=8080, help="Portul proxy")
    parser.add_argument(
        "--backends", 
        default="localhost:8001,localhost:8002",
        help="Lista de backend-uri (host:port,host:port,...)"
    )
    
    args = parser.parse_args()
    backends = parse_backends(args.backends)
    
    proxy = ReverseProxy(args.host, args.port, backends)
    proxy.run()


if __name__ == "__main__":
    main()
