#!/usr/bin/env python3
"""
Demonstrație Client SSH cu Paramiko
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script demonstrează conectarea SSH programatică folosind biblioteca Paramiko.
Ilustrează conceptele de autentificare, execuție comenzi și transfer de date securizat.

Utilizare:
    python demo_ssh.py                    # Conectare la serverul implicit
    python demo_ssh.py --gazda 192.168.1.1 --port 22
    python demo_ssh.py --interactiv       # Mod shell interactiv
"""

import argparse
import sys
import time

try:
    import paramiko
except ImportError:
    print("Eroare: Biblioteca Paramiko nu este instalată")
    print("Rulați: pip install paramiko")
    sys.exit(1)


# Configurație implicită pentru serverul de laborator
CONFIG_IMPLICIT = {
    "gazda": "localhost",
    "port": 2222,
    "utilizator": "labuser",
    "parola": "labpass",
}


def afiseaza_banner():
    """Afișează bannerul aplicației."""
    print()
    print("=" * 60)
    print("  DEMONSTRAȚIE CLIENT SSH (Paramiko)")
    print("  Laborator Rețele de Calculatoare")
    print("=" * 60)
    print()


def conecteaza_ssh(
    gazda: str,
    port: int,
    utilizator: str,
    parola: str,
    timeout: int = 10
) -> paramiko.SSHClient:
    """
    Creează o conexiune SSH către server.
    
    Args:
        gazda: Adresa serverului SSH
        port: Portul SSH
        utilizator: Numele de utilizator
        parola: Parola
        timeout: Timeout pentru conexiune în secunde
    
    Returns:
        Client SSH conectat
    
    Raises:
        Exception: Dacă conexiunea eșuează
    """
    print(f"  Conectare la {utilizator}@{gazda}:{port}...")
    
    # Creează clientul SSH
    client = paramiko.SSHClient()
    
    # Acceptă automat cheile necunoscute (doar pentru laborator!)
    # În producție, folosiți o politică mai strictă
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(
            hostname=gazda,
            port=port,
            username=utilizator,
            password=parola,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False
        )
        print("  ✓ Conectat cu succes!")
        return client
    
    except paramiko.AuthenticationException:
        print("  ✗ Eroare de autentificare - verificați credențialele")
        raise
    except paramiko.SSHException as e:
        print(f"  ✗ Eroare SSH: {e}")
        raise
    except Exception as e:
        print(f"  ✗ Eroare conexiune: {e}")
        raise


def executa_comanda(client: paramiko.SSHClient, comanda: str) -> tuple:
    """
    Execută o comandă pe serverul remote.
    
    Args:
        client: Clientul SSH conectat
        comanda: Comanda de executat
    
    Returns:
        Tuple (cod_iesire, stdout, stderr)
    """
    print(f"\n  $ {comanda}")
    print("  " + "-" * 40)
    
    stdin, stdout, stderr = client.exec_command(comanda)
    
    # Așteaptă terminarea comenzii
    cod_iesire = stdout.channel.recv_exit_status()
    
    iesire_std = stdout.read().decode('utf-8').strip()
    iesire_err = stderr.read().decode('utf-8').strip()
    
    if iesire_std:
        for linie in iesire_std.split('\n'):
            print(f"    {linie}")
    
    if iesire_err:
        print("  [stderr]:")
        for linie in iesire_err.split('\n'):
            print(f"    {linie}")
    
    print(f"  [cod ieșire: {cod_iesire}]")
    
    return cod_iesire, iesire_std, iesire_err


def demonstratie_comenzi(client: paramiko.SSHClient):
    """Rulează o serie de comenzi demonstrative."""
    print("\n" + "─" * 60)
    print("  DEMONSTRAȚIE COMENZI SSH")
    print("─" * 60)
    
    comenzi = [
        ("whoami", "Identificare utilizator curent"),
        ("hostname", "Numele gazdei"),
        ("pwd", "Directorul curent de lucru"),
        ("ls -la", "Listare fișiere"),
        ("uname -a", "Informații despre sistem"),
        ("cat /etc/os-release | head -5", "Versiunea sistemului de operare"),
        ("date", "Data și ora curentă"),
        ("echo 'Salut din SSH!'", "Afișare mesaj personalizat"),
    ]
    
    for comanda, descriere in comenzi:
        print(f"\n  [{descriere}]")
        executa_comanda(client, comanda)
        time.sleep(0.3)  # Pauză scurtă între comenzi


def demonstratie_sftp(client: paramiko.SSHClient):
    """Demonstrează operații SFTP."""
    print("\n" + "─" * 60)
    print("  DEMONSTRAȚIE SFTP")
    print("─" * 60)
    
    try:
        sftp = client.open_sftp()
        
        # Listare fișiere
        print("\n  Conținutul directorului home:")
        fisiere = sftp.listdir('.')
        for fisier in fisiere:
            stat = sftp.stat(fisier)
            dimensiune = stat.st_size
            print(f"    {fisier:30} {dimensiune:>10} bytes")
        
        # Creare fișier temporar
        nume_fisier = "test_laborator.txt"
        continut = "Acest fișier a fost creat prin SFTP.\nLaborator Rețele de Calculatoare - ASE\n"
        
        print(f"\n  Creare fișier '{nume_fisier}'...")
        with sftp.file(nume_fisier, 'w') as f:
            f.write(continut)
        print("  ✓ Fișier creat")
        
        # Citire fișier
        print(f"\n  Citire fișier '{nume_fisier}':")
        with sftp.file(nume_fisier, 'r') as f:
            for linie in f:
                print(f"    {linie.rstrip()}")
        
        # Ștergere fișier
        print(f"\n  Ștergere fișier '{nume_fisier}'...")
        sftp.remove(nume_fisier)
        print("  ✓ Fișier șters")
        
        sftp.close()
        
    except Exception as e:
        print(f"  ✗ Eroare SFTP: {e}")


def mod_interactiv(client: paramiko.SSHClient):
    """Mod shell interactiv simplu."""
    print("\n" + "─" * 60)
    print("  MOD INTERACTIV")
    print("  Tastați 'exit' sau 'quit' pentru a ieși")
    print("─" * 60)
    
    while True:
        try:
            comanda = input("\n  ssh> ").strip()
            
            if not comanda:
                continue
            
            if comanda.lower() in ('exit', 'quit', 'q'):
                print("  La revedere!")
                break
            
            executa_comanda(client, comanda)
            
        except KeyboardInterrupt:
            print("\n  Întrerupt.")
            break
        except EOFError:
            break


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Demonstrație Client SSH cu Paramiko"
    )
    parser.add_argument(
        "--gazda", "-H",
        default=CONFIG_IMPLICIT["gazda"],
        help=f"Adresa serverului SSH (implicit: {CONFIG_IMPLICIT['gazda']})"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=CONFIG_IMPLICIT["port"],
        help=f"Portul SSH (implicit: {CONFIG_IMPLICIT['port']})"
    )
    parser.add_argument(
        "--utilizator", "-u",
        default=CONFIG_IMPLICIT["utilizator"],
        help=f"Numele de utilizator (implicit: {CONFIG_IMPLICIT['utilizator']})"
    )
    parser.add_argument(
        "--parola", "-P",
        default=CONFIG_IMPLICIT["parola"],
        help="Parola"
    )
    parser.add_argument(
        "--interactiv", "-i",
        action="store_true",
        help="Pornește modul shell interactiv"
    )
    parser.add_argument(
        "--sftp",
        action="store_true",
        help="Include demonstrația SFTP"
    )
    args = parser.parse_args()
    
    afiseaza_banner()
    
    client = None
    
    try:
        # Conectare
        client = conecteaza_ssh(
            gazda=args.gazda,
            port=args.port,
            utilizator=args.utilizator,
            parola=args.parola
        )
        
        if args.interactiv:
            mod_interactiv(client)
        else:
            demonstratie_comenzi(client)
            
            if args.sftp:
                demonstratie_sftp(client)
        
        print("\n" + "=" * 60)
        print("  Demonstrație finalizată cu succes!")
        print("=" * 60)
        return 0
        
    except KeyboardInterrupt:
        print("\n\n  Întrerupt de utilizator")
        return 130
    except Exception as e:
        print(f"\n  Eroare fatală: {e}")
        return 1
    finally:
        if client:
            client.close()
            print("\n  Conexiune închisă.")


if __name__ == "__main__":
    sys.exit(main())
