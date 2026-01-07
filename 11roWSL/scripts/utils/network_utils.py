#!/usr/bin/env python3
"""
Utilitare de Rețea
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Oferă funcții pentru testarea și benchmark-ul serviciilor de rețea.
"""

import socket
import time
import threading
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class RaspunsHTTP:
    """Reprezintă un răspuns HTTP."""
    status: int
    headers: dict
    body: str
    latenta_ms: float


def http_get(url: str, timeout: float = 5.0) -> RaspunsHTTP:
    """
    Execută o cerere HTTP GET simplă.
    
    Args:
        url: URL-ul de accesat
        timeout: Timeout în secunde
    
    Returns:
        Obiect RaspunsHTTP cu răspunsul
    """
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 80
    path = parsed.path or "/"
    if parsed.query:
        path += f"?{parsed.query}"
    
    timp_start = time.time()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect((host, port))
        
        # Construiește cererea HTTP
        cerere = f"GET {path} HTTP/1.1\r\n"
        cerere += f"Host: {host}\r\n"
        cerere += "Connection: close\r\n"
        cerere += "\r\n"
        
        s.sendall(cerere.encode())
        
        # Primește răspunsul
        raspuns = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            raspuns += chunk
    
    latenta_ms = (time.time() - timp_start) * 1000
    
    # Parsează răspunsul
    raspuns_text = raspuns.decode('utf-8', errors='ignore')
    parti = raspuns_text.split('\r\n\r\n', 1)
    header_text = parti[0]
    body = parti[1] if len(parti) > 1 else ""
    
    # Parsează headerele
    linii = header_text.split('\r\n')
    linie_status = linii[0]
    status = int(linie_status.split()[1])
    
    headers = {}
    for linie in linii[1:]:
        if ':' in linie:
            cheie, valoare = linie.split(':', 1)
            headers[cheie.strip()] = valoare.strip()
    
    return RaspunsHTTP(
        status=status,
        headers=headers,
        body=body,
        latenta_ms=latenta_ms
    )


def testeaza_echilibror_sarcina(
    url: str, 
    numar_cereri: int = 10
) -> dict[str, int]:
    """
    Testează distribuția echilibrului de sarcină.
    
    Args:
        url: URL-ul echilibrului
        numar_cereri: Numărul de cereri de trimis
    
    Returns:
        Dicționar cu distribuția pe backend-uri
    """
    distributie = {}
    
    for _ in range(numar_cereri):
        try:
            raspuns = http_get(url)
            
            if raspuns.status == 200:
                # Detectează backend-ul din conținut sau headere
                backend = "necunoscut"
                
                # Verifică headerele
                for header in ['x-backend-id', 'x-served-by']:
                    if header in raspuns.headers:
                        backend = raspuns.headers[header]
                        break
                
                # Verifică conținutul
                if backend == "necunoscut":
                    continut = raspuns.body.lower()
                    for i in range(1, 10):
                        if f"web{i}" in continut or f"backend {i}" in continut:
                            backend = f"backend_{i}"
                            break
                
                distributie[backend] = distributie.get(backend, 0) + 1
                
        except Exception:
            distributie["eroare"] = distributie.get("eroare", 0) + 1
        
        time.sleep(0.05)  # Pauză scurtă între cereri
    
    return distributie


def _worker_cerere(url: str, timeout: float) -> tuple[int, float]:
    """
    Worker pentru o singură cerere (folosit în benchmark).
    
    Returns:
        Tuple (cod_status, latenta_ms)
    """
    try:
        raspuns = http_get(url, timeout)
        return (raspuns.status, raspuns.latenta_ms)
    except Exception:
        return (0, 0.0)


def benchmark_endpoint(
    url: str,
    numar_cereri: int = 100,
    concurenta: int = 10,
    timeout: float = 10.0
) -> dict:
    """
    Execută benchmark pe un endpoint.
    
    Args:
        url: URL-ul de testat
        numar_cereri: Numărul total de cereri
        concurenta: Numărul de cereri concurente
        timeout: Timeout per cerere
    
    Returns:
        Dicționar cu metricile de performanță
    """
    latente = []
    statusuri = {}
    
    timp_start = time.time()
    
    with ThreadPoolExecutor(max_workers=concurenta) as executor:
        futures = [
            executor.submit(_worker_cerere, url, timeout)
            for _ in range(numar_cereri)
        ]
        
        for future in as_completed(futures):
            status, latenta = future.result()
            statusuri[status] = statusuri.get(status, 0) + 1
            if latenta > 0:
                latente.append(latenta)
    
    durata = time.time() - timp_start
    
    # Calculează percentilele
    latente.sort()
    
    def percentila(p: float) -> float:
        if not latente:
            return 0.0
        index = int(len(latente) * p / 100)
        index = min(index, len(latente) - 1)
        return latente[index]
    
    return {
        "total_cereri": numar_cereri,
        "cereri_reusite": sum(c for s, c in statusuri.items() if 200 <= s < 300),
        "durata_secunde": durata,
        "cereri_pe_secunda": numar_cereri / durata if durata > 0 else 0,
        "distributie_statusuri": statusuri,
        "latenta_p50_ms": percentila(50),
        "latenta_p90_ms": percentila(90),
        "latenta_p95_ms": percentila(95),
        "latenta_p99_ms": percentila(99),
    }


def verifica_port_disponibil(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Verifică dacă un port este deschis și acceptă conexiuni.
    
    Args:
        host: Adresa gazdei
        port: Numărul portului
        timeout: Timeout în secunde
    
    Returns:
        True dacă portul răspunde
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
