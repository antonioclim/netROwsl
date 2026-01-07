#!/usr/bin/env python3
"""
Exercițiul 5.03 – Generator Quiz Interactiv de Subnetare
========================================================
Quiz interactiv pentru testarea cunoștințelor de adresare IP și subnetare.

Utilizare:
    python ex_5_03_generator_quiz.py                    Quiz complet
    python ex_5_03_generator_quiz.py --intrebari 5      5 întrebări
    python ex_5_03_generator_quiz.py --dificultate greu Quiz dificil

Autor: Material didactic ASE-CSIE
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
import ipaddress

# Import utilitar local
RADACINA = Path(__file__).resolve().parents[2]
if str(RADACINA) not in sys.path:
    sys.path.insert(0, str(RADACINA))


# Coduri culori ANSI
class Culori:
    ALBASTRU = '\033[94m'
    CYAN = '\033[96m'
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    BOLD = '\033[1m'
    SFARSIT = '\033[0m'


def coloreaza(text: str, culoare: str) -> str:
    """Aplică culoare dacă stdout este un terminal."""
    if sys.stdout.isatty():
        return f"{culoare}{text}{Culori.SFARSIT}"
    return text


@dataclass
class Intrebare:
    """Reprezintă o întrebare de quiz."""
    text: str
    raspuns_corect: str
    explicatie: str
    dificultate: str


class GeneratorQuiz:
    """Generator de întrebări pentru quiz de subnetare."""
    
    DIFICULTATI = {
        'usor': {'prefixe': [24, 25, 26], 'retele_private': True},
        'mediu': {'prefixe': [20, 21, 22, 23, 24, 25, 26, 27], 'retele_private': True},
        'greu': {'prefixe': list(range(16, 31)), 'retele_private': False},
    }
    
    def __init__(self, dificultate: str = 'mediu'):
        self.dificultate = dificultate
        self.config = self.DIFICULTATI.get(dificultate, self.DIFICULTATI['mediu'])
    
    def _genereaza_ip_aleatoriu(self) -> str:
        """Generează o adresă IP aleatorie."""
        if self.config['retele_private']:
            # Folosește rețele private
            retele = [
                (10, range(0, 256), range(0, 256)),
                (172, range(16, 32), range(0, 256)),
                (192, [168], range(0, 256)),
            ]
            retea = random.choice(retele)
            return f"{retea[0]}.{random.choice(retea[1])}.{random.choice(retea[2])}.{random.randint(1, 254)}"
        else:
            return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    
    def _genereaza_cidr_aleatoriu(self) -> Tuple[str, ipaddress.IPv4Network]:
        """Generează o notație CIDR aleatorie."""
        ip = self._genereaza_ip_aleatoriu()
        prefix = random.choice(self.config['prefixe'])
        cidr = f"{ip}/{prefix}"
        retea = ipaddress.ip_network(cidr, strict=False)
        return cidr, retea
    
    def intrebare_adresa_retea(self) -> Intrebare:
        """Generează o întrebare despre adresa de rețea."""
        cidr, retea = self._genereaza_cidr_aleatoriu()
        
        return Intrebare(
            text=f"Care este adresa de rețea pentru {cidr}?",
            raspuns_corect=str(retea.network_address),
            explicatie=f"Pentru /{retea.prefixlen}, masca este {retea.netmask}. "
                       f"Aplicând operația AND între IP și mască obținem adresa de rețea.",
            dificultate=self.dificultate
        )
    
    def intrebare_broadcast(self) -> Intrebare:
        """Generează o întrebare despre adresa de broadcast."""
        cidr, retea = self._genereaza_cidr_aleatoriu()
        
        return Intrebare(
            text=f"Care este adresa de broadcast pentru {cidr}?",
            raspuns_corect=str(retea.broadcast_address),
            explicatie=f"Adresa de broadcast are toți biții de gazdă setați pe 1. "
                       f"Pentru /{retea.prefixlen}, avem {32-retea.prefixlen} biți de gazdă.",
            dificultate=self.dificultate
        )
    
    def intrebare_numar_gazde(self) -> Intrebare:
        """Generează o întrebare despre numărul de gazde utilizabile."""
        cidr, retea = self._genereaza_cidr_aleatoriu()
        gazde = max(0, retea.num_addresses - 2)
        
        return Intrebare(
            text=f"Câte gazde utilizabile sunt în rețeaua {cidr}?",
            raspuns_corect=str(gazde),
            explicatie=f"Formula: 2^(32-prefix) - 2 = 2^{32-retea.prefixlen} - 2 = {gazde}. "
                       f"Scădem 2 pentru adresa de rețea și broadcast.",
            dificultate=self.dificultate
        )
    
    def intrebare_prima_gazda(self) -> Intrebare:
        """Generează o întrebare despre prima gazdă utilizabilă."""
        cidr, retea = self._genereaza_cidr_aleatoriu()
        gazde = list(retea.hosts())
        prima = str(gazde[0]) if gazde else "N/A"
        
        return Intrebare(
            text=f"Care este prima gazdă utilizabilă în {cidr}?",
            raspuns_corect=prima,
            explicatie=f"Prima gazdă = adresa de rețea + 1 = {retea.network_address} + 1 = {prima}",
            dificultate=self.dificultate
        )
    
    def intrebare_ultima_gazda(self) -> Intrebare:
        """Generează o întrebare despre ultima gazdă utilizabilă."""
        cidr, retea = self._genereaza_cidr_aleatoriu()
        gazde = list(retea.hosts())
        ultima = str(gazde[-1]) if gazde else "N/A"
        
        return Intrebare(
            text=f"Care este ultima gazdă utilizabilă în {cidr}?",
            raspuns_corect=ultima,
            explicatie=f"Ultima gazdă = adresa de broadcast - 1 = {retea.broadcast_address} - 1 = {ultima}",
            dificultate=self.dificultate
        )
    
    def intrebare_masca(self) -> Intrebare:
        """Generează o întrebare despre conversia prefix-mască."""
        prefix = random.choice(self.config['prefixe'])
        retea = ipaddress.ip_network(f"10.0.0.0/{prefix}", strict=False)
        
        return Intrebare(
            text=f"Care este masca de rețea pentru prefixul /{prefix}?",
            raspuns_corect=str(retea.netmask),
            explicatie=f"/{prefix} înseamnă {prefix} biți de 1 urmați de {32-prefix} biți de 0 în mască.",
            dificultate=self.dificultate
        )
    
    def intrebare_prefix_pentru_gazde(self) -> Intrebare:
        """Generează o întrebare despre prefixul necesar."""
        import math
        gazde_necesare = random.choice([10, 25, 50, 100, 200, 500, 1000])
        
        # Calculează prefixul minim
        biti_gazda = math.ceil(math.log2(gazde_necesare + 2))
        prefix = 32 - biti_gazda
        gazde_disponibile = (2 ** biti_gazda) - 2
        
        return Intrebare(
            text=f"Care este cel mai lung prefix care poate acomoda {gazde_necesare} gazde?",
            raspuns_corect=f"/{prefix}",
            explicatie=f"Avem nevoie de cel puțin {gazde_necesare}+2={gazde_necesare+2} adrese. "
                       f"2^{biti_gazda}={2**biti_gazda} ≥ {gazde_necesare+2}, deci /{prefix} cu {gazde_disponibile} gazde.",
            dificultate=self.dificultate
        )
    
    def genereaza_intrebari(self, numar: int = 10) -> List[Intrebare]:
        """Generează o listă de întrebări aleatorii."""
        generatoare = [
            self.intrebare_adresa_retea,
            self.intrebare_broadcast,
            self.intrebare_numar_gazde,
            self.intrebare_prima_gazda,
            self.intrebare_ultima_gazda,
            self.intrebare_masca,
            self.intrebare_prefix_pentru_gazde,
        ]
        
        intrebari = []
        for _ in range(numar):
            generator = random.choice(generatoare)
            intrebari.append(generator())
        
        return intrebari


def ruleaza_quiz(intrebari: List[Intrebare]) -> Tuple[int, int]:
    """
    Rulează quiz-ul interactiv.
    
    Returns:
        Tuple (răspunsuri corecte, total întrebări)
    """
    corecte = 0
    total = len(intrebari)
    
    print()
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print(coloreaza("  Quiz Interactiv de Subnetare", Culori.BOLD))
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print()
    print(f"  Total întrebări: {total}")
    print(f"  Tastați răspunsul și apăsați Enter.")
    print(f"  Tastați 'renunt' pentru a ieși.")
    print()
    
    for i, intrebare in enumerate(intrebari, 1):
        print(coloreaza(f"─── Întrebarea {i}/{total} ", Culori.CYAN) + "─" * 40)
        print()
        print(f"  {intrebare.text}")
        print()
        
        try:
            raspuns = input(coloreaza("  Răspunsul dumneavoastră: ", Culori.GALBEN)).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nQuiz întrerupt.")
            break
        
        if raspuns.lower() == 'renunt':
            print("\nQuiz abandonat.")
            break
        
        # Verifică răspunsul (normalizare)
        raspuns_normalizat = raspuns.replace(" ", "").lower()
        corect_normalizat = intrebare.raspuns_corect.replace(" ", "").lower()
        
        if raspuns_normalizat == corect_normalizat:
            corecte += 1
            print(coloreaza("  ✓ Corect!", Culori.VERDE))
        else:
            print(coloreaza(f"  ✗ Incorect. Răspunsul corect: {intrebare.raspuns_corect}", Culori.ROSU))
        
        print(coloreaza(f"  ℹ {intrebare.explicatie}", Culori.CYAN))
        print()
    
    return corecte, total


def afiseaza_rezultat(corecte: int, total: int):
    """Afișează rezultatul final al quiz-ului."""
    if total == 0:
        return
    
    procent = (corecte / total) * 100
    
    print()
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print(coloreaza("  Rezultat Final", Culori.BOLD))
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print()
    print(f"  Răspunsuri corecte: {corecte} din {total}")
    print(f"  Scor: {procent:.1f}%")
    print()
    
    if procent >= 90:
        print(coloreaza("  🎉 Excelent! Stăpânești perfect subnetarea!", Culori.VERDE))
    elif procent >= 70:
        print(coloreaza("  👍 Foarte bine! Mai exersează puțin.", Culori.VERDE))
    elif procent >= 50:
        print(coloreaza("  📚 Satisfăcător. Revizuiește teoria.", Culori.GALBEN))
    else:
        print(coloreaza("  📖 Necesită mai multă practică. Recitește materialul.", Culori.ROSU))
    
    print()


def main(argv: Optional[List[str]] = None) -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Quiz Interactiv de Subnetare",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  %(prog)s                         Quiz implicit (10 întrebări, mediu)
  %(prog)s --intrebari 5           5 întrebări
  %(prog)s --dificultate greu      Quiz dificil
  %(prog)s -n 20 -d usor           20 întrebări ușoare
"""
    )
    
    parser.add_argument(
        "--intrebari", "-n",
        type=int,
        default=10,
        help="Numărul de întrebări (implicit: 10)"
    )
    parser.add_argument(
        "--dificultate", "-d",
        choices=['usor', 'mediu', 'greu'],
        default='mediu',
        help="Nivelul de dificultate (implicit: mediu)"
    )
    
    args = parser.parse_args(argv)
    
    generator = GeneratorQuiz(args.dificultate)
    intrebari = generator.genereaza_intrebari(args.intrebari)
    
    corecte, total = ruleaza_quiz(intrebari)
    afiseaza_rezultat(corecte, total)
    
    return 0 if corecte == total else 1


if __name__ == "__main__":
    sys.exit(main())
