#!/usr/bin/env python3
"""
Demonstrații Automate pentru Laborator
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script rulează demonstrații interactive pentru prezentări în clasă.
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
from pathlib import Path
from typing import Optional

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("demo")

# Culori ANSI
CYAN = "\033[96m"
VERDE = "\033[92m"
GALBEN = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def afiseaza_titlu(titlu: str) -> None:
    """Afișează un titlu formatat pentru demonstrație."""
    print()
    print(f"{BOLD}{CYAN}{'═' * 70}{RESET}")
    print(f"{BOLD}{CYAN}  {titlu}{RESET}")
    print(f"{BOLD}{CYAN}{'═' * 70}{RESET}")
    print()


def afiseaza_comanda(comanda: str, descriere: str = "") -> None:
    """Afișează o comandă care va fi executată."""
    if descriere:
        print(f"{GALBEN}# {descriere}{RESET}")
    print(f"{VERDE}$ {comanda}{RESET}")


def executa_in_container(
    comanda: str,
    container: str = "week1_lab",
    interactiv: bool = False
) -> str:
    """Execută o comandă în container și returnează rezultatul."""
    cmd = ["docker", "exec"]
    if interactiv:
        cmd.append("-it")
    cmd.extend([container, "bash", "-c", comanda])
    
    rezultat = subprocess.run(cmd, capture_output=True, text=True)
    return rezultat.stdout + rezultat.stderr


def asteapta_utilizator(mesaj: str = "Apăsați Enter pentru a continua...") -> None:
    """Așteaptă confirmarea utilizatorului."""
    input(f"\n{GALBEN}{mesaj}{RESET}")


def demo_diagnostic_retea() -> None:
    """Demonstrație: Comenzi de diagnostic de rețea."""
    afiseaza_titlu("DEMO 1: DIAGNOSTIC DE REȚEA")
    
    print("Această demonstrație prezintă comenzile de bază pentru")
    print("inspectarea configurației de rețea într-un sistem Linux.")
    
    # Pas 1: Interfețe
    asteapta_utilizator()
    afiseaza_comanda("ip addr show", "Afișează toate interfețele de rețea")
    print()
    print(executa_in_container("ip addr show"))
    
    # Pas 2: Format scurt
    asteapta_utilizator()
    afiseaza_comanda("ip -br addr show", "Format scurt pentru vizualizare rapidă")
    print()
    print(executa_in_container("ip -br addr show"))
    
    # Pas 3: Tabela de rutare
    asteapta_utilizator()
    afiseaza_comanda("ip route show", "Afișează tabela de rutare")
    print()
    print(executa_in_container("ip route show"))
    
    # Pas 4: Socket-uri active
    asteapta_utilizator()
    afiseaza_comanda("ss -tunap", "Afișează socket-uri TCP/UDP active")
    print()
    print(executa_in_container("ss -tunap"))
    
    # Pas 5: Test conectivitate
    asteapta_utilizator()
    afiseaza_comanda("ping -c 3 127.0.0.1", "Test conectivitate loopback")
    print()
    print(executa_in_container("ping -c 3 127.0.0.1"))
    
    afiseaza_titlu("DEMO 1: FINALIZAT")


def demo_tcp_vs_udp() -> None:
    """Demonstrație: Comparație TCP vs UDP."""
    afiseaza_titlu("DEMO 2: COMPARAȚIE TCP vs UDP")
    
    print("Această demonstrație compară comportamentul protocoalelor")
    print("TCP (orientat pe conexiune) și UDP (fără conexiune).")
    
    # TCP Demo
    asteapta_utilizator()
    afiseaza_comanda("# Demonstrație TCP", "Pornire server TCP și trimitere mesaj")
    print()
    
    # Pornim serverul TCP în fundal
    print(f"{GALBEN}Se pornește serverul TCP pe portul 9999...{RESET}")
    executa_in_container("timeout 5 nc -l -p 9999 &")
    time.sleep(1)
    
    # Trimitem un mesaj
    print(f"{GALBEN}Se trimite mesaj la server...{RESET}")
    rezultat = executa_in_container('echo "Salut TCP!" | nc -q 1 localhost 9999')
    print(f"Rezultat: {rezultat}")
    
    # Verificăm starea socket-urilor
    asteapta_utilizator()
    afiseaza_comanda("ss -tn state established", "Verifică conexiunile stabilite")
    print()
    print(executa_in_container("ss -tn state established || echo 'Nicio conexiune activă'"))
    
    # UDP Demo
    asteapta_utilizator()
    afiseaza_comanda("# Demonstrație UDP", "Trimitere mesaj UDP (fără conexiune)")
    print()
    
    # Pornim receptorul UDP
    print(f"{GALBEN}Se pornește receptorul UDP pe portul 9998...{RESET}")
    executa_in_container("timeout 5 nc -u -l -p 9998 &")
    time.sleep(1)
    
    # Trimitem datagram
    print(f"{GALBEN}Se trimite datagram UDP...{RESET}")
    executa_in_container('echo "Salut UDP!" | nc -u -q 1 localhost 9998')
    
    # Explicație diferențe
    asteapta_utilizator()
    print()
    print(f"{BOLD}DIFERENȚE CHEIE:{RESET}")
    print()
    print("┌────────────────┬────────────────────────┬────────────────────────┐")
    print("│    Aspect      │          TCP           │          UDP           │")
    print("├────────────────┼────────────────────────┼────────────────────────┤")
    print("│ Conexiune      │ Necesară (handshake)   │ Fără conexiune         │")
    print("│ Fiabilitate    │ Garantată              │ Best-effort            │")
    print("│ Ordonare       │ Păstrată               │ Negarantată            │")
    print("│ Overhead       │ Mai mare (20+ bytes)   │ Mai mic (8 bytes)      │")
    print("│ Viteză         │ Mai lent               │ Mai rapid              │")
    print("└────────────────┴────────────────────────┴────────────────────────┘")
    
    afiseaza_titlu("DEMO 2: FINALIZAT")


def demo_socket_python() -> None:
    """Demonstrație: Programare socket în Python."""
    afiseaza_titlu("DEMO 3: SOCKET-URI PYTHON")
    
    print("Această demonstrație prezintă programarea socket-urilor în Python,")
    print("arătând atât partea de server cât și partea de client.")
    
    # Cod server
    asteapta_utilizator()
    print(f"{BOLD}COD SERVER TCP:{RESET}")
    print()
    cod_server = '''
import socket

# Creează socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Legare la adresă și port
server.bind(('0.0.0.0', 9999))
server.listen(1)

print('Serverul ascultă pe portul 9999...')
conn, addr = server.accept()
print(f'Conectat de la: {addr}')

# Primește și trimite date
data = conn.recv(1024)
print(f'Primit: {data.decode()}')
conn.send(b'Mesaj primit!')

conn.close()
server.close()
'''
    print(f"{CYAN}{cod_server}{RESET}")
    
    # Cod client
    asteapta_utilizator()
    print(f"{BOLD}COD CLIENT TCP:{RESET}")
    print()
    cod_client = '''
import socket

# Creează socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectare la server
client.connect(('localhost', 9999))

# Trimite și primește date
client.send(b'Salut de la client!')
response = client.recv(1024)
print(f'Răspuns: {response.decode()}')

client.close()
'''
    print(f"{CYAN}{cod_client}{RESET}")
    
    # Rulează exercițiul
    asteapta_utilizator("Apăsați Enter pentru a rula exercițiul...")
    print()
    print(f"{GALBEN}Se rulează exercițiul server-client...{RESET}")
    print()
    
    rezultat = executa_in_container("cd /work/src/exercises && python ex_1_02_tcp_server_client.py 2>&1 || echo 'Verificați dacă exercițiul există'")
    print(rezultat)
    
    afiseaza_titlu("DEMO 3: FINALIZAT")


def lista_demonstratii() -> None:
    """Afișează lista demonstrațiilor disponibile."""
    print()
    print(f"{BOLD}DEMONSTRAȚII DISPONIBILE:{RESET}")
    print()
    print("  1. Diagnostic de Rețea")
    print("     Comenzi: ip addr, ip route, ss, ping")
    print("     Durată: ~5 minute")
    print()
    print("  2. Comparație TCP vs UDP")
    print("     Demonstrează diferențele dintre protocoale")
    print("     Durată: ~5 minute")
    print()
    print("  3. Socket-uri Python")
    print("     Programarea socket-urilor client-server")
    print("     Durată: ~7 minute")
    print()


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Demonstrații Automate pentru Laborator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python ruleaza_demo.py --lista        # Afișează demonstrațiile disponibile
  python ruleaza_demo.py --demo 1       # Rulează Demo 1
  python ruleaza_demo.py --demo 2       # Rulează Demo 2
  python ruleaza_demo.py --toate        # Rulează toate demonstrațiile
        """
    )
    parser.add_argument(
        "--demo",
        type=int,
        choices=[1, 2, 3],
        help="Numărul demonstrației de rulat"
    )
    parser.add_argument(
        "--lista",
        action="store_true",
        help="Afișează lista demonstrațiilor disponibile"
    )
    parser.add_argument(
        "--toate",
        action="store_true",
        help="Rulează toate demonstrațiile"
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + "  DEMONSTRAȚII LABORATOR SĂPTĂMÂNA 1".center(68) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE, Informatică".center(68) + "║")
    print("╚" + "═" * 68 + "╝")

    if args.lista:
        lista_demonstratii()
        return 0

    # Verifică dacă containerul rulează
    rezultat = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", "week1_lab"],
        capture_output=True,
        text=True
    )
    
    if "true" not in rezultat.stdout.lower():
        logger.error("Containerul week1_lab nu rulează!")
        logger.error("Porniți mai întâi laboratorul cu: python scripts/porneste_lab.py")
        return 1

    try:
        if args.toate:
            demo_diagnostic_retea()
            demo_tcp_vs_udp()
            demo_socket_python()
        elif args.demo == 1:
            demo_diagnostic_retea()
        elif args.demo == 2:
            demo_tcp_vs_udp()
        elif args.demo == 3:
            demo_socket_python()
        else:
            lista_demonstratii()
            print(f"{GALBEN}Utilizați --demo N pentru a rula o demonstrație{RESET}")
            return 0

        print()
        print(f"{VERDE}✓ Demonstrație finalizată cu succes!{RESET}")
        print()
        return 0

    except KeyboardInterrupt:
        print(f"\n{GALBEN}Demonstrație întreruptă de utilizator{RESET}")
        return 130
    except Exception as e:
        logger.error(f"Eroare în timpul demonstrației: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
