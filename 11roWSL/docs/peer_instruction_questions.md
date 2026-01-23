# Întrebări Peer Instruction — Săptămâna 11

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix
>
> Folosiți aceste întrebări pentru discuții în perechi.
> **Secvență:** Vot individual (1 min) → Discuție în perechi (3 min) → Revot (30 sec) → Explicație (2 min)

---

## PI-1: Port Mapping

### Scenariu

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

### Întrebare

Ce URL folosești din Windows pentru a accesa nginx-ul din container?

| Opțiune | Răspuns |
|:-------:|---------|
| **A** | `http://localhost:80` |
| **B** | `http://localhost:8080` |
| **C** | `http://172.17.0.2:80` |
| **D** | `http://nginx:80` |

<details>
<summary>📝 Răspuns și explicație</summary>

### Răspuns corect: **B**

**De ce celelalte sunt greșite:**
- **A)** 80 este portul din interiorul containerului, nu cel expus către host
- **C)** IP-ul intern Docker (172.17.x.x) nu este accesibil direct din Windows
- **D)** Numele `nginx` se rezolvă doar în interiorul rețelei Docker, nu din afară

**Concept cheie:** Sintaxa `host_port:container_port` — primul număr este cel la care te conectezi din exterior.

**Analogie:** Blocul are adresa "localhost", apartamentul 8080 duce la camera 80 din container.
</details>

---

## PI-2: Health Check Timing

### Scenariu

```yaml
healthcheck:
  interval: 10s
  timeout: 5s
  retries: 3
  start_period: 30s
```

### Întrebare

Un backend care funcționa perfect cade brusc. După câte secunde (aproximativ) va fi scos din rotație?

| Opțiune | Răspuns |
|:-------:|---------|
| **A** | 5 secunde |
| **B** | 15 secunde |
| **C** | 30 secunde |
| **D** | 45 secunde |

<details>
<summary>📝 Răspuns și explicație</summary>

### Răspuns corect: **C** (aproximativ 30 secunde)

**Calcul:**
- Prima verificare eșuează: așteptăm `interval` = 10s
- A doua verificare eșuează: încă 10s
- A treia verificare eșuează: încă 10s → **MARCAT NESĂNĂTOS**

Total: 3 × 10s = ~30 secunde în cel mai rău caz

**Atenție:** `start_period` (30s) se aplică doar la pornirea containerului, nu la detectarea căderilor ulterioare!

**De ce nu 15s?** Timeout-ul de 5s este timpul maxim de așteptare pentru un singur răspuns, nu se adună.
</details>

---

## PI-3: Comunicare între Containere

### Scenariu

```yaml
services:
  frontend:
    networks: [webnet]
  backend:
    networks: [webnet, dbnet]
  database:
    networks: [dbnet]
```

### Întrebare

Poate containerul `frontend` să acceseze containerul `database` direct?

| Opțiune | Răspuns |
|:-------:|---------|
| **A** | Da, sunt în același fișier docker-compose |
| **B** | Da, dar doar prin adresa IP a containerului |
| **C** | Nu, sunt pe rețele diferite fără suprapunere |
| **D** | Nu, containerele Docker nu pot comunica niciodată între ele |

<details>
<summary>📝 Răspuns și explicație</summary>

### Răspuns corect: **C**

**Analiza rețelelor:**
- `frontend` este DOAR pe `webnet`
- `database` este DOAR pe `dbnet`
- Nu există suprapunere → **nu pot comunica**

**Cine poate comunica cu cine:**
```
frontend ◄──► backend ◄──► database
   │              │            │
 webnet      webnet+dbnet    dbnet
```

`backend` este pe ambele rețele, deci poate fi "punte" între `frontend` și `database`.

**De ce A și B sunt greșite:** Faptul că sunt în același docker-compose NU înseamnă că pot comunica — rețelele le izolează!

**De ce D este greșit:** Containerele CHIAR pot comunica, dar DOAR dacă sunt pe aceeași rețea.
</details>

---

## PI-4: Algoritm IP Hash

### Scenariu

Ai 3 backend-uri configurate cu algoritmul `ip_hash`. Un singur client face 100 de cereri consecutive.

### Întrebare

Cum se distribuie cele 100 de cereri între backend-uri?

| Opțiune | Răspuns |
|:-------:|---------|
| **A** | ~33 cereri la fiecare backend |
| **B** | Toate 100 la un singur backend |
| **C** | Primele 50 la unul, restul la altul |
| **D** | Depinde de încărcarea fiecărui backend |

<details>
<summary>📝 Răspuns și explicație</summary>

### Răspuns corect: **B**

**De ce?** `ip_hash` calculează `hash(IP_client)` și folosește rezultatul pentru a alege backend-ul. Același IP → același hash → **același backend mereu**.

**Când ai folosi IP Hash:**
- Aplicații cu sesiuni server-side (shopping cart în memorie)
- Când vrei "sticky sessions" fără cookies

**Ce ar da celelalte răspunsuri:**
- **A (~33 fiecare)** = Round Robin
- **D (după încărcare)** = Least Connections

**Atenție:** IP Hash poate crea dezechilibru dacă mulți clienți vin din spatele aceluiași NAT (toți au același IP public)!
</details>

---

## PI-5: FTP Activ vs Pasiv

### Scenariu

Un client din spatele unui router NAT casnic încearcă să descarce un fișier de pe un server FTP din internet.

### Întrebare

Ce mod FTP va funcționa?

| Opțiune | Răspuns |
|:-------:|---------|
| **A** | Doar modul ACTIV |
| **B** | Doar modul PASIV |
| **C** | Ambele moduri |
| **D** | Niciunul, FTP nu funcționează prin NAT |

<details>
<summary>📝 Răspuns și explicație</summary>

### Răspuns corect: **B**

**De ce modul ACTIV eșuează:**
1. Clientul trimite `PORT 192,168,1,5,78,32` (IP-ul său local)
2. Serverul încearcă să se conecteze la 192.168.1.5 — dar aceasta este o adresă privată!
3. Serverul nu poate ajunge la client → **EȘEC**

**De ce modul PASIV funcționează:**
1. Clientul trimite `PASV`
2. Serverul răspunde cu IP-ul și portul său public
3. Clientul inițiază conexiunea către server (outbound) → **NAT permite**

**Regulă simplă:** Conexiunile outbound (tu → internet) trec prin NAT. Conexiunile inbound (internet → tu) sunt blocate implicit.

**De aceea** aproape toate aplicațiile FTP moderne folosesc PASV implicit.
</details>

---

## PI-6: DNS TTL

### Scenariu

Faci o cerere DNS pentru `example.com` și primești răspunsul cu TTL = 300 secunde.

### Întrebare

Ce se întâmplă dacă faci aceeași cerere după 200 de secunde?

| Opțiune | Răspuns |
|:-------:|---------|
| **A** | Se trimite o nouă cerere către serverul DNS |
| **B** | Se returnează răspunsul din cache cu TTL = 100 |
| **C** | Se returnează răspunsul din cache cu TTL = 300 |
| **D** | Eroare — TTL-ul trebuie să expire complet |

<details>
<summary>📝 Răspuns și explicație</summary>

### Răspuns corect: **B**

**Cum funcționează TTL-ul:**
- La primirea răspunsului: TTL = 300s, salvat în cache
- După 200s: TTL rămas = 300 - 200 = **100s**
- Răspunsul se returnează din cache cu TTL = 100

**De ce contează:**
- Clientul știe cât timp mai poate folosi informația
- Când TTL ajunge la 0, trebuie să întrebe din nou serverul DNS

**Analogie cu agenda:** Ai scris numărul Mariei cu nota "valid 5 minute". După 3 minute, numărul e încă valid, dar doar pentru încă 2 minute.

**Când se trimite nouă cerere:** Doar după ce TTL ajunge la 0 (după 300s).
</details>

---

## PI-7: Nginx Upstream Weight

### Scenariu

```nginx
upstream backend {
    server web1:80 weight=3;
    server web2:80 weight=2;
    server web3:80 weight=1;
}
```

### Întrebare

Dacă primești 60 de cereri, aproximativ câte vor ajunge la fiecare backend?

| Opțiune | Răspuns |
|:-------:|---------|
| **A** | web1: 20, web2: 20, web3: 20 |
| **B** | web1: 30, web2: 20, web3: 10 |
| **C** | web1: 60, web2: 0, web3: 0 |
| **D** | web1: 10, web2: 20, web3: 30 |

<details>
<summary>📝 Răspuns și explicație</summary>

### Răspuns corect: **B**

**Calcul:**
- Total ponderi = 3 + 2 + 1 = 6
- web1: (3/6) × 60 = **30 cereri** (50%)
- web2: (2/6) × 60 = **20 cereri** (~33%)
- web3: (1/6) × 60 = **10 cereri** (~17%)

**Când folosești ponderi:**
- Servere cu capacități diferite (web1 e de 3x mai puternic)
- Migrare graduală (noul server primește mai puțin trafic inițial)

**De ce nu D:** Weight-ul mai mare = mai multe cereri, nu invers!
</details>

---

## PI-8: Docker Volume vs Bind Mount

### Scenariu

```yaml
services:
  web:
    volumes:
      - ./html:/usr/share/nginx/html:ro    # Opțiunea A
      - nginx_data:/var/log/nginx           # Opțiunea B
      
volumes:
  nginx_data:
```

### Întrebare

Care afirmație este corectă?

| Opțiune | Răspuns |
|:-------:|---------|
| **A** | Ambele sunt volume Docker gestionate de Docker |
| **B** | Ambele sunt bind mounts către sistemul de fișiere host |
| **C** | Prima (./html) e bind mount, a doua (nginx_data) e volume Docker |
| **D** | Prima e read-write, a doua e read-only |

<details>
<summary>📝 Răspuns și explicație</summary>

### Răspuns corect: **C**

**Diferența:**
- `./html:/path` — **Bind mount**: mapează direct un folder din host
- `nginx_data:/path` — **Volume Docker**: gestionat de Docker, stocat în `/var/lib/docker/volumes/`

**Cum le recunoști:**
- Cale relativă/absolută (`./`, `/home/`) = Bind mount
- Nume simplu (`nginx_data`) = Volume Docker

**De ce contează:**
- Bind mounts: ușor de editat din host, dar depind de structura host-ului
- Volumes: portabile, gestionate de Docker, backup mai ușor

**Nota `:ro`:** Prima montare este read-only (containerul nu poate modifica), dar asta nu o face volume Docker.
</details>

---

## Note pentru Instructor

### Cum să folosești aceste întrebări

1. **Afișează întrebarea** (fără răspuns) pe ecran
2. **Vot individual** — studenții votează A/B/C/D (1 minut)
3. **Notează distribuția** — dacă e 30-70%, perfect pentru discuție
4. **Discuție în perechi** — "Convinge-ți colegul" (3 minute)
5. **Revot** — vezi dacă s-a schimbat distribuția
6. **Explicație** — folosește secțiunea "Răspuns și explicație"

### Ținte pentru distribuția votului inițial

| Distribuție | Interpretare | Acțiune |
|:-----------:|--------------|---------|
| >80% corect | Prea ușoară | Treci mai departe |
| 50-80% corect | Ideal | Discuție în perechi |
| <50% corect | Concept dificil | Explică, apoi revino la întrebare |

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
