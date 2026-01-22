#!/usr/bin/env python3
"""
Exercițiu 1: Client Protocol TEXT
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Implementați un client simplu pentru protocolul TEXT care poate
    trimite comenzi și primi răspunsuri de la server.

ÎNAINTE DE A ÎNCEPE — Răspunde mental:
======================================
1. Ce tip de socket folosești pentru TCP? (SOCK_STREAM sau SOCK_DGRAM?)
2. Ce excepție primești dacă serverul nu rulează când apelezi connect()?
3. Pentru mesajul "PING", care e formatul complet conform protocolului TEXT?
4. recv(1024) returnează exact 1024 bytes? De ce da/nu?

Notează răspunsurile și verifică-le după ce termini exercițiul.

INSTRUCȚIUNI:
    1. Completați funcțiile marcate cu TODO
    2. Testați cu serverul din container: localhost:5400
    3. Observați traficul în Wireshark

PROTOCOL TEXT:
    Format mesaj: <LUNGIME> <COMANDĂ> [ARGUMENTE]
    Exemple:
        - "4 PING" (lungime=4 pentru "PING")
        - "13 SET cheie val" (lungime=13 pentru "SET cheie val")

PUNCTAJ: 10 puncte
"""

import socket
from typing import Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE
# Scop: Parametrii de conexiune la server
# ═══════════════════════════════════════════════════════════════════════════════

SERVER_HOST = 'localhost'
SERVER_PORT = 5400
TIMEOUT = 5.0  # secunde


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_PROTOCOL
# Scop: Formatare și parsare mesaje conform protocolului TEXT
# Transferabil la: Orice protocol bazat pe prefix de lungime
# ═══════════════════════════════════════════════════════════════════════════════

def formateaza_mesaj(comanda: str) -> str:
    """
    Formatează o comandă conform protocolului TEXT.
    
    PREDICȚIE: 
    - Pentru comanda "PING", ce string va returna această funcție?
    - Pentru "SET a b", care e lungimea corectă?
    
    Protocol: <LUNGIME> <COMANDĂ>
    Exemplu: "PING" -> "4 PING"
    
    Args:
        comanda: Comanda de formatat (ex: "PING", "SET cheie valoare")
    
    Returns:
        Mesajul formatat cu prefix de lungime
    """
    # TODO: Implementați formatarea mesajului
    # Indiciu: lungime = len(comanda), apoi returnați f"{lungime} {comanda}"
    pass


def parseaza_raspuns(raspuns: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Parsează un răspuns de la server.
    
    PREDICȚIE:
    - Dacă serverul trimite "4 PONG", ce va returna această funcție?
    - Ce se întâmplă dacă răspunsul e malformat?
    
    Args:
        raspuns: Răspunsul brut de la server
    
    Returns:
        Tuple (lungime, continut) sau (None, None) dacă invalid
    """
    # TODO: Implementați parsarea răspunsului
    # Indiciu:
    # 1. Împărțiți string-ul la primul spațiu: parts = raspuns.split(' ', 1)
    # 2. Primul element e lungimea, al doilea e conținutul
    # 3. Returnați (int(lungime), continut)
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_REȚEA
# Scop: Comunicare cu serverul prin socket TCP
# Transferabil la: Orice client TCP simplu
# ═══════════════════════════════════════════════════════════════════════════════

def trimite_comanda(sock: socket.socket, comanda: str) -> Optional[str]:
    """
    Trimite o comandă și primește răspunsul.
    
    PREDICȚIE:
    - Ce se întâmplă dacă serverul închide conexiunea înainte de recv()?
    - send() vs sendall() - care garantează trimiterea completă?
    
    Args:
        sock: Socket-ul conectat
        comanda: Comanda de trimis
    
    Returns:
        Răspunsul de la server sau None dacă a eșuat
    """
    # TODO: Implementați trimiterea și recepția
    # Indiciu:
    # 1. Formatați mesajul cu formateaza_mesaj()
    # 2. Trimiteți cu sock.sendall(mesaj.encode())
    # 3. Primiți răspunsul cu sock.recv(4096)
    # 4. Decodați și returnați: raspuns.decode().strip()
    pass


def conecteaza() -> Optional[socket.socket]:
    """
    Creează și conectează un socket la server.
    
    PREDICȚIE:
    - În ce ordine apelezi socket(), settimeout(), connect()?
    - Ce excepție primești pentru timeout? Pentru server inexistent?
    
    Returns:
        Socket-ul conectat sau None dacă a eșuat
    """
    # TODO: Implementați conectarea
    # Indiciu:
    # 1. Creați socket: socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. Setați timeout: sock.settimeout(TIMEOUT)
    # 3. Conectați: sock.connect((SERVER_HOST, SERVER_PORT))
    # 4. Gestionați excepțiile: socket.timeout, ConnectionRefusedError
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRAM_PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Demonstrează utilizarea clientului TEXT."""
    print("=" * 50)
    print("Client Protocol TEXT")
    print("=" * 50)
    
    # Conectare
    print("\n1. Conectare la server...")
    sock = conecteaza()
    if sock is None:
        print("   EROARE: Nu s-a putut conecta!")
        print("   Verificați că laboratorul e pornit:")
        print("   python3 scripts/start_lab.py")
        return
    print("   Conectat cu succes!")
    
    try:
        # Test PING
        print("\n2. Test PING...")
        raspuns = trimite_comanda(sock, "PING")
        if raspuns:
            lungime, continut = parseaza_raspuns(raspuns)
            print(f"   Trimis: 4 PING")
            print(f"   Primit: {raspuns}")
            print(f"   Parsat: lungime={lungime}, continut={continut}")
        
        # Test SET
        print("\n3. Test SET...")
        raspuns = trimite_comanda(sock, "SET cheie valoare_test")
        if raspuns:
            print(f"   Trimis: SET cheie valoare_test")
            print(f"   Primit: {raspuns}")
        
        # Test GET
        print("\n4. Test GET...")
        raspuns = trimite_comanda(sock, "GET cheie")
        if raspuns:
            print(f"   Trimis: GET cheie")
            print(f"   Primit: {raspuns}")
        
        # Test COUNT
        print("\n5. Test COUNT...")
        raspuns = trimite_comanda(sock, "COUNT")
        if raspuns:
            print(f"   Trimis: COUNT")
            print(f"   Primit: {raspuns}")
        
        # Test DEL
        print("\n6. Test DEL...")
        raspuns = trimite_comanda(sock, "DEL cheie")
        if raspuns:
            print(f"   Trimis: DEL cheie")
            print(f"   Primit: {raspuns}")
        
        # Test QUIT
        print("\n7. Test QUIT...")
        raspuns = trimite_comanda(sock, "QUIT")
        if raspuns:
            print(f"   Trimis: QUIT")
            print(f"   Primit: {raspuns}")
    
    finally:
        # Închide conexiunea
        sock.close()
        print("\n8. Conexiune închisă.")
    
    print("\n" + "=" * 50)
    print("Test complet!")
    print("=" * 50)
    
    # Verificare răspunsuri predicție
    print("\n" + "-" * 50)
    print("VERIFICARE PREDICȚII:")
    print("-" * 50)
    print("1. TCP folosește SOCK_STREAM (UDP ar fi SOCK_DGRAM)")
    print("2. ConnectionRefusedError dacă serverul nu rulează")
    print("3. Format corect: '4 PING' (lungime spațiu comandă)")
    print("4. recv() returnează PÂNĂ LA 1024 bytes, poate fi mai puțin!")


if __name__ == "__main__":
    main()
