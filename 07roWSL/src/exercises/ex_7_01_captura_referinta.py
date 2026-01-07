#!/usr/bin/env python3
"""
Exercițiul 7.01: Captură de Referință
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu stabilește conectivitatea de referință și generează
trafic TCP/UDP pentru captura în Wireshark.

Obiective:
- Verificarea conectivității către serviciile de laborator
- Generarea traficului TCP echo pentru observarea handshake-ului
- Generarea traficului UDP pentru observarea comportamentului fără conexiune
- Salvarea unei capturi de referință pentru comparații ulterioare
"""

from __future__ import annotations

import socket
import time
from datetime import datetime


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}", flush=True)


def pauza_pentru_captura(secunde: float = 2.0):
    """Pauză pentru a permite capturarea în Wireshark."""
    print(f"  ... pauză {secunde}s pentru captură ...", flush=True)
    time.sleep(secunde)


def test_tcp_echo(host: str, port: int, mesaj: str) -> bool:
    """
    Testează conectivitatea TCP echo.
    
    Observații Wireshark:
    - Pachet SYN de la client
    - Pachet SYN-ACK de la server
    - Pachet ACK de la client (handshake complet)
    - Pachet PSH-ACK cu datele
    - Pachet ACK de confirmare
    """
    logheaza(f"Test TCP Echo: {host}:{port}")
    logheaza(f"  Mesaj: '{mesaj}'")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        
        logheaza("  Inițiere conexiune (SYN)...")
        sock.connect((host, port))
        logheaza("  Conexiune stabilită (handshake complet)")
        
        pauza_pentru_captura(1.0)
        
        logheaza(f"  Trimitere date: {len(mesaj)} octeți")
        sock.sendall(mesaj.encode())
        
        logheaza("  Așteptare răspuns...")
        raspuns = sock.recv(4096).decode()
        logheaza(f"  Răspuns primit: '{raspuns.strip()}'")
        
        pauza_pentru_captura(1.0)
        
        logheaza("  Închidere conexiune (FIN)...")
        sock.close()
        logheaza("  [OK] Test TCP reușit")
        
        return True
        
    except ConnectionRefusedError:
        logheaza("  [EROARE] Conexiune refuzată")
        return False
    except socket.timeout:
        logheaza("  [EROARE] Timeout")
        return False
    except Exception as e:
        logheaza(f"  [EROARE] {e}")
        return False


def test_udp_trimitere(host: str, port: int, mesaje: list[str]) -> bool:
    """
    Testează trimiterea UDP.
    
    Observații Wireshark:
    - Datagrame UDP individuale
    - Niciun handshake (protocol fără conexiune)
    - Nicio confirmare de primire
    """
    logheaza(f"Test UDP: {host}:{port}")
    logheaza(f"  Număr mesaje: {len(mesaje)}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for i, mesaj in enumerate(mesaje, 1):
            logheaza(f"  Trimitere datagramă #{i}: '{mesaj}'")
            sock.sendto(mesaj.encode(), (host, port))
            pauza_pentru_captura(0.5)
        
        sock.close()
        logheaza("  [OK] Datagrame UDP trimise")
        logheaza("  Notă: UDP nu garantează livrarea!")
        
        return True
        
    except Exception as e:
        logheaza(f"  [EROARE] {e}")
        return False


def main():
    """
    Funcția principală - rulează secvența de capturare de referință.
    """
    print()
    print("=" * 60)
    print("  Exercițiul 7.01: Captură de Referință")
    print("  Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    print()
    
    print("INSTRUCȚIUNI:")
    print("1. Deschideți Wireshark")
    print("2. Selectați interfața Docker corespunzătoare")
    print("3. Aplicați filtrul: tcp.port == 9090 or udp.port == 9091")
    print("4. Porniți capturarea")
    print("5. Apăsați Enter pentru a continua...")
    print()
    
    input(">>> Apăsați Enter când sunteți gata... ")
    print()
    
    # Configurare
    TCP_HOST = "localhost"
    TCP_PORT = 9090
    UDP_HOST = "localhost"
    UDP_PORT = 9091
    
    logheaza("Începere secvență de testare")
    print()
    
    # Faza 1: Test TCP
    print("-" * 40)
    logheaza("FAZA 1: Testare TCP Echo")
    print("-" * 40)
    
    mesaje_tcp = [
        "Salut de la exercitiul 7.01",
        "Test handshake TCP",
        "Mesaj final TCP"
    ]
    
    for mesaj in mesaje_tcp:
        test_tcp_echo(TCP_HOST, TCP_PORT, mesaj)
        pauza_pentru_captura(2.0)
    
    print()
    
    # Faza 2: Test UDP
    print("-" * 40)
    logheaza("FAZA 2: Testare UDP")
    print("-" * 40)
    
    mesaje_udp = [
        "Datagrama UDP #1",
        "Datagrama UDP #2",
        "Datagrama UDP #3"
    ]
    
    test_udp_trimitere(UDP_HOST, UDP_PORT, mesaje_udp)
    
    print()
    
    # Sumar
    print("=" * 60)
    logheaza("SECVENȚĂ COMPLETĂ")
    print("=" * 60)
    print()
    print("Ce să observați în Wireshark:")
    print()
    print("TCP (port 9090):")
    print("  - Handshake în trei pași: SYN → SYN-ACK → ACK")
    print("  - Transmisia datelor cu flag-uri PSH-ACK")
    print("  - Închiderea conexiunii: FIN → FIN-ACK")
    print()
    print("UDP (port 9091):")
    print("  - Datagrame individuale fără handshake")
    print("  - Nicio confirmare de primire")
    print("  - Natura 'fire-and-forget' a UDP")
    print()
    print("ACȚIUNE: Salvați captura ca 'saptamana7_ex1_referinta.pcap'")
    print("=" * 60)


if __name__ == "__main__":
    main()
