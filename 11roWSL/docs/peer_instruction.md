# 🗳️ Întrebări Peer Instruction — Săptămâna 11
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


## Întrebarea 1: Load Balancing Round-Robin

> 💭 **PREDICȚIE:** Cu 3 servere și 10 cereri, câte cereri primește fiecare server?

### Scenariu
```nginx
upstream backend {
    server app1:8001;
    server app2:8002;
    server app3:8003;
}
```

### Întrebare
Cu algoritmul round-robin, dacă app2 devine indisponibil, ce se întâmplă cu cererile sale?

### Opțiuni
- **A)** Se pierd
- **B)** Se redistribuie automat la app1 și app3
- **C)** Toate cererile merg la app1
- **D)** Load balancer-ul se oprește

### Răspuns corect
**B** — Nginx detectează serverul indisponibil și redistribuie traficul la serverele active.

---

## Întrebarea 2: Sticky Sessions

### Scenariu
Un utilizator se autentifică pe app1, apoi face altă cerere.

### Întrebare
Fără sticky sessions, ce problemă poate apărea?

### Opțiuni
- **A)** Sesiunea se pierde dacă cererea merge la app2
- **B)** Performanța scade
- **C)** Nu există nicio problemă
- **D)** Conexiunea TCP se închide

### Răspuns corect
**A** — Fără sticky sessions sau session store partajat, utilizatorul ar trebui să se re-autentifice.


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect (dacă >90% sau <30%, întrebarea e prea ușoară/grea)
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
- **Încurajează dezbaterea** — studenții învață explicând unul altuia
