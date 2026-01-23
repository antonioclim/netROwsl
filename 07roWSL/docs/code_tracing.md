# Exerciții de Code Tracing - Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix
>
> Code Tracing = urmărirea pas-cu-pas a execuției codului și predicția output-ului.
> Această tehnică dezvoltă abilitatea de a "citi" cod și de a înțelege fluxul de execuție.

---

## Exercițiul T1: Handshake TCP în Log

### Cod de Analizat

```python
import socket

def client_simplu():
    print("1. Creare socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("2. Înainte de connect")
    sock.connect(("localhost", 9090))
    print("3. După connect")
    
    print("4. Înainte de send")
    sock.sendall(b"TEST")
    print("5. După send")
    
    print("6. Înainte de recv")
    data = sock.recv(1024)
    print(f"7. După recv: {data}")
    
    print("8. Înainte de close")
    sock.close()
    print("9. După close")

client_simplu()
```

### Întrebări

**Q1:** În ce ordine apar mesajele 1-9 pe ecran? (presupunem că serverul răspunde corect)

```
Răspuns: ___________________________________
```

**Q2:** Între care două mesaje (`print`) se realizează handshake-ul TCP (SYN, SYN-ACK, ACK)?

```
Răspuns: Între mesajul ___ și mesajul ___
```

**Q3:** Dacă serverul nu rulează (port închis), care este ULTIMUL mesaj care apare?

```
Răspuns: Mesajul ___
```

<details>
<summary>Vezi Răspunsurile</summary>

**Q1:** `1, 2, 3, 4, 5, 6, 7, 8, 9` - în ordine, presupunând succes

**Q2:** Între mesajul **2** și mesajul **3** - handshake-ul TCP se realizează în interiorul `connect()`

**Q3:** Mesajul **2** - `connect()` va arunca `ConnectionRefusedError` și programul se oprește

**Explicație:**
- `socket()` doar creează structura de date, nu face I/O de rețea
- `connect()` face handshake-ul complet (SYN → SYN-ACK → ACK)
- `sendall()` și `recv()` transferă date pe conexiunea deja stabilită
- `close()` trimite FIN pentru închidere grațioasă

</details>

---

## Exercițiul T2: Comportament iptables

### Scenariu

Pe server sunt configurate următoarele reguli:

```bash
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j REJECT
iptables -A INPUT -p tcp --dport 22 -j DROP
iptables -A INPUT -p tcp -j REJECT
```

### Întrebări

**Q1:** Ce se întâmplă când un client încearcă să se conecteze la portul 80?

```
Răspuns: ___________________________________
```

**Q2:** Ce se întâmplă când un client încearcă să se conecteze la portul 443?

```
Răspuns: ___________________________________
```

**Q3:** Ce se întâmplă când un client încearcă să se conecteze la portul 22?

```
Răspuns: ___________________________________
```

**Q4:** Ce se întâmplă când un client încearcă să se conecteze la portul 8080?

```
Răspuns: ___________________________________
```

<details>
<summary>Vezi Răspunsurile</summary>

**Q1:** Conexiunea **REUȘEȘTE** (ACCEPT) - portul 80 este permis explicit

**Q2:** Conexiunea **EȘUEAZĂ IMEDIAT** cu RST (REJECT) - clientul primește "Connection refused"

**Q3:** Conexiunea **EXPIRĂ DUPĂ TIMEOUT** (DROP) - clientul așteaptă ~30-75 secunde fără răspuns

**Q4:** Conexiunea **EȘUEAZĂ IMEDIAT** cu RST (REJECT) - se aplică ultima regulă (`-p tcp -j REJECT`)

**Explicație:**
- Regulile se evaluează în ordine (first-match-wins)
- Portul 8080 nu are regulă specifică, așa că se aplică regula generală pentru TCP
- DROP = tăcere, REJECT = răspuns explicit

</details>

---

## Exercițiul T3: Log Container Docker

### Output de Analizat

Acesta este log-ul containerului `week7_server_tcp`:

```
[2025-01-23 10:00:00] Server TCP Echo pornit pe 0.0.0.0:9090
[2025-01-23 10:00:00] Așteptare conexiuni...
[2025-01-23 10:00:15] Conexiune nouă de la 172.17.0.1:45678
[2025-01-23 10:00:15] Primit de la 172.17.0.1:45678: Salut
[2025-01-23 10:00:15] Trimis către 172.17.0.1:45678: Salut
[2025-01-23 10:00:20] Conexiune nouă de la 172.17.0.1:45679
[2025-01-23 10:00:20] Primit de la 172.17.0.1:45679: Test
[2025-01-23 10:00:20] Trimis către 172.17.0.1:45679: Test
[2025-01-23 10:00:25] Client 172.17.0.1:45678 deconectat
[2025-01-23 10:00:30] Conexiune resetată de 172.17.0.1:45679
```

### Întrebări

**Q1:** Câte conexiuni TCP au fost deschise în total?

```
Răspuns: ___ conexiuni
```

**Q2:** Care conexiune a fost închisă normal (cu FIN) și care a fost terminată brusc (cu RST)?

```
Normal (FIN): conexiunea de pe portul ___
Brusc (RST): conexiunea de pe portul ___
```

**Q3:** De ce porturile efemere (45678, 45679) sunt diferite pentru fiecare conexiune?

```
Răspuns: ___________________________________
```

**Q4:** Câte secunde a durat conexiunea de pe portul 45678?

```
Răspuns: ___ secunde
```

<details>
<summary>Vezi Răspunsurile</summary>

**Q1:** **2 conexiuni** (45678 și 45679)

**Q2:** 
- Normal (FIN): **45678** ("Client deconectat" = închidere grațioasă)
- Brusc (RST): **45679** ("Conexiune resetată" = terminare bruscă)

**Q3:** Fiecare conexiune TCP are un port efemer (temporar) unic alocat de sistemul de operare al clientului. Aceasta permite multiple conexiuni simultane către același server.

**Q4:** **10 secunde** (de la 10:00:15 la 10:00:25)

</details>

---

## Exercițiul T4: Captura Wireshark

### Captura de Analizat

```
No.  Time      Source        Dest          Proto  Info
1    0.000000  192.168.1.10  10.0.7.100    TCP    45678 → 9090 [SYN]
2    0.000500  10.0.7.100    192.168.1.10  TCP    9090 → 45678 [SYN, ACK]
3    0.001000  192.168.1.10  10.0.7.100    TCP    45678 → 9090 [ACK]
4    0.002000  192.168.1.10  10.0.7.100    TCP    45678 → 9090 [PSH, ACK] Len=5
5    0.002500  10.0.7.100    192.168.1.10  TCP    9090 → 45678 [ACK]
6    0.003000  10.0.7.100    192.168.1.10  TCP    9090 → 45678 [PSH, ACK] Len=5
7    0.003500  192.168.1.10  10.0.7.100    TCP    45678 → 9090 [ACK]
8    0.004000  192.168.1.10  10.0.7.100    TCP    45678 → 9090 [FIN, ACK]
9    0.004500  10.0.7.100    192.168.1.10  TCP    9090 → 45678 [FIN, ACK]
10   0.005000  192.168.1.10  10.0.7.100    TCP    45678 → 9090 [ACK]
```

### Întrebări

**Q1:** Care pachete formează handshake-ul TCP (three-way handshake)?

```
Răspuns: Pachetele ___, ___, ___
```

**Q2:** În pachetul #4, câți octeți de date au fost trimiși?

```
Răspuns: ___ octeți
```

**Q3:** Cine a inițiat închiderea conexiunii - clientul sau serverul?

```
Răspuns: _______________
```

**Q4:** Care este latența rețelei (round-trip time) bazată pe pachetele 1 și 2?

```
Răspuns: ___ milisecunde
```

**Q5:** Scrie filtrul Wireshark care ar afișa DOAR acest stream:

```
Răspuns: ___________________________________
```

<details>
<summary>Vezi Răspunsurile</summary>

**Q1:** Pachetele **1, 2, 3** (SYN → SYN-ACK → ACK)

**Q2:** **5 octeți** (Len=5 în info)

**Q3:** **Clientul** (192.168.1.10) - el trimite primul FIN în pachetul #8

**Q4:** **0.5 milisecunde** (0.000500 - 0.000000 = 500 microsecunde = 0.5 ms)

**Q5:** `tcp.port == 9090 && tcp.port == 45678` sau `tcp.stream eq 0` (dacă e primul stream)

**Explicație flux:**
```
Client                          Server
  |-------- SYN (#1) ----------->|
  |<------ SYN-ACK (#2) ---------|
  |-------- ACK (#3) ----------->|  ← Handshake complet
  |-------- DATA (#4) ---------->|
  |<-------- ACK (#5) ----------|
  |<------- DATA (#6) ----------|  ← Echo response
  |-------- ACK (#7) ----------->|
  |-------- FIN (#8) ----------->|  ← Client inițiază închiderea
  |<------ FIN-ACK (#9) ---------|
  |-------- ACK (#10) ---------->|  ← Conexiune închisă
```

</details>

---

## Exercițiul T5: Cod cu Eroare

### Cod de Analizat

Următorul cod are o **eroare logică**. Identifică problema:

```python
import socket

def sonda_port(host, port):
    """Verifică dacă un port este deschis."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0)
    
    rezultat = sock.connect_ex((host, port))
    
    if rezultat == 0:
        print(f"Port {port}: DESCHIS")
    else:
        print(f"Port {port}: ÎNCHIS")
    
    # Sondare următorul port
    sonda_port(host, port + 1)

# Sondează porturile 9090-9095
sonda_port("localhost", 9090)
```

### Întrebări

**Q1:** Care este problema principală cu acest cod?

```
Răspuns: ___________________________________
```

**Q2:** Ce se întâmplă cu socket-ul după fiecare verificare?

```
Răspuns: ___________________________________
```

**Q3:** Rescrie funcția corectată:

```python
# Spațiu pentru codul corectat:



```

<details>
<summary>Vezi Răspunsurile</summary>

**Q1:** Două probleme principale:
1. **Socket-ul nu se închide niciodată** - memory leak / resource leak
2. **Recursie infinită** - funcția se apelează pe sine fără condiție de oprire

**Q2:** Socket-ul rămâne deschis, consumând resurse. După suficiente apeluri, sistemul va refuza să creeze socket-uri noi ("Too many open files").

**Q3:** Cod corectat:

```python
import socket

def sonda_port(host, port):
    """Verifică dacă un port este deschis."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0)
    
    try:
        rezultat = sock.connect_ex((host, port))
        
        if rezultat == 0:
            print(f"Port {port}: DESCHIS")
        else:
            print(f"Port {port}: ÎNCHIS")
    finally:
        sock.close()  # IMPORTANT: Închide socket-ul

def sonda_interval(host, port_start, port_end):
    """Sondează un interval de porturi."""
    for port in range(port_start, port_end + 1):
        sonda_port(host, port)

# Sondează porturile 9090-9095
sonda_interval("localhost", 9090, 9095)
```

</details>

---

## Tabel de Auto-Evaluare

| Exercițiu | Întrebări Corecte | Total |
|-----------|-------------------|-------|
| T1: Handshake Log | ___/3 | 3 |
| T2: iptables | ___/4 | 4 |
| T3: Docker Log | ___/4 | 4 |
| T4: Wireshark | ___/5 | 5 |
| T5: Eroare Cod | ___/3 | 3 |
| **TOTAL** | **___/19** | 19 |

**Interpretare:**
- 17-19: Excelent! Înțelegi foarte bine fluxul de execuție
- 13-16: Bun. Revizuiește secțiunile unde ai greșit
- 9-12: Satisfăcător. Ai nevoie de mai multă practică
- <9: Recitește teoria și încearcă din nou

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
