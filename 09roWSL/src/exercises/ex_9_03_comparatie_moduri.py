#!/usr/bin/env python3
"""
Exercițiul 9.03: Comparație Mod Activ vs Pasiv FTP

═══════════════════════════════════════════════════════════════════════════════
NIVEL BLOOM: EVALUATE (Evaluare)
═══════════════════════════════════════════════════════════════════════════════

Acest exercițiu vă cere să EVALUAȚI și JUSTIFICAȚI alegerea modului FTP
bazat pe diferite scenarii de rețea.

OBIECTIVE:
1. Evaluați avantajele și dezavantajele fiecărui mod FTP
2. Justificați alegerea modului optim pentru scenarii specifice
3. Analizați impactul firewall-urilor și NAT asupra FTP

═══════════════════════════════════════════════════════════════════════════════
CONTEXT TEORETIC:
═══════════════════════════════════════════════════════════════════════════════

MOD ACTIV (PORT):
- Client trimite comanda PORT cu IP:port local
- SERVER inițiază conexiunea de date CĂTRE client
- Server: port 20 → Client: port specificat
- Problematic cu firewall-uri pe client

MOD PASIV (PASV):
- Client trimite comanda PASV
- Server răspunde cu IP:port pentru date
- CLIENT inițiază conexiunea de date CĂTRE server
- Funcționează prin NAT și firewall-uri pe client

═══════════════════════════════════════════════════════════════════════════════
UTILIZARE:
═══════════════════════════════════════════════════════════════════════════════

    python3 ex_9_03_comparatie_moduri.py --demo      # Demonstrație scenarii
    python3 ex_9_03_comparatie_moduri.py --test      # Verifică implementarea
    python3 ex_9_03_comparatie_moduri.py --interactiv # Quiz interactiv
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ModFTP(Enum):
    """Modurile de transfer FTP."""
    ACTIV = "ACTIV"
    PASIV = "PASIV"
    AMBELE = "AMBELE"
    NICIUNUL = "NICIUNUL"


@dataclass
class ScenariuRetea:
    """Descrie un scenariu de rețea pentru evaluare."""
    nume: str
    descriere: str
    
    # Configurație client
    client_are_ip_public: bool
    client_firewall_permite_inbound: bool
    client_in_spatele_nat: bool
    
    # Configurație server
    server_are_ip_public: bool
    server_firewall_permite_inbound: bool
    server_porturi_pasive_deschise: bool
    
    # Răspunsul corect pentru verificare
    mod_optim: ModFTP
    justificare: str


# ═══════════════════════════════════════════════════════════════════════════
# SCENARII DE EVALUAT
# ═══════════════════════════════════════════════════════════════════════════

SCENARII = [
    ScenariuRetea(
        nume="Rețea corporativă cu NAT",
        descriere="""
        Clientul este într-o rețea corporativă în spatele unui NAT.
        Serverul FTP este public pe Internet cu toate porturile deschise.
        Firewall-ul corporativ blochează conexiunile inbound.
        """,
        client_are_ip_public=False,
        client_firewall_permite_inbound=False,
        client_in_spatele_nat=True,
        server_are_ip_public=True,
        server_firewall_permite_inbound=True,
        server_porturi_pasive_deschise=True,
        mod_optim=ModFTP.PASIV,
        justificare="NAT și firewall-ul blochează conexiunile inbound. "
                    "Modul pasiv permite clientului să inițieze toate conexiunile."
    ),
    
    ScenariuRetea(
        nume="Rețea internă izolată",
        descriere="""
        Ambele calculatoare sunt în aceeași rețea internă (LAN).
        Nu există firewall între ele.
        Ambele au IP-uri private dar pot comunica direct.
        """,
        client_are_ip_public=False,
        client_firewall_permite_inbound=True,
        client_in_spatele_nat=False,
        server_are_ip_public=False,
        server_firewall_permite_inbound=True,
        server_porturi_pasive_deschise=True,
        mod_optim=ModFTP.AMBELE,
        justificare="Într-o rețea LAN fără firewall-uri, ambele moduri funcționează. "
                    "Modul activ poate fi ușor mai rapid (server inițiază imediat)."
    ),
    
    ScenariuRetea(
        nume="Server protejat, client public",
        descriere="""
        Clientul are IP public și acceptă conexiuni inbound.
        Serverul este într-un DMZ cu firewall strict.
        Serverul NU are porturi passive deschise.
        """,
        client_are_ip_public=True,
        client_firewall_permite_inbound=True,
        client_in_spatele_nat=False,
        server_are_ip_public=True,
        server_firewall_permite_inbound=True,
        server_porturi_pasive_deschise=False,
        mod_optim=ModFTP.ACTIV,
        justificare="Serverul nu poate deschide porturi passive. "
                    "Clientul acceptă conexiuni inbound, deci modul activ funcționează."
    ),
    
    ScenariuRetea(
        nume="Double NAT",
        descriere="""
        Clientul este în spatele unui NAT.
        Serverul este și el în spatele unui NAT (hosting acasă).
        Nici unul nu are port forwarding configurat.
        """,
        client_are_ip_public=False,
        client_firewall_permite_inbound=False,
        client_in_spatele_nat=True,
        server_are_ip_public=False,
        server_firewall_permite_inbound=False,
        server_porturi_pasive_deschise=False,
        mod_optim=ModFTP.NICIUNUL,
        justificare="Double NAT fără port forwarding face imposibilă "
                    "stabilirea conexiunii de date în oricare mod."
    ),
    
    ScenariuRetea(
        nume="Client mobil pe 4G/5G",
        descriere="""
        Clientul este pe o conexiune mobilă (CGNAT - Carrier Grade NAT).
        Serverul este un server FTP public standard.
        Operatorul mobil blochează toate conexiunile inbound.
        """,
        client_are_ip_public=False,
        client_firewall_permite_inbound=False,
        client_in_spatele_nat=True,  # CGNAT
        server_are_ip_public=True,
        server_firewall_permite_inbound=True,
        server_porturi_pasive_deschise=True,
        mod_optim=ModFTP.PASIV,
        justificare="CGNAT este o formă strictă de NAT. "
                    "Doar modul pasiv funcționează pe rețele mobile."
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# FUNCȚII DE IMPLEMENTAT
# ═══════════════════════════════════════════════════════════════════════════

def evalueaza_scenariu(scenariu: ScenariuRetea) -> tuple[ModFTP, str]:
    """
    Evaluează un scenariu de rețea și determină modul FTP optim.
    
    Această funcție trebuie implementată de student.
    
    Argumente:
        scenariu: Obiect ScenariuRetea cu configurația rețelei
        
    Returnează:
        tuple: (ModFTP optim, justificare string)
        
    Logica de decizie:
    
    1. MOD ACTIV funcționează DOAR dacă:
       - Clientul acceptă conexiuni inbound (nu e în spatele NAT strict)
       - Clientul nu are firewall care blochează inbound
       
    2. MOD PASIV funcționează DOAR dacă:
       - Serverul are porturi passive deschise
       - Serverul acceptă conexiuni inbound pe acele porturi
       
    3. AMBELE funcționează dacă condițiile 1 ȘI 2 sunt îndeplinite
    
    4. NICIUNUL dacă nici 1 nici 2 nu sunt îndeplinite
    """
    # TODO: Implementați logica de evaluare
    #
    # Hint: Analizați fiecare condiție pas cu pas
    #
    # activ_posibil = ???
    # pasiv_posibil = ???
    #
    # if activ_posibil and pasiv_posibil:
    #     return ModFTP.AMBELE, "..."
    # elif pasiv_posibil:
    #     return ModFTP.PASIV, "..."
    # elif activ_posibil:
    #     return ModFTP.ACTIV, "..."
    # else:
    #     return ModFTP.NICIUNUL, "..."
    
    raise NotImplementedError("Implementați funcția evalueaza_scenariu()")


def compara_moduri() -> str:
    """
    Generează un tabel comparativ între modurile FTP.
    
    Returnează:
        str: Tabel formatat cu comparație detaliată
    """
    tabel = """
╔══════════════════╦═══════════════════════════╦═══════════════════════════╗
║ Caracteristică   ║ MOD ACTIV (PORT)          ║ MOD PASIV (PASV)          ║
╠══════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Cine inițiază    ║ Server → Client           ║ Client → Server           ║
║ conexiunea date  ║ (Server activ)            ║ (Client activ)            ║
╠══════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Port server date ║ 20 (fix)                  ║ Dinamic (ex: 60000-60100) ║
╠══════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Port client date ║ Specificat de client      ║ Efemer (aleator)          ║
╠══════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Funcționează     ║ ❌ NU                      ║ ✅ DA                      ║
║ prin NAT client  ║                           ║                           ║
╠══════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Funcționează cu  ║ ❌ NU (inbound blocat)     ║ ✅ DA (outbound permis)    ║
║ firewall client  ║                           ║                           ║
╠══════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Cerințe server   ║ Port 20 deschis outbound  ║ Range porturi deschise    ║
║                  ║                           ║ inbound                   ║
╠══════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Utilizare tipică ║ Rețele interne/legacy     ║ Internet, cloud, mobil    ║
╚══════════════════╩═══════════════════════════╩═══════════════════════════╝
"""
    return tabel


# ═══════════════════════════════════════════════════════════════════════════
# DEMONSTRAȚIE
# ═══════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrație a scenariilor și comparației."""
    print("=" * 70)
    print("  DEMO: Comparație Mod Activ vs Pasiv FTP")
    print("=" * 70)
    
    print("\n▶ Tabel Comparativ:\n")
    print(compara_moduri())
    
    print("\n" + "=" * 70)
    print("  SCENARII DE ANALIZĂ")
    print("=" * 70)
    
    for i, scenariu in enumerate(SCENARII, 1):
        print(f"\n{'─' * 70}")
        print(f"  Scenariul {i}: {scenariu.nume}")
        print(f"{'─' * 70}")
        print(scenariu.descriere.strip())
        
        print("\n  Configurație:")
        print(f"    Client IP public: {scenariu.client_are_ip_public}")
        print(f"    Client acceptă inbound: {scenariu.client_firewall_permite_inbound}")
        print(f"    Client în spatele NAT: {scenariu.client_in_spatele_nat}")
        print(f"    Server porturi pasive: {scenariu.server_porturi_pasive_deschise}")
        
        print(f"\n  ✓ Mod Optim: {scenariu.mod_optim.value}")
        print(f"  ✓ Justificare: {scenariu.justificare}")


def test():
    """Testează implementarea studentului."""
    print("=" * 50)
    print("  TEST: Verificare Implementare")
    print("=" * 50)
    
    corecte = 0
    total = len(SCENARII)
    
    for scenariu in SCENARII:
        try:
            mod, justificare = evalueaza_scenariu(scenariu)
            
            if mod == scenariu.mod_optim:
                print(f"  ✓ {scenariu.nume}: CORECT")
                corecte += 1
            else:
                print(f"  ✗ {scenariu.nume}: GREȘIT")
                print(f"      Ai răspuns: {mod.value}")
                print(f"      Corect: {scenariu.mod_optim.value}")
                
        except NotImplementedError:
            print(f"  ⚠ {scenariu.nume}: NEIMPLEMENTAT")
        except Exception as e:
            print(f"  ✗ {scenariu.nume}: EROARE - {e}")
    
    print()
    print("=" * 50)
    print(f"  Rezultat: {corecte}/{total} scenarii corecte")
    print("=" * 50)
    
    return corecte == total


def interactiv():
    """Quiz interactiv pentru student."""
    print("\n" + "=" * 70)
    print("  QUIZ INTERACTIV: Alege Modul FTP Optim")
    print("=" * 70)
    print("\n  Pentru fiecare scenariu, alege: A=Activ, P=Pasiv, B=Ambele, N=Niciunul\n")
    
    scor = 0
    
    for i, scenariu in enumerate(SCENARII, 1):
        print(f"\n{'─' * 70}")
        print(f"  Scenariul {i}: {scenariu.nume}")
        print(f"{'─' * 70}")
        print(scenariu.descriere.strip())
        
        while True:
            raspuns = input("\n  Răspunsul tău (A/P/B/N): ").strip().upper()
            
            if raspuns in ['A', 'P', 'B', 'N']:
                break
            print("  ❌ Răspuns invalid. Folosește A, P, B sau N.")
        
        mapare = {'A': ModFTP.ACTIV, 'P': ModFTP.PASIV, 
                  'B': ModFTP.AMBELE, 'N': ModFTP.NICIUNUL}
        
        if mapare[raspuns] == scenariu.mod_optim:
            print(f"  ✅ CORECT! {scenariu.justificare}")
            scor += 1
        else:
            print(f"  ❌ Greșit. Răspunsul corect: {scenariu.mod_optim.value}")
            print(f"     {scenariu.justificare}")
    
    print("\n" + "=" * 70)
    print(f"  SCOR FINAL: {scor}/{len(SCENARII)}")
    print("=" * 70)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Exercițiul 9.03: Comparație Mod Activ vs Pasiv FTP",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--demo", action="store_true", 
                        help="Demonstrație scenarii și comparație")
    parser.add_argument("--test", action="store_true",
                        help="Verifică implementarea")
    parser.add_argument("--interactiv", action="store_true",
                        help="Quiz interactiv")
    
    args = parser.parse_args()
    
    if not (args.demo or args.test or args.interactiv):
        parser.print_help()
        print("\n[!] Specifică --demo, --test sau --interactiv")
        return
    
    if args.demo:
        demo()
    
    if args.test:
        test()
    
    if args.interactiv:
        interactiv()


if __name__ == "__main__":
    main()
