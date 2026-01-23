# 🐍 Python pentru Rețele de Calculatoare

Material complementar pentru cursul de Rețele de Calculatoare.

## Structură

```
PYTHON ghid de auto-perfectionare/
├── GHID_PYTHON_NETWORKING_RO.md    # Ghidul principal (citește asta!)
├── cheatsheets/
│   └── PYTHON_RAPID.md             # Referință rapidă
├── examples/
│   ├── 01_socket_tcp.py            # Server/Client TCP
│   ├── 02_bytes_vs_str.py          # Bytes vs Strings
│   ├── 03_struct_parsing.py        # Parsing binar
│   └── tests/
│       └── test_smoke.py           # Teste automate
├── images/                          # Screenshots (Portainer, Wireshark)
└── PRESENTATIONS_RO/
    ├── 01_introducere_setup.html   # Slide-uri interactive
    └── ...
```

## Cum să Folosești

1. **Citește ghidul** — `GHID_PYTHON_NETWORKING_RO.md`
2. **Rulează exemplele** — în folderul `examples/`
3. **Parcurge prezentările** — deschide fișierele HTML în browser
4. **Testează înțelegerea** — rezolvă întrebările Peer Instruction
5. **Creează** — încearcă exercițiile CREATE pentru proiectare independentă

## Cerințe

- Python 3.11+
- WSL2 cu Ubuntu 22.04 (recomandat)
- Docker (pentru exercițiile avansate)

## Rulare Teste

```bash
cd examples/tests
python test_smoke.py
```

## Ce E Nou în Versiunea 3.0

- **10 întrebări Peer Instruction** — cu distractori bazați pe misconceptii reale
- **3 exerciții CREATE** — proiectare protocol, port scanner, load balancer
- **8 diagrame ASCII** — TCP handshake, Docker port mapping, socket lifecycle
- **FAQ extins** — 12 întrebări frecvente
- **Exercițiu pair programming** — Debug Mystery Server
- **Subgoal labels** — etichetare pași în cod și documentație
- **Smoke tests** — verificare automată a exemplelor

## Note

- Acest material este **opțional**
- Nu afectează nota la laborator
- Scopul e înțelegerea conceptelor Python din spatele exercițiilor

## Contribuții

Raportează probleme sau sugerează îmbunătățiri pe GitHub Issues.

---

*Versiune: 3.0 — Ianuarie 2025*  
*Cu îmbunătățiri pedagogice CPA, Peer Instruction și CREATE*
