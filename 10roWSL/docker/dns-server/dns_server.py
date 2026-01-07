#!/usr/bin/env python3
"""
Server DNS pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Server DNS simplu care rezolvă domenii *.lab.local folosind dnslib.
"""

import socket
from dnslib import DNSRecord, DNSHeader, RR, A, QTYPE

# Configurație înregistrări DNS
# Format: domeniu -> adresă IP
INREGISTRARI_DNS = {
    "myservice.lab.local.": "10.10.10.10",
    "api.lab.local.": "10.10.10.20",
    "web.lab.local.": "172.20.0.10",
    "dns.lab.local.": "172.20.0.53",
    "ssh.lab.local.": "172.20.0.22",
    "ftp.lab.local.": "172.20.0.21",
    "debug.lab.local.": "172.20.0.200",
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
        
        # Creează răspunsul
        raspuns = DNSRecord(
            DNSHeader(id=cerere.header.id, qr=1, aa=1, ra=1),
            q=cerere.q
        )
        
        # Obține numele domeniului din cerere
        nume_domeniu = str(cerere.q.qname)
        tip_cerere = cerere.q.qtype
        
        print(f"[CERERE] {QTYPE[tip_cerere]} {nume_domeniu}")
        
        # Răspunde doar la cereri de tip A (adresă IPv4)
        if tip_cerere == QTYPE.A:
            if nume_domeniu in INREGISTRARI_DNS:
                adresa_ip = INREGISTRARI_DNS[nume_domeniu]
                raspuns.add_answer(
                    RR(cerere.q.qname, QTYPE.A, rdata=A(adresa_ip), ttl=300)
                )
                print(f"[RĂSPUNS] {nume_domeniu} -> {adresa_ip}")
            else:
                # NXDOMAIN pentru domenii necunoscute
                raspuns.header.rcode = 3  # NXDOMAIN
                print(f"[RĂSPUNS] {nume_domeniu} -> NXDOMAIN")
        
        return raspuns.pack()
        
    except Exception as e:
        print(f"[EROARE] Procesare cerere: {e}")
        return b""


def main():
    """Funcția principală - pornește serverul DNS."""
    print("=" * 50)
    print("  Server DNS - Laborator Săptămâna 10")
    print("=" * 50)
    print()
    print(f"  Ascultare pe {GAZDA}:{PORT_DNS}/UDP")
    print()
    print("  Înregistrări configurate:")
    for domeniu, ip in INREGISTRARI_DNS.items():
        print(f"    {domeniu:30} -> {ip}")
    print()
    print("  Așteptare cereri...")
    print("-" * 50)
    
    # Creează socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((GAZDA, PORT_DNS))
        
        while True:
            try:
                # Primește cerere
                date, adresa_client = sock.recvfrom(512)
                
                # Procesează și trimite răspuns
                raspuns = proceseaza_cerere(date)
                if raspuns:
                    sock.sendto(raspuns, adresa_client)
                    
            except KeyboardInterrupt:
                print("\nServer oprit.")
                break
            except Exception as e:
                print(f"[EROARE] {e}")


if __name__ == "__main__":
    main()
