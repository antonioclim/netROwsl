# Întrebări Peer Instruction - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Ghid de Utilizare

Folosiți aceste întrebări în timpul laboratorului pentru a verifica înțelegerea conceptelor.

**Secvență recomandată:**
1. **Vot individual** (1 minut) - Studenții votează în tăcere
2. **Discuție în perechi** (3 minute) - Discută cu colegul de bancă
3. **Revot** (30 secunde) - Votează din nou după discuție
4. **Explicație** (2 minute) - Instructorul explică răspunsul corect

---

## PI-1: Coduri de Răspuns SMTP

### Scenariu
Trimiți comanda RCPT TO:<inexistent@domeniu.ro> către un server SMTP.

### Întrebare
Ce tip de cod de răspuns vei primi cel mai probabil?

### Opțiuni
- **A)** 250 - OK, destinatar acceptat
- **B)** 354 - Trimite datele mesajului
- **C)** 450 - Cutie poștală temporar indisponibilă
- **D)** 550 - Cutie poștală inexistentă

### Răspuns corect: D

### Analiza distractorilor
| Opțiune | Misconceptia vizată |
|---------|---------------------|
| A | Studenții care cred că serverul acceptă orice adresă |
| B | Confuzie cu răspunsul la comanda DATA |
| C | Confuzie între erori temporare (4xx) și permanente (5xx) |

---

## PI-2: Ordinea Comenzilor SMTP

### Scenariu
Vrei să trimiți un email. Ai deja conexiunea deschisă și ai primit codul 220.

### Întrebare
Care e ordinea CORECTĂ a comenzilor?

### Opțiuni
- **A)** DATA → MAIL FROM → RCPT TO → QUIT
- **B)** HELO → RCPT TO → MAIL FROM → DATA → QUIT
- **C)** HELO → MAIL FROM → RCPT TO → DATA → QUIT
- **D)** MAIL FROM → HELO → RCPT TO → DATA → QUIT

### Răspuns corect: C

---

## PI-3: JSON-RPC vs REST

### Scenariu
Vrei să aduni două numere pe un server remote.

### Întrebare
Care e diferența PRINCIPALĂ între JSON-RPC și REST pentru această operație?

### Opțiuni
- **A)** JSON-RPC folosește JSON, REST folosește XML
- **B)** JSON-RPC trimite numele metodei în body, REST în URL/verb HTTP
- **C)** JSON-RPC e mai rapid pentru că folosește UDP
- **D)** REST nu poate face operații matematice

### Răspuns corect: B

---

## PI-4: Protocol Buffers vs JSON

### Scenariu
Ai un mesaj gRPC cu a=10, b=20 pentru metoda Add.

### Întrebare
De ce payload-ul gRPC e mai mic decât JSON-RPC echivalent?

### Opțiuni
- **A)** gRPC comprimă JSON-ul automat
- **B)** gRPC folosește numere în loc de nume de câmpuri
- **C)** gRPC trimite doar diferențele față de apelul anterior
- **D)** gRPC folosește caractere Unicode mai scurte

### Răspuns corect: B

### Demonstrație în Wireshark
JSON:     {"a":10,"b":20}     → ~15 bytes text
Protobuf: 08 0A 10 14         → 4 bytes binar

---

## PI-5: Port Mapping Docker

### Scenariu
Serverul SMTP din container ascultă pe portul 25, dar docker-compose are ports: - "1025:25"

### Întrebare
Ce comandă funcționează din Windows/WSL host?

### Opțiuni
- **A)** nc localhost 25
- **B)** nc localhost 1025
- **C)** nc 172.28.12.10 25
- **D)** Toate funcționează

### Răspuns corect: B (din host), C (din alt container pe aceeași rețea)

---

## PI-6: Notificări JSON-RPC

### Scenariu
Trimiți cererea: {"jsonrpc":"2.0","method":"log","params":["mesaj"]}

### Întrebare
Ce răspuns vei primi de la server?

### Opțiuni
- **A)** {"jsonrpc":"2.0","result":null,"id":null}
- **B)** {"jsonrpc":"2.0","result":"ok","id":1}
- **C)** Niciun răspuns (conexiunea se închide fără date)
- **D)** Eroare: "id" is required

### Răspuns corect: C

---

## PI-7: HTTP/2 vs HTTP/1.1

### Scenariu
Trimiți 10 cereri gRPC consecutive către același server.

### Întrebare
Câte conexiuni TCP se deschid?

### Opțiuni
- **A)** 10 conexiuni (una per cerere)
- **B)** 1 conexiune (multiplexare HTTP/2)
- **C)** 2 conexiuni (pool minim)
- **D)** Depinde de server

### Răspuns corect: B

---

## PI-8: Terminatorul SMTP DATA

### Scenariu
Trimiți corpul unui email prin SMTP și vrei să termini.

### Întrebare
Ce secvență marchează sfârșitul corpului mesajului?

### Opțiuni
- **A)** Două linii goale consecutive
- **B)** Caracterul EOF (Ctrl+D)
- **C)** O linie conținând doar un punct (.)
- **D)** Comanda END

### Răspuns corect: C

---

## PI-9: Introspecție XML-RPC

### Scenariu
Te conectezi la un server XML-RPC necunoscut și vrei să vezi ce metode oferă.

### Întrebare
Ce metodă standard apelezi?

### Opțiuni
- **A)** help()
- **B)** system.listMethods()
- **C)** getMethods()
- **D)** __dir__()

### Răspuns corect: B

---

## PI-10: Alegerea Protocolului RPC

### Scenariu
Construiești un sistem cu: Frontend web în browser, 50 de microservicii backend.

### Întrebare
Ce combinație de protocoale ai alege?

### Opțiuni
- **A)** JSON-RPC pentru toate
- **B)** gRPC pentru toate
- **C)** JSON-RPC pentru frontend↔backend, gRPC pentru backend↔backend
- **D)** XML-RPC pentru toate (e mai matur)

### Răspuns corect: C

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
