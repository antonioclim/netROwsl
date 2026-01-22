# Întrebări Frecvente (FAQ)

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

---

## Configurare și Instalare

### Q: "Cannot connect to Docker daemon" - ce fac?

**R:** Docker nu rulează. În terminalul WSL Ubuntu:

```bash
sudo service docker start
# Parolă: stud

# Verifică că funcționează
docker ps
```

Dacă tot nu merge:
```bash
# Verifică statusul detaliat
sudo service docker status

# Repornește complet
sudo service docker restart
```

---

### Q: Am uitat parola Portainer. Cum o resetez?

**R:** Resetează Portainer complet (nu afectează celelalte containere):

```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Recreează - vei seta o parolă nouă la prima accesare
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

Apoi accesează http://localhost:9000 și setează parola nouă.

---

### Q: Portul 5400 e deja ocupat. Ce fac?

**R:** Găsește ce îl folosește:

```bash
# În WSL
sudo ss -tlnp | grep 5400

# Sau
sudo lsof -i :5400
```

Apoi oprește procesul respectiv sau schimbă portul în `docker/docker-compose.yml`:

```yaml
ports:
  - "5410:5400"  # Folosește 5410 în loc de 5400 pe host
```

---

### Q: WSL nu vede folderul D:\RETELE

**R:** Verifică că unitatea e montată:

```bash
ls /mnt/d/

# Dacă nu există, montează manual
sudo mkdir -p /mnt/d
sudo mount -t drvfs D: /mnt/d
```

---

### Q: Docker spune "permission denied"

**R:** Adaugă utilizatorul la grupul docker:

```bash
sudo usermod -aG docker $USER

# Aplică imediat (sau deconectează/reconectează)
newgrp docker

# Verifică
docker ps
```

---

## Protocoale

### Q: De ce CRC32 și nu MD5 sau SHA?

**R:** CRC32 și hash-urile criptografice au scopuri diferite:

| Proprietate | CRC32 | MD5/SHA |
|-------------|-------|---------|
| Scop principal | Detectare erori accidentale | Verificare integritate + securitate |
| Viteză | Foarte rapid | Mai lent |
| Rezistență la manipulare | Nulă | Ridicată |
| Lungime output | 32 biți | 128/256+ biți |
| Utilizare tipică | Ethernet, ZIP, protocoale | Semnături digitale, parole |

CRC32 e perfect pentru detectarea erorilor de transmisie (corupere accidentală), dar nu oferă nicio protecție împotriva modificărilor intenționate.

---

### Q: De ce antetul BINAR are fix 14 bytes?

**R:** Dimensiunea fixă simplifică parsarea:

1. **Știi exact câți bytes să citești** - nu trebuie să cauți delimitatori
2. **Poți prealoca buffer-ul** - eficiență la nivel de memorie
3. **Parsare O(1)** - accesezi direct orice câmp prin offset
4. **Recuperare din erori** - dacă pierzi sincronizarea, cauți Magic-ul

Structura de 14 bytes e un compromis între informație și overhead:
- 2B Magic + 1B Versiune + 1B Tip + 2B Lungime + 4B Secvență + 4B CRC = 14B

---

### Q: UDP nu e nesigur? De ce îl folosim?

**R:** UDP nu garantează livrarea, dar are avantaje majore pentru anumite aplicații:

**Avantaje UDP:**
- Overhead mic (8 bytes vs ~40 pentru TCP)
- Fără handshake (latență mai mică)
- Fără stare de conexiune (scalabilitate)
- Fire-and-forget (simplitate)

**Pentru senzori IoT pe baterie:**
- O citire pierdută nu e critică (vine alta în câteva secunde)
- Economie de energie (mai puține pachete)
- Implementare mai simplă

**Când NU folosești UDP:**
- Date critice care trebuie să ajungă (folosește TCP)
- Ordine importantă (TCP garantează ordinea)
- Transfer de fișiere (TCP cu retransmisie)

---

### Q: Ce înseamnă "Network Byte Order"?

**R:** E o convenție pentru ordinea bytes-ilor în protocoale de rețea.

**Problema:** Calculatoarele stochează numerele diferit:
- **Little-endian** (x86, ARM): byte-ul mai puțin semnificativ primul
- **Big-endian** (rețea): byte-ul mai semnificativ primul

**Exemplu pentru 0x12345678:**
```
Little-endian: [78] [56] [34] [12]  (cum stochează PC-ul tău)
Big-endian:    [12] [34] [56] [78]  (cum trebuie în rețea)
```

**În Python:**
```python
import struct

# GREȘIT (ordinea sistemului):
struct.pack('I', 0x12345678)  # → b'xV4\x12' pe x86

# CORECT (network order):
struct.pack('!I', 0x12345678)  # → b'\x124Vx' (big-endian)
```

---

### Q: Cum știu dacă CRC-ul e calculat corect?

**R:** Folosește o valoare de test cunoscută:

```python
import binascii

# Valoare standard de verificare CRC32
# CRC32("123456789") = 0xCBF43926
test = binascii.crc32(b"123456789") & 0xFFFFFFFF
print(f"0x{test:08X}")  # Trebuie să fie 0xCBF43926

if test == 0xCBF43926:
    print("CRC32 funcționează corect!")
else:
    print("EROARE: implementare CRC incorectă")
```

---

## Exerciții și Teme

### Q: Cum testez fără serverul Docker pornit?

**R:** Poți rula serverele direct în Python (mod nativ):

```bash
# Terminal 1 - Pornește serverul TEXT
python3 src/apps/text_proto_server.py

# Terminal 2 - Rulează clientul
python3 src/apps/text_proto_client.py
```

Sau folosește scriptul cu opțiunea `--native`:
```bash
python3 scripts/start_lab.py --native
```

---

### Q: Unde găsesc soluțiile la exerciții?

**R:** Soluțiile complete sunt disponibile doar pentru instructor prin canalele oficiale ale cursului.

Pentru auto-verificare:
1. Testele din `tests/` validează funcționalitatea
2. Serverele returnează mesaje de eroare descriptive
3. Wireshark arată exact ce se trimite/primește

---

### Q: Exercițiul meu nu trece testele. Cum depanez?

**R:** Pași de debugging:

1. **Rulează manual** și observă output-ul:
   ```bash
   python3 src/exercises/ex1_text_client.py
   ```

2. **Adaugă print-uri**:
   ```python
   print(f"Trimit: {mesaj!r}")
   print(f"Primit: {raspuns!r}")
   ```

3. **Capturează în Wireshark** și compară cu protocolul

4. **Verifică CRC** dacă lucrezi cu BINAR:
   ```python
   print(f"CRC: 0x{crc:08X}")
   ```

---

## Wireshark

### Q: Nu văd pachete în Wireshark. Ce fac?

**R:** Checklist:

1. **Interfața corectă?** - Selectează "vEthernet (WSL)"
2. **Captura e pornită?** - Butonul albastru (aripioara de rechin), nu roșu
3. **Filtrul ascunde?** - Șterge filtrul temporar și vezi dacă apar pachete
4. **Generezi trafic?** - Rulează clientul ÎN TIMPUL capturii, nu înainte

---

### Q: Filtrul devine roșu. De ce?

**R:** Eroare de sintaxă. Exemple corecte vs greșite:

| Corect | Greșit |
|--------|--------|
| `tcp.port == 5400` | `tcp.port = 5400` (un singur =) |
| `tcp contains "PING"` | `tcp contains 'PING'` (ghilimele simple) |
| `udp.port == 5402` | `port == 5402` (lipsește udp) |
| `tcp.port == 5400 and tcp.flags.syn == 1` | `tcp.port == 5400 AND tcp.flags.syn == 1` (AND majuscule) |

---

### Q: Cum export o captură pentru temă?

**R:** 

1. File → Save As → `captura_tema.pcapng`
2. Sau pentru filtrare: File → Export Specified Packets → selectează "Displayed"

---

## Erori Comune

### Q: "Connection refused" - ce înseamnă?

**R:** Serverul nu ascultă pe portul respectiv. Verifică:

```bash
# Containerul rulează?
docker ps | grep saptamana4

# Portul e deschis?
nc -zv localhost 5400
```

---

### Q: "Address already in use" - cum rezolv?

**R:** Alt proces folosește portul. Găsește-l și oprește-l:

```bash
sudo ss -tlnp | grep 5400
# Notează PID-ul
kill -9 <PID>

# Sau oprește toate containerele
docker compose down
```

---

### Q: Python spune "struct.error: unpack requires a buffer of X bytes"

**R:** Nu ai primit suficiente date. Cauze:
- Conexiunea s-a închis prematur
- Serverul a trimis mai puțin decât așteptai
- Buffer-ul de receive e prea mic

Soluție: verifică lungimea înainte de unpack:
```python
date = sock.recv(1024)
if len(date) < 14:
    print(f"Date insuficiente: {len(date)} bytes")
else:
    # Acum e sigur să faci unpack
    header = struct.unpack('!2sBBHII', date[:14])
```

---

## Alte Întrebări

### Q: Pot folosi alt limbaj în loc de Python?

**R:** Da, protocoalele sunt independente de limbaj. Ai nevoie de:
- Socket TCP/UDP
- Funcție de calcul CRC32
- Împachetare/despachetare binară

Exemple în alte limbaje sunt disponibile în [Lectură Suplimentară](further_reading.md).

---

### Q: De ce trebuie să folosesc WSL? Nu merge direct pe Windows?

**R:** Merge și direct pe Windows, dar WSL oferă:
- Consistență cu serverele Linux reale
- Acces la utilitare Unix (nc, ss, tcpdump)
- Docker Desktop se integrează nativ
- Comenzile din curs funcționează fără modificări

---

### Q: Cum raportez o problemă cu materialele?

**R:** 
1. Verifică mai întâi acest FAQ și [Troubleshooting](troubleshooting.md)
2. Descrie exact: ce ai încercat, ce ai așteptat, ce s-a întâmplat
3. Include output-ul complet al erorilor
4. Contactează asistentul de laborator sau folosește forumul cursului

---

## Referințe

- [README principal](../README.md)
- [Ghid Debugging](debugging_guide.md)
- [Troubleshooting](troubleshooting.md)
- [Lectură Suplimentară](further_reading.md)

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
