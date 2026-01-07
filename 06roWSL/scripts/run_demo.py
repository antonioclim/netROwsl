#!/usr/bin/env python3
"""
Executor demonstrații Săptămâna 6
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Rulează demonstrații automatizate pentru exercițiile NAT/PAT și SDN.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import setup_logger

logger = setup_logger("run_demo")

DEMONSTRATII = {
    "nat": {
        "description": "Topologie NAT/PAT cu traducere MASQUERADE",
        "topology": "topo_nat.py",
        "mode": "cli"
    },
    "nat-test": {
        "description": "Test automat rapid pentru topologia NAT",
        "topology": "topo_nat.py",
        "mode": "test"
    },
    "sdn": {
        "description": "Topologie SDN cu politici OpenFlow",
        "topology": "topo_sdn.py",
        "mode": "cli",
        "extra_args": ["--install-flows"]
    },
    "sdn-test": {
        "description": "Test automat rapid pentru topologia SDN",
        "topology": "topo_sdn.py",
        "mode": "test",
        "extra_args": ["--install-flows"]
    },
    "nat-visual": {
        "description": "Vizualizare traducere NAT (automatizat)",
        "script": "nat_visual_demo"
    },
    "sdn-flows": {
        "description": "Demonstrație instalare fluxuri SDN",
        "script": "sdn_flow_demo"
    },
}


def verifica_mininet() -> bool:
    """Verifică dacă Mininet este disponibil."""
    try:
        rezultat = subprocess.run(
            ["mn", "--version"],
            capture_output=True,
            timeout=5
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def ruleaza_demo_topologie(
    topologie: str,
    mod: str,
    argumente_extra: Optional[list[str]] = None
) -> int:
    """
    Rulează o demonstrație de topologie Mininet.
    
    Argumente:
        topologie: Numele fișierului de topologie
        mod: Fie 'cli' fie 'test'
        argumente_extra: Argumente suplimentare de transmis
        
    Returnează:
        Cod de ieșire
    """
    # Localizează fișierul de topologie
    cai_topologie = [
        RADACINA_PROIECT / "src" / "exercises" / topologie,
        RADACINA_PROIECT / "mininet" / "topologies" / topologie,
    ]
    
    fisier_topo = None
    for cale in cai_topologie:
        if cale.exists():
            fisier_topo = cale
            break
    
    if fisier_topo is None:
        logger.error(f"Fișierul de topologie nu a fost găsit: {topologie}")
        logger.info(f"Căutat în: {[str(p) for p in cai_topologie]}")
        return 1
    
    # Construiește comanda
    cmd = ["sudo", "python3", str(fisier_topo)]
    
    if mod == "cli":
        cmd.append("--cli")
    elif mod == "test":
        cmd.append("--test")
    
    if argumente_extra:
        cmd.extend(argumente_extra)
    
    logger.info(f"Execut: {' '.join(cmd)}")
    print()
    
    try:
        rezultat = subprocess.run(cmd)
        return rezultat.returncode
    except KeyboardInterrupt:
        print("\nDemonstrație întreruptă")
        return 130


def ruleaza_demo_nat_vizual() -> int:
    """
    Rulează demonstrația de vizualizare NAT arătând PAT în acțiune.
    """
    logger.info("Demonstrație Vizualizare Traducere NAT")
    logger.info("=" * 60)
    print()
    print("Această demonstrație va:")
    print("  1. Porni topologia NAT")
    print("  2. Lansa observatorul NAT pe h3")
    print("  3. Genera conexiuni de la h1 și h2")
    print("  4. Afișa observațiile despre traducere")
    print()
    
    # Aceasta ar rula normal o demonstrație automatizată în mai mulți pași
    # Deocamdată, ghidăm utilizatorul către versiunea interactivă
    logger.info("Pornirea demonstrației NAT interactive...")
    return ruleaza_demo_topologie("topo_nat.py", "cli")


def ruleaza_demo_fluxuri_sdn() -> int:
    """
    Rulează demonstrația de instalare fluxuri SDN.
    """
    logger.info("Demonstrație Instalare Fluxuri SDN")
    logger.info("=" * 60)
    print()
    print("Această demonstrație va:")
    print("  1. Porni topologia SDN cu fluxuri statice")
    print("  2. Arăta tabela de fluxuri inițială")
    print("  3. Demonstra traficul permis (h1 ↔ h2)")
    print("  4. Demonstra traficul blocat (h1 → h3)")
    print("  5. Arăta tabela de fluxuri actualizată cu statistici")
    print()
    
    logger.info("Pornirea demonstrației SDN interactive...")
    return ruleaza_demo_topologie("topo_sdn.py", "cli", ["--install-flows"])


def listeaza_demonstratii() -> None:
    """Afișează demonstrațiile disponibile."""
    print()
    print("Demonstrații disponibile:")
    print("=" * 60)
    
    for nume, info in DEMONSTRATII.items():
        descriere = info.get("description", "Fără descriere")
        print(f"  {nume:<15} - {descriere}")
    
    print()
    print("Utilizare: python scripts/run_demo.py --demo <nume>")
    print()


def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Rulează demonstrațiile de laborator Săptămâna 6"
    )
    parser.add_argument(
        "--demo", "-d",
        choices=list(DEMONSTRATII.keys()),
        help="Demonstrația de rulat"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Listează demonstrațiile disponibile"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișare detaliată"
    )
    args = parser.parse_args()
    
    if args.verbose:
        from scripts.utils.logger import set_verbose
        set_verbose(logger, True)
    
    if args.list or not args.demo:
        listeaza_demonstratii()
        return 0
    
    # Verifică cerințele preliminare
    if not verifica_mininet():
        logger.error("Mininet nu este disponibil")
        logger.info("Te rugăm să rulezi demonstrațiile în interiorul containerului Docker:")
        logger.info("  docker exec -it week6_lab bash")
        logger.info("  make <nume-demo>")
        return 1
    
    info_demo = DEMONSTRATII.get(args.demo)
    if not info_demo:
        logger.error(f"Demonstrație necunoscută: {args.demo}")
        listeaza_demonstratii()
        return 1
    
    print()
    logger.info("=" * 60)
    logger.info(f"Demonstrație: {info_demo.get('description', args.demo)}")
    logger.info("=" * 60)
    print()
    
    # Rulează demonstrația
    if "script" in info_demo:
        # Demonstrație cu script personalizat
        script = info_demo["script"]
        if script == "nat_visual_demo":
            return ruleaza_demo_nat_vizual()
        elif script == "sdn_flow_demo":
            return ruleaza_demo_fluxuri_sdn()
        else:
            logger.error(f"Script necunoscut: {script}")
            return 1
    else:
        # Demonstrație bazată pe topologie
        return ruleaza_demo_topologie(
            info_demo["topology"],
            info_demo.get("mode", "cli"),
            info_demo.get("extra_args")
        )


if __name__ == "__main__":
    sys.exit(main())
