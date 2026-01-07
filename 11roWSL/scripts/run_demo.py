#!/usr/bin/env python3
"""
Demonstrații Laborator Săptămâna 11
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest script rulează demonstrații automate pentru prezentare.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.network_utils import (
    http_get, 
    testeaza_echilibror_sarcina, 
    benchmark_endpoint
)

logger = configureaza_logger("run_demo")


def demo_echilibrare_sarcina():
    """Demonstrează distribuția cererilor pe backend-uri."""
    logger.info("\n" + "=" * 60)
    logger.info("DEMO 1: Echilibrare de Sarcină Round-Robin")
    logger.info("=" * 60)
    
    logger.info("\nTrimitem 12 cereri către echilibror...")
    logger.info("URL: http://localhost:8080/")
    print()
    
    distributie = {}
    
    for i in range(12):
        try:
            raspuns = http_get("http://localhost:8080/")
            
            if raspuns.status == 200:
                # Detectează backend-ul din conținut
                continut = raspuns.body.lower()
                backend = "necunoscut"
                for j in range(1, 4):
                    if f"web{j}" in continut or f"backend {j}" in continut:
                        backend = f"Backend {j}"
                        break
                
                distributie[backend] = distributie.get(backend, 0) + 1
                logger.info(f"  Cerere {i+1:2d}: {backend} (latență: {raspuns.latenta_ms:.1f}ms)")
            else:
                logger.warning(f"  Cerere {i+1:2d}: Eroare HTTP {raspuns.status}")
                
        except Exception as e:
            logger.error(f"  Cerere {i+1:2d}: Eșuată - {e}")
        
        time.sleep(0.2)
    
    logger.info("\nDistribuție finală:")
    for backend, count in sorted(distributie.items()):
        procent = count / 12 * 100
        bara = "█" * int(procent / 5)
        logger.info(f"  {backend}: {count:2d} cereri ({procent:.1f}%) {bara}")


def demo_inspectie_headere():
    """Demonstrează headerele adăugate de echilibror."""
    logger.info("\n" + "=" * 60)
    logger.info("DEMO 2: Inspecție Headere HTTP")
    logger.info("=" * 60)
    
    logger.info("\nExaminăm headerele răspunsului de la echilibror...")
    
    try:
        raspuns = http_get("http://localhost:8080/")
        
        logger.info(f"\nStatus: {raspuns.status}")
        logger.info("\nHeadere relevante:")
        
        headere_relevante = [
            "server", "x-backend-id", "x-served-by", 
            "x-load-balancer", "content-type"
        ]
        
        for cheie, valoare in raspuns.headers.items():
            if cheie.lower() in headere_relevante:
                logger.info(f"  {cheie}: {valoare}")
        
        logger.info(f"\nConținut răspuns (primele 200 caractere):")
        logger.info(f"  {raspuns.body[:200]}")
        
    except Exception as e:
        logger.error(f"Eroare la obținerea răspunsului: {e}")


def demo_failover():
    """Demonstrează comportamentul la căderea unui backend."""
    logger.info("\n" + "=" * 60)
    logger.info("DEMO 3: Failover și Recuperare")
    logger.info("=" * 60)
    
    logger.info("\nPas 1: Testăm distribuția inițială...")
    distributie_initiala = testeaza_echilibror_sarcina("http://localhost:8080/", 6)
    logger.info(f"  Distribuție: {distributie_initiala}")
    
    logger.info("\nPas 2: Oprim Backend 2...")
    try:
        subprocess.run(
            ["docker", "stop", "s11_backend_2"],
            capture_output=True,
            timeout=10
        )
        logger.info("  ✓ Backend 2 oprit")
    except Exception as e:
        logger.error(f"  ✗ Nu s-a putut opri: {e}")
        return
    
    logger.info("\nPas 3: Așteptăm detectarea căderilor (5 secunde)...")
    time.sleep(5)
    
    logger.info("\nPas 4: Testăm redistribuția...")
    distributie_failover = testeaza_echilibror_sarcina("http://localhost:8080/", 6)
    logger.info(f"  Distribuție: {distributie_failover}")
    logger.info("  → Traficul ar trebui să meargă doar la Backend 1 și 3")
    
    logger.info("\nPas 5: Repornim Backend 2...")
    try:
        subprocess.run(
            ["docker", "start", "s11_backend_2"],
            capture_output=True,
            timeout=10
        )
        logger.info("  ✓ Backend 2 repornit")
    except Exception as e:
        logger.error(f"  ✗ Nu s-a putut reporni: {e}")
        return
    
    logger.info("\nPas 6: Așteptăm reintegrarea (5 secunde)...")
    time.sleep(5)
    
    logger.info("\nPas 7: Testăm recuperarea...")
    distributie_recuperare = testeaza_echilibror_sarcina("http://localhost:8080/", 6)
    logger.info(f"  Distribuție: {distributie_recuperare}")
    logger.info("  → Traficul ar trebui să meargă din nou la toate cele 3 backend-uri")


def demo_benchmark():
    """Demonstrează benchmarking-ul echilibrului de sarcină."""
    logger.info("\n" + "=" * 60)
    logger.info("DEMO 4: Benchmark Performanță")
    logger.info("=" * 60)
    
    logger.info("\nRulăm benchmark cu 200 cereri, 10 workers concurenți...")
    
    rezultat = benchmark_endpoint("http://localhost:8080/", numar_cereri=200, concurenta=10)
    
    logger.info(f"\nRezultate benchmark:")
    logger.info(f"  Cereri totale:    {rezultat['total_cereri']}")
    logger.info(f"  Cereri reușite:   {rezultat['cereri_reusite']}")
    logger.info(f"  Durată totală:    {rezultat['durata_secunde']:.2f}s")
    logger.info(f"  Cereri/secundă:   {rezultat['cereri_pe_secunda']:.2f}")
    logger.info(f"\nLatențe:")
    logger.info(f"  p50 (mediană):    {rezultat['latenta_p50_ms']:.2f}ms")
    logger.info(f"  p90:              {rezultat['latenta_p90_ms']:.2f}ms")
    logger.info(f"  p95:              {rezultat['latenta_p95_ms']:.2f}ms")
    logger.info(f"  p99:              {rezultat['latenta_p99_ms']:.2f}ms")


def demo_verificare_stare():
    """Demonstrează endpoint-ul de verificare a stării."""
    logger.info("\n" + "=" * 60)
    logger.info("DEMO 5: Verificare Stare Servicii")
    logger.info("=" * 60)
    
    endpoints = [
        ("Echilibror sarcină", "http://localhost:8080/"),
        ("Health check", "http://localhost:8080/health"),
        ("Status Nginx", "http://localhost:8080/nginx_status"),
    ]
    
    for nume, url in endpoints:
        logger.info(f"\n{nume}: {url}")
        try:
            raspuns = http_get(url)
            logger.info(f"  Status: {raspuns.status}")
            logger.info(f"  Latență: {raspuns.latenta_ms:.2f}ms")
            if len(raspuns.body) < 500:
                logger.info(f"  Răspuns:\n{raspuns.body}")
        except Exception as e:
            logger.error(f"  Eroare: {e}")


def ruleaza_demo_complet():
    """Rulează toate demonstrațiile în ordine."""
    logger.info("\n" + "=" * 60)
    logger.info("DEMONSTRAȚIE COMPLETĂ - Săptămâna 11")
    logger.info("Echilibrare de Sarcină și Protocoale de Aplicație")
    logger.info("=" * 60)
    
    timp_start = datetime.now()
    
    # Rulează toate demonstrațiile
    demo_echilibrare_sarcina()
    time.sleep(1)
    
    demo_inspectie_headere()
    time.sleep(1)
    
    demo_failover()
    time.sleep(1)
    
    demo_benchmark()
    time.sleep(1)
    
    demo_verificare_stare()
    
    # Sumar
    durata = (datetime.now() - timp_start).total_seconds()
    
    logger.info("\n" + "=" * 60)
    logger.info("DEMONSTRAȚIE FINALIZATĂ")
    logger.info(f"Durată totală: {durata:.1f} secunde")
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Rulează demonstrații pentru Săptămâna 11"
    )
    parser.add_argument(
        "--demo",
        choices=["echilibrare", "headere", "failover", "benchmark", "stare"],
        help="Rulează o demonstrație specifică"
    )
    parser.add_argument(
        "--all", "--toate",
        action="store_true",
        help="Rulează toate demonstrațiile"
    )
    parser.add_argument(
        "--save", "--salveaza",
        action="store_true",
        help="Salvează output-ul într-un fișier jurnal"
    )
    args = parser.parse_args()

    # Configurează salvarea jurnalului
    if args.save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fisier_jurnal = RADACINA_PROIECT / "artifacts" / f"demo_{timestamp}.log"
        fisier_jurnal.parent.mkdir(exist_ok=True)
        logger.info(f"Jurnalul va fi salvat în: {fisier_jurnal}")

    try:
        if args.all:
            ruleaza_demo_complet()
        elif args.demo == "echilibrare":
            demo_echilibrare_sarcina()
        elif args.demo == "headere":
            demo_inspectie_headere()
        elif args.demo == "failover":
            demo_failover()
        elif args.demo == "benchmark":
            demo_benchmark()
        elif args.demo == "stare":
            demo_verificare_stare()
        else:
            # Implicit: rulează demonstrația de echilibrare
            demo_echilibrare_sarcina()
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\nDemonstrație întreruptă de utilizator.")
        return 0
    except Exception as e:
        logger.error(f"Eroare la rularea demonstrației: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
