# Întrebări Frecvente (FAQ)

> Laborator Săptămâna 13 - IoT și Securitate
>
> Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

---

## Generale

### De ce folosim Docker în loc de mașini virtuale?

Containerele Docker sunt mai eficiente decât VM-urile:
- **Dimensiune:** MB vs GB
- **Pornire:** secunde vs minute
- **Resurse:** partajează kernel-ul host-ului

Pentru laborator, nu avem nevoie de izolare completă la nivel de kernel — containerele oferă suficientă separare pentru experimente de rețea.

### Trebuie să știu Docker pentru acest laborator?

Nu în profunzime. Toate comenzile necesare sunt documentate pas-cu-pas, iar scripturile Python automatizează operațiile comune. Vei învăța Docker gradual prin utilizare.

### Ce fac dacă am ratat laboratorul anterior?

Fiecare laborator este relativ independent. Revizuiește:
1. `README.md` — pentru configurarea mediului
2. `docs/sumar_teorie.md` — pentru conceptele teoretice
3. Rulează `python scripts/porneste_lab.py` pentru a verifica că totul funcționează

---

## MQTT

### Ce este un "broker" MQTT?

Broker-ul este intermediarul central care:
- Primește mesaje de la **publisheri** (ex: senzori)
- Le distribuie către **subscriberi** (ex: aplicații dashboard)
- Gestionează topicurile și conexiunile

În laborator, broker-ul este containerul `week13_mosquitto` (Eclipse Mosquitto).

### De ce QoS 2 nu garantează livrare instantă?

QoS 2 garantează că mesajul ajunge **EXACT O DATĂ**, nu că ajunge **IMEDIAT**.

Dacă rețeaua este întreruptă:
- Mesajul este păstrat local
- Va fi livrat când conexiunea revine
- Protocolul în 4 pași previne duplicatele

### Care este diferența între QoS 0, 1 și 2?

| QoS | Garanție | Overhead | Când să folosești |
|-----|----------|----------|-------------------|
| 0 | Cel mult o dată (poate pierde) | Minim | Telemetrie frecventă, pierderi OK |
| 1 | Cel puțin o dată (posibil duplicat) | Mediu | Alertări, date importante |
| 2 | Exact o dată | Maxim | Comenzi critice, tranzacții |

### Pot vedea conținutul mesajelor MQTT în Wireshark?

Depinde de port:
- **Port 1883 (text clar):** DA — payload-ul este vizibil în clar
- **Port 8883 (TLS):** NU — traficul apare ca "Application Data" criptat

Aceasta este demonstrația practică a importanței TLS.

### Ce sunt wildcards în topicuri MQTT?

Permit abonarea la multiple topicuri simultan:
- `+` înlocuiește **un singur nivel**: `senzori/+/temp` → `senzori/camera1/temp`, `senzori/camera2/temp`
- `#` înlocuiește **orice număr de niveluri**: `senzori/#` → toate topicurile sub `senzori/`

---

## Securitate

### Backdoor-ul din vsftpd este real?

**NU.** Este o **SIMULARE educațională**.

Vulnerabilitatea reală (CVE-2011-2523) a existat în vsftpd 2.3.4 și permitea executarea de cod arbitrar. Noi simulăm doar comportamentul pentru a învăța tehnici de detectare, fără riscuri reale.

### Este legal să scanez porturi?

- **În laborator (localhost, containere proprii):** DA — este mediul tău controlat
- **Pe sisteme externe fără autorizare explicită:** NU — este infracțiune conform legii

Întotdeauna obține permisiune scrisă înainte de a scana sisteme care nu îți aparțin.

### De ce DVWA este "Damn Vulnerable"?

DVWA (Damn Vulnerable Web Application) conține vulnerabilități **INTENȚIONATE**:
- SQL Injection
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- File Inclusion
- Command Injection

Scopul este să înveți tehnici de atac ȘI apărare într-un mediu sigur. **NU expuneți NICIODATĂ DVWA pe internet!**

### Ce protejează TLS și ce nu?

**Protejează:**
- Conținutul mesajelor (criptare)
- Integritatea datelor (nu pot fi modificate în tranzit)
- Identitatea serverului (certificate)

**NU protejează:**
- Metadate (dimensiuni pachete, timing)
- Faptul că are loc o comunicație
- Adresele IP sursă/destinație
- Încrederea în server (certificatul valid ≠ server de încredere)

---

## Probleme Tehnice

### Docker nu pornește în WSL

```bash
# Pornește serviciul Docker
sudo service docker start
# Parolă: stud

# Verifică starea
sudo service docker status

# Dacă tot nu merge, verifică WSL2
wsl --status  # în PowerShell
```

### Portainer nu răspunde la http://localhost:9000

1. Verifică dacă containerul există:
   ```bash
   docker ps -a | grep portainer
   ```

2. Dacă e oprit, pornește-l:
   ```bash
   docker start portainer
   ```

3. Dacă nu există, creează-l:
   ```bash
   docker run -d -p 9000:9000 --name portainer --restart=always \
     -v /var/run/docker.sock:/var/run/docker.sock \
     -v portainer_data:/data portainer/portainer-ce:latest
   ```

### Am uitat parola Portainer

Resetează Portainer (nu afectează alte containere):
```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data
# Recreează cu comanda de mai sus
# La prima accesare, setează parola: studstudstud
```

### Wireshark nu vede traficul Docker

Selectează interfața corectă:
- ✅ `vEthernet (WSL)` — pentru trafic Docker în WSL
- ❌ `Ethernet` sau `Wi-Fi` — acestea sunt pentru trafic fizic extern

Dacă tot nu vezi pachete:
1. Verifică că capturezi în timpul generării traficului
2. Șterge filtrul de afișare pentru a vedea toate pachetele
3. Încearcă "Capture → Options → Promiscuous mode"

### Eroare: "ModuleNotFoundError: No module named 'paho'"

Instalează pachetul lipsă:
```bash
pip install paho-mqtt

# Sau toate dependențele:
pip install -r requirements.txt
```

### Eroare: "Permission denied" la Scapy

Scapy necesită privilegii root pentru captură raw:
```bash
sudo python3 src/exercises/ex_13_03_sniffer_pachete.py --numar 10
# Parolă: stud
```

### Containerele pornesc dar serviciile nu răspund

1. Așteaptă inițializarea (10-30 secunde după `docker compose up`)
2. Verifică health check:
   ```bash
   docker ps  # Coloana STATUS arată "healthy" sau "unhealthy"
   ```
3. Verifică logurile:
   ```bash
   docker logs week13_mosquitto
   docker logs week13_dvwa
   ```

### Portul este deja utilizat

```bash
# Găsește ce folosește portul
sudo ss -tlnp | grep 1883

# Sau modifică porturile în .env:
MQTT_PLAIN_PORT=11883
MQTT_TLS_PORT=18883
```

---

## Întrebări Conceptuale

### Care este diferența între TCP Connect scan și SYN scan?

| Aspect | Connect Scan | SYN Scan |
|--------|--------------|----------|
| Completează handshake | DA (SYN→SYN/ACK→ACK) | NU (SYN→SYN/ACK→RST) |
| Apare în loguri | DA | De obicei NU |
| Necesită root | NU | DA |
| Viteză | Mai lent | Mai rapid |

### De ce MQTT folosește portul 1883?

IANA (Internet Assigned Numbers Authority) a alocat:
- **1883** pentru MQTT text clar
- **8883** pentru MQTT over TLS

Acestea sunt porturi "well-known" standardizate, similar cu 80 pentru HTTP și 443 pentru HTTPS.

### Ce înseamnă "publish/subscribe" vs "client/server"?

| Aspect | Client/Server | Publish/Subscribe |
|--------|---------------|-------------------|
| Cunoaștere | Clientul cunoaște serverul | Publisherul NU cunoaște subscriberii |
| Cuplare | Strânsă | Slabă |
| Scalabilitate | Limitată | Ridicată |
| Exemplu | HTTP request/response | MQTT topic messaging |

---

## Resurse Adiționale

### Unde găsesc mai multe informații?

- **MQTT:** https://mqtt.org/mqtt-specification/
- **OWASP IoT:** https://owasp.org/www-project-internet-of-things/
- **Docker:** https://docs.docker.com/
- **Wireshark:** https://www.wireshark.org/docs/

### Cum pot exersa mai mult acasă?

1. Instalează Docker Desktop pe calculatorul personal
2. Clonează repository-ul laboratorului
3. Experimentează cu configurații diferite în `docker-compose.yml`
4. Încearcă să creezi propriile topicuri MQTT pentru un proiect IoT simplu

---

*Pentru probleme neacoperite aici, consultați `docs/depanare.md` sau contactați instructorul.*

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
