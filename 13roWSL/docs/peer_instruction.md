# 🗳️ Întrebări Peer Instruction — Săptămâna 13
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


## Întrebarea 1: MQTT QoS

> 💭 **PREDICȚIE:** Ce înseamnă QoS 2 în MQTT?

### Scenariu
Un senzor IoT publică temperatura la fiecare 5 secunde.

### Întrebare
Ce QoS level alegi dacă pierderile ocazionale sunt acceptabile?

### Opțiuni
- **A)** QoS 0 (at most once)
- **B)** QoS 1 (at least once)
- **C)** QoS 2 (exactly once)
- **D)** Nu contează

### Răspuns corect
**A** — Pentru telemetrie frecventă, QoS 0 e suficient și mai eficient.

---

## Întrebarea 2: Vulnerabilități IoT

### Întrebare
Care e cea mai comună vulnerabilitate în dispozitivele IoT?

### Opțiuni
- **A)** SQL Injection
- **B)** Credențiale default neschimbate
- **C)** Buffer overflow
- **D)** XSS

### Răspuns corect
**B** — Majoritatea dispozitivelor IoT sunt compromise prin credențiale default (admin/admin).


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
