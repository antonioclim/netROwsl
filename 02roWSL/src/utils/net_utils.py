#!/usr/bin/env python3
"""
Utilitare de Rețea pentru Exerciții
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Funcții helper comune pentru programarea socket-urilor.
"""

import socket
import struct
import time
from typing import Tuple, Optional, Any


# ============================================================================
# Creare Socket-uri
# ============================================================================

def creează_socket_tcp(
    timeout: Optional[float] = None,
    reuse_addr: bool = True
) -> socket.socket:
    """
    Creează un socket TCP cu opțiuni comune.
    
    Args:
        timeout: Timeout opțional în secunde
        reuse_addr: Dacă să permită reutilizarea adresei
        
    Returns:
        Socket TCP configurat
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if reuse_addr:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    if timeout is not None:
        sock.settimeout(timeout)
    
    return sock


def creează_socket_udp(
    timeout: Optional[float] = None,
    broadcast: bool = False
) -> socket.socket:
    """
    Creează un socket UDP cu opțiuni comune.
    
    Args:
        timeout: Timeout opțional în secunde
        broadcast: Dacă să permită broadcast
        
    Returns:
        Socket UDP configurat
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    if broadcast:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    if timeout is not None:
        sock.settimeout(timeout)
    
    return sock


# ============================================================================
# Parsing și Formatare Adrese
# ============================================================================

def parsează_adresă(adresă_text: str) -> Tuple[str, int]:
    """
    Parsează o adresă în format "host:port".
    
    Args:
        adresă_text: String în format "host:port" sau doar "port"
        
    Returns:
        Tuple (host, port)
        
    Raises:
        ValueError: Dacă formatul este invalid
        
    Exemple:
        >>> parsează_adresă("localhost:8080")
        ('localhost', 8080)
        >>> parsează_adresă("8080")
        ('0.0.0.0', 8080)
    """
    if ":" in adresă_text:
        părți = adresă_text.rsplit(":", 1)
        host = părți[0]
        port = int(părți[1])
    else:
        host = "0.0.0.0"
        port = int(adresă_text)
    
    if not (0 < port < 65536):
        raise ValueError(f"Port invalid: {port}")
    
    return (host, port)


def formatează_adresă(adresă: Tuple[str, int]) -> str:
    """
    Formatează o adresă ca string.
    
    Args:
        adresă: Tuple (host, port)
        
    Returns:
        String în format "host:port"
    """
    return f"{adresă[0]}:{adresă[1]}"


# ============================================================================
# Verificare Porturi
# ============================================================================

def port_disponibil(port: int, host: str = "127.0.0.1") -> bool:
    """
    Verifică dacă un port TCP este disponibil pentru binding.
    
    Args:
        port: Numărul portului
        host: Adresa de verificat
        
    Returns:
        True dacă portul este disponibil
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.bind((host, port))
            return True
    except OSError:
        return False


def găsește_port_liber(
    start: int = 8000,
    sfârșit: int = 9000,
    host: str = "127.0.0.1"
) -> Optional[int]:
    """
    Găsește primul port liber într-un interval.
    
    Args:
        start: Începutul intervalului
        sfârșit: Sfârșitul intervalului
        host: Adresa de verificat
        
    Returns:
        Primul port disponibil sau None
    """
    for port in range(start, sfârșit + 1):
        if port_disponibil(port, host):
            return port
    return None


# ============================================================================
# Măsurare RTT
# ============================================================================

def măsoară_rtt_tcp(
    host: str,
    port: int,
    mesaj: bytes = b"ping",
    timeout: float = 5.0
) -> Optional[float]:
    """
    Măsoară round-trip time pentru o conexiune TCP.
    
    Args:
        host: Adresa serverului
        port: Portul serverului
        mesaj: Mesajul de trimis
        timeout: Timeout în secunde
        
    Returns:
        RTT în milisecunde sau None la eroare
    """
    try:
        start = time.perf_counter()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.sendall(mesaj)
            sock.recv(1024)
        
        return (time.perf_counter() - start) * 1000
    except Exception:
        return None


def măsoară_rtt_udp(
    host: str,
    port: int,
    mesaj: bytes = b"ping",
    timeout: float = 2.0
) -> Optional[float]:
    """
    Măsoară round-trip time pentru o cerere UDP.
    
    Args:
        host: Adresa serverului
        port: Portul serverului
        mesaj: Mesajul de trimis
        timeout: Timeout în secunde
        
    Returns:
        RTT în milisecunde sau None la eroare/timeout
    """
    try:
        start = time.perf_counter()
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            sock.sendto(mesaj, (host, port))
            sock.recvfrom(1024)
        
        return (time.perf_counter() - start) * 1000
    except socket.timeout:
        return None
    except Exception:
        return None


# ============================================================================
# Protocol Simplu de Framing
# ============================================================================

def trimite_cu_lungime(sock: socket.socket, date: bytes) -> None:
    """
    Trimite date prefixate cu lungimea (4 bytes, big-endian).
    
    Protocolul de framing:
    [4 bytes: lungime][N bytes: date]
    
    Args:
        sock: Socket-ul conectat
        date: Datele de trimis
    """
    lungime = len(date)
    header = struct.pack(">I", lungime)
    sock.sendall(header + date)


def primește_cu_lungime(sock: socket.socket, timeout: Optional[float] = None) -> bytes:
    """
    Primește date prefixate cu lungimea.
    
    Args:
        sock: Socket-ul conectat
        timeout: Timeout opțional
        
    Returns:
        Datele primite
        
    Raises:
        ConnectionError: Dacă conexiunea se închide prematur
    """
    if timeout:
        sock.settimeout(timeout)
    
    # Citire header (4 bytes)
    header = _primește_exact(sock, 4)
    lungime = struct.unpack(">I", header)[0]
    
    # Citire date
    return _primește_exact(sock, lungime)


def _primește_exact(sock: socket.socket, nr_bytes: int) -> bytes:
    """
    Primește exact un număr specificat de bytes.
    
    Args:
        sock: Socket-ul conectat
        nr_bytes: Numărul de bytes de primit
        
    Returns:
        Exact nr_bytes de date
        
    Raises:
        ConnectionError: Dacă conexiunea se închide prematur
    """
    date = b""
    while len(date) < nr_bytes:
        fragment = sock.recv(nr_bytes - len(date))
        if not fragment:
            raise ConnectionError("Conexiune închisă prematur")
        date += fragment
    return date


# ============================================================================
# Calcul Checksum
# ============================================================================

def calculează_checksum(date: bytes) -> int:
    """
    Calculează checksum-ul pe 16 biți (complement de 1).
    
    Similar cu checksum-ul folosit în IP/TCP/UDP.
    
    Args:
        date: Datele pentru checksum
        
    Returns:
        Valoarea checksum pe 16 biți
    """
    if len(date) % 2 == 1:
        date += b'\x00'
    
    sumă = 0
    for i in range(0, len(date), 2):
        cuvânt = (date[i] << 8) + date[i + 1]
        sumă += cuvânt
    
    # Adăugare carry
    while sumă >> 16:
        sumă = (sumă & 0xFFFF) + (sumă >> 16)
    
    # Complement de 1
    return ~sumă & 0xFFFF


def verifică_checksum(date: bytes, checksum: int) -> bool:
    """
    Verifică dacă checksum-ul este corect.
    
    Args:
        date: Datele originale
        checksum: Checksum-ul de verificat
        
    Returns:
        True dacă checksum-ul este valid
    """
    return calculează_checksum(date) == checksum


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("Test Utilitare Rețea")
    print("=" * 40)
    
    # Test parsing adresă
    print("\nParsare adresă:")
    print(f"  'localhost:8080' -> {parsează_adresă('localhost:8080')}")
    print(f"  '9090' -> {parsează_adresă('9090')}")
    
    # Test port disponibil
    print("\nVerificare porturi:")
    for port in [80, 8080, 9090, 9091]:
        stare = "disponibil" if port_disponibil(port) else "ocupat/restricționat"
        print(f"  Port {port}: {stare}")
    
    # Test găsire port liber
    port_liber = găsește_port_liber(8000, 8100)
    print(f"  Primul port liber în 8000-8100: {port_liber}")
    
    # Test checksum
    print("\nChecksum:")
    date_test = b"Test data for checksum"
    cs = calculează_checksum(date_test)
    print(f"  Date: {date_test}")
    print(f"  Checksum: {cs:04X}")
    print(f"  Verificare: {verifică_checksum(date_test, cs)}")
    
    print("\n✓ Toate testele finalizate")
