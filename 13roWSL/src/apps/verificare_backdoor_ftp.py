#!/usr/bin/env python3
"""
Verificator Backdoor FTP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Verifică prezența backdoor-ului vsftpd 2.3.4 (CVE-2011-2523)
într-un mod sigur, fără a-l exploata efectiv.

NOTĂ: Acest script este pentru DETECTARE, nu pentru exploatare.
      În laborator, backdoor-ul este doar simulat.

UTILIZARE:
    python ftp_backdoor_check.py --host localhost --port 2121
"""

import argparse
import socket
import sys
from datetime import datetime


class Culori:
    ROSU = "\033[91m"
    VERDE = "\033[92m"
    GALBEN = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def verifica_banner_ftp(host: str, port: int, timeout: float = 5.0) -> tuple:
    """
    Verifică banner-ul FTP pentru identificarea versiunii.
    
    Returns:
        Tuplu (succes, banner, vulnerabil)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        
        # Verifică dacă este vsftpd 2.3.4
        vulnerabil = "2.3.4" in banner and "vsftpd" in banner.lower()
        
        return True, banner, vulnerabil
        
    except socket.timeout:
        return False, "Timeout la conectare", False
    except ConnectionRefusedError:
        return False, "Conexiune refuzată", False
    except Exception as e:
        return False, str(e), False


def verifica_port_backdoor(host: str, port: int = 6200, timeout: float = 3.0) -> bool:
    """
    Verifică dacă portul de backdoor este deschis.
    
    NOTĂ: Nu încearcă să execute comenzi, doar verifică conectivitatea.
    
    Returns:
        True dacă portul este deschis
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        rezultat = sock.connect_ex((host, port))
        sock.close()
        return rezultat == 0
    except Exception:
        return False


def afiseaza_raport(host: str, port_ftp: int, banner: str, 
                    vulnerabil: bool, backdoor_activ: bool):
    """Afișează raportul de verificare."""
    print("\n" + "=" * 60)
    print(f"{Culori.BOLD}RAPORT VERIFICARE BACKDOOR vsftpd{Culori.RESET}")
    print("=" * 60)
    print(f"Țintă:        {host}")
    print(f"Port FTP:     {port_ftp}")
    print(f"Banner:       {banner}")
    print("-" * 60)
    
    if vulnerabil:
        print(f"\n{Culori.ROSU}[VULNERABIL]{Culori.RESET} Versiune vsftpd 2.3.4 detectată!")
        print(f"""
    ┌────────────────────────────────────────────────────────┐
    │ CVE-2011-2523: Backdoor în vsftpd 2.3.4               │
    ├────────────────────────────────────────────────────────┤
    │ Descriere:                                             │
    │ Între 30 iunie și 1 iulie 2011, serverul de          │
    │ distribuție vsftpd a fost compromis. Versiunea        │
    │ 2.3.4 descărcată conținea un backdoor care           │
    │ deschide un shell pe portul 6200 când utilizatorul    │
    │ se autentifică cu un username conținând ":)"          │
    ├────────────────────────────────────────────────────────┤
    │ Impact: CRITIC (CVSS 10.0)                            │
    │ - Acces complet la sistem fără autentificare          │
    │ - Execuție de cod arbitrar                            │
    └────────────────────────────────────────────────────────┘
        """)
    else:
        print(f"\n{Culori.VERDE}[OK]{Culori.RESET} Versiunea vsftpd nu pare a fi 2.3.4")
    
    print("-" * 60)
    print(f"Port backdoor (6200): ", end="")
    
    if backdoor_activ:
        print(f"{Culori.ROSU}DESCHIS ⚠️{Culori.RESET}")
        print(f"""
    {Culori.ROSU}[ALERTĂ]{Culori.RESET} Portul de backdoor este activ!
    
    În mediu real, aceasta ar indica:
    - Backdoor-ul a fost activat
    - Sistemul este potențial compromis
    - Necesită investigare imediată
    
    NOTĂ: În acest laborator, backdoor-ul este SIMULAT
          și nu execută efectiv comenzi.
        """)
    else:
        print(f"{Culori.VERDE}ÎNCHIS ✓{Culori.RESET}")
    
    print("=" * 60)
    
    # Recomandări
    print(f"\n{Culori.CYAN}Recomandări:{Culori.RESET}")
    print("  1. Actualizați vsftpd la versiunea 2.3.5 sau mai nouă")
    print("  2. Verificați integritatea surselor software (hash-uri)")
    print("  3. Monitorizați porturile neobișnuite (6200)")
    print("  4. Verificați log-urile pentru autentificări suspecte")
    print("  5. Considerați migrarea la SFTP (SSH File Transfer)")


def main():
    parser = argparse.ArgumentParser(
        description="Verificator Backdoor vsftpd 2.3.4 (CVE-2011-2523)",
        epilog="Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix"
    )
    parser.add_argument("--host", "-H", default="localhost",
                        help="Host-ul de verificat (implicit: localhost)")
    parser.add_argument("--port", "-p", type=int, default=2121,
                        help="Port FTP (implicit: 2121)")
    parser.add_argument("--timeout", "-t", type=float, default=5.0,
                        help="Timeout în secunde")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"{Culori.BOLD}VERIFICATOR BACKDOOR FTP - SĂPTĂMÂNA 13{Culori.RESET}")
    print("=" * 60)
    print(f"\n{Culori.GALBEN}NOTĂ: Acest script DETECTEAZĂ, nu exploatează!{Culori.RESET}\n")
    
    print(f"[INFO] Verificare {args.host}:{args.port}...")
    
    # Verifică banner-ul FTP
    succes, banner, vulnerabil = verifica_banner_ftp(
        args.host, args.port, args.timeout
    )
    
    if not succes:
        print(f"{Culori.ROSU}[EROARE]{Culori.RESET} Nu s-a putut conecta: {banner}")
        return 1
    
    # Verifică portul de backdoor
    print(f"[INFO] Verificare port backdoor 6200...")
    backdoor_activ = verifica_port_backdoor(args.host, 6200, args.timeout)
    
    # Afișează raportul
    afiseaza_raport(args.host, args.port, banner, vulnerabil, backdoor_activ)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
