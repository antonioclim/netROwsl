#!/usr/bin/env python3
"""
Exercițiul 1.03: Parsarea Datelor CSV din Capturi de Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu demonstrează procesarea datelor de rețea exportate în format CSV.
Veți învăța să extrageți și să analizați informații din capturi de trafic.

Concepte cheie:
- Exportul datelor din tshark în format CSV
- Parsarea și procesarea datelor tabulare
- Analiza statistică a traficului de rețea
- Agregarea datelor pe diverse criterii

Rulare:
    python ex_1_03_parsare_csv.py
    python ex_1_03_parsare_csv.py --fisier date_captura.csv
"""

from __future__ import annotations

import csv
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class PachetRetea:
    """Reprezintă un pachet de rețea parsat din CSV."""
    numar_cadru: int
    timp_relativ: float
    ip_sursa: str
    ip_destinatie: str
    port_sursa: Optional[int]
    port_destinatie: Optional[int]
    protocol: str
    lungime: int


def genereaza_date_exemplu() -> str:
    """Generează un fișier CSV de exemplu pentru demonstrație.
    
    Returns:
        Calea către fișierul generat
    """
    date_exemplu = """frame_number,frame_time_relative,ip_src,ip_dst,tcp_srcport,tcp_dstport,frame_len
1,0.000000,192.168.1.100,93.184.216.34,52341,80,74
2,0.023456,93.184.216.34,192.168.1.100,80,52341,74
3,0.045123,192.168.1.100,93.184.216.34,52341,80,66
4,0.089234,192.168.1.100,93.184.216.34,52341,80,583
5,0.112456,93.184.216.34,192.168.1.100,80,52341,1514
6,0.134567,93.184.216.34,192.168.1.100,80,52341,1514
7,0.156789,192.168.1.100,93.184.216.34,52341,80,66
8,0.178901,93.184.216.34,192.168.1.100,80,52341,892
9,0.201234,192.168.1.100,93.184.216.34,52341,80,66
10,0.223456,192.168.1.100,93.184.216.34,52341,80,66
11,0.245678,93.184.216.34,192.168.1.100,80,52341,66
12,0.267890,192.168.1.100,93.184.216.34,52341,80,66
13,0.312345,192.168.1.100,8.8.8.8,54321,53,72
14,0.345678,8.8.8.8,192.168.1.100,53,54321,156
15,0.378901,192.168.1.100,172.217.16.142,52342,443,583
16,0.401234,172.217.16.142,192.168.1.100,443,52342,1514
17,0.423456,192.168.1.100,172.217.16.142,52342,443,66
18,0.445678,172.217.16.142,192.168.1.100,443,52342,1514
19,0.467890,192.168.1.100,172.217.16.142,52342,443,66
20,0.490123,172.217.16.142,192.168.1.100,443,52342,456"""
    
    cale_fisier = Path("/tmp/date_retea_exemplu.csv")
    cale_fisier.write_text(date_exemplu)
    
    return str(cale_fisier)


def parseaza_csv(cale_fisier: str) -> List[PachetRetea]:
    """Parsează un fișier CSV cu date de rețea.
    
    Args:
        cale_fisier: Calea către fișierul CSV
        
    Returns:
        Lista de pachete parsate
    """
    pachete = []
    
    with open(cale_fisier, 'r', newline='') as f:
        cititor = csv.DictReader(f)
        
        for rand in cititor:
            try:
                pachet = PachetRetea(
                    numar_cadru=int(rand.get('frame_number', 0)),
                    timp_relativ=float(rand.get('frame_time_relative', 0)),
                    ip_sursa=rand.get('ip_src', '') or rand.get('ip.src', ''),
                    ip_destinatie=rand.get('ip_dst', '') or rand.get('ip.dst', ''),
                    port_sursa=int(rand.get('tcp_srcport', 0) or rand.get('udp_srcport', 0) or 0) or None,
                    port_destinatie=int(rand.get('tcp_dstport', 0) or rand.get('udp_dstport', 0) or 0) or None,
                    protocol=determina_protocol(rand),
                    lungime=int(rand.get('frame_len', 0) or rand.get('frame.len', 0))
                )
                pachete.append(pachet)
            except (ValueError, KeyError) as e:
                print(f"⚠ Eroare la parsarea rândului: {e}")
                continue
    
    return pachete


def determina_protocol(rand: Dict[str, Any]) -> str:
    """Determină protocolul din datele rândului.
    
    Args:
        rand: Dicționarul cu datele rândului
        
    Returns:
        Numele protocolului
    """
    if rand.get('tcp_srcport') or rand.get('tcp_dstport'):
        port_dst = int(rand.get('tcp_dstport', 0) or 0)
        if port_dst == 80:
            return "HTTP"
        elif port_dst == 443:
            return "HTTPS"
        elif port_dst == 22:
            return "SSH"
        return "TCP"
    elif rand.get('udp_srcport') or rand.get('udp_dstport'):
        port_dst = int(rand.get('udp_dstport', 0) or 0)
        if port_dst == 53:
            return "DNS"
        return "UDP"
    return "Necunoscut"


def analizeaza_pachete(pachete: List[PachetRetea]) -> Dict[str, Any]:
    """Analizează lista de pachete și calculează statistici.
    
    Args:
        pachete: Lista de pachete de analizat
        
    Returns:
        Dicționar cu statisticile calculate
    """
    if not pachete:
        return {}
    
    # Statistici de bază
    lungimi = [p.lungime for p in pachete]
    timpuri = [p.timp_relativ for p in pachete]
    
    # Agregare per IP sursă
    trafic_per_ip_sursa = defaultdict(lambda: {'pachete': 0, 'octeti': 0})
    for p in pachete:
        trafic_per_ip_sursa[p.ip_sursa]['pachete'] += 1
        trafic_per_ip_sursa[p.ip_sursa]['octeti'] += p.lungime
    
    # Agregare per IP destinație
    trafic_per_ip_dest = defaultdict(lambda: {'pachete': 0, 'octeti': 0})
    for p in pachete:
        trafic_per_ip_dest[p.ip_destinatie]['pachete'] += 1
        trafic_per_ip_dest[p.ip_destinatie]['octeti'] += p.lungime
    
    # Agregare per protocol
    trafic_per_protocol = defaultdict(lambda: {'pachete': 0, 'octeti': 0})
    for p in pachete:
        trafic_per_protocol[p.protocol]['pachete'] += 1
        trafic_per_protocol[p.protocol]['octeti'] += p.lungime
    
    # Agregare per port destinație
    trafic_per_port = defaultdict(lambda: {'pachete': 0, 'octeti': 0})
    for p in pachete:
        if p.port_destinatie:
            trafic_per_port[p.port_destinatie]['pachete'] += 1
            trafic_per_port[p.port_destinatie]['octeti'] += p.lungime
    
    return {
        'total_pachete': len(pachete),
        'total_octeti': sum(lungimi),
        'lungime_medie': sum(lungimi) / len(lungimi),
        'lungime_min': min(lungimi),
        'lungime_max': max(lungimi),
        'durata_captura': max(timpuri) - min(timpuri),
        'trafic_per_ip_sursa': dict(trafic_per_ip_sursa),
        'trafic_per_ip_dest': dict(trafic_per_ip_dest),
        'trafic_per_protocol': dict(trafic_per_protocol),
        'trafic_per_port': dict(trafic_per_port),
    }


def formateaza_octeti(octeti: int) -> str:
    """Formatează o valoare în octeți într-un format citibil.
    
    Args:
        octeti: Numărul de octeți
        
    Returns:
        Șir formatat
    """
    for unitate in ['B', 'KB', 'MB', 'GB']:
        if abs(octeti) < 1024.0:
            return f"{octeti:.1f} {unitate}"
        octeti /= 1024.0
    return f"{octeti:.1f} TB"


def afiseaza_rezultate(statistici: Dict[str, Any]) -> None:
    """Afișează rezultatele analizei într-un format citibil.
    
    Args:
        statistici: Dicționarul cu statisticile
    """
    print("\n" + "=" * 60)
    print("  REZULTATELE ANALIZEI CSV")
    print("=" * 60)
    
    # Statistici generale
    print("\n📊 STATISTICI GENERALE")
    print("-" * 40)
    print(f"  Total pachete:        {statistici['total_pachete']}")
    print(f"  Total date:           {formateaza_octeti(statistici['total_octeti'])}")
    print(f"  Dimensiune medie:     {statistici['lungime_medie']:.1f} octeți")
    print(f"  Dimensiune minimă:    {statistici['lungime_min']} octeți")
    print(f"  Dimensiune maximă:    {statistici['lungime_max']} octeți")
    print(f"  Durata capturii:      {statistici['durata_captura']:.3f} secunde")
    
    # Trafic per protocol
    print("\n📡 TRAFIC PER PROTOCOL")
    print("-" * 40)
    for protocol, date in sorted(
        statistici['trafic_per_protocol'].items(),
        key=lambda x: x[1]['octeti'],
        reverse=True
    ):
        procent = (date['octeti'] / statistici['total_octeti']) * 100
        print(f"  {protocol:12} {date['pachete']:5} pachete  "
              f"{formateaza_octeti(date['octeti']):>10}  ({procent:.1f}%)")
    
    # Top IP-uri sursă
    print("\n🔼 TOP 5 IP-URI SURSĂ (după volum)")
    print("-" * 40)
    top_surse = sorted(
        statistici['trafic_per_ip_sursa'].items(),
        key=lambda x: x[1]['octeti'],
        reverse=True
    )[:5]
    for ip, date in top_surse:
        print(f"  {ip:18} {date['pachete']:5} pachete  "
              f"{formateaza_octeti(date['octeti']):>10}")
    
    # Top IP-uri destinație
    print("\n🔽 TOP 5 IP-URI DESTINAȚIE (după volum)")
    print("-" * 40)
    top_dest = sorted(
        statistici['trafic_per_ip_dest'].items(),
        key=lambda x: x[1]['octeti'],
        reverse=True
    )[:5]
    for ip, date in top_dest:
        print(f"  {ip:18} {date['pachete']:5} pachete  "
              f"{formateaza_octeti(date['octeti']):>10}")
    
    # Top porturi
    print("\n🚪 TOP 5 PORTURI DESTINAȚIE (după volum)")
    print("-" * 40)
    top_porturi = sorted(
        statistici['trafic_per_port'].items(),
        key=lambda x: x[1]['octeti'],
        reverse=True
    )[:5]
    
    # Mapare porturi cunoscute
    porturi_cunoscute = {
        20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet",
        25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3",
        143: "IMAP", 443: "HTTPS", 993: "IMAPS", 995: "POP3S"
    }
    
    for port, date in top_porturi:
        nume_serviciu = porturi_cunoscute.get(port, "")
        eticheta = f"{port} ({nume_serviciu})" if nume_serviciu else str(port)
        print(f"  {eticheta:18} {date['pachete']:5} pachete  "
              f"{formateaza_octeti(date['octeti']):>10}")
    
    print("\n" + "=" * 60)


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Parsarea și Analiza Datelor CSV din Capturi de Rețea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python ex_1_03_parsare_csv.py                    # Folosește date de exemplu
  python ex_1_03_parsare_csv.py --fisier date.csv  # Folosește fișier propriu

Generare CSV din tshark:
  tshark -r captura.pcap -T fields -E header=y -E separator=, \\
      -e frame.number -e frame.time_relative -e ip.src -e ip.dst \\
      -e tcp.srcport -e tcp.dstport -e frame.len > date.csv
        """
    )
    parser.add_argument(
        "--fisier", "-f",
        help="Calea către fișierul CSV de analizat"
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  EXERCIȚIUL 1.03: PARSAREA DATELOR CSV".center(58) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    try:
        # Determină fișierul de folosit
        if args.fisier:
            cale_fisier = args.fisier
            if not Path(cale_fisier).exists():
                print(f"\n✗ Fișierul nu există: {cale_fisier}")
                return 1
        else:
            print("\n📁 Se generează date de exemplu...")
            cale_fisier = genereaza_date_exemplu()
            print(f"   Fișier creat: {cale_fisier}")
        
        # Parsează fișierul
        print(f"\n📖 Se parsează fișierul: {cale_fisier}")
        pachete = parseaza_csv(cale_fisier)
        print(f"   Pachete găsite: {len(pachete)}")
        
        if not pachete:
            print("\n⚠ Nu s-au găsit pachete în fișier")
            return 1
        
        # Analizează și afișează rezultatele
        statistici = analizeaza_pachete(pachete)
        afiseaza_rezultate(statistici)
        
        return 0

    except KeyboardInterrupt:
        print("\n\n⚠ Întrerupt de utilizator")
        return 130
    except Exception as e:
        print(f"\n✗ Eroare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
