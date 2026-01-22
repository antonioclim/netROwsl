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

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom |
|---------|-----------------|----------------|
| 7 min | ★★☆☆☆ | UNDERSTAND |

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

### Note Instructor

**Anticipare răspunsuri:**
- Dacă >50% aleg A: Studenții confundă containerele cu VM-uri. Desenează diagrama izolării.
- Dacă >40% aleg B: Consolidează diferența host_port vs container_port cu analogia "cutia poștală".
- Dacă >30% aleg D: Explică că IP-ul intern NU e rutabil din afara Docker.

**Demo live după explicație:**
```bash
# Arată că IP-ul intern nu răspunde din Windows
ping 10.5.0.20  # timeout

# Arată că localhost:8080 funcționează
curl -s http://localhost:8080 && echo "Merge!"
```

**Conexiune cu misconceptii comune:**
- Studenții confundă EXPOSE (documentație în Dockerfile) cu port publish (-p)
- Numele serviciului rezolvă DNS doar în rețele user-defined, nu din afara Docker

**Follow-up recomandat:** Întreabă "Dar din alt container pe aceeași rețea?"

---

## Întrebarea 2: Calcul Gazde CIDR

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom |
|---------|-----------------|----------------|
| 7 min | ★★☆☆☆ | APPLY |

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

### Note Instructor

**Anticipare răspunsuri:**
- Dacă >40% aleg A: Formula e cunoscută dar semnificația lui "-2" nu. Desenează linia de adrese.
- Dacă >30% aleg D: Confuzie fundamentală prefix/gazde — revino la definiții.

**Vizualizare recomandată:**
```
Adrese în /26:
[.0]────[.1]────[.2]────...────[.62]────[.63]
 ↑       ↑                       ↑        ↑
REȚEA  PRIMA                  ULTIMA   BROADCAST
       GAZDĂ                  GAZDĂ
```

**Întrebare follow-up:** "Dar pentru /30? De ce e special?"
- Răspuns: /30 are 2 gazde, ideal pentru legături point-to-point

**Eroare frecventă de evitat:** Studenții uită că /31 (RFC 3021) e excepție — are 2 gazde fără broadcast.

---

## Întrebarea 3: VLSM – Ordinea Alocării

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom |
|---------|-----------------|----------------|
| 7 min | ★★★☆☆ | ANALYZE |

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

### Note Instructor

**Anticipare răspunsuri:**
- Dacă >40% aleg D: Demonstrează cu exemplu concret ce se întâmplă când aloci mic-mare.
- Dacă >30% aleg B: Confuzie cu sortări din alte contexte (ex: algoritmi de căutare).

**Demo la tablă:**
```
Scenariul GREȘIT (crescător 5, 10, 25, 50):
[/29][/28][───/27───][────────────/26?────────────]
 ↑                                    ↑
.0-.7                              .32 - nealiniat!

Problema: /26 trebuie să înceapă la multiplu de 64, dar .32 nu e.

Scenariul CORECT (descrescător 50, 25, 10, 5):
[────────────/26────────────][───/27───][/28][/29]
.0                        .63 .64    .95 .96 .111 .112
```

**Întrebare follow-up:** "Ce faci dacă cerințele sunt egale?"
- Răspuns: Ordinea nu mai contează (FLSM = VLSM în acest caz)

---

## Întrebarea 4: Adresa de Broadcast

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom |
|---------|-----------------|----------------|
| 8 min | ★★★☆☆ | APPLY |

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

### Note Instructor

**Anticipare răspunsuri:**
- Dacă >50% aleg A: Mentalitate "/24 implicit" — subliniază că prefixul NU respectă granițele octeților.
- Dacă >30% aleg C: Studenții revin la clasele de adrese — reamintește că CIDR a înlocuit clasful.

**Metodă rapidă de calcul:**
```
Pentru /20:
- Salt = 2^(32-20) = 2^12 = 4096 adrese
- 4096 / 256 = 16 (încap 16 "clase C" în fiecare subrețea /20)
- 172.16.50.x este în subrețeaua care începe la 172.16.48.0
  (48 este cel mai mare multiplu de 16 ≤ 50)
- Broadcast = 172.16.48.0 + 4095 = 172.16.63.255
```

**Verificare cu script:**
```bash
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 172.16.50.100/20
```

---

## Întrebarea 5: IPv6 Comprimare

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom |
|---------|-----------------|----------------|
| 7 min | ★★☆☆☆ | APPLY |

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

### Note Instructor

**Anticipare răspunsuri:**
- Dacă >30% aleg C: Subliniază regula "O SINGURĂ ::" — arată de ce e ambiguu altfel.
- Dacă >40% aleg D: Studenții sunt prudenți — explică că D e corect dar nu optim.

**Demo la tablă pentru opțiunea C:**
```
2001:db8::42::1

Interpretare 1: 2001:db8:0:0:42:0:0:1
Interpretare 2: 2001:db8:0:42:0:0:0:1
Interpretare 3: 2001:db8:0:0:0:42:0:1
... AMBIGUU! De aceea e invalid.
```

**Verificare cu script:**
```bash
python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-comprimare \
    "2001:0db8:0000:0042:0000:0000:0000:0001"
```

---

## Întrebări Suplimentare (Nivel Avansat)

### Întrebarea 6: Eficiență VLSM

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom |
|---------|-----------------|----------------|
| 5 min | ★★★★☆ | EVALUATE |

**Scenariu:** Ai 200 de gazde de împărțit în 4 subrețele de 50 fiecare.

**Întrebare:** Care metodă irosește mai puține adrese?

| Opțiune | Metodă |
|---------|--------|
| A | FLSM cu /26 pentru toate |
| B | VLSM cu /26 pentru fiecare |
| C | Ambele la fel |
| D | Depinde de situație |

**Răspuns:** C — În acest caz specific, cerințele sunt egale, deci FLSM și VLSM dau același rezultat.

**Notă instructor:** Întrebare-capcană. Scopul e să verifice dacă studenții înțeleg CÂND VLSM aduce avantaj.

---

### Întrebarea 7: Mască Wildcard

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom |
|---------|-----------------|----------------|
| 5 min | ★★☆☆☆ | APPLY |

**Scenariu:** Ai masca de rețea `255.255.255.224`

**Întrebare:** Care este masca wildcard corespunzătoare?

| Opțiune | Răspuns |
|---------|---------|
| A | 0.0.0.32 |
| B | 0.0.0.31 |
| C | 0.0.0.224 |
| D | 255.255.255.31 |

**Răspuns:** B — `0.0.0.31` (255 - 224 = 31)

**Notă instructor:** Wildcard = NOT(Mască). Pe fiecare octet: 255 - valoare.

---

### Întrebarea 8: RFC 3021 — Rețele /31

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom |
|---------|-----------------|----------------|
| 5 min | ★★★☆☆ | UNDERSTAND |

**Întrebare:** Câte gazde utilizabile are o rețea /31?

| Opțiune | Răspuns |
|---------|---------|
| A | 0 (nu se poate folosi) |
| B | 1 |
| C | 2 |
| D | -1 (formulă dă negativ) |

**Răspuns:** C — RFC 3021 permite 2 gazde pentru legături point-to-point (fără adresă de rețea/broadcast dedicate).

**Notă instructor:** Excepție importantă de la formula standard. Folosit în backbone-uri pentru economie de adrese.

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

### Prag de Intervenție

| Procent Corect (după discuție) | Acțiune |
|--------------------------------|---------|
| >80% | Treci la următoarea întrebare |
| 60-80% | Explicație standard + 1 exemplu |
| 40-60% | Explicație detaliată + demo + exercițiu suplimentar |
| <40% | STOP — revino la teorie, folosește vizualizări |

---

## Navigare Rapidă

| ← Anterior | Document | Următor → |
|------------|----------|-----------|
| [Fișa de Comenzi](fisa_comenzi.md) | **Peer Instruction** | [Exerciții Perechi](exercitii_perechi.md) |

## Documente Înrudite

- [README Principal](../README.md) — Ghid laborator
- [Rezumat Teoretic](rezumat_teorie.md) — Concepte de bază
- [Exerciții Perechi](exercitii_perechi.md) — Pair programming
- [Exerciții Trace](exercitii_trace.md) — Non-coding

---

*Material Peer Instruction pentru Laborator Rețele de Calculatoare – ASE București*
