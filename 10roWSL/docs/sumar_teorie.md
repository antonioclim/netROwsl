# Sumar Teoretic - Săptămâna 10

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Cuprins

1. [Protocolul HTTP/HTTPS](#protocolul-httphttps)
2. [Handshake-ul TLS](#handshake-ul-tls)
3. [Arhitectura REST](#arhitectura-rest)
4. [Modelul Richardson](#modelul-richardson)
5. [Protocolul DNS](#protocolul-dns)
6. [Protocolul SSH](#protocolul-ssh)
7. [Protocolul FTP](#protocolul-ftp)

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
  |─── PORT n ────────────────────>|
  |<────────────────── Date ───────|
            (server → client:n)
```

**Mod Pasiv:**
```
Client                           Server
  |                                |
  |─── PASV ──────────────────────>|
  |<─── 227 (ip,port) ─────────────|
  |═══════ Date ══════════════════>|
        (client → server:port)
```

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
