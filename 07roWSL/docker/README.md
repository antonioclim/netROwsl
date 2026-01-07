# Configurare Docker pentru Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Prezentare Generală

Acest director conține configurația Docker pentru laboratorul de interceptare și filtrare a pachetelor.

## Servicii Definite

| Serviciu | Container | IP | Port | Descriere |
|----------|-----------|-----|------|-----------|
| server_tcp | week7_server_tcp | 10.0.7.100 | 9090 | Server TCP echo |
| receptor_udp | week7_receptor_udp | 10.0.7.200 | 9091/udp | Receptor datagrame UDP |
| filtru_pachete | week7_filtru_pachete | 10.0.7.50 | 8888 | Proxy cu filtrare conținut |
| demo | week7_demo | 10.0.7.10 | - | Container pentru demonstrații |

## Utilizare

### Pornire Servicii de Bază

```bash
# Pornește server_tcp și receptor_udp
docker compose up -d

# Verifică statusul
docker compose ps
```

### Pornire cu Profil Demo

```bash
# Include filtru_pachete și containerul demo
docker compose --profile demo up -d
```

### Pornire cu Profil Proxy

```bash
# Include doar filtru_pachete
docker compose --profile proxy up -d
```

### Oprire Servicii

```bash
# Oprește și elimină containerele
docker compose down

# Oprește și elimină inclusiv volumele
docker compose down -v
```

## Rețea

Toate containerele sunt conectate la rețeaua `week7net`:
- Subnet: `10.0.7.0/24`
- Gateway: `10.0.7.1`

## Profile de Firewall

Fișierul `configs/firewall_profiles.json` conține profile predefinite:

1. **referinta** - Nicio filtrare, trafic normal
2. **blocare_tcp_9090** - REJECT pe TCP 9090
3. **blocare_udp_9091** - DROP pe UDP 9091
4. **filtrare_mixta** - Combinație REJECT + DROP
5. **blocare_tcp_drop** - DROP pe TCP pentru comparație cu REJECT

## Depanare

### Container nu pornește

```bash
# Verificați logurile
docker compose logs server_tcp

# Verificați rețeaua
docker network inspect week7net
```

### Port ocupat

```bash
# Verificați ce folosește portul
netstat -ano | findstr :9090
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
