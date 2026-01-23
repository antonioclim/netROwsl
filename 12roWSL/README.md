# Săptămâna 12: Protocoale de Email (SMTP) și Apel de Procedură la Distanță (RPC)

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Credențiale Standard:**
| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | stud | stud |
| Portainer | stud | studstudstud |

---

## Prezentare Generală

SMTP stă la baza email-ului. Simplu, bazat pe text, ușor de înțeles.

RPC face altceva: permite programelor să cheme funcții pe alte calculatoare. Parcă ar fi locale, dar nu sunt. Vom vedea trei variante: JSON-RPC (text, simplu), XML-RPC (text, verbose) și gRPC (binar, rapid).

Care-i diferența practică? O vedem în Wireshark.

## Obiective de Învățare

1. **Identificați** componentele unei tranzacții SMTP
2. **Explicați** diferențele arhitecturale dintre JSON-RPC, XML-RPC și gRPC
3. **Implementați** dialoguri SMTP folosind netcat
4. **Demonstrați** apeluri RPC folosind toate cele trei framework-uri
5. **Analizați** traficul de rețea în Wireshark
6. **Evaluați** adecvarea diferitelor protocoale RPC pentru diverse scenarii

---

## Pornire Rapidă

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT12/12roWSL

# Pornește toate serviciile
python3 scripts/porneste_lab.py
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Descriere |
|----------|----------|-----------|
| Portainer | http://localhost:9000 | Management Docker |
| Server SMTP | localhost:1025 | Server SMTP educațional |
| Server JSON-RPC | http://localhost:6200 | JSON-RPC 2.0 |
| Server XML-RPC | http://localhost:6201 | XML-RPC cu introspecție |
| Server gRPC | localhost:6251 | gRPC (HTTP/2 + Protocol Buffers) |

---

## Exercițiul 1: Dialog SMTP Manual

**Obiectiv:** Realizarea unui dialog SMTP complet folosind netcat

---

**🔮 PREDICȚIE (răspunde ÎNAINTE de a te conecta):**

1. Ce cod numeric va trimite serverul ca salut? (2xx, 4xx, sau 5xx?)
2. Câte linii va avea răspunsul la comanda EHLO?
3. Ce se întâmplă dacă trimiți DATA înainte de RCPT TO?
4. Cum se termină corpul mesajului în SMTP?

*Notează răspunsurile pe hârtie, apoi verifică!*

---

**Pași:**

```bash
nc localhost 1025
```

```
HELO client.local
MAIL FROM:<expeditor@exemplu.ro>
RCPT TO:<destinatar@exemplu.ro>
DATA
Subject: Test SMTP

Corpul mesajului.
.
QUIT
```

---

**🔍 VERIFICARE PREDICȚII:**

| Predicția ta | Răspuns corect | Explicație |
|--------------|----------------|------------|
| Cod salut | 220 | "Service ready" |
| Linii EHLO | 3-5+ | Server-ul listează extensiile |
| DATA fără RCPT | 503 | "Bad sequence of commands" |
| Terminator corp | Linie cu doar "." | RFC 5321 |

---

## Exercițiul 2: Apeluri JSON-RPC 2.0

---

**🔮 PREDICȚIE:**

1. Ce câmp va conține rezultatul în răspuns? (`result` sau `data`?)
2. Ce HTTP status code primești? (200, 201, sau 204?)
3. Ce se întâmplă dacă omit câmpul `id`?

---

```bash
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"add","params":[10,20],"id":1}'
```

---

**🔍 VERIFICARE:**
- Câmp rezultat: `result` (Standard JSON-RPC 2.0)
- HTTP status: 200 (Mereu 200, erorile sunt în body)
- Fără `id`: Niciun răspuns (e o "notificare")

---

## Exercițiul 3: Apeluri XML-RPC

```bash
curl -X POST http://localhost:6201 \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
  <methodCall>
    <methodName>system.listMethods</methodName>
  </methodCall>'
```

---

## Exercițiul 4: Apeluri gRPC

---

**🔮 PREDICȚIE:**

1. Care payload e mai mic: JSON-RPC sau gRPC? De câte ori?
2. gRPC folosește HTTP/1.1 sau HTTP/2?
3. Poți citi payload-ul gRPC cu ochiul liber în Wireshark?

---

```bash
python3 src/apps/rpc/grpc/grpc_client.py
```

---

**🔍 VERIFICARE:**
- gRPC e ~10x mai mic (binar vs text)
- HTTP/2 (multiplexare, compresie)
- Nu, format binar

---

## Exercițiul 5: Benchmark Comparativ

```bash
python3 src/apps/rpc/benchmark_rpc.py --calls 1000
```

---

## Diagrame Comparative

### Comparație Dimensiuni Payload RPC

```
JSON-RPC add(10,20):  {"jsonrpc":"2.0","method":"add","params":[10,20],"id":1}
                      ~55 bytes

gRPC Add(10,20):      08 0A 10 14
                      ~4 bytes
```

---

## ❓ Întrebări Frecvente (FAQ)

### De ce folosim portul 1025 și nu 25?

Portul 25 necesită privilegii root. Portul 1025 e neprivilegiat.

### Care RPC să aleg pentru proiectul meu?

| Scenariu | Recomandare |
|----------|-------------|
| API public pentru browsere | JSON-RPC sau REST |
| Microservicii interne | gRPC |
| Integrare sisteme legacy | XML-RPC |

### De ce gRPC nu apare în Wireshark ca "gRPC"?

gRPC folosește HTTP/2. Wireshark îl vede ca HTTP2.

---

## Oprire și Curățare

```bash
# Oprește containerele de laborator
python3 scripts/opreste_lab.py

# Curățare completă
python3 scripts/curata.py --complet
```

---

## Referințe

- RFC 5321 - Simple Mail Transfer Protocol
- JSON-RPC 2.0 Specification (https://www.jsonrpc.org/specification)
- gRPC Documentation (https://grpc.io/docs/)
- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach*

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
