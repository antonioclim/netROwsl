#!/usr/bin/env python3
"""
Tema 2: Client REST Complet
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Implementați un client care interacționează cu toate nivelurile REST.

TODO:
1. Implementați clientul pentru Nivelul 0 (RPC)
2. Implementați clientul pentru Nivelul 2 (Verbe HTTP)
3. Implementați clientul pentru Nivelul 3 (HATEOAS)
4. Adăugați navigare folosind linkurile HATEOAS
"""

import requests
import json


class ClientREST:
    """Client pentru interacțiunea cu API-ul REST."""
    
    def __init__(self, url_baza: str = "http://localhost:5000"):
        """
        Inițializează clientul.
        
        Args:
            url_baza: URL-ul de bază al serverului REST
        """
        self.url_baza = url_baza
        self.sesiune = requests.Session()
    
    # ═══════════════════════════════════════════════════════════
    # NIVELUL 0: RPC peste HTTP
    # ═══════════════════════════════════════════════════════════
    
    def nivel0_listeaza(self) -> dict:
        """
        Listează toate produsele folosind stilul RPC.
        
        TODO: Implementați cererea POST cu {"actiune": "listeaza"}
        
        Returns:
            Dicționar cu rezultatul
        """
        # Implementați aici
        pass
    
    def nivel0_creeaza(self, date: dict) -> dict:
        """
        Creează un produs nou folosind stilul RPC.
        
        TODO: Implementați cererea POST cu {"actiune": "creeaza", "date": ...}
        
        Args:
            date: Datele produsului
        
        Returns:
            Dicționar cu rezultatul
        """
        # Implementați aici
        pass
    
    # ═══════════════════════════════════════════════════════════
    # NIVELUL 2: Verbe HTTP
    # ═══════════════════════════════════════════════════════════
    
    def nivel2_listeaza(self) -> list:
        """
        Listează produsele folosind GET.
        
        TODO: Implementați cererea GET /api/nivel2/produse
        
        Returns:
            Lista de produse
        """
        # Implementați aici
        pass
    
    def nivel2_creeaza(self, date: dict) -> dict:
        """
        Creează un produs folosind POST.
        
        TODO: Implementați cererea POST /api/nivel2/produse
        
        Args:
            date: Datele produsului
        
        Returns:
            Produsul creat
        """
        # Implementați aici
        pass
    
    def nivel2_actualizeaza(self, id_produs: int, date: dict) -> dict:
        """
        Actualizează un produs folosind PUT.
        
        TODO: Implementați cererea PUT /api/nivel2/produse/{id}
        
        Args:
            id_produs: ID-ul produsului
            date: Datele noi
        
        Returns:
            Produsul actualizat
        """
        # Implementați aici
        pass
    
    def nivel2_sterge(self, id_produs: int) -> bool:
        """
        Șterge un produs folosind DELETE.
        
        TODO: Implementați cererea DELETE /api/nivel2/produse/{id}
        
        Args:
            id_produs: ID-ul produsului
        
        Returns:
            True dacă ștergerea a reușit
        """
        # Implementați aici
        pass
    
    # ═══════════════════════════════════════════════════════════
    # NIVELUL 3: HATEOAS
    # ═══════════════════════════════════════════════════════════
    
    def nivel3_navigheaza(self, url_start: str = None) -> dict:
        """
        Navighează API-ul folosind linkurile HATEOAS.
        
        TODO: Implementați navigarea folosind câmpul _linkuri
        
        Args:
            url_start: URL-ul de pornire (implicit: /api/nivel3/produse)
        
        Returns:
            Răspunsul curent cu linkuri
        """
        # Implementați aici
        pass
    
    def nivel3_urmareaza_link(self, raspuns: dict, nume_link: str) -> dict:
        """
        Urmărește un link din răspunsul HATEOAS.
        
        TODO: Extrageți href din _linkuri și faceți cererea
        
        Args:
            raspuns: Răspunsul anterior cu _linkuri
            nume_link: Numele linkului de urmărit
        
        Returns:
            Răspunsul de la link
        """
        # Implementați aici
        pass


def meniu_interactiv():
    """
    Meniu interactiv pentru utilizator.
    
    TODO: Implementați un meniu cu opțiuni pentru toate operațiile
    """
    client = ClientREST()
    
    while True:
        print("\n" + "=" * 50)
        print("  CLIENT REST - Meniu Principal")
        print("=" * 50)
        print("  1. Nivelul 0 - Listare (RPC)")
        print("  2. Nivelul 2 - Operații CRUD")
        print("  3. Nivelul 3 - Navigare HATEOAS")
        print("  0. Ieșire")
        print("-" * 50)
        
        optiune = input("  Alegeți opțiunea: ").strip()
        
        if optiune == "0":
            print("  La revedere!")
            break
        elif optiune == "1":
            # TODO: Implementați submeniul pentru Nivelul 0
            pass
        elif optiune == "2":
            # TODO: Implementați submeniul pentru Nivelul 2
            pass
        elif optiune == "3":
            # TODO: Implementați submeniul pentru Nivelul 3
            pass
        else:
            print("  Opțiune invalidă!")


if __name__ == "__main__":
    meniu_interactiv()
