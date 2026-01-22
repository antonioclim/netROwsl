# Întrebări Peer Instruction - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Cum să Folosești Aceste Întrebări

**Metodologia Peer Instruction (Eric Mazur, Harvard):**

1. **Prezentare** (1 min): Citește întrebarea și opțiunile
2. **Vot individual** (1 min): Fiecare student votează fără discuții
3. **Discuție în perechi** (3 min): Studenții cu răspunsuri diferite își explică raționamentul
4. **Revot** (30 sec): Votează din nou după discuție
5. **Explicație** (2 min): Profesorul explică răspunsul corect

**Notă:** Întrebările sunt concepute să aibă un "distractor plauzibil" - o opțiune greșită care pare corectă la prima vedere.

---

## 🗳️ Întrebarea 1: Port Mapping Docker

**Scenariu:**
Ai configurat un container cu următoarea mapare de porturi:
```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

**Întrebare:** Din browser-ul Windows, ce URL folosești pentru a accesa nginx?

| Opțiune | Răspuns |
|---------|---------|
| A) `http://localhost:80` | |
| B) `http://localhost:8080` | |
| C) `http://172.20.1.2:80` | |
| D) `http://nginx:80` | |

<details>
<summary><b>Click pentru răspuns și explicație</b></summary>

**Răspuns corect: B) `http://localhost:8080`**

**Explicații pentru fiecare opțiune:**

- **A) `http://localhost:80`** ❌ — Portul 80 este portul INTERN al containerului. Din Windows nu poți accesa direct portul intern.

- **B) `http://localhost:8080`** ✅ — CORECT! Formatul `-p HOST:CONTAINER` înseamnă că portul 8080 de pe mașina gazdă (Windows) este redirecționat către portul 80 din container.

- **C) `http://172.20.1.2:80`** ❌ — Aceasta este adresa IP internă Docker. Din Windows NU poți accesa direct rețeaua Docker (doar din alte containere sau din WSL).

- **D) `http://nginx:80`** ❌ — Numele serviciului (`nginx`) funcționează doar pentru rezoluția DNS ÎNTRE containere pe aceeași rețea Docker. Din Windows, numele nu este rezolvabil.

**Concluzie:** Maparea porturilor creează o "punte" între lumea Windows și lumea Docker.

</details>

---

## 🗳️ Întrebarea 2: TCP vs UDP - Număr de Pachete

**Scenariu:** 
Trimiți exact 5 mesaje identice ("Hello") folosind:
- Varianta A: Socket TCP
- Varianta B: Socket UDP

Capturezi traficul cu Wireshark în ambele cazuri.

**Întrebare:** De ce captura TCP arată mai multe pachete decât captura UDP pentru aceleași 5 mesaje?

| Opțiune | Răspuns |
|---------|---------|
| A) TCP comprimă datele, necesitând pachete suplimentare pentru metadate de decompresie | |
| B) TCP are handshake (SYN, SYN-ACK, ACK) și trimite confirmări (ACK) pentru fiecare segment | |
| C) UDP pierde pachete pe drum, deci par mai puține | |
| D) Pachetele TCP sunt mai mici, deci trebuie mai multe pentru aceleași date | |

<details>
<summary><b>Click pentru răspuns și explicație</b></summary>

**Răspuns corect: B)**

**Explicații:**

- **A)** ❌ — TCP NU comprimă datele. Compresia (dacă există) se face la nivelul aplicației, nu al transportului.

- **B)** ✅ — CORECT! TCP necesită:
  - 3 pachete pentru handshake inițial (SYN → SYN-ACK → ACK)
  - 1 ACK pentru fiecare segment primit (sau ACK cumulativ)
  - 4 pachete pentru închiderea conexiunii (FIN → ACK → FIN → ACK)
  
  Pentru 5 mesaje: ~3 (handshake) + 5 (date) + 5 (ACK-uri) + 4 (închidere) = ~17 pachete

- **C)** ❌ — UDP nu "pierde" pachete în mod sistematic. Dacă pierde, nu e din cauza protocolului, ci a rețelei. În plus, Wireshark capturează ce pleacă, nu ce ajunge.

- **D)** ❌ — Headerul TCP (20+ bytes) este mai MARE decât headerul UDP (8 bytes). Deci pachetele TCP sunt mai mari, nu mai mici.

**Numărătoare tipică:**
- UDP: 5 pachete (unul per mesaj)
- TCP: 15-20 pachete (handshake + date + ACK-uri + închidere)

</details>

---

## 🗳️ Întrebarea 3: Stări Socket TCP

**Scenariu:**
Un server TCP acceptă o conexiune. Clientul trimite date, serverul răspunde, apoi clientul apelează `close()`.

**Întrebare:** În ce stare se află socket-ul CLIENTULUI imediat după ce apelează `close()`?

| Opțiune | Răspuns |
|---------|---------|
| A) CLOSED — conexiunea s-a terminat | |
| B) FIN_WAIT_1 sau TIME_WAIT — în proces de închidere | |
| C) ESTABLISHED — încă deschisă până serverul confirmă | |
| D) LISTEN — așteaptă noi conexiuni | |

<details>
<summary><b>Click pentru răspuns și explicație</b></summary>

**Răspuns corect: B) FIN_WAIT_1 sau TIME_WAIT**

**Explicații:**

- **A) CLOSED** ❌ — Socket-ul NU trece direct în CLOSED. Trebuie să aștepte confirmarea de la server și să se asigure că toate pachetele au ajuns.

- **B) FIN_WAIT_1 sau TIME_WAIT** ✅ — CORECT!
  - `close()` trimite un pachet FIN
  - Socket-ul intră în FIN_WAIT_1 (așteaptă ACK pentru FIN)
  - După ACK: FIN_WAIT_2 (așteaptă FIN de la server)
  - După FIN de la server: TIME_WAIT (așteaptă 2×MSL pentru pachete întârziate)
  - Abia apoi: CLOSED

- **C) ESTABLISHED** ❌ — Era starea ÎNAINTE de `close()`. După `close()`, se inițiază închiderea.

- **D) LISTEN** ❌ — LISTEN este doar pentru SERVERE care așteaptă conexiuni noi. Un client nu intră niciodată în LISTEN.

**De ce TIME_WAIT durează?**
- Evită ca pachete vechi întârziate să fie confundate cu o nouă conexiune
- Durată tipică: 60-120 secunde (2×MSL - Maximum Segment Lifetime)

</details>

---

## 🗳️ Întrebarea 4: Căi Fișiere WSL

**Scenariu:**
Ai creat un fișier Python în Ubuntu WSL:
```bash
stud@PC:~$ echo "print('Hello')" > /home/stud/script.py
```

**Întrebare:** Cum poți deschide acest fișier din Windows Explorer?

| Opțiune | Răspuns |
|---------|---------|
| A) `C:\home\stud\script.py` | |
| B) `\\wsl$\Ubuntu\home\stud\script.py` | |
| C) `D:\WSL\home\stud\script.py` | |
| D) Nu se poate accesa din Windows | |

<details>
<summary><b>Click pentru răspuns și explicație</b></summary>

**Răspuns corect: B) `\\wsl$\Ubuntu\home\stud\script.py`**

**Explicații:**

- **A) `C:\home\stud\...`** ❌ — Sistemul de fișiere WSL nu este pe C:. WSL are propriul sistem de fișiere virtual.

- **B) `\\wsl$\Ubuntu\...`** ✅ — CORECT! 
  - `\\wsl$\` este o "share" virtuală creată de WSL
  - `Ubuntu` este numele distribuției (poate fi `Ubuntu-22.04` etc.)
  - Restul căii urmează structura Linux
  - Poți lipi această cale în Windows Explorer sau în File > Open din orice aplicație

- **C) `D:\WSL\...`** ❌ — WSL nu creează un folder explicit pe D:. Confuzie cu locația imaginii VHDX (care e în AppData, nu accesibilă direct).

- **D) Nu se poate** ❌ — Se poate! Microsoft a adăugat integrarea `\\wsl$\` tocmai pentru asta.

**Bonus - și invers funcționează:**
- Din WSL, accesezi `D:\RETELE\` ca `/mnt/d/RETELE/`
- Drive-urile Windows sunt montate în `/mnt/`

</details>

---

## 🗳️ Întrebarea 5: Izolare Rețele Docker

**Scenariu:**
Ai două containere definite în `docker-compose.yml`:
```yaml
services:
  frontend:
    networks:
      - webnet
  database:
    networks:
      - dbnet

networks:
  webnet:
  dbnet:
```

**Întrebare:** Poate containerul `frontend` să facă ping la containerul `database`?

| Opțiune | Răspuns |
|---------|---------|
| A) Da, toate containerele din același docker-compose.yml pot comunica | |
| B) Da, dar doar prin IP numeric, nu prin numele `database` | |
| C) Nu, sunt pe rețele Docker diferite, complet izolate | |
| D) Depinde de configurația firewall-ului Windows | |

<details>
<summary><b>Click pentru răspuns și explicație</b></summary>

**Răspuns corect: C) Nu, sunt pe rețele Docker diferite, complet izolate**

**Explicații:**

- **A) Da, toate din același compose...** ❌ — Fals! Docker Compose NU pune automat toate containerele pe aceeași rețea. Fiecare serviciu este conectat DOAR la rețelele specificate în secțiunea `networks:` a acelui serviciu.

- **B) Da, prin IP...** ❌ — Nici prin IP nu merge. Rețelele Docker sunt izolate la nivel Layer 2. Nu există rută între `webnet` și `dbnet`.

- **C) Nu, izolate** ✅ — CORECT! 
  - `frontend` este DOAR pe `webnet`
  - `database` este DOAR pe `dbnet`
  - Nu există suprapunere → nu pot comunica
  - Pentru comunicare, ambele trebuie să fie pe cel puțin o rețea comună

- **D) Depinde de firewall Windows** ❌ — Firewall-ul Windows nu intervine în comunicarea ÎNTRE containere. Izolarea este la nivel Docker, nu Windows.

**Soluția pentru a permite comunicarea:**
```yaml
services:
  frontend:
    networks:
      - webnet
      - shared  # adaugă rețea comună
  database:
    networks:
      - dbnet
      - shared  # adaugă aceeași rețea

networks:
  webnet:
  dbnet:
  shared:  # rețea comună pentru comunicare
```

</details>

---

## Utilizare în Laborator

### Când să Folosești Fiecare Întrebare

| Întrebare | Moment Optim | Durată |
|-----------|--------------|--------|
| 1. Port Mapping | După explicația docker-compose.yml | 7 min |
| 2. TCP vs UDP | După Exercițiul 3 (TCP) | 7 min |
| 3. Stări Socket | După demonstrația handshake | 7 min |
| 4. Căi WSL | La începutul laboratorului | 5 min |
| 5. Izolare Rețele | Când se discută despre networking | 7 min |

### Instrumente pentru Vot

- **Low-tech:** Ridicat mâna / Cartonașe colorate (A/B/C/D)
- **Mid-tech:** Google Forms cu răspuns live
- **High-tech:** Mentimeter, Kahoot, Poll Everywhere

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
