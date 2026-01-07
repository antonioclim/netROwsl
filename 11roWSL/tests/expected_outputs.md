# Rezultate Așteptate pentru Exerciții

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest document descrie rezultatele așteptate pentru fiecare exercițiu.

## Exercițiul 1: Servere Backend HTTP

### Comandă

```powershell
curl http://localhost:8081/
```

### Rezultat Așteptat

```
Backend 1 | Gazdă: NUMELE-PC | Timp: 2025-01-06T14:30:00 | Cerere #1
```

### Header-e Așteptate

```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
X-Backend-ID: 1
X-Served-By: backend-1
```

---

## Exercițiul 2: Distribuție Round Robin

### Comandă

```powershell
for /L %i in (1,1,6) do @curl -s http://localhost:8080/
```

### Rezultat Așteptat

Cererile ar trebui să fie distribuite ciclic:

```
Backend 1 | Gazdă: ... | Cerere #1
Backend 2 | Gazdă: ... | Cerere #1
Backend 3 | Gazdă: ... | Cerere #1
Backend 1 | Gazdă: ... | Cerere #2
Backend 2 | Gazdă: ... | Cerere #2
Backend 3 | Gazdă: ... | Cerere #2
```

### Ce Verificăm

- Fiecare cerere consecutivă merge la un backend diferit
- Ordinea se repetă: 1 → 2 → 3 → 1 → 2 → 3

---

## Exercițiul 3: Sesiuni Persistente IP Hash

### Comandă

```powershell
for /L %i in (1,1,5) do @curl -s http://localhost:8080/
```

### Rezultat Așteptat

Toate cererile ar trebui să meargă la același backend:

```
Backend 2 | Gazdă: ... | Cerere #1
Backend 2 | Gazdă: ... | Cerere #2
Backend 2 | Gazdă: ... | Cerere #3
Backend 2 | Gazdă: ... | Cerere #4
Backend 2 | Gazdă: ... | Cerere #5
```

### Ce Verificăm

- Același ID de backend pentru toate cererile
- Sesiunea este "lipită" de client pe baza IP-ului

---

## Exercițiul 4: Failover

### Scenariul

1. Backend 2 este oprit
2. Se trimit cereri

### Rezultat Așteptat în Timpul Căderilor

```
Backend 1 | Gazdă: ... | Cerere #N
Backend 3 | Gazdă: ... | Cerere #N
Backend 1 | Gazdă: ... | Cerere #N+1
Backend 3 | Gazdă: ... | Cerere #N+1
```

### Ce Verificăm

- Traficul se redistribuie automat
- Nu apar erori 502/503 (sau doar temporar)
- Backend 2 revine în rotație după repornire

---

## Exercițiul 5: Nginx Docker

### Comandă - Health Check

```powershell
curl http://localhost:8080/health
```

### Rezultat Așteptat

```
OK
```

### Comandă - Status Nginx

```powershell
curl http://localhost:8080/nginx_status
```

### Rezultat Așteptat

```
Active connections: 1 
server accepts handled requests
 123 123 456 
Reading: 0 Writing: 1 Waiting: 0 
```

---

## Exercițiul 6: Client DNS

### Comandă

```powershell
python src/exercises/ex_11_03_dns_client.py google.com A --verbose
```

### Rezultat Așteptat

```
[Interogare DNS] google.com A
[Trimitere către] 8.8.8.8:53
[Hexadecimal pachet]
  12 34 01 00 00 01 00 00 00 00 00 00 06 67 6f 6f
  67 6c 65 03 63 6f 6d 00 00 01 00 01

[Răspuns]
  Cod răspuns: 0
  Înregistrări: 1 răspunsuri, 0 autoritate, 0 adiționale

Rezultate pentru google.com (A):
--------------------------------------------------
  Nume: google.com
  Tip: A
  TTL: 299
  Date: 142.250.185.78
```

---

## Exercițiul 7: Benchmark

### Comandă

```powershell
python src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 200 --c 10
```

### Rezultat Așteptat - Echilibror Python

```
[generator] url=http://localhost:8080/
[generator] n=200 c=10
[generator] durata=0.456s rps=438.60
[generator] distribuție_statusuri={200: 200}
[generator] latențe_ms: p50=18.4532 p90=28.1234 p95=32.5678 p99=45.8901
```

### Rezultat Așteptat - Nginx

```
[generator] url=http://localhost:8080/
[generator] n=200 c=10
[generator] durata=0.021s rps=9523.81
[generator] distribuție_statusuri={200: 200}
[generator] latențe_ms: p50=0.8234 p90=1.2345 p95=1.5678 p99=2.3456
```

### Comparație Tipică

| Metric | Echilibror Python | Nginx |
|--------|-------------------|-------|
| RPS | 400 - 1.000 | 5.000 - 20.000 |
| Latență p50 | 15 - 50 ms | 0.5 - 5 ms |
| Latență p99 | 40 - 100 ms | 5 - 20 ms |

**Observație:** Nginx este semnificativ mai rapid datorită implementării în C și optimizărilor pentru I/O asincron.

---

## Note Generale

### Factori care Afectează Rezultatele

1. **Hardware-ul mașinii** - CPU, memorie, SSD/HDD
2. **Resurse Docker** - CPU și memorie alocate containerelor
3. **Încărcarea sistemului** - alte procese care rulează
4. **Rețeaua** - chiar și pentru localhost, există overhead

### Troubleshooting

Dacă rezultatele diferă semnificativ:

1. Verificați că Docker are suficiente resurse alocate
2. Închideți alte aplicații care consumă resurse
3. Reporniți containerele: `docker compose restart`
4. Verificați jurnalele: `docker compose logs`

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
