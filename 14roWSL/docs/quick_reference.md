# Quick Reference Card - Săptămâna 14

> Printează această pagină pentru referință rapidă în timpul laboratorului.

---

## 🐳 Docker Commands

```bash
# Status
docker ps                    # Containere active
docker ps -a                 # Toate containerele
docker images                # Imagini disponibile

# Pornire/Oprire
docker start <container>     # Pornește container
docker stop <container>      # Oprește grațios
docker restart <container>   # Repornește

# Logs & Debug
docker logs <container>              # Vezi loguri
docker logs -f <container>           # Urmărește în timp real
docker exec -it <container> bash     # Shell în container

# Docker Compose
docker compose up -d         # Pornește stack
docker compose down          # Oprește și elimină
docker compose logs -f       # Loguri pentru tot stack-ul
```

---

## 🔧 Scripturi Laborator

```bash
# Din /mnt/d/RETELE/SAPT14/14roWSL

python3 scripts/porneste_lab.py      # Pornește tot
python3 scripts/porneste_lab.py -s   # Doar status
python3 scripts/opreste_lab.py       # Oprește containere
python3 scripts/curata.py -c         # Curățare completă
```

---

## 🌐 Adrese Servicii

| Serviciu | URL/Adresă |
|----------|------------|
| **Portainer** | http://localhost:9000 |
| **Load Balancer** | http://localhost:8080 |
| **Backend 1** | http://localhost:8001 |
| **Backend 2** | http://localhost:8002 |
| **Echo Server** | tcp://localhost:9090 |

**Credențiale Portainer:** `stud` / `studstudstud`

---

## 🦈 Filtre Wireshark

```
# HTTP
http                         # Tot traficul HTTP
tcp.port == 8080            # Load Balancer
http.request.method == GET  # Cereri GET

# TCP Analysis
tcp.flags.syn == 1          # Conexiuni noi
tcp.flags.rst == 1          # Reset-uri
tcp.analysis.retransmission # Retransmisii

# Per Backend
ip.addr == 172.20.0.2       # App1
ip.addr == 172.20.0.3       # App2
```

---

## 🔍 Testare Rapidă

```bash
# Test Load Balancer (vezi distribuția)
for i in {1..10}; do curl -s http://localhost:8080/; done

# Test Echo Server
echo "Test" | nc localhost 9090

# Test Health Checks
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8080/lb-status

# Verifică porturi
ss -tlnp | grep -E "8080|8001|8002|9090|9000"
```

---

## 🚨 Depanare Rapidă

| Problemă | Soluție |
|----------|---------|
| "Cannot connect to Docker" | `sudo service docker start` |
| "Port already in use" | `docker compose down` sau `docker stop $(docker ps -q)` |
| "Connection refused" | Verifică `docker ps` - containerul rulează? |
| Portainer nu răspunde | `docker start portainer` |
| Wireshark nu capturează | Selectează interfața "vEthernet (WSL)" |

---

## 📊 Arhitectura Rețelei

```
┌──────────────────────────────────────────────────────┐
│  FRONTEND (172.21.0.0/24)                            │
│    Client(172.21.0.2) ←→ LB(172.21.0.10:8080)       │
└───────────────────────────┬──────────────────────────┘
                            │
┌───────────────────────────┴──────────────────────────┐
│  BACKEND (172.20.0.0/24)                             │
│    LB(172.20.0.10) ←→ App1(172.20.0.2:8001)         │
│                    ←→ App2(172.20.0.3:8001)         │
│                    ←→ Echo(172.20.0.20:9090)        │
└──────────────────────────────────────────────────────┘

Portainer: http://localhost:9000 (management)
```

---

*Laborator Rețele de Calculatoare - ASE | by Revolvix*
