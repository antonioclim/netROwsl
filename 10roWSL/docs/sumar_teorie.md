# Sumar Teoretic - Săptămâna 10

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Cuprins

1. [Analogii pentru Înțelegere (CPA)](#analogii-pentru-înțelegere-cpa)
2. [Protocolul HTTP/HTTPS](#protocolul-httphttps)
3. [Handshake-ul TLS](#handshake-ul-tls)
4. [Arhitectura REST](#arhitectura-rest)
5. [Modelul Richardson](#modelul-richardson)
6. [Protocolul DNS](#protocolul-dns)
7. [Protocolul SSH](#protocolul-ssh)
8. [Protocolul FTP](#protocolul-ftp)

---

## Analogii pentru Înțelegere (CPA)

**Metoda Concret → Pictorial → Abstract** te ajută să înțelegi concepte noi pornind de la lucruri familiare.

### Container Docker

| Etapă | Explicație |
|-------|------------|
| **CONCRET** | Imaginează-ți o cutie de carton care conține TOT ce ai nevoie pentru a face o prăjitură: ingrediente, ustensile, rețetă, cuptor portabil. Oriunde duci cutia, poți face prăjitura identic - nu depinzi de bucătăria gazdei. |
| **PICTORIAL** | ![Container cu layers](https://docs.docker.com/get-started/images/container-what-is-container.png) - O cutie izolată cu aplicația și dependențele |
| **ABSTRACT** | `docker run nginx` - Creează și pornește un container din imaginea nginx |

### Port Mapping (-p 8080:80)

| Etapă | Explicație |
|-------|------------|
| **CONCRET** | Locuiești într-un bloc de apartamente. Adresa blocului e "Strada X, Nr. 8080" (portul HOST), dar apartamentul tău e "Ap. 80" (portul CONTAINER). Poștașul (cererea HTTP) vine la adresa blocului, portarul (Docker) îl direcționează la apartamentul corect. |
| **PICTORIAL** | `[Browser] → localhost:8080 → [Docker Host] → container:80 → [nginx]` |
| **ABSTRACT** | `-p 8080:80` sau în compose: `ports: ["8080:80"]` |

**Regulă de memorat:** `HOST:CONTAINER` - ce e în stânga e "ușa din exterior", ce e în dreapta e "ușa din interior".

### TLS Handshake

| Etapă | Explicație |
|-------|------------|
| **CONCRET** | Când suni la bancă pentru o operațiune: (1) Te prezinți și spui ce operațiune vrei, (2) Banca se prezintă și îți trimite o carte de vizită oficială cu ștampilă, (3) Verifici ștampila, (4) Stabiliți un cod secret pentru conversație pe care doar voi doi îl știți. |
| **PICTORIAL** | Vezi diagrama de mai jos |
| **ABSTRACT** | `ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)` |

### REST HATEOAS

| Etapă | Explicație |
|-------|------------|
| **CONCRET** | La un restaurant modern, meniul electronic nu doar listează felurile - fiecare fel are butoane: "Comandă", "Vezi ingrediente", "Adaugă la favorite", "Vezi rețete similare". Nu trebuie să memorezi unde să găsești fiecare funcție - meniul îți arată opțiunile disponibile. |
| **PICTORIAL** | Răspunsul JSON include `_links` cu acțiunile posibile |
| **ABSTRACT** | `{"id": 1, "nume": "Produs", "_links": {"self": "/produse/1", "delete": {"href": "/produse/1", "method": "DELETE"}}}` |

### FTP: Activ vs Pasiv

| Etapă | Explicație |
|-------|------------|
| **CONCRET** | **Activ:** Suni la o firmă de curierat și spui "Trimiteți curierul la mine acasă" - ei inițiază vizita. Dar dacă ești într-o clădire cu interfon și nu răspunzi, curierul nu poate intra. **Pasiv:** Suni la firmă și spui "Dați-mi adresa depozitului, vin eu să ridic coletul" - tu inițiezi vizita, deci nu ai probleme cu interfonul. |
| **PICTORIAL** | Vezi diagrama de mai jos |
| **ABSTRACT** | Comanda `PASV` în loc de `PORT` |

---

## Protocolul HTTP/HTTPS

### HTTP (Hypertext Transfer Protocol)

HTTP este un protocol de nivel aplicație care funcționează peste TCP. Folosit pentru comunicarea între clienți web (browsere) și servere web.

**Structura unei cereri HTTP:**
```
METODĂ URI HTTP/Versiune
Headere
[Corp opțional]
```

**Metode HTTP principale:**

| Metodă | Descriere | Idempotentă | Sigură |
|--------|-----------|-------------|--------|
| GET | Obține o resursă | Da | Da |
| POST | Creează o resursă | Nu | Nu |
| PUT | Actualizează/înlocuiește | Da | Nu |
| DELETE | Șterge o resursă | Da | Nu |
| HEAD | GET fără corp | Da | Da |
| OPTIONS | Opțiuni disponibile | Da | Da |

**Coduri de stare importante:**

- **2xx** - Succes (200 OK, 201 Created, 204 No Content)
- **3xx** - Redirecționare (301, 302, 304)
- **4xx** - Eroare client (400 Bad Request, 401, 403, 404 Not Found)
- **5xx** - Eroare server (500 Internal Server Error, 503)

### HTTPS

HTTPS = HTTP + TLS/SSL. Oferă:
- **Confidențialitate** - datele sunt criptate
- **Integritate** - datele nu pot fi modificate în tranzit
- **Autentificare** - serverul este verificat prin certificat

---

## Handshake-ul TLS

Procesul de negociere TLS 1.3:

```
Client                                  Server
  |                                       |
  |──── ClientHello ────────────────────>|
  |     (versiune, cipher suites,        |
  |      random, extensii)               |
  |                                       |
  |<────────────────── ServerHello ──────|
  |                    (cipher selectat,  |
  |                     random, cert)     |
  |                                       |
  |<───── EncryptedExtensions ───────────|
  |<───── Certificate ───────────────────|
  |<───── CertificateVerify ─────────────|
  |<───── Finished ──────────────────────|
  |                                       |
  |────── Finished ─────────────────────>|
  |                                       |
  |═══════ Trafic Criptat ═══════════════|
```

---

## Arhitectura REST

**REST** (Representational State Transfer) este un stil arhitectural pentru sisteme distribuite.

### Principii REST:

1. **Client-Server** - Separarea responsabilităților
2. **Stateless** - Fiecare cerere conține toată informația necesară
3. **Cacheable** - Răspunsurile pot fi stocate în cache
4. **Interfață Uniformă** - Resurse identificate prin URI-uri
5. **Sistem Stratificat** - Arhitectură pe straturi
6. **Code on Demand** (opțional) - Cod executabil transferat la cerere

### Resurse REST

O resursă este orice entitate care poate fi denumită și adresată:
- Colecție: `/api/produse`
- Element: `/api/produse/123`
- Sub-resursă: `/api/produse/123/recenzii`

---

## Modelul Richardson

Leonard Richardson a definit 4 niveluri de maturitate pentru API-uri web:

### Diagrama Nivelurilor REST

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Nivel 3: HATEOAS                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ GET /produse/1                                           │   │
│  │ → { id: 1, nume: "Laptop",                               │   │
│  │     _links: {                                            │   │
│  │       self: "/produse/1",                                │   │
│  │       actualizeaza: {href: "/produse/1", method: "PUT"}, │   │
│  │       sterge: {href: "/produse/1", method: "DELETE"},    │   │
│  │       recenzii: "/produse/1/recenzii"                    │   │
│  │     }                                                    │   │
│  │   }                                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ▲                                   │
│ ─────────────────────────────┼─────────────────────────────────  │
│                              │                                   │
│  Nivel 2: Verbe HTTP                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ GET    /produse       → 200 OK + listă                   │   │
│  │ POST   /produse       → 201 Created + resursă nouă       │   │
│  │ PUT    /produse/1     → 200 OK + resursă actualizată     │   │
│  │ DELETE /produse/1     → 204 No Content                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ▲                                   │
│ ─────────────────────────────┼─────────────────────────────────  │
│                              │                                   │
│  Nivel 1: Resurse                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ POST /produse           (creează)                        │   │
│  │ POST /produse/1         (citește/actualizează/șterge)    │   │
│  │ POST /categorii         (operații pe categorii)          │   │
│  │ → Toate acțiunile sunt POST, dar URI-uri separate        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ▲                                   │
│ ─────────────────────────────┼─────────────────────────────────  │
│                              │                                   │
│  Nivel 0: RPC (Mlaștina POX)                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ POST /api                                                │   │
│  │ Body: {"actiune": "listeazaProduse"}                     │   │
│  │ Body: {"actiune": "creeazaProdus", "date": {...}}        │   │
│  │ Body: {"actiune": "stergeProdus", "id": 1}               │   │
│  │ → Un singur endpoint, acțiunea e în body                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Nivelul 0: Mlaștina POX (Plain Old XML/JSON)

- Un singur endpoint
- HTTP folosit doar ca transport
- Operații specificate în corpul cererii
- Exemplu RPC:
  ```json
  POST /api
  {"actiune": "obtineProdus", "id": 123}
  ```

### Nivelul 1: Resurse

- Endpoint-uri separate pentru fiecare resursă
- Încă un singur verb HTTP (de obicei POST)
- URI-uri ca identificatori de resurse
  ```
  POST /produse
  POST /produse/123
  ```

### Nivelul 2: Verbe HTTP

- Utilizarea corectă a metodelor HTTP
- GET, POST, PUT, DELETE etc.
- Coduri de stare HTTP corecte
  ```
  GET    /produse       → 200 OK
  POST   /produse       → 201 Created
  PUT    /produse/123   → 200 OK
  DELETE /produse/123   → 204 No Content
  ```

### Nivelul 3: HATEOAS

**HATEOAS** = Hypermedia As The Engine Of Application State

Răspunsurile includ linkuri către acțiunile disponibile:

```json
{
  "id": 123,
  "nume": "Laptop",
  "pret": 2999.99,
  "_links": {
    "self": "/produse/123",
    "actualizeaza": {"href": "/produse/123", "method": "PUT"},
    "sterge": {"href": "/produse/123", "method": "DELETE"},
    "recenzii": "/produse/123/recenzii"
  }
}
```

---

## Protocolul DNS

### Structura Mesajelor DNS

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ID                         |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|QR|  Opcode |AA|TC|RD|RA|  Z |    RCODE        |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                  QDCOUNT                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                  ANCOUNT                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                  NSCOUNT                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                  ARCOUNT                      |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

### Tipuri de Înregistrări DNS

| Tip | Descriere | Exemplu |
|-----|-----------|---------|
| A | Adresă IPv4 | example.com → 93.184.216.34 |
| AAAA | Adresă IPv6 | example.com → 2606:2800:... |
| CNAME | Alias (nume canonic) | www → example.com |
| MX | Server mail | example.com → mail.example.com |
| NS | Server de nume | example.com → ns1.example.com |
| TXT | Text arbitrar | Verificări, SPF, DKIM |
| SOA | Start of Authority | Metadate zonă |

### Coduri de Răspuns DNS

| Cod | Nume | Semnificație |
|-----|------|--------------|
| 0 | NOERROR | Interogare procesată cu succes |
| 3 | NXDOMAIN | Domeniul nu există |
| 2 | SERVFAIL | Eroare server DNS |
| 5 | REFUSED | Server refuză cererea |

---

## Protocolul SSH

### Arhitectura SSH

SSH are trei straturi principale:

1. **Transport Layer** (RFC 4253)
   - Negocierea algoritmilor
   - Schimb de chei (Diffie-Hellman)
   - Criptare și integritate

2. **User Authentication** (RFC 4252)
   - Autentificare cu parolă
   - Autentificare cu cheie publică
   - Autentificare keyboard-interactive

3. **Connection Layer** (RFC 4254)
   - Multiplexare canale
   - Sesiuni interactive
   - Port forwarding

### Tipuri de Canale SSH

- **session** - Sesiune shell sau comandă
- **x11** - Forwarding X11
- **forwarded-tcpip** - Port forwarding remote
- **direct-tcpip** - Port forwarding local

---

## Protocolul FTP

### Moduri de Transfer

**Mod Activ:**
```
Client                           Server
  |                                |
  |─── PORT client_ip,port ──────>|  (1) Client spune: "Trimite date la mine"
  |                                |
  |<──────── Date ─────────────────|  (2) Server inițiază conexiune → CLIENT
            (server → client:port)           ↑
                                       POATE FI BLOCAT DE FIREWALL!
```

**Mod Pasiv:**
```
Client                           Server
  |                                |
  |─── PASV ─────────────────────>|  (1) Client întreabă: "Pe ce port să mă conectez?"
  |                                |
  |<─── 227 (server_ip,port) ─────|  (2) Server răspunde cu port
  |                                |
  |═══════ Date ═════════════════>|  (3) Client inițiază conexiune → SERVER
        (client → server:port)            ↑
                                    FUNCȚIONEAZĂ PRIN FIREWALL!
```

**De ce modul pasiv funcționează prin firewall:**
- Firewall-urile permit de obicei conexiuni OUTBOUND (din interior spre exterior)
- Blochează conexiuni INBOUND (din exterior spre interior)
- În modul activ, SERVERUL inițiază conexiunea de date → blocat
- În modul pasiv, CLIENTUL inițiază conexiunea de date → permis

### Comenzi FTP Comune

| Comandă | Descriere |
|---------|-----------|
| USER | Nume utilizator |
| PASS | Parolă |
| PWD | Print working directory |
| CWD | Change working directory |
| LIST | Listează directorul |
| RETR | Descarcă fișier |
| STOR | Încarcă fișier |
| DELE | Șterge fișier |
| PASV | Activează modul pasiv |
| PORT | Activează modul activ |
| QUIT | Închide sesiunea |

---

## Referințe

- RFC 2616 - HTTP/1.1
- RFC 8446 - TLS 1.3
- RFC 1035 - DNS
- RFC 4253 - SSH Transport
- RFC 959 - FTP
- Fielding, R. (2000) - Disertație REST

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
