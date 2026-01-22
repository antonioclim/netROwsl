#!/usr/bin/env python3
"""
Tema 7.01: Proiectare Profil Firewall Personalizat
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

OBIECTIV:
Creați un profil de firewall original care demonstrează înțelegerea
semanticii REJECT vs DROP și aplicați-l pentru a observa comportamentul.

CERINȚE:
1. Creați un fișier JSON cu profilul dvs. personalizat
2. Profilul trebuie să conțină minim 3 reguli
3. Trebuie să includeți cel puțin o regulă REJECT și una DROP
4. Documentați alegerea fiecărei reguli într-o analiză scrisă (500-750 cuvinte)

LIVRABILE:
1. Fișier JSON: homework/solutions/profil_personalizat_<NUME>.json
2. Analiză scrisă: homework/solutions/analiza_<NUME>.md
3. Capturi de ecran Wireshark demonstrând comportamentul (opțional)

PUNCTAJ:
- Corectitudinea sintaxei JSON: 20%
- Creativitate și relevanță a regulilor: 30%
- Calitatea analizei scrise: 40%
- Demonstrație practică: 10%
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}")


def valideaza_profil(cale_fisier: Path) -> tuple[bool, list[str]]:
    """
    Validează un fișier de profil firewall.
    
    Args:
        cale_fisier: Calea către fișierul JSON
    
    Returns:
        Tuplu (valid, lista_erori)
    """
    erori = []
    
    # Verificare existență fișier
    if not cale_fisier.exists():
        return False, [f"Fișierul nu există: {cale_fisier}"]
    
    # Încărcare și validare JSON
    try:
        with open(cale_fisier, 'r', encoding='utf-8') as f:
            profil = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Eroare de sintaxă JSON: {e}"]
    except Exception as e:
        return False, [f"Eroare la citirea fișierului: {e}"]
    
    # Verificare structură de bază
    if not isinstance(profil, dict):
        erori.append("Profilul trebuie să fie un obiect JSON (dicționar)")
        return False, erori
    
    # Verificare câmpuri obligatorii
    campuri_obligatorii = ["name", "description", "rules"]
    for camp in campuri_obligatorii:
        if camp not in profil:
            erori.append(f"Câmp obligatoriu lipsă: '{camp}'")
    
    if erori:
        return False, erori
    
    # Verificare nume
    if not profil["name"] or not isinstance(profil["name"], str):
        erori.append("Câmpul 'name' trebuie să fie un șir de caractere nevid")
    
    # Verificare descriere
    if not profil["description"] or not isinstance(profil["description"], str):
        erori.append("Câmpul 'description' trebuie să fie un șir de caractere nevid")
    
    # Verificare reguli
    reguli = profil.get("rules", [])
    
    if not isinstance(reguli, list):
        erori.append("Câmpul 'rules' trebuie să fie o listă")
        return False, erori
    
    if len(reguli) < 3:
        erori.append(f"Trebuie să aveți minim 3 reguli (aveți {len(reguli)})")
    
    # Verificare existență REJECT și DROP
    actiuni = [r.get("action", "").upper() for r in reguli if isinstance(r, dict)]
    
    if "REJECT" not in actiuni:
        erori.append("Trebuie să includeți cel puțin o regulă cu acțiunea REJECT")
    
    if "DROP" not in actiuni:
        erori.append("Trebuie să includeți cel puțin o regulă cu acțiunea DROP")
    
    # Validare fiecare regulă
    for i, regula in enumerate(reguli, 1):
        if not isinstance(regula, dict):
            erori.append(f"Regula {i} trebuie să fie un obiect")
            continue
        
        # Verificare protocol
        protocol = regula.get("protocol", "").lower()
        if protocol not in ["tcp", "udp", "icmp"]:
            erori.append(f"Regula {i}: protocol invalid '{protocol}' (permis: tcp, udp, icmp)")
        
        # Verificare port
        port = regula.get("port")
        if protocol in ["tcp", "udp"]:
            if not isinstance(port, int) or port < 1 or port > 65535:
                erori.append(f"Regula {i}: port invalid '{port}' (trebuie 1-65535)")
        
        # Verificare acțiune
        actiune = regula.get("action", "").upper()
        if actiune not in ["ACCEPT", "DROP", "REJECT"]:
            erori.append(f"Regula {i}: acțiune invalidă '{actiune}'")
        
        # Verificare comentariu (recomandat)
        if "comment" not in regula:
            logheaza(f"Atenție: Regula {i} nu are comentariu explicativ")
    
    return len(erori) == 0, erori


def afiseaza_sablon():
    """Afișează un șablon pentru profilul personalizat."""
    sablon = {
        "name": "profil_personalizat_student",
        "description": "Descriere detaliată a scopului profilului",
        "author": "Numele Studentului",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "rules": [
            {
                "protocol": "tcp",
                "port": 80,
                "action": "REJECT",
                "reject_with": "tcp-reset",
                "comment": "Blochează HTTP cu REJECT pentru feedback rapid"
            },
            {
                "protocol": "udp",
                "port": 53,
                "action": "DROP",
                "comment": "Elimină silențios traficul DNS extern"
            },
            {
                "protocol": "tcp",
                "port": 22,
                "action": "ACCEPT",
                "comment": "Permite SSH pentru administrare"
            }
        ]
    }
    
    print("\n" + "=" * 60)
    print("ȘABLON PROFIL FIREWALL PERSONALIZAT")
    print("=" * 60)
    print()
    print(json.dumps(sablon, indent=2, ensure_ascii=False))
    print()
    print("=" * 60)
    print("Salvați acest șablon și modificați-l conform cerințelor.")
    print("=" * 60)


def afiseaza_cerinte_analiza():
    """Afișează cerințele pentru analiza scrisă."""
    print("\n" + "=" * 60)
    print("CERINȚE ANALIZĂ SCRISĂ (500-750 cuvinte)")
    print("=" * 60)
    print()
    print("Analiza dvs. trebuie să conțină următoarele secțiuni:")
    print()
    print("1. INTRODUCERE (50-100 cuvinte)")
    print("   - Scopul profilului de firewall creat")
    print("   - Scenariul de utilizare vizat")
    print()
    print("2. DESCRIEREA REGULILOR (200-300 cuvinte)")
    print("   - Explicați fiecare regulă în detaliu")
    print("   - De ce ați ales acel protocol și port?")
    print("   - De ce REJECT vs DROP pentru fiecare caz?")
    print()
    print("3. COMPORTAMENT OBSERVABIL (150-200 cuvinte)")
    print("   - Ce veți vedea în Wireshark pentru fiecare regulă?")
    print("   - Cum diferă REJECT de DROP în captură?")
    print("   - Timpii de răspuns așteptați")
    print()
    print("4. COMPROMISURI DE SECURITATE (100-150 cuvinte)")
    print("   - Avantaje și dezavantaje ale alegerii REJECT")
    print("   - Când este DROP mai potrivit?")
    print("   - Impactul asupra utilizatorilor legitimi")
    print()
    print("=" * 60)


def afiseaza_rubrica():
    """Afișează rubrica detaliată de evaluare."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RUBRICA DE EVALUARE - Tema 7.01                           ║
║              Proiectare Profil Firewall Personalizat                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1. CORECTITUDINEA SINTAXEI JSON                              20 puncte     ║
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Excelent (18-20)  │ JSON valid, parsabil, toate câmpurile prezente     │
║  │  Bun (14-17)       │ JSON valid, lipsesc câmpuri opționale              │
║  │  Satisfăcător (10-13) │ Erori minore de sintaxă, structură corectă      │
║  │  Insuficient (<10) │ JSON invalid sau structură incorectă               │
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Verificare:                                                            │
║  │  □ Fișier parsabil fără erori                                          │
║  │  □ Câmpuri obligatorii: name, description, rules                       │
║  │  □ Minim 3 reguli definite                                             │
║  │  □ Include cel puțin o regulă REJECT și una DROP                       │
║                                                                              ║
║  2. CREATIVITATE ȘI RELEVANȚĂ REGULI                          30 puncte     ║
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Excelent (27-30)  │ Scenarii realiste, reguli variate și justificate   │
║  │  Bun (21-26)       │ Reguli corecte, scenarii plauzibile               │
║  │  Satisfăcător (15-20) │ Reguli funcționale, lipsă justificare          │
║  │  Insuficient (<15) │ Reguli generice sau copiate                       │
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Verificare:                                                            │
║  │  □ Reguli 3+ distincte (nu doar porturi diferite)                      │
║  │  □ Utilizare corectă REJECT pentru servicii interne                    │
║  │  □ Utilizare corectă DROP pentru securitate perimetrală                │
║  │  □ Comentarii explicative pentru fiecare regulă                        │
║                                                                              ║
║  3. CALITATEA ANALIZEI SCRISE                                 40 puncte     ║
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Excelent (36-40)  │ Analiză tehnică profundă, argumente solide        │
║  │  Bun (28-35)       │ Explicații clare, acoperă toate secțiunile        │
║  │  Satisfăcător (20-27) │ Explicații de bază, lipsesc detalii            │
║  │  Insuficient (<20) │ Superficial, sub 500 cuvinte, lipsă secțiuni      │
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Verificare:                                                            │
║  │  □ 500-750 cuvinte                                                     │
║  │  □ Secțiunea Introducere prezentă                                      │
║  │  □ Secțiunea Descriere Reguli prezentă                                 │
║  │  □ Secțiunea Comportament Observabil prezentă                          │
║  │  □ Secțiunea Compromisuri Securitate prezentă                          │
║  │  □ Explicație corectă diferență REJECT vs DROP                         │
║                                                                              ║
║  4. DEMONSTRAȚIE PRACTICĂ                                     10 puncte     ║
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Excelent (9-10)   │ Capturi Wireshark adnotate, RST/timeout vizibile  │
║  │  Bun (7-8)         │ Capturi relevante, descrieri adecvate             │
║  │  Satisfăcător (5-6) │ Capturi prezente dar neadnotate                   │
║  │  Bonus             │ +2 puncte pentru video demonstrativ               │
║  ├─────────────────────────────────────────────────────────────────────────┤
║  │  Verificare:                                                            │
║  │  □ Captură care arată RST pentru REJECT                                │
║  │  □ Captură care arată timeout/retransmisii pentru DROP                 │
║  │  □ Adnotări care indică pachetele relevante                            │
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  TOTAL                                                       100 puncte     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PENALIZĂRI:                                                                 ║
║  • Plagiat sau copiere: -100% (notă 1)                                      ║
║  • Lipsă analiză scrisă: -40 puncte                                         ║
║  • JSON invalid/neparsabil: -20 puncte                                      ║
║  • Sub 500 cuvinte în analiză: -10 puncte                                   ║
║  • Predare cu întârziere: -10% pe zi                                        ║
║                                                                              ║
║  BONUSURI:                                                                   ║
║  • Video demonstrativ (max 3 min): +5 puncte                                ║
║  • Profil complex (5+ reguli justificate): +5 puncte                        ║
║  • Comparație practică timing REJECT vs DROP: +5 puncte                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Validator și ghid pentru Tema 7.01"
    )
    parser.add_argument(
        "--valideaza", "-v",
        type=Path,
        metavar="FISIER",
        help="Validează un fișier de profil"
    )
    parser.add_argument(
        "--sablon", "-s",
        action="store_true",
        help="Afișează șablonul de profil"
    )
    parser.add_argument(
        "--cerinte", "-c",
        action="store_true",
        help="Afișează cerințele pentru analiză"
    )
    parser.add_argument(
        "--rubrica", "-r",
        action="store_true",
        help="Afișează rubrica detaliată de evaluare"
    )
    args = parser.parse_args()

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    Tema 7.01: Proiectare Profil Firewall Personalizat   ║")
    print("║    Curs REȚELE DE CALCULATOARE - ASE, Informatică       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    if args.valideaza:
        logheaza(f"Validare fișier: {args.valideaza}")
        valid, erori = valideaza_profil(args.valideaza)
        
        if valid:
            print()
            print("✓ Profilul este VALID!")
            print()
            print("Pași următori:")
            print("1. Testați profilul cu: python src/apps/firewallctl.py aplica <nume_profil>")
            print("2. Observați comportamentul în Wireshark")
            print("3. Scrieți analiza conform cerințelor")
        else:
            print()
            print("✗ Profilul are ERORI:")
            for eroare in erori:
                print(f"  - {eroare}")
            return 1
    
    elif args.sablon:
        afiseaza_sablon()
    
    elif args.cerinte:
        afiseaza_cerinte_analiza()
    
    elif args.rubrica:
        afiseaza_rubrica()
    
    else:
        parser.print_help()
        print()
        print("Exemplu de utilizare:")
        print("  python hw_7_01.py --sablon          # Afișează șablon")
        print("  python hw_7_01.py --cerinte         # Afișează cerințe analiză")
        print("  python hw_7_01.py --rubrica         # Afișează rubrica de evaluare")
        print("  python hw_7_01.py --valideaza profil.json  # Validează fișier")

    return 0


if __name__ == "__main__":
    sys.exit(main())
