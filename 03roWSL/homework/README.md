# Teme pentru Acasă - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Prezentare Generală

Acest director conține trei teme care extind conceptele abordate în laborator. Fiecare temă include un fișier schelet cu structura de bază și indicații pentru implementare.

**Termen limită:** Consultați platforma e-learning pentru data exactă.

---

## Tema 1: Receptor Broadcast cu Statistici

**Fișier:** `exercises/tema_3_01.py`

**Obiectiv:** Extindeți receptorul UDP broadcast pentru a colecta și afișa statistici detaliate despre traficul primit.

### Cerințe

1. **Statistici pachete (40%)**
   - Numărați pachetele primite
   - Identificați expeditorii unici (IP)
   - Calculați rata de recepție (pachete/secundă)
   - Calculați dimensiunea payload: min, max, medie

2. **Analiză temporală (20%)**
   - Calculați intervalul între pachete consecutive
   - Detectați pauze mai mari de 5 secunde

3. **Afișare în timp real (20%)**
   - Actualizați statisticile la fiecare 5 secunde
   - Format clar și lizibil

4. **Oprire elegantă (20%)**
   - Tratați Ctrl+C pentru oprire
   - Afișați sumar final la oprire

5. **BONUS: Export JSON (10%)**
   - Opțiune `--output` pentru salvare în fișier JSON

### Criterii de Evaluare

| Criteriu | Punctaj |
|----------|---------|
| Colectare statistici corecte | 40% |
| Oprire elegantă cu sumar | 20% |
| Calitate cod (docstrings, typing) | 20% |
| Export JSON funcțional | 20% |

### Testare

```bash
# Porniți receptorul
python tema_3_01.py --port 5007

# Într-un alt terminal, trimiteți mesaje
python ex_3_01_udp_broadcast.py --mod sender --numar 20

# Verificați statisticile afișate
```

---

## Tema 2: Aplicație Chat Multicast

**Fișier:** `exercises/tema_3_02.py`

**Obiectiv:** Implementați o aplicație de chat bazată pe multicast care permite comunicarea între mai mulți utilizatori.

### Cerințe

1. **Comunicare Multicast (30%)**
   - Folosiți grupul 239.0.0.10, portul 5010
   - Înscrierea și dezabonarea corectă din grup

2. **Protocol Mesaje (20%)**
   - Format JSON cu tipuri: JOIN, MESSAGE, LEAVE
   - Structură: `{"type": "...", "user": "...", "text": "...", "timestamp": "..."}`

3. **Concurență (25%)**
   - Thread separat pentru recepție
   - Buclă principală pentru input utilizator

4. **Experiență Utilizator (25%)**
   - Notificări când utilizatori intră/pleacă
   - Afișare timestamp și username
   - Ignorarea propriilor mesaje

### Protocol Mesaje

```json
// Intrare în chat
{"type": "JOIN", "user": "Alice", "timestamp": "2024-01-15T10:30:00"}

// Mesaj normal
{"type": "MESSAGE", "user": "Alice", "text": "Salut tuturor!", "timestamp": "2024-01-15T10:30:05"}

// Părăsire chat
{"type": "LEAVE", "user": "Alice", "timestamp": "2024-01-15T10:35:00"}
```

### Criterii de Evaluare

| Criteriu | Punctaj |
|----------|---------|
| Înscriere/dezabonare multicast | 30% |
| Threading corect | 25% |
| Protocol JSON complet | 20% |
| UX (notificări, formatare) | 25% |

### Testare

```bash
# Terminal 1
python tema_3_02.py --username Alice

# Terminal 2
python tema_3_02.py --username Bob

# Terminal 3
python tema_3_02.py --username Carol
```

---

## Tema 3: Tunel TCP cu Logging și Metrici

**Fișier:** `exercises/tema_3_03.py`

**Obiectiv:** Îmbunătățiți tunelul TCP cu sistem de logging, metrici de performanță și gestionare avansată a conexiunilor.

### Cerințe

1. **Logging Complet (30%)**
   - Log pentru fiecare conexiune nouă
   - Log pentru transferuri de date
   - Suport pentru nivele: DEBUG, INFO, WARNING, ERROR
   - Opțiune pentru salvare în fișier

2. **Metrici Trafic (25%)**
   - Bytes transferați în fiecare direcție
   - Durata conexiunilor
   - Throughput (bytes/secundă)
   - Număr maxim de conexiuni simultane

3. **Gestionare Conexiuni (25%)**
   - Limită maximă de conexiuni concurente
   - Timeout pentru conexiuni inactive
   - Închidere elegantă la Ctrl+C

4. **Afișare Status (20%)**
   - Afișare metrici la semnal SIGUSR1
   - Sau la comandă specială prin stdin

### Argumente Linie de Comandă

```bash
python tema_3_03.py \
    --port-ascultare 9090 \
    --host-tinta localhost \
    --port-tinta 8080 \
    --max-conexiuni 10 \
    --timeout 300 \
    --log-file tunel.log \
    --debug
```

### Criterii de Evaluare

| Criteriu | Punctaj |
|----------|---------|
| Logging complet cu nivele | 30% |
| Metrici corecte | 25% |
| Gestionare conexiuni solidă | 25% |
| Caracteristici opționale | 20% |

### Testare

```bash
# Porniți tunelul
python tema_3_03.py --port-ascultare 9090 --host-tinta localhost --port-tinta 8080 --max-conexiuni 5

# Testați cu multiple conexiuni
for i in {1..10}; do echo "Test $i" | nc localhost 9090 & done

# Verificați log-urile și metricile
```

---

## Instrucțiuni de Trimitere

### Format Fișiere

Fiecare fișier trebuie să înceapă cu:

```python
#!/usr/bin/env python3
"""
Tema 3.X: [Titlu]
Laborator Rețele de Calculatoare - ASE

Autor: [Numele Complet]
Grupă: [Grupa]
Data: [Data]
"""
```

### Ce Trebuie Trimis

1. Codul sursă (`.py`)
2. Captură Wireshark demonstrativă (opțional)
3. Fișier README cu instrucțiuni de rulare (dacă diferă)

### Cum Testați

```bash
# Asigurați-vă că laboratorul rulează
python scripts/porneste_lab.py --broadcast

# Rulați testele
python tests/test_exercitii.py

# Testați tema în containere
docker exec -it week3_client python3 /app/homework/exercises/tema_3_01.py
```

---

## Criterii Generale de Evaluare

### Calitatea Codului

- **Docstrings**: Documentați funcțiile și clasele
- **Type hints**: Folosiți adnotări de tip
- **Denumiri**: Variabile și funcții cu nume descriptive
- **Structură**: Cod organizat și modular

### Corectitudine Funcțională

- Programul rulează fără erori
- Toate cerințele sunt implementate
- Tratarea corectă a erorilor

### Bonus și Penalizări

- **+10%**: Implementare excepțională sau funcționalități extra
- **-10%**: Cod copiat fără înțelegere
- **-20%**: Trimis după termen limită (pe zi)

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*

---

## 🤝 Exerciții pentru Perechi (Pair Programming)

Aceste exerciții sunt concepute pentru lucru în echipă de 2 persoane.

### Pair Exercise 1: Debug the Broadcast

**Roluri:** Driver (scrie cod) + Navigator (ghidează, verifică)

**⚠️ Schimbați rolurile la fiecare 5 minute!**

**Situație:** Codul de mai jos NU funcționează. Receptorul nu primește nimic.

```python
# sender.py - COD CU PROBLEME
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"Hello", ('255.255.255.255', 5007))

# receiver.py - COD CU PROBLEME
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('172.20.0.100', 5007))
data = sock.recvfrom(1024)
print(data)
```

**Sarcină:**
1. **Navigator:** Identifică TOATE erorile (sunt exact 2)
2. **Driver:** Corectează codul
3. **Ambii:** Testați în containere Docker
4. **Schimbați rolurile** și explicați-vă reciproc DE CE au fost erori

<details>
<summary>Hint (deschide doar după 5 minute de încercări)</summary>

- Eroare 1: Emițătorul... (ce opțiune socket lipsește pentru broadcast?)
- Eroare 2: Receptorul face bind la... (ce adresă specială primește TOATE pachetele?)

</details>

<details>
<summary>Soluție completă (doar după rezolvare)</summary>

```python
# sender.py - CORECTAT
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # FIX 1
sock.sendto(b"Hello", ('255.255.255.255', 5007))

# receiver.py - CORECTAT
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5007))  # FIX 2: bind la toate interfețele
data = sock.recvfrom(1024)
print(data)
```

</details>

---

### Pair Exercise 2: Multicast Chat Mini

**Roluri:** Driver + Navigator (schimb la 10 minute)

**Sarcină:** Implementați împreună un mini-chat multicast:

**Runda 1 (Driver A, 10 min):** Scrie funcția de trimitere mesaje
- Grup: 239.0.0.50
- Port: 5050
- TTL: 1

**Runda 2 (Driver B, 10 min):** Scrie funcția de recepție cu IGMP join
- Bind la '' (toate interfețele)
- IP_ADD_MEMBERSHIP pentru grupul de mai sus

**Runda 3 (Ambii, 10 min):** Integrați și testați cu 2 terminale în containere diferite

**Cerințe minime:**
- Mesajele includ username-ul expeditorului
- Funcționează în containere Docker
- Receptorul afișează și timestamp-ul

**Discuție finală:** 
- Ce s-ar întâmpla dacă TTL=0?
- Dar TTL=255?
- De ce trebuie să faci bind ÎNAINTE de IP_ADD_MEMBERSHIP?

---

### Pair Exercise 3: Trace the Tunnel

**Tip:** Exercițiu de analiză (fără cod)

**Materiale necesare:** Wireshark + laboratorul pornit

**Sarcină:**
1. **Ambii:** Porniți Wireshark cu filtrul `tcp.port == 9090 || tcp.port == 8080`
2. **Driver:** Trimite 3 mesaje prin tunel: `echo "test1" | nc 172.20.0.254 9090`
3. **Navigator:** Numără și notează:
   - Câte pachete SYN vezi în total?
   - Câte conexiuni TCP separate există?
   - Care sunt IP-urile sursă și destinație pentru fiecare conexiune?
4. **Schimbați rolurile** și repetați cu alt mesaj
5. **Ambii:** Desenați diagrama conexiunilor pe hârtie

**Întrebări de verificare:**
- Serverul echo vede IP-ul clientului sau IP-ul tunelului?
- Ce se întâmplă în Wireshark când clientul trimite FIN?

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
