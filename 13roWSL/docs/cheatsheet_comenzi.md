# Cheatsheet Comenzi

> Laborator Săptămâna 13 - IoT și Securitate
>
> Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

---

## Comenzi Rapide Laborator

### Pornire și Oprire

```powershell
# Pornire laborator
python scripts/porneste_lab.py

# Verificare stare
python scripts/porneste_lab.py --status

# Oprire laborator (păstrează date)
python scripts/opreste_lab.py

# Curățare completă
python scripts/curata.py --complet
```

### Exerciții

```powershell
# Exercițiul 1: Scanner Porturi
python src/exercises/ex_13_01_scanner_porturi.py --tinta localhost --porturi 1883,8883,8080,2121,6200

# Exercițiul 2: Client MQTT
python src/exercises/ex_13_02_client_mqtt.py --mod subscribe --topic "senzori/#"
python src/exercises/ex_13_02_client_mqtt.py --mod publish --topic "test" --mesaj "salut"

# Exercițiul 3: Sniffer
python src/exercises/ex_13_03_sniffer_pachete.py --numar 20

# Exercițiul 4: Verificator Vulnerabilități
python src/exercises/ex_13_04_verificator_vulnerabilitati.py --tinta localhost --toate
```

### Demonstrații

```powershell
python scripts/ruleaza_demo.py --demo 1  # Recunoaștere
python scripts/ruleaza_demo.py --demo 2  # TLS vs text clar
python scripts/ruleaza_demo.py --demo 3  # Detecție backdoor
```

---

## Comenzi Docker

```powershell
# Stare containere
docker ps

# Loguri serviciu specific
docker logs week13_mosquitto
docker logs week13_dvwa
docker logs week13_vsftpd

# Urmărire loguri în timp real
docker logs -f week13_mosquitto

# Execuție comandă în container
docker exec -it week13_mosquitto sh

# Curățare resurse Docker
docker system prune -f
```

---

## Comenzi MQTT (mosquitto_pub/sub)

```bash
# Abonare la topic
mosquitto_sub -h localhost -p 1883 -t "senzori/#"

# Publicare mesaj
mosquitto_pub -h localhost -p 1883 -t "test/mesaj" -m "Hello"

# Conexiune TLS
mosquitto_sub -h localhost -p 8883 -t "#" --cafile docker/configs/certs/ca.crt
```

---

## Filtre Wireshark

```
# Trafic MQTT text clar
tcp.port == 1883

# Trafic MQTT TLS
tcp.port == 8883

# Trafic HTTP (DVWA)
tcp.port == 8080 and http

# Trafic FTP
tcp.port == 2121

# Toate serviciile laboratorului
tcp.port in {1883, 8883, 8080, 2121, 6200}

# Conexiuni noi (SYN)
tcp.flags.syn == 1 and tcp.flags.ack == 0

# Mesaje MQTT PUBLISH
mqtt.msgtype == 3
```

---

## Comenzi Rețea

```powershell
# Testare conectivitate port (PowerShell)
Test-NetConnection -ComputerName localhost -Port 1883

# Scanare porturi (nmap)
nmap -sV localhost -p 1883,8883,8080,2121,6200

# Verificare procese pe port
netstat -ano | findstr :1883

# WSL: Testare port
nc -zv localhost 1883
```

---

## Comenzi Git (Opțional)

```bash
# Inițializare repo
git init

# Adăugare fișiere
git add .

# Commit
git commit -m "Laboratorul 13 finalizat"

# Stare
git status
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*

---

## Verificare Rapidă Stare

```bash
# One-liner: verifică toate serviciile laboratorului
for p in 1883 8883 8080 2121 6200; do 
  nc -zv localhost $p 2>&1 | grep -q succeeded && echo "Port $p: OK" || echo "Port $p: FAIL"
done

# Sau cu Python
python3 -c "
import socket
ports = [1883, 8883, 8080, 2121, 6200]
for p in ports:
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect(('localhost', p))
        print(f'Port {p}: OK')
        s.close()
    except:
        print(f'Port {p}: FAIL')
"
```

---

## Comenzi de Urgență

```bash
# Totul s-a blocat? Reset complet (păstrează Portainer):
docker compose -f docker/docker-compose.yml down -v
docker compose -f docker/docker-compose.yml up -d

# Doar un container problematic:
docker restart week13_mosquitto

# Forțează rebuild imaginilor:
docker compose -f docker/docker-compose.yml build --no-cache
docker compose -f docker/docker-compose.yml up -d

# Verifică ce ocupă un port:
sudo ss -tlnp | grep :1883
# sau în Windows PowerShell:
netstat -ano | findstr :1883
```

---

## Alias-uri Recomandate (opțional)

Adaugă în `~/.bashrc` pentru acces rapid:

```bash
# Navigare rapidă
alias lab13='cd /mnt/d/RETELE/SAPT13/13roWSL'

# Comenzi laborator
alias lab13-start='python3 scripts/porneste_lab.py'
alias lab13-stop='python3 scripts/opreste_lab.py'
alias lab13-status='docker ps --filter "name=week13" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias lab13-logs='docker compose -f docker/docker-compose.yml logs -f'

# Exerciții
alias lab13-scan='python3 src/exercises/ex_13_01_scanner_porturi.py'
alias lab13-mqtt='python3 src/exercises/ex_13_02_client_mqtt.py'
alias lab13-sniff='sudo python3 src/exercises/ex_13_03_sniffer_pachete.py'
alias lab13-vuln='python3 src/exercises/ex_13_04_verificator_vulnerabilitati.py'

# Aplicare: source ~/.bashrc
```

---

## Combinații Utile

```bash
# Scanează și salvează rezultatul cu timestamp
python3 src/exercises/ex_13_01_scanner_porturi.py \
  --tinta localhost \
  --porturi 1-10000 \
  --output "scan_$(date +%Y%m%d_%H%M%S).json"

# Subscribe MQTT cu logging în fișier
python3 src/exercises/ex_13_02_client_mqtt.py \
  --mod subscribe \
  --topic "#" \
  2>&1 | tee mqtt_log_$(date +%Y%m%d).txt

# Captură pachete și deschide automat în Wireshark
sudo python3 src/exercises/ex_13_03_sniffer_pachete.py \
  --numar 100 \
  --output captura.pcap && \
  wireshark captura.pcap &
```

---

## Troubleshooting Rapid

| Simptom | Comandă de diagnostic | Soluție probabilă |
|---------|----------------------|-------------------|
| Docker nu răspunde | `sudo service docker status` | `sudo service docker start` |
| Port ocupat | `sudo ss -tlnp \| grep :PORT` | Oprește procesul sau schimbă portul |
| Container crash loop | `docker logs week13_X` | Verifică configurația/dependențele |
| Wireshark gol | Verifică interfața selectată | Selectează `vEthernet (WSL)` |
| TLS error | `openssl s_client -connect localhost:8883` | Regenerează certificatele |

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
