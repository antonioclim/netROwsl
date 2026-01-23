# 🗳️ Întrebări Peer Instruction — Săptămâna 7
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


## Întrebarea 1: Filtrare pachete

> 💭 **PREDICȚIE:** Filtrul `tcp.port == 80` va captura și pachete HTTPS?

### Scenariu
În Wireshark, aplici filtrul: `tcp.port == 80`

### Întrebare
Ce trafic vei vedea?

### Opțiuni
- **A)** Doar cereri HTTP GET
- **B)** Tot traficul TCP către/de la portul 80
- **C)** Doar pachete HTTP (fără handshake TCP)
- **D)** Tot traficul web (inclusiv HTTPS)

### Răspuns corect
**B** — Filtrul capturează TOATE pachetele TCP cu portul 80 (inclusiv SYN, ACK, FIN, nu doar HTTP).

### Misconceptie vizată
Studenții cred că filtrele de port sunt inteligente și știu ce protocol e.

---

## Întrebarea 2: Captură tcpdump

### Scenariu
```bash
sudo tcpdump -i eth0 -w captura.pcap port 53
```

### Întrebare
Ce trafic va fi salvat în `captura.pcap`?

### Opțiuni
- **A)** Doar cereri DNS (UDP)
- **B)** Tot traficul DNS (UDP și TCP)
- **C)** Tot traficul de pe interfața eth0
- **D)** Doar răspunsuri DNS

### Răspuns corect
**B** — DNS folosește atât UDP (cereri normale) cât și TCP (răspunsuri mari, zone transfers).


---

## Note pentru Instructor

- **Țintă vot inițial:** 30-70% corect (dacă >90% sau <30%, întrebarea e prea ușoară/grea)
- **Cronometrează strict** — folosește un timer vizibil
- **Nu dezvălui răspunsul** până la Pasul 5
- **Încurajează dezbaterea** — studenții învață explicând unul altuia
