# Parsons Problems - Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix
>
> Parsons Problems sunt exerciții în care trebuie să rearanjezi linii de cod
> amestecate pentru a obține un program corect. Această tehnică reduce 
> sarcina cognitivă și ajută la înțelegerea structurii programelor.

---

## Problema 1: Client TCP Simplu

### Instrucțiuni

Rearanjează liniile de mai jos pentru a crea un client TCP care:
1. Creează un socket
2. Se conectează la server
3. Trimite un mesaj
4. Primește răspunsul
5. Închide conexiunea

### Linii Amestecate

```python
# A
raspuns = sock.recv(4096)

# B
sock.close()

# C
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# D
print(f"Răspuns: {raspuns.decode()}")

# E
sock.connect(("localhost", 9090))

# F
sock.sendall(b"Salut server!")

# G
import socket
```

### Spațiu pentru Răspuns

Scrie ordinea corectă (ex: G, C, E, F, A, D, B):

```
Ordinea mea: ___, ___, ___, ___, ___, ___, ___
```

<details>
<summary>Vezi Soluția</summary>

**Ordinea corectă: G, C, E, F, A, D, B**

```python
import socket                                          # G - Import întâi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # C - Creează socket
sock.connect(("localhost", 9090))                      # E - Conectare
sock.sendall(b"Salut server!")                         # F - Trimite
raspuns = sock.recv(4096)                              # A - Primește
print(f"Răspuns: {raspuns.decode()}")                  # D - Afișează
sock.close()                                           # B - Închide
```

**Explicație:**
- Import-urile sunt MEREU primele
- Socket-ul trebuie creat înainte de conectare
- Conectarea trebuie făcută înainte de trimitere/primire
- `close()` este MEREU ultimul

</details>

---

## Problema 2: Regulă iptables

### Instrucțiuni

Rearanjează componentele pentru a crea o regulă iptables care:
- Blochează (DROP) traficul TCP
- Pe portul 9090
- Pentru pachete care intră (INPUT)

### Componente Amestecate

```bash
# A
-j DROP

# B  
-p tcp

# C
iptables

# D
--dport 9090

# E
-A INPUT
```

### Spațiu pentru Răspuns

```
Comanda mea: ___ ___ ___ ___ ___
```

<details>
<summary>Vezi Soluția</summary>

**Ordinea corectă: C, E, B, D, A**

```bash
iptables -A INPUT -p tcp --dport 9090 -j DROP
```

**Structura generală iptables:**
```
iptables -A [LANȚ] -p [PROTOCOL] --dport [PORT] -j [ACȚIUNE]
```

**Explicație componentelor:**
- `iptables` - comanda de bază
- `-A INPUT` - adaugă la lanțul INPUT (pachete care intră)
- `-p tcp` - protocolul TCP
- `--dport 9090` - portul destinație
- `-j DROP` - acțiunea (saltul la DROP)

</details>

---

## Problema 3: Filtru Wireshark

### Instrucțiuni

Construiește un filtru Wireshark care afișează:
- Pachete TCP pe portul 9090 SAU
- Pachete UDP pe portul 9091 SAU
- Mesaje ICMP

### Componente Amestecate

```
# A
tcp.port == 9090

# B
or

# C
udp.port == 9091

# D
or

# E
icmp
```

### Spațiu pentru Răspuns

```
Filtrul meu: ___ ___ ___ ___ ___
```

<details>
<summary>Vezi Soluția</summary>

**Ordinea corectă: A, B, C, D, E**

```
tcp.port == 9090 or udp.port == 9091 or icmp
```

**Variante acceptate:**
- `(tcp.port == 9090) or (udp.port == 9091) or icmp`
- `icmp or tcp.port == 9090 or udp.port == 9091`

**Notă:** Ordinea operanzilor nu contează, dar operatorul `or` trebuie între fiecare condiție.

</details>

---

## Problema 4: Server UDP cu Logging

### Instrucțiuni

Rearanjează pentru a crea un receptor UDP care:
1. Creează socket UDP
2. Leagă socket-ul de un port
3. Așteaptă datagrame într-o buclă
4. Afișează datele primite

### Linii Amestecate (cu distractor!)

```python
# A
data, addr = sock.recvfrom(4096)

# B
sock.bind(("0.0.0.0", 9091))

# C
while True:

# D
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# E
print(f"Primit de la {addr}: {data.decode()}")

# F - DISTRACTOR (nu aparține soluției!)
sock.listen(5)

# G
import socket
```

### Spațiu pentru Răspuns

Scrie ordinea corectă (una din linii NU trebuie inclusă!):

```
Ordinea mea: ___, ___, ___, ___, ___, ___
```

<details>
<summary>Vezi Soluția</summary>

**Ordinea corectă: G, D, B, C, A, E**

**Linia F (`sock.listen(5)`) NU se folosește!** - `listen()` este doar pentru TCP, nu pentru UDP!

```python
import socket                                          # G
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # D - DGRAM = UDP
sock.bind(("0.0.0.0", 9091))                           # B
while True:                                            # C
    data, addr = sock.recvfrom(4096)                   # A
    print(f"Primit de la {addr}: {data.decode()}")     # E
```

**Diferențe cheie TCP vs UDP:**
| TCP | UDP |
|-----|-----|
| `SOCK_STREAM` | `SOCK_DGRAM` |
| Necesită `listen()` și `accept()` | Direct `recvfrom()` |
| `recv()` | `recvfrom()` (returnează și adresa) |

</details>

---

## Problema 5: Verificare Port cu Timeout

### Instrucțiuni

Rearanjează pentru a crea o funcție care verifică dacă un port TCP este deschis, cu timeout de 2 secunde.

### Linii Amestecate

```python
# A
return True

# B
sock.settimeout(2.0)

# C
except (socket.timeout, ConnectionRefusedError):

# D
def verifica_port(host, port):

# E
return False

# F
try:

# G
sock.connect((host, port))

# H
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# I
finally:

# J
sock.close()
```

### Spațiu pentru Răspuns

```
Ordinea mea: ___, ___, ___, ___, ___, ___, ___, ___, ___, ___
```

<details>
<summary>Vezi Soluția</summary>

**Ordinea corectă: D, H, B, F, G, A, C, E, I, J**

```python
def verifica_port(host, port):           # D
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # H
    sock.settimeout(2.0)                 # B
    try:                                 # F
        sock.connect((host, port))       # G
        return True                      # A
    except (socket.timeout, ConnectionRefusedError):  # C
        return False                     # E
    finally:                             # I
        sock.close()                     # J
```

**Structura try-except-finally:**
- `try`: cod care poate eșua
- `except`: gestionare erori
- `finally`: cleanup (se execută MEREU)

</details>

---

## Auto-Evaluare

| Problemă | Rezolvată Corect? | Timp (minute) |
|----------|-------------------|---------------|
| 1. Client TCP | ☐ Da / ☐ Nu | ___ |
| 2. iptables | ☐ Da / ☐ Nu | ___ |
| 3. Filtru Wireshark | ☐ Da / ☐ Nu | ___ |
| 4. Server UDP | ☐ Da / ☐ Nu | ___ |
| 5. Verificare Port | ☐ Da / ☐ Nu | ___ |

**Scor:** ___/5 corecte

**Reflecție:** Ce concepte trebuie să revizuiesc?

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
