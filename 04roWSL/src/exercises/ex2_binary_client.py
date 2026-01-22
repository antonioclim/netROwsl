#!/usr/bin/env python3
"""
Exercițiu 2: Client Protocol BINAR
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Implementați un client pentru protocolul BINAR cu antet fix
    și verificare CRC32.

ÎNAINTE DE A ÎNCEPE — Răspunde mental:
======================================
1. Câți bytes are antetul protocolului BINAR? (hint: vezi theory_summary.md)
2. Ce înseamnă '!' în struct.pack('!I', valoare)? De ce e important?
3. CRC32 se calculează peste ce date exact? (antet complet sau parțial?)
4. Ce valoare returnează binascii.crc32(b"123456789")? (verifică-ți implementarea!)

Notează răspunsurile și verifică-le după ce termini exercițiul.

INSTRUCȚIUNI:
    1. Completați funcțiile marcate cu TODO
    2. Respectați structura antetului din documentație
    3. Testați cu serverul din container: localhost:5401
    4. Capturați traficul în Wireshark și verificați structura

STRUCTURA ANTETULUI (14 bytes):
    | Offset | Lungime | Câmp      | Format      |
    |--------|---------|-----------|-------------|
    | 0-1    | 2       | Magic     | bytes "NP"  |
    | 2      | 1       | Versiune  | uint8       |
    | 3      | 1       | Tip       | uint8       |
    | 4-5    | 2       | Lungime   | uint16 BE   |
    | 6-9    | 4       | Secvență  | uint32 BE   |
    | 10-13  | 4       | CRC32     | uint32 BE   |

    BE = Big-Endian (Network Byte Order)

PUNCTAJ: 15 puncte
"""

import socket
import struct
import binascii
from typing import Optional, Tuple, Dict, Any
from enum import IntEnum


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# Scop: Definește valorile fixe ale protocolului BINAR
# Transferabil la: Orice implementare de protocol cu antet fix
# ═══════════════════════════════════════════════════════════════════════════════

BINAR_MAGIC = b'NP'
BINAR_VERSIUNE = 1
BINAR_DIMENSIUNE_ANTET = 14

SERVER_HOST = 'localhost'
SERVER_PORT = 5401
TIMEOUT = 5.0


class TipMesaj(IntEnum):
    """Tipurile de mesaje ale protocolului BINAR."""
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_CRC
# Scop: Calculul și verificarea CRC32
# Transferabil la: Orice protocol care necesită verificare integritate
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc32(date: bytes) -> int:
    """
    Calculează CRC32 pentru un șir de bytes.
    
    PREDICȚIE:
    - Pentru b"123456789", CRC32 trebuie să fie 0xCBF43926
    - De ce folosim `& 0xFFFFFFFF`?
    
    Args:
        date: Datele pentru care se calculează CRC
    
    Returns:
        Valoarea CRC32 ca întreg pozitiv pe 32 de biți
    """
    # TODO: Implementați calculul CRC32
    # Indiciu: binascii.crc32(date) & 0xFFFFFFFF
    pass


def verifica_crc_cunoscut():
    """Verifică implementarea CRC32 cu o valoare cunoscută."""
    crc = calculeaza_crc32(b"123456789")
    asteptat = 0xCBF43926
    if crc == asteptat:
        print(f"✓ CRC32 corect: 0x{crc:08X}")
        return True
    else:
        print(f"✗ CRC32 greșit: 0x{crc:08X} (așteptat 0x{asteptat:08X})")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_PROTOCOL
# Scop: Construcție și parsare mesaje BINAR
# Transferabil la: Orice protocol cu antet binar de dimensiune fixă
# ═══════════════════════════════════════════════════════════════════════════════

def construieste_mesaj(tip: TipMesaj, payload: bytes, secventa: int) -> bytes:
    """
    Construiește un mesaj BINAR complet.
    
    PREDICȚIE:
    - Pentru un PING (payload gol), câți bytes va avea mesajul final?
    - În ce ordine trebuie să apară câmpurile în struct.pack?
    - Ce se întâmplă dacă uiți '!' din format string?
    
    Args:
        tip: Tipul mesajului (din enum TipMesaj)
        payload: Datele utile (poate fi gol pentru PING)
        secventa: Numărul de secvență
    
    Returns:
        Mesajul complet ca bytes
    """
    # TODO: Implementați construcția mesajului
    # Pași:
    # 1. Calculează lungimea payload-ului
    # 2. Construiește antetul parțial (fără CRC) - 10 bytes:
    #    struct.pack('!2sBBHI', BINAR_MAGIC, BINAR_VERSIUNE, tip, lungime, secventa)
    # 3. Calculează CRC32 peste (antet_partial + payload)
    # 4. Construiește mesajul final cu CRC inclus
    pass


def parseaza_mesaj(date: bytes) -> Optional[Dict[str, Any]]:
    """
    Parsează un mesaj BINAR și verifică CRC.
    
    PREDICȚIE:
    - Ce returnezi dacă primești mai puțin de 14 bytes?
    - Cum extragi payload-ul din mesaj?
    - Cum verifici că CRC-ul primit e corect?
    
    Args:
        date: Buffer-ul cu mesajul primit
    
    Returns:
        Dicționar cu câmpurile parsate sau None dacă invalid
    """
    # TODO: Implementați parsarea mesajului
    # Pași:
    # 1. Verifică lungimea minimă (14 bytes)
    # 2. Despachetează antetul: struct.unpack('!2sBBHII', date[:14])
    # 3. Verifică magic-ul
    # 4. Extrage payload-ul: date[14:14+lungime]
    # 5. Verifică CRC-ul
    # 6. Returnează dicționar cu: tip, versiune, lungime, secventa, payload, crc_valid
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_REȚEA
# Scop: Comunicare cu serverul prin socket TCP
# ═══════════════════════════════════════════════════════════════════════════════

def conecteaza() -> Optional[socket.socket]:
    """
    Creează și conectează un socket la server.
    
    Returns:
        Socket-ul conectat sau None dacă a eșuat
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((SERVER_HOST, SERVER_PORT))
        return sock
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        print(f"Eroare conectare: {e}")
        return None


def trimite_si_primeste(sock: socket.socket, tip: TipMesaj, 
                        payload: bytes, secventa: int) -> Optional[Dict[str, Any]]:
    """
    Trimite un mesaj și așteaptă răspunsul.
    
    PREDICȚIE:
    - recv(1024) garantează că primești exact 1024 bytes?
    - Ce se întâmplă dacă serverul trimite răspunsul în două pachete TCP?
    
    Args:
        sock: Socket-ul conectat
        tip: Tipul mesajului de trimis
        payload: Payload-ul mesajului
        secventa: Numărul de secvență
    
    Returns:
        Răspunsul parsat sau None dacă a eșuat
    """
    # TODO: Implementați trimiterea și recepția
    # Pași:
    # 1. Construiește mesajul cu construieste_mesaj()
    # 2. Trimite cu sock.sendall()
    # 3. Primește răspunsul cu sock.recv(1024)
    # 4. Parsează cu parseaza_mesaj()
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRAM_PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Demonstrează utilizarea clientului BINAR."""
    print("=" * 60)
    print("Client Protocol BINAR")
    print("=" * 60)
    
    # Verifică implementarea CRC
    print("\n1. Verificare implementare CRC32...")
    if not verifica_crc_cunoscut():
        print("   EROARE: Implementați calculeaza_crc32() corect!")
        return
    
    # Conectare
    print("\n2. Conectare la server...")
    sock = conecteaza()
    if sock is None:
        print("   EROARE: Nu s-a putut conecta!")
        print("   Verificați că laboratorul e pornit:")
        print("   python3 scripts/start_lab.py")
        return
    print("   Conectat cu succes!")
    
    secventa = 0
    
    try:
        # Test PING
        print("\n3. Test PING...")
        secventa += 1
        raspuns = trimite_si_primeste(sock, TipMesaj.PING, b'', secventa)
        if raspuns:
            print(f"   Trimis: PING (secvență={secventa})")
            print(f"   Primit: tip={raspuns.get('tip')}, CRC valid={raspuns.get('crc_valid')}")
            if raspuns.get('tip') == TipMesaj.PONG:
                print("   ✓ PONG primit corect!")
        
        # Test SET
        print("\n4. Test SET...")
        secventa += 1
        payload = b'cheie\x00valoare_test'  # cheie + null + valoare
        raspuns = trimite_si_primeste(sock, TipMesaj.SET, payload, secventa)
        if raspuns:
            print(f"   Trimis: SET cheie=valoare_test (secvență={secventa})")
            print(f"   Primit: tip={raspuns.get('tip')}, CRC valid={raspuns.get('crc_valid')}")
        
        # Test GET
        print("\n5. Test GET...")
        secventa += 1
        payload = b'cheie'
        raspuns = trimite_si_primeste(sock, TipMesaj.GET, payload, secventa)
        if raspuns:
            print(f"   Trimis: GET cheie (secvență={secventa})")
            print(f"   Primit: tip={raspuns.get('tip')}, payload={raspuns.get('payload')}")
        
        # Test DELETE
        print("\n6. Test DELETE...")
        secventa += 1
        payload = b'cheie'
        raspuns = trimite_si_primeste(sock, TipMesaj.DELETE, payload, secventa)
        if raspuns:
            print(f"   Trimis: DELETE cheie (secvență={secventa})")
            print(f"   Primit: tip={raspuns.get('tip')}, CRC valid={raspuns.get('crc_valid')}")
    
    finally:
        sock.close()
        print("\n7. Conexiune închisă.")
    
    print("\n" + "=" * 60)
    print("Test complet!")
    print("=" * 60)
    
    # Verificare răspunsuri predicție
    print("\n" + "-" * 60)
    print("VERIFICARE PREDICȚII:")
    print("-" * 60)
    print("1. Antetul are 14 bytes (2+1+1+2+4+4)")
    print("2. '!' = Network Byte Order (big-endian), esențial pentru interoperabilitate")
    print("3. CRC se calculează peste antet FĂRĂ CRC (10 bytes) + payload")
    print("4. CRC32('123456789') = 0xCBF43926 (valoare standard de verificare)")


if __name__ == "__main__":
    main()
