# 🗳️ Întrebări Peer Instruction — Săptămâna 9
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


## Întrebarea 1: TLS Handshake

> 💭 **PREDICȚIE:** Câte mesaje sunt schimbate într-un TLS 1.3 handshake complet?

### Scenariu
Te conectezi la https://example.com.

### Întrebare
Ce se negociază în TLS handshake?

### Opțiuni
- **A)** Doar versiunea TLS
- **B)** Cipher suite, certificate, și chei de sesiune
- **C)** Doar certificatul serverului
- **D)** Username și parolă

### Răspuns corect
**B** — Handshake-ul negociază algoritmii criptografici, verifică identitatea și stabilește cheile de sesiune.

---

## Întrebarea 2: Compresie date

### Întrebare
De ce HTTP/2 folosește compresie pentru headere (HPACK)?

### Opțiuni
- **A)** Pentru securitate
- **B)** Pentru a reduce overhead-ul headerelor repetitive
- **C)** Pentru compatibilitate cu HTTP/1.1
- **D)** Nu folosește compresie

### Răspuns corect
**B)** — Headerele HTTP sunt adesea repetitive; HPACK reduce semnificativ bandwidth-ul necesar.


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
