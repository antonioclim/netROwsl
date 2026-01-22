#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 6
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

import argparse
import subprocess
import sys
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("cleanup")


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_GLOBALE
# ═══════════════════════════════════════════════════════════════════════════════

PREFIX_SAPTAMANA = "week6"


# ═══════════════════════════════════════════════════════════════════════════════
# CURATARE_MININET
# ═══════════════════════════════════════════════════════════════════════════════

def curata_mininet() -> bool:
    """
    Curăță starea reziduală Mininet.
    
    Returnează:
        True dacă operația a reușit
    """
    logger.info("Curățarea stării Mininet...")
    
    try:
        # Rulează mn -c pentru a curăța Mininet
        rezultat = subprocess.run(
            ["sudo", "mn", "-c"],
            capture_output=True,
            timeout=30
        )
        if rezultat.returncode == 0:
            logger.info("  ✓ Curățare Mininet reușită")
            return True
        else:
            logger.warning("  ! Curățarea Mininet a returnat non-zero (poate fi OK)")
            return True
    except subprocess.TimeoutExpired:
        logger.warning("  ! Timeout la curățarea Mininet")
        return False
    except FileNotFoundError:
        logger.debug("  Mininet nu este instalat (curățare omisă)")
        return True
    except Exception as e:
        logger.warning(f"  ! Eroare la curățarea Mininet: {e}")
        return True  # Nu este critică


# ═══════════════════════════════════════════════════════════════════════════════
# CURATARE_OVS
# ═══════════════════════════════════════════════════════════════════════════════

def curata_ovs() -> bool:
    """
    Curăță bridge-urile Open vSwitch.
    
    Returnează:
        True dacă operația a reușit
    """
    logger.info("Curățarea bridge-urilor OVS...")
    
    try:
        # Listează bridge-urile OVS
        rezultat = subprocess.run(
            ["sudo", "ovs-vsctl", "list-br"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if rezultat.returncode != 0:
            logger.debug("  OVS nu este disponibil (curățare omisă)")
            return True
        
        bridge_uri = rezultat.stdout.strip().split('\n')
        bridge_uri = [b for b in bridge_uri if b]
        
        for bridge in bridge_uri:
            logger.info(f"  Eliminare bridge: {bridge}")
            subprocess.run(
                ["sudo", "ovs-vsctl", "--if-exists", "del-br", bridge],
                capture_output=True,
                timeout=10
            )
        
        logger.info("  ✓ Curățare OVS reușită")
        return True
    except FileNotFoundError:
        logger.debug("  OVS nu este instalat (curățare omisă)")
        return True
    except Exception as e:
        logger.warning(f"  ! Eroare la curățarea OVS: {e}")
        return True  # Nu este critică


# ═══════════════════════════════════════════════════════════════════════════════
# CURATARE_ARTEFACTE
# ═══════════════════════════════════════════════════════════════════════════════

def curata_artefacte(complet: bool = False) -> None:
    """
    Curăță artefactele generate.
    
    Argumente:
        complet: Dacă să elimine toate artefactele
    """
    logger.info("Curățarea artefactelor...")
    
    director_artefacte = RADACINA_PROIECT / "artifacts"
    director_pcap = RADACINA_PROIECT / "pcap"
    
    if not complet:
        logger.info("  Păstrează artefactele (folosește --full pentru a le elimina)")
        return
    
    # Curăță directorul de artefacte
    if director_artefacte.exists():
        for f in director_artefacte.glob("*"):
            if f.name != ".gitkeep":
                if f.is_file():
                    f.unlink()
                    logger.debug(f"  Eliminat: {f.name}")
        logger.info("  ✓ Artefacte curățate")
    
    # Curăță directorul pcap
    if director_pcap.exists():
        for f in director_pcap.glob("*.pcap"):
            f.unlink()
            logger.debug(f"  Eliminat: {f.name}")
        logger.info("  ✓ Capturi de pachete curățate")


# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Punct de intrare principal."""
    
    # ───────────────────────────────────────────────────────────────────────
    # Pasul 1: Parsare argumente
    # ───────────────────────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="Curăță mediul de laborator Săptămâna 6"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Elimină volumele și toate datele (folosește înainte de săptămâna următoare)"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Elimină și resursele Docker neutilizate"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Arată ce ar fi eliminat fără să elimine efectiv"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Omite solicitările de confirmare"
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
    
    # ───────────────────────────────────────────────────────────────────────
    # Pasul 2: Inițializare Docker Manager
    # ───────────────────────────────────────────────────────────────────────
    director_docker = RADACINA_PROIECT / "docker"
    
    try:
        docker = DockerManager(director_docker)
    except FileNotFoundError as e:
        logger.error(f"Configurația Docker nu a fost găsită: {e}")
        return 1
    
    # ───────────────────────────────────────────────────────────────────────
    # Pasul 3: Afișare banner
    # ───────────────────────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("Curățarea mediului de laborator Săptămâna 6")
    if args.full:
        logger.info("Mod: Curățare COMPLETĂ (elimină toate datele)")
    else:
        logger.info("Mod: Curățare standard (păstrează datele)")
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("[SIMULARE] Nu se vor face modificări")
        logger.info("")
    
    # ───────────────────────────────────────────────────────────────────────
    # Pasul 4: Confirmare pentru curățare completă
    # ───────────────────────────────────────────────────────────────────────
    if args.full and not args.force and not args.dry_run:
        print()
        print("ATENȚIE: Curățarea completă va elimina toate datele inclusiv:")
        print("  - Volumele Docker")
        print("  - Capturile de pachete")
        print("  - Artefactele generate")
        print()
        raspuns = input("Ești sigur? (da/nu): ")
        if raspuns.lower() not in ("da", "d", "yes", "y"):
            print("Curățare anulată")
            return 0
    
    try:
        # ───────────────────────────────────────────────────────────────────
        # Pasul 5: Oprește serviciile Docker Compose
        # ───────────────────────────────────────────────────────────────────
        logger.info("")
        logger.info("Oprirea serviciilor Docker...")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)
        
        # ───────────────────────────────────────────────────────────────────
        # Pasul 6: Elimină resursele Docker specifice săptămânii
        # ───────────────────────────────────────────────────────────────────
        logger.info("")
        logger.info(f"Eliminarea resurselor {PREFIX_SAPTAMANA}_*...")
        docker.remove_by_prefix(PREFIX_SAPTAMANA, dry_run=args.dry_run)
        
        # ───────────────────────────────────────────────────────────────────
        # Pasul 7: Curăță Mininet (dacă este disponibil)
        # ───────────────────────────────────────────────────────────────────
        if not args.dry_run:
            logger.info("")
            curata_mininet()
        
        # ───────────────────────────────────────────────────────────────────
        # Pasul 8: Curăță OVS (dacă este disponibil)
        # ───────────────────────────────────────────────────────────────────
        if not args.dry_run:
            logger.info("")
            curata_ovs()
        
        # ───────────────────────────────────────────────────────────────────
        # Pasul 9: Curăță artefactele
        # ───────────────────────────────────────────────────────────────────
        if not args.dry_run:
            logger.info("")
            curata_artefacte(complet=args.full)
        
        # ───────────────────────────────────────────────────────────────────
        # Pasul 10: Elimină resursele Docker neutilizate (opțional)
        # ───────────────────────────────────────────────────────────────────
        if args.prune and not args.dry_run:
            logger.info("")
            logger.info("Eliminarea resurselor Docker neutilizate...")
            docker.system_prune()
        
        # ───────────────────────────────────────────────────────────────────
        # Pasul 11: Afișează sumar
        # ───────────────────────────────────────────────────────────────────
        logger.info("")
        logger.info("=" * 60)
        if args.dry_run:
            logger.info("[SIMULARE] Simulare curățare completă")
        else:
            logger.info("✓ Curățare completă!")
            if args.full:
                logger.info("Sistemul este pregătit pentru următoarea sesiune de laborator.")
            else:
                logger.info("Containerele au fost eliminate, datele au fost păstrate.")
                logger.info("Folosește --full pentru a elimina toate datele.")
        logger.info("=" * 60)
        
        return 0
    
    except KeyboardInterrupt:
        print("\nCurățare întreruptă")
        return 130
    except Exception as e:
        logger.error(f"Curățare eșuată: {e}")
        return 1


# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
