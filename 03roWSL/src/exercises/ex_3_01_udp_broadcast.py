#!/usr/bin/env python3
"""
Exercițiul 3.1: Transmisie UDP Broadcast
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Demonstrează comunicarea broadcast UDP folosind socket-uri Python.
Broadcast-ul permite transmiterea unui mesaj către toate dispozitivele
dintr-un segment de rețea simultan.

ANALOGIE: Broadcast-ul este ca un ANUNȚ PE MEGAFON într-o piață aglomerată.
    - Toți cei prezenți aud mesajul, indiferent dacă sunt interesați sau nu.
    - Nu poți alege cine aude - toată "piața" (rețeaua locală) primește.
    - Opțiunea SO_BROADCAST este "permisul de megafon" - fără ea, 
      sistemul refuză să transmită la adresa de broadcast.

Concepte cheie:
- Opțiunea socket SO_BROADCAST
- Adresa de broadcast limitat (255.255.255.255)
- Comunicarea fără conexiune (UDP)

PREDICȚIE pentru student: Înainte de a rula, gândește-te:
- La ce adresă trebuie să faci bind() receptorul? De ce nu la IP-ul specific?
- Ce se întâmplă dacă uiți SO_REUSEADDR și repornești rapid programul?
- Ce adresă MAC va avea pachetul la Layer 2?

Utilizare:
    Receptor:  python ex_3_01_udp_broadcast.py --mod receiver
    Emițător:  python ex_3_01_udp_broadcast.py --mod sender --numar 5 --mesaj "Salut!"
"""

import socket
import sys
import time
import argparse
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAȚIE
# ═══════════════════════════════════════════════════════════════════════════

PORT_BROADCAST = 5007
ADRESA_BROADCAST = '255.255.255.255'
DIMENSIUNE_BUFFER = 1024
MESAJ_IMPLICIT = 'Mesaj broadcast de test'


# ═══════════════════════════════════════════════════════════════════════════
# RECEPTOR BROADCAST
# ═══════════════════════════════════════════════════════════════════════════

def porneste_receptor(port: int = PORT_BROADCAST) -> None:
    """
    Pornește un receptor UDP care ascultă mesaje broadcast.
    
    ANALOGIE: Receptorul este ca o persoană în piață care ascultă anunțurile.
    Pentru a auzi TOATE anunțurile (inclusiv broadcast), trebuie să fie
    "în centrul pieței" (bind la 0.0.0.0), nu într-un colț specific.
    
    Pași implementați:
    1. Creează socket UDP
    2. Activează SO_REUSEADDR pentru rebindare rapidă
    3. Leagă socket-ul de toate interfețele (0.0.0.0)
    4. Așteaptă și afișează mesajele primite
    
    Args:
        port: Portul pe care să asculte
    """
    print("=" * 50)
    print("RECEPTOR UDP BROADCAST")
    print("=" * 50)
    print(f"Ascultare pe: 0.0.0.0:{port}")
    print("Apăsați Ctrl+C pentru oprire")
    print("-" * 50)
    
    # Creează socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Permite rebindarea rapidă a portului
    # Util când reporniți rapid receptorul
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Leagă la toate interfețele
    # IMPORTANT: Folosiți '0.0.0.0' nu o adresă specifică pentru a primi broadcast
    sock.bind(('0.0.0.0', port))
    
    numar_mesaje = 0
    
    try:
        while True:
            # Primește date și adresa expeditorului
            date, adresa_expeditor = sock.recvfrom(DIMENSIUNE_BUFFER)
            numar_mesaje += 1
            
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            mesaj = date.decode('utf-8', errors='replace')
            ip_expeditor, port_expeditor = adresa_expeditor
            
            print(f"[{timestamp}] #{numar_mesaje}")
            print(f"  De la: {ip_expeditor}:{port_expeditor}")
            print(f"  Lungime: {len(date)} bytes")
            print(f"  Mesaj: {mesaj}")
            print()
            
    except KeyboardInterrupt:
        print("\n" + "-" * 50)
        print(f"Receptor oprit. Total mesaje primite: {numar_mesaje}")
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════
# EMIȚĂTOR BROADCAST
# ═══════════════════════════════════════════════════════════════════════════

def porneste_emitator(
    mesaj: str = MESAJ_IMPLICIT,
    port: int = PORT_BROADCAST,
    numar_mesaje: int = 5,
    interval: float = 1.0
) -> None:
    """
    Transmite mesaje broadcast UDP.
    
    ANALOGIE: Emițătorul este persoana cu megafonul. Dar înainte de a striga,
    trebuie să obțină "permisul" (SO_BROADCAST). Fără acest permis, sistemul
    de operare refuză să transmită la adresa de broadcast.
    
    Pași implementați:
    1. Creează socket UDP
    2. Activează SO_BROADCAST (OBLIGATORIU pentru broadcast)
    3. Transmite mesaje la adresa de broadcast
    
    Args:
        mesaj: Mesajul de transmis
        port: Portul destinație
        numar_mesaje: Câte mesaje să transmită
        interval: Pauza între mesaje (secunde)
    """
    print("=" * 50)
    print("EMIȚĂTOR UDP BROADCAST")
    print("=" * 50)
    print(f"Destinație: {ADRESA_BROADCAST}:{port}")
    print(f"Mesaj: {mesaj}")
    print(f"Număr mesaje: {numar_mesaje}")
    print("-" * 50)
    
    # Creează socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # CRITIC: Activează opțiunea SO_BROADCAST
    # Fără această opțiune, sistemul va refuza să trimită la adresa de broadcast
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    try:
        for i in range(1, numar_mesaje + 1):
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            
            # Adaugă numărul mesajului pentru identificare
            mesaj_complet = f"[{i}/{numar_mesaje}] {mesaj}"
            
            # Transmite la adresa de broadcast
            bytes_trimisi = sock.sendto(
                mesaj_complet.encode('utf-8'),
                (ADRESA_BROADCAST, port)
            )
            
            print(f"[{timestamp}] Trimis mesajul {i}: {bytes_trimisi} bytes")
            
            if i < numar_mesaje:
                time.sleep(interval)
        
        print("-" * 50)
        print(f"Transmisie completă: {numar_mesaje} mesaje trimise")
        
    except PermissionError:
        print("EROARE: Permisiune refuzată pentru broadcast")
        print("  Pe Windows, rulați ca Administrator")
        print("  Sau folosiți containerele Docker")
    except Exception as e:
        print(f"EROARE: {e}")
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════
# PUNCT DE INTRARE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Parsează argumentele și pornește modul selectat."""
    parser = argparse.ArgumentParser(
        description='Demonstrație UDP Broadcast',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  Pornire receptor:
    python ex_3_01_udp_broadcast.py --mod receiver
    
  Trimitere mesaje:
    python ex_3_01_udp_broadcast.py --mod sender --numar 10 --mesaj "Test"
    
  Cu port personalizat:
    python ex_3_01_udp_broadcast.py --mod receiver --port 5555
        """
    )
    
    parser.add_argument(
        '--mod', '-m',
        type=str,
        required=True,
        choices=['sender', 'receiver', 'emitator', 'receptor'],
        help='Modul de operare: sender/emitator sau receiver/receptor'
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=PORT_BROADCAST,
        help=f'Portul UDP (implicit: {PORT_BROADCAST})'
    )
    parser.add_argument(
        '--mesaj', '-M',
        type=str,
        default=MESAJ_IMPLICIT,
        help='Mesajul de transmis (doar pentru emițător)'
    )
    parser.add_argument(
        '--numar', '-n',
        type=int,
        default=5,
        help='Numărul de mesaje de trimis (implicit: 5)'
    )
    parser.add_argument(
        '--interval', '-i',
        type=float,
        default=1.0,
        help='Interval între mesaje în secunde (implicit: 1.0)'
    )
    
    args = parser.parse_args()
    
    if args.mod in ['receiver', 'receptor']:
        porneste_receptor(port=args.port)
    else:
        porneste_emitator(
            mesaj=args.mesaj,
            port=args.port,
            numar_mesaje=args.numar,
            interval=args.interval
        )


if __name__ == '__main__':
    main()
