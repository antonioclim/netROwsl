#!/usr/bin/env python3
"""
Script Demonstrații Laborator
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Demonstrații automate pentru prezentarea conceptelor de securitate.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.utilitare_retea import verifica_port, obtine_banner

logger = configureaza_logger("ruleaza_demo")


def pauza(secunde: float = 2.0, mesaj: str = None):
    """Face o pauză cu mesaj opțional."""
    if mesaj:
        print(f"\n⏳ {mesaj}")
    time.sleep(secunde)


def afiseaza_sectiune(titlu: str):
    """Afișează un separator de secțiune."""
    print("\n" + "=" * 60)
    print(f"  {titlu}")
    print("=" * 60)


def demo_recunoastere_completa():
    """
    Demo 1: Pipeline complet de recunoaștere.
    
    Demonstrează fluxul tipic de evaluare a securității:
    1. Scanare porturi
    2. Banner grabbing
    3. Verificare vulnerabilități
    """
    afiseaza_sectiune("DEMO 1: PIPELINE RECUNOAȘTERE SECURITATE")
    
    print("""
    Această demonstrație prezintă etapele unui audit de securitate:
    
    1. Descoperirea serviciilor (scanare porturi)
    2. Identificarea versiunilor (banner grabbing)
    3. Evaluarea vulnerabilităților
    """)
    pauza(3)
    
    # Etapa 1: Scanare porturi
    afiseaza_sectiune("ETAPA 1: SCANARE PORTURI")
    print("\nSe scanează porturile țintă...")
    
    porturi_laborator = [1883, 8883, 8080, 2121, 6200]
    
    for port in porturi_laborator:
        pauza(0.5)
        deschis = verifica_port("localhost", port)
        stare = "DESCHIS ✓" if deschis else "ÎNCHIS ✗"
        print(f"  Port {port:5}: {stare}")
    
    pauza(2)
    
    # Etapa 2: Banner grabbing
    afiseaza_sectiune("ETAPA 2: IDENTIFICARE SERVICII")
    print("\nSe obțin banner-ele serviciilor...")
    
    for port in porturi_laborator:
        if verifica_port("localhost", port):
            pauza(0.5)
            banner = obtine_banner("localhost", port)
            if banner:
                banner_scurt = banner[:60] + "..." if len(banner) > 60 else banner
                print(f"  Port {port}: {banner_scurt}")
            else:
                print(f"  Port {port}: (banner nedisponibil)")
    
    pauza(2)
    
    # Etapa 3: Verificare vulnerabilități
    afiseaza_sectiune("ETAPA 3: EVALUARE VULNERABILITĂȚI")
    print("\nSe verifică vulnerabilitățile cunoscute...")
    pauza(1)
    
    print("""
    ┌────────────────────────────────────────────────────────────┐
    │                    RAPORT VULNERABILITĂȚI                   │
    ├────────────────────────────────────────────────────────────┤
    │ [CRITIC] Port 2121 - vsftpd 2.3.4                          │
    │          CVE-2011-2523: Backdoor în codul sursă            │
    │                                                            │
    │ [CRITIC] Port 1883 - MQTT fără autentificare               │
    │          Permite publicare/abonare neautorizată            │
    │                                                            │
    │ [RIDICAT] Port 8080 - DVWA (Damn Vulnerable Web App)       │
    │          Aplicație intenționat vulnerabilă                 │
    │                                                            │
    │ [MEDIU]  Port 6200 - Port backdoor detectat                │
    │          Necesită investigare suplimentară                 │
    ├────────────────────────────────────────────────────────────┤
    │ SUMAR: 2 CRITICE | 1 RIDICAT | 1 MEDIU                     │
    └────────────────────────────────────────────────────────────┘
    """)
    
    pauza(3)
    print("\n✓ Demo 1 complet!")


def demo_comparatie_tls():
    """
    Demo 2: Comparație trafic text clar vs TLS.
    
    Demonstrează diferența dintre comunicația necriptată și cea securizată.
    """
    afiseaza_sectiune("DEMO 2: TEXT CLAR VS TLS")
    
    print("""
    Această demonstrație compară traficul MQTT:
    - Port 1883: Text clar (vizibil în captură)
    - Port 8883: TLS (criptat)
    """)
    pauza(3)
    
    # Verifică disponibilitatea serviciilor
    mqtt_plain = verifica_port("localhost", 1883)
    mqtt_tls = verifica_port("localhost", 8883)
    
    if not mqtt_plain or not mqtt_tls:
        print("\n⚠️ Serviciile MQTT nu sunt disponibile!")
        print("   Rulați mai întâi: python scripts/porneste_lab.py")
        return
    
    afiseaza_sectiune("SIMULARE: TRAFIC TEXT CLAR (PORT 1883)")
    print("""
    În Wireshark, pe portul 1883 vedeți:
    
    ┌──────────────────────────────────────────────────────────┐
    │ No.  Time     Source        Destination   Protocol Info │
    ├──────────────────────────────────────────────────────────┤
    │ 1    0.000    172.20.0.1    172.20.0.100  MQTT CONNECT  │
    │      Client ID: sensor-temp-01                           │
    │                                                          │
    │ 2    0.001    172.20.0.100  172.20.0.1    MQTT CONNACK  │
    │      Return: Connection Accepted                         │
    │                                                          │
    │ 3    0.050    172.20.0.1    172.20.0.100  MQTT PUBLISH  │
    │      Topic: sensors/temperature/room1                    │
    │      Message: {"temp": 23.5, "unit": "C"}  ← VIZIBIL!   │
    └──────────────────────────────────────────────────────────┘
    """)
    pauza(4)
    
    afiseaza_sectiune("SIMULARE: TRAFIC TLS (PORT 8883)")
    print("""
    În Wireshark, pe portul 8883 vedeți:
    
    ┌──────────────────────────────────────────────────────────┐
    │ No.  Time     Source        Destination   Protocol Info │
    ├──────────────────────────────────────────────────────────┤
    │ 1    0.000    172.20.0.1    172.20.0.100  TLSv1.3       │
    │      Client Hello                                        │
    │                                                          │
    │ 2    0.001    172.20.0.100  172.20.0.1    TLSv1.3       │
    │      Server Hello, Certificate, Finished                 │
    │                                                          │
    │ 3    0.050    172.20.0.1    172.20.0.100  TLSv1.3       │
    │      Application Data [encrypted]  ← CRIPTAT!           │
    │      0x17 03 03 00 45 8a b2 c7 f3 2e...                 │
    └──────────────────────────────────────────────────────────┘
    
    ⚠️ ATENȚIE: Chiar și cu TLS, metadatele sunt vizibile:
       - Adrese IP sursă/destinație
       - Dimensiuni pachete
       - Timing-ul comunicației
    """)
    pauza(3)
    print("\n✓ Demo 2 complet!")


def demo_detectie_backdoor():
    """
    Demo 3: Recunoaștere și detecție backdoor.
    
    Demonstrează tehnicile de fingerprinting și detecție.
    """
    afiseaza_sectiune("DEMO 3: DETECTIE BACKDOOR")
    
    print("""
    Această demonstrație prezintă:
    - Fingerprinting-ul serviciilor
    - Detecția porturilor suspecte
    - Identificarea versiunilor vulnerabile
    """)
    pauza(3)
    
    afiseaza_sectiune("FINGERPRINTING SERVICIU FTP")
    
    banner_ftp = obtine_banner("localhost", 2121)
    
    print(f"\n  Port 2121 - Banner obținut:")
    print(f"  \"{banner_ftp or 'N/A'}\"")
    
    if banner_ftp and "2.3.4" in banner_ftp:
        print("""
    ┌────────────────────────────────────────────────────────────┐
    │ ⚠️  ALERTĂ: VERSIUNE VULNERABILĂ DETECTATĂ!               │
    ├────────────────────────────────────────────────────────────┤
    │                                                            │
    │  Serviciu: vsftpd 2.3.4                                    │
    │  CVE: CVE-2011-2523                                        │
    │  Severitate: CRITICĂ (CVSS 10.0)                           │
    │                                                            │
    │  Descriere:                                                │
    │  Versiunea 2.3.4 a vsftpd conține un backdoor             │
    │  introdus malițios în codul sursă. Când un client         │
    │  se autentifică cu un username care conține ":)"          │
    │  (smiley face), se deschide un shell pe portul 6200.      │
    │                                                            │
    │  Remediere:                                                │
    │  - Actualizați la versiunea 2.3.5 sau mai nouă            │
    │  - Verificați integritatea surselor software              │
    │  - Monitorizați portul 6200 pentru conexiuni suspecte     │
    │                                                            │
    └────────────────────────────────────────────────────────────┘
        """)
    
    pauza(3)
    
    afiseaza_sectiune("VERIFICARE PORT BACKDOOR")
    
    backdoor_deschis = verifica_port("localhost", 6200)
    
    print(f"\n  Port 6200: {'DESCHIS ⚠️' if backdoor_deschis else 'ÎNCHIS ✓'}")
    
    if backdoor_deschis:
        print("""
    ┌────────────────────────────────────────────────────────────┐
    │ 🔴 PORT BACKDOOR ACTIV!                                    │
    ├────────────────────────────────────────────────────────────┤
    │                                                            │
    │  În mediu real, acest port ar permite:                     │
    │  - Acces neautorizat la sistem                             │
    │  - Execuție de comenzi arbitrare                           │
    │  - Exfiltrare de date                                      │
    │                                                            │
    │  NOTĂ: În acest laborator, backdoor-ul este SIMULAT       │
    │  și nu execută efectiv comenzi.                            │
    │                                                            │
    └────────────────────────────────────────────────────────────┘
        """)
    
    pauza(3)
    print("\n✓ Demo 3 complet!")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Demonstrații Laborator Săptămâna 13",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Demonstrații disponibile:
  1 - Pipeline complet de recunoaștere (scanare, fingerprinting, evaluare)
  2 - Comparație trafic text clar vs TLS
  3 - Detecție backdoor și fingerprinting servicii

Exemple:
  python ruleaza_demo.py --demo 1
  python ruleaza_demo.py --demo 2
  python ruleaza_demo.py --toate
        """
    )
    
    parser.add_argument("--demo", type=int, choices=[1, 2, 3],
                        help="Numărul demonstrației de rulat")
    parser.add_argument("--toate", action="store_true",
                        help="Rulează toate demonstrațiile")
    parser.add_argument("--lista", action="store_true",
                        help="Listează demonstrațiile disponibile")
    
    args = parser.parse_args()
    
    if args.lista or (not args.demo and not args.toate):
        print("""
╔════════════════════════════════════════════════════════════════╗
║         DEMONSTRAȚII LABORATOR SĂPTĂMÂNA 13                    ║
║         IoT și Securitate în Rețelele de Calculatoare          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Demo 1: Pipeline Recunoaștere                                 ║
║          Scanare porturi → Identificare servicii →             ║
║          Evaluare vulnerabilități                              ║
║                                                                ║
║  Demo 2: Text Clar vs TLS                                      ║
║          Comparație vizuală a traficului MQTT                  ║
║          necriptat și criptat                                  ║
║                                                                ║
║  Demo 3: Detecție Backdoor                                     ║
║          Fingerprinting vsftpd și detectarea                   ║
║          CVE-2011-2523                                         ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║  Utilizare: python ruleaza_demo.py --demo <1|2|3>              ║
║             python ruleaza_demo.py --toate                     ║
╚════════════════════════════════════════════════════════════════╝
        """)
        return 0
    
    demos = {
        1: demo_recunoastere_completa,
        2: demo_comparatie_tls,
        3: demo_detectie_backdoor
    }
    
    try:
        if args.toate:
            for numar, functie in demos.items():
                functie()
                if numar < 3:
                    print("\n" + "─" * 60)
                    input("Apăsați Enter pentru următoarea demonstrație...")
        elif args.demo:
            demos[args.demo]()
        
        print("\n" + "=" * 60)
        print("DEMONSTRAȚIE FINALIZATĂ")
        print("=" * 60)
        return 0
        
    except KeyboardInterrupt:
        print("\n\nÎntrerupt de utilizator.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
