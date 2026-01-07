# Săptămâna 10: Nivelul Aplicație - HTTP/S, REST și Servicii de Rețea

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
> 
> by Revolvix

## Prezentare Generală

Această sesiune de laborator explorează **nivelul aplicație** al stivei TCP/IP, concentrându-se pe protocoalele fundamentale care susțin comunicarea modernă în Internet. Studenții vor examina mecanismele interne ale HTTP și HTTPS, vor înțelege principiile arhitecturale REST și vor interacționa direct cu serviciile de rețea esențiale: DNS, SSH și FTP.

Mediul de laborator utilizează containere Docker orchestrate pentru a simula o infrastructură de rețea realistă. Fiecare serviciu rulează izolat, permițând analiza traficului de rețea fără interferențe externe. Această abordare oferă un spațiu sigur pentru experimentare cu protocoale și configurații.

Competențele dobândite în această sesiune sunt direct aplicabile în dezvoltarea aplicațiilor web, administrarea sistemelor și securitatea rețelelor. Înțelegerea profundă a acestor protocoale constituie fundamentul pentru arhitecturile distribuite moderne.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** componentele principale ale unei cereri și răspuns HTTP, incluzând metodele, headerele și codurile de stare
2. **Explicați** diferențele dintre HTTP și HTTPS, descriind rolul TLS în securizarea comunicației
3. **Implementați** un server REST simplu care demonstrează nivelurile de maturitate Richardson (0-3)
4. **Analizați** traficul DNS folosind instrumente de captură, interpretând structura mesajelor de interogare și răspuns
5. **Comparați** modurile de transfer FTP (activ vs. pasiv) și implicațiile lor pentru traversarea firewall-urilor
6. **Evaluați** securitatea relativă a diferitelor protocoale de nivel aplicație

## Cerințe Preliminare

### Cunoștințe Necesare
- Fundamentele modelului TCP/IP și ale comunicării client-server
- Experiență de bază cu linia de comandă Linux/Windows
- Noțiuni elementare de programare Python
- Familiaritate cu conceptul de containere Docker

### Cerințe Software
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git (opțional, pentru versionare)

### Cerințe Hardware
- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate de rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK10_WSLkit_RO

# Verificați cerințele preliminare
python setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```powershell
# Porniți toate serviciile
python scripts/porneste_lab.py

# Verificați starea serviciilor
python scripts/porneste_lab.py --stare
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se setează la prima accesare |
| Server Web | http://localhost:8000 | - |
| Server DNS | localhost:5353/udp | - |
| Server SSH | localhost:2222 | labuser / labpass |
| Server FTP | localhost:2121 | labftp / labftp |

## Exerciții de Laborator

### Exercițiul 1: Explorarea Serviciului HTTP

**Obiectiv:** Înțelegerea structurii cererilor și răspunsurilor HTTP prin interacțiune directă cu serverul web containerizat.

**Durată estimată:** 20 minute

**Pași:**

1. Verificați că serverul web rulează:
   ```bash
   curl -v http://localhost:8000/
   ```

2. Observați headerele răspunsului:
   - `Content-Type` - tipul MIME al conținutului
   - `Content-Length` - dimensiunea în octeți
   - `Server` - identificarea serverului

3. Testați diferite metode HTTP:
   ```bash
   # Cerere HEAD (doar headere, fără corp)
   curl -I http://localhost:8000/hello.txt
   
   # Cerere cu header personalizat
   curl -H "Accept-Language: ro" http://localhost:8000/
   ```

4. Folosiți containerul debug pentru teste din interiorul rețelei:
   ```bash
   docker exec -it week10_debug curl http://web:8000/
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 1
```

**Ce trebuie observat:**
- Corelația dintre codul de stare HTTP și succesul operației
- Diferența dintre cererile din exterior (localhost) și interior (numele containerului)

---

### Exercițiul 2: Rezoluția DNS

**Obiectiv:** Analiza procesului de rezoluție DNS folosind serverul DNS personalizat și instrumentele de diagnosticare.

**Durată estimată:** 15 minute

**Pași:**

1. Interogați serverul DNS pentru înregistrările configurate:
   ```bash
   # Din containerul debug
   docker exec -it week10_debug dig @dns-server -p 5353 web.lab.local
   
   # Din sistemul gazdă
   dig @localhost -p 5353 myservice.lab.local
   ```

2. Testați rezoluția pentru toate domeniile configurate:
   - `myservice.lab.local` → 10.10.10.10
   - `api.lab.local` → 10.10.10.20
   - `web.lab.local` → 172.20.0.10
   - `ssh.lab.local` → 172.20.0.22
   - `ftp.lab.local` → 172.20.0.21

3. Observați răspunsul pentru un domeniu inexistent:
   ```bash
   dig @localhost -p 5353 inexistent.lab.local
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 2
```

**Ce trebuie observat:**
- Structura răspunsului DNS (secțiunile QUESTION, ANSWER, AUTHORITY)
- Codul de răspuns pentru domenii inexistente (NXDOMAIN)

---

### Exercițiul 3: Comunicația SSH Criptată

**Obiectiv:** Demonstrarea comunicației securizate prin SSH și analiza procesului de autentificare.

**Durată estimată:** 15 minute

**Pași:**

1. Conectați-vă la serverul SSH din linia de comandă:
   ```bash
   ssh -p 2222 labuser@localhost
   # Parolă: labpass
   ```

2. Executați comenzi pe serverul remote:
   ```bash
   whoami
   hostname
   ls -la
   exit
   ```

3. Rulați demonstrația Paramiko din container:
   ```bash
   docker exec -it week10_ssh_client python /app/paramiko_client.py
   ```

4. Sau rulați scriptul local:
   ```bash
   python src/apps/demo_ssh.py
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 3
```

**Ce trebuie observat:**
- Avertismentul despre cheia gazdei la prima conectare
- Imposibilitatea de a citi conținutul traficului SSH în Wireshark (criptat)

---

### Exercițiul 4: Protocolul FTP Multi-Canal

**Obiectiv:** Înțelegerea separării între canalul de control și canalul de date în FTP.

**Durată estimată:** 15 minute

**Pași:**

1. Conectați-vă la serverul FTP:
   ```bash
   # Folosind clientul ftp integrat
   ftp localhost 2121
   # Utilizator: labftp
   # Parolă: labftp
   ```

2. Executați comenzi FTP de bază:
   ```ftp
   pwd
   ls
   passive
   ls
   quit
   ```

3. Rulați demonstrația Python:
   ```bash
   python src/apps/demo_ftp.py
   ```

4. Din containerul debug, folosiți lftp:
   ```bash
   docker exec -it week10_debug lftp -u labftp,labftp ftp-server:2121
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 4
```

**Ce trebuie observat:**
- Diferența între modul activ și pasiv
- Porturile utilizate pentru canalul de date (30000-30009)

---

### Exercițiul 5: HTTPS cu TLS Auto-Semnat

**Obiectiv:** Implementarea unui server HTTPS cu certificat auto-semnat și înțelegerea negocierii TLS.

**Durată estimată:** 25 minute

**Pași:**

1. Rulați exercițiul HTTPS:
   ```bash
   python src/exercises/ex_10_01_https.py
   ```

2. Într-un alt terminal, testați serverul:
   ```bash
   # Cerere HTTPS (ignorând validarea certificatului)
   curl -k https://localhost:4443/
   
   # Vizualizați informațiile certificatului
   curl -kv https://localhost:4443/ 2>&1 | grep -A 10 "Server certificate"
   ```

3. Testați operațiile CRUD:
   ```bash
   # CREATE
   curl -k -X POST -H "Content-Type: application/json" \
        -d '{"nume": "Test", "valoare": 42}' \
        https://localhost:4443/api/resurse
   
   # READ
   curl -k https://localhost:4443/api/resurse
   
   # UPDATE
   curl -k -X PUT -H "Content-Type: application/json" \
        -d '{"nume": "Actualizat", "valoare": 100}' \
        https://localhost:4443/api/resurse/1
   
   # DELETE
   curl -k -X DELETE https://localhost:4443/api/resurse/1
   ```

4. Rulați modul de auto-testare:
   ```bash
   python src/exercises/ex_10_01_https.py --selftest
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 5
```

**Ce trebuie observat:**
- Avertismentul browserului pentru certificatele auto-semnate
- Structura handshake-ului TLS în Wireshark

---

### Exercițiul 6: Nivelurile de Maturitate REST

**Obiectiv:** Compararea diferitelor niveluri ale modelului de maturitate Richardson pentru API-uri REST.

**Durată estimată:** 30 minute

**Pași:**

1. Porniți serverul Flask cu toate nivelurile:
   ```bash
   python src/exercises/ex_10_02_rest_levels.py
   ```

2. Testați Nivelul 0 (RPC prin HTTP):
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"actiune": "listeaza"}' \
        http://localhost:5000/api/nivel0
   
   curl -X POST -H "Content-Type: application/json" \
        -d '{"actiune": "creeaza", "date": {"nume": "Produs"}}' \
        http://localhost:5000/api/nivel0
   ```

3. Testați Nivelul 1 (Resurse):
   ```bash
   curl http://localhost:5000/api/nivel1/produse
   curl -X POST -H "Content-Type: application/json" \
        -d '{"nume": "Laptop"}' \
        http://localhost:5000/api/nivel1/produse
   ```

4. Testați Nivelul 2 (Verbe HTTP):
   ```bash
   curl http://localhost:5000/api/nivel2/produse
   curl -X POST -H "Content-Type: application/json" \
        -d '{"nume": "Monitor"}' \
        http://localhost:5000/api/nivel2/produse
   curl -X PUT -H "Content-Type: application/json" \
        -d '{"nume": "Monitor 4K"}' \
        http://localhost:5000/api/nivel2/produse/1
   curl -X DELETE http://localhost:5000/api/nivel2/produse/1
   ```

5. Testați Nivelul 3 (HATEOAS):
   ```bash
   curl http://localhost:5000/api/nivel3/produse
   # Observați linkurile _links în răspuns
   ```

6. Rulați auto-testarea:
   ```bash
   python src/exercises/ex_10_02_rest_levels.py --selftest
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 6
```

**Ce trebuie observat:**
- Evoluția de la un singur endpoint (L0) la resurse cu linkuri (L3)
- Utilizarea corectă a codurilor de stare HTTP la fiecare nivel

---

## Demonstrații

### Demonstrație 1: Tur Complet al Serviciilor

Demonstrație automată care prezintă toate serviciile din laborator:

```powershell
python scripts/ruleaza_demo.py --demo 1
```

**Ce se va observa:**
- Pornirea și verificarea tuturor containerelor
- Teste de conectivitate pentru fiecare serviciu
- Exemple de interacțiune cu HTTP, DNS, SSH și FTP

### Demonstrație 2: Comparație REST

```powershell
python scripts/ruleaza_demo.py --demo 2
```

**Ce se va observa:**
- Diferențele vizuale între nivelurile de maturitate REST
- Evoluția răspunsurilor de la RPC la HATEOAS

---

## Captură și Analiză de Trafic

### Capturarea Traficului

```powershell
# Pornire captură
python scripts/captura_trafic.py --interfata eth0 --iesire pcap/week10_captura.pcap

# Sau folosiți Wireshark direct
# Deschideți Wireshark > Selectați interfața Docker sau "\\.\pipe\docker_engine"
```

### Filtre Wireshark Recomandate

```
# Trafic HTTP
http or tcp.port == 8000

# Trafic DNS
udp.port == 5353

# Trafic SSH
tcp.port == 2222 or tcp.port == 22

# Trafic FTP (control și date)
tcp.port == 2121 or tcp.portrange == 30000-30009

# Trafic HTTPS/TLS
tcp.port == 4443 or tls

# Doar traficul din rețeaua laboratorului
ip.addr == 172.20.0.0/24
```

---

## Oprire și Curățare

### La Sfârșitul Sesiunii

```powershell
# Oprirea containerelor (păstrează datele)
python scripts/opreste_lab.py

# Verificare oprire
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Elimină toate containerele, rețelele și volumele acestei săptămâni
python scripts/curata.py --complet

# Verificare curățare
docker system df
```

---

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de realizat acasă.

### Tema 1: Server DNS Extins
Extindeți serverul DNS pentru a suporta înregistrări MX și CNAME.

### Tema 2: Client REST Complet
Implementați un client Python care interacționează cu toate cele 4 niveluri REST.

---

## Depanare

### Probleme Frecvente

#### Problema: Containerele nu pornesc
**Soluție:** Verificați că Docker Desktop rulează și are suficientă memorie alocată (minim 4GB pentru WSL2).

```powershell
# Verificați starea Docker
docker info

# Reporniți Docker Desktop dacă este necesar
```

#### Problema: Porturile sunt ocupate
**Soluție:** Identificați și opriți procesele care utilizează porturile necesare.

```powershell
# Verificați ce folosește portul 8000
netstat -ano | findstr :8000

# Opriți procesul cu PID-ul găsit
taskkill /PID <pid> /F
```

#### Problema: Eroare de conectare SSH "Host key verification failed"
**Soluție:** Ștergeți vechea cheie din known_hosts.

```bash
ssh-keygen -R "[localhost]:2222"
```

#### Problema: Certificatul HTTPS nu este acceptat
**Soluție:** Pentru certificate auto-semnate, folosiți flag-ul `-k` cu curl sau acceptați excepția în browser.

Consultați `docs/depanare.md` pentru mai multe soluții.

---

## Fundamente Teoretice

### Protocolul HTTP/HTTPS

HTTP (Hypertext Transfer Protocol) operează la nivelul aplicație, folosind TCP ca transport. Structura unei cereri include: linia de cerere (metodă, URI, versiune), headere și opțional un corp. HTTPS adaugă un strat TLS/SSL pentru criptare, autentificare și integritate.

### Modelul REST

REST (Representational State Transfer) definește un stil arhitectural pentru sisteme distribuite. Modelul de maturitate Richardson clasifică API-urile în 4 niveluri:
- **Nivelul 0:** HTTP ca tunel pentru RPC
- **Nivelul 1:** Resurse individuale cu URI-uri distincte
- **Nivelul 2:** Utilizarea corectă a verbelor HTTP
- **Nivelul 3:** HATEOAS - hypermedia ca motor al stării aplicației

### Protocolul DNS

DNS (Domain Name System) traduce nume de domenii în adrese IP. Mesajele DNS conțin secțiuni pentru întrebare, răspuns, autoritate și informații adiționale. Tipurile comune de înregistrări includ A (IPv4), AAAA (IPv6), MX (mail) și CNAME (alias).

### Protocolul SSH

SSH (Secure Shell) oferă comunicație criptată pentru acces remote. Arhitectura include trei straturi: transport (criptare, integritate), autentificare utilizator și conexiune (multiplexare canale).

### Protocolul FTP

FTP (File Transfer Protocol) utilizează două conexiuni separate: canalul de control (port 21) pentru comenzi și canalul de date pentru transferuri. Modul pasiv rezolvă problemele de traversare a firewall-urilor prin inițierea conexiunii de date de către client.

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. Doctoral dissertation, University of California, Irvine.
- RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1
- RFC 8446 - The Transport Layer Security (TLS) Protocol Version 1.3
- RFC 1035 - Domain Names - Implementation and Specification
- RFC 4253 - The Secure Shell (SSH) Transport Layer Protocol
- RFC 959 - File Transfer Protocol

---

## Diagrama Arhitecturii

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Rețeaua Laboratorului Week 10                     │
│                      week10_labnet (172.20.0.0/24)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   web       │  │ dns-server  │  │ ssh-server  │  │ ftp-server  │ │
│  │ 172.20.0.10 │  │ 172.20.0.53 │  │ 172.20.0.22 │  │ 172.20.0.21 │ │
│  │   :8000     │  │  :5353/udp  │  │    :22      │  │   :2121     │ │
│  │  (HTTP)     │  │   (DNS)     │  │   (SSH)     │  │   (FTP)     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │                │        │
│         └────────────────┴────────────────┴────────────────┘        │
│                                   │                                  │
│  ┌─────────────┐  ┌─────────────┐ │                                  │
│  │ ssh-client  │  │   debug     │ │                                  │
│  │172.20.0.100 │  │172.20.0.200 │ │                                  │
│  │ (Paramiko)  │  │(dig,curl,..)│ │                                  │
│  └─────────────┘  └─────────────┘ │                                  │
│                                   │                                  │
├───────────────────────────────────┼──────────────────────────────────┤
│                          Docker Host                                 │
│                                   │                                  │
│    Porturi expuse:  8000 ←───────┤                                  │
│                     5353/udp ←────┤                                  │
│                     2222 ←────────┤                                  │
│                     2121 ←────────┤                                  │
│                     9443 (Portainer)                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
