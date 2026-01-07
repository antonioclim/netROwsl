# Ieșiri Așteptate - Săptămâna 2

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest document descrie ieșirile așteptate pentru exercițiile de laborator.

## Exercițiul 1: Server TCP Concurent

### Pornire Server (Mod Threaded)

```
============================================================
Server TCP pornit pe 0.0.0.0:9090
Mod: CONCURENT (threaded)
Apăsați Ctrl+C pentru oprire
============================================================
```

### Conectare Client

**Intrare:**
```
python ex_2_01_tcp.py client --message "salut lume"
```

**Ieșire așteptată:**
```
Răspuns: OK: SALUT LUME
```

### Sesiune Interactivă

**Exemplu sesiune:**
```
Conectat la localhost:9090
Introduceți mesaje (exit/quit pentru ieșire)
----------------------------------------
> test
< OK: TEST
> rețele de calculatoare
< OK: REȚELE DE CALCULATOARE
> exit
< La revedere!
```

### Test de Încărcare

**Comandă:**
```
python ex_2_01_tcp.py load --clients 5 --messages 10
```

**Ieșire așteptată (aproximativ):**
```
============================================================
Test de Încărcare: 5 clienți × 10 mesaje
============================================================

Rezultate:
  Total cereri: 50
  Reușite: 50
  Eșuate: 0
  Durată totală: 0.15s
  Latență medie: 1.23ms
  Latență min: 0.85ms
  Latență max: 3.21ms
  Throughput: 333.3 req/s
============================================================
```

## Exercițiul 2: Server UDP cu Protocol

### Pornire Server

```
============================================================
Server UDP pornit pe 0.0.0.0:9091
Protocol: Comenzi text personalizate
Apăsați Ctrl+C pentru oprire
============================================================
```

### Comenzi și Răspunsuri Așteptate

| Comandă | Răspuns Așteptat |
|---------|------------------|
| `ping` | `PONG` |
| `upper:salut` | `SALUT` |
| `lower:SALUT` | `salut` |
| `reverse:abc` | `cba` |
| `echo:test` | `test` |
| `time` | `2025-01-06 14:30:45` (format dată/oră) |
| `help` | Lista comenzilor disponibile |
| `comandă_greșită` | `EROARE:Comandă necunoscută...` |

### Sesiune Interactivă UDP

```
Client UDP conectat la localhost:9091
Introduceți comenzi (quit pentru ieșire, help pentru ajutor)
----------------------------------------
> ping
PONG
> upper:test
TEST
> time
2025-01-06 14:30:45
> reverse:Python
nohtyP
> quit
La revedere!
```

## Teste Automate

### Test Exercițiul 1

**Comandă:**
```
python tests/test_exercises.py --exercise 1
```

**Ieșire așteptată (toate testele trec):**
```
============================================================
Teste Exercițiul 1: Server TCP Concurent
============================================================

  ✓ TCP: Conexiune de bază (1.2ms)
  ✓ TCP: Transformare majuscule (2.3ms)
  ✓ TCP: Mesaje multiple (5.1ms)
  ✓ TCP: Concurență (3 clienți) (15.2ms)

============================================================
Sumar Teste
============================================================
Total: 4 teste
Reușite: 4
Eșuate: 0
Durată medie: 5.9ms

✓ Toate testele au trecut!
```

### Test Exercițiul 2

**Comandă:**
```
python tests/test_exercises.py --exercise 2
```

**Ieșire așteptată (toate testele trec):**
```
============================================================
Teste Exercițiul 2: Server UDP cu Protocol
============================================================

  ✓ UDP: Comandă ping (0.8ms)
  ✓ UDP: Comandă upper (0.9ms)
  ✓ UDP: Comandă reverse (0.7ms)
  ✓ UDP: Comandă time (0.9ms)
  ✓ UDP: Comenzi multiple (2.1ms)

============================================================
Sumar Teste
============================================================
Total: 5 teste
Reușite: 5
Eșuate: 0
Durată medie: 1.1ms

✓ Toate testele au trecut!
```

## Capturare Wireshark

### Filtre Recomandate

Pentru vizualizarea traficului în Wireshark:

**Handshake TCP:**
```
tcp.port == 9090 && tcp.flags.syn == 1
```

Ar trebui să vedeți pachete cu flag-uri:
- `[SYN]` - De la client
- `[SYN, ACK]` - De la server
- `[ACK]` - De la client

**Transfer Date TCP:**
```
tcp.port == 9090 && tcp.len > 0
```

Ar trebui să vedeți pachete cu flag `[PSH, ACK]` conținând datele.

**Trafic UDP:**
```
udp.port == 9091
```

Ar trebui să vedeți perechi de datagrame (cerere-răspuns) fără handshake.

## Verificare Mediu

### Comandă Verificare

```
python setup/verify_environment.py
```

### Ieșire Așteptată (totul OK)

```
============================================================
Verificarea Mediului pentru Laboratorul Săptămânii 2
Rețele de Calculatoare - ASE, Informatică Economică
============================================================

Mediul Python:
  [OK]    Python 3.11.x
  [OK]    Pachet Python: docker
  [OK]    Pachet Python: requests
  [OK]    Pachet Python: pyyaml

Mediul Docker:
  [OK]    Docker instalat
  [OK]    Docker Compose instalat
  [OK]    Daemon-ul Docker pornit

Mediul WSL2:
  [OK]    WSL2 disponibil

Instrumente de Rețea:
  [OK]    Wireshark disponibil

Structura Proiectului:
  [OK]    Structură directoare completă

============================================================
Rezultate: 10 reușite, 0 eșuate, 0 avertismente
✓ Mediul de lucru este pregătit!
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
