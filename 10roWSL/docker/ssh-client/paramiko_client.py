#!/usr/bin/env python3
"""
Client SSH cu Paramiko pentru Container
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Demonstrează conexiunea SSH programatică către serverul de laborator.
"""

import paramiko
import time
import sys

# Configurație conexiune
GAZDA = "ssh-server"
PORT = 22
UTILIZATOR = "labuser"
PAROLA = "labpass"

# Comenzi de demonstrație
COMENZI_DEMO = [
    "echo '=== Demonstrație SSH cu Paramiko ==='",
    "echo 'Salut de pe serverul SSH!'",
    "whoami",
    "hostname",
    "pwd",
    "ls -la",
    "cat bun_venit.txt",
    "date",
    "uptime",
]


def main():
    """Funcția principală - execută demonstrația SSH."""
    print()
    print("=" * 60)
    print("  CLIENT SSH PARAMIKO - DEMONSTRAȚIE")
    print("  Laborator Rețele de Calculatoare")
    print("=" * 60)
    print()
    print(f"  Conectare la {UTILIZATOR}@{GAZDA}:{PORT}...")
    print()
    
    # Creează clientul SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Așteaptă serverul să fie disponibil
        for incercare in range(10):
            try:
                client.connect(
                    hostname=GAZDA,
                    port=PORT,
                    username=UTILIZATOR,
                    password=PAROLA,
                    timeout=5
                )
                break
            except Exception:
                print(f"  Așteptare server... ({incercare + 1}/10)")
                time.sleep(2)
        else:
            print("  ✗ Serverul SSH nu este disponibil")
            return 1
        
        print("  ✓ Conectat cu succes!")
        print()
        
        # Afișează informații despre conexiune
        transport = client.get_transport()
        if transport:
            print("  Informații conexiune:")
            print(f"    Cipher: {transport.remote_cipher}")
            print(f"    MAC: {transport.remote_mac}")
            print()
        
        # Execută comenzile demo
        print("─" * 60)
        print("  EXECUȚIE COMENZI:")
        print("─" * 60)
        
        for comanda in COMENZI_DEMO:
            print(f"\n  $ {comanda}")
            print("  " + "-" * 40)
            
            stdin, stdout, stderr = client.exec_command(comanda)
            
            iesire = stdout.read().decode('utf-8')
            erori = stderr.read().decode('utf-8')
            
            if iesire:
                for linie in iesire.strip().split('\n'):
                    print(f"    {linie}")
            
            if erori:
                print(f"  [EROARE] {erori.strip()}")
        
        print()
        print("─" * 60)
        print("  ✓ Demonstrație finalizată cu succes!")
        print("=" * 60)
        
        return 0
        
    except paramiko.AuthenticationException:
        print("  ✗ Eroare de autentificare")
        return 1
    
    except Exception as e:
        print(f"  ✗ Eroare: {e}")
        return 1
    
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
