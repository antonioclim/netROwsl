# 🗳️ Întrebări Peer Instruction — Săptămâna 1
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


## Întrebarea 1: Latența rețelei

> 💭 **PREDICȚIE:** Ce valoare de latență consideri "bună" pentru o conexiune locală?

### Scenariu
Rulezi comanda `ping -c 4 localhost` și obții:
```
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.042 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.038 ms
```

### Întrebare
Ce reprezintă valoarea `time=0.042 ms`?

### Opțiuni
- **A)** Timpul total de transmisie a pachetului
- **B)** Round-Trip Time (dus-întors)
- **C)** Timpul de procesare doar la destinație
- **D)** Timpul de așteptare în coada routerului

### Răspuns corect
**B** — RTT (Round-Trip Time) include timpul de: trimitere + propagare + procesare + răspuns + propagare înapoi.

### Misconceptie vizată
Studenții confundă adesea RTT cu latența unidirecțională (care e ~RTT/2).

---

## Întrebarea 2: Starea conexiunilor

### Scenariu
Rulezi `ss -t` și vezi:
```
State      Recv-Q  Send-Q   Local Address:Port    Peer Address:Port
ESTAB      0       0        192.168.1.5:45678     93.184.216.34:80
```

### Întrebare
Ce înseamnă starea `ESTAB`?

### Opțiuni
- **A)** Conexiunea este în curs de stabilire
- **B)** Conexiunea este complet stabilită și activă
- **C)** Conexiunea se închide
- **D)** Conexiunea așteaptă date

### Răspuns corect
**B** — ESTABLISHED înseamnă că handshake-ul TCP s-a completat cu succes.


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect (dacă >90% sau <30%, întrebarea e prea ușoară/grea)
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
- **Încurajează dezbaterea** — studenții învață explicând unul altuia
