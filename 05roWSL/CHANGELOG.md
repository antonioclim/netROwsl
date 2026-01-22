# Changelog

Toate modificările notabile sunt documentate în acest fișier.

Formatul se bazează pe [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/),
și proiectul aderă la [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-01-22

### Adăugat

**Exerciții Interactive**
- Exercițiul 5.01: Analiză CIDR și subnetare FLSM cu mod `--invata`
- Exercițiul 5.02: Alocare VLSM și operații IPv6 cu mod `--invata-vlsm`
- Exercițiul 5.03: Quiz interactiv de subnetare cu 3 nivele de dificultate

**Bibliotecă de Rețea**
- Modul `net_utils.py` cu funcții complete pentru calcule IPv4/IPv6
- Modul `constante.py` pentru centralizarea valorilor
- Funcții de validare cu mesaje descriptive de eroare
- Alias-uri în limba engleză pentru toate funcțiile

**Documentație**
- Referință API completă (`docs/api_reference.md`)
- Diagrame arhitectură cod (`docs/arhitectura.md`)
- 5 întrebări Peer Instruction pentru seminarii (`docs/peer_instruction.md`)
- Exerciții pair programming structurate (`docs/exercitii_perechi.md`)
- Exerciții trace non-coding (`docs/exercitii_trace.md`)
- Exemple de utilizare cu scenarii complete (`docs/exemple_utilizare.md`)

**Teme**
- Tema 1: Proiectare rețea corporativă cu VLSM (nivel APPLY)
- Tema 2: Plan de migrare la IPv6 (nivel ANALYZE)
- Tema 3: Design rețea pentru startup (nivel CREATE)

**Teste**
- Teste unitare pentru funcțiile de bază
- Teste pentru edge cases și cazuri limită
- Teste de performanță pentru volume mari
- Teste de integrare pentru workflow-uri complete
- Teste pentru modulele utilitare Docker

**Mediu Docker**
- Configurație Docker Compose cu 3 containere
- Rețea `week5_labnet` (10.5.0.0/24)
- Capabilități NET_ADMIN și NET_RAW pentru tcpdump
- Integrare cu Portainer pentru management vizual

### Modificat

- README.md rescris pentru claritate și navigare mai bună
- Rezumat teoretic actualizat cu analogie IPv6 concretă
- Ghid depanare extins cu mai multe scenarii
- Fișa de comenzi reorganizată pe categorii

### Remediat

- Mesaje quiz naturalizate (eliminare ton AI)
- Reducere densitate emoji la <30%
- Variație în lungimea listelor pentru naturalețe
- Eliminare formulări detectabile ca AI-generate

---

## [0.9.0] - 2025-01-15

### Adăugat
- Structura inițială a kit-ului de laborator
- Scripturi de automatizare (pornește/oprește laborator)
- Documentație troubleshooting de bază
- Exerciții în formă preliminară

### Cunoscute
- Mod interactiv neimplementat
- Lipsesc teste pentru edge cases
- Documentație API incompletă

---

## Convenții

Tipurile de modificări:
- **Adăugat** — funcționalități noi
- **Modificat** — schimbări în funcționalitatea existentă
- **Depreciat** — funcționalități care vor fi eliminate
- **Eliminat** — funcționalități eliminate
- **Remediat** — bug-uri corectate
- **Securitate** — vulnerabilități adresate

---

*Laborator Rețele de Calculatoare – ASE București*
