#!/usr/bin/env python3
"""
Tema 2.03: Proiectare Protocol Binar pentru Transfer Mesaje
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

CERINȚĂ:
Proiectați și implementați un protocol binar simplu pentru schimb de mesaje.

SPECIFICAȚII PROTOCOL:
1. Header fix de 8 bytes:
   - Byte 0-1: Magic number (0xCAFE) — identificator protocol
   - Byte 2: Versiune protocol (0x01)
   - Byte 3: Tip mesaj (0x01=TEXT, 0x02=PING, 0x03=PONG, 0xFF=ERROR)
   - Byte 4-5: Lungime payload (big-endian, unsigned, max 65535)
   - Byte 6-7: Checksum XOR (peste payload, big-endian)

2. Payload: date variabile (0-65535 bytes)

DIAGRAMA PACHET:
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│  0xCA   │  0xFE   │ Version │ MsgType │ Len Hi  │ Len Lo  │ Chk Hi  │ Chk Lo  │
│ (magic) │ (magic) │  (0x01) │ (tip)   │  (MSB)  │  (LSB)  │  (MSB)  │  (LSB)  │
├─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┤
│                              Payload (variabil)                               │
│                           (0 până la 65535 bytes)                             │
└───────────────────────────────────────────────────────────────────────────────┘

NIVEL: Avansat (Bloom: CREATE)
TIMP ESTIMAT: 60-90 minute
PREREQUISITE: Înțelegerea struct.pack/unpack, bitwise XOR

EXEMPLE INTERACȚIUNE:
    # Codare mesaj text
    >>> encoded = encode_message(TipMesaj.TEXT, b"Salut!")
    >>> print(encoded.hex())
    cafe0101000653616c757421xxxx  # xxxx = checksum

    # Decodare
    >>> tip, payload = decode_message(encoded)
    >>> print(tip, payload)
    TipMesaj.TEXT b'Salut!'

HINTS:
- struct.pack(">H", valoare) — împachetează uint16 big-endian
- struct.unpack(">H", bytes)[0] — despachetează uint16 big-endian
- bytes[i] ^ bytes[j] — XOR între octeți
"""

from __future__ import annotations

import struct
import argparse
import sys
from dataclasses import dataclass
from typing import Tuple
from enum import IntEnum


# ============================================================================
# CONSTANTE PROTOCOL
# ============================================================================

MAGIC_NUMBER: int = 0xCAFE
PROTOCOL_VERSION: int = 0x01
HEADER_SIZE: int = 8
MAX_PAYLOAD_SIZE: int = 65535


class TipMesaj(IntEnum):
    """
    Tipurile de mesaje suportate de protocol.
    
    Attributes:
        TEXT: Mesaj text obișnuit (payload = text UTF-8)
        PING: Verificare disponibilitate (payload gol)
        PONG: Răspuns la PING (payload gol)
        ERROR: Mesaj de eroare (payload = descriere eroare)
    """
    TEXT = 0x01
    PING = 0x02
    PONG = 0x03
    ERROR = 0xFF


class ProtocolError(Exception):
    """
    Excepție pentru erori de protocol.
    
    Aruncată când:
    - Magic number invalid
    - Versiune necunoscută
    - Lungime payload incorectă
    - Checksum invalid
    """
    pass


# ============================================================================
# FUNCȚII AUXILIARE
# ============================================================================

def _bytes_to_hex_dump(data: bytes, bytes_per_line: int = 16) -> str:
    """
    Convertește bytes la reprezentare hex dump pentru debugging.
    
    Args:
        data: Datele de convertit
        bytes_per_line: Câți bytes pe linie
        
    Returns:
        String formatat hex dump
    """
    lines = []
    for i in range(0, len(data), bytes_per_line):
        chunk = data[i:i + bytes_per_line]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        lines.append(f"{i:04x}  {hex_part:<{bytes_per_line * 3}}  {ascii_part}")
    return '\n'.join(lines)


# ============================================================================
# TODO: IMPLEMENTAȚI FUNCȚIILE DE CODARE/DECODARE
# ============================================================================

def calculeaza_checksum(payload: bytes) -> int:
    """
    Calculează checksum XOR pentru payload.
    
    Algoritmul:
    1. Dacă payload e gol, returnează 0
    2. Împarte payload în perechi de bytes (padding cu 0 dacă lungime impară)
    3. Interpretează fiecare pereche ca uint16 big-endian
    4. XOR între toate valorile uint16
    
    Args:
        payload: Datele pentru care se calculează checksum
        
    Returns:
        Checksum pe 16 biți (0-65535)
        
    Exemple:
        >>> calculeaza_checksum(b"")
        0
        >>> calculeaza_checksum(b"AB")  # 0x4142
        16706
        >>> calculeaza_checksum(b"ABCD")  # 0x4142 ^ 0x4344 = 0x0206
        518
        
    TODO: Implementare
    """
    # HINT: Structura implementării
    # 1. Verifică dacă payload e gol
    # 2. Adaugă padding dacă lungime impară: payload + b'\x00'
    # 3. Iterează prin payload câte 2 bytes
    # 4. Folosește struct.unpack(">H", payload[i:i+2])[0] pentru conversie
    # 5. Acumulează XOR
    pass


def encode_message(tip: TipMesaj, payload: bytes = b"") -> bytes:
    """
    Codifică un mesaj în format binar conform protocolului.
    
    Structura mesajului rezultat:
    - Bytes 0-1: MAGIC_NUMBER (0xCAFE)
    - Byte 2: PROTOCOL_VERSION (0x01)
    - Byte 3: tip (din enum TipMesaj)
    - Bytes 4-5: len(payload) ca uint16 big-endian
    - Bytes 6-7: checksum ca uint16 big-endian
    - Bytes 8+: payload
    
    Args:
        tip: Tipul mesajului (TipMesaj enum)
        payload: Datele mesajului (poate fi gol pentru PING/PONG)
        
    Returns:
        Mesajul codificat complet (header + payload)
        
    Raises:
        ValueError: Dacă payload depășește MAX_PAYLOAD_SIZE (65535) bytes
        TypeError: Dacă tip nu este TipMesaj sau payload nu este bytes
        
    Exemple:
        >>> encode_message(TipMesaj.PING).hex()
        'cafe010200000000'
        >>> len(encode_message(TipMesaj.TEXT, b"test"))
        12  # 8 header + 4 payload
        
    TODO: Implementare
    """
    # HINT: Structura implementării
    # 1. Validare: isinstance(tip, TipMesaj), isinstance(payload, bytes)
    # 2. Validare: len(payload) <= MAX_PAYLOAD_SIZE
    # 3. Calculează checksum cu funcția calculeaza_checksum()
    # 4. Construiește header: struct.pack(">HBBHH", magic, version, tip, lungime, checksum)
    # 5. Returnează header + payload
    pass


def decode_message(data: bytes) -> Tuple[TipMesaj, bytes]:
    """
    Decodifică un mesaj din format binar.
    
    Pași de validare (în ordine):
    1. Verifică lungime minimă (>= HEADER_SIZE)
    2. Verifică magic number (== MAGIC_NUMBER)
    3. Verifică versiune (== PROTOCOL_VERSION)
    4. Extrage și verifică lungime payload
    5. Verifică că există destule date pentru payload
    6. Extrage payload
    7. Recalculează și verifică checksum
    
    Args:
        data: Datele brute primite (bytes)
        
    Returns:
        Tuple (tip_mesaj, payload) unde:
        - tip_mesaj: TipMesaj enum
        - payload: bytes cu datele mesajului
        
    Raises:
        ProtocolError: Cu mesaj descriptiv pentru fiecare tip de eroare:
            - "Date insuficiente: așteptat minim {HEADER_SIZE} bytes, primit {n}"
            - "Magic number invalid: așteptat 0xCAFE, primit 0x{magic:04X}"
            - "Versiune protocol necunoscută: {version}"
            - "Lungime payload invalidă: anunțată {announced}, disponibilă {available}"
            - "Checksum invalid: așteptat 0x{expected:04X}, calculat 0x{calculated:04X}"
            - "Tip mesaj necunoscut: 0x{tip:02X}"
            
    Exemple:
        >>> tip, payload = decode_message(bytes.fromhex('cafe010200000000'))
        >>> tip == TipMesaj.PING
        True
        >>> payload
        b''
        
    TODO: Implementare
    """
    # HINT: Structura implementării
    # 1. if len(data) < HEADER_SIZE: raise ProtocolError(...)
    # 2. magic, version, tip_raw, lungime, checksum_primit = struct.unpack(">HBBHH", data[:8])
    # 3. Validări în ordine (vezi docstring)
    # 4. payload = data[HEADER_SIZE:HEADER_SIZE + lungime]
    # 5. checksum_calculat = calculeaza_checksum(payload)
    # 6. Compară checksum-urile
    # 7. Convertește tip_raw la TipMesaj (poate arunca ValueError)
    # 8. return (TipMesaj(tip_raw), payload)
    pass


# ============================================================================
# FUNCȚII HELPER PENTRU UTILIZARE PRACTICĂ
# ============================================================================

def encode_text(text: str) -> bytes:
    """
    Shortcut pentru codarea unui mesaj text.
    
    Args:
        text: Textul de trimis (va fi encodat UTF-8)
        
    Returns:
        Mesaj binar complet
    """
    return encode_message(TipMesaj.TEXT, text.encode('utf-8'))


def encode_ping() -> bytes:
    """Shortcut pentru mesaj PING."""
    return encode_message(TipMesaj.PING)


def encode_pong() -> bytes:
    """Shortcut pentru mesaj PONG."""
    return encode_message(TipMesaj.PONG)


def encode_error(descriere: str) -> bytes:
    """
    Shortcut pentru mesaj de eroare.
    
    Args:
        descriere: Descrierea erorii
        
    Returns:
        Mesaj binar de eroare
    """
    return encode_message(TipMesaj.ERROR, descriere.encode('utf-8'))


# ============================================================================
# TESTE
# ============================================================================

def rulează_teste() -> bool:
    """
    Rulează suita de teste pentru protocol.
    
    Returns:
        True dacă toate testele trec, False altfel
    """
    print("=" * 60)
    print("Teste Protocol Binar - Tema 2.03")
    print("=" * 60)
    
    teste_trecute = 0
    teste_totale = 0
    
    # Test 1: Checksum payload gol
    teste_totale += 1
    print("\nTest 1: Checksum payload gol")
    try:
        rezultat = calculeaza_checksum(b"")
        if rezultat == 0:
            print("  ✓ PASS: checksum(b'') = 0")
            teste_trecute += 1
        else:
            print(f"  ✗ FAIL: așteptat 0, primit {rezultat}")
    except Exception as e:
        print(f"  ✗ FAIL: excepție {e}")
    
    # Test 2: Checksum 2 bytes
    teste_totale += 1
    print("\nTest 2: Checksum 2 bytes")
    try:
        rezultat = calculeaza_checksum(b"AB")  # 0x4142
        if rezultat == 0x4142:
            print(f"  ✓ PASS: checksum(b'AB') = 0x{rezultat:04X}")
            teste_trecute += 1
        else:
            print(f"  ✗ FAIL: așteptat 0x4142, primit 0x{rezultat:04X}")
    except Exception as e:
        print(f"  ✗ FAIL: excepție {e}")
    
    # Test 3: Checksum 4 bytes (XOR)
    teste_totale += 1
    print("\nTest 3: Checksum 4 bytes (cu XOR)")
    try:
        rezultat = calculeaza_checksum(b"ABCD")  # 0x4142 ^ 0x4344 = 0x0206
        if rezultat == 0x0206:
            print(f"  ✓ PASS: checksum(b'ABCD') = 0x{rezultat:04X}")
            teste_trecute += 1
        else:
            print(f"  ✗ FAIL: așteptat 0x0206, primit 0x{rezultat:04X}")
    except Exception as e:
        print(f"  ✗ FAIL: excepție {e}")
    
    # Test 4: Checksum lungime impară (padding)
    teste_totale += 1
    print("\nTest 4: Checksum lungime impară")
    try:
        rezultat = calculeaza_checksum(b"ABC")  # 0x4142 ^ 0x4300 = 0x0242
        if rezultat == 0x0242:
            print(f"  ✓ PASS: checksum(b'ABC') = 0x{rezultat:04X}")
            teste_trecute += 1
        else:
            print(f"  ✗ FAIL: așteptat 0x0242, primit 0x{rezultat:04X}")
    except Exception as e:
        print(f"  ✗ FAIL: excepție {e}")
    
    # Test 5: Encode/Decode PING
    teste_totale += 1
    print("\nTest 5: Encode/Decode PING")
    try:
        encoded = encode_message(TipMesaj.PING)
        print(f"  Encoded: {encoded.hex()}")
        tip, payload = decode_message(encoded)
        if tip == TipMesaj.PING and payload == b"":
            print("  ✓ PASS: PING encode/decode corect")
            teste_trecute += 1
        else:
            print(f"  ✗ FAIL: tip={tip}, payload={payload}")
    except Exception as e:
        print(f"  ✗ FAIL: excepție {e}")
    
    # Test 6: Encode/Decode TEXT
    teste_totale += 1
    print("\nTest 6: Encode/Decode TEXT")
    try:
        text_original = "Salut, lume! 🎉"
        encoded = encode_message(TipMesaj.TEXT, text_original.encode('utf-8'))
        print(f"  Original: {text_original}")
        print(f"  Encoded ({len(encoded)} bytes): {encoded[:20].hex()}...")
        tip, payload = decode_message(encoded)
        text_decodat = payload.decode('utf-8')
        if tip == TipMesaj.TEXT and text_decodat == text_original:
            print(f"  Decoded: {text_decodat}")
            print("  ✓ PASS: TEXT encode/decode corect")
            teste_trecute += 1
        else:
            print(f"  ✗ FAIL: tip={tip}, text={text_decodat}")
    except Exception as e:
        print(f"  ✗ FAIL: excepție {e}")
    
    # Test 7: Detectare magic invalid
    teste_totale += 1
    print("\nTest 7: Detectare magic number invalid")
    try:
        bad_data = b"\xDE\xAD\x01\x01\x00\x00\x00\x00"
        decode_message(bad_data)
        print("  ✗ FAIL: ar fi trebuit să arunce ProtocolError")
    except ProtocolError as e:
        print(f"  ✓ PASS: detectat corect - {e}")
        teste_trecute += 1
    except Exception as e:
        print(f"  ✗ FAIL: excepție greșită {type(e).__name__}: {e}")
    
    # Test 8: Detectare checksum corupt
    teste_totale += 1
    print("\nTest 8: Detectare checksum corupt")
    try:
        good = encode_message(TipMesaj.TEXT, b"test data")
        # Corupem ultimul byte din header (parte din checksum)
        corrupted = good[:7] + bytes([good[7] ^ 0xFF]) + good[8:]
        decode_message(corrupted)
        print("  ✗ FAIL: ar fi trebuit să arunce ProtocolError")
    except ProtocolError as e:
        print(f"  ✓ PASS: detectat corect - {e}")
        teste_trecute += 1
    except Exception as e:
        print(f"  ✗ FAIL: excepție greșită {type(e).__name__}: {e}")
    
    # Test 9: Detectare date insuficiente
    teste_totale += 1
    print("\nTest 9: Detectare date insuficiente")
    try:
        decode_message(b"\xCA\xFE\x01")  # Doar 3 bytes
        print("  ✗ FAIL: ar fi trebuit să arunce ProtocolError")
    except ProtocolError as e:
        print(f"  ✓ PASS: detectat corect - {e}")
        teste_trecute += 1
    except Exception as e:
        print(f"  ✗ FAIL: excepție greșită {type(e).__name__}: {e}")
    
    # Test 10: Payload maxim
    teste_totale += 1
    print("\nTest 10: Validare payload prea mare")
    try:
        huge_payload = b"X" * (MAX_PAYLOAD_SIZE + 1)
        encode_message(TipMesaj.TEXT, huge_payload)
        print("  ✗ FAIL: ar fi trebuit să arunce ValueError")
    except ValueError as e:
        print(f"  ✓ PASS: detectat corect - {e}")
        teste_trecute += 1
    except Exception as e:
        print(f"  ✗ FAIL: excepție greșită {type(e).__name__}: {e}")
    
    # Sumar
    print("\n" + "=" * 60)
    print(f"Rezultate: {teste_trecute}/{teste_totale} teste trecute")
    print("=" * 60)
    
    if teste_trecute == teste_totale:
        print("🎉 Toate testele au trecut! Implementare corectă.")
        return True
    else:
        print(f"⚠️  {teste_totale - teste_trecute} teste eșuate. Verifică implementarea.")
        return False


# ============================================================================
# DEMONSTRAȚIE INTERACTIVĂ
# ============================================================================

def demo_interactiv() -> None:
    """Demonstrație interactivă a protocolului."""
    print("=" * 60)
    print("Demo Protocol Binar - Mod Interactiv")
    print("=" * 60)
    print("\nComenzi disponibile:")
    print("  text <mesaj>  - Codează mesaj text")
    print("  ping          - Codează PING")
    print("  decode <hex>  - Decodează din hex")
    print("  quit          - Ieșire")
    print()
    
    while True:
        try:
            linie = input("> ").strip()
            
            if not linie:
                continue
            
            părți = linie.split(maxsplit=1)
            comandă = părți[0].lower()
            argument = părți[1] if len(părți) > 1 else ""
            
            if comandă == "quit":
                print("La revedere!")
                break
            
            elif comandă == "text":
                if not argument:
                    print("Eroare: lipsește mesajul")
                    continue
                encoded = encode_text(argument)
                print(f"Hex: {encoded.hex()}")
                print(f"Dump:\n{_bytes_to_hex_dump(encoded)}")
            
            elif comandă == "ping":
                encoded = encode_ping()
                print(f"Hex: {encoded.hex()}")
            
            elif comandă == "decode":
                if not argument:
                    print("Eroare: lipsește hex-ul")
                    continue
                try:
                    data = bytes.fromhex(argument.replace(" ", ""))
                    tip, payload = decode_message(data)
                    print(f"Tip: {tip.name}")
                    if payload:
                        try:
                            print(f"Payload (text): {payload.decode('utf-8')}")
                        except UnicodeDecodeError:
                            print(f"Payload (hex): {payload.hex()}")
                    else:
                        print("Payload: (gol)")
                except ValueError as e:
                    print(f"Eroare hex invalid: {e}")
                except ProtocolError as e:
                    print(f"Eroare protocol: {e}")
            
            else:
                print(f"Comandă necunoscută: {comandă}")
                
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nLa revedere!")
            break


# ============================================================================
# PUNCT DE INTRARE
# ============================================================================

def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Protocol Binar pentru Transfer Mesaje - Tema 2.03",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python hw_2_03.py test           # Rulează testele
  python hw_2_03.py demo           # Mod interactiv
  python hw_2_03.py encode "Salut" # Codează mesaj
  python hw_2_03.py decode CAFE... # Decodează din hex

Acest exercițiu testează capacitatea de a proiecta și implementa
un protocol binar simplu cu validare și detecție erori.
        """
    )
    
    subparsers = parser.add_subparsers(dest="comandă")
    
    # Subcomandă: test
    subparsers.add_parser("test", help="Rulează testele automate")
    
    # Subcomandă: demo
    subparsers.add_parser("demo", help="Mod interactiv")
    
    # Subcomandă: encode
    parser_encode = subparsers.add_parser("encode", help="Codează un mesaj")
    parser_encode.add_argument("mesaj", help="Mesajul de codat")
    
    # Subcomandă: decode
    parser_decode = subparsers.add_parser("decode", help="Decodează din hex")
    parser_decode.add_argument("hex", help="Datele în format hex")
    
    args = parser.parse_args()
    
    if args.comandă == "test":
        succes = rulează_teste()
        return 0 if succes else 1
    
    elif args.comandă == "demo":
        demo_interactiv()
        return 0
    
    elif args.comandă == "encode":
        try:
            encoded = encode_text(args.mesaj)
            print(encoded.hex())
            return 0
        except Exception as e:
            print(f"Eroare: {e}", file=sys.stderr)
            return 1
    
    elif args.comandă == "decode":
        try:
            data = bytes.fromhex(args.hex.replace(" ", ""))
            tip, payload = decode_message(data)
            print(f"Tip: {tip.name}")
            if payload:
                try:
                    print(f"Payload: {payload.decode('utf-8')}")
                except UnicodeDecodeError:
                    print(f"Payload (hex): {payload.hex()}")
            return 0
        except ProtocolError as e:
            print(f"Eroare protocol: {e}", file=sys.stderr)
            return 1
        except ValueError as e:
            print(f"Eroare hex: {e}", file=sys.stderr)
            return 1
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
