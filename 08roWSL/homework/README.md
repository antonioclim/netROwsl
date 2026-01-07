# Teme pentru Acasă — Săptămâna 8

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Prezentare Generală

Acest director conține temele pentru acasă pentru Săptămâna 8. Fiecare temă se bazează pe conceptele acoperite în exercițiile de laborator și necesită implementare independentă.

## Tema 1: Server HTTPS cu TLS

**Fișier:** `exercises/tema_8_01_server_https.py`

**Durată estimată:** 90-120 minute

**Punctaj:** 100 puncte

### Descriere

Extindeți serverul HTTP de bază pentru a suporta conexiuni HTTPS folosind TLS (Transport Layer Security).

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

```bash
# Generare certificat
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes

# Pornire server
python exercises/tema_8_01_server_https.py

# Testare HTTP
curl http://localhost:8080/

# Testare HTTPS (ignorare verificare certificat)
curl -k https://localhost:8443/
```

---

## Tema 2: Echilibrator de Încărcare cu Ponderi

**Fișier:** `exercises/tema_8_02_echilibrator_ponderat.py`

**Durată estimată:** 120-150 minute

**Punctaj:** 100 puncte

### Descriere

Implementați un echilibrator de încărcare weighted round-robin cu verificare a stării de sănătate și failover automat.

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
BACKEND_URI = {
    ("127.0.0.1", 8001): {"pondere": 5, "nume": "Primary"},
    ("127.0.0.1", 8002): {"pondere": 3, "nume": "Secondary"},
    ("127.0.0.1", 8003): {"pondere": 1, "nume": "Backup"},
}
```

### Testare

```bash
# Porniți 3 backend-uri
python -m http.server 8001 --directory www/ &
python -m http.server 8002 --directory www/ &
python -m http.server 8003 --directory www/ &

# Porniți echilibratorul
python exercises/tema_8_02_echilibrator_ponderat.py

# Testare distribuție (ar trebui să fie aproximativ 5:3:1)
for i in {1..18}; do curl -s http://localhost:8000/ >/dev/null; done

# Verificați statisticile în output-ul echilibratorului
```

---

## Resurse

### Documentație Python
- [Modulul ssl](https://docs.python.org/3/library/ssl.html)
- [Modulul socket](https://docs.python.org/3/library/socket.html)
- [Modulul threading](https://docs.python.org/3/library/threading.html)

### Tutoriale OpenSSL
- Generare certificat auto-semnat
- Formatul PEM

### Algoritmi de echilibrare
- Round-robin ponderat
- Smooth weighted round-robin
- Verificare sănătate (health checking)

---

## Reguli de Predare

1. Predați fișierele Python completate
2. Includeți instrucțiuni de rulare
3. Documentați orice dependențe suplimentare
4. Testați înainte de predare

## Politica de Integritate Academică

Temele trebuie să reprezinte munca proprie. Colaborarea pentru înțelegerea conceptelor este permisă, dar codul trebuie scris individual.

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
