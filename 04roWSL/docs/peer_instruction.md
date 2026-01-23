# 🗳️ Întrebări Peer Instruction — Săptămâna 4
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


## Întrebarea 1: Adresare MAC

> 💭 **PREDICȚIE:** Câți bytes are o adresă MAC?

### Scenariu
Trimiti un frame Ethernet de la PC-ul tău (MAC: AA:BB:CC:DD:EE:FF) către router.

### Întrebare
Ce adresă MAC destinație va fi în frame?

### Opțiuni
- **A)** MAC-ul serverului final
- **B)** MAC-ul routerului (gateway)
- **C)** FF:FF:FF:FF:FF:FF (broadcast)
- **D)** Propria adresă MAC

### Răspuns corect
**B** — La nivelul 2, frame-ul merge către next-hop (routerul), nu către destinația finală.

---

## Întrebarea 2: struct.pack în Python

### Scenariu
```python
data = struct.pack('>HI', 80, 12345)
```

### Întrebare
Câți bytes va avea `data`?

### Opțiuni
- **A)** 2 bytes
- **B)** 4 bytes
- **C)** 6 bytes
- **D)** 8 bytes

### Răspuns corect
**C** — H = unsigned short (2 bytes) + I = unsigned int (4 bytes) = 6 bytes total.


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
