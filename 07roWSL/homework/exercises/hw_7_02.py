#!/usr/bin/env python3
"""
Tema 7.02: Raport de Analiză a Eșecurilor de Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

OBIECTIV:
Analizați trei scenarii de eșec de rețea, capturați traficul și produceți
un raport profesional de incident care identifică cauza fundamentală.

SCENARII:
1. Conexiune TCP respinsă (REJECT)
2. Pachet UDP eliminat silențios (DROP)
3. Cerere blocată la nivel aplicație

CERINȚE:
1. Rulați fiecare scenariu de simulare
2. Capturați traficul în fișiere PCAP separate
3. Analizați capturile în Wireshark
4. Scrieți un raport de incident (1000-1500 cuvinte)

LIVRABILE:
1. Capturi: homework/solutions/captura_scenariu_1.pcap (și 2, 3)
2. Raport: homework/solutions/raport_incident_<NUME>.md
3. Capturi de ecran Wireshark (minim 3)

PUNCTAJ:
- Capturi complete și corecte: 25%
- Identificarea corectă a cauzelor: 35%
- Calitatea raportului: 30%
- Capturi de ecran explicative: 10%
"""

from __future__ import annotations

import argparse
import socket
import sys
import time
from datetime import datetime
from pathlib import Path


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}")


def simuleaza_scenariu_1():
    """
    Scenariu 1: Conexiune TCP respinsă (REJECT)
    
    Simulează o conexiune către un port blocat cu REJECT.
    În captură veți vedea: SYN -> RST sau ICMP Port Unreachable
    """
    print()
    print("=" * 60)
    print("SCENARIU 1: Conexiune TCP Respinsă (REJECT)")
    print("=" * 60)
    print()
    print("Descriere:")
    print("  Încercăm să ne conectăm la un serviciu TCP care este blocat")
    print("  cu o regulă REJECT. Firewall-ul va răspunde imediat cu RST.")
    print()
    print("Ce să observați în Wireshark:")
    print("  1. Pachetul SYN trimis de client")
    print("  2. Răspunsul RST imediat (sau ICMP Port Unreachable)")
    print("  3. Timp de răspuns: foarte scurt (milisecunde)")
    print("  4. Nicio retransmisie SYN")
    print()
    
    input("Apăsați Enter pentru a începe simularea...")
    print()
    
    host = "localhost"
    port = 9090
    
    logheaza(f"Încercare conexiune la {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        timp_start = time.time()
        rezultat = sock.connect_ex((host, port))
        timp_scurs = time.time() - timp_start
        
        sock.close()
        
        if rezultat == 0:
            logheaza(f"Conexiune reușită în {timp_scurs:.3f}s")
            logheaza("Notă: Pentru a vedea REJECT, aplicați profilul blocare_tcp_9090")
        else:
            logheaza(f"Conexiune eșuată în {timp_scurs:.3f}s (cod eroare: {rezultat})")
            if timp_scurs < 1:
                logheaza("Aceasta arată comportament REJECT - eșec rapid!")
            else:
                logheaza("Timp lung - posibil DROP sau timeout")
                
    except ConnectionRefusedError:
        timp_scurs = time.time() - timp_start
        logheaza(f"Connection Refused în {timp_scurs:.3f}s - comportament REJECT tipic")
    except socket.timeout:
        logheaza("Timeout - aceasta seamănă cu DROP, nu cu REJECT")
    except Exception as e:
        logheaza(f"Eroare: {e}")


def simuleaza_scenariu_2():
    """
    Scenariu 2: Pachet UDP eliminat silențios (DROP)
    
    Simulează trimiterea unui pachet UDP către un port blocat cu DROP.
    În captură veți vedea: UDP -> (nimic)
    """
    print()
    print("=" * 60)
    print("SCENARIU 2: Pachet UDP Eliminat Silențios (DROP)")
    print("=" * 60)
    print()
    print("Descriere:")
    print("  Trimitem un pachet UDP către un port blocat cu DROP.")
    print("  Firewall-ul va elimina silențios pachetul, fără răspuns.")
    print()
    print("Ce să observați în Wireshark:")
    print("  1. Datagrama UDP trimisă")
    print("  2. NICIUN răspuns - nici ICMP, nici nimic")
    print("  3. Acest comportament este identic cu pierderea pachetelor")
    print("  4. Imposibil de distins de o problemă de rețea")
    print()
    
    input("Apăsați Enter pentru a începe simularea...")
    print()
    
    host = "localhost"
    port = 9091
    mesaj = "Test UDP pentru scenariu DROP"
    
    logheaza(f"Trimitere datagramă UDP către {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        
        sock.sendto(mesaj.encode(), (host, port))
        logheaza("Datagramă trimisă!")
        
        logheaza("Așteptare răspuns (3 secunde)...")
        try:
            raspuns, adresa = sock.recvfrom(4096)
            logheaza(f"Răspuns primit: {raspuns.decode()}")
        except socket.timeout:
            logheaza("Timeout - niciun răspuns primit")
            logheaza("Aceasta este comportamentul DROP tipic!")
        
        sock.close()
        
    except Exception as e:
        logheaza(f"Eroare: {e}")


def simuleaza_scenariu_3():
    """
    Scenariu 3: Cerere blocată la nivel aplicație
    
    Simulează o cerere HTTP/TCP care conține cuvinte cheie blocate.
    În captură veți vedea: conexiune TCP reușită, dar răspuns 403.
    """
    print()
    print("=" * 60)
    print("SCENARIU 3: Blocare la Nivel Aplicație")
    print("=" * 60)
    print()
    print("Descriere:")
    print("  Trimitem o cerere către filtrul de pachete la nivel aplicație.")
    print("  Conexiunea TCP reușește, dar cererea este respinsă pe baza")
    print("  conținutului (cuvânt cheie blocat).")
    print()
    print("Ce să observați în Wireshark:")
    print("  1. Handshake TCP complet (SYN, SYN-ACK, ACK)")
    print("  2. Date transmise (cererea)")
    print("  3. Răspuns de la server (403 Forbidden)")
    print("  4. Încheiere conexiune normală (FIN)")
    print()
    print("Diferența față de filtrarea la nivel rețea:")
    print("  - Conexiunea TCP se stabilește cu succes")
    print("  - Blocarea are loc după inspecția conținutului")
    print()
    
    input("Apăsați Enter pentru a începe simularea...")
    print()
    
    host = "localhost"
    port = 8888
    
    # Test cu conținut permis
    logheaza("Test 1: Cerere cu conținut permis...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        cerere = "GET / HTTP/1.0\r\nHost: test\r\n\r\nContinut normal"
        sock.sendall(cerere.encode())
        
        raspuns = sock.recv(4096).decode()
        sock.close()
        
        if "200" in raspuns:
            logheaza("Cerere ACCEPTATĂ (200 OK)")
        else:
            logheaza(f"Răspuns: {raspuns[:100]}...")
            
    except ConnectionRefusedError:
        logheaza("Conexiune refuzată - porniți filtrul cu: --profile proxy")
    except Exception as e:
        logheaza(f"Eroare: {e}")
    
    print()
    
    # Test cu conținut blocat
    logheaza("Test 2: Cerere cu conținut blocat (cuvânt cheie: 'malware')...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        cerere = "GET / HTTP/1.0\r\nHost: test\r\n\r\nDownload malware here"
        sock.sendall(cerere.encode())
        
        raspuns = sock.recv(4096).decode()
        sock.close()
        
        if "403" in raspuns or "Forbidden" in raspuns or "blocat" in raspuns.lower():
            logheaza("Cerere BLOCATĂ (403 Forbidden)")
            logheaza("Aceasta demonstrează filtrarea la nivel aplicație!")
        else:
            logheaza(f"Răspuns: {raspuns[:100]}...")
            
    except ConnectionRefusedError:
        logheaza("Conexiune refuzată - porniți filtrul cu: --profile proxy")
    except Exception as e:
        logheaza(f"Eroare: {e}")


def afiseaza_sablon_raport():
    """Afișează șablonul pentru raportul de incident."""
    print()
    print("=" * 60)
    print("ȘABLON RAPORT DE INCIDENT")
    print("=" * 60)
    print("""
# Raport de Analiză a Eșecurilor de Rețea

**Autor:** [Numele Studentului]
**Data:** [Data]
**Versiune:** 1.0

## 1. Sumar Executiv (100-150 cuvinte)

[Rezumați pe scurt cele trei incidente analizate și concluziile principale]

## 2. Metodologie

### 2.1 Instrumente Utilizate
- Wireshark [versiune]
- Python [versiune]
- Docker [versiune]

### 2.2 Configurația Mediului
[Descrieți mediul de test]

## 3. Analiza Incidentelor

### 3.1 Incident 1: Conexiune TCP Respinsă (REJECT)

**Simptome observate:**
[Descrieți ce ați observat]

**Evidență din captură:**
[Inserați captură de ecran și explicații]

**Cauza fundamentală:**
[Identificați cauza]

**Recomandări:**
[Propuneți soluții]

### 3.2 Incident 2: Pachet UDP Eliminat (DROP)

**Simptome observate:**
[Descrieți ce ați observat]

**Evidență din captură:**
[Inserați captură de ecran și explicații]

**Cauza fundamentală:**
[Identificați cauza]

**Recomandări:**
[Propuneți soluții]

### 3.3 Incident 3: Blocare Nivel Aplicație

**Simptome observate:**
[Descrieți ce ați observat]

**Evidență din captură:**
[Inserați captură de ecran și explicații]

**Cauza fundamentală:**
[Identificați cauza]

**Recomandări:**
[Propuneți soluții]

## 4. Comparație și Concluzii

### 4.1 Tabel Comparativ

| Aspect | REJECT | DROP | Aplicație |
|--------|--------|------|-----------|
| Timp răspuns | | | |
| Vizibil în captură | | | |
| Informații pentru atacator | | | |

### 4.2 Concluzii

[Sintetizați învățămintele principale]

## 5. Anexe

### 5.1 Fișiere PCAP
- captura_scenariu_1.pcap
- captura_scenariu_2.pcap
- captura_scenariu_3.pcap

### 5.2 Capturi de Ecran
[Listați capturile incluse]
""")
    print("=" * 60)


def afiseaza_rubrica():
    """Afișează rubrica detaliată de evaluare."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RUBRICA DE EVALUARE - Tema 7.02                           ║
║              Raport de Analiză a Eșecurilor de Rețea                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1. CAPTURI PCAP COMPLETE ȘI CORECTE                          25 puncte     ║
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Excelent (23-25)  │ 3 fișiere PCAP, filtre corecte, pachete relevante  │
║  │  Bun (18-22)       │ 3 fișiere, unele pachete irelevante incluse        │
║  │  Satisfăcător (13-17) │ 2 fișiere complete sau 3 incomplete             │
║  │  Insuficient (<13) │ Fișiere lipsă sau corupte                          │
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Verificare pentru fiecare captură:                                     │
║  │  □ captura_scenariu_1.pcap - conține SYN și RST/ICMP                   │
║  │  □ captura_scenariu_2.pcap - conține UDP fără răspuns                  │
║  │  □ captura_scenariu_3.pcap - conține handshake + HTTP 403               │
║  │  □ Fișiere deschidibile în Wireshark fără erori                        │
║                                                                              ║
║  2. IDENTIFICAREA CAUZELOR FUNDAMENTALE                       35 puncte     ║
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Excelent (32-35)  │ Cauze corecte, explicații tehnice detaliate        │
║  │  Bun (25-31)       │ Cauze corecte, explicații de bază                  │
║  │  Satisfăcător (18-24) │ Cauze parțial corecte, confuzii minore          │
║  │  Insuficient (<18) │ Cauze incorecte sau lipsă                          │
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Verificare:                                                            │
║  │  □ Scenariu 1: Identificat RST ca semn de REJECT                       │
║  │  □ Scenariu 1: Menționat timp de răspuns rapid                         │
║  │  □ Scenariu 2: Identificat absența răspunsului ca semn de DROP         │
║  │  □ Scenariu 2: Explicat de ce e greu de depanat                        │
║  │  □ Scenariu 3: Diferențiat de filtrarea nivel rețea                    │
║  │  □ Scenariu 3: Explicat că handshake-ul TCP reușește                   │
║                                                                              ║
║  3. CALITATEA RAPORTULUI                                      30 puncte     ║
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Excelent (27-30)  │ Profesional, 1000-1500 cuvinte, toate secțiunile  │
║  │  Bun (21-26)       │ Clar structurat, acoperă cerințele                │
║  │  Satisfăcător (15-20) │ Structură de bază, lipsesc detalii             │
║  │  Insuficient (<15) │ Sub 800 cuvinte, secțiuni lipsă                   │
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Verificare:                                                            │
║  │  □ Lungime 1000-1500 cuvinte                                           │
║  │  □ Sumar executiv prezent                                              │
║  │  □ Metodologie descrisă                                                │
║  │  □ Toate cele 3 incidente analizate individual                         │
║  │  □ Tabel comparativ REJECT vs DROP vs Aplicație                        │
║  │  □ Concluzii și recomandări                                            │
║  │  □ Limbaj profesional, fără greșeli majore                             │
║                                                                              ║
║  4. CAPTURI DE ECRAN EXPLICATIVE                              10 puncte     ║
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Excelent (9-10)   │ 3+ capturi adnotate, pachete evidențiate          │
║  │  Bun (7-8)         │ 3 capturi relevante, descrieri adecvate           │
║  │  Satisfăcător (5-6) │ Capturi prezente dar neadnotate                   │
║  │  Insuficient (<5)  │ Capturi lipsă sau irelevante                      │
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Verificare:                                                            │
║  │  □ Captură care arată RST pentru Scenariu 1                            │
║  │  □ Captură care arată UDP singur pentru Scenariu 2                     │
║  │  □ Captură care arată handshake + 403 pentru Scenariu 3                │
║  │  □ Pachete relevante evidențiate/încercuite                            │
║  │  □ Adnotări text care explică ce se vede                               │
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  TOTAL                                                       100 puncte     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PENALIZĂRI:                                                                 ║
║  • Plagiat sau copiere: -100% (notă 1)                                      ║
║  • Lipsă fișiere PCAP: -25 puncte                                           ║
║  • Lipsă raport scris: -30 puncte                                           ║
║  • Sub 800 cuvinte: -10 puncte                                              ║
║  • Fără capturi de ecran: -10 puncte                                        ║
║  • Predare cu întârziere: -10% pe zi                                        ║
║                                                                              ║
║  BONUSURI:                                                                   ║
║  • Analiză suplimentară a timing-ului (grafic): +5 puncte                   ║
║  • Comparație cu tcpdump în terminal: +3 puncte                             ║
║  • Recomandări de îmbunătățire a securității: +5 puncte                     ║
║  • Format raport LaTeX/PDF profesional: +2 puncte                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Simulator și ghid pentru Tema 7.02"
    )
    parser.add_argument(
        "--scenariu", "-s",
        type=int,
        choices=[1, 2, 3],
        help="Rulează un scenariu specific (1, 2, sau 3)"
    )
    parser.add_argument(
        "--toate", "-a",
        action="store_true",
        help="Rulează toate scenariile"
    )
    parser.add_argument(
        "--sablon", "-t",
        action="store_true",
        help="Afișează șablonul de raport"
    )
    parser.add_argument(
        "--rubrica", "-r",
        action="store_true",
        help="Afișează rubrica detaliată de evaluare"
    )
    args = parser.parse_args()

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Tema 7.02: Raport de Analiză a Eșecurilor de Rețea    ║")
    print("║   Curs REȚELE DE CALCULATOARE - ASE, Informatică        ║")
    print("╚══════════════════════════════════════════════════════════╝")

    if args.sablon:
        afiseaza_sablon_raport()
    elif args.rubrica:
        afiseaza_rubrica()
    elif args.scenariu == 1:
        simuleaza_scenariu_1()
    elif args.scenariu == 2:
        simuleaza_scenariu_2()
    elif args.scenariu == 3:
        simuleaza_scenariu_3()
    elif args.toate:
        simuleaza_scenariu_1()
        print("\n" + "-" * 60 + "\n")
        simuleaza_scenariu_2()
        print("\n" + "-" * 60 + "\n")
        simuleaza_scenariu_3()
    else:
        parser.print_help()
        print()
        print("Exemplu de utilizare:")
        print("  python hw_7_02.py --scenariu 1   # Rulează scenariul 1")
        print("  python hw_7_02.py --toate        # Rulează toate scenariile")
        print("  python hw_7_02.py --sablon       # Afișează șablonul de raport")
        print("  python hw_7_02.py --rubrica      # Afișează rubrica de evaluare")
        print()
        print("Pași recomandați:")
        print("  1. Porniți Wireshark și începeți captura")
        print("  2. Rulați fiecare scenariu separat")
        print("  3. Salvați capturile în fișiere PCAP separate")
        print("  4. Analizați și scrieți raportul")

    return 0


if __name__ == "__main__":
    sys.exit(main())
