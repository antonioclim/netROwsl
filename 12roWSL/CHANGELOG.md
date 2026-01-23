# Changelog - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Toate modificările notabile ale materialelor pentru Săptămâna 12 sunt documentate în acest fișier.

Formatul este bazat pe [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.2.0] - 2026-01-XX

### Adăugat

#### Pedagogic
- **Întrebări Peer Instruction** - 10 întrebări MCQ cu analiza distractorilor (docs/peer_instruction.md)
- **Prompt-uri de predicție** - 12+ predicții în toate exercițiile din README.md
- **Subgoal labels** - Separatoare vizuale în toate scripturile Python principale
- **Analogii CPA** - Tabel complet Concret-Pictorial-Abstract în docs/rezumat_teorie.md
- **Instrucțiuni Pair Programming** - Ghid complet cu bonus în homework/README.md
- **Scaffolding exerciții** - Pași detaliați cu predicții în src/exercises/ex_01_smtp.py

#### Documentație
- **Glosar de termeni** - Definiții complete pentru SMTP, RPC, gRPC (docs/glosar.md)
- **Secțiune FAQ** - Întrebări frecvente în README.md
- **Diagrame ASCII** - Flux SMTP și comparație payload RPC în README.md
- **CHANGELOG.md** - Acest fișier

#### Cod
- **Benchmark complet gRPC** - Adăugat suport gRPC în benchmark_rpc.py
- **Teste unitare pytest** - Suite de teste în tests/test_unitare.py
- **Type hints** - Adnotări de tip în funcțiile principale

### Îmbunătățit

#### README.md
- Restructurare secțiuni pentru claritate
- Reducere formulări AI-sounding ("explorează", "fundamentale", "dobândi experiență")
- Adăugare variație stilistică naturală (propoziții scurte, întrebări retorice)
- Verificare predicții după fiecare exercițiu

#### Scripturi Python
- scripts/porneste_lab.py - Subgoal labels, documentație îmbunătățită
- scripts/opreste_lab.py - Subgoal labels, verificări adiționale
- scripts/curata.py - Subgoal labels, protecție Portainer
- src/apps/rpc/jsonrpc/jsonrpc_server.py - Subgoal labels, statistici îmbunătățite
- src/apps/rpc/benchmark_rpc.py - Suport complet JSON-RPC + XML-RPC + gRPC

#### Documentație
- docs/rezumat_teorie.md - Analogii CPA, structură îmbunătățită
- homework/README.md - Instrucțiuni pair programming, checklist predare

### Remediat
- Benchmark-ul includea doar 2 din 3 protocoale RPC (lipsea gRPC)
- Lipsă întrebări de verificare a înțelegerii
- Absența scaffolding-ului pentru exerciții

---

## [1.1.0] - 2025-12-XX

### Adăugat
- Suport gRPC cu Protocol Buffers
- Capturi de trafic Wireshark pre-configurate
- Script de verificare mediu

---

## [1.0.0] - 2025-11-XX

### Adăugat
- Server SMTP educațional
- Server JSON-RPC 2.0
- Server XML-RPC cu introspecție
- Scripturi de automatizare (porneste_lab, opreste_lab, curata)
- Documentație de bază

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
