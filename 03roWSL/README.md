# Săptămâna 3: Programare în Rețea - Broadcast, Multicast și Tunel TCP

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
>
> by Revolvix

## Prezentare Generală

Această sesiune de laborator explorează mecanismele fundamentale de comunicare în rețea prin intermediul programării cu socket-uri: transmisia broadcast, comunicarea multicast și tunelarea TCP. Aceste paradigme reprezintă piloni esențiali ai arhitecturilor distribuite moderne, de la descoperirea serviciilor în rețele locale până la sisteme multimedia și infrastructuri VPN.

Transmisia **broadcast** permite unui singur emițător să comunice simultan cu toate dispozitivele dintr-un segment de rețea, eliminând necesitatea cunoașterii prealabile a destinatarilor. **Multicast** extinde acest concept prin crearea grupurilor de interes, unde doar stațiile membre primesc traficul, optimizând astfel utilizarea lățimii de bandă. **Tunelarea TCP** oferă mecanisme de redirecționare transparentă a conexiunilor, fundamentale pentru proxy-uri, load balancere și rețele virtuale private.

Exercițiile practice utilizează containere Docker pentru simularea unei topologii de rețea izolate, permițând observarea comportamentului protocoalelor fără a afecta infrastructura reală. Analiza pachetelor cu Wireshark completează înțelegerea teoretică prin vizualizarea directă a structurii cadrelor și fluxurilor de date.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** diferențele dintre comunicarea unicast, broadcast și multicast la nivel conceptual și practic
2. **Explicați** mecanismul IGMP pentru gestionarea apartenenței la grupuri multicast și rolul TTL în propagarea pachetelor
3. **Implementați** aplicații client-server folosind socket-uri UDP cu opțiuni SO_BROADCAST și IP_ADD_MEMBERSHIP
4. **Construiți** un tunel TCP bidirecțional pentru redirecționarea transparentă a conexiunilor între endpoint-uri
5. **Analizați** traficul de rețea capturat, identificând tipare specifice broadcast-ului, multicast-ului și tunelării
6. **Evaluați** avantajele și dezavantajele fiecărei paradigme de comunicare în scenarii practice

## Cerințe Preliminare

### Cunoștințe Necesare
- Fundamentele modelului TCP/IP și adresării IPv4
- Programare Python de bază (funcții, clase, module)
- Diferențele dintre protocoalele TCP și UDP
- Utilizarea liniei de comandă (PowerShell, Bash)

### Cerințe Software
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git (opțional, recomandat)

### Cerințe Hardware
- Minimum 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK3_WSLkit_RO

# Verificați cerințele preliminare
python setup/verifica_mediu.py

# Dacă există probleme, rulați asistentul de instalare
python setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```powershell
# Porniți toate serviciile
python scripts/porneste_lab.py

# Verificați că totul funcționează
python scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se configurează la prima accesare |
| Server Echo | localhost:8080 | - |
| Tunel TCP | localhost:9090 | - |
| Receiver Broadcast | 172.20.0.101:5007 | - |

## Exerciții de Laborator

### Exercițiul 1: Transmisie UDP Broadcast

**Obiectiv:** Implementarea și testarea comunicării broadcast folosind socket-uri UDP cu opțiunea SO_BROADCAST.

**Durată estimată:** 30 minute

**Fundament teoretic:**
Broadcast-ul permite transmiterea unui singur pachet către toate stațiile dintr-un segment de rețea. Adresa de broadcast limitat (255.255.255.255) nu traversează routere, fiind confinată la rețeaua locală. Socket-urile necesită activarea explicită a opțiunii SO_BROADCAST pentru a permite astfel de transmisii.

**Pași:**

1. Porniți containerul receiver într-un terminal:
   ```bash
   docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod receiver
   ```

2. Într-un alt terminal, porniți emițătorul:
   ```bash
   docker exec -it week3_server python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod sender --numar 5
   ```

3. Observați mesajele primite și notați:
   - Adresa sursă a pachetelor
   - Timpul de propagare
   - Comportamentul când multiple receivere sunt active

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 1
```

**Întrebări de reflecție:**
- De ce este necesară opțiunea SO_BROADCAST?
- Ce se întâmplă dacă adresa de broadcast este înlocuită cu o adresă unicast?

---

### Exercițiul 2: Comunicare UDP Multicast

**Obiectiv:** Configurarea socket-urilor pentru comunicare multicast și înțelegerea mecanismului IGMP de înscriere în grupuri.

**Durată estimată:** 35 minute

**Fundament teoretic:**
Multicast-ul permite comunicarea eficientă unul-la-mulți prin utilizarea adreselor din intervalul 224.0.0.0 - 239.255.255.255. Receptorii se înscriu în grupuri folosind protocolul IGMP (Internet Group Management Protocol), iar rețeaua livrează pachetele doar membrilor activi. Spre deosebire de broadcast, multicast-ul poate traversa routere configurate corespunzător.

**Pași:**

1. Porniți primul receptor:
   ```bash
   docker exec -it week3_client python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver
   ```

2. Porniți al doilea receptor (terminal separat):
   ```bash
   docker exec -it week3_receiver python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver
   ```

3. Transmiteți mesaje către grup:
   ```bash
   docker exec -it week3_server python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod sender --numar 5
   ```

4. Verificați înscrierea în grup IGMP:
   ```bash
   docker exec week3_client cat /proc/net/igmp
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 2
```

**Întrebări de reflecție:**
- Care este diferența dintre broadcast și multicast din perspectiva eficienței rețelei?
- Ce rol joacă TTL în propagarea pachetelor multicast?

---

### Exercițiul 3: Tunel TCP Bidirecțional

**Obiectiv:** Construirea unui releu TCP care redirecționează transparent conexiunile între client și server.

**Durată estimată:** 40 minute

**Fundament teoretic:**
Tunelarea TCP implică acceptarea conexiunilor pe un port și redirecționarea traficului către o destinație diferită. Acest pattern este fundamental pentru proxy-uri, load balancere și gateway-uri de securitate. Implementarea corectă necesită gestionarea bidirecțională a datelor și tratarea elegantă a deconectărilor.

**Pași:**

1. Verificați că serverul echo funcționează:
   ```bash
   echo "Test direct" | docker exec -i week3_client nc 172.20.0.10 8080
   ```

2. Testați conexiunea prin tunel:
   ```bash
   echo "Test prin tunel" | docker exec -i week3_client nc 172.20.0.254 9090
   ```

3. Examinați codul tunelului și identificați:
   - Cum se creează conexiunea către server
   - Cum se gestionează traficul bidirecțional
   - Cum se tratează deconectările

4. Monitorizați conexiunile active:
   ```bash
   docker exec week3_router ss -tnp
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 3
```

**Întrebări de reflecție:**
- De ce este necesară utilizarea thread-urilor pentru relay-ul bidirecțional?
- Ce avantaje oferă un tunel TCP față de conexiunea directă?

---

### Exercițiul 4: Analiză cu Wireshark

**Obiectiv:** Capturarea și analiza traficului de rețea pentru identificarea tiparelor specifice fiecărui tip de comunicare.

**Durată estimată:** 25 minute

**Pași:**

1. Porniți captura de trafic:
   ```powershell
   python scripts/captureaza_trafic.py --container server --durata 60 --output pcap/analiza_week3.pcap
   ```

2. În timpul capturii, executați exercițiile 1-3

3. Deschideți fișierul pcap în Wireshark și aplicați filtrele:
   ```
   # Trafic broadcast
   eth.dst == ff:ff:ff:ff:ff:ff
   
   # Trafic multicast
   ip.dst >= 239.0.0.0 and ip.dst <= 239.255.255.255
   
   # Mesaje IGMP
   igmp
   
   # Trafic tunel
   tcp.port == 9090 or tcp.port == 8080
   ```

4. Documentați observațiile pentru fiecare tip de trafic

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 4
```

## Demonstrații

### Demo 1: Broadcast în Acțiune

Demonstrație automată care ilustrează propagarea mesajelor broadcast către multiple receptoare.

```powershell
python scripts/ruleaza_demo.py --demo broadcast
```

**Ce trebuie observat:**
- Toate containerele primesc același mesaj simultan
- Adresa MAC destinație este ff:ff:ff:ff:ff:ff
- Nu există confirmare de primire (UDP)

### Demo 2: Grupuri Multicast

Demonstrație a înscrierii și comunicării în grupuri multicast.

```powershell
python scripts/ruleaza_demo.py --demo multicast
```

**Ce trebuie observat:**
- Rapoartele IGMP la înscriere și părăsire
- Doar membrii grupului primesc mesaje
- Adresa IP destinație este în intervalul multicast

### Demo 3: Tunelare TCP

Demonstrație a redirecționării transparente prin tunel.

```powershell
python scripts/ruleaza_demo.py --demo tunel
```

**Ce trebuie observat:**
- Două conexiuni TCP separate (client-tunel, tunel-server)
- Datele sunt relayate transparent
- Conexiunile se închid sincronizat

## Captură și Analiză Pachete

### Capturarea Traficului

```powershell
# Pornire captură
python scripts/captureaza_trafic.py --container eth0 --output pcap/captura_week3.pcap

# Sau folosind Wireshark direct
# Deschideți Wireshark > Selectați interfața WSL/Docker
```

### Filtre Wireshark Recomandate

```
# Broadcast UDP
udp and eth.dst == ff:ff:ff:ff:ff:ff

# Multicast specific
ip.dst == 239.0.0.1 and udp.port == 5008

# Tot traficul laboratorului
ip.addr == 172.20.0.0/24

# Trafic TCP tunel
tcp.port == 8080 or tcp.port == 9090
```

## Oprire și Curățare

### Sfârșitul Sesiunii

```powershell
# Opriți toate containerele (păstrează datele)
python scripts/opreste_lab.py

# Verificați oprirea
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python scripts/curata.py --complet

# Verificați curățarea
docker system df
```

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de rezolvat acasă.

### Tema 1: Receiver Broadcast cu Statistici
Extindeți receiver-ul UDP pentru a colecta și afișa statistici detaliate despre traficul primit.

### Tema 2: Aplicație Chat Multicast
Implementați o aplicație de chat bazată pe multicast cu suport pentru mai mulți utilizatori.

### Tema 3: Tunel TCP cu Logging și Metrici
Îmbunătățiți tunelul TCP cu logging detaliat, metrici de performanță și limite de conexiuni.

## Depanare

### Probleme Frecvente

#### Eroare: `OSError: [Errno 10013] Permission denied`
**Soluție:** Rulați ca Administrator sau folosiți containerele Docker unde permisiunile sunt deja configurate.

#### Eroare: `Address already in use`
**Soluție:** Opriți procesele anterioare sau reporniți containerul:
```bash
docker restart week3_server
```

#### Mesajele broadcast nu sunt primite
**Soluție:** Verificați că receiver-ul este legat la `0.0.0.0`, nu la o adresă IP specifică.

#### Multicast nu funcționează
**Soluție:** Verificați înscrierea în grup:
```bash
docker exec week3_client cat /proc/net/igmp | grep 239
```

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundament Teoretic

### Broadcast vs Multicast vs Unicast

| Caracteristică | Unicast | Broadcast | Multicast |
|---------------|---------|-----------|-----------|
| Destinatari | Unul | Toți din segment | Membrii grupului |
| Eficiență | O copie/destinatar | O copie/segment | O copie/grup |
| Traversare routere | Da | Nu (limitat) | Da (cu suport) |
| Adresă exemplu | 172.20.0.10 | 255.255.255.255 | 239.0.0.1 |

### Opțiuni Socket Relevante

- **SO_BROADCAST**: Permite transmisia broadcast
- **SO_REUSEADDR**: Permite rebindarea rapidă a portului
- **IP_ADD_MEMBERSHIP**: Înscrie socket-ul într-un grup multicast
- **IP_MULTICAST_TTL**: Controlează propagarea multicast
- **IP_MULTICAST_LOOP**: Controlează primirea propriilor mesaje

### Structura IGMP

Internet Group Management Protocol gestionează apartenenţa la grupuri multicast:
- **Membership Query**: Router-ul întreabă ce grupuri sunt active
- **Membership Report**: Stația raportează apartenența la grup
- **Leave Group**: Stația notifică părăsirea grupului

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 919 - Broadcasting Internet Datagrams
- RFC 1112 - Host Extensions for IP Multicasting
- RFC 2236 - Internet Group Management Protocol, Version 2

## Diagrama Arhitecturii

```
┌─────────────────────────────────────────────────────────────────┐
│                      Rețea Docker: 172.20.0.0/24                │
│                                                                 │
│   ┌─────────────┐         ┌─────────────┐         ┌───────────┐│
│   │   SERVER    │         │   ROUTER    │         │  CLIENT   ││
│   │ 172.20.0.10 │◄────────│172.20.0.254 │◄────────│172.20.0.100│
│   │  Port 8080  │  Tunel  │  Port 9090  │         │ (testare) ││
│   │ (Echo TCP)  │         │ (Relay TCP) │         │           ││
│   └─────────────┘         └─────────────┘         └───────────┘│
│                                                                 │
│                           ┌─────────────┐                       │
│                           │  RECEIVER   │                       │
│                           │172.20.0.101 │                       │
│                           │  Port 5007  │                       │
│                           │(Broadcast/  │                       │
│                           │ Multicast)  │                       │
│                           └─────────────┘                       │
│                                                                 │
│   ════════════════════════════════════════════════════════════  │
│   Broadcast: 255.255.255.255:5007  │  Multicast: 239.0.0.1:5008 │
└─────────────────────────────────────────────────────────────────┘
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
