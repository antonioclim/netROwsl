# Analogii pentru Concepte Cheie — Metoda CPA

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix
>
> Acest document prezintă fiecare concept tehnic folosind metoda 
> Concret → Pictorial → Abstract pentru învățare progresivă.

---

## 1. Load Balancer (Echilibror de Sarcină)

### 🎯 CONCRET

Imaginează-ți un **ospătar-șef într-un restaurant** cu 3 bucătari.
Când vine o comandă, ospătarul-șef nu o dă mereu aceluiași bucătar.
El distribuie comenzile astfel încât niciunul să nu fie supraîncărcat.

- Dacă bucătarul A are 5 comenzi și B are 2, noua comandă merge la B
- Dacă un bucătar pleacă în pauză, ospătarul nu-i mai trimite comenzi
- Clienții nu știu care bucătar le-a gătit mâncarea — doar primesc farfuria

### 📊 PICTORIAL

```
   Clienți
     │
     ▼
┌─────────────┐
│ OSPĂTAR-ȘEF │ ◄── Load Balancer (nginx)
│   (nginx)   │
└──────┬──────┘
       │
   ┌───┼───┐
   ▼   ▼   ▼
 ┌───┬───┬───┐
 │ A │ B │ C │ ◄── Backend-uri (bucătari)
 └───┴───┴───┘
```

### 💻 ABSTRACT

```yaml
upstream backend_pool {
    server web1:80;  # Bucătar A
    server web2:80;  # Bucătar B  
    server web3:80;  # Bucătar C
}
```

---

## 2. DNS Cache

### 🎯 CONCRET

DNS cache este ca **agenda ta de telefon**.
Prima dată când suni pe Maria, cauți numărul în cartea de telefon (server DNS).
Apoi îl salvezi în agendă. Data viitoare, nu mai cauți în carte — deschizi direct agenda.

- Dacă Maria își schimbă numărul, agenda ta e "expirată"
- TTL = cât timp ții numărul în agendă înainte de a verifica din nou

### 📊 PICTORIAL

```
Prima cerere:                    A doua cerere:
                                
Tu ──► DNS Server ──► Răspuns    Tu ──► Cache local ──► Răspuns
       (cartea de telefon)              (agenda ta)
       ~100ms                           ~1ms
```

### 💻 ABSTRACT

```python
cache = {}
ttl = 300  # 5 minute

def resolve(domain):
    if domain in cache and not expired(cache[domain]):
        return cache[domain]  # Din agendă
    else:
        result = query_dns_server(domain)  # Din cartea de telefon
        cache[domain] = result
        return result
```

---

## 3. Health Check

### 🎯 CONCRET

Health check-ul este ca un **doctor care verifică pulsul pacientului**.
La fiecare 10 secunde, doctorul întreabă: "Ești OK?"

- Dacă pacientul răspunde "Da" → e sănătos, poate primi vizitatori
- Dacă nu răspunde de 3 ori → e "nesănătos", nu mai primește vizitatori
- Când începe să răspundă din nou → după 2 răspunsuri OK, e iar sănătos

### 📊 PICTORIAL

```
   Doctor (nginx)
        │
        │ "Ești OK?" la fiecare 10s
        ▼
   ┌─────────┐
   │ Backend │──► "200 OK" = sănătos ✓
   └─────────┘    timeout  = nesănătos ✗
   
   3× nesănătos → scos din rotație
   2× sănătos   → readăugat
```

### 💻 ABSTRACT

```yaml
healthcheck:
  test: ["CMD", "wget", "-q", "--spider", "http://localhost/health"]
  interval: 10s      # La fiecare 10 secunde
  timeout: 5s        # Așteaptă max 5 secunde
  retries: 3         # 3 eșecuri = nesănătos
```

---

## 4. Port Mapping

### 🎯 CONCRET

Port mapping este ca **sistemul de apartamente dintr-un bloc**.
Adresa blocului este `localhost` (strada principală).
Fiecare apartament are un număr (port).

- Vizitatorii vin la adresa blocului (localhost:8080)
- Portarul îi direcționează la apartamentul corect (container:80)
- Apartamentul 8080 al blocului duce la apartamentul 80 din container

### 📊 PICTORIAL

```
Din Windows:                În container:
                           
localhost:8080 ────────────► container:80
    │                            │
    │ "Vreau apt 8080"          │ "Aici e apt 80"
    ▼                            ▼
┌─────────┐               ┌─────────┐
│  BLOC   │──── port ────►│ APART.  │
│(Docker) │    mapping    │(nginx)  │
└─────────┘               └─────────┘
```

### 💻 ABSTRACT

```yaml
ports:
  - "8080:80"   # bloc:apartament
  # Vizitatorii la 8080 ajung în container la 80
```

---

## 5. Docker Network Bridge

### 🎯 CONCRET

O rețea Docker bridge este ca o **stradă privată într-un cartier închis**.

- Casele (containerele) de pe aceeași stradă se pot vizita între ele
- Case de pe străzi diferite NU se pot vizita direct
- Fiecare casă are adresă proprie pe stradă (IP intern)

### 📊 PICTORIAL

```
┌─────────────────────────────────────┐
│        Cartier s11_network          │
│  ┌─────┐   ┌─────┐   ┌─────┐       │
│  │web1 │◄─►│web2 │◄─►│nginx│       │
│  │.2   │   │.3   │   │.4   │       │
│  └─────┘   └─────┘   └─────┘       │
│         172.28.0.0/16              │
└─────────────────────────────────────┘
         │
         ✗ nu poate accesa
         │
┌─────────────────────────────────────┐
│       Alt cartier (altă rețea)      │
└─────────────────────────────────────┘
```

### 💻 ABSTRACT

```yaml
networks:
  s11_net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

---

## 6. Round Robin vs Least Connections

### 🎯 CONCRET

**Round Robin** = **Roata cu cifre la tombolă**
- Bila cade pe 1, apoi 2, apoi 3, apoi iar 1
- Nu contează cât de ocupat e fiecare
- Simplu, previzibil

**Least Connections** = **Casa de bilete cu mai multe ghișee**
- Clientul merge la ghișeul cu cea mai scurtă coadă
- Adaptiv la încărcare
- Mai eficient când cererile durează diferit

### 📊 PICTORIAL

```
Round Robin:              Least Connections:
                         
Cereri: 1→2→3→1→2→3      Cereri: → cel mai liber
                         
 B1: ████                  B1: ██████
 B2: ████                  B2: ██
 B3: ████                  B3: ████
 (egal întotdeauna)        (echilibrează după coadă)
```

### 💻 ABSTRACT

```nginx
# Round Robin (implicit)
upstream backend {
    server web1:80;
    server web2:80;
    server web3:80;
}

# Least Connections
upstream backend {
    least_conn;
    server web1:80;
    server web2:80;
    server web3:80;
}
```

---

## 7. FTP Activ vs Pasiv

### 🎯 CONCRET

**FTP Activ** = Tu îi dai cuiva adresa ta și **el vine la tine**
- "Eu stau la adresa X, vino să-mi aduci fișierul"
- Problemă: dacă stai într-un bloc cu interfon (NAT), nu poate intra

**FTP Pasiv** = Tu **te duci la el** să iei fișierul
- "Dă-mi adresa ta, vin eu să iau fișierul"
- Funcționează chiar dacă tu ești în spatele unui NAT

### 📊 PICTORIAL

```
ACTIV:                      PASIV:
                           
Client ◄──── Server         Client ────► Server
 (eu)    "vin la tine"       (eu)    "vin eu"
   │          │                │          │
 [NAT]      [OK]             [NAT]      [OK]
   ✗ blocat                    ✓ funcționează
```

### 💻 ABSTRACT

```
ACTIV:  PORT 192,168,1,5,78,32  → Server conectează la client
PASIV:  PASV                     → Client conectează la server

# Aproape toate clienții moderni folosesc PASV implicit
```

---

## 8. SSH Tunneling (Port Forwarding)

### 🎯 CONCRET

SSH tunneling este ca un **tunel secret** care trece prin munți (firewall).

**Local Forwarding (-L):** Faci o gaură din camera ta către o cameră îndepărtată
- Intri pe ușa ta locală, ieși în camera îndepărtată

**Remote Forwarding (-R):** Faci o gaură din camera îndepărtată către tine
- Cineva intră pe ușa lor îndepărtată, iese în camera ta

### 📊 PICTORIAL

```
Local Forwarding (-L 8080:db:5432 bastion):

  [Tu]                    [Bastion]              [DB Server]
    │                         │                       │
localhost:8080 ══════════════►│═══════════════════► db:5432
    │         SSH Tunnel      │                       │
    └─────────────────────────┴───────────────────────┘
              Firewall      

Tu te conectezi la localhost:8080, dar ajungi la db:5432
```

### 💻 ABSTRACT

```bash
# Local: conectează-te local, ieși remote
ssh -L 8080:database:5432 bastion
# localhost:8080 → database:5432

# Remote: conectează-te remote, ieși local  
ssh -R 9000:localhost:3000 server
# server:9000 → localhost:3000

# Dynamic: proxy SOCKS
ssh -D 1080 server
# Toate conexiunile prin localhost:1080 ies prin server
```

---

## 9. Upstream și Proxy Pass

### 🎯 CONCRET

**Upstream** = Lista de furnizori pe care ospătarul-șef îi cunoaște
**Proxy Pass** = Regula "trimite comanda la unul dintre furnizori"

E ca un **call center** cu mai mulți operatori:
- Upstream = Lista operatorilor disponibili
- Proxy Pass = "Orice apel primit, trimite-l la un operator din listă"

### 📊 PICTORIAL

```
           Cerere HTTP
               │
               ▼
┌──────────────────────────┐
│     nginx (call center)  │
│                          │
│  proxy_pass              │
│  http://backend_pool ────┼──┐
│                          │  │
└──────────────────────────┘  │
                              │
              ┌───────────────┘
              ▼
┌──────────────────────────┐
│    upstream backend_pool │
│    ┌─────┬─────┬─────┐  │
│    │web1 │web2 │web3 │  │ ◄── Operatori
│    └─────┴─────┴─────┘  │
└──────────────────────────┘
```

### 💻 ABSTRACT

```nginx
# Definește lista de servere
upstream backend_pool {
    server web1:80;
    server web2:80;
    server web3:80;
}

server {
    listen 80;
    
    location / {
        # Trimite cererea la unul din servere
        proxy_pass http://backend_pool;
    }
}
```

---

## Cum să Folosești Acest Document

1. **Când întâlnești un concept nou:** Citește mai întâi secțiunea CONCRET
2. **Când vrei să vizualizezi:** Studiază diagrama PICTORIAL
3. **Când ești gata să implementezi:** Treci la codul ABSTRACT

**Sfat:** Întoarce-te la analogia concretă când ceva nu funcționează cum te aștepți. Întreabă-te: "În restaurantul meu imaginar, ce s-ar întâmpla?"

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
