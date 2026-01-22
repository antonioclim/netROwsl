# Changelog

Toate modificările notabile ale acestui proiect sunt documentate aici.

Formatul urmează [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/),
și proiectul aderă la [Semantic Versioning](https://semver.org/lang/ro/).

## [2.1.0] - 2025-01-22

### Adăugat
- **Analogii CPA (Concret-Pictorial-Abstract)** în ghidul Python pentru toate conceptele majore
- **5 întrebări Peer Instruction** cu distractori bazați pe misconceptii comune
- **Prompt-uri de predicție** înainte de execuția codului pentru învățare activă
- **Secțiuni "De Ce Funcționează Așa?"** pentru înțelegere profundă
- **GLOSAR.md** cu termeni tehnici și explicații
- **CHANGELOG.md** (acest fișier)
- Error handling complet în toate exemplele Python
- Type hints 100% în exemplele Python
- Docstrings format Google în toate funcțiile
- Logging consistent în scripturi

### Modificat
- Restructurare `GHID_PYTHON_NETWORKING_RO.md` cu cadru pedagogic îmbunătățit
- Înlocuire termeni AI-sounding: "comprehensiv"→"complet", "robust"→"solid"
- Îmbunătățire `01_socket_tcp.py` cu error handling și documentație completă
- Îmbunătățire `02_bytes_vs_str.py` cu demonstrații de erori și quiz
- Îmbunătățire `03_struct_parsing.py` cu dataclass și validare input
- Actualizare `verify_lab_environment.sh` cu verificări extinse

### Remediat
- Lipsa context managers pentru operații I/O
- Comentarii insuficiente pentru începători
- Absența exemplelor de gestionare erori

## [2.0.0] - 2025-01-09

### Adăugat
- Prezentări HTML interactive pentru toate cele 14 săptămâni
- Script `verify_lab_environment.sh` v2.0 cu verificări extinse
- Ghid Python pentru Networking (auto-studiu opțional)
- Suport pentru Docker Compose v2
- Cheatsheet Python rapid

### Modificat
- Restructurare folder conform standardului netROwsl
- Actualizare versiuni: Portainer 2.33.6, Docker 28.x
- Îmbunătățire troubleshooting section în Prerequisites

### Remediat
- Compatibilitate WSL2 pe Windows 11 24H2
- Problema cu caractere unicode în căi Windows

## [1.0.0] - 2024-09-01

### Adăugat
- Versiunea inițială pentru semestrul 2024-2025
- Prerequisites de bază pentru configurare mediu
- Structură folder standard pentru 14 săptămâni
- Documentație inițială în română

---

## Tipuri de modificări

- **Adăugat** pentru funcționalități noi
- **Modificat** pentru schimbări în funcționalitatea existentă
- **Depreciat** pentru funcționalități ce vor fi eliminate în curând
- **Eliminat** pentru funcționalități eliminate
- **Remediat** pentru bug fixes
- **Securitate** pentru vulnerabilități

---

*Menținut de: ing. dr. Antonio Clim, ASE-CSIE București*
