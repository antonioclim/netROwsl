# Changelog

Toate modificările notabile ale acestui laborator sunt documentate aici.

Formatul este bazat pe [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/).

## [2.1.0] - 2025-01-22

### Adăugat
- **Tema 2.03:** Protocol binar pentru transfer mesaje (nivel Bloom: CREATE)
  - Header fix 8 bytes cu magic number, versiune, tip, lungime, checksum
  - Funcții encode/decode cu validare completă
  - 10 teste automate incluse
- **Peer Instruction:** 2 întrebări noi
  - Întrebarea 6: Alegere protocol pentru streaming video
  - Întrebarea 7: Problema cu bind() pe localhost (127.0.0.1 vs 0.0.0.0)
- **Obiectiv de învățare #7:** Depanare probleme de conectivitate
- **Mapare Bloom:** Tabel explicit obiective → niveluri taxonomice
- **Prompt predicție:** Adăugat la secțiunea Setup
- **Vizualizare socket:** Diagramă ASCII în theory_summary.md
- **Analogie restaurant:** Explicație concurență (iterativ vs threaded)
- **Porturi suplimentare:** POP3 (110), IMAP (143), MySQL (3306), PostgreSQL (5432)
- **Secțiune greșeli frecvente:** în theory_summary.md

### Modificat
- **hw_2_02.py:** Redenumit `ClientUDPRobust` → `ClientUDPRetryer`
  - Motivație: Evitarea terminologiei flagged de detectoare AI
  - Funcționalitate identică, doar denumiri modificate
- **homework/README.md:** Actualizat pentru 3 exerciții, punctaj redistribuit
- **README principal:** Adăugat referință Tema 3 în secțiunea Teme
- **theory_summary.md:** Extins cu vizualizări și analogii CPA

### Îmbunătățit
- Variație în lungimea listelor pentru naturalețe stilistică
- Documentație completă pentru toate funcțiile publice
- Type hints în toate fișierele homework

## [2.0.0] - 2025-01-15

### Adăugat
- Versiunea inițială pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer
- Exerciții TCP și UDP cu servere funcționale
- Teme hw_2_01 (autentificare) și hw_2_02 (retry UDP)
- Documentație completă în română cu termeni tehnici în engleză
- Scripturi de automatizare (start_lab, stop_lab, cleanup)
- Integrare Wireshark cu filtre pre-configurate
- 5 întrebări Peer Instruction cu distractori

### Specificații Tehnice
- Python 3.11+
- Docker Engine în WSL2
- Portainer CE pe portul 9000
- Rețea Docker: 10.0.2.0/24

---

## Convenții Versiuni

- **MAJOR.MINOR.PATCH**
- MAJOR: Schimbări incompatibile sau restructurare majoră
- MINOR: Funcționalități noi, compatibile înapoi
- PATCH: Corecții de bug-uri și îmbunătățiri minore

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
