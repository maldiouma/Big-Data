# ============================================================================
# MODULE : STOCKAGE HBASE ET CALCUL DES AFFECTATIONS
# Objectif : Simuler HBase et générer les affectations finales
# ============================================================================

import json
import os

# ============================================================================
# CLASSE SIMPLIFIÉE POUR SIMULER HBASE
# (En production, on utiliserait la librarie HappyBase)
# ============================================================================

class HBaseSimulee:
    """
    Simulation d'une base HBase avec des dictionnaires Python
    Structure :
    - Table FILIERE : clé = code_filiere, valeur = {capacité, places_restantes}
    - Table CHOIX : clé = Num_CIN, valeur = [Choix1, Choix2, Choix3]
    - Table RESULTATS : clé = Num_CIN, valeur = {filiere_affectee, rang}
    """
    
    def __init__(self):
        """Initialiser les 3 tables HBase"""
        self.table_filiere = {}
        self.table_choix = {}
        self.table_resultats = {}
    
    def creer_table_filiere(self, filieres):
        """
        Créer la table FILIERE
        Structure : {code_filiere: {"capacite": X, "places_restantes": X, "nom": "..."}}
        """
        print("🗄️  HBase - Création de la table FILIERE...")
        
        for code_filiere, (nom_ecole, capacite) in filieres.items():
            self.table_filiere[code_filiere] = {
                "capacite": capacite,
                "places_restantes": capacite,
                "nom_ecole": nom_ecole
            }
        
        print(f"   ✓ Table FILIERE créée avec {len(self.table_filiere)} filières")
        
        return self.table_filiere
    
    def creer_table_choix(self, choix):
        """
        Créer la table CHOIX
        Structure : {Num_CIN: [Choix1, Choix2, Choix3]}
        """
        print("🗄️  HBase - Création de la table CHOIX...")
        
        self.table_choix = choix.copy()
        
        print(f"   ✓ Table CHOIX créée avec {len(self.table_choix)} candidats")
        
        return self.table_choix
    
    def creer_table_resultats(self):
        """
        Créer la table RESULTATS (vide initialement)
        Structure : {Num_CIN: {filiere_affectee, rang}}
        """
        print("🗄️  HBase - Création de la table RESULTATS...")
        
        self.table_resultats = {}
        
        print("   ✓ Table RESULTATS créée (vide)")
        
        return self.table_resultats
    
    def tester_choix(self, num_cin, rang_dict):
        """
        Tester les choix d'un candidat dans l'ordre
        Retourner le premier choix disponible
        """
        
        # Récupérer les choix du candidat
        if num_cin not in self.table_choix:
            return None
        
        choix_candidat = self.table_choix[num_cin]
        
        # Tester chaque choix dans l'ordre
        for choix in choix_candidat:
            # Vérifier que la filière existe
            if choix in self.table_filiere:
                # Vérifier qu'il reste des places
                if self.table_filiere[choix]["places_restantes"] > 0:
                    # Décrémenter les places disponibles
                    self.table_filiere[choix]["places_restantes"] -= 1
                    return choix
        
        # Aucun choix disponible
        return None
    
    def inserer_resultat(self, num_cin, filiere_affectee, rang):
        """
        Insérer un résultat d'affectation dans HBase
        """
        self.table_resultats[num_cin] = {
            "filiere_affectee": filiere_affectee,
            "rang": rang
        }
    
    def scan_filiere(self):
        """
        Afficher l'état de la table FILIERE (capacités restantes)
        """
        print("\n🔍 HBase SCAN - Table FILIERE :")
        print("-" * 80)
        print(f"{'Code Filière':<15} {'Nom École':<30} {'Capacité':<10} {'Places Restantes':<15}")
        print("-" * 80)
        
        for code_filiere, donnees in self.table_filiere.items():
            print(f"{code_filiere:<15} {donnees['nom_ecole']:<30} {donnees['capacite']:<10} {donnees['places_restantes']:<15}")
        
        print("-" * 80 + "\n")
    
    def scan_resultats(self, limit=10):
        """
        Afficher les premiers résultats d'affectation
        """
        print("\n🔍 HBase SCAN - Table RESULTATS (premiers 10) :")
        print("-" * 80)
        print(f"{'Num_CIN':<12} {'Filière Affectée':<25} {'Rang':<10}")
        print("-" * 80)
        
        for i, (num_cin, donnees) in enumerate(list(self.table_resultats.items())[:limit], 1):
            print(f"{num_cin:<12} {donnees['filiere_affectee']:<25} {donnees['rang']:<10}")
        
        print("-" * 80 + "\n")


# ============================================================================
# FONCTION PRINCIPALE D'AFFECTATION
# ============================================================================

def creation_resultat(fichier_rang="data/rang.txt",
                     fichier_choix="data/choix.txt",
                     fichier_filieres="data/filiere.json",
                     fichier_resultats="data/resultats.txt"):
    """
    ALGORITHME D'AFFECTATION NATIONAL :
    
    Principe :
    1. Charger les candidats triés par rang (meilleur au premier)
    2. Pour chaque candidat (dans l'ordre de rang) :
       a. Tester choix1
       b. Sinon tester choix2
       c. Sinon tester choix3
       d. Sinon pas d'affectation
    3. Décrémenter la capacité dans HBase à chaque affectation
    4. Générer le fichier resultats.txt
    
    Important : Cet algorithme respecte le principe de mérité.
    Un meilleur candidat a priorité sur un moins bon.
    """
    
    print("\n" + "="*70)
    print("ALGORITHME D'AFFECTATION - SYSTÈME D'ORIENTATION NATIONALE")
    print("="*70)
    
    # ========================================================================
    # ÉTAPE 1 : Charger les données
    # ========================================================================
    
    print("\n📖 Étape 1 : Chargement des données...")
    
    # Charger les rangs
    print("   • Chargement des rangs...")
    rangs = {}
    with open(fichier_rang, 'r', encoding='utf-8') as f:
        f.readline()  # Ignorer l'en-tête
        for ligne in f:
            parties = ligne.strip().split()
            if len(parties) >= 3:
                rangs[parties[0]] = int(parties[2])
    print(f"     ✓ {len(rangs)} candidats chargés")
    
    # Charger les choix
    print("   • Chargement des choix...")
    choix = {}
    with open(fichier_choix, 'r', encoding='utf-8') as f:
        f.readline()  # Ignorer l'en-tête
        for ligne in f:
            parties = ligne.strip().split()
            if len(parties) >= 4:
                choix[parties[0]] = parties[1:4]
    print(f"     ✓ {len(choix)} candidats avec leurs choix")
    
    # Charger les filières
    print("   • Chargement des filières...")
    with open(fichier_filieres, 'r', encoding='utf-8') as f:
        filieres = json.load(f)
    print(f"     ✓ {len(filieres)} filières chargées")
    
    # ========================================================================
    # ÉTAPE 2 : Initialiser HBase
    # ========================================================================
    
    print("\n📀 Étape 2 : Initialisation des tables HBase...")
    
    hbase = HBaseSimulee()
    hbase.creer_table_filiere(filieres)
    hbase.creer_table_choix(choix)
    hbase.creer_table_resultats()
    
    hbase.scan_filiere()
    
    # ========================================================================
    # ÉTAPE 3 : Appliquer l'algorithme d'affectation
    # ========================================================================
    
    print("\n🎯 Étape 3 : Affectation des candidats...")
    
    # Trier les candidats par rang (le 1er rang d'abord)
    candidats_tries = sorted(rangs.keys(), key=lambda x: rangs[x])
    
    affectations = 0
    non_affectations = 0
    
    # Pour chaque candidat dans l'ordre de rang
    for i, num_cin in enumerate(candidats_tries):
        rang = rangs[num_cin]
        
        # Tester les choix du candidat
        filiere_affectee = hbase.tester_choix(num_cin, rangs)
        
        if filiere_affectee:
            # Ajouter le résultat
            hbase.inserer_resultat(num_cin, filiere_affectee, rang)
            affectations += 1
            
            # Afficher la progression tous les 500 candidats
            if (i + 1) % 500 == 0:
                print(f"   Progression : {i + 1}/{len(candidats_tries)} candidats traités")
        else:
            non_affectations += 1
    
    print(f"   ✓ {affectations} candidats affectés")
    print(f"   ✗ {non_affectations} candidats non affectés")
    
    # ========================================================================
    # ÉTAPE 4 : Afficher l'état final de HBase
    # ========================================================================
    
    hbase.scan_filiere()
    hbase.scan_resultats()
    
    # ========================================================================
    # ÉTAPE 5 : Générer le fichier resultats.txt
    # ========================================================================
    
    print("\n📝 Étape 4 : Génération du fichier resultats.txt...")
    
    os.makedirs(os.path.dirname(fichier_resultats), exist_ok=True)
    
    with open(fichier_resultats, 'w', encoding='utf-8') as f:
        # En-tête
        f.write("Num_CIN Filiere_Affectee\n")
        
        # Données triées par rang
        for num_cin in candidats_tries:
            if num_cin in hbase.table_resultats:
                filiere = hbase.table_resultats[num_cin]["filiere_affectee"]
                f.write(f"{num_cin} {filiere}\n")
            else:
                # Candidat non affecté
                f.write(f"{num_cin} AUCUNE\n")
    
    print(f"   ✓ Fichier {fichier_resultats} généré")
    
    # ========================================================================
    # STATISTIQUES FINALES
    # ========================================================================
    
    print("\n" + "="*70)
    print("✅ AFFECTATION TERMINÉE")
    print("="*70)
    
    # Calculer les statistiques par filière
    stats_filieres = {}
    for num_cin, resultat in hbase.table_resultats.items():
        filiere = resultat["filiere_affectee"]
        if filiere not in stats_filieres:
            stats_filieres[filiere] = 0
        stats_filieres[filiere] += 1
    
    print("\n📊 RÉPARTITION DES AFFECTATIONS :")
    for code_filiere, nombre in sorted(stats_filieres.items()):
        capacite = hbase.table_filiere[code_filiere]["capacite"]
        pourcentage = (nombre / capacite * 100) if capacite > 0 else 0
        nom_ecole = hbase.table_filiere[code_filiere]["nom_ecole"]
        print(f"   • {code_filiere} ({nom_ecole}) : {nombre}/{capacite} ({pourcentage:.1f}%)")
    
    print(f"\n   • TOTAL AFFECTÉS : {affectations}/{len(candidats_tries)} ({affectations*100/len(candidats_tries):.1f}%)")
    print()


if __name__ == "__main__":
    # Exécuter l'algorithme d'affectation
    creation_resultat()
