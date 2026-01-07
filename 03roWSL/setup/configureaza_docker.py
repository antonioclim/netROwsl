#!/usr/bin/env python3
"""
Asistent de Configurare Docker
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică și ajută la configurarea Docker Desktop pentru laborator.

Utilizare:
    python setup/configureaza_docker.py
"""

import subprocess
import sys
import json
from pathlib import Path


class ConfiguratorDocker:
    """Verifică și configurează Docker pentru laborator."""
    
    def __init__(self):
        self.erori = []
        self.avertismente = []
    
    def verifica_daemon(self) -> bool:
        """Verifică dacă daemon-ul Docker rulează."""
        print("Verificare daemon Docker...")
        try:
            rezultat = subprocess.run(
                ["docker", "info", "--format", "{{json .}}"],
                capture_output=True,
                timeout=30
            )
            if rezultat.returncode == 0:
                print("  ✓ Daemon-ul Docker rulează")
                return True
            else:
                print("  ✗ Daemon-ul Docker nu răspunde")
                self.erori.append("Porniți Docker Desktop")
                return False
        except FileNotFoundError:
            print("  ✗ Docker nu este instalat")
            self.erori.append("Instalați Docker Desktop")
            return False
        except subprocess.TimeoutExpired:
            print("  ✗ Timeout la conectarea la Docker")
            self.erori.append("Docker Desktop pare să nu răspundă")
            return False
    
    def verifica_compose(self) -> bool:
        """Verifică disponibilitatea Docker Compose."""
        print("\nVerificare Docker Compose...")
        try:
            rezultat = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                versiune = rezultat.stdout.decode().strip()
                print(f"  ✓ Docker Compose disponibil: {versiune}")
                return True
            else:
                print("  ✗ Docker Compose nu este disponibil")
                self.erori.append("Actualizați Docker Desktop pentru Compose V2")
                return False
        except Exception as e:
            print(f"  ✗ Eroare la verificare: {e}")
            return False
    
    def verifica_resurse(self) -> bool:
        """Verifică resursele alocate Docker."""
        print("\nVerificare resurse Docker...")
        try:
            rezultat = subprocess.run(
                ["docker", "info", "--format", "{{json .}}"],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                info = json.loads(rezultat.stdout.decode())
                
                # Verifică memoria
                memorie_gb = info.get('MemTotal', 0) / (1024**3)
                if memorie_gb >= 4:
                    print(f"  ✓ Memorie disponibilă: {memorie_gb:.1f} GB")
                else:
                    print(f"  ⚠ Memorie disponibilă: {memorie_gb:.1f} GB (recomandat: 4GB+)")
                    self.avertismente.append("Creșteți memoria alocată în Docker Desktop Settings")
                
                # Verifică CPU-urile
                cpus = info.get('NCPU', 0)
                if cpus >= 2:
                    print(f"  ✓ CPU-uri disponibile: {cpus}")
                else:
                    print(f"  ⚠ CPU-uri disponibile: {cpus} (recomandat: 2+)")
                    self.avertismente.append("Creșteți CPU-urile alocate în Docker Desktop Settings")
                
                return True
        except Exception as e:
            print(f"  ✗ Nu s-au putut verifica resursele: {e}")
            return False
    
    def verifica_retea(self) -> bool:
        """Verifică configurația de rețea Docker."""
        print("\nVerificare rețele Docker...")
        try:
            # Verifică dacă rețeaua week3 există deja
            rezultat = subprocess.run(
                ["docker", "network", "ls", "--filter", "name=week3", "--format", "{{.Name}}"],
                capture_output=True,
                timeout=10
            )
            retele = rezultat.stdout.decode().strip().split('\n')
            retele = [r for r in retele if r]
            
            if retele:
                print(f"  ℹ Rețele week3 existente: {', '.join(retele)}")
                print("    (Vor fi refolosite sau recreate la pornirea laboratorului)")
            else:
                print("  ✓ Nicio rețea week3 existentă (se va crea la pornire)")
            
            # Verifică subnet-ul
            rezultat = subprocess.run(
                ["docker", "network", "inspect", "bridge", "--format", "{{range .IPAM.Config}}{{.Subnet}}{{end}}"],
                capture_output=True,
                timeout=10
            )
            subnet_bridge = rezultat.stdout.decode().strip()
            print(f"  ℹ Subnet bridge implicit: {subnet_bridge}")
            
            # Verifică conflict potențial
            if "172.20.0" in subnet_bridge:
                print("  ⚠ Potențial conflict cu subnet-ul laboratorului (172.20.0.0/24)")
                self.avertismente.append("Subnet-ul 172.20.0.0/24 ar putea fi în conflict")
            else:
                print("  ✓ Niciun conflict de subnet detectat")
            
            return True
        except Exception as e:
            print(f"  ✗ Eroare la verificarea rețelei: {e}")
            return False
    
    def testeaza_construire_imagine(self) -> bool:
        """Testează că Docker poate construi imagini."""
        print("\nTestare capabilitate de construire...")
        try:
            # Test simplu de build
            rezultat = subprocess.run(
                ["docker", "build", "--help"],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                print("  ✓ Comanda docker build disponibilă")
                return True
            else:
                print("  ✗ Comanda docker build nu funcționează")
                return False
        except Exception as e:
            print(f"  ✗ Eroare: {e}")
            return False
    
    def verifica_fisier_compose(self) -> bool:
        """Verifică fișierul docker-compose.yml."""
        print("\nVerificare docker-compose.yml...")
        
        cale_compose = Path(__file__).parent.parent / "docker" / "docker-compose.yml"
        
        if not cale_compose.exists():
            print(f"  ✗ Fișierul nu există: {cale_compose}")
            self.erori.append("Fișierul docker-compose.yml lipsește")
            return False
        
        print(f"  ✓ Fișier găsit: {cale_compose}")
        
        # Validare YAML
        try:
            import yaml
            with open(cale_compose, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            servicii = config.get('services', {})
            print(f"  ✓ Servicii definite: {', '.join(servicii.keys())}")
            
            retele = config.get('networks', {})
            print(f"  ✓ Rețele definite: {', '.join(retele.keys())}")
            
            return True
        except ImportError:
            print("  ⚠ PyYAML nu este instalat, nu s-a putut valida YAML")
            self.avertismente.append("Instalați pyyaml pentru validare completă")
            return True
        except Exception as e:
            print(f"  ✗ Eroare la parsarea YAML: {e}")
            self.erori.append(f"docker-compose.yml invalid: {e}")
            return False
    
    def afiseaza_sumar(self) -> int:
        """Afișează sumarul verificărilor."""
        print("\n" + "=" * 50)
        print("SUMAR CONFIGURARE DOCKER")
        print("=" * 50)
        
        if self.erori:
            print("\n✗ Erori care necesită atenție:")
            for eroare in self.erori:
                print(f"  - {eroare}")
        
        if self.avertismente:
            print("\n⚠ Avertismente (opționale):")
            for avertisment in self.avertismente:
                print(f"  - {avertisment}")
        
        if not self.erori:
            print("\n✓ Docker este configurat corect pentru laborator!")
            print("\nPașii următori:")
            print("  1. python scripts/porneste_lab.py")
            print("  2. Așteptați pornirea containerelor")
            print("  3. Accesați https://localhost:9443 pentru Portainer")
            return 0
        else:
            print("\nVă rugăm să remediați erorile de mai sus.")
            return 1
    
    def ruleaza(self) -> int:
        """Rulează toate verificările."""
        print("=" * 50)
        print("Configurare Docker pentru Laboratorul Săptămânii 3")
        print("Rețele de Calculatoare - ASE, Informatică Economică")
        print("=" * 50)
        
        if not self.verifica_daemon():
            return self.afiseaza_sumar()
        
        self.verifica_compose()
        self.verifica_resurse()
        self.verifica_retea()
        self.testeaza_construire_imagine()
        self.verifica_fisier_compose()
        
        return self.afiseaza_sumar()


def main():
    """Punctul principal de intrare."""
    configurator = ConfiguratorDocker()
    return configurator.ruleaza()


if __name__ == "__main__":
    sys.exit(main())
