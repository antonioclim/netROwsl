#!/usr/bin/env python3
"""
Exercițiul 5: Calculul Întârzierii de Transmisie
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script demonstrează conceptele de întârziere în rețele:
- Întârziere de transmisie (transmission delay)
- Întârziere de propagare (propagation delay)
- Întârziere de procesare (processing delay)
- Întârziere de așteptare (queuing delay)
"""

from __future__ import annotations

import time
import socket
import threading
from dataclasses import dataclass
from typing import List, Optional, Tuple
import argparse


@dataclass
class RezultatMasurare:
    """Rezultatul unei măsurători de întârziere."""
    dimensiune_date: int  # în octeți
    timp_total: float     # în secunde
    rata_transfer: float  # în octeți/secundă
    
    @property
    def timp_ms(self) -> float:
        """Returnează timpul în milisecunde."""
        return self.timp_total * 1000
    
    @property
    def rata_mbps(self) -> float:
        """Returnează rata în Mbps."""
        return (self.rata_transfer * 8) / 1_000_000


@dataclass
class ParametriRetea:
    """Parametrii simulați ai unei rețele."""
    latime_banda_bps: float    # lățime de bandă în biți/secundă
    distanta_km: float         # distanța în kilometri
    viteza_propagare: float    # fracțiune din viteza luminii (0.67 pentru fibră)
    
    VITEZA_LUMINA = 3e8  # m/s
    
    @property
    def intarziere_propagare_ms(self) -> float:
        """Calculează întârzierea de propagare în milisecunde."""
        distanta_m = self.distanta_km * 1000
        viteza_mediu = self.VITEZA_LUMINA * self.viteza_propagare
        return (distanta_m / viteza_mediu) * 1000
    
    def intarziere_transmisie_ms(self, dimensiune_octeti: int) -> float:
        """Calculează întârzierea de transmisie pentru o cantitate de date.
        
        Args:
            dimensiune_octeti: Dimensiunea datelor în octeți
            
        Returns:
            Întârzierea de transmisie în milisecunde
        """
        dimensiune_biti = dimensiune_octeti * 8
        return (dimensiune_biti / self.latime_banda_bps) * 1000


def calculeaza_intarziere_teoretica(
    dimensiune: int,
    latime_banda_mbps: float,
    distanta_km: float,
    viteza_propagare: float = 0.67
) -> dict:
    """Calculează întârzierea teoretică a transmisiei.
    
    Args:
        dimensiune: Dimensiunea datelor în octeți
        latime_banda_mbps: Lățimea de bandă în Mbps
        distanta_km: Distanța în kilometri
        viteza_propagare: Fracțiunea din viteza luminii
        
    Returns:
        Dicționar cu componentele întârzierii
    """
    params = ParametriRetea(
        latime_banda_bps=latime_banda_mbps * 1_000_000,
        distanta_km=distanta_km,
        viteza_propagare=viteza_propagare
    )
    
    intarziere_transmisie = params.intarziere_transmisie_ms(dimensiune)
    intarziere_propagare = params.intarziere_propagare_ms
    
    return {
        "dimensiune_octeti": dimensiune,
        "latime_banda_mbps": latime_banda_mbps,
        "distanta_km": distanta_km,
        "intarziere_transmisie_ms": intarziere_transmisie,
        "intarziere_propagare_ms": intarziere_propagare,
        "intarziere_totala_ms": intarziere_transmisie + intarziere_propagare,
    }


def masoara_transfer_tcp(
    gazda: str,
    port: int,
    dimensiune: int,
    repetitii: int = 5
) -> List[RezultatMasurare]:
    """Măsoară transferul real de date prin TCP.
    
    Args:
        gazda: Adresa gazdei
        port: Portul de conectare
        dimensiune: Dimensiunea datelor de transmis
        repetitii: Numărul de măsurători
        
    Returns:
        Lista de rezultate ale măsurătorilor
    """
    rezultate = []
    date = b"X" * dimensiune
    
    for i in range(repetitii):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(30)
                s.connect((gazda, port))
                
                # Măsoară timpul de trimitere
                start = time.perf_counter()
                s.sendall(date)
                # Așteaptă confirmarea (echo)
                primit = b""
                while len(primit) < dimensiune:
                    chunk = s.recv(min(dimensiune - len(primit), 65536))
                    if not chunk:
                        break
                    primit += chunk
                sfarsit = time.perf_counter()
                
                timp = sfarsit - start
                rata = (dimensiune * 2) / timp  # dus-întors
                
                rezultate.append(RezultatMasurare(
                    dimensiune_date=dimensiune,
                    timp_total=timp,
                    rata_transfer=rata
                ))
                
        except Exception as e:
            print(f"  Eroare la măsurarea {i+1}: {e}")
    
    return rezultate


def server_echo(port: int, oprire: threading.Event) -> None:
    """Server echo pentru măsurători.
    
    Args:
        port: Portul pe care să asculte
        oprire: Eveniment pentru oprirea serverului
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(1.0)
        s.bind(("0.0.0.0", port))
        s.listen(5)
        
        while not oprire.is_set():
            try:
                conn, addr = s.accept()
                with conn:
                    conn.settimeout(30)
                    while True:
                        date = conn.recv(65536)
                        if not date:
                            break
                        conn.sendall(date)
            except socket.timeout:
                continue
            except Exception:
                break


def demonstreaza_calcul_teoretic() -> None:
    """Demonstrează calculele teoretice de întârziere."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + "  CALCUL TEORETIC AL ÎNTÂRZIERII".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Scenarii de demonstrație
    scenarii = [
        {"nume": "LAN local (Ethernet 1Gbps, 100m)", 
         "dimensiune": 1500, "banda": 1000, "distanta": 0.1},
        {"nume": "Rețea metropolitană (100Mbps, 50km)",
         "dimensiune": 1500, "banda": 100, "distanta": 50},
        {"nume": "WAN intercontinental (1Gbps, 5000km)",
         "dimensiune": 1500, "banda": 1000, "distanta": 5000},
        {"nume": "Transfer fișier mare LAN (1GB, 1Gbps)",
         "dimensiune": 1_000_000_000, "banda": 1000, "distanta": 0.1},
    ]
    
    print("Formula întârzierii totale:")
    print("  d_total = d_transmisie + d_propagare + d_procesare + d_așteptare")
    print()
    print("Unde:")
    print("  d_transmisie = L / R  (L = dimensiune date, R = lățime bandă)")
    print("  d_propagare = D / S   (D = distanță, S = viteză propagare)")
    print()
    
    for scenariu in scenarii:
        rezultat = calculeaza_intarziere_teoretica(
            dimensiune=scenariu["dimensiune"],
            latime_banda_mbps=scenariu["banda"],
            distanta_km=scenariu["distanta"]
        )
        
        print(f"{'─' * 70}")
        print(f"Scenariu: {scenariu['nume']}")
        print(f"  Dimensiune:              {rezultat['dimensiune_octeti']:,} octeți")
        print(f"  Lățime de bandă:         {rezultat['latime_banda_mbps']:,} Mbps")
        print(f"  Distanță:                {rezultat['distanta_km']:,} km")
        print()
        print(f"  Întârziere transmisie:   {rezultat['intarziere_transmisie_ms']:.6f} ms")
        print(f"  Întârziere propagare:    {rezultat['intarziere_propagare_ms']:.6f} ms")
        print(f"  ÎNTÂRZIERE TOTALĂ:       {rezultat['intarziere_totala_ms']:.6f} ms")
        print()


def demonstreaza_masuratori_reale(port: int = 9999) -> None:
    """Demonstrează măsurători reale de întârziere."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + "  MĂSURĂTORI REALE DE ÎNTÂRZIERE".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Pornește serverul echo în fundal
    oprire = threading.Event()
    thread_server = threading.Thread(target=server_echo, args=(port, oprire))
    thread_server.daemon = True
    thread_server.start()
    
    time.sleep(0.5)  # Așteaptă pornirea serverului
    
    dimensiuni = [100, 1000, 10000, 100000, 1000000]
    
    print(f"Se măsoară transferul pe localhost:{port}")
    print()
    print(f"{'Dimensiune':>12} │ {'Timp (ms)':>12} │ {'Rată (MB/s)':>12} │ {'Rată (Mbps)':>12}")
    print("─" * 58)
    
    for dim in dimensiuni:
        rezultate = masoara_transfer_tcp("127.0.0.1", port, dim, repetitii=3)
        
        if rezultate:
            timp_mediu = sum(r.timp_ms for r in rezultate) / len(rezultate)
            rata_medie = sum(r.rata_transfer for r in rezultate) / len(rezultate)
            rata_mbps = (rata_medie * 8) / 1_000_000
            rata_mbs = rata_medie / 1_000_000
            
            print(f"{dim:>12,} │ {timp_mediu:>12.3f} │ {rata_mbs:>12.2f} │ {rata_mbps:>12.2f}")
    
    oprire.set()
    thread_server.join(timeout=2)
    
    print()
    print("Notă: Măsurătorile pe localhost au întârziere minimă de propagare.")
    print("      Valorile reale în rețele WAN vor fi semnificativ mai mari.")


def afiseaza_comparatie() -> None:
    """Afișează o comparație între diferite scenarii."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + "  COMPARAȚIE SCENARII".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    print("Impactul lățimii de bandă vs. distanță pentru 1MB de date:")
    print()
    print(f"{'Scenariu':<35} │ {'Transmisie':>10} │ {'Propagare':>10} │ {'Total':>10}")
    print("─" * 72)
    
    scenarii = [
        ("10 Mbps, 1 km (ADSL local)", 10, 1),
        ("100 Mbps, 100 km (fibră regională)", 100, 100),
        ("1 Gbps, 1 km (LAN enterprise)", 1000, 1),
        ("1 Gbps, 1000 km (fibră națională)", 1000, 1000),
        ("10 Gbps, 10000 km (backbone)", 10000, 10000),
    ]
    
    dimensiune = 1_000_000  # 1 MB
    
    for nume, banda, distanta in scenarii:
        rez = calculeaza_intarziere_teoretica(dimensiune, banda, distanta)
        print(f"{nume:<35} │ {rez['intarziere_transmisie_ms']:>9.2f}ms │ "
              f"{rez['intarziere_propagare_ms']:>9.2f}ms │ {rez['intarziere_totala_ms']:>9.2f}ms")
    
    print()
    print("Concluzie:")
    print("  • Pentru date mici și distanțe mari: întârzierea de propagare domină")
    print("  • Pentru date mari și distanțe mici: întârzierea de transmisie domină")
    print("  • Optimizarea depinde de scenariul specific!")


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Demonstrație calcul întârziere transmisie",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python ex_1_05_intarziere_transmisie.py              # Toate demonstrațiile
  python ex_1_05_intarziere_transmisie.py --teoretic   # Doar calcule teoretice
  python ex_1_05_intarziere_transmisie.py --masurat    # Doar măsurători reale
  python ex_1_05_intarziere_transmisie.py --comparatie # Doar comparație
        """
    )
    parser.add_argument(
        "--teoretic",
        action="store_true",
        help="Afișează doar calculele teoretice"
    )
    parser.add_argument(
        "--masurat",
        action="store_true",
        help="Rulează doar măsurătorile reale"
    )
    parser.add_argument(
        "--comparatie",
        action="store_true",
        help="Afișează doar comparația scenariilor"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9999,
        help="Portul pentru serverul de test (implicit: 9999)"
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + "  EXERCIȚIUL 5: ÎNTÂRZIEREA DE TRANSMISIE".center(68) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE, Informatică".center(68) + "║")
    print("╚" + "═" * 68 + "╝")

    toate = not (args.teoretic or args.masurat or args.comparatie)

    try:
        if toate or args.teoretic:
            demonstreaza_calcul_teoretic()
        
        if toate or args.comparatie:
            afiseaza_comparatie()
        
        if toate or args.masurat:
            demonstreaza_masuratori_reale(args.port)

        print()
        print("─" * 70)
        print("Exercițiu finalizat cu succes!")
        print("─" * 70)
        return 0

    except KeyboardInterrupt:
        print("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        print(f"\nEroare: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
