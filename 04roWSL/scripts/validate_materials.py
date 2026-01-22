#!/usr/bin/env python3
"""
Script de Validare Materiale Laborator
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Verifică automat:
- Absența cuvintelor AI-sounding
- Proporția emoji-urilor în headings
- Prezența blocurilor de predicție
- Prezența subgoal labels în cod
- Acoperirea docstrings
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE
# ═══════════════════════════════════════════════════════════════════════════════

AI_SIGNAL_WORDS = [
    # Markeri AI în engleză
    "delve", "comprehensive", "robust", "seamless", "leverage",
    "facilitate", "harness", "multifaceted", "pivotal", "paramount",
    "utilize", "foster", "cultivate", "bolster", "underscore",
    "landscape", "ecosystem", "paradigm", "realm", "tapestry",
    "holistic", "synergy", "empower", "streamline", "cutting-edge",
    
    # Echivalenți români AI
    "comprehensiv", "a valorifica", "în profunzime", "peisajul",
    "ecosistemul", "paradigma", "esențial de menționat",
    "crucial să", "fundamental important",
]

AI_PHRASES = [
    "este esențial de menționat",
    "în această secțiune vom",
    "să explorăm",
    "containerizare fericită",
    "joacă un rol crucial",
    "în lumea modernă",
    "pe scară largă",
]

EMOJI_PATTERN = r'[\U0001F300-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0]'

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII VALIDARE
# ═══════════════════════════════════════════════════════════════════════════════

def gaseste_ai_words(cale: Path) -> List[Tuple[str, int, str]]:
    """
    Caută cuvinte AI într-un fișier.
    
    Returns:
        Lista de tuple (cuvânt, linie, context)
    """
    gasiri = []
    try:
        continut = cale.read_text(encoding='utf-8')
        linii = continut.split('\n')
        
        for nr_linie, linie in enumerate(linii, 1):
            linie_lower = linie.lower()
            for cuvant in AI_SIGNAL_WORDS:
                if cuvant.lower() in linie_lower:
                    gasiri.append((cuvant, nr_linie, linie.strip()[:80]))
            for fraza in AI_PHRASES:
                if fraza.lower() in linie_lower:
                    gasiri.append((fraza, nr_linie, linie.strip()[:80]))
    except Exception as e:
        print(f"  Eroare la citirea {cale}: {e}")
    
    return gasiri


def numara_emoji_headings(cale: Path) -> Tuple[int, int, float]:
    """
    Numără headings și cele cu emoji.
    
    Returns:
        (total_headings, cu_emoji, procent)
    """
    try:
        continut = cale.read_text(encoding='utf-8')
        headings = re.findall(r'^#+\s+.+$', continut, re.MULTILINE)
        cu_emoji = [h for h in headings if re.search(EMOJI_PATTERN, h)]
        
        total = len(headings)
        emoji_count = len(cu_emoji)
        procent = (emoji_count / total * 100) if total > 0 else 0
        
        return total, emoji_count, procent
    except Exception:
        return 0, 0, 0


def numara_predictii(cale: Path) -> int:
    """Numără blocurile de predicție într-un fișier."""
    try:
        continut = cale.read_text(encoding='utf-8')
        # Caută variante de "PREDICȚIE" sau "Predicție"
        return len(re.findall(r'PREDICȚIE|Predicție', continut, re.IGNORECASE))
    except Exception:
        return 0


def numara_subgoal_labels(cale: Path) -> int:
    """Numără subgoal labels într-un fișier Python."""
    try:
        continut = cale.read_text(encoding='utf-8')
        # Pattern: linie de ═ cu text în mijloc
        return len(re.findall(r'# ═+\n# [A-Z_]+\n', continut))
    except Exception:
        return 0


def verifica_docstrings(cale: Path) -> Tuple[int, int, float]:
    """
    Verifică acoperirea docstrings.
    
    Returns:
        (functii, cu_docstring, procent)
    """
    try:
        continut = cale.read_text(encoding='utf-8')
        
        # Numără funcții și clase
        definitii = re.findall(r'^(?:def|class)\s+\w+', continut, re.MULTILINE)
        total_def = len(definitii)
        
        # Numără docstrings ("""...""" sau '''...''')
        docstrings = len(re.findall(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', continut))
        
        # Aproximare: fiecare funcție/clasă ar trebui să aibă un docstring
        procent = (docstrings / total_def * 100) if total_def > 0 else 100
        
        return total_def, docstrings, min(procent, 100)
    except Exception:
        return 0, 0, 0


def verifica_type_hints(cale: Path) -> Tuple[int, int, float]:
    """
    Verifică prezența type hints.
    
    Returns:
        (functii, cu_hints, procent)
    """
    try:
        continut = cale.read_text(encoding='utf-8')
        
        # Funcții cu return type hint
        cu_hints = len(re.findall(r'def\s+\w+\([^)]*\)\s*->', continut))
        
        # Total funcții
        total = len(re.findall(r'^def\s+\w+', continut, re.MULTILINE))
        
        procent = (cu_hints / total * 100) if total > 0 else 100
        
        return total, cu_hints, procent
    except Exception:
        return 0, 0, 0


# ═══════════════════════════════════════════════════════════════════════════════
# RAPORTARE
# ═══════════════════════════════════════════════════════════════════════════════

def print_section(titlu: str) -> None:
    """Afișează un titlu de secțiune."""
    print(f"\n{'═' * 60}")
    print(f" {titlu}")
    print('═' * 60)


def main() -> int:
    """
    Rulează toate validările.
    
    Returns:
        0 dacă totul e OK, 1 dacă sunt probleme
    """
    root = Path('.')
    probleme = 0
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║        VALIDARE MATERIALE LABORATOR - SĂPTĂMÂNA 4         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 1. Verificare AI Words
    # ═══════════════════════════════════════════════════════════════════════
    print_section("1. VERIFICARE CUVINTE AI")
    
    fisiere_md = list(root.glob('**/*.md'))
    fisiere_md = [f for f in fisiere_md if '.git' not in str(f)]
    
    gasiri_totale = 0
    for f in fisiere_md:
        gasiri = gaseste_ai_words(f)
        if gasiri:
            gasiri_totale += len(gasiri)
            print(f"\n⚠️  {f}:")
            for cuvant, linie, context in gasiri[:3]:  # Max 3 exemple
                print(f"     L{linie}: \"{cuvant}\" în: {context}...")
    
    if gasiri_totale == 0:
        print("✓ Niciun cuvânt AI detectat!")
    else:
        print(f"\n❌ Total: {gasiri_totale} apariții în fișiere .md")
        probleme += 1
    
    # ═══════════════════════════════════════════════════════════════════════
    # 2. Verificare Emoji în Headings
    # ═══════════════════════════════════════════════════════════════════════
    print_section("2. VERIFICARE EMOJI ÎN HEADINGS")
    
    for f in sorted(fisiere_md):
        if f.name in ['README.md'] or 'docs' in str(f):
            total, cu_emoji, procent = numara_emoji_headings(f)
            if total > 0:
                status = "✓" if procent <= 30 else "⚠️"
                if procent > 30:
                    probleme += 1
                print(f"{status} {f.name}: {cu_emoji}/{total} headings cu emoji ({procent:.0f}%)")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 3. Verificare Predicții în Exerciții
    # ═══════════════════════════════════════════════════════════════════════
    print_section("3. VERIFICARE PREDICȚII ÎN EXERCIȚII")
    
    exercitii = list(root.glob('src/exercises/*.py')) + list(root.glob('homework/exercises/*.py'))
    
    for f in sorted(exercitii):
        count = numara_predictii(f)
        status = "✓" if count >= 2 else "⚠️"
        if count < 2:
            probleme += 1
        print(f"{status} {f.name}: {count} blocuri PREDICȚIE (min recomandat: 2)")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 4. Verificare Subgoal Labels în Apps
    # ═══════════════════════════════════════════════════════════════════════
    print_section("4. VERIFICARE SUBGOAL LABELS")
    
    apps = list(root.glob('src/apps/*.py'))
    apps = [f for f in apps if f.name != '__init__.py']
    
    for f in sorted(apps):
        count = numara_subgoal_labels(f)
        status = "✓" if count >= 3 else "⚠️"
        if count < 3:
            probleme += 1
        print(f"{status} {f.name}: {count} subgoal labels (min recomandat: 3)")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 5. Verificare Docstrings
    # ═══════════════════════════════════════════════════════════════════════
    print_section("5. VERIFICARE DOCSTRINGS")
    
    fisiere_py = list(root.glob('src/**/*.py')) + list(root.glob('scripts/*.py'))
    fisiere_py = [f for f in fisiere_py if f.name != '__init__.py']
    
    total_functii = 0
    total_docs = 0
    
    for f in fisiere_py[:10]:  # Primele 10
        functii, docs, procent = verifica_docstrings(f)
        total_functii += functii
        total_docs += docs
    
    procent_global = (total_docs / total_functii * 100) if total_functii > 0 else 100
    status = "✓" if procent_global >= 80 else "⚠️"
    print(f"{status} Acoperire docstrings: {procent_global:.0f}% (țintă: 80%)")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 6. Verificare Type Hints
    # ═══════════════════════════════════════════════════════════════════════
    print_section("6. VERIFICARE TYPE HINTS")
    
    total_f = 0
    total_h = 0
    
    for f in fisiere_py[:10]:
        functii, hints, procent = verifica_type_hints(f)
        total_f += functii
        total_h += hints
    
    procent_hints = (total_h / total_f * 100) if total_f > 0 else 100
    status = "✓" if procent_hints >= 70 else "⚠️"
    print(f"{status} Acoperire type hints: {procent_hints:.0f}% (țintă: 70%)")
    
    # ═══════════════════════════════════════════════════════════════════════
    # SUMAR
    # ═══════════════════════════════════════════════════════════════════════
    print_section("SUMAR")
    
    if probleme == 0:
        print("✓ Toate verificările au trecut!")
        print("\nMaterialele sunt pregătite pentru utilizare.")
        return 0
    else:
        print(f"⚠️  {probleme} verificări au avertismente.")
        print("\nRevizuiți avertismentele înainte de utilizare.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
