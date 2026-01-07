# Rezultate Așteptate - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Exercițiul 1: Broadcast UDP

### Output Emițător

```
==================================================
EMIȚĂTOR UDP BROADCAST
==================================================
Destinație: 255.255.255.255:5007
Mesaj: Mesaj broadcast de test
Număr mesaje: 5
--------------------------------------------------
[10:30:01.234] Trimis mesajul 1: 28 bytes
[10:30:02.235] Trimis mesajul 2: 28 bytes
[10:30:03.236] Trimis mesajul 3: 28 bytes
[10:30:04.237] Trimis mesajul 4: 28 bytes
[10:30:05.238] Trimis mesajul 5: 28 bytes
--------------------------------------------------
Transmisie completă: 5 mesaje trimise
```

### Output Receptor

```
==================================================
RECEPTOR UDP BROADCAST
==================================================
Ascultare pe: 0.0.0.0:5007
Apăsați Ctrl+C pentru oprire
--------------------------------------------------
[10:30:01.235] #1
  De la: 172.20.0.10:54321
  Lungime: 28 bytes
  Mesaj: [1/5] Mesaj broadcast de test

[10:30:02.236] #2
  De la: 172.20.0.10:54321
  Lungime: 28 bytes
  Mesaj: [2/5] Mesaj broadcast de test
...
```

### Filtre Wireshark

```
# Trafic broadcast pe portul 5007
udp.port == 5007

# Tot traficul broadcast
eth.dst == ff:ff:ff:ff:ff:ff

# Combinat
udp.port == 5007 and eth.dst == ff:ff:ff:ff:ff:ff
```

### Structura Pachetului

| Câmp | Valoare Așteptată |
|------|-------------------|
| IP Destinație | 255.255.255.255 |
| MAC Destinație | ff:ff:ff:ff:ff:ff |
| Protocol | UDP |
| Port Destinație | 5007 |
| Port Sursă | Efemer (>1024) |

---

## Exercițiul 2: Multicast UDP

### Output Emițător

```
==================================================
EMIȚĂTOR UDP MULTICAST
==================================================
Grup multicast: 239.0.0.1:5008
TTL: 1
Mesaj: Mesaj multicast de test
Număr mesaje: 5
--------------------------------------------------
[10:35:01.123] Trimis mesajul 1 către 239.0.0.1: 30 bytes
[10:35:02.124] Trimis mesajul 2 către 239.0.0.1: 30 bytes
...
```

### Output Receptor

```
==================================================
RECEPTOR UDP MULTICAST
==================================================
Grup multicast: 239.0.0.1
Port: 5008
Apăsați Ctrl+C pentru oprire
--------------------------------------------------
Înscris în grupul multicast 239.0.0.1
Așteptare mesaje...

[10:35:01.124] #1
  De la: 172.20.0.10:54322
  Lungime: 30 bytes
  Mesaj: [1/5] Mesaj multicast de test
...
```

### Verificare Înscrierea IGMP

```bash
# În container
docker exec week3_client cat /proc/net/igmp

# Output așteptat (ef000001 = 239.0.0.1 în hex little-endian)
2    eth0            : 1 00000000
                       1 EF000001
```

### Filtre Wireshark

```
# Trafic către grupul multicast
ip.dst == 239.0.0.1

# Mesaje IGMP
igmp

# IGMP Membership Report (înscriere)
igmp.type == 0x16

# IGMP Leave Group (părăsire)
igmp.type == 0x17

# Tot traficul multicast
ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255
```

### Comportament IGMP

| Eveniment | Mesaj IGMP | Tip |
|-----------|------------|-----|
| Receptor pornește | Membership Report | 0x16 |
| Router Query | Membership Query | 0x11 |
| Răspuns la Query | Membership Report | 0x16 |
| Receptor oprește | Leave Group | 0x17 |

### Structura Pachetului

| Câmp | Valoare Așteptată |
|------|-------------------|
| IP Destinație | 239.0.0.1 |
| MAC Destinație | 01:00:5e:00:00:01 |
| Protocol | UDP |
| Port Destinație | 5008 |
| TTL | 1 |

---

## Exercițiul 3: Tunel TCP

### Output Tunel

```
==================================================
TUNEL TCP BIDIRECȚIONAL
==================================================
Ascultare pe: 0.0.0.0:9090
Redirecționare către: 172.20.0.10:8080
Apăsați Ctrl+C pentru oprire
--------------------------------------------------
[10:40:01.001] [tunel] Tunel pornit, așteptare conexiuni...
[10:40:05.123] [conn-001] Nouă conexiune de la 172.20.0.100:54000
[10:40:05.130] [conn-001] Conectat la țintă 172.20.0.10:8080
[10:40:05.135] [conn-001] client→server: terminat, 15 bytes transferați
[10:40:05.136] [conn-001] server→client: terminat, 15 bytes transferați
[10:40:05.137] [conn-001] Conexiune închisă
```

### Test Manual

```bash
# Conexiune directă (pentru comparație)
$ echo "Test direct" | docker exec -i week3_client nc 172.20.0.10 8080
Test direct

# Conexiune prin tunel
$ echo "Test prin tunel" | docker exec -i week3_client nc 172.20.0.254 9090
Test prin tunel
```

### Filtre Wireshark

```
# Toate conexiunile tunelului
tcp.port == 9090 or tcp.port == 8080

# Conexiunea client-tunel
tcp.port == 9090

# Conexiunea tunel-server
tcp.port == 8080

# Urmărire flux TCP
tcp.stream eq 0
```

### Comportament Așteptat

| Scenariu | Comportament |
|----------|--------------|
| Mesaj simplu | Echo corect prin tunel |
| Mesaje multiple | Toate relayate în ordine |
| Payload mare (10KB) | Transfer complet |
| Client deconectează | Ambele conexiuni închise |
| Server indisponibil | Conexiune refuzată raportată |

### Structura Conexiunilor

```
Client (172.20.0.100:54000)
    │
    └──── TCP ────► Tunel (172.20.0.254:9090)
                         │
                         └──── TCP ────► Server (172.20.0.10:8080)

Două conexiuni TCP separate:
1. Client ↔ Tunel
2. Tunel ↔ Server
```

---

## Exercițiul 4: Analiză Wireshark

### Comenzi de Captură

```bash
# Folosind scriptul
python scripts/captureaza_trafic.py --container client --durata 60 --output captura_week3.pcap

# Direct cu tcpdump
docker exec week3_client tcpdump -i eth0 -w /tmp/captura.pcap

# Copiere din container
docker cp week3_client:/tmp/captura.pcap ./captura.pcap
```

### Statistici Așteptate

După rularea exercițiilor 1-3, captura ar trebui să conțină aproximativ:

| Tip Trafic | Număr Pachete |
|------------|---------------|
| Total | 100-500 |
| Broadcast UDP | 20-50 |
| Multicast UDP | 20-50 |
| IGMP | 2-10 |
| TCP (tunel) | 50-200 |

### Verificare în Wireshark

```
# Statistici protocol
Statistics → Protocol Hierarchy

# Conversații
Statistics → Conversations

# Endpoints
Statistics → Endpoints

# Flux TCP
Analyze → Follow → TCP Stream
```

---

## Probleme Frecvente și Soluții

### Broadcast: Permisiune refuzată (Windows)

```
OSError: [Errno 10013] Permission denied
```

**Soluție:** Rulați ca Administrator sau folosiți containerele Docker.

### Multicast: Mesajele nu sunt primite

```bash
# Verificați înscrierea în grup
docker exec week3_client cat /proc/net/igmp | grep 239
```

**Soluție:** Asigurați-vă că receptorul are IP_ADD_MEMBERSHIP setat corect.

### Tunel: Conexiune refuzată

```bash
# Verificați că serverul echo rulează
docker exec week3_server ss -tlnp | grep 8080
```

**Soluție:** Reporniți containerul server sau verificați configurația.

---

## Verificare Teste

Output așteptat pentru testele automate:

```
$ python tests/test_rapid.py

============================================================
TEST RAPID DE VERIFICARE - Săptămâna 3
============================================================

Verificări Docker:
----------------------------------------
✓ TRECUT Docker disponibil (0.52s)
✓ TRECUT Compose valid (0.31s)
✓ TRECUT Container server (0.12s)
✓ TRECUT Container router (0.11s)
✓ TRECUT Container client (0.11s)
✓ TRECUT Rețea Docker (0.15s)

Verificări Conectivitate:
----------------------------------------
✓ TRECUT Server echo răspunde (0.08s)
✓ TRECUT Tunel redirecționează (0.09s)

Verificări Socket-uri:
----------------------------------------
✓ TRECUT Socket broadcast (0.01s)
✓ TRECUT Join multicast (0.02s)

Verificări Instrumente:
----------------------------------------
✓ TRECUT tcpdump în container (0.45s)
✓ TRECUT Sintaxă scripturi (1.23s)

============================================================
REZULTAT: 12 trecute, 0 eșuate, 0 sărite
Timp total: 3.20s
============================================================

✓ PREGĂTIT PENTRU LABORATOR

Puteți începe exercițiile!
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
