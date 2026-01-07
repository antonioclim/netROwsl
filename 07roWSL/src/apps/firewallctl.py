#!/usr/bin/env python3
"""
Controller Firewall (iptables)
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Instrument pentru gestionarea regulilor iptables bazat pe profile JSON.
Permite aplicarea, listarea și resetarea regulilor de filtrare.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}", flush=True)


class ControllerFirewall:
    """Gestionează regulile iptables bazate pe profile."""
    
    def __init__(self, cale_profile: Path):
        """
        Inițializează controller-ul.
        
        Args:
            cale_profile: Calea către fișierul JSON cu profile
        """
        self.cale_profile = cale_profile
        self.profile: dict = {}
        self._incarca_profile()
    
    def _incarca_profile(self):
        """Încarcă profilele din fișierul JSON."""
        if not self.cale_profile.exists():
            logheaza(f"AVERTISMENT: Fișierul de profile nu există: {self.cale_profile}")
            return
        
        try:
            with open(self.cale_profile, 'r', encoding='utf-8') as f:
                self.profile = json.load(f)
            logheaza(f"Profile încărcate din {self.cale_profile}")
        except Exception as e:
            logheaza(f"Eroare la încărcarea profilelor: {e}")
    
    def _ruleaza_iptables(self, argumente: list[str]) -> tuple[bool, str]:
        """
        Rulează o comandă iptables.
        
        Args:
            argumente: Lista de argumente pentru iptables
        
        Returns:
            Tuplu (succes, mesaj)
        """
        comanda = ["iptables"] + argumente
        
        try:
            rezultat = subprocess.run(
                comanda,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if rezultat.returncode == 0:
                return True, rezultat.stdout
            else:
                return False, rezultat.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Timeout la execuția comenzii"
        except PermissionError:
            return False, "Permisiuni insuficiente. Rulați ca root/administrator."
        except FileNotFoundError:
            return False, "iptables nu este instalat sau disponibil"
        except Exception as e:
            return False, str(e)
    
    def listeaza_profile(self):
        """Listează toate profilele disponibile."""
        lista_profile = self.profile.get("profiles", [])
        
        if not lista_profile:
            logheaza("Niciun profil disponibil")
            return
        
        logheaza("Profile disponibile:")
        logheaza("-" * 50)
        
        for profil in lista_profile:
            nume = profil.get("name", "fără nume")
            descriere = profil.get("description", "Fără descriere")
            nr_reguli = len(profil.get("rules", []))
            
            print(f"  {nume}")
            print(f"    Descriere: {descriere}")
            print(f"    Reguli: {nr_reguli}")
            print()
    
    def obtine_profil(self, nume: str) -> dict | None:
        """
        Obține un profil după nume.
        
        Args:
            nume: Numele profilului
        
        Returns:
            Dicționarul profilului sau None
        """
        for profil in self.profile.get("profiles", []):
            if profil.get("name") == nume:
                return profil
        return None
    
    def aplica_profil(self, nume: str, dry_run: bool = False) -> bool:
        """
        Aplică un profil de firewall.
        
        Args:
            nume: Numele profilului de aplicat
            dry_run: Doar afișează comenzile fără a le executa
        
        Returns:
            True dacă profilul a fost aplicat cu succes
        """
        profil = self.obtine_profil(nume)
        
        if not profil:
            logheaza(f"Profilul '{nume}' nu a fost găsit")
            return False
        
        logheaza(f"Aplicare profil: {nume}")
        logheaza(f"Descriere: {profil.get('description', 'N/A')}")
        
        # Resetare reguli existente
        if not dry_run:
            logheaza("Resetare reguli existente...")
            self.reseteaza_reguli()
        else:
            logheaza("[SIMULARE] S-ar reseta regulile existente")
        
        # Aplicare reguli noi
        reguli = profil.get("rules", [])
        
        if not reguli:
            logheaza("Profil fără reguli - toate conexiunile sunt permise")
            return True
        
        for i, regula in enumerate(reguli, 1):
            protocol = regula.get("protocol", "tcp")
            port = regula.get("port")
            actiune = regula.get("action", "DROP")
            comentariu = regula.get("comment", "")
            
            # Construire comandă iptables
            args_iptables = [
                "-A", "INPUT",
                "-p", protocol,
                "--dport", str(port),
                "-j", actiune
            ]
            
            # Adăugare opțiuni specifice pentru REJECT
            if actiune == "REJECT":
                reject_with = regula.get("reject_with", "icmp-port-unreachable")
                args_iptables.extend(["--reject-with", reject_with])
            
            if dry_run:
                logheaza(f"[SIMULARE] Regulă {i}: iptables {' '.join(args_iptables)}")
                if comentariu:
                    logheaza(f"           Comentariu: {comentariu}")
            else:
                ok, mesaj = self._ruleaza_iptables(args_iptables)
                if ok:
                    logheaza(f"Regulă {i} aplicată: {protocol.upper()} {port} -> {actiune}")
                else:
                    logheaza(f"Eroare la aplicarea regulii {i}: {mesaj}")
                    return False
        
        logheaza(f"Profil '{nume}' aplicat cu succes ({len(reguli)} reguli)")
        return True
    
    def reseteaza_reguli(self) -> bool:
        """
        Resetează toate regulile iptables la starea implicită.
        
        Returns:
            True dacă resetarea a reușit
        """
        comenzi = [
            ["-F"],           # Flush toate regulile
            ["-X"],           # Șterge lanțurile personalizate
            ["-P", "INPUT", "ACCEPT"],    # Politică implicită ACCEPT
            ["-P", "OUTPUT", "ACCEPT"],
            ["-P", "FORWARD", "ACCEPT"],
        ]
        
        for args in comenzi:
            ok, mesaj = self._ruleaza_iptables(args)
            if not ok:
                logheaza(f"Eroare la resetare: {mesaj}")
                return False
        
        logheaza("Reguli resetate la starea implicită")
        return True
    
    def afiseaza_reguli_curente(self):
        """Afișează regulile iptables curente."""
        logheaza("Reguli iptables curente:")
        logheaza("-" * 50)
        
        ok, iesire = self._ruleaza_iptables(["-L", "-n", "-v"])
        
        if ok:
            print(iesire)
        else:
            logheaza(f"Eroare la listarea regulilor: {iesire}")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Controller firewall bazat pe profile pentru Săptămâna 7"
    )
    parser.add_argument(
        "--profile", "-p",
        type=Path,
        default=Path("docker/configs/firewall_profiles.json"),
        help="Calea către fișierul de profile"
    )
    
    subparsers = parser.add_subparsers(dest="comanda", help="Comenzi disponibile")
    
    # Comandă: listeaza
    subparsers.add_parser("listeaza", help="Listează profilele disponibile")
    
    # Comandă: aplica
    parser_aplica = subparsers.add_parser("aplica", help="Aplică un profil")
    parser_aplica.add_argument("nume", help="Numele profilului de aplicat")
    parser_aplica.add_argument(
        "--simulare",
        action="store_true",
        help="Doar afișează comenzile fără a le executa"
    )
    
    # Comandă: reseteaza
    subparsers.add_parser("reseteaza", help="Resetează regulile la starea implicită")
    
    # Comandă: arata
    subparsers.add_parser("arata", help="Afișează regulile curente")
    
    args = parser.parse_args()

    controller = ControllerFirewall(args.profile)

    if args.comanda == "listeaza":
        controller.listeaza_profile()
    elif args.comanda == "aplica":
        controller.aplica_profil(args.nume, dry_run=args.simulare)
    elif args.comanda == "reseteaza":
        controller.reseteaza_reguli()
    elif args.comanda == "arata":
        controller.afiseaza_reguli_curente()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
