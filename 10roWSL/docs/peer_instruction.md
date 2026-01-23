# Întrebări Peer Instruction - Săptămâna 10

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Instrucțiuni pentru Instructor

**Metodologie Peer Instruction (Mazur):**
1. Prezintă scenariul și întrebarea (1 min)
2. Studenții votează individual - fără discuții (1 min)
3. Discuție în perechi - argumentează alegerea (3 min)
4. Revot individual (30 sec)
5. Explicație și demonstrație (2 min)

**Țintă:** ~50% răspunsuri corecte la primul vot (indică dificultate optimă)

---

## 🗳️ PI-1: Port Mapping Docker

### Scenariu

Ai următoarea configurație în `docker-compose.yml`:

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

### Întrebare

Ce URL folosești din browserul Windows pentru a accesa acest server nginx?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | `http://localhost:80` |
| **B** | `http://localhost:8080` |
| **C** | `http://172.20.0.10:80` |
| **D** | `http://nginx:80` |

---

### Note Instructor

**Răspuns corect:** B

**Analiza distractorilor:**

| Opțiune | Misconceptie | % Studenți |
|---------|--------------|------------|
| A | Confuzie port container vs port host - crede că portul din dreapta (80) e cel expus | ~30% |
| C | Crede că trebuie IP-ul intern Docker pentru acces din Windows | ~20% |
| D | Crede că numele serviciului se rezolvă din afara rețelei Docker | ~15% |

**După discuție:** Desenează pe tablă:
```
[Browser Windows] → localhost:8080 → [Docker Host] → container:80 → [nginx]
                    ^^^^^^^^^^^^                      ^^^^^^^^^^^
                    port HOST                         port CONTAINER
```

**Întrebare follow-up:** „Ce s-ar întâmpla dacă ai `-p 80:80`?"

---

## 🗳️ PI-2: HTTP vs HTTPS în Wireshark

### Scenariu

Capturezi trafic cu Wireshark pe interfața `vEthernet (WSL)`. Ai două ferestre de terminal:
- Terminal 1: `curl http://localhost:8000/secret.txt`
- Terminal 2: `curl -k https://localhost:4443/secret.txt`

### Întrebare

Ce vei vedea diferit în Wireshark între cele două capturi?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | HTTP arată cereri/răspunsuri în clar, HTTPS arată doar „Encrypted Application Data" |
| **B** | Ambele arată conținutul în clar, doar headerele diferă |
| **C** | HTTP nu apare deloc în Wireshark, doar HTTPS |
| **D** | HTTPS arată mai multe pachete, dar conținutul e identic vizibil |

---

### Note Instructor

**Răspuns corect:** A

**Analiza distractorilor:**

| Opțiune | Misconceptie | % Studenți |
|---------|--------------|------------|
| B | Nu înțelege scopul TLS - crede că e doar „altceva" nu criptare | ~25% |
| C | Confuzie între protocoale - HTTP e cel mai vizibil în Wireshark | ~10% |
| D | Înțelege că sunt diferite dar nu că diferența e criptarea | ~20% |

**Demonstrație live:**
1. Pornește captura Wireshark
2. Rulează ambele curl-uri
3. Filtru `http` - arată conținutul `secret.txt` în clar
4. Filtru `tls` - arată „Application Data" fără conținut vizibil

**Concept cheie:** TLS criptează TOTUL după handshake, nu doar „datele sensibile"

---

## 🗳️ PI-3: Niveluri REST Richardson

### Scenariu

Un API returnează următorul răspuns pentru `GET /produse/1`:

```json
{
  "id": 1,
  "nume": "Laptop Gaming",
  "pret": 4500,
  "_links": {
    "self": {"href": "/produse/1"},
    "actualizeaza": {"href": "/produse/1", "method": "PUT"},
    "sterge": {"href": "/produse/1", "method": "DELETE"},
    "categorie": {"href": "/categorii/electronice"}
  }
}
```

### Întrebare

Ce nivel de maturitate REST (Richardson) este implementat?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | Nivelul 0 - RPC (Remote Procedure Call) |
| **B** | Nivelul 1 - Resurse |
| **C** | Nivelul 2 - Verbe HTTP |
| **D** | Nivelul 3 - HATEOAS |

---

### Note Instructor

**Răspuns corect:** D

**Analiza distractorilor:**

| Opțiune | Misconceptie | % Studenți |
|---------|--------------|------------|
| B | Vede URL-ul `/produse/1` și se oprește acolo | ~15% |
| C | Vede că folosește GET și presupune că e nivelul verbelor | ~35% |
| A | Nu înțelege deloc modelul Richardson | ~10% |

**Indicator cheie:** Prezența `_links` = HATEOAS (Hypermedia As The Engine Of Application State)

**Întrebări de verificare:**
- „Ce nivel ar fi dacă NU ar avea `_links`?" → Nivelul 2
- „Ce nivel ar fi dacă TOTUL ar fi POST pe `/api`?" → Nivelul 0

**Diagrama pe tablă:**
```
Nivel 3: _links prezente (navigare prin hypermedia)
   ↑
Nivel 2: GET/POST/PUT/DELETE corecte
   ↑
Nivel 1: URI-uri separate (/produse, /categorii)
   ↑
Nivel 0: Un singur endpoint, acțiuni în body
```

---

## 🗳️ PI-4: FTP Activ vs Pasiv

### Scenariu

Un student lucrează de acasă, în spatele unui router cu NAT și firewall care:
- Permite conexiuni OUTBOUND (din casă spre internet)
- Blochează conexiuni INBOUND (din internet spre casă)

Studentul încearcă să se conecteze la un server FTP public pentru a descărca un fișier.

### Întrebare

Ce mod FTP va funcționa în această situație?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | Mod Activ - serverul inițiază conexiunea de date către client |
| **B** | Mod Pasiv - clientul inițiază conexiunea de date către server |
| **C** | Ambele moduri funcționează identic |
| **D** | Niciunul nu funcționează prin NAT/firewall |

---

### Note Instructor

**Răspuns corect:** B

**Analiza distractorilor:**

| Opțiune | Misconceptie | % Studenți |
|---------|--------------|------------|
| A | Nu înțelege direcția conexiunii în modul activ | ~40% |
| C | Nu înțelege diferența fundamentală între moduri | ~15% |
| D | Pesimism excesiv - nu știe că pasiv rezolvă problema | ~10% |

**Diagrama pe tablă:**

```
MOD ACTIV (NU funcționează prin NAT):
Client ──PORT 20000──> Server (control)
Client <──────────── Server (date) ← BLOCAT de firewall!

MOD PASIV (funcționează):
Client ──────────────> Server (control)
Client ──────────────> Server:30000 (date) ← Client inițiază = OK
```

**Concept cheie:** 
- Firewall-ul blochează conexiuni INBOUND
- Modul PASIV = clientul inițiază AMBELE conexiuni (control + date)
- De aceea serverul nostru FTP folosește porturi pasive 30000-30009

---

## 🗳️ PI-5: DNS Resolution - NXDOMAIN

### Scenariu

Rulezi următoarea comandă către serverul DNS din laborator:

```bash
dig @localhost -p 5353 inexistent.lab.local
```

Domeniul `inexistent.lab.local` NU este configurat în serverul DNS.

### Întrebare

Ce cod de răspuns DNS vei primi?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | NOERROR cu secțiunea ANSWER goală |
| **B** | NXDOMAIN (Non-Existent Domain) |
| **C** | SERVFAIL (Server Failure) |
| **D** | REFUSED (Query Refused) |

---

### Note Instructor

**Răspuns corect:** B

**Analiza distractorilor:**

| Opțiune | Misconceptie | % Studenți |
|---------|--------------|------------|
| A | Confuzie între „găsit dar gol" vs „nu există deloc" | ~30% |
| C | Crede că orice eroare = SERVFAIL | ~15% |
| D | Confuzie cu firewall/permisiuni | ~10% |

**Diferența critică:**
- **NOERROR + ANSWER gol:** Domeniul EXISTĂ dar nu are înregistrarea cerută (ex: ceri MX dar există doar A)
- **NXDOMAIN:** Domeniul NU EXISTĂ deloc în zona DNS

**Demonstrație:**
```bash
# NXDOMAIN - domeniu inexistent
dig @localhost -p 5353 xyz.lab.local
# Observă: status: NXDOMAIN

# NOERROR - domeniu există
dig @localhost -p 5353 web.lab.local
# Observă: status: NOERROR, ANSWER: 1
```

---

## 🗳️ PI-6: Container Networking

### Scenariu

Ai următoarea configurație Docker Compose:

```yaml
services:
  frontend:
    networks:
      - webnet
  backend:
    networks:
      - webnet
      - dbnet
  database:
    networks:
      - dbnet

networks:
  webnet:
  dbnet:
```

### Întrebare

Poate containerul `frontend` să comunice direct cu containerul `database`?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | Da, toate containerele din același fișier compose pot comunica |
| **B** | Da, dar doar prin adresa IP, nu prin nume |
| **C** | Nu, sunt pe rețele diferite fără suprapunere |
| **D** | Nu, containerele Docker nu pot comunica niciodată între ele |

---

### Note Instructor

**Răspuns corect:** C

**Analiza distractorilor:**

| Opțiune | Misconceptie | % Studenți |
|---------|--------------|------------|
| A | Crede că „același compose" = „aceeași rețea" | ~35% |
| B | Înțelege parțial izolarea dar crede că IP-ul traversează | ~20% |
| D | Pesimism excesiv, nu înțelege rețelele Docker | ~5% |

**Diagrama pe tablă:**
```
┌─────────────────────────────────────────┐
│              webnet                      │
│  ┌──────────┐      ┌──────────┐         │
│  │ frontend │ ←──→ │ backend  │         │
│  └──────────┘      └────┬─────┘         │
└─────────────────────────│───────────────┘
                          │
┌─────────────────────────│───────────────┐
│              dbnet      │               │
│                    ┌────┴─────┐         │
│                    │ backend  │         │
│                    └────┬─────┘         │
│                         │               │
│                    ┌────┴─────┐         │
│                    │ database │         │
│                    └──────────┘         │
└─────────────────────────────────────────┘

frontend ←✗→ database (rețele diferite, fără cale)
frontend ←──→ backend ←──→ database (backend e "podul")
```

**Concept cheie:** Izolarea prin rețele Docker - backend acționează ca gateway/proxy

---

## Sumar Întrebări

| # | Subiect | Concept Cheie | Dificultate |
|---|---------|---------------|-------------|
| PI-1 | Port Mapping | host:container | Medie |
| PI-2 | HTTP vs HTTPS | Criptare TLS | Medie |
| PI-3 | REST Levels | HATEOAS | Medie-Ridicată |
| PI-4 | FTP Modes | Direcția conexiunii | Ridicată |
| PI-5 | DNS Codes | NXDOMAIN vs NOERROR | Medie |
| PI-6 | Docker Networks | Izolare rețele | Ridicată |

---

## Utilizare Recomandată

| Moment în laborator | Întrebări recomandate |
|---------------------|----------------------|
| După prezentarea Docker Compose | PI-1, PI-6 |
| Înainte de exercițiul Wireshark | PI-2 |
| După explicația REST | PI-3 |
| Înainte de exercițiul FTP | PI-4 |
| După demonstrația DNS | PI-5 |

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
