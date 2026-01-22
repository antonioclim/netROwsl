# Changelog

Toate modificările notabile sunt documentate aici.

Format bazat pe [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/).

---

## [1.1.0] - 2025-01

### Adăugat

**Documentație Pedagogică**
- `docs/peer_instruction.md` — 5 întrebări Peer Instruction pentru instructor cu ghid de utilizare
- `docs/architecture.md` — Diagrame ASCII detaliate pentru arhitectură și protocoale
- `docs/debugging_guide.md` — Ghid pas-cu-pas pentru debugging probleme comune
- `docs/faq.md` — Întrebări frecvente cu răspunsuri detaliate

**Exerciții Noi**
- `src/exercises/ex5_pair_debugging.py` — Exercițiu pair programming cu 7 bug-uri intenționate
- `src/exercises/ex6_wireshark_trace.md` — Exercițiu non-cod pentru analiză Wireshark

**Teste Automatizate**
- `tests/test_protocol_utils.py` — Teste unitare pytest pentru utilitare protocol

### Modificat

**Îmbunătățiri Pedagogice**
- README.md: Adăugare prompturi de predicție înainte de comenzi
- README.md: Restructurare liste pentru variație (eliminare pattern 3/5 elemente)
- README.md: Reducere utilizare emoji (doar pentru avertismente critice)
- README.md: Adăugare exemple de output pentru comenzi principale
- README.md: Adăugare linkuri către documentația nouă

- docs/theory_summary.md: Adăugare secțiune "Analogii pentru Înțelegere" (CPA)
- docs/theory_summary.md: Restructurare liste în proză pentru variație
- docs/theory_summary.md: Linkuri către alte documente

- docs/troubleshooting.md: Eliminare formulări pasive
- docs/troubleshooting.md: Linkuri către FAQ și debugging guide

**Îmbunătățiri Cod**
- homework/exercises/tema_4_01.py: Adăugare prompturi de predicție la TODO-uri
- homework/exercises/tema_4_02.py: Adăugare prompturi de predicție la TODO-uri

### Eliminat
- Emoji-uri decorative din headings (păstrate doar ⚠️ pentru avertismente)
- Formatare bold excesivă
- Structuri de liste perfect paralele (înlocuite cu variație)

---

## [1.0.0] - 2025-01

### Adăugat

**Protocoale**
- Protocol TEXT pe port TCP 5400
  - Comenzi: PING, SET, GET, DEL, COUNT, KEYS, QUIT
  - Format: `<lungime> <comandă> [argumente]`
- Protocol BINAR pe port TCP 5401
  - Antet fix 14 bytes cu CRC32
  - Tipuri: PING, PONG, SET, GET, DELETE, RESPONSE, ERROR
- Protocol Senzor UDP pe port 5402
  - Datagrame fixe 23 bytes
  - Câmpuri: versiune, sensor_id, temperatură, locație, CRC32

**Infrastructură Docker**
- `docker/docker-compose.yml` cu 3 servicii
- Health checks pentru toate containerele
- Rețea izolată `retea_saptamana4`
- Compatibilitate cu Portainer CE

**Documentație**
- `README.md` cu instrucțiuni complete
- `docs/theory_summary.md` cu fundamente teoretice
- `docs/commands_cheatsheet.md` pentru referință rapidă
- `docs/troubleshooting.md` pentru depanare
- `docs/further_reading.md` cu resurse suplimentare

**Exerciții**
- `src/exercises/ex1_text_client.py` — Client protocol TEXT
- `src/exercises/ex2_binary_client.py` — Client protocol BINAR
- `src/exercises/ex3_udp_sensor.py` — Client senzor UDP
- `src/exercises/ex4_crc_detection.py` — Detectare erori CRC32

**Teme**
- `homework/exercises/tema_4_01.py` — Client BINAR key-value store
- `homework/exercises/tema_4_02.py` — Simulator rețea senzori

**Scripturi**
- `scripts/start_lab.py` — Pornire automată mediu laborator
- `scripts/stop_lab.py` — Oprire curată mediu laborator
- `scripts/utils/docker_utils.py` — Utilitare Docker

**Teste**
- `tests/test_protocols.py` — Teste de integrare protocoale

### Compatibilitate
- Windows 11 + WSL2 + Ubuntu 22.04
- Docker Engine 24.x+
- Python 3.10+
- Portainer CE 2.x

---

## Template Versiuni Viitoare

### [X.Y.Z] - YYYY-MM-DD

#### Adăugat
- Funcționalități noi

#### Modificat
- Modificări la funcționalități existente

#### Deprecat
- Funcționalități care vor fi eliminate

#### Eliminat
- Funcționalități eliminate

#### Corectat
- Bug-uri rezolvate

#### Securitate
- Vulnerabilități adresate

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
