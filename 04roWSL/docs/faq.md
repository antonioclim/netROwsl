# Întrebări Frecvente (FAQ)

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest document conține cele mai frecvente întrebări. Pentru detalii suplimentare, consultă [FAQ Extins](faq_extended.md).

---

## Docker și Containere

### 1. "Cannot connect to Docker daemon" — ce fac?

Docker nu rulează. În terminalul WSL Ubuntu:

```bash
sudo service docker start
# Parolă: stud

docker ps  # Verifică că funcționează
```

### 2. Portul 5400/5401/5402 e deja ocupat

Găsește ce îl folosește și oprește:

```bash
sudo ss -tlnp | grep 5400
docker compose down  # Oprește toate containerele
```

### 3. Docker spune "permission denied"

Adaugă utilizatorul la grupul docker:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 4. Am uitat parola Portainer

Resetează Portainer: `docker stop portainer && docker rm portainer && docker volume rm portainer_data`. Apoi recreează containerul și setează parolă nouă.

---

## Protocoale și CRC

### 5. De ce CRC32 și nu MD5 sau SHA?

CRC32 e pentru detectarea erorilor accidentale de transmisie — rapid și eficient. Hash-urile criptografice (MD5, SHA) sunt pentru verificarea integrității cu rezistență la manipulare intenționată. CRC nu oferă securitate!

### 6. Ce înseamnă "Network Byte Order"?

Ordinea big-endian (byte-ul mai semnificativ primul) folosită în protocoale de rețea. În Python, folosește `!` în struct.pack: `struct.pack('!I', valoare)`.

### 7. Cum verific că CRC-ul e calculat corect?

CRC32 pentru `"123456789"` trebuie să fie `0xCBF43926`:

```python
import binascii
assert binascii.crc32(b"123456789") & 0xFFFFFFFF == 0xCBF43926
```

### 8. De ce antetul BINAR are fix 14 bytes?

Dimensiune fixă = parsare O(1), prealoc buffer, acces direct prin offset. Structura: 2B Magic + 1B Versiune + 1B Tip + 2B Lungime + 4B Secvență + 4B CRC = 14B.

### 9. UDP nu e nesigur? De ce îl folosim pentru senzori?

Pentru senzori IoT: overhead mic (economie baterie), fără handshake (latență mică), o citire pierdută nu e critică (vine alta în câteva secunde).

---

## Wireshark

### 10. Nu văd pachete în Wireshark

Checklist: 1) Interfața corectă? (selectează "vEthernet (WSL)"), 2) Captura pornită? (buton albastru), 3) Filtrul ascunde? (șterge-l temporar), 4) Generezi trafic ÎN TIMPUL capturii?

### 11. Filtrul devine roșu — eroare de sintaxă

Exemple corecte: `tcp.port == 5400` (dublu =), `tcp contains "PING"` (ghilimele duble). Greșite: `tcp.port = 5400`, `tcp contains 'PING'`.

### 12. Cum export o captură pentru temă?

File → Save As → `captura_tema.pcapng`. Pentru doar pachetele filtrate: File → Export Specified Packets → selectează "Displayed".

---

## Erori Comune

### 13. "Connection refused"

Serverul nu ascultă. Verifică: `docker ps | grep saptamana4` și `nc -zv localhost 5400`.

### 14. "Address already in use"

Alt proces folosește portul: `sudo ss -tlnp | grep 5400`, apoi `docker compose down`.

### 15. "struct.error: unpack requires X bytes"

Nu ai primit suficiente date. Verifică lungimea înainte de unpack:

```python
date = sock.recv(1024)
if len(date) < 14:
    print(f"Date insuficiente: {len(date)} bytes")
```

### 16. CRC invalid la fiecare mesaj

Verifică: 1) Folosești `!` pentru network byte order? 2) CRC calculat peste datele corecte? 3) Lungimea payload-ului e corectă?

---

## Configurare și WSL

### 17. WSL nu vede folderul D:\RETELE

```bash
ls /mnt/d/
# Dacă nu există:
sudo mkdir -p /mnt/d && sudo mount -t drvfs D: /mnt/d
```

### 18. Pot testa fără Docker?

Da, rulează serverele direct în Python:

```bash
python3 src/apps/text_proto_server.py  # Terminal 1
python3 src/apps/text_proto_client.py  # Terminal 2
```

### 19. Pot folosi alt limbaj în loc de Python?

Da, protocoalele sunt independente de limbaj. Ai nevoie de: socket TCP/UDP, funcție CRC32, împachetare binară.

### 20. Unde găsesc soluțiile la exerciții?

Soluțiile complete sunt disponibile doar prin canalele oficiale. Pentru auto-verificare: testele din `tests/`, mesajele de eroare ale serverului, Wireshark.

---

## Vezi și

- [Troubleshooting](troubleshooting.md) — Ghid pas cu pas pentru probleme
- [Debugging Guide](debugging_guide.md) — Tehnici de debugging
- [Glossar](glossar.md) — Termeni tehnici

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
