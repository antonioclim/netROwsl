#!/usr/bin/env python3
"""
Executor Demonstrații Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script execută demonstrații automatizate pentru prezentarea
conceptelor de filtrare a pachetelor în laborator.
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.network_utils import UtilitareRetea

logger = configureaza_logger("ruleaza_demo")


def incarca_profile() -> dict:
    """Încarcă profilele de firewall din fișierul JSON."""
    cale_profile = RADACINA_PROIECT / "docker" / "configs" / "firewall_profiles.json"
    with open(cale_profile, 'r', encoding='utf-8') as f:
        return json.load(f)


def aplica_profil(nume_profil: str) -> bool:
    """
    Aplică un profil de firewall.
    
    Args:
        nume_profil: Numele profilului de aplicat
    
    Returns:
        True dacă profilul a fost aplicat cu succes
    """
    logger.info(f"Aplicare profil firewall: {nume_profil}")
    
    # În acest exemplu, doar simulăm aplicarea profilului
    # Într-o implementare reală, s-ar folosi iptables sau firewallctl.py
    profile = incarca_profile()
    
    profil_gasit = None
    for profil in profile.get("profiles", []):
        if profil.get("name") == nume_profil:
            profil_gasit = profil
            break
    
    if not profil_gasit:
        logger.error(f"Profilul '{nume_profil}' nu a fost găsit")
        return False
    
    logger.info(f"  Descriere: {profil_gasit.get('description', 'N/A')}")
    reguli = profil_gasit.get("rules", [])
    logger.info(f"  Număr reguli: {len(reguli)}")
    
    for regula in reguli:
        protocol = regula.get("protocol", "?")
        port = regula.get("port", "?")
        actiune = regula.get("action", "?")
        logger.info(f"    {protocol.upper()} port {port} -> {actiune}")
    
    return True


def demo_referinta():
    """Demonstrație: Conectivitate de referință (fără filtrare)."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMO: Conectivitate de Referință")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Acest demo verifică conectivitatea normală TCP și UDP")
    logger.info("fără nicio regulă de filtrare activă.")
    logger.info("")
    
    aplica_profil("referinta")
    
    logger.info("")
    logger.info("Test TCP Echo (port 9090):")
    ok, mesaj = UtilitareRetea.test_echo_tcp("localhost", 9090, "hello_demo")
    if ok:
        logger.info(f"  [OK] Echo funcțional: '{mesaj.strip()}'")
    else:
        logger.warning(f"  [AVERTISMENT] {mesaj}")
    
    logger.info("")
    logger.info("Test UDP (port 9091):")
    ok, mesaj = UtilitareRetea.test_trimitere_udp("localhost", 9091, "hello_udp")
    if ok:
        logger.info(f"  [OK] {mesaj}")
    else:
        logger.warning(f"  [AVERTISMENT] {mesaj}")


def demo_tcp_reject():
    """Demonstrație: Filtrare TCP cu REJECT."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMO: Filtrare TCP cu REJECT")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Acest demo arată comportamentul când TCP este blocat")
    logger.info("folosind acțiunea REJECT (trimite RST sau ICMP).")
    logger.info("")
    
    aplica_profil("blocare_tcp_9090")
    
    logger.info("")
    logger.info("Test conexiune TCP (port 9090):")
    
    timp_start = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        rezultat = sock.connect_ex(("localhost", 9090))
        sock.close()
        timp_scurs = time.time() - timp_start
        
        if rezultat == 0:
            logger.info(f"  [INFO] Conexiune reușită în {timp_scurs:.3f}s")
            logger.info("         (Profilul de filtrare nu este activ pe acest host)")
        else:
            logger.info(f"  [OK] Conexiune refuzată în {timp_scurs:.3f}s")
            logger.info("       Aceasta este comportamentul REJECT - eșec rapid!")
            
    except ConnectionRefusedError:
        timp_scurs = time.time() - timp_start
        logger.info(f"  [OK] Conexiune refuzată în {timp_scurs:.3f}s")
        logger.info("       Aceasta este comportamentul REJECT tipic")
    except socket.timeout:
        logger.info("  [INFO] Timeout - aceasta seamănă cu comportamentul DROP")
    except Exception as e:
        logger.error(f"  [EROARE] {e}")


def demo_udp_drop():
    """Demonstrație: Filtrare UDP cu DROP."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMO: Filtrare UDP cu DROP")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Acest demo arată comportamentul când UDP este blocat")
    logger.info("folosind acțiunea DROP (eliminare silențioasă).")
    logger.info("")
    
    aplica_profil("blocare_udp_9091")
    
    logger.info("")
    logger.info("Test trimitere UDP (port 9091):")
    
    ok, mesaj = UtilitareRetea.test_trimitere_udp(
        "localhost", 9091, 
        "test_drop",
        asteapta_raspuns=True
    )
    
    if ok:
        logger.info(f"  [INFO] {mesaj}")
    else:
        logger.info(f"  [OK] {mesaj}")
        logger.info("       Aceasta este comportamentul DROP - niciun răspuns!")
        logger.info("       Nu se poate distinge de pierderea pachetelor.")


def demo_sondare():
    """Demonstrație: Sondare defensivă a porturilor."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMO: Sondare Defensivă a Porturilor")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Acest demo arată cum să identificați starea porturilor")
    logger.info("și să detectați regulile de firewall.")
    logger.info("")
    
    rezultate = UtilitareRetea.sondeaza_porturi(
        "localhost",
        (9085, 9095),
        timeout_per_port=1.0
    )
    
    logger.info("")
    logger.info("Interpretare rezultate:")
    logger.info("  DESCHIS  = Serviciu activ, acceptă conexiuni")
    logger.info("  ÎNCHIS   = Niciun serviciu, port accesibil")
    logger.info("  FILTRAT  = Firewall DROP activ")


def demo_reject_vs_drop():
    """Demonstrație: Comparație REJECT vs DROP."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMO: Comparație REJECT vs DROP")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Acest demo compară direct comportamentul REJECT și DROP")
    logger.info("pentru a evidenția diferențele de timp și răspuns.")
    logger.info("")
    
    # Faza 1: REJECT
    logger.info("-" * 40)
    logger.info("Faza 1: Test cu REJECT")
    logger.info("-" * 40)
    
    aplica_profil("blocare_tcp_9090")
    
    timp_start = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        rezultat = sock.connect_ex(("localhost", 9090))
        sock.close()
    except Exception:
        pass
    timp_reject = time.time() - timp_start
    
    logger.info(f"  Timp răspuns REJECT: {timp_reject:.3f} secunde")
    
    # Faza 2: DROP (simulat)
    logger.info("")
    logger.info("-" * 40)
    logger.info("Faza 2: Test cu DROP (simulat)")
    logger.info("-" * 40)
    
    aplica_profil("blocare_tcp_drop")
    
    timp_start = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)  # Timeout mai scurt pentru demo
        rezultat = sock.connect_ex(("localhost", 9090))
        sock.close()
    except socket.timeout:
        pass
    except Exception:
        pass
    timp_drop = time.time() - timp_start
    
    logger.info(f"  Timp răspuns DROP: {timp_drop:.3f} secunde")
    
    # Analiză
    logger.info("")
    logger.info("=" * 60)
    logger.info("ANALIZĂ")
    logger.info("=" * 60)
    logger.info("")
    logger.info(f"REJECT: {timp_reject:.3f}s - Eșec rapid, dezvăluie prezența firewall-ului")
    logger.info(f"DROP:   {timp_drop:.3f}s - Eșec lent (timeout), pare o problemă de rețea")
    logger.info("")
    logger.info("Compromis de securitate:")
    logger.info("  - REJECT este prietenos cu utilizatorul dar dezvăluie configurația")
    logger.info("  - DROP este mai discret dar cauzează timeout-uri în aplicații")


def demo_complet():
    """Rulează toate demonstrațiile secvențial."""
    logger.info("")
    logger.info("╔══════════════════════════════════════════════════════════╗")
    logger.info("║          DEMONSTRAȚIE COMPLETĂ SĂPTĂMÂNA 7              ║")
    logger.info("║   Interceptarea și Filtrarea Pachetelor                 ║")
    logger.info("╚══════════════════════════════════════════════════════════╝")
    
    demos = [
        ("Referință", demo_referinta),
        ("TCP REJECT", demo_tcp_reject),
        ("UDP DROP", demo_udp_drop),
        ("Sondare Porturi", demo_sondare),
        ("REJECT vs DROP", demo_reject_vs_drop),
    ]
    
    for i, (nume, functie) in enumerate(demos, 1):
        logger.info("")
        logger.info(f">>> Demo {i}/{len(demos)}: {nume}")
        input("    Apăsați Enter pentru a continua...")
        functie()
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Demonstrație completă finalizată!")
    logger.info("=" * 60)


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Execută demonstrații pentru Laboratorul Săptămânii 7"
    )
    parser.add_argument(
        "--demo", "-d",
        choices=["referinta", "tcp", "udp", "sondare", "reject_vs_drop", "complet"],
        default="complet",
        help="Demonstrația de rulat (implicit: complet)"
    )
    parser.add_argument(
        "--listeaza",
        action="store_true",
        help="Listează demonstrațiile disponibile"
    )
    args = parser.parse_args()

    if args.listeaza:
        print("Demonstrații disponibile:")
        print("  referinta     - Conectivitate de referință fără filtrare")
        print("  tcp           - Filtrare TCP cu REJECT")
        print("  udp           - Filtrare UDP cu DROP")
        print("  sondare       - Sondare defensivă a porturilor")
        print("  reject_vs_drop - Comparație directă REJECT vs DROP")
        print("  complet       - Toate demonstrațiile secvențial")
        return 0

    logger.info("=" * 60)
    logger.info("Demonstrații Laborator Săptămâna 7")
    logger.info("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    logger.info("=" * 60)

    demos = {
        "referinta": demo_referinta,
        "tcp": demo_tcp_reject,
        "udp": demo_udp_drop,
        "sondare": demo_sondare,
        "reject_vs_drop": demo_reject_vs_drop,
        "complet": demo_complet,
    }

    try:
        demos[args.demo]()
        return 0
    except KeyboardInterrupt:
        logger.info("\nDemonstrație întreruptă de utilizator")
        return 0
    except Exception as e:
        logger.error(f"Eroare în timpul demonstrației: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
