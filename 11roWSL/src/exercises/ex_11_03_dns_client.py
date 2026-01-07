#!/usr/bin/env python3
"""
Exercițiul 11.03: Client DNS
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Implementare client DNS care demonstrează structura mesajelor DNS
conform RFC 1035.

Utilizare:
    python ex_11_03_dns_client.py google.com A
    python ex_11_03_dns_client.py google.com MX --verbose
    python ex_11_03_dns_client.py google.com NS --server 1.1.1.1
"""

import argparse
import socket
import struct
import random
from dataclasses import dataclass
from typing import Optional


# Tipuri de înregistrări DNS
TIPURI_INREGISTRARI = {
    'A': 1,
    'NS': 2,
    'CNAME': 5,
    'SOA': 6,
    'PTR': 12,
    'MX': 15,
    'TXT': 16,
    'AAAA': 28,
}

TIPURI_INVERSE = {v: k for k, v in TIPURI_INREGISTRARI.items()}


@dataclass
class InregistrareDNS:
    """Reprezintă o înregistrare DNS."""
    nume: str
    tip: str
    clasa: int
    ttl: int
    date: str


def codeaza_nume_domeniu(nume: str) -> bytes:
    """
    Codează un nume de domeniu în format DNS.
    
    Exemplu: "www.google.com" -> b'\x03www\x06google\x03com\x00'
    """
    parti = nume.rstrip('.').split('.')
    rezultat = b''
    for parte in parti:
        rezultat += bytes([len(parte)]) + parte.encode()
    rezultat += b'\x00'
    return rezultat


def decodeaza_nume_domeniu(date: bytes, offset: int) -> tuple[str, int]:
    """
    Decodează un nume de domeniu din format DNS.
    
    Gestionează și pointerii de compresie.
    
    Returns:
        Tuple (nume_domeniu, offset_nou)
    """
    etichete = []
    offset_original = offset
    saltat = False
    
    while True:
        lungime = date[offset]
        
        # Verifică pointer de compresie
        if (lungime & 0xC0) == 0xC0:
            if not saltat:
                offset_original = offset + 2
            pointer = ((lungime & 0x3F) << 8) | date[offset + 1]
            offset = pointer
            saltat = True
            continue
        
        if lungime == 0:
            if not saltat:
                offset_original = offset + 1
            break
        
        offset += 1
        etichete.append(date[offset:offset + lungime].decode())
        offset += lungime
    
    return '.'.join(etichete), offset_original


def construieste_interogare_dns(nume: str, tip_inregistrare: str) -> bytes:
    """
    Construiește un pachet de interogare DNS.
    
    Args:
        nume: Numele de domeniu de interogat
        tip_inregistrare: Tipul înregistrării (A, AAAA, MX, etc.)
    
    Returns:
        Pachetul DNS ca bytes
    """
    # Generează ID tranzacție aleator
    id_tranzactie = random.randint(0, 65535)
    
    # Flags: QR=0 (interogare), RD=1 (recursie dorită)
    flags = 0x0100
    
    # Antet DNS (12 octeți)
    antet = struct.pack(
        '>HHHHHH',
        id_tranzactie,  # ID
        flags,          # Flags
        1,              # QDCOUNT (1 întrebare)
        0,              # ANCOUNT
        0,              # NSCOUNT
        0               # ARCOUNT
    )
    
    # Secțiunea întrebare
    tip_cod = TIPURI_INREGISTRARI.get(tip_inregistrare.upper(), 1)
    intrebare = codeaza_nume_domeniu(nume) + struct.pack('>HH', tip_cod, 1)
    
    return antet + intrebare


def parseaza_raspuns_dns(date: bytes) -> tuple[list[InregistrareDNS], dict]:
    """
    Parsează un răspuns DNS.
    
    Returns:
        Tuple (lista_inregistrari, informatii_antet)
    """
    # Parsează antetul
    antet = struct.unpack('>HHHHHH', date[:12])
    id_tranzactie, flags, qdcount, ancount, nscount, arcount = antet
    
    info_antet = {
        'id': id_tranzactie,
        'qr': (flags >> 15) & 1,
        'opcode': (flags >> 11) & 0xF,
        'aa': (flags >> 10) & 1,
        'tc': (flags >> 9) & 1,
        'rd': (flags >> 8) & 1,
        'ra': (flags >> 7) & 1,
        'rcode': flags & 0xF,
        'qdcount': qdcount,
        'ancount': ancount,
        'nscount': nscount,
        'arcount': arcount,
    }
    
    offset = 12
    
    # Sari peste secțiunea întrebări
    for _ in range(qdcount):
        _, offset = decodeaza_nume_domeniu(date, offset)
        offset += 4  # QTYPE + QCLASS
    
    # Parsează înregistrările de răspuns
    inregistrari = []
    
    for _ in range(ancount + nscount + arcount):
        if offset >= len(date):
            break
        
        # Parsează numele
        nume, offset = decodeaza_nume_domeniu(date, offset)
        
        # Parsează câmpurile fixe
        if offset + 10 > len(date):
            break
        
        tip, clasa, ttl, rdlength = struct.unpack('>HHIH', date[offset:offset + 10])
        offset += 10
        
        # Parsează datele înregistrării
        rdata = date[offset:offset + rdlength]
        offset += rdlength
        
        # Formatează datele în funcție de tip
        date_formatate = formateaza_rdata(tip, rdata, date)
        tip_str = TIPURI_INVERSE.get(tip, str(tip))
        
        inregistrari.append(InregistrareDNS(
            nume=nume,
            tip=tip_str,
            clasa=clasa,
            ttl=ttl,
            date=date_formatate
        ))
    
    return inregistrari, info_antet


def formateaza_rdata(tip: int, rdata: bytes, pachet_complet: bytes) -> str:
    """Formatează datele unei înregistrări în funcție de tip."""
    if tip == 1:  # A
        return '.'.join(str(b) for b in rdata)
    elif tip == 28:  # AAAA
        return ':'.join(f'{rdata[i]:02x}{rdata[i+1]:02x}' for i in range(0, 16, 2))
    elif tip in (2, 5, 12):  # NS, CNAME, PTR
        nume, _ = decodeaza_nume_domeniu(pachet_complet, 
                                         pachet_complet.index(rdata))
        return nume
    elif tip == 15:  # MX
        preferinta = struct.unpack('>H', rdata[:2])[0]
        schimb, _ = decodeaza_nume_domeniu(pachet_complet,
                                           pachet_complet.index(rdata) + 2)
        return f"{preferinta} {schimb}"
    elif tip == 16:  # TXT
        return rdata[1:1 + rdata[0]].decode('utf-8', errors='ignore')
    else:
        return rdata.hex()


def interogare_dns(
    nume: str,
    tip_inregistrare: str = 'A',
    server: str = '8.8.8.8',
    port: int = 53,
    verbose: bool = False
) -> list[InregistrareDNS]:
    """
    Execută o interogare DNS.
    
    Args:
        nume: Numele de domeniu
        tip_inregistrare: Tipul înregistrării (A, AAAA, MX, NS, etc.)
        server: Serverul DNS de folosit
        port: Portul DNS
        verbose: Afișează detalii despre pachet
    
    Returns:
        Lista înregistrărilor găsite
    """
    # Construiește interogarea
    interogare = construieste_interogare_dns(nume, tip_inregistrare)
    
    if verbose:
        print(f"[Interogare DNS] {nume} {tip_inregistrare}")
        print(f"[Trimitere către] {server}:{port}")
        print(f"[Hexadecimal pachet]")
        for i in range(0, len(interogare), 16):
            hex_str = ' '.join(f'{b:02x}' for b in interogare[i:i+16])
            print(f"  {hex_str}")
        print()
    
    # Trimite interogarea
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5.0)
        sock.sendto(interogare, (server, port))
        raspuns, _ = sock.recvfrom(512)
    
    # Parsează răspunsul
    inregistrari, info_antet = parseaza_raspuns_dns(raspuns)
    
    if verbose:
        print("[Răspuns]")
        print(f"  Cod răspuns: {info_antet['rcode']}")
        print(f"  Înregistrări: {info_antet['ancount']} răspunsuri, "
              f"{info_antet['nscount']} autoritate, {info_antet['arcount']} adiționale")
        print()
    
    return inregistrari


def main():
    parser = argparse.ArgumentParser(
        description="Client DNS pentru interogări",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python ex_11_03_dns_client.py google.com A
  python ex_11_03_dns_client.py google.com MX --verbose
  python ex_11_03_dns_client.py google.com AAAA --server 1.1.1.1
        """
    )
    
    parser.add_argument(
        'domeniu',
        help='Numele de domeniu de interogat'
    )
    parser.add_argument(
        'tip',
        nargs='?',
        default='A',
        choices=['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT', 'SOA', 'PTR'],
        help='Tipul înregistrării (implicit: A)'
    )
    parser.add_argument(
        '--server', '-s',
        default='8.8.8.8',
        help='Serverul DNS de folosit (implicit: 8.8.8.8)'
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=53,
        help='Portul DNS (implicit: 53)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Afișează detalii despre pachetele DNS'
    )
    
    args = parser.parse_args()
    
    try:
        inregistrari = interogare_dns(
            args.domeniu,
            args.tip,
            args.server,
            args.port,
            args.verbose
        )
        
        if inregistrari:
            print(f"Rezultate pentru {args.domeniu} ({args.tip}):")
            print("-" * 50)
            for inr in inregistrari:
                print(f"  Nume: {inr.nume}")
                print(f"  Tip: {inr.tip}")
                print(f"  TTL: {inr.ttl}")
                print(f"  Date: {inr.date}")
                print()
        else:
            print(f"Nu s-au găsit înregistrări {args.tip} pentru {args.domeniu}")
            
    except socket.timeout:
        print(f"Eroare: Timeout la interogarea serverului {args.server}")
    except Exception as e:
        print(f"Eroare: {e}")


if __name__ == '__main__':
    main()
