# Teme pentru Acasă — Săptămâna 8

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix
>
> **Vezi și:** [README principal](../README.md) | [Exerciții de laborator](../src/exercises/)

---

## Prezentare Generală

Acest director conține temele pentru acasă pentru Săptămâna 8. Fiecare temă se bazează pe conceptele acoperite în exercițiile de laborator și necesită implementare independentă.

**🔮 PREDICȚIE înainte de a începe:** Cât timp estimezi că îți va lua fiecare temă? Notează estimarea și compară la final cu timpul real.

---

## Tema 1: Server HTTPS cu TLS

**Fișier:** `exercises/tema_8_01_server_https.py`

**Durată estimată:** 90-120 minute

**Punctaj:** 100 puncte

### Descriere

Extindeți serverul HTTP de bază pentru a suporta conexiuni HTTPS folosind TLS (Transport Layer Security).

### 💡 De la Concret la Abstract: TLS Handshake

**CONCRET:**
> Imaginează-ți că vrei să trimiți o scrisoare secretă unui prieten.
> 1. Îi ceri o copie a lacătului său deschis (certificat public)
> 2. Pui scrisoarea într-o cutie și o încui cu lacătul lui
> 3. Doar el are cheia să o deschidă (cheia privată)
> 
> TLS face exact asta, dar pentru date de rețea.

**ABSTRACT:**
```python
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
secure_socket = context.wrap_socket(socket, server_side=True)
```

### Cerințe

1. **Generare certificat** (20 puncte)
   - Generați un certificat auto-semnat folosind OpenSSL
   - Salvați certificatul și cheia în directorul `certs/`

2. **Implementare TLS** (30 puncte)
   - Folosiți modulul `ssl` din Python
   - Configurați context SSL cu TLS 1.2 sau mai nou
   - Gestionați corect erorile de handshake

3. **Server dual-port** (20 puncte)
   - HTTP pe portul 8080
   - HTTPS pe portul 8443
   - Ambele servere rulează simultan

4. **Gestionare erori** (15 puncte)
   - Tratați erorile de certificat
   - Logați conexiunile și erorile

5. **Calitatea codului** (15 puncte)
   - Documentație adecvată
   - Cod clar și organizat

### Testare

**🔮 PREDICȚIE:** Ce diferență vei observa în Wireshark între traficul HTTP și HTTPS?

```bash
# Generare certificat
mkdir -p certs
openssl req -x509 -newkey rsa:4096 \
    -keyout certs/key.pem \
    -out certs/cert.pem \
    -days 365 -nodes \
    -subj "/CN=localhost"

# Pornire server
python3 exercises/tema_8_01_server_https.py

# Testare HTTP
curl http://localhost:8080/

# Testare HTTPS (ignorare verificare certificat)
curl -k https://localhost:8443/
```

**Verificare:** Ambele cereri returnează același conținut? HTTPS-ul afișează warning despre certificat?

---

## Tema 2: Echilibrator de Încărcare cu Ponderi

**Fișier:** `exercises/tema_8_02_echilibrator_ponderat.py`

**Durată estimată:** 120-150 minute

**Punctaj:** 100 puncte

### Descriere

Implementați un echilibrator de încărcare weighted round-robin cu verificare a stării de sănătate și failover automat.

### 💡 De la Concret la Abstract: Weighted Round-Robin

**CONCRET:**
> Imaginează-ți 3 ospătari într-un restaurant:
> - Ospătarul A (experimentat): primește 5 mese
> - Ospătarul B (mediu): primește 3 mese
> - Ospătarul C (nou): primește 1 masă
> 
> Din 9 clienți, A servește 5, B servește 3, C servește 1.

**PICTORIAL:**
```
Cereri: ①②③④⑤⑥⑦⑧⑨

Distribuție (5:3:1):
Backend A (w=5): ① ② ③ ④ ⑤
Backend B (w=3): ⑥ ⑦ ⑧
Backend C (w=1): ⑨
```

**ABSTRACT:**
```python
BACKEND_CONFIG = {
    ("127.0.0.1", 8001): {"weight": 5},
    ("127.0.0.1", 8002): {"weight": 3},
    ("127.0.0.1", 8003): {"weight": 1},
}
```

### Cerințe

1. **Algoritm weighted round-robin** (35 puncte)
   - Distribuție proporțională cu ponderile configurate
   - Implementare smooth weighted round-robin
   - Configurație flexibilă a ponderilor

2. **Verificare sănătate** (25 puncte)
   - Verificări periodice ale backend-urilor
   - Endpoint configurabil pentru verificare
   - Timeout pentru cereri de sănătate

3. **Failover automat** (20 puncte)
   - Eliminare backend-uri nesănătoase
   - Reintroducere automată când revin online
   - Redistribuire încărcare

4. **Statistici** (10 puncte)
   - Numărare cereri per backend
   - Timp mediu de răspuns
   - Rata de succes/eroare

5. **Calitatea codului** (10 puncte)
   - Documentație adecvată
   - Cod clar și organizat

### Configurație exemplu

```python
BACKEND_CONFIG = {
    ("127.0.0.1", 8001): {"weight": 5, "name": "Primary"},
    ("127.0.0.1", 8002): {"weight": 3, "name": "Secondary"},
    ("127.0.0.1", 8003): {"weight": 1, "name": "Backup"},
}
```

### Testare

**🔮 PREDICȚIE:** Din 18 cereri cu ponderi 5:3:1, câte va primi fiecare backend?

```bash
# Porniți 3 backend-uri
python3 -m http.server 8001 --directory ../www/ &
python3 -m http.server 8002 --directory ../www/ &
python3 -m http.server 8003 --directory ../www/ &

# Porniți echilibratorul
python3 exercises/tema_8_02_echilibrator_ponderat.py

# Testare distribuție
for i in {1..18}; do curl -s http://localhost:8000/ >/dev/null; done

# Verificați statisticile în output-ul echilibratorului
```

**Verificare:** Distribuția este aproximativ 10:6:2 (5:3:1 × 2)?

### 👥 Exercițiu Pair Programming Opțional

Implementați tema împreună cu un coleg:
- **Driver A:** Implementează weighted round-robin
- **Navigator A:** Verifică corectitudinea algoritmului
- **Schimbare roluri**
- **Driver B:** Implementează health check și failover
- **Navigator B:** Testează edge cases

---

## Resurse

### Documentație Python
- [Modulul ssl](https://docs.python.org/3/library/ssl.html)
- [Modulul socket](https://docs.python.org/3/library/socket.html)
- [Modulul threading](https://docs.python.org/3/library/threading.html)

### Comenzi OpenSSL
```bash
# Generare certificat auto-semnat
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Verificare certificat
openssl x509 -in cert.pem -text -noout

# Testare conexiune TLS
openssl s_client -connect localhost:8443
```

### Algoritmi de echilibrare
- Round-robin simplu: 1→2→3→1→2→3
- Round-robin ponderat: distribuție proporțională
- Smooth weighted round-robin: distribuție uniformă în timp
- Least connections: către cel mai puțin încărcat

---

## Reguli de Predare

1. Predați fișierele Python completate
2. Includeți instrucțiuni de rulare în comentarii
3. Documentați orice dependențe suplimentare
4. Testați înainte de predare
5. **Opțional:** Includeți capturi Wireshark relevante

## Politica de Integritate Academică

Temele trebuie să reprezinte munca proprie. Colaborarea pentru înțelegerea conceptelor este permisă, dar codul trebuie scris individual.

## Checklist Pre-Predare

- [ ] Codul rulează fără erori
- [ ] Toate funcțiile TODO sunt implementate
- [ ] Testele de bază trec
- [ ] Documentația este completă
- [ ] Comentariile explică logica complexă

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
