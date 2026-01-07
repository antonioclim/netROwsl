#!/usr/bin/env python3
"""
Tema 1: Server DNS Extins
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Extindeți acest server DNS pentru a suporta înregistrări MX, CNAME și TXT.

TODO:
1. Implementați suport pentru înregistrări MX (Mail Exchange)
2. Implementați suport pentru înregistrări CNAME (Alias)
3. Implementați suport pentru înregistrări TXT

Consultați RFC 1035 pentru detalii despre structura înregistrărilor.
"""

import socket
from dnslib import DNSRecord, DNSHeader, RR, A, MX, CNAME, TXT, QTYPE

# ═══════════════════════════════════════════════════════════════
# CONFIGURAȚIE ÎNREGISTRĂRI DNS
# Extindeți aceste dicționare cu tipurile suplimentare
# ═══════════════════════════════════════════════════════════════

# Înregistrări A (Adresă IPv4)
INREGISTRARI_A = {
    "web.lab.local.": "172.20.0.10",
    "ssh.lab.local.": "172.20.0.22",
    "smtp.lab.local.": "172.20.0.30",
}

# TODO: Înregistrări MX (Mail Exchange)
# Format: domeniu -> (prioritate, server_mail)
INREGISTRARI_MX = {
    # Exemplu: "lab.local.": (10, "smtp.lab.local."),
}

# TODO: Înregistrări CNAME (Alias)
# Format: alias -> domeniu_real
INREGISTRARI_CNAME = {
    # Exemplu: "www.lab.local.": "web.lab.local.",
}

# TODO: Înregistrări TXT
# Format: domeniu -> text
INREGISTRARI_TXT = {
    # Exemplu: "lab.local.": "v=spf1 include:smtp.lab.local ~all",
}

PORT_DNS = 5353
GAZDA = "0.0.0.0"


def proceseaza_cerere(date: bytes) -> bytes:
    """
    Procesează o cerere DNS și returnează răspunsul.
    
    Args:
        date: Datele cererii DNS în format binar
    
    Returns:
        Răspunsul DNS în format binar
    """
    try:
        cerere = DNSRecord.parse(date)
        
        raspuns = DNSRecord(
            DNSHeader(id=cerere.header.id, qr=1, aa=1, ra=1),
            q=cerere.q
        )
        
        nume_domeniu = str(cerere.q.qname)
        tip_cerere = cerere.q.qtype
        
        print(f"[CERERE] {QTYPE[tip_cerere]} {nume_domeniu}")
        
        # Înregistrări de tip A
        if tip_cerere == QTYPE.A:
            if nume_domeniu in INREGISTRARI_A:
                raspuns.add_answer(
                    RR(cerere.q.qname, QTYPE.A,
                       rdata=A(INREGISTRARI_A[nume_domeniu]), ttl=300)
                )
            else:
                raspuns.header.rcode = 3  # NXDOMAIN
        
        # TODO: Implementați suport pentru MX
        elif tip_cerere == QTYPE.MX:
            # Implementați aici
            pass
        
        # TODO: Implementați suport pentru CNAME
        elif tip_cerere == QTYPE.CNAME:
            # Implementați aici
            pass
        
        # TODO: Implementați suport pentru TXT
        elif tip_cerere == QTYPE.TXT:
            # Implementați aici
            pass
        
        else:
            # Tip de înregistrare nesuportat
            raspuns.header.rcode = 4  # NOTIMP
        
        return raspuns.pack()
        
    except Exception as e:
        print(f"[EROARE] {e}")
        return b""


def main():
    """Pornește serverul DNS."""
    print("=" * 50)
    print("  Server DNS Extins - Tema 1")
    print("=" * 50)
    print(f"\n  Ascultare pe {GAZDA}:{PORT_DNS}/UDP")
    print("  Așteptare cereri...")
    print("-" * 50)
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((GAZDA, PORT_DNS))
        
        while True:
            try:
                date, adresa = sock.recvfrom(512)
                raspuns = proceseaza_cerere(date)
                if raspuns:
                    sock.sendto(raspuns, adresa)
            except KeyboardInterrupt:
                print("\nServer oprit.")
                break


if __name__ == "__main__":
    main()
