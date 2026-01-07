#!/usr/bin/env python3
"""
Exercițiul 4: Analiza Statisticilor din Fișiere PCAP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script demonstrează cum să extrageți și să analizați statistici
din fișiere de captură de pachete (PCAP) folosind Python.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class StatisticiPCAP:
    """Clasă pentru stocarea statisticilor unui fișier PCAP."""
    cale_fisier: Path
    total_pachete: int = 0
    total_octeti: int = 0
    durata_secunde: float = 0.0
    protocoale: Dict[str, int] = field(default_factory=dict)
    adrese_sursa: Dict[str, int] = field(default_factory=dict)
    adrese_destinatie: Dict[str, int] = field(default_factory=dict)
    porturi: Dict[int, int] = field(default_factory=dict)
    
    @property
    def dimensiune_medie_pachet(self) -> float:
        """Calculează dimensiunea medie a pachetelor."""
        if self.total_pachete == 0:
            return 0.0
        return self.total_octeti / self.total_pachete
    
    @property
    def rata_transfer(self) -> float:
        """Calculează rata de transfer în bytes/secundă."""
        if self.durata_secunde == 0:
            return 0.0
        return self.total_octeti / self.durata_secunde


def analizeaza_cu_tshark(cale_pcap: Path) -> Optional[StatisticiPCAP]:
    """Analizează un fișier PCAP folosind tshark.
    
    Args:
        cale_pcap: Calea către fișierul PCAP
        
    Returns:
        Obiect StatisticiPCAP sau None în caz de eroare
    """
    if not cale_pcap.exists():
        print(f"Eroare: Fișierul {cale_pcap} nu există")
        return None
    
    stats = StatisticiPCAP(cale_fisier=cale_pcap)
    
    try:
        # Obține informațiile de bază despre captură
        rezultat = subprocess.run(
            ["tshark", "-r", str(cale_pcap), "-q", "-z", "io,stat,0"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if rezultat.returncode != 0:
            print(f"Eroare tshark: {rezultat.stderr}")
            return None
        
        # Parsează statisticile I/O
        for linie in rezultat.stdout.split("\n"):
            if "<>" in linie and "|" in linie:
                parti = linie.split("|")
                if len(parti) >= 3:
                    try:
                        stats.total_pachete = int(parti[1].strip())
                        stats.total_octeti = int(parti[2].strip())
                    except ValueError:
                        pass
        
        # Obține distribuția protocoalelor
        rezultat = subprocess.run(
            ["tshark", "-r", str(cale_pcap), "-q", "-z", "io,phs"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if rezultat.returncode == 0:
            for linie in rezultat.stdout.split("\n"):
                linie = linie.strip()
                if linie and not linie.startswith("=") and not linie.startswith("Protocol"):
                    parti = linie.split()
                    if len(parti) >= 2:
                        protocol = parti[0]
                        try:
                            numar = int(parti[1])
                            stats.protocoale[protocol] = numar
                        except ValueError:
                            pass
        
        # Obține conversațiile IP
        rezultat = subprocess.run(
            ["tshark", "-r", str(cale_pcap), "-q", "-z", "conv,ip"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if rezultat.returncode == 0:
            for linie in rezultat.stdout.split("\n"):
                if "<->" in linie:
                    parti = linie.split("<->")
                    if len(parti) >= 2:
                        sursa = parti[0].strip().split()[0] if parti[0].strip() else ""
                        dest = parti[1].strip().split()[0] if parti[1].strip() else ""
                        if sursa:
                            stats.adrese_sursa[sursa] = stats.adrese_sursa.get(sursa, 0) + 1
                        if dest:
                            stats.adrese_destinatie[dest] = stats.adrese_destinatie.get(dest, 0) + 1
        
        return stats
        
    except subprocess.TimeoutExpired:
        print("Eroare: Timeout la analiza fișierului")
        return None
    except FileNotFoundError:
        print("Eroare: tshark nu este instalat")
        return None
    except Exception as e:
        print(f"Eroare neașteptată: {e}")
        return None


def analizeaza_manual(cale_pcap: Path) -> Optional[StatisticiPCAP]:
    """Analizează un fișier PCAP folosind câmpuri exportate.
    
    Args:
        cale_pcap: Calea către fișierul PCAP
        
    Returns:
        Obiect StatisticiPCAP sau None în caz de eroare
    """
    if not cale_pcap.exists():
        print(f"Eroare: Fișierul {cale_pcap} nu există")
        return None
    
    stats = StatisticiPCAP(cale_fisier=cale_pcap)
    
    try:
        # Exportă câmpuri specifice
        rezultat = subprocess.run(
            [
                "tshark", "-r", str(cale_pcap),
                "-T", "fields",
                "-e", "frame.number",
                "-e", "frame.time_relative",
                "-e", "frame.len",
                "-e", "ip.src",
                "-e", "ip.dst",
                "-e", "ip.proto",
                "-e", "tcp.srcport",
                "-e", "tcp.dstport",
                "-e", "udp.srcport",
                "-e", "udp.dstport",
                "-E", "header=n",
                "-E", "separator=,"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if rezultat.returncode != 0:
            return None
        
        timp_maxim = 0.0
        
        for linie in rezultat.stdout.strip().split("\n"):
            if not linie:
                continue
            
            campuri = linie.split(",")
            if len(campuri) < 6:
                continue
            
            stats.total_pachete += 1
            
            # Timp relativ
            try:
                timp = float(campuri[1]) if campuri[1] else 0.0
                if timp > timp_maxim:
                    timp_maxim = timp
            except ValueError:
                pass
            
            # Dimensiune pachet
            try:
                dimensiune = int(campuri[2]) if campuri[2] else 0
                stats.total_octeti += dimensiune
            except ValueError:
                pass
            
            # Adrese IP
            if campuri[3]:
                stats.adrese_sursa[campuri[3]] = stats.adrese_sursa.get(campuri[3], 0) + 1
            if campuri[4]:
                stats.adrese_destinatie[campuri[4]] = stats.adrese_destinatie.get(campuri[4], 0) + 1
            
            # Protocol
            try:
                proto = int(campuri[5]) if campuri[5] else 0
                if proto == 6:
                    stats.protocoale["TCP"] = stats.protocoale.get("TCP", 0) + 1
                elif proto == 17:
                    stats.protocoale["UDP"] = stats.protocoale.get("UDP", 0) + 1
                elif proto == 1:
                    stats.protocoale["ICMP"] = stats.protocoale.get("ICMP", 0) + 1
            except ValueError:
                pass
            
            # Porturi
            for idx in [6, 7, 8, 9]:  # tcp.srcport, tcp.dstport, udp.srcport, udp.dstport
                if idx < len(campuri) and campuri[idx]:
                    try:
                        port = int(campuri[idx])
                        stats.porturi[port] = stats.porturi.get(port, 0) + 1
                    except ValueError:
                        pass
        
        stats.durata_secunde = timp_maxim
        return stats
        
    except Exception as e:
        print(f"Eroare la analiza manuală: {e}")
        return None


def afiseaza_statistici(stats: StatisticiPCAP) -> None:
    """Afișează statisticile într-un format lizibil.
    
    Args:
        stats: Obiectul StatisticiPCAP de afișat
    """
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  STATISTICI PCAP".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    print(f"Fișier: {stats.cale_fisier.name}")
    print("-" * 60)
    
    print(f"\n{'REZUMAT GENERAL':}")
    print(f"  Total pachete:          {stats.total_pachete:,}")
    print(f"  Total octeți:           {stats.total_octeti:,}")
    print(f"  Dimensiune medie:       {stats.dimensiune_medie_pachet:.1f} octeți/pachet")
    print(f"  Durată captură:         {stats.durata_secunde:.2f} secunde")
    print(f"  Rata de transfer:       {stats.rata_transfer:.1f} octeți/s")
    
    if stats.protocoale:
        print(f"\n{'DISTRIBUȚIE PROTOCOALE':}")
        for protocol, numar in sorted(stats.protocoale.items(), key=lambda x: -x[1])[:10]:
            procent = (numar / stats.total_pachete * 100) if stats.total_pachete > 0 else 0
            print(f"  {protocol:20} {numar:8,} ({procent:5.1f}%)")
    
    if stats.adrese_sursa:
        print(f"\n{'TOP 5 ADRESE SURSĂ':}")
        for ip, numar in sorted(stats.adrese_sursa.items(), key=lambda x: -x[1])[:5]:
            print(f"  {ip:20} {numar:8,} pachete")
    
    if stats.adrese_destinatie:
        print(f"\n{'TOP 5 ADRESE DESTINAȚIE':}")
        for ip, numar in sorted(stats.adrese_destinatie.items(), key=lambda x: -x[1])[:5]:
            print(f"  {ip:20} {numar:8,} pachete")
    
    if stats.porturi:
        print(f"\n{'TOP 10 PORTURI':}")
        for port, numar in sorted(stats.porturi.items(), key=lambda x: -x[1])[:10]:
            serviciu = obtine_nume_serviciu(port)
            print(f"  {port:5} ({serviciu:10}) {numar:8,} pachete")
    
    print()


def obtine_nume_serviciu(port: int) -> str:
    """Returnează numele serviciului pentru un port comun.
    
    Args:
        port: Numărul portului
        
    Returns:
        Numele serviciului sau "necunoscut"
    """
    servicii = {
        20: "FTP-Data",
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S",
        3306: "MySQL",
        5432: "PostgreSQL",
        6379: "Redis",
        8080: "HTTP-Alt",
        9090: "Lab-TCP",
        9091: "Lab-UDP",
    }
    return servicii.get(port, "necunoscut")


def genereaza_raport(stats: StatisticiPCAP, cale_raport: Path) -> None:
    """Generează un raport Markdown cu statisticile.
    
    Args:
        stats: Obiectul StatisticiPCAP
        cale_raport: Calea pentru raportul de ieșire
    """
    with open(cale_raport, "w", encoding="utf-8") as f:
        f.write("# Raport Analiză PCAP\n\n")
        f.write(f"**Fișier:** `{stats.cale_fisier.name}`\n\n")
        
        f.write("## Rezumat General\n\n")
        f.write(f"| Metrică | Valoare |\n")
        f.write(f"|---------|--------|\n")
        f.write(f"| Total pachete | {stats.total_pachete:,} |\n")
        f.write(f"| Total octeți | {stats.total_octeti:,} |\n")
        f.write(f"| Dimensiune medie | {stats.dimensiune_medie_pachet:.1f} octeți |\n")
        f.write(f"| Durată | {stats.durata_secunde:.2f} s |\n")
        f.write(f"| Rata transfer | {stats.rata_transfer:.1f} B/s |\n\n")
        
        if stats.protocoale:
            f.write("## Distribuție Protocoale\n\n")
            f.write("| Protocol | Pachete | Procent |\n")
            f.write("|----------|---------|----------|\n")
            for proto, num in sorted(stats.protocoale.items(), key=lambda x: -x[1]):
                pct = (num / stats.total_pachete * 100) if stats.total_pachete > 0 else 0
                f.write(f"| {proto} | {num:,} | {pct:.1f}% |\n")
        
        f.write("\n---\n")
        f.write("*Generat de exercițiul ex_1_04_statistici_pcap.py*\n")
    
    print(f"Raport salvat: {cale_raport}")


def main() -> int:
    """Funcția principală."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analiză statistici fișiere PCAP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python ex_1_04_statistici_pcap.py captura.pcap
  python ex_1_04_statistici_pcap.py captura.pcap --raport analiza.md
  python ex_1_04_statistici_pcap.py /work/pcap/*.pcap
        """
    )
    parser.add_argument(
        "fisiere",
        nargs="*",
        type=Path,
        default=[Path("/work/pcap")],
        help="Fișiere PCAP de analizat (sau director)"
    )
    parser.add_argument(
        "--raport",
        type=Path,
        help="Generează raport Markdown"
    )
    args = parser.parse_args()
    
    # Colectează fișierele PCAP
    fisiere_pcap = []
    for cale in args.fisiere:
        if cale.is_dir():
            fisiere_pcap.extend(cale.glob("*.pcap"))
        elif cale.suffix.lower() == ".pcap":
            fisiere_pcap.append(cale)
    
    if not fisiere_pcap:
        print("Nu s-au găsit fișiere PCAP.")
        print("\nPentru a crea o captură de test:")
        print("  tcpdump -i lo -c 100 -w /work/pcap/test.pcap &")
        print("  ping -c 10 127.0.0.1")
        return 1
    
    for fisier in fisiere_pcap:
        stats = analizeaza_manual(fisier)
        if stats is None:
            stats = analizeaza_cu_tshark(fisier)
        
        if stats:
            afiseaza_statistici(stats)
            
            if args.raport:
                genereaza_raport(stats, args.raport)
        else:
            print(f"Nu s-a putut analiza: {fisier}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
