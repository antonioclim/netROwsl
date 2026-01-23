# 🗳️ Întrebări Peer Instruction — Săptămâna 8
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


## Întrebarea 1: TCP Handshake

> 💭 **PREDICȚIE:** Câte pachete sunt necesare pentru a stabili o conexiune TCP?

### Scenariu
Clientul se conectează la server pe portul 80.

### Întrebare
Care este secvența corectă a flag-urilor TCP în handshake?

### Opțiuni
- **A)** SYN → ACK → SYN-ACK
- **B)** SYN → SYN-ACK → ACK
- **C)** ACK → SYN → SYN-ACK
- **D)** SYN-ACK → SYN → ACK

### Răspuns corect
**B** — Client trimite SYN, server răspunde SYN-ACK, client confirmă cu ACK.

---

## Întrebarea 2: HTTP Response Codes

### Scenariu
Serverul răspunde cu `HTTP/1.1 301 Moved Permanently`.

### Întrebare
Ce trebuie să facă clientul?

### Opțiuni
- **A)** Să afișeze eroare utilizatorului
- **B)** Să urmeze header-ul `Location` pentru noua adresă
- **C)** Să retrimită cererea identic
- **D)** Să închidă conexiunea imediat

### Răspuns corect
**B** — Codul 301 indică o redirecționare permanentă; clientul trebuie să acceseze noua adresă din `Location`.


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect (dacă >90% sau <30%, întrebarea e prea ușoară/grea)
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
- **Încurajează dezbaterea** — studenții învață explicând unul altuia
