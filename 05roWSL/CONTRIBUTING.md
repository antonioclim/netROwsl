# Ghid de Contribuție

Mulțumim pentru interesul de a contribui la materialele de laborator!

---

## Raportarea Problemelor

Dacă găsești o eroare sau ai o sugestie:

1. Verifică dacă problema nu a fost deja raportată
2. Deschide un Issue cu:
   - Descrierea clară a problemei
   - Pașii pentru reproducere
   - Output-ul așteptat vs. cel real
   - Versiunea Python și sistemul de operare
   - Mesajele de eroare complete (dacă există)

---

## Propunerea de Modificări

### Pregătire

```bash
# Clonează repository-ul
git clone https://github.com/antonioclim/netROwsl.git
cd netROwsl/05roWSL

# Creează un branch pentru modificări
git checkout -b feature/descriere-scurta
```

### Stil Cod Python

```python
#!/usr/bin/env python3
"""
Descriere Modul
Laborator Rețele de Calculatoare – ASE | realizat de Revolvix

Descriere extinsă a modulului.
"""

from typing import List, Dict, Optional


def functie_noua(parametru: str, optional: int = 10) -> bool:
    """
    Descriere scurtă pe o singură linie.
    
    Descriere extinsă dacă e necesar, explicând contextul,
    algoritmul sau detalii importante.
    
    Args:
        parametru: Ce reprezintă parametrul
        optional: Parametru opțional cu valoare implicită
    
    Returns:
        Ce returnează funcția și în ce condiții
    
    Raises:
        ValueError: Când parametrul este invalid
    
    Example:
        >>> functie_noua("test", 5)
        True
    """
    # Implementare
    ...
```

**Reguli generale:**
- Funcții în română cu alias-uri în engleză
- Type hints pentru toate funcțiile publice
- Docstrings în format Google/NumPy
- Maxim 100 caractere pe linie
- 4 spații pentru indentare (nu tab-uri)

### Stil Documentație Markdown

- Headings cu `##` pentru secțiuni principale
- Cod în blocuri ``` cu limbajul specificat
- Tabele pentru date structurate
- Emoji-uri doar pe headings de nivel 2 (maxim 30% din headings)
- Link-uri relative pentru navigare între documente

### Structura Commit-urilor

```
tip(scop): descriere scurtă

Descriere detaliată dacă e necesar.
Explică DE CE, nu doar CE.

Closes #123
```

**Tipuri:**
- `feat` — funcționalitate nouă
- `fix` — corectare bug
- `docs` — doar documentație
- `test` — adăugare/modificare teste
- `refactor` — restructurare cod fără schimbare funcționalitate
- `style` — formatare, fără schimbare logică
- `chore` — task-uri de mentenanță

**Exemple:**
```
feat(vlsm): adaugă mod interactiv cu predicții

Implementează flag-ul --invata care permite studenților
să facă predicții înainte de a vedea rezultatul.

Closes #42
```

```
fix(ipv6): corectează validarea adreselor cu :: dublu

Adresele cu două secvențe :: erau acceptate greșit.
Acum se aruncă ValueError cu mesaj descriptiv.
```

---

## Testare

Înainte de a trimite modificări:

```bash
# Rulează toate testele
python -m pytest tests/ -v

# Rulează teste specifice
python -m pytest tests/test_exercitii.py -v

# Verifică coverage
python -m pytest tests/ --cov=src --cov-report=html

# Verifică stilul (dacă ai flake8 instalat)
python -m flake8 src/ scripts/ --max-line-length=100
```

**Cerințe minime:**
- Toate testele existente trec
- Funcționalități noi au teste
- Coverage nu scade sub 80%

---

## Structura Proiectului

```
05roWSL/
├── src/                    # Cod sursă principal
│   ├── utils/              # Biblioteci reutilizabile
│   ├── exercises/          # Exerciții CLI
│   └── apps/               # Aplicații standalone
├── scripts/                # Scripturi automatizare
├── tests/                  # Teste automatizate
├── docs/                   # Documentație
├── homework/               # Teme
└── docker/                 # Configurație containere
```

**Unde să adaugi:**
- Funcții de rețea → `src/utils/net_utils.py`
- Constante → `src/utils/constante.py`
- Exerciții noi → `src/exercises/ex_5_XX_nume.py`
- Documentație → `docs/`
- Teste → `tests/test_*.py`

---

## Review Process

1. Creează Pull Request din branch-ul tău
2. Completează template-ul PR
3. Așteaptă review de la maintainer
4. Adresează feedback-ul primit
5. După aprobare, PR-ul va fi merge-uit

**Timp estimat review:** 2-5 zile lucrătoare

---

## Convenții de Denumire

| Element | Convenție | Exemplu |
|---------|-----------|---------|
| Fișiere Python | snake_case | `net_utils.py` |
| Funcții (RO) | snake_case | `analizeaza_interfata_ipv4` |
| Clase | PascalCase | `InfoRetea` |
| Constante | SCREAMING_SNAKE | `BITI_IPV4` |
| Variabile | snake_case | `numar_gazde` |

---

## Documentație pentru Funcții Noi

Fiecare funcție publică nouă trebuie documentată în:

1. **Docstring** — în codul sursă
2. **api_reference.md** — dacă e parte din API-ul public
3. **exemple_utilizare.md** — dacă are caz de utilizare comun

---

## Contact

- **Probleme tehnice:** Deschide un Issue pe GitHub
- **Întrebări generale:** antonio.clim@csie.ase.ro
- **Pull requests:** Via GitHub

---

## Licență

Contribuțiile tale vor fi sub aceeași licență ca proiectul principal.

---

*Laborator Rețele de Calculatoare – ASE București*
