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
