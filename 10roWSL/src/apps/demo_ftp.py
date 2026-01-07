#!/usr/bin/env python3
"""
Demonstrație Client FTP
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script demonstrează operațiile FTP folosind biblioteca ftplib.
Ilustrează conectarea, navigarea, transferul de fișiere și diferența
între modul activ și pasiv.

Utilizare:
    python demo_ftp.py                    # Conectare la serverul implicit
    python demo_ftp.py --gazda 192.168.1.1 --port 21
    python demo_ftp.py --activ            # Folosește modul activ
"""

import argparse
import sys
import os
import tempfile
from ftplib import FTP, error_perm
from io import BytesIO


# Configurație implicită pentru serverul de laborator
CONFIG_IMPLICIT = {
    "gazda": "localhost",
    "port": 2121,
    "utilizator": "labftp",
    "parola": "labftp",
}


def afiseaza_banner():
    """Afișează bannerul aplicației."""
    print()
    print("=" * 60)
    print("  DEMONSTRAȚIE CLIENT FTP")
    print("  Laborator Rețele de Calculatoare")
    print("=" * 60)
    print()


def conecteaza_ftp(
    gazda: str,
    port: int,
    utilizator: str,
    parola: str,
    mod_pasiv: bool = True
) -> FTP:
    """
    Creează o conexiune FTP către server.
    
    Args:
        gazda: Adresa serverului FTP
        port: Portul FTP
        utilizator: Numele de utilizator
        parola: Parola
        mod_pasiv: True pentru modul pasiv, False pentru activ
    
    Returns:
        Conexiune FTP activă
    """
    print(f"  Conectare la {gazda}:{port}...")
    print(f"  Mod transfer: {'PASIV' if mod_pasiv else 'ACTIV'}")
    
    try:
        ftp = FTP()
        ftp.connect(gazda, port, timeout=10)
        
        # Setează modul de transfer
        ftp.set_pasv(mod_pasiv)
        
        # Autentificare
        raspuns = ftp.login(utilizator, parola)
        print(f"  ✓ {raspuns}")
        
        return ftp
        
    except Exception as e:
        print(f"  ✗ Eroare conectare: {e}")
        raise


def afiseaza_informatii_server(ftp: FTP):
    """Afișează informații despre serverul FTP."""
    print("\n" + "─" * 60)
    print("  INFORMAȚII SERVER")
    print("─" * 60)
    
    try:
        # Mesaj de bun venit
        print(f"\n  Mesaj bun venit: {ftp.getwelcome()}")
        
        # Director curent
        print(f"  Director curent: {ftp.pwd()}")
        
        # Tip sistem
        print(f"  Tip sistem: {ftp.sendcmd('SYST')}")
        
        # Funcționalități suportate
        print("\n  Funcționalități suportate:")
        try:
            raspuns = ftp.sendcmd('FEAT')
            for linie in raspuns.split('\n'):
                if linie.strip() and not linie.startswith('211'):
                    print(f"    {linie.strip()}")
        except error_perm:
            print("    [FEAT nu este suportat]")
            
    except Exception as e:
        print(f"  Eroare: {e}")


def listeaza_fisiere(ftp: FTP, cale: str = "."):
    """Listează fișierele din directorul specificat."""
    print(f"\n  Conținutul directorului '{cale}':")
    print("  " + "-" * 50)
    
    try:
        # Folosim MLSD dacă e disponibil, altfel LIST
        try:
            for nume, atribute in ftp.mlsd(cale):
                tip = atribute.get('type', '?')
                dimensiune = atribute.get('size', '-')
                simbol = "📁" if tip == 'dir' else "📄"
                print(f"    {simbol} {nume:30} {dimensiune:>10}")
        except error_perm:
            # Fallback la LIST
            fisiere = []
            ftp.dir(cale, fisiere.append)
            for linie in fisiere:
                print(f"    {linie}")
                
    except Exception as e:
        print(f"  Eroare listare: {e}")


def demonstratie_navigare(ftp: FTP):
    """Demonstrează navigarea în sistemul de fișiere."""
    print("\n" + "─" * 60)
    print("  DEMONSTRAȚIE NAVIGARE")
    print("─" * 60)
    
    director_initial = ftp.pwd()
    print(f"\n  Director inițial: {director_initial}")
    
    # Listare
    listeaza_fisiere(ftp)
    
    # Creare director nou
    try:
        nume_dir = "test_laborator"
        print(f"\n  Creare director '{nume_dir}'...")
        ftp.mkd(nume_dir)
        print("  ✓ Director creat")
        
        # Navigare în director
        print(f"  Navigare în '{nume_dir}'...")
        ftp.cwd(nume_dir)
        print(f"  Director curent: {ftp.pwd()}")
        
        # Revenire
        print("  Revenire la directorul părinte...")
        ftp.cwd("..")
        print(f"  Director curent: {ftp.pwd()}")
        
        # Ștergere director
        print(f"  Ștergere director '{nume_dir}'...")
        ftp.rmd(nume_dir)
        print("  ✓ Director șters")
        
    except error_perm as e:
        print(f"  ⚠ Operație nepermisă: {e}")
    except Exception as e:
        print(f"  Eroare: {e}")


def demonstratie_transfer(ftp: FTP):
    """Demonstrează transferul de fișiere."""
    print("\n" + "─" * 60)
    print("  DEMONSTRAȚIE TRANSFER FIȘIERE")
    print("─" * 60)
    
    nume_fisier = "test_upload.txt"
    continut = "Conținut de test pentru laboratorul de rețele.\nLinia 2.\nLinia 3.\n"
    
    try:
        # UPLOAD (STOR)
        print(f"\n  [UPLOAD] Încărcare fișier '{nume_fisier}'...")
        
        # Creăm fișierul în memorie
        buffer = BytesIO(continut.encode('utf-8'))
        
        # Transfer binar
        raspuns = ftp.storbinary(f"STOR {nume_fisier}", buffer)
        print(f"  ✓ {raspuns}")
        
        # Verificare existență
        print("\n  Verificare fișier încărcat:")
        listeaza_fisiere(ftp)
        
        # DOWNLOAD (RETR)
        print(f"\n  [DOWNLOAD] Descărcare fișier '{nume_fisier}'...")
        
        buffer_descarcare = BytesIO()
        raspuns = ftp.retrbinary(f"RETR {nume_fisier}", buffer_descarcare.write)
        print(f"  ✓ {raspuns}")
        
        # Afișare conținut descărcat
        continut_descarcat = buffer_descarcare.getvalue().decode('utf-8')
        print("\n  Conținut descărcat:")
        for linie in continut_descarcat.split('\n'):
            print(f"    {linie}")
        
        # Verificare dimensiune
        dimensiune = ftp.size(nume_fisier)
        print(f"\n  Dimensiune pe server: {dimensiune} bytes")
        
        # DELETE
        print(f"\n  [DELETE] Ștergere fișier '{nume_fisier}'...")
        ftp.delete(nume_fisier)
        print("  ✓ Fișier șters")
        
    except error_perm as e:
        print(f"  ⚠ Operație nepermisă: {e}")
    except Exception as e:
        print(f"  Eroare transfer: {e}")


def demonstratie_moduri_transfer(ftp: FTP):
    """Demonstrează diferența între modul ASCII și BINARY."""
    print("\n" + "─" * 60)
    print("  MODURI DE TRANSFER")
    print("─" * 60)
    
    print("\n  Modul ASCII (TYPE A):")
    print("    - Pentru fișiere text")
    print("    - Convertește caracterele de sfârșit de linie")
    print("    - \\r\\n (Windows) <-> \\n (Unix)")
    
    ftp.sendcmd("TYPE A")
    print("    ✓ Mod ASCII activat")
    
    print("\n  Modul BINARY (TYPE I):")
    print("    - Pentru fișiere binare (imagini, arhive)")
    print("    - Transfer exact, fără conversii")
    
    ftp.sendcmd("TYPE I")
    print("    ✓ Mod binar activat")


def demonstratie_comenzi_raw(ftp: FTP):
    """Demonstrează comenzi FTP brute."""
    print("\n" + "─" * 60)
    print("  COMENZI FTP BRUTE")
    print("─" * 60)
    
    comenzi = [
        ("NOOP", "Verificare conexiune activă"),
        ("PWD", "Afișare director curent"),
        ("SYST", "Tipul sistemului"),
        ("STAT", "Starea serverului"),
    ]
    
    for comanda, descriere in comenzi:
        print(f"\n  {comanda} - {descriere}:")
        try:
            raspuns = ftp.sendcmd(comanda)
            print(f"    {raspuns}")
        except error_perm as e:
            print(f"    ⚠ {e}")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Demonstrație Client FTP"
    )
    parser.add_argument(
        "--gazda", "-H",
        default=CONFIG_IMPLICIT["gazda"],
        help=f"Adresa serverului FTP (implicit: {CONFIG_IMPLICIT['gazda']})"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=CONFIG_IMPLICIT["port"],
        help=f"Portul FTP (implicit: {CONFIG_IMPLICIT['port']})"
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
        "--activ",
        action="store_true",
        help="Folosește modul activ în loc de pasiv"
    )
    parser.add_argument(
        "--simplu",
        action="store_true",
        help="Rulează doar demonstrația simplificată"
    )
    args = parser.parse_args()
    
    afiseaza_banner()
    
    ftp = None
    
    try:
        # Conectare
        ftp = conecteaza_ftp(
            gazda=args.gazda,
            port=args.port,
            utilizator=args.utilizator,
            parola=args.parola,
            mod_pasiv=not args.activ
        )
        
        # Informații server
        afiseaza_informatii_server(ftp)
        
        if not args.simplu:
            # Demonstrații complete
            demonstratie_navigare(ftp)
            demonstratie_transfer(ftp)
            demonstratie_moduri_transfer(ftp)
            demonstratie_comenzi_raw(ftp)
        else:
            # Doar listare
            listeaza_fisiere(ftp)
        
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
        if ftp:
            try:
                ftp.quit()
                print("\n  Conexiune închisă (QUIT).")
            except Exception:
                ftp.close()
                print("\n  Conexiune închisă forțat.")


if __name__ == "__main__":
    sys.exit(main())
