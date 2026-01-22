# Întrebări Peer Instruction – Săptămâna 5

> Material pentru seminarii și discuții în grup
> Laborator Rețele de Calculatoare – ASE, Informatică Economică

---

## Cum să Folosești Aceste Întrebări

**Format Peer Instruction (recomandat):**

1. **Vot individual** (1 min) — Studenții votează fără discuție
2. **Discuție în perechi** (3 min) — Discută cu colegul de bancă
3. **Revot** (30 sec) — Votează din nou după discuție
4. **Explicație** (2 min) — Profesorul explică răspunsul corect

**Notă:** Distractorii sunt concepuți pe baza greșelilor comune ale studenților.

---

## Întrebarea 1: Port Mapping vs Adresă Container

### Scenariu

Un container Docker are IP-ul intern `10.5.0.20` și rulează un server web pe portul 80.  
În `docker-compose.yml` ai configurat:

```yaml
ports:
  - "8080:80"
```

### Întrebare

**Din Windows, ce URL folosești pentru a accesa serverul?**

| Opțiune | Răspuns |
|---------|---------|
| A | http://10.5.0.20:80 |
| B | http://localhost:80 |
| C | http://localhost:8080 |
| D | http://10.5.0.20:8080 |

### Răspuns Corect

**C** — `http://localhost:8080`

### Explicație Distractori

| Opțiune | Greșeală Comună |
|---------|-----------------|
| A | **IP intern Docker nu e accesibil direct din Windows.** Rețeaua Docker bridge e izolată. |
| B | **Confuzie între portul container și portul host.** Portul 80 e cel din container, nu cel expus. |
| D | **Combinație greșită.** IP-ul intern cu portul host nu funcționează. |

### Concepte Testate

- Izolarea rețelelor Docker
- Diferența între port mapping host:container
- Accesul din afara containerului

---

## Întrebarea 2: Calcul Gazde CIDR

### Scenariu

Ai rețeaua `192.168.10.0/26`

### Întrebare

**Câte gazde UTILIZABILE ai în această rețea?**

| Opțiune | Răspuns |
|---------|---------|
| A | 64 |
| B | 62 |
| C | 63 |
| D | 26 |

### Răspuns Corect

**B** — 62 gazde utilizabile

### Explicație Distractori

| Opțiune | Greșeală Comună |
|---------|-----------------|
| A | **Uită să scadă 2.** Calculează 2^6 = 64 dar nu scade adresa de rețea și broadcast. |
| C | **Scade doar 1.** Scade broadcast dar uită adresa de rețea (sau invers). |
| D | **Confundă prefixul cu numărul de gazde.** 26 e prefixul, nu numărul de gazde. |

### Formulă

```
Gazde utilizabile = 2^(32 - prefix) - 2
                  = 2^(32 - 26) - 2
                  = 2^6 - 2
                  = 64 - 2
                  = 62
```

---

## Întrebarea 3: VLSM – Ordinea Alocării

### Scenariu

Ai rețeaua de bază `10.0.0.0/24` și cerințele: 50, 10, 25, 5 gazde.

### Întrebare

**În ce ordine trebuie alocate subrețelele în VLSM?**

| Opțiune | Ordine |
|---------|--------|
| A | 50, 10, 25, 5 (ordinea originală) |
| B | 5, 10, 25, 50 (crescător) |
| C | 50, 25, 10, 5 (descrescător) |
| D | Nu contează ordinea |

### Răspuns Corect

**C** — 50, 25, 10, 5 (descrescător)

### Explicație Distractori

| Opțiune | Greșeală Comună |
|---------|-----------------|
| A | **Nu aplică sortarea.** VLSM necesită sortare pentru eficiență maximă. |
| B | **Sortare inversă.** Ar duce la fragmentare și spațiu irosit. |
| D | **Ignoră importanța ordinii.** Ordinea contează pentru a evita "găurile" în spațiul de adrese. |

### De Ce Descrescător?

- Subrețelele mari necesită aliniere la granițe mai mari
- Alocarea de la mare la mic evită fragmentarea
- Subrețelele mici se potrivesc în spațiile rămase

---

## Întrebarea 4: Adresa de Broadcast

### Scenariu

Ai interfața configurată cu `172.16.50.100/20`

### Întrebare

**Care este adresa de broadcast a acestei rețele?**

| Opțiune | Răspuns |
|---------|---------|
| A | 172.16.50.255 |
| B | 172.16.63.255 |
| C | 172.16.255.255 |
| D | 172.16.48.255 |

### Răspuns Corect

**B** — 172.16.63.255

### Explicație Distractori

| Opțiune | Greșeală Comună |
|---------|-----------------|
| A | **Presupune /24.** Pune .255 doar pe ultimul octet, ignorând prefixul /20. |
| C | **Presupune /16.** Pune .255.255, confundând cu clasa B implicită. |
| D | **Confundă adresa de rețea cu broadcast.** 172.16.48.0 e adresa de rețea, nu broadcast. |

### Calcul

```
/20 = primii 20 biți sunt rețea

172.16.50.100 în binar:
  172.16.  = 10101100.00010000
  50       = 00110010
  100      = 01100100

Mască /20: 11111111.11111111.11110000.00000000

Adresa de rețea: 172.16.48.0 (primii 20 biți)
Broadcast:       172.16.63.255 (ultimii 12 biți = 1)

48 + (2^12 - 1) = 48 + 4095 = ... ajungem la 63.255
```

---

## Întrebarea 5: IPv6 Comprimare

### Scenariu

Ai adresa IPv6: `2001:0db8:0000:0042:0000:0000:0000:0001`

### Întrebare

**Care este forma comprimată corectă?**

| Opțiune | Răspuns |
|---------|---------|
| A | 2001:db8:0:42::1 |
| B | 2001:db8::42:0:0:0:1 |
| C | 2001:db8::42::1 |
| D | 2001:db8:0:42:0:0:0:1 |

### Răspuns Corect

**A** — `2001:db8:0:42::1`

### Explicație Distractori

| Opțiune | Greșeală Comună |
|---------|-----------------|
| B | **Nu aplică :: în locul optim.** Pune :: după 42, dar lasă zerourile finale. |
| C | **Două :: în aceeași adresă.** INVALID — doar o secvență :: e permisă. |
| D | **Nu folosește :: deloc.** Corect semantic, dar nu e forma cea mai comprimată. |

### Reguli de Comprimare

1. Zerourile din față ale grupurilor se omit: `0db8` → `db8`
2. Cel mai lung șir de grupuri zero consecutive devine `::`
3. Doar O SINGURĂ secvență `::` e permisă (altfel ar fi ambiguu)

---

## Întrebări Suplimentare (Nivel Avansat)

### Întrebarea 6: Eficiență VLSM

**Scenariu:** Ai 200 de gazde de împărțit în 4 subrețele de 50 fiecare.

**Întrebare:** Care metodă irosește mai puține adrese?

| Opțiune | Metodă |
|---------|--------|
| A | FLSM cu /26 pentru toate |
| B | VLSM cu /26 pentru fiecare |
| C | Ambele la fel |
| D | Depinde de situație |

**Răspuns:** C — În acest caz specific, cerințele sunt egale, deci FLSM și VLSM dau același rezultat.

---

### Întrebarea 7: Mască Wildcard

**Scenariu:** Ai masca de rețea `255.255.255.224`

**Întrebare:** Care este masca wildcard corespunzătoare?

| Opțiune | Răspuns |
|---------|---------|
| A | 0.0.0.32 |
| B | 0.0.0.31 |
| C | 0.0.0.224 |
| D | 255.255.255.31 |

**Răspuns:** B — `0.0.0.31` (255 - 224 = 31)

---

### Întrebarea 8: RFC 3021 — Rețele /31

**Întrebare:** Câte gazde utilizabile are o rețea /31?

| Opțiune | Răspuns |
|---------|---------|
| A | 0 (nu se poate folosi) |
| B | 1 |
| C | 2 |
| D | -1 (formulă dă negativ) |

**Răspuns:** C — RFC 3021 permite 2 gazde pentru legături point-to-point (fără adresă de rețea/broadcast dedicate).

---

## Utilizare în Seminar

### Timing Recomandat

| Fază | Durată | Activitate |
|------|--------|------------|
| Prezentare întrebare | 30 sec | Citește și afișează |
| Vot individual | 1 min | Studenții votează în tăcere |
| Discuție perechi | 3 min | Discuție și argumentare |
| Revot | 30 sec | Votează din nou |
| Explicație | 2-3 min | Răspuns corect + distractori |
| **Total per întrebare** | **~7 min** | |

### Sfaturi pentru Facilitator

- Nu dezvălui răspunsul înainte de revot
- Încurajează studenții să-și explice raționamentul colegului
- Folosește distractorii pentru a aborda misconceptiile
- Dacă >70% răspund corect din prima, treci rapid la explicație
- Dacă <40% răspund corect după discuție, dedică mai mult timp explicației

---

## Documente Înrudite

- [README Principal](../README.md) — Ghid laborator
- [Rezumat Teoretic](rezumat_teorie.md) — Concepte de bază
- [Exerciții Perechi](exercitii_perechi.md) — Pair programming
- [Exerciții Trace](exercitii_trace.md) — Non-coding

---

*Material Peer Instruction pentru Laborator Rețele de Calculatoare – ASE București*
