# 🗳️ Întrebări Peer Instruction — Săptămâna 3
## Rețele de Calculatoare — ASE, CSIE | by Revolvix

---

## Structura Peer Instruction (5 pași)

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


## Întrebarea 1: Paradigme de Programare în Rețea

> 💭 **PREDICȚIE:** Ce paradigmă folosești când browserul descarcă o pagină web?

### Scenariu
Trebuie să implementezi un server de fișiere.

### Întrebare
Ce model de server alegi pentru a gestiona 1000 de clienți simultan?

### Opțiuni
- **A)** Un thread per client
- **B)** Un proces per client  
- **C)** Select/Poll cu un singur thread
- **D)** Nu contează, toate sunt la fel

### Răspuns corect
**C** — Pentru 1000+ clienți, select/poll/epoll sunt mai eficiente decât thread/proces per client (overhead mai mic).

---

## Întrebarea 2: Blocking vs Non-blocking

### Întrebare
Ce se întâmplă când apelezi `recv()` pe un socket blocking și nu sunt date?

### Opțiuni
- **A)** Returnează imediat cu 0 bytes
- **B)** Aruncă o excepție
- **C)** Blochează până când vin date
- **D)** Returnează -1

### Răspuns corect
**C** — Socket-urile blocking opresc execuția până când operația poate fi completată.


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
