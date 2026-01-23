# Rezumat Teoretic: Protocoale de Aplicație și Echilibrare de Sarcină

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

> 📚 **Documente înrudite:**
> - [Analogii pentru Concepte](./analogii_concepte.md) — Explicații vizuale CPA
> - [Glosar](./glosar.md) — Definiții termeni
> - [Întrebări Peer Instruction](./peer_instruction_questions.md) — Pentru discuții

---

## 1. File Transfer Protocol (FTP)

### 1.1 Arhitectură cu Conexiune Duală

FTP folosește o arhitectură distinctă cu două conexiuni separate:

**Canal de control (Portul 21)**
- Conexiune TCP persistentă pe toată durata sesiunii
- Transportă comenzile și răspunsurile
- Format text (ASCII) ușor de citit
- Comenzi: USER, PASS, LIST, RETR, STOR, QUIT

**Canal de date (Port dinamic)**
- Conexiune TCP separată pentru fiecare transfer
- Transportă datele efective (fișiere, listări)
- Închisă după fiecare transfer
- Portul depinde de modul (activ/pasiv)

### 1.2 Moduri de Operare

**Modul Activ (PORT)**
```
Client                              Server
  |                                    |
  |-------- Conectare port 21 -------->|
  |<-------- 220 Bun venit ------------|
  |-------- USER utilizator ---------->|
  |<-------- 331 Parolă? --------------|
  |-------- PASS parola -------------->|
  |<-------- 230 Autentificat ---------|
  |-------- PORT 192,168,1,5,78,32 --->|  (Client ascultă pe 192.168.1.5:20000)
  |<-------- 200 OK -------------------|
  |-------- RETR fisier.txt ---------->|
  |<======= Conexiune de date =========|  (Server conectează la client)
  |<======= Conținut fișier ===========|
  |<-------- 226 Transfer complet -----|
```

**Modul Pasiv (PASV)**
```
Client                              Server
  |                                    |
  |-------- PASV --------------------->|
  |<-------- 227 (192,168,1,10,195,80) |  (Server ascultă pe 192.168.1.10:50000)
  |=======> Conexiune de date ========>|  (Client conectează la server)
  |-------- RETR fisier.txt ---------->|
  |<======= Conținut fișier ===========|
  |<-------- 226 Transfer complet -----|
```

> 🧪 **Verifică înțelegerea:** Dacă un client din spatele unui NAT încearcă FTP activ, ce se va întâmpla? De ce modul pasiv rezolvă problema?

**Comparație**

| Aspect | Mod Activ | Mod Pasiv |
|--------|-----------|-----------|
| Inițiator conexiune date | Server | Client |
| Compatibil NAT | Nu | Da |
| Compatibil firewall | Dificil | Mai ușor |
| Folosire modernă | Rar | Standard |

### 1.3 Comenzi FTP Comune

| Comandă | Descriere | Exemplu |
|---------|-----------|---------|
| USER | Nume utilizator | USER admin |
| PASS | Parolă | PASS secret123 |
| LIST | Listează directorul | LIST /pub |
| RETR | Descarcă fișier | RETR document.pdf |
| STOR | Încarcă fișier | STOR raport.xlsx |
| PWD | Director curent | PWD |
| CWD | Schimbă director | CWD /home/user |
| QUIT | Deconectare | QUIT |

---

## 2. Domain Name System (DNS)

### 2.1 Ierarhia DNS

DNS funcționează ca o bază de date distribuită ierarhic:

```
                          [Servere Root (.)]
                          13 clustere distribuite global
                                   |
              +--------------------+--------------------+
              |                    |                    |
          [.com]               [.org]               [.ro]
     Servere TLD          Servere TLD          Servere TLD
              |                                        |
     +--------+--------+                               |
     |                 |                               |
[google.com]     [example.com]                   [gov.ro]
  Autoritative       Autoritative               Autoritative
              |
     [www.google.com] → 142.250.185.78
```

> 💡 **Analogie:** DNS cache este ca agenda ta de telefon — prima dată cauți numărul în cartea de telefon (server DNS), apoi îl salvezi local. Vezi [Analogii Concepte](./analogii_concepte.md#2-dns-cache).

### 2.2 Tipuri de Rezolvere

**Rezolvare Recursivă**
- Clientul trimite o singură cerere
- Rezolver-ul face toate interogările necesare
- Răspunsul final returnează clientului

**Rezolvare Iterativă**
- Serverul returnează cel mai bun răspuns cunoscut
- Clientul continuă să interogheze
- Folosită între servere DNS

> 🧪 **Experiment mental:** Dacă cache-ul DNS local expiră și serverul root este temporar inaccesibil, ce se întâmplă cu rezolvarea `google.com`?

### 2.3 Tipuri de Înregistrări DNS

| Tip | Scop | Exemplu Valoare |
|-----|------|-----------------|
| A | Adresă IPv4 | 93.184.216.34 |
| AAAA | Adresă IPv6 | 2606:2800:220:1:... |
| MX | Server de email | 10 mail.example.com |
| NS | Nameserver | ns1.example.com |
| CNAME | Alias | www → example.com |
| TXT | Text arbitrar | "v=spf1 include:..." |
| SOA | Început de autoritate | Parametri zonă |
| PTR | Rezolvare inversă | 34.216.184.93.in-addr.arpa |

### 2.4 Format Mesaj DNS

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                      ID                       |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    QDCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ANCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    NSCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ARCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                   Întrebare                   |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                   Răspuns                     |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

### 2.5 DNSSEC

DNSSEC adaugă semnături criptografice pentru a valida autenticitatea răspunsurilor:

- **RRSIG** - Semnătură digitală pentru înregistrări
- **DNSKEY** - Cheia publică pentru verificare
- **DS** - Delegare semnată (leagă zonele)
- **NSEC/NSEC3** - Demonstrează inexistența

---

## 3. Secure Shell (SSH)

### 3.1 Arhitectura pe Straturi

SSH este organizat în trei straturi:

**Stratul de Transport**
- Stabilește conexiunea TCP
- Negociază algoritmii de criptare
- Realizează schimbul de chei (Diffie-Hellman)
- Oferă confidențialitate și integritate

**Stratul de Autentificare**
- Verifică identitatea clientului
- Metode: parolă, cheie publică, GSSAPI
- Poate folosi autentificare multi-factor

**Stratul de Conexiune**
- Multiplexează canale logice
- Fiecare canal are un scop specific
- Gestionează controlul fluxului

### 3.2 Schimbul de Chei Diffie-Hellman

```
Client                                    Server
   |                                         |
   |---- p, g (parametri publici) ---------->|
   |                                         |
   |<--- Server public key (g^b mod p) ------|
   |                                         |
   |---- Client public key (g^a mod p) ----->|
   |                                         |
   |   Ambele părți calculează:              |
   |   Secret = (g^ab mod p)                 |
   |                                         |
   |========= Comunicație criptată ==========>|
```

### 3.3 Tipuri de Canale SSH

| Canal | Folosire | Port Implicit |
|-------|----------|---------------|
| session | Shell interactiv | - |
| direct-tcpip | Port forwarding local | - |
| forwarded-tcpip | Port forwarding remote | - |
| x11 | Forwarding X11 | 6000+ |
| auth-agent | Forwarding agent | - |

### 3.4 Port Forwarding

> 💡 **Analogie:** SSH tunneling este ca un tunel secret care trece prin munți (firewall). Vezi [Analogii Concepte](./analogii_concepte.md#8-ssh-tunneling-port-forwarding).

**Local Forwarding (-L)**
```
ssh -L 8080:server-intern:80 bastion
# Conexiunile la localhost:8080 ajung la server-intern:80
```

**Remote Forwarding (-R)**
```
ssh -R 9000:localhost:3000 server-public
# Conexiunile la server-public:9000 ajung la localhost:3000
```

**Dynamic Forwarding (-D)**
```
ssh -D 1080 server
# Creează un proxy SOCKS pe localhost:1080
```

---

## 4. Echilibrarea Sarcinii

### 4.1 Concepte Fundamentale

> 💡 **Analogie:** Load balancer = ospătar-șef care distribuie comenzile între bucătari. Vezi [Analogii Concepte](./analogii_concepte.md#1-load-balancer-echilibror-de-sarcină).

**Echiliborul de sarcină** distribuie traficul de intrare pe multiple servere backend pentru a:

- **Îmbunătăți disponibilitatea** - Dacă un server cade, altele preiau
- **Crește scalabilitatea** - Adaugă servere pentru mai mult trafic
- **Optimiza performanța** - Distribuie încărcarea uniform
- **Oferi flexibilitate** - Mentenanță fără downtime

### 4.2 Algoritmi de Distribuție

**Round Robin**
```python
def selecteaza_backend_round_robin(backends, index):
    backend = backends[index % len(backends)]
    return backend, index + 1
```
- Distribuție ciclică simplă
- Presupune servere identice
- Nu ține cont de încărcare

> 🤔 **Predicție:** Cu 3 backend-uri și round-robin, dacă trimiți 9 cereri, câte primește fiecare?

**Weighted Round Robin**
```python
# Ponderile reflectă capacitatea
backends = [
    {"server": "A", "weight": 5},  # 50% trafic
    {"server": "B", "weight": 3},  # 30% trafic
    {"server": "C", "weight": 2},  # 20% trafic
]
```

**Least Connections**
```python
def selecteaza_least_connections(backends):
    return min(backends, key=lambda b: b.conexiuni_active)
```
- Selectează serverul cel mai puțin încărcat
- Bun pentru cereri cu durată variabilă
- Necesită tracking conexiuni

**IP Hash**
```python
def selecteaza_ip_hash(backends, ip_client):
    hash_val = hash(ip_client)
    index = hash_val % len(backends)
    return backends[index]
```
- Același client → Același server
- Bun pentru aplicații cu stare
- Sesiuni persistente fără cookies

> 🤔 **Predicție:** Cu IP Hash și 3 backend-uri, dacă 100 de clienți diferiți fac câte o cerere, cum se va distribui traficul?

### 4.3 Verificări de Stare

> 💡 **Analogie:** Health check = doctor care verifică pulsul pacientului. Vezi [Analogii Concepte](./analogii_concepte.md#3-health-check).

**Verificări Pasive**
- Monitorizează răspunsurile reale
- Marchează serverul ca "down" după N eșecuri
- Nu adaugă trafic suplimentar

**Verificări Active**
- Trimite cereri periodice de test
- Endpoint dedicat: `/health` sau `/ping`
- Detectează probleme mai rapid

**Parametri Tipici**
```nginx
upstream backend {
    server web1:80 max_fails=3 fail_timeout=30s;
    server web2:80 max_fails=3 fail_timeout=30s;
    server web3:80 max_fails=3 fail_timeout=30s;
}
```

> 🧪 **Verifică înțelegerea:** Cu `max_fails=3` și `fail_timeout=30s`, cât timp durează până când un backend căzut este scos din rotație?

### 4.4 Nginx ca Echilibror

**Configurație Minimă**
```nginx
upstream backend_pool {
    server web1:80;
    server web2:80;
    server web3:80;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend_pool;
    }
}
```

**Configurație Avansată**
```nginx
upstream backend_pool {
    least_conn;  # Algoritm
    
    server web1:80 weight=3;
    server web2:80 weight=2;
    server web3:80 weight=1 backup;
    
    keepalive 32;  # Conexiuni persistente
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend_pool;
        
        # Header-e pentru backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
        
        # Failover
        proxy_next_upstream error timeout http_502 http_503;
    }
}
```

---

## 5. Referințe Bibliografice

1. Kurose, J. F. & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
2. Tanenbaum, A. S. & Wetherall, D. J. (2011). *Computer Networks* (5th ed.). Pearson.
3. Stevens, W. R. (2003). *UNIX Network Programming* (3rd ed.). Addison-Wesley.
4. RFC 959 - File Transfer Protocol
5. RFC 1035 - Domain Names - Implementation and Specification
6. RFC 4251-4254 - Secure Shell Protocol
7. Nginx Documentation - https://nginx.org/en/docs/

---

## Navigare Rapidă

- [← Înapoi la README](../README.md)
- [Comenzi Utile →](./commands_cheatsheet.md)
- [Depanare →](./troubleshooting.md)
- [Glosar →](./glosar.md)

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
