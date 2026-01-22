#!/usr/bin/env python3
"""
Exercițiu 5: Debugging în Perechi — Protocol BINAR

Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

INSTRUCȚIUNI PAIR PROGRAMMING
=============================

ROLURI:
- DRIVER: Controlează tastatura, scrie codul/notițele
- NAVIGATOR: Observă, sugerează, verifică logica, consultă documentația

ROTAȚIE: Schimbați rolurile la fiecare 10 minute (folosiți un timer!)

REGULI:
1. Driver-ul explică CE face ÎNAINTE de a scrie
2. Navigator-ul întreabă DE CE, nu dictează codul
3. Ambii trebuie să înțeleagă fiecare linie
4. Notați descoperirile pe hârtie/whiteboard

EXERCIȚIU:
==========
Codul de mai jos conține 7 BUG-URI INTENȚIONATE.
Găsiți-le PRIN INSPECȚIE, fără a rula codul!

Pași:
1. Citiți specificația protocolului BINAR din docs/theory_summary.md
2. Comparați fiecare linie cu specificația
3. Notați: numărul liniei, bug-ul găsit, corecția propusă
4. ABIA DUPĂ ce ați găsit toate 7, rulați codul pentru verificare

Timp alocat: 30-40 minute
Punctaj: 10 puncte (~ 1.5 puncte per bug găsit corect)

STRUCTURA ANTETULUI BINAR (14 octeți):
======================================
| Offset | Lungime | Câmp      | Format           |
|--------|---------|-----------|------------------|
| 0-1    | 2       | Magic     | bytes "NP"       |
| 2      | 1       | Versiune  | uint8            |
| 3      | 1       | Tip       | uint8            |
| 4-5    | 2       | Lungime   | uint16 BE        |
| 6-9    | 4       | Secvență  | uint32 BE        |
| 10-13  | 4       | CRC32     | uint32 BE        |

BE = Big-Endian (Network Byte Order)
CRC32 se calculează peste: bytes 0-9 (antet fără CRC) + payload
"""

import struct
import binascii
from typing import Optional, Dict, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE
# ═══════════════════════════════════════════════════════════════════════════════

MAGIC = b'NP'
VERSIUNE = 1
DIMENSIUNE_ANTET = 14

# Tipuri de mesaje
TIP_PING = 0x01
TIP_PONG = 0x02
TIP_SET = 0x03
TIP_GET = 0x04
TIP_DELETE = 0x05
TIP_RESPONSE = 0x06
TIP_ERROR = 0xFF


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII CU BUG-URI — GĂSIȚI TOATE 7!
# ═══════════════════════════════════════════════════════════════════════════════

def construieste_mesaj_buggy(tip: int, payload: bytes, secventa: int) -> bytes:
    """
    Construiește un mesaj în format BINAR.
    
    ATENȚIE: Această funcție conține BUG-URI pentru exercițiu!
    
    Întrebări pentru Navigator:
    - Ordinea bytes-ilor e corectă pentru rețea?
    - Dimensiunile câmpurilor corespund cu specificația?
    - CRC-ul include datele corecte?
    
    Args:
        tip: Tipul mesajului (0x01-0xFF)
        payload: Datele utile
        secventa: Numărul de secvență
    
    Returns:
        Mesaj complet (antet + payload)
    """
    # Calculează lungimea payload-ului
    lungime = len(payload) + 1  # BUG 1: De ce +1? Lungimea e EXACT len(payload)
    
    # Construiește antetul parțial (fără CRC)
    # BUG 2: Lipsește '!' din format string pentru network byte order
    antet_partial = struct.pack('2sBBHI',  
        MAGIC,      # 2 bytes
        VERSIUNE,   # 1 byte
        tip,        # 1 byte
        lungime,    # 2 bytes
        secventa    # 4 bytes
    )  # Total: 10 bytes (corect)
    
    # Calculează CRC32
    # BUG 3: CRC trebuie calculat peste antet_partial + payload, nu doar payload
    crc = binascii.crc32(payload) & 0xFFFFFFFF
    
    # Construiește mesajul complet
    # BUG 4: Ordinea parametrilor e greșită (tip și versiune inversate)
    mesaj = struct.pack('!2sBBHII',
        MAGIC,
        tip,        # Greșit! Ar trebui VERSIUNE
        VERSIUNE,   # Greșit! Ar trebui tip  
        lungime,
        secventa,
        crc
    ) + payload
    
    return mesaj


def parseaza_antet_buggy(date: bytes) -> Optional[Dict[str, Any]]:
    """
    Parsează antetul unui mesaj BINAR.
    
    ATENȚIE: Această funcție conține BUG-URI pentru exercițiu!
    
    Întrebări pentru Navigator:
    - Indexarea bytes-ilor e corectă?
    - Se verifică toate condițiile de validare?
    - Ordinea bytes-ilor la despachetare?
    
    Args:
        date: Buffer-ul de date primit
    
    Returns:
        Dicționar cu câmpurile antetului sau None dacă invalid
    """
    # Verifică lungimea minimă
    if len(date) < DIMENSIUNE_ANTET:
        print(f"Eroare: date prea scurte ({len(date)} < {DIMENSIUNE_ANTET})")
        return None
    
    # Extrage Magic
    # BUG 5: Indexare greșită - ar trebui [0:2] nu [0:1]
    magic = date[0:1]
    
    # Verifică Magic
    if magic != MAGIC:
        print(f"Eroare: magic invalid {magic}")
        return None
    
    # Extrage versiunea
    # BUG 6: Index greșit din cauza bug-ului anterior
    # Dacă magic e [0:1], atunci versiune ar fi la [1], nu [2]
    # Dar CORECT ar fi: magic [0:2], versiune [2]
    versiune = date[2]
    
    # Extrage tipul
    tip = date[3]
    
    # Extrage lungimea
    # BUG 7: Lipsește '!' pentru network byte order
    lungime = struct.unpack('H', date[4:6])[0]
    
    # Extrage secvența (această linie e corectă pentru comparație)
    secventa = struct.unpack('!I', date[6:10])[0]
    
    # Extrage CRC
    crc = struct.unpack('!I', date[10:14])[0]
    
    return {
        'magic': magic,
        'versiune': versiune,
        'tip': tip,
        'lungime': lungime,
        'secventa': secventa,
        'crc': crc
    }


def verifica_crc_buggy(date: bytes, lungime_payload: int) -> bool:
    """
    Verifică CRC-ul unui mesaj.
    
    Această funcție e CORECTĂ - folosiți-o ca referință!
    
    Args:
        date: Mesajul complet (antet + payload)
        lungime_payload: Lungimea payload-ului din antet
    
    Returns:
        True dacă CRC e valid, False altfel
    """
    if len(date) < DIMENSIUNE_ANTET + lungime_payload:
        return False
    
    # Extrage CRC-ul primit
    crc_primit = struct.unpack('!I', date[10:14])[0]
    
    # Extrage datele pentru verificare CRC
    antet_fara_crc = date[0:10]
    payload = date[14:14 + lungime_payload]
    
    # Calculează CRC
    crc_calculat = binascii.crc32(antet_fara_crc + payload) & 0xFFFFFFFF
    
    return crc_primit == crc_calculat


# ═══════════════════════════════════════════════════════════════════════════════
# NU RULAȚI PÂNĂ NU GĂSIȚI TOATE BUG-URILE!
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcție de test - NU RULAȚI până nu găsiți bug-urile!"""
    print("=" * 70)
    print("EXERCIȚIU PAIR PROGRAMMING: Găsește Bug-urile în Protocol BINAR")
    print("=" * 70)
    print()
    print("INSTRUCȚIUNI:")
    print("1. Lucrați în PERECHI (Driver + Navigator)")
    print("2. NU rulați acest cod încă!")
    print("3. Citiți specificația din docs/theory_summary.md")
    print("4. Găsiți toate 7 bug-urile prin CITIRE și comparație")
    print("5. Notați pe hârtie: linia, bug-ul, corecția")
    print("6. Abia după ce ați găsit toate 7, rulați pentru verificare")
    print()
    print("Timp alocat: 30-40 minute")
    print("=" * 70)
    print()
    
    # Test simplu pentru verificare după găsirea bug-urilor
    print("Test construcție mesaj PING:")
    try:
        mesaj = construieste_mesaj_buggy(TIP_PING, b'', 1)
        print(f"  Lungime mesaj: {len(mesaj)} bytes (așteptat: 14)")
        print(f"  Hex: {mesaj.hex()}")
        
        # Încearcă să parseze
        antet = parseaza_antet_buggy(mesaj)
        if antet:
            print(f"  Antet parsat: {antet}")
        else:
            print("  EROARE la parsare!")
            
    except Exception as e:
        print(f"  EXCEPȚIE: {e}")
    
    print()
    print("=" * 70)
    print("VERIFICARE RĂSPUNSURI")
    print("=" * 70)
    print()
    print("Ați găsit toate 7 bug-urile?")
    print()
    print("Comparați cu lista de mai jos DOAR după ce ați terminat exercițiul:")
    print()
    print("(scroll down pentru soluții)")
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print("─" * 70)
    print("SOLUȚII (pentru auto-verificare)")
    print("─" * 70)
    print("""
Bug 1 (linia ~73): lungime = len(payload) + 1
  CORECȚIE: lungime = len(payload)
  EXPLICAȚIE: Lungimea payload-ului e exact len(payload), nu +1

Bug 2 (linia ~76): struct.pack('2sBBHI', ...)
  CORECȚIE: struct.pack('!2sBBHI', ...)
  EXPLICAȚIE: Lipsește '!' pentru network byte order (big-endian)

Bug 3 (linia ~86): crc = binascii.crc32(payload)
  CORECȚIE: crc = binascii.crc32(antet_partial + payload)
  EXPLICAȚIE: CRC trebuie calculat peste antet (fără CRC) + payload

Bug 4 (linia ~90-92): MAGIC, tip, VERSIUNE, ...
  CORECȚIE: MAGIC, VERSIUNE, tip, ...
  EXPLICAȚIE: Ordinea câmpurilor e greșită - versiune vine înainte de tip

Bug 5 (linia ~118): magic = date[0:1]
  CORECȚIE: magic = date[0:2]
  EXPLICAȚIE: Magic-ul are 2 bytes ("NP"), nu 1

Bug 6 (linia ~127): versiune = date[2]
  NOTĂ: Acest bug e cauzat de bug 5, dar linia în sine e corectă
  dacă magic e extras corect ca [0:2]

Bug 7 (linia ~133): struct.unpack('H', date[4:6])
  CORECȚIE: struct.unpack('!H', date[4:6])
  EXPLICAȚIE: Lipsește '!' pentru network byte order
""")


if __name__ == "__main__":
    main()
