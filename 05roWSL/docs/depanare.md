# Ghid de Depanare – Săptămâna 5

> Soluții pentru problemele frecvente în laborator
> ASE, Informatică Economică | realizat de Revolvix

---

## Probleme Docker

### Docker nu pornește

**Simptome:**
- Comanda `docker ps` returnează eroare
- Mesaj: "Cannot connect to the Docker daemon"

**Soluție:**
```bash
# Pornește serviciul Docker
sudo service docker start

# Verifică status
sudo service docker status

# Dacă nu merge, repornește
sudo service docker restart
```

**Dacă tot nu funcționează:**
```bash
# Verifică dacă Docker e instalat
which docker
docker --version

# Verifică log-urile
sudo journalctl -u docker
```

---

### Containerele nu pornesc

**Simptome:**
- `docker compose up` eșuează
- Containerele intră în starea "Exited"

**Soluție:**
```bash
# Verifică log-urile containerului
docker logs week5_python

# Reconstruiește imaginea
docker compose build --no-cache

# Pornește cu output vizibil
docker compose up  # fără -d pentru a vedea erorile
```

**Cauze comune:**
- Port deja ocupat → Schimbă portul în docker-compose.yml
- Eroare în Dockerfile → Verifică sintaxa
- Lipsă dependențe → Verifică requirements.txt

---

### Portainer nu răspunde

**Simptome:**
- http://localhost:9000 nu se încarcă
- Timeout la accesare

**Soluție:**
```bash
# Verifică dacă Portainer e pornit
docker ps | grep portainer

# Dacă nu e pornit, pornește-l
docker start portainer

# Dacă nu există, creează-l
docker run -d \
  --name portainer \
  -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  --restart always \
  portainer/portainer-ce:latest
```

---

### Containerele nu comunică între ele

**Simptome:**
- Ping între containere eșuează
- Conexiune refuzată pe porturi

**Soluție:**
```bash
# Verifică că sunt pe aceeași rețea
docker network inspect week5_labnet

# Verifică IP-urile
docker exec week5_python ip addr
docker exec week5_udp-server ip addr

# Verifică conectivitatea
docker exec week5_python ping -c 3 10.5.0.20

# Dacă rețeaua nu există, creează-o
docker network create \
  --driver bridge \
  --subnet 10.5.0.0/24 \
  --gateway 10.5.0.1 \
  week5_labnet
```

---

## Probleme Python

### ModuleNotFoundError

**Simptome:**
```
ModuleNotFoundError: No module named 'src'
ModuleNotFoundError: No module named 'src.utils'
```

**Soluție:**
```bash
# Navighează în directorul corect
cd /mnt/d/RETELE/SAPT5/05roWSL

# Setează PYTHONPATH
export PYTHONPATH=.

# Sau rulează cu -m
python3 -m src.exercises.ex_5_01_cidr_flsm analizeaza 192.168.1.0/24
```

**Alternativ, adaugă în ~/.bashrc:**
```bash
echo 'export PYTHONPATH="/mnt/d/RETELE/SAPT5/05roWSL:$PYTHONPATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### Eroare la import ipaddress

**Simptome:**
```
AttributeError: 'str' object has no attribute 'network_address'
```

**Cauză:** Ai pasat un string în loc de obiect IPv4Network.

**Soluție:**
```python
import ipaddress

# Greșit
retea = "192.168.1.0/24"
print(retea.network_address)  # Eroare!

# Corect
retea = ipaddress.ip_network("192.168.1.0/24")
print(retea.network_address)  # 192.168.1.0
```

---

### ValueError la CIDR

**Simptome:**
```
ValueError: '192.168.1.100/24' has host bits set
```

**Cauză:** Adresa IP nu e adresa de rețea pentru prefixul dat.

**Soluție:**
```python
import ipaddress

# Opțiunea 1: Folosește strict=False
retea = ipaddress.ip_network("192.168.1.100/24", strict=False)

# Opțiunea 2: Folosește ip_interface pentru a păstra adresa originală
interfata = ipaddress.ip_interface("192.168.1.100/24")
print(interfata.ip)      # 192.168.1.100
print(interfata.network) # 192.168.1.0/24
```

---

## Probleme WSL

### WSL nu găsește unitatea D:

**Simptome:**
```
-bash: cd: /mnt/d: No such file or directory
```

**Soluție:**
```bash
# Verifică unitățile montate
ls /mnt/

# Montează manual
sudo mkdir -p /mnt/d
sudo mount -t drvfs D: /mnt/d

# Pentru montare permanentă, editează /etc/fstab
echo "D: /mnt/d drvfs defaults 0 0" | sudo tee -a /etc/fstab
```

---

### Permisiuni fișiere Windows

**Simptome:**
- Nu poți executa scripturi
- Erori de permisiune la salvare

**Soluție:**
```bash
# Dă permisiuni de execuție
chmod +x scripts/*.py

# Pentru toate fișierele Python
find . -name "*.py" -exec chmod +x {} \;
```

---

### WSL foarte lent

**Cauze posibile:**
- Antivirus scanează fișierele
- Operații pe /mnt/ sunt lente

**Soluție:**
```bash
# Lucrează în sistemul de fișiere Linux (mai rapid)
cp -r /mnt/d/RETELE/SAPT5/05roWSL ~/laborator
cd ~/laborator

# Excludă folderul WSL din antivirus (în Windows):
# Windows Security → Virus & threat protection → Manage settings
# → Add an exclusion → Folder → \\wsl$
```

---

## Probleme Wireshark

### Nu văd interfața vEthernet (WSL)

**Soluție:**
1. Rulează Wireshark ca Administrator
2. Instalează Npcap cu opțiunea "Support raw 802.11 traffic"
3. Repornește Wireshark

---

### Nu capturez trafic Docker

**Cauze:**
- Interfața greșită selectată
- Traficul e doar local în WSL

**Soluție:**
- Selectează **vEthernet (WSL)** pentru trafic între containere
- Pentru trafic localhost, selectează **Loopback**

---

### Filtru nu funcționează

**Simptome:**
- Filtrul apare cu fundal roșu
- Nu afișează nimic

**Soluții:**
```
# Filtre corecte
ip.addr == 10.5.0.10       # Corect
ip.addr = 10.5.0.10        # GREȘIT (un singur =)
ip.address == 10.5.0.10    # GREȘIT (numele câmpului)

# Verifică sintaxa pe wiki.wireshark.org/DisplayFilters
```

---

## Probleme Generale

### Scriptul nu găsește fișierele

**Simptome:**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Soluție:**
```bash
# Verifică directorul curent
pwd

# Navighează în directorul corect
cd /mnt/d/RETELE/SAPT5/05roWSL

# Verifică structura
ls -la
```

---

### Erori de codificare (UTF-8)

**Simptome:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Soluție:**
```bash
# Setează locale-ul corect
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Sau adaugă în script
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

---

### Git clone eșuează

**Simptome:**
- Timeout la clone
- Eroare de autentificare

**Soluție:**
```bash
# Verifică conexiunea la GitHub
ping github.com

# Folosește HTTPS în loc de SSH
git clone https://github.com/antonioclim/netROwsl.git

# Dacă e problema de proxy
git config --global http.proxy http://proxy:port
```

---

## Verificare Rapidă a Mediului

Rulează acest script pentru a verifica toate componentele:

```bash
cd /mnt/d/RETELE/SAPT5/05roWSL
python3 setup/verifica_mediu.py
```

Sau manual:

```bash
echo "=== Verificare Docker ===" && docker --version && docker ps
echo "=== Verificare Python ===" && python3 --version
echo "=== Verificare Rețea ===" && docker network ls | grep week5
echo "=== Verificare Containere ===" && docker ps | grep week5
```

---

## Documente Înrudite

- [README Principal](../README.md) — Ghid de pornire
- [Fișa de Comenzi](fisa_comenzi.md) — Referință rapidă
- [Rezumat Teoretic](rezumat_teorie.md) — Concepte de bază
- [Arhitectura Cod](arhitectura.md) — Structura proiectului

---

## Încă ai probleme?

1. Verifică secțiunea de [Issues pe GitHub](https://github.com/antonioclim/netROwsl/issues)
2. Deschide un Issue nou cu:
   - Descrierea problemei
   - Comanda exactă executată
   - Mesajul de eroare complet
   - Output-ul comenzii `docker ps` și `python3 --version`

---

*Laborator Rețele de Calculatoare – ASE București*
