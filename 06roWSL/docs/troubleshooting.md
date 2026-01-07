# Săptămâna 6: Ghid de depanare

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:** Comenzile Docker se blochează sau eșuează cu erori de conexiune.

**Soluții:**
1. Asigură-te că Docker Desktop rulează (verifică în system tray)
2. Repornește Docker Desktop
3. Verifică dacă integrarea WSL2 este activată:
   - Docker Desktop → Settings → Resources → WSL Integration
   - Activează integrarea cu distribuția ta Ubuntu

### Erori la containerele privilegiate

**Simptome:** Containerul nu pornește cu erori de permisiuni.

**Soluții:**
1. Asigură-te că Docker Desktop este configurat pentru containere privilegiate
2. Pe Windows, repornește Docker Desktop cu privilegii de administrator
3. Verifică în docker-compose.yml că `privileged: true` este setat

### Modul de rețea host nu funcționează

**Simptome:** Containerele nu pot accesa rețeaua host sau Mininet eșuează.

**Soluții:**
1. Pe Docker Desktop pentru Windows/Mac, rețeaua host este limitată
2. Folosește containerul Docker furnizat care este configurat corect
3. Pentru funcționalitate completă, folosește Linux nativ sau o mașină virtuală Linux

## Probleme Mininet

### Eroare "File exists" la pornire

**Simptome:** Mininet nu pornește cu mesaje despre interfețe existente.

**Soluții:**
```bash
# Curăță starea Mininet
sudo mn -c

# Dacă eșuează, elimină manual interfețele
sudo ip link delete s1-eth1 2>/dev/null
sudo ip link delete s1-eth2 2>/dev/null

# Omoară procesele orfane
sudo pkill -9 ovs
sudo pkill -9 controller
```

### "OVS switch failed to connect"

**Simptome:** Topologia SDN arată switch-urile dar conexiunea la controller eșuează.

**Soluții:**
1. Verifică dacă controller-ul rulează:
   ```bash
   ss -ltn | grep 6633
   ```
2. Verifică configurația OVS:
   ```bash
   ovs-vsctl show
   ```
3. Verifică dacă IP-ul controller-ului în topologie corespunde cu controller-ul real
4. Verifică dacă regulile de firewall nu blochează portul 6633

### Ping foarte lent sau timeout

**Simptome:** Primele ping-uri durează mai multe secunde, ping-urile următoare eșuează.

**Soluții:**
1. Pentru topologia SDN, verifică dacă regulile de flux sunt instalate:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1
   ```
2. Asigură-te că ARP funcționează (ar trebui să existe fluxuri pentru ARP)
3. Verifică dacă controller-ul procesează evenimentele packet-in
4. Încearcă să folosești flag-ul `--install-flows` pentru fluxuri statice

### "mn: command not found"

**Simptome:** Mininet nu este instalat.

**Soluții:**
```bash
# Instalează Mininet
sudo apt-get update
sudo apt-get install -y mininet openvswitch-switch

# Verifică instalarea
mn --version
```

## Probleme NAT

### NAT nu traduce pachetele

**Simptome:** Hosturile private nu pot ajunge la hosturile publice.

**Soluții:**
1. Verifică dacă IP forwarding-ul este activat:
   ```bash
   sysctl net.ipv4.ip_forward
   # Dacă este 0, activează-l:
   sudo sysctl -w net.ipv4.ip_forward=1
   ```

2. Verifică dacă regula MASQUERADE există:
   ```bash
   iptables -t nat -L -n -v | grep MASQUERADE
   ```

3. Verifică rutarea pe hosturile private:
   ```bash
   ip route
   # Ar trebui să aibă default prin routerul NAT
   ```

4. Verifică dacă numele interfețelor corespund regulilor iptables

### Tabela conntrack plină

**Simptome:** Conexiunile noi eșuează, conexiunile existente funcționează.

**Soluții:**
```bash
# Verifică conexiunile curente
conntrack -C

# Crește limita conntrack
sudo sysctl -w net.netfilter.nf_conntrack_max=131072
```

## Probleme SDN

### Controller-ul nu primește evenimente packet-in

**Simptome:** Tabela de fluxuri arată doar regula table-miss, fără fluxuri specifice traficului.

**Soluții:**
1. Verifică dacă switch-ul este conectat la controller:
   ```bash
   ovs-vsctl show
   # Caută "is_connected: true"
   ```

2. Verifică dacă versiunea OpenFlow corespunde:
   ```bash
   ovs-vsctl get bridge s1 protocols
   # Ar trebui să arate OpenFlow13
   ```

3. Asigură-te că regula table-miss trimite la controller:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1
   # Ar trebui să aibă: actions=CONTROLLER
   ```

### os-ken / osken-manager nu este găsit

**Simptome:** `osken-manager: command not found`

**Soluții:**
1. os-ken 4.0.0+ a eliminat instrumentele CLI
2. Folosește instalarea statică de fluxuri în schimb:
   ```bash
   python3 topo_sdn.py --cli --install-flows
   ```
3. Sau instalează versiunea mai veche os-ken:
   ```bash
   pip install "os-ken<4.0.0"
   ```

### Fluxurile nu potrivesc traficul

**Simptome:** Fluxul există dar traficul nu se potrivește cu el.

**Soluții:**
1. Verifică dacă criteriile de potrivire corespund exact cu traficul:
   - Verifică adresele IP, porturile, protocoalele
   - Verifică prioritatea (prioritate mai mare se potrivește prima)

2. Folosește statisticile de flux pentru depanare:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets
   ```

3. Verifică dacă pachetul ajunge la switch:
   ```bash
   tcpdump -i s1-eth1 -n
   ```

## Probleme WSL2

### Probleme de performanță WSL2

**Simptome:** Comenzile sunt lente, latența rețelei este mare.

**Soluții:**
1. Asigură-te că folosești WSL2, nu WSL1:
   ```powershell
   wsl --list --verbose
   ```

2. Dacă folosești WSL1, convertește:
   ```powershell
   wsl --set-version Ubuntu 2
   ```

3. Alocă mai multe resurse în `.wslconfig`:
   ```ini
   [wsl2]
   memory=8GB
   processors=4
   ```

### Conectivitate de rețea din WSL2

**Simptome:** Nu poți ajunge la containerele Docker din WSL2.

**Soluții:**
1. Folosește localhost în loc de IP-ul containerului
2. Asigură-te că integrarea Docker Desktop WSL este activată
3. Verifică dacă Windows Firewall nu blochează

## Probleme Python

### Erori la importul modulelor

**Simptome:** `ModuleNotFoundError: No module named 'os_ken'`

**Soluții:**
```bash
pip install --break-system-packages os-ken scapy requests pyyaml docker
```

### API-ul Python Mininet nu este găsit

**Simptome:** `ModuleNotFoundError: No module named 'mininet'`

**Soluții:**
```bash
# API-ul Python Mininet vine cu instalarea Mininet
sudo apt-get install mininet

# Modulul Python este instalat global de apt, nu de pip
```

## Obținerea ajutorului

Dacă întâmpini probleme neacoperite aici:

1. Verifică mesajul de eroare cu atenție
2. Caută pe forumurile cursului
3. Verifică logurile:
   ```bash
   docker compose logs
   journalctl -u openvswitch-switch
   ```
4. Întreabă în timpul orelor de laborator

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
