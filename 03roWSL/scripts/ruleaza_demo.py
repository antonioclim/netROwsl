#!/usr/bin/env python3
"""
Demonstrații Automate - Săptămâna 3
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Rulează demonstrații automate pentru conceptele săptămânii.

Utilizare:
    python scripts/ruleaza_demo.py --demo broadcast
    python scripts/ruleaza_demo.py --demo multicast  
    python scripts/ruleaza_demo.py --demo tunel
    python scripts/ruleaza_demo.py --demo toate
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import time
import argparse
import threading
from pathlib import Path

# Adaugă rădăcina proiectului în PATH

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("ruleaza_demo")



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def ruleaza_in_container(container: str, comanda: str, timeout: int = 30) -> tuple:
    """
    Rulează o comandă într-un container Docker.
    
    Args:
        container: Numele containerului (cu sau fără prefix week3_)
        comanda: Comanda de executat
        timeout: Timeout în secunde
        
    Returns:
        Tuple (success, output)
    """
    if not container.startswith("week3_"):
        container = f"week3_{container}"
    
    try:
        rezultat = subprocess.run(
            ["docker", "exec", container, "bash", "-c", comanda],
            capture_output=True,
            timeout=timeout
        )
        return rezultat.returncode == 0, rezultat.stdout.decode() + rezultat.stderr.decode()
    except subprocess.TimeoutExpired:
        return False, "Timeout expirat"
    except Exception as e:
        return False, str(e)


def demo_broadcast():
    """Demonstrație transmisie broadcast UDP."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMONSTRAȚIE: Transmisie Broadcast UDP")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Broadcast-ul permite transmiterea unui mesaj către")
    logger.info("toate dispozitivele din segmentul de rețea simultan.")
    logger.info("")
    
    # Verifică dacă receiver-ul este pornit
    succes, _ = ruleaza_in_container("receiver", "echo test", timeout=5)
    if not succes:
        logger.warning("Containerul receiver nu este pornit!")
        logger.warning("Porniți cu: python scripts/porneste_lab.py --broadcast")
        logger.info("")
        logger.info("Continuăm demonstrația doar cu client...")
    
    logger.info("PASUL 1: Pornire receptor broadcast în fundal")
    logger.info("-" * 40)
    
    # Pornește receiver-ul în fundal
    def receiver_background():
        ruleaza_in_container(
            "client",
            "timeout 15 python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod receiver 2>&1 | head -20",
            timeout=20
        )
    
    thread_receiver = threading.Thread(target=receiver_background)
    thread_receiver.start()
    time.sleep(2)
    
    logger.info("PASUL 2: Transmitere mesaje broadcast")
    logger.info("-" * 40)
    
    succes, output = ruleaza_in_container(
        "server",
        "python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod sender --numar 3",
        timeout=15
    )
    
    if succes:
        logger.info("Mesaje transmise cu succes:")
        for linie in output.strip().split('\n')[:10]:
            logger.info(f"  {linie}")
    else:
        logger.error(f"Eroare la transmisie: {output}")
    
    thread_receiver.join(timeout=5)
    
    logger.info("")
    logger.info("OBSERVAȚII:")
    logger.info("  • Adresa destinație: 255.255.255.255 (broadcast limitat)")
    logger.info("  • Adresa MAC destinație: ff:ff:ff:ff:ff:ff")
    logger.info("  • Toate dispozitivele din rețea primesc pachetul")
    logger.info("  • Nu există confirmare de primire (UDP)")
    logger.info("")


def demo_multicast():
    """Demonstrație comunicare multicast UDP."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMONSTRAȚIE: Comunicare Multicast UDP")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Multicast-ul permite comunicarea eficientă cu un")
    logger.info("grup selectat de receptori prin protocoalul IGMP.")
    logger.info("")
    
    logger.info("PASUL 1: Verificare suport multicast în container")
    logger.info("-" * 40)
    
    succes, output = ruleaza_in_container(
        "client",
        "cat /proc/net/igmp | head -5",
        timeout=10
    )
    
    if succes:
        logger.info("Suport IGMP activ:")
        for linie in output.strip().split('\n'):
            logger.info(f"  {linie}")
    
    logger.info("")
    logger.info("PASUL 2: Înscriere în grup și recepție")
    logger.info("-" * 40)
    
    # Pornește receiver multicast în fundal
    def multicast_receiver():
        ruleaza_in_container(
            "client",
            "timeout 15 python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver 2>&1 | head -15",
            timeout=20
        )
    
    thread_receiver = threading.Thread(target=multicast_receiver)
    thread_receiver.start()
    time.sleep(3)
    
    logger.info("PASUL 3: Transmitere mesaje către grup")
    logger.info("-" * 40)
    
    succes, output = ruleaza_in_container(
        "server",
        "python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod sender --numar 3",
        timeout=15
    )
    
    if succes:
        logger.info("Mesaje transmise către grup multicast:")
        for linie in output.strip().split('\n')[:10]:
            logger.info(f"  {linie}")
    
    thread_receiver.join(timeout=5)
    
    # Verifică apartenența la grup
    logger.info("")
    logger.info("PASUL 4: Verificare apartenență IGMP")
    logger.info("-" * 40)
    
    succes, output = ruleaza_in_container(
        "client",
        "ip maddr show dev eth0",
        timeout=10
    )
    
    if succes and output:
        logger.info("Grupuri multicast pe eth0:")
        for linie in output.strip().split('\n'):
            logger.info(f"  {linie}")
    
    logger.info("")
    logger.info("OBSERVAȚII:")
    logger.info("  • Adresa grup: 239.0.0.1 (administrativ scoped)")
    logger.info("  • IGMP gestionează apartenența la grup")
    logger.info("  • Doar membrii grupului primesc traficul")
    logger.info("  • Mai eficient decât broadcast pentru grupuri selectate")
    logger.info("")


def demo_tunel():
    """Demonstrație tunel TCP."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMONSTRAȚIE: Tunel TCP Bidirecțional")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Tunelul TCP redirecționează conexiunile transparent")
    logger.info("între client și server prin intermediarul (router).")
    logger.info("")
    
    logger.info("PASUL 1: Test conexiune directă la server")
    logger.info("-" * 40)
    
    succes, output = ruleaza_in_container(
        "client",
        "echo 'Test DIRECT' | nc -q1 172.20.0.10 8080",
        timeout=10
    )
    
    if succes:
        logger.info(f"Răspuns server (direct): {output.strip()}")
    else:
        logger.error(f"Eroare conexiune directă: {output}")
    
    logger.info("")
    logger.info("PASUL 2: Test conexiune prin tunel")
    logger.info("-" * 40)
    
    succes, output = ruleaza_in_container(
        "client",
        "echo 'Test prin TUNEL' | nc -q1 172.20.0.254 9090",
        timeout=10
    )
    
    if succes:
        logger.info(f"Răspuns server (prin tunel): {output.strip()}")
    else:
        logger.error(f"Eroare conexiune tunel: {output}")
    
    logger.info("")
    logger.info("PASUL 3: Verificare conexiuni active pe router")
    logger.info("-" * 40)
    
    succes, output = ruleaza_in_container(
        "router",
        "ss -tnp | grep -E '(8080|9090)' | head -5",
        timeout=10
    )
    
    if succes and output:
        logger.info("Conexiuni TCP pe router:")
        for linie in output.strip().split('\n'):
            logger.info(f"  {linie}")
    
    logger.info("")
    logger.info("OBSERVAȚII:")
    logger.info("  • Client se conectează la router (172.20.0.254:9090)")
    logger.info("  • Router creează conexiune către server (172.20.0.10:8080)")
    logger.info("  • Datele sunt relayate bidirecțional")
    logger.info("  • Clientul nu cunoaște adresa reală a serverului")
    logger.info("")


def demo_toate():
    """Rulează toate demonstrațiile."""
    demo_broadcast()
    input("\nApăsați Enter pentru demonstrația următoare...")
    
    demo_multicast()
    input("\nApăsați Enter pentru demonstrația următoare...")
    
    demo_tunel()



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Rulează demonstrații automate pentru Săptămâna 3"
    )
    parser.add_argument(
        "--demo", "-d",
        type=str,
        required=True,
        choices=["broadcast", "multicast", "tunel", "toate"],
        help="Demonstrația de rulat"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Demonstrații Automate - Săptămâna 3")
    logger.info("Rețele de Calculatoare - ASE, Informatică Economică")
    logger.info("=" * 60)

    # Verifică că laboratorul este pornit
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=week3_server", "--format", "{{.Names}}"],
            capture_output=True,
            timeout=10
        )
        if "week3_server" not in rezultat.stdout.decode():
            logger.error("Laboratorul nu este pornit!")
            logger.error("Rulați: python scripts/porneste_lab.py")
            return 1
    except Exception as e:
        logger.error(f"Eroare la verificarea containerelor: {e}")
        return 1

    # Rulează demonstrația selectată
    demonstratii = {
        "broadcast": demo_broadcast,
        "multicast": demo_multicast,
        "tunel": demo_tunel,
        "toate": demo_toate
    }
    
    demonstratii[args.demo]()
    
    logger.info("=" * 60)
    logger.info("Demonstrație finalizată!")
    logger.info("=" * 60)
    
    return 0



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
