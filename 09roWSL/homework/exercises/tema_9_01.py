#!/usr/bin/env python3
"""
Tema 9.01: Protocol Multi-Format
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Implementați un protocol binar care suportă mai multe tipuri de mesaje:
TEXT, INTEGER și BLOB.

Punctaj: 100 puncte
Dificultate: Medie
"""

import struct
import zlib
from typing import Tuple, Union


# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTE - NU MODIFICAȚI
# ═══════════════════════════════════════════════════════════════════════════

MAGIC = b'MFMT'          # Octeți magic pentru identificarea protocolului
VERSIUNE = 1             # Versiunea curentă a protocolului

# Tipuri de mesaje
TIP_TEXT = 1             # Payload: șir UTF-8
TIP_INTEGER = 2          # Payload: număr întreg pe 8 octeți
TIP_BLOB = 3             # Payload: date binare arbitrare

# Format header: magic(4) + versiune(1) + tip(1) + lungime(4) + crc(4) = 14 octeți
FORMAT_HEADER = ">4sBBII"
DIMENSIUNE_HEADER = struct.calcsize(FORMAT_HEADER)


# ═══════════════════════════════════════════════════════════════════════════
# FUNCȚII DE IMPLEMENTAT
# ═══════════════════════════════════════════════════════════════════════════

def impacheteaza_mesaj(tip: int, date: Union[str, int, bytes]) -> bytes:
    """
    Împachetează un mesaj în format binar.
    
    Argumente:
        tip: Tipul mesajului (TIP_TEXT, TIP_INTEGER sau TIP_BLOB)
        date: Datele de împachetat
              - Pentru TIP_TEXT: str
              - Pentru TIP_INTEGER: int
              - Pentru TIP_BLOB: bytes
    
    Returnează:
        bytes: Mesajul binar complet (header + payload)
    
    Aruncă:
        ValueError: Dacă tipul este invalid sau datele nu corespund tipului
    
    Exemple:
        >>> mesaj = impacheteaza_mesaj(TIP_TEXT, "Salut!")
        >>> len(mesaj) == DIMENSIUNE_HEADER + len("Salut!".encode())
        True
        
        >>> mesaj = impacheteaza_mesaj(TIP_INTEGER, 12345)
        >>> len(mesaj) == DIMENSIUNE_HEADER + 8
        True
    """
    # TODO: Implementați această funcție
    #
    # Pași:
    # 1. Validați tipul mesajului
    # 2. Convertiți datele în bytes (payload):
    #    - TEXT: date.encode('utf-8')
    #    - INTEGER: struct.pack(">q", date)  # 8 octeți, signed
    #    - BLOB: date (deja bytes)
    # 3. Calculați CRC-32 al payload-ului
    # 4. Construiți header-ul cu struct.pack
    # 5. Returnați header + payload
    
    raise NotImplementedError("Implementați funcția impacheteaza_mesaj()")


def despachetaza_mesaj(mesaj: bytes) -> Tuple[int, Union[str, int, bytes]]:
    """
    Despachetează un mesaj din format binar.
    
    Argumente:
        mesaj: Mesajul binar complet (header + payload)
    
    Returnează:
        tuple: (tip, date)
               - tip: Tipul mesajului (TIP_TEXT, TIP_INTEGER sau TIP_BLOB)
               - date: Datele decodificate
    
    Aruncă:
        ValueError: Dacă mesajul este invalid:
                    - Magic incorect
                    - Versiune nesuportată
                    - Lungime incorectă
                    - CRC-32 nu se potrivește
    
    Exemple:
        >>> mesaj = impacheteaza_mesaj(TIP_TEXT, "Test")
        >>> tip, date = despachetaza_mesaj(mesaj)
        >>> tip == TIP_TEXT and date == "Test"
        True
    """
    # TODO: Implementați această funcție
    #
    # Pași:
    # 1. Verificați că mesajul are cel puțin DIMENSIUNE_HEADER octeți
    # 2. Despachetați header-ul cu struct.unpack
    # 3. Verificați magic == MAGIC
    # 4. Verificați versiune == VERSIUNE
    # 5. Extrageți payload-ul (mesaj[DIMENSIUNE_HEADER:DIMENSIUNE_HEADER+lungime])
    # 6. Verificați CRC-32
    # 7. Decodificați payload-ul în funcție de tip:
    #    - TEXT: payload.decode('utf-8')
    #    - INTEGER: struct.unpack(">q", payload)[0]
    #    - BLOB: payload (păstrați ca bytes)
    # 8. Returnați (tip, date)
    
    raise NotImplementedError("Implementați funcția despachetaza_mesaj()")


# ═══════════════════════════════════════════════════════════════════════════
# FUNCȚII HELPER (OPȚIONALE)
# ═══════════════════════════════════════════════════════════════════════════

def calculeaza_crc(date: bytes) -> int:
    """
    Calculează CRC-32 pentru un set de date.
    
    Argumente:
        date: Datele pentru care se calculează CRC
    
    Returnează:
        int: Valoarea CRC-32 (32 biți fără semn)
    """
    return zlib.crc32(date) & 0xFFFFFFFF


def verifica_crc(date: bytes, crc_asteptat: int) -> bool:
    """
    Verifică dacă CRC-ul calculat se potrivește cu cel așteptat.
    
    Argumente:
        date: Datele de verificat
        crc_asteptat: Valoarea CRC așteptată
    
    Returnează:
        bool: True dacă CRC-ul se potrivește
    """
    return calculeaza_crc(date) == crc_asteptat


def tip_la_nume(tip: int) -> str:
    """
    Convertește un tip numeric la numele său.
    
    Argumente:
        tip: Codul numeric al tipului
    
    Returnează:
        str: Numele tipului
    """
    nume_tipuri = {
        TIP_TEXT: "TEXT",
        TIP_INTEGER: "INTEGER",
        TIP_BLOB: "BLOB"
    }
    return nume_tipuri.get(tip, "NECUNOSCUT")


# ═══════════════════════════════════════════════════════════════════════════
# TESTE LOCALE
# ═══════════════════════════════════════════════════════════════════════════

def test_protocol():
    """Rulează teste de bază pentru verificare."""
    print("=" * 50)
    print("Teste Protocol Multi-Format")
    print("=" * 50)
    print()
    
    teste_trecute = 0
    teste_total = 0
    
    # Test 1: Mesaj text
    teste_total += 1
    try:
        text_original = "Salut, lume!"
        mesaj = impacheteaza_mesaj(TIP_TEXT, text_original)
        tip, text_decodat = despachetaza_mesaj(mesaj)
        
        assert tip == TIP_TEXT, f"Tip greșit: {tip}"
        assert text_decodat == text_original, f"Text greșit: {text_decodat}"
        
        print(f"  ✓ Test TEXT: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print(f"  ⚠ Test TEXT: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test TEXT: EȘUAT - {e}")
    
    # Test 2: Mesaj integer
    teste_total += 1
    try:
        numar_original = 1234567890123
        mesaj = impacheteaza_mesaj(TIP_INTEGER, numar_original)
        tip, numar_decodat = despachetaza_mesaj(mesaj)
        
        assert tip == TIP_INTEGER, f"Tip greșit: {tip}"
        assert numar_decodat == numar_original, f"Număr greșit: {numar_decodat}"
        
        print(f"  ✓ Test INTEGER: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print(f"  ⚠ Test INTEGER: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test INTEGER: EȘUAT - {e}")
    
    # Test 3: Mesaj blob
    teste_total += 1
    try:
        blob_original = b'\x00\x01\x02\xff\xfe\xfd'
        mesaj = impacheteaza_mesaj(TIP_BLOB, blob_original)
        tip, blob_decodat = despachetaza_mesaj(mesaj)
        
        assert tip == TIP_BLOB, f"Tip greșit: {tip}"
        assert blob_decodat == blob_original, f"Blob greșit"
        
        print(f"  ✓ Test BLOB: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print(f"  ⚠ Test BLOB: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test BLOB: EȘUAT - {e}")
    
    # Test 4: Verificare CRC
    teste_total += 1
    try:
        mesaj = impacheteaza_mesaj(TIP_TEXT, "Test CRC")
        # Modificăm un octet din payload
        mesaj_corupt = mesaj[:-1] + bytes([mesaj[-1] ^ 0xFF])
        
        try:
            despachetaza_mesaj(mesaj_corupt)
            print(f"  ✗ Test CRC: EȘUAT - Nu a detectat corupția")
        except ValueError:
            print(f"  ✓ Test CRC: TRECUT (a detectat corupția)")
            teste_trecute += 1
    except NotImplementedError:
        print(f"  ⚠ Test CRC: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test CRC: EȘUAT - {e}")
    
    # Sumar
    print()
    print("=" * 50)
    print(f"Rezultate: {teste_trecute}/{teste_total} teste trecute")
    print("=" * 50)
    
    return teste_trecute == teste_total


if __name__ == "__main__":
    test_protocol()
