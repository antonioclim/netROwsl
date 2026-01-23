# 🗳️ Întrebări Peer Instruction — Săptămâna 2
## Rețele de Calculatoare — ASE, CSIE | by Revolvix

---

## Structura Peer Instruction (5 pași)

Fiecare întrebare trebuie parcursă în **5 pași obligatorii**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PAS 1 (1 min)  │  Citește întrebarea și gândește individual               │
├─────────────────────────────────────────────────────────────────────────────┤
│  PAS 2 (30 sec) │  Votează răspunsul tău (A/B/C/D) — fără discuții!        │
├─────────────────────────────────────────────────────────────────────────────┤
│  PAS 3 (2 min)  │  Discută cu colegul de lângă tine — convinge-l!          │
├─────────────────────────────────────────────────────────────────────────────┤
│  PAS 4 (30 sec) │  Re-votează — poți schimba răspunsul                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  PAS 5 (2 min)  │  Instructorul explică răspunsul corect                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---


## Întrebarea 1: Tipuri de socket

> 💭 **PREDICȚIE:** Pentru streaming video, ce tip de socket ai alege?

### Scenariu
Trebuie să implementezi o aplicație de chat în timp real.

### Întrebare
Ce tip de socket alegi?

### Opțiuni
- **A)** `SOCK_STREAM` pentru fiabilitate
- **B)** `SOCK_DGRAM` pentru viteză
- **C)** `SOCK_RAW` pentru control total
- **D)** Nu contează, ambele merg la fel

### Răspuns corect
**A** — Pentru chat, mesajele trebuie să ajungă în ordine și complet, deci TCP (`SOCK_STREAM`).

### Misconceptie vizată
"UDP e mai rapid deci mai bun" — ignoră că pierderea mesajelor în chat e inacceptabilă.

---

## Întrebarea 2: Ordinea operațiilor socket

### Scenariu
Scrii un server TCP simplu.

### Întrebare
Care este ordinea corectă a operațiilor pentru server?

### Opțiuni
- **A)** socket → connect → listen → accept
- **B)** socket → bind → listen → accept
- **C)** socket → listen → bind → accept
- **D)** socket → bind → accept → listen

### Răspuns corect
**B** — Serverul: `socket()` → `bind()` → `listen()` → `accept()`

### Misconceptie vizată
Confuzia între `connect()` (client) și `bind()` (server).


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect (dacă >90% sau <30%, întrebarea e prea ușoară/grea)
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
- **Încurajează dezbaterea** — studenții învață explicând unul altuia
