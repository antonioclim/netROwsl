# Ieșiri Așteptate pentru Teste

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest document descrie ieșirile așteptate pentru fiecare exercițiu de laborator.

---

## Exercițiul 1: Inspectarea Interfețelor de Rețea

### Comandă: `ip addr show`

**Ieșire așteptată (exemplu):**
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0@if5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:ac:14:01:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.20.1.2/24 brd 172.20.1.255 scope global eth0
       valid_lft forever preferred_lft forever
```

**Ce să verificați:**
- ✓ Interfața `lo` există cu adresa 127.0.0.1
- ✓ Cel puțin o interfață de rețea este UP
- ✓ Adresele IP sunt afișate corect

---

## Exercițiul 2: Testarea Conectivității

### Comandă: `ping -c 4 127.0.0.1`

**Ieșire așteptată:**
```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.025 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.031 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.029 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.028 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3062ms
rtt min/avg/max/mdev = 0.025/0.028/0.031/0.002 ms
```

**Ce să verificați:**
- ✓ 0% pierdere de pachete
- ✓ Timp de răspuns (RTT) sub 1ms pentru loopback
- ✓ Toate cele 4 pachete primite

---

## Exercițiul 3: Comunicarea TCP

### Script: `ex_1_02_tcp_server_client.py`

**Ieșire așteptată:**
```
╔══════════════════════════════════════════════════════════════╗
║  EXERCIȚIUL 2: SERVER-CLIENT TCP                             ║
║  Curs REȚELE DE CALCULATOARE - ASE, Informatică              ║
╚══════════════════════════════════════════════════════════════╝

Se pornește serverul TCP pe portul 9999...
[Server] Ascult pe 0.0.0.0:9999

Se pornește clientul TCP...
[Client] Conectat la 127.0.0.1:9999
[Server] Conexiune acceptată de la ('127.0.0.1', XXXXX)

[Client] Trimis: Salut de la client! (Mesaj 1)
[Server] Primit: Salut de la client! (Mesaj 1)
[Server] Trimis: Confirmare: Salut de la client! (Mesaj 1)
[Client] Primit: Confirmare: Salut de la client! (Mesaj 1)

...

Comunicare finalizată cu succes!
```

**Ce să verificați:**
- ✓ Serverul pornește fără erori
- ✓ Clientul se conectează
- ✓ Mesajele sunt transmise și recepționate corect
- ✓ Conexiunea se închide grațios

---

## Exercițiul 4: Captura de Trafic

### Comandă: `tcpdump -i lo -c 10`

**Ieșire așteptată (exemplu):**
```
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
12:34:56.123456 IP localhost.9999 > localhost.12345: Flags [S], seq 12345678, win 65535, ...
12:34:56.123457 IP localhost.12345 > localhost.9999: Flags [S.], seq 87654321, ack 12345679, ...
12:34:56.123458 IP localhost.9999 > localhost.12345: Flags [.], ack 1, win 65535, ...
...
10 packets captured
10 packets received by filter
0 packets dropped by kernel
```

**Ce să verificați:**
- ✓ tcpdump pornește fără erori de permisiuni
- ✓ Pachetele sunt capturate
- ✓ Flag-urile TCP sunt vizibile (S=SYN, .=ACK)

---

## Exercițiul 5: Analiza PCAP

### Script: `ex_1_04_statistici_pcap.py`

**Ieșire așteptată:**
```
╔══════════════════════════════════════════════════════════════╗
║  STATISTICI PCAP                                             ║
╚══════════════════════════════════════════════════════════════╝

Fișier: captura_test.pcap
────────────────────────────────────────────────────────────────

REZUMAT GENERAL:
  Total pachete:          100
  Total octeți:           15,234
  Dimensiune medie:       152.3 octeți/pachet
  Durată captură:         5.23 secunde
  Rata de transfer:       2,912.4 octeți/s

DISTRIBUȚIE PROTOCOALE:
  TCP                          85 (85.0%)
  UDP                          10 (10.0%)
  ICMP                          5 ( 5.0%)

TOP 5 ADRESE SURSĂ:
  127.0.0.1                    50 pachete
  172.20.1.2                   30 pachete
  ...
```

**Ce să verificați:**
- ✓ Fișierul PCAP este citit corect
- ✓ Statisticile sunt calculate
- ✓ Protocoalele sunt identificate
- ✓ Adresele IP sunt extrase

---

## Coduri de Ieșire Așteptate

| Script | Cod Succes | Cod Eroare |
|--------|------------|------------|
| test_mediu.py | 0 | 1 |
| test_exercitii.py | 0 | 1 |
| test_rapid.py | 0 | 1 |
| porneste_lab.py | 0 | 1 |
| opreste_lab.py | 0 | 1 |

---

## Verificare Automată

Rulați suita completă de teste:

```bash
python tests/test_mediu.py && \
python tests/test_exercitii.py && \
echo "Toate testele au trecut!"
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
