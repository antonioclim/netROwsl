#!/usr/bin/env python3
"""
Exercițiul 3.2: Comunicare UDP Multicast
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Demonstrează comunicarea multicast UDP folosind socket-uri Python.
Multicast-ul permite transmiterea eficientă către un grup selectat
de receptori, folosind protocoalul IGMP pentru gestionarea apartenenței.

ANALOGIE: Multicast-ul este ca un GRUP DE WHATSAPP:
    - Creezi un grup (adresa multicast, ex: 239.0.0.1)
    - Oamenii se alătură voluntar (IGMP Join / IP_ADD_MEMBERSHIP)
    - Mesajele ajung DOAR la membri, nu la toată lumea
    - Poți pleca oricând (IGMP Leave / IP_DROP_MEMBERSHIP)
    - TTL-ul este ca un "bilet de metrou valabil N stații" - la fiecare 
      router traversat, se consumă o "stație". TTL=0 = doar local.

Concepte cheie:
- Adrese multicast (224.0.0.0 - 239.255.255.255)
- Protocolul IGMP (Internet Group Management Protocol)
- Opțiunile socket IP_ADD_MEMBERSHIP și IP_MULTICAST_TTL
- Diferența dintre broadcast și multicast

PREDICȚIE pentru student: Înainte de a rula, gândește-te:
- Ce mesaj IGMP trimite receptorul când pornește? (Join sau Leave?)
- Dacă TTL=0, cine va primi pachetele?
- De ce multicast e mai eficient decât broadcast pentru 10 receptori din 100?

Utilizare:
    Receptor:  python ex_3_02_udp_multicast.py --mod receiver
    Emițător:  python ex_3_02_udp_multicast.py --mod sender --numar 5
"""

import socket
import struct
import sys
import time
import argparse
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAȚIE
# ═══════════════════════════════════════════════════════════════════════════

# Adresă multicast din intervalul administrativ scoped (239.x.x.x)
# Acest interval este destinat utilizării locale/organizaționale
GRUP_MULTICAST = '239.0.0.1'
PORT_MULTICAST = 5008
DIMENSIUNE_BUFFER = 1024
MESAJ_IMPLICIT = 'Mesaj multicast de test'

# TTL (Time To Live) pentru pachete multicast
# 1 = doar rețeaua locală
# 32 = organizație
# 64 = regiune
# 128 = continent
# 255 = nelimitat
TTL_MULTICAST = 1


# ═══════════════════════════════════════════════════════════════════════════
# RECEPTOR MULTICAST
# ═══════════════════════════════════════════════════════════════════════════

def porneste_receptor(
    grup: str = GRUP_MULTICAST,
    port: int = PORT_MULTICAST
) -> None:
    """
    Pornește un receptor UDP care se alătură unui grup multicast.
    
    ANALOGIE: Este ca să te alături unui grup de WhatsApp:
    1. Deschizi aplicația (creezi socket-ul)
    2. Te abonezi la grup (IP_ADD_MEMBERSHIP trimite IGMP Join)
    3. Primești mesajele grupului
    4. Când pleci, anunți (IP_DROP_MEMBERSHIP trimite IGMP Leave)
    
    Pași implementați:
    1. Creează socket UDP
    2. Activează SO_REUSEADDR pentru multiple receptoare pe același port
    3. Leagă socket-ul la port
    4. Se alătură grupului multicast (IGMP Join)
    5. Primește și afișează mesajele
    
    Args:
        grup: Adresa grupului multicast
        port: Portul pe care să asculte
    """
    print("=" * 50)
    print("RECEPTOR UDP MULTICAST")
    print("=" * 50)
    print(f"Grup multicast: {grup}")
    print(f"Port: {port}")
    print("Apăsați Ctrl+C pentru oprire")
    print("-" * 50)
    
    # Creează socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Permite mai multe bind-uri pe același port
    # Necesar pentru mai mulți receptori pe aceeași mașină
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Leagă socket-ul
    # Notă: Pe unele sisteme trebuie să legați la grupul multicast,
    # pe altele la '' sau '0.0.0.0'
    sock.bind(('', port))
    
    # ═══════════════════════════════════════════════════════════════════════
    # ÎNSCRIEREA ÎN GRUP - PARTEA CRITICĂ
    # ═══════════════════════════════════════════════════════════════════════
    
    # Construiește structura pentru IP_ADD_MEMBERSHIP
    # Format: 4 bytes adresă grup + 4 bytes interfață locală
    # 
    # inet_aton() convertește adresa în format binar (network byte order)
    # '0.0.0.0' pentru interfață înseamnă "toate interfețele"
    
    mreq = struct.pack(
        '4s4s',
        socket.inet_aton(grup),      # Adresa grupului multicast
        socket.inet_aton('0.0.0.0')  # Interfața (toate)
    )
    
    # Trimite IGMP Membership Report
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    print(f"Înscris în grupul multicast {grup}")
    print("Așteptare mesaje...")
    print()
    
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
        # Părăsește grupul multicast (IGMP Leave)
        # Opțional dar recomandat pentru curățare corectă
        try:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
            print(f"Părăsit grupul multicast {grup}")
        except Exception:
            pass
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════
# EMIȚĂTOR MULTICAST
# ═══════════════════════════════════════════════════════════════════════════

def porneste_emitator(
    mesaj: str = MESAJ_IMPLICIT,
    grup: str = GRUP_MULTICAST,
    port: int = PORT_MULTICAST,
    numar_mesaje: int = 5,
    interval: float = 1.0,
    ttl: int = TTL_MULTICAST
) -> None:
    """
    Transmite mesaje UDP către un grup multicast.
    
    ANALOGIE: Emițătorul este ca administratorul grupului WhatsApp care 
    trimite mesaje. Nu trebuie să fie membru pentru a trimite - doar 
    membrii primesc. TTL-ul controlează "cât de departe" ajunge mesajul:
    TTL=1 = doar rețeaua locală, TTL=32 = poate traversa routere interne.
    
    Pași implementați:
    1. Creează socket UDP
    2. Configurează TTL pentru multicast
    3. Transmite mesaje către adresa grupului
    
    Args:
        mesaj: Mesajul de transmis
        grup: Adresa grupului multicast
        port: Portul destinație
        numar_mesaje: Câte mesaje să transmită
        interval: Pauza între mesaje
        ttl: Time To Live pentru pachete
    """
    print("=" * 50)
    print("EMIȚĂTOR UDP MULTICAST")
    print("=" * 50)
    print(f"Grup multicast: {grup}:{port}")
    print(f"TTL: {ttl}")
    print(f"Mesaj: {mesaj}")
    print(f"Număr mesaje: {numar_mesaje}")
    print("-" * 50)
    
    # Creează socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # ═══════════════════════════════════════════════════════════════════════
    # CONFIGURARE TTL
    # ═══════════════════════════════════════════════════════════════════════
    
    # TTL controlează cât de departe pot călători pachetele multicast
    # Fiecare router decrementează TTL-ul cu 1
    # Când TTL ajunge la 0, pachetul este eliminat
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    
    # Opțional: Dezactivează primirea propriilor mesaje (loopback)
    # Util când emițătorul nu vrea să primească ce trimite
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    
    try:
        for i in range(1, numar_mesaje + 1):
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            
            mesaj_complet = f"[{i}/{numar_mesaje}] {mesaj}"
            
            # Transmite către grupul multicast
            # Notă: Nu este necesară înscrierea în grup pentru a transmite
            bytes_trimisi = sock.sendto(
                mesaj_complet.encode('utf-8'),
                (grup, port)
            )
            
            print(f"[{timestamp}] Trimis mesajul {i} către {grup}: {bytes_trimisi} bytes")
            
            if i < numar_mesaje:
                time.sleep(interval)
        
        print("-" * 50)
        print(f"Transmisie completă: {numar_mesaje} mesaje trimise")
        
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
        description='Demonstrație UDP Multicast',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  Pornire receptor:
    python ex_3_02_udp_multicast.py --mod receiver
    
  Trimitere mesaje:
    python ex_3_02_udp_multicast.py --mod sender --numar 10 --mesaj "Test"
    
  Cu grup personalizat:
    python ex_3_02_udp_multicast.py --mod receiver --grup 239.1.1.1 --port 5555
    
Intervale de adrese multicast:
  224.0.0.0   - 224.0.0.255   : Local Network Control (nu traversează routere)
  224.0.1.0   - 224.0.1.255   : Internetwork Control
  239.0.0.0   - 239.255.255.255 : Administratively Scoped (recomandat pentru teste)
        """
    )
    
    parser.add_argument(
        '--mod', '-m',
        type=str,
        required=True,
        choices=['sender', 'receiver', 'emitator', 'receptor'],
        help='Modul de operare'
    )
    parser.add_argument(
        '--grup', '-g',
        type=str,
        default=GRUP_MULTICAST,
        help=f'Adresa grupului multicast (implicit: {GRUP_MULTICAST})'
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=PORT_MULTICAST,
        help=f'Portul UDP (implicit: {PORT_MULTICAST})'
    )
    parser.add_argument(
        '--mesaj', '-M',
        type=str,
        default=MESAJ_IMPLICIT,
        help='Mesajul de transmis'
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
    parser.add_argument(
        '--ttl', '-t',
        type=int,
        default=TTL_MULTICAST,
        help=f'TTL pentru pachete multicast (implicit: {TTL_MULTICAST})'
    )
    
    args = parser.parse_args()
    
    if args.mod in ['receiver', 'receptor']:
        porneste_receptor(grup=args.grup, port=args.port)
    else:
        porneste_emitator(
            mesaj=args.mesaj,
            grup=args.grup,
            port=args.port,
            numar_mesaje=args.numar,
            interval=args.interval,
            ttl=args.ttl
        )


if __name__ == '__main__':
    main()
