# ============================================================================
# DÉMONSTRATION COMPLÈTE DU PROJET BIG DATA
# Objectif : Exécuter le pipeline complet avec explications
# ============================================================================

"""
★★★ PROJET BIG DATA - SYSTÈME D'ORIENTATION NATIONALE ★★★

Ce script démontre l'exécution complète du projet de A à Z.
Chaque étape est commentée comme si vous la faisiez vous-même.

Étapes du projet :
1. ✅ Génération du dataset massif (5000+ candidats)
2. ✅ Stockage dans un répertoire (simulation HDFS)
3. ✅ MapReduce : calcul du score FG et classement
4. ✅ Hive : analyses statistiques
5. ✅ HBase : affectations nationales
6. ✅ Visualisations : graphiques statistiques
7. ✅ Menu interactif : orchestrer tout cela

Usage :
    python DEMO_COMPLETE.py
"""

import sys
import os

# Ajouter le répertoire scripts au chemin Python pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

# ============================================================================
# ÉTAPE 1 : IMPORTER LES MODULES
# ============================================================================

print("\n" + "="*80)
print(" "*20 + "DÉMONSTRATION COMPLÈTE - PROJET BIG DATA")
print("="*80)

print("\n📦 Étape 1 : Import des modules...\n")

try:
    # Importer tous les modules nécessaires
    from generation_dataset import (
        creation_liste_candidats,
        creation_notes,
        creation_choix,
        creation_filiere,
        generer_dataset_complet
    )
    from mapreduce_job import job_mapreduce_score_fg
    from hive_queries import executer_requetes_hive
    from hbase_operations import creation_resultat
    from visualisations import trace_courbes
    
    print("✅ Tous les modules importés avec succès!")
    
except ImportError as e:
    print(f"❌ ERREUR : {str(e)}")
    print("Assurez-vous que tous les fichiers sont dans le répertoire 'scripts/'")
    sys.exit(1)


# ============================================================================
# ÉTAPE 2 : CONFIGURATION
# ============================================================================

print("\n" + "-"*80)
print("📋 CONFIGURATION DU PROJET")
print("-"*80)

# Configuration
NOMBRE_CANDIDATS = 5000
DOSSIER_DATA = "data"
DOSSIER_VISUALS = "visualisations"

print(f"""
Configuration :
  • Nombre de candidats : {NOMBRE_CANDIDATS}
  • Dossier des données : {DOSSIER_DATA}
  • Dossier des graphiques : {DOSSIER_VISUALS}
  • Matières considérées : 8 (Analyse, Algèbre, Physique, Chimie, Informatique, STA, Français, Anglais)
  • Filières disponibles : MP, PC
  • Choix par candidat : 3
""")


# ============================================================================
# ÉTAPE 3 : GÉNÉRER LE DATASET COMPLET
# ============================================================================

def demo_etape_1_dataset():
    """
    ÉTAPE 1 : GÉNÉRATION DU DATASET MASSIF
    
    Objectif : Créer un dataset de 5000 candidats avec leurs notes et choix
    
    Fichiers générés :
      • candidats.txt : Liste des candidats avec filière
      • notes.txt : Notes pour chaque candidat (8 matières)
      • choix.txt : 3 choix de filière par candidat
      • filiere.json : Dictionnaire des filières
    """
    
    print("\n" + "="*80)
    print("ÉTAPE 1 : GÉNÉRATION DU DATASET MASSIF")
    print("="*80)
    
    print("""
Concept :
  Le dataset est généré de manière aléatoire mais réaliste pour simuler
  une vraie base de candidats à l'orientation nationale.
  
Processus :
  1. Créer 5000 candidats avec des noms, prénoms et filière (MP/PC)
  2. Générer 8 notes (0-20) pour chaque candidat
  3. Donner 3 choix de filière à chaque candidat
  4. Créer un dictionnaire des filières avec capacités

Résultat :
  ✓ 5000 candidats générés
  ✓ 40,000 notes générées (5000 x 8 matières)
  ✓ 15,000 choix générés (5000 x 3 choix)
  ✓ 5 filières avec capacités différentes
""")
    
    # Générer le dataset
    generer_dataset_complet(NOMBRE_CANDIDATS)
    
    print("\n✅ ÉTAPE 1 TERMINÉE : Dataset généré et sauvegardé!")


# ============================================================================
# ÉTAPE 4 : MAPREDUCE
# ============================================================================

def demo_etape_2_mapreduce():
    """
    ÉTAPE 2 : TRAITEMENT MAPREDUCE - CALCUL DU SCORE FG
    
    Objectif : Calculer le score FG pour chaque candidat et générer un classement
    
    Formule FG (Score Global pondéré) :
      FG = Analyse*8 + Algèbre*6 + Physique*8 + Chimie*6 
           + Informatique*6 + STA*4 + Français*3 + Anglais*3
    
    Processus MapReduce :
      1. MAPPER : Fusionne candidats.txt + notes.txt
      2. REDUCE : Calcule FG et assigne les rangs
      3. OUTPUT : Génère rang.txt trié par FG décroissant
    """
    
    print("\n" + "="*80)
    print("ÉTAPE 2 : MAPREDUCE - CALCUL DU SCORE FG ET CLASSEMENT")
    print("="*80)
    
    print("""
Architecture MapReduce :
  
  Entrées : candidats.txt + notes.txt
    ↓
  [MAPPER] : Fusionne les données par Num_CIN
    ↓
  [SHUFFLE & SORT] : Groupe par candidat
    ↓
  [REDUCER] : Calcule FG, trie, assigne rangs
    ↓
  Sortie : rang.txt (Num_CIN FG Rang)

Formule de Score :
  • Analyse (Coeff 8) : Discipline fondamentale
  • Algèbre (Coeff 6) : Discipline fondamentale
  • Physique (Coeff 8) : Discipline scientifique
  • Chimie (Coeff 6) : Discipline scientifique
  • Informatique (Coeff 6) : Compétence future
  • STA (Coeff 4) : Statistiques/Probabilités
  • Français (Coeff 3) : Langue maternelle
  • Anglais (Coeff 3) : Langue étrangère

Exemple de calcul :
  Si candidat a : [14, 13, 16, 12, 15, 14, 11, 10]
  FG = 14*8 + 13*6 + 16*8 + 12*6 + 15*6 + 14*4 + 11*3 + 10*3
     = 112 + 78 + 128 + 72 + 90 + 56 + 33 + 30
     = 599
""")
    
    # Exécuter le job MapReduce
    job_mapreduce_score_fg()
    
    print("\n✅ ÉTAPE 2 TERMINÉE : Rangs calculés et classement généré!")


# ============================================================================
# ÉTAPE 5 : HIVE
# ============================================================================

def demo_etape_3_hive():
    """
    ÉTAPE 3 : REQUÊTES HIVE - ANALYSES ANALYTIQUES
    
    Objectif : Effectuer des analyses statistiques sur les données
    
    Requêtes exécutées :
      1. Moyenne par matière
      2. Statistiques des scores FG
      3. Distribution MP vs PC
      4. TOP 10 meilleurs scores
      5. Statistiques d'affectation
    """
    
    print("\n" + "="*80)
    print("ÉTAPE 3 : HIVE - ANALYSES ANALYTIQUES")
    print("="*80)
    
    print("""
Concepts Hive :
  • Hive est un entrepôt de données pour Hadoop
  • Utilise le langage HQL similaire au SQL
  • Exécute des requêtes ad-hoc sur les données
  • Parfait pour les analyses OLAP (Online Analytical Processing)

Tables créées :
  • candidats : Informations sur les candidats
  • notes : Notes par matière
  • rang : Classement avec scores FG
  • choix : Préférences des candidats
  • resultats : Affectations finales

Requêtes analytiques :
  1. GROUP BY matiere → Moyennes
  2. SELECT AVG(FG), MIN(FG), MAX(FG) → Statistiques
  3. GROUP BY filiere → Distribution
  4. ORDER BY FG DESC LIMIT 10 → Top 10
  5. GROUP BY filiere_affectee → Répartition affectations
""")
    
    # Exécuter les requêtes Hive
    executer_requetes_hive()
    
    print("\n✅ ÉTAPE 3 TERMINÉE : Analyses Hive exécutées!")


# ============================================================================
# ÉTAPE 6 : HBASE
# ============================================================================

def demo_etape_4_hbase():
    """
    ÉTAPE 4 : HBASE - AFFECTATIONS NATIONALES
    
    Objectif : Utiliser une base NoSQL pour gérer les affectations
    
    Tables HBase créées :
      • FILIERE : Capacités et places disponibles
      • CHOIX : Préférences des candidats
      • RESULTATS : Affectations finales
    
    Algorithme d'affectation :
      Parcourir par rang décroissant (meilleur au premier)
      Pour chaque candidat :
        • Tester choix1, sinon choix2, sinon choix3
        • Vérifier les places disponibles
        • Affecter et décrémenter la capacité
    """
    
    print("\n" + "="*80)
    print("ÉTAPE 4 : HBASE - AFFECTATIONS NATIONALES")
    print("="*80)
    
    print("""
Architecture HBase (NoSQL) :
  
  Table FILIERE :
    Row Key : Code_Filiere (E101, E205, E301, E402, E503)
    Columns : capacite_total, places_restantes, nom_ecole
    
  Table CHOIX :
    Row Key : Num_CIN
    Columns : choix1, choix2, choix3
    
  Table RESULTATS :
    Row Key : Num_CIN
    Columns : filiere_affectee, rang
  
  Avantages NoSQL :
    ✓ Décrémentation atomique des capacités
    ✓ Accès rapide aux affectations
    ✓ Flexible pour les mises à jour
    ✓ Scalabilité horizontale

Algorithme d'affectation (système juste) :
  Principe : Respect du mérite + Respect des choix
  
  1. Trier candidats par rang (1 = meilleur)
  2. Pour each candidat(i) :
       a. Chercher choix1(i) disponible ?
            Si oui → affecter + décrémenter
          
       b. Sinon, chercher choix2(i) disponible ?
            Si oui → affecter + décrémenter
          
       c. Sinon, chercher choix3(i) disponible ?
            Si oui → affecter + décrémenter
          
       d. Sinon → REFUSE
  
  Exemple :
    • Candidat 1 (rang 1) : choix [E101, E205, E301] → affecté à E101 ✓
    • Candidat 2 (rang 2) : choix [E101, E205, E301] → E101 plein, affecté à E205 ✓
    • Candidat 3 (rang 3) : choix [E101, E205, ...] → E101 plein, E205 plein → choix3 ✓
    • ...
    • Candidat 5000 : Tous les choix pleins → REFUSE ✗
""")
    
    # Exécuter l'algorithme d'affectation
    creation_resultat()
    
    print("\n✅ ÉTAPE 4 TERMINÉE : Affectations calculées!")


# ============================================================================
# ÉTAPE 7 : VISUALISATIONS
# ============================================================================

def demo_etape_5_visualisations():
    """
    ÉTAPE 5 : VISUALISATIONS - GRAPHIQUES STATISTIQUES
    
    Objectif : Créer des visualisations pour interpréter les données
    
    Graphiques générés :
      1. Histogrammes des notes par matière
      2. Distribution MP vs PC (camembert)
      3. Courbe des moyennes par matière
      4. Histogramme des scores FG
      5. Répartition des affectations par filière
    """
    
    print("\n" + "="*80)
    print("ÉTAPE 5 : VISUALISATIONS - GRAPHIQUES STATISTIQUES")
    print("="*80)
    
    print(f"""
Graphiques générés dans '{DOSSIER_VISUALS}/' :

  1. Histogrammes_Matieres.png
     • 8 graphiques côte à côte (une matière par graphique)
     • Distribution des notes pour chaque matière
     • Montre la courbe gaussienne de répartition
     • Indique la moyenne avec une ligne rouge

  2. Distribution_Filieres.png
     • Camembert (pie chart) montrant MP et PC
     • Pourcentages et nombres absolus
     • Permet de visualiser la répartition

  3. Courbe_Moyennes.png
     • Ligne montrant l'évolution des moyennes
     • Bande d'écart-type (moyenne ± écart-type)
     • Ligne horizontale à 10 (moyenne théorique)

  4. Histogramme_FG.png
     • Distribution des scores FG de tous les candidats
     • Lignes pour moyenne et médiane
     • Statistiques texte (min, max, écart-type)

  5. Repartition_Affectations.png
     • Barres montrant affectations par filière
     • Code couleur : vert = affectée, rouge = AUCUNE
     • Nombres sur les barres

Interprétation statistique :
  • Moyenne = Tendance centrale
  • Médiane = Valeur du milieu (résistante aux extrêmes)
  • Écart-type = Dispersion (normal si 3-4 points)
  • Distribution = Gaussienne si bien équilibrée
""")
    
    # Générer les visualisations
    trace_courbes()
    
    print(f"\n✅ ÉTAPE 5 TERMINÉE : Graphiques générés dans '{DOSSIER_VISUALS}/'!")


# ============================================================================
# ÉTAPE 8 : RÉSUMÉS FINAUX
# ============================================================================

def afficher_resumes():
    """
    Afficher des résumés et statistiques finales
    """
    
    print("\n" + "="*80)
    print("RÉSUMÉS ET STATISTIQUES FINALES")
    print("="*80)
    
    try:
        # Résumé : Total candidats
        with open("data/candidats.txt", 'r', encoding='utf-8') as f:
            lignes = f.readlines()
            total_candidats = len(lignes) - 1  # Exclure l'en-tête
        
        # Résumé : Top 10
        print("\n🏆 TOP 10 DES MEILLEURS CANDIDATS")
        print("-"*80)
        print(f"{'Rang':<6} {'Num_CIN':<12} {'Nom & Prénom':<30} {'Score FG':<12}")
        print("-"*80)
        
        count = 0
        with open("data/rang.txt", 'r', encoding='utf-8') as f:
            f.readline()  # Ignorer l'en-tête
            for ligne in f:
                if count >= 10:
                    break
                parties = ligne.strip().split()
                if len(parties) >= 3:
                    num_cin = parties[0]
                    fg = float(parties[1])
                    rang = int(parties[2])
                    
                    # Récupérer le nom du candidat
                    with open("data/candidats.txt", 'r', encoding='utf-8') as cf:
                        cf.readline()
                        for ligne_c in cf:
                            if ligne_c.startswith(num_cin):
                                parties_c = ligne_c.strip().split()
                                if len(parties_c) >= 4:
                                    nom_prenom = parties_c[1] + " " + parties_c[2]
                                    print(f"{rang:<6} {num_cin:<12} {nom_prenom:<30} {fg:>8.2f}")
                                break
                    count += 1
        
        # Résumé : Affectations
        print("\n\n📊 RÉPARTITION FINALE DES AFFECTATIONS")
        print("-"*80)
        print(f"{'Filière':<25} {'Nombre Affectés':<20} {'Pourcentage':<15}")
        print("-"*80)
        
        affectations = {}
        with open("data/resultats.txt", 'r', encoding='utf-8') as f:
            f.readline()
            for ligne in f:
                parties = ligne.strip().split()
                if len(parties) >= 2:
                    filiere = parties[1]
                    if filiere not in affectations:
                        affectations[filiere] = 0
                    affectations[filiere] += 1
        
        for filiere in sorted(affectations.keys(), 
                             key=lambda x: affectations[x], 
                             reverse=True):
            nombre = affectations[filiere]
            pourcentage = (nombre / total_candidats * 100)
            print(f"{filiere:<25} {nombre:<20} {pourcentage:>6.2f}%")
        
        print("-"*80)
        print(f"{'TOTAL':<25} {total_candidats:<20} {100.0:>6.2f}%")
        
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """
    Exécuter la démonstration complète du projet Big Data
    """
    
    try:
        # Exécuter toutes les étapes
        demo_etape_1_dataset()
        
        input("\n⏸️  Appuyez sur ENTRÉE pour continuer vers MapReduce...")
        demo_etape_2_mapreduce()
        
        input("\n⏸️  Appuyez sur ENTRÉE pour continuer vers Hive...")
        demo_etape_3_hive()
        
        input("\n⏸️  Appuyez sur ENTRÉE pour continuer vers HBase...")
        demo_etape_4_hbase()
        
        input("\n⏸️  Appuyez sur ENTRÉE pour continuer vers Visualisations...")
        demo_etape_5_visualisations()
        
        # Afficher les résumés
        afficher_resumes()
        
        # Résumé final
        print("\n" + "="*80)
        print("✅ DÉMONSTRATION COMPLÈTE RÉUSSIE!")
        print("="*80)
        
        print("""
Fichiers générés :
  ✓ data/candidats.txt → 5000 candidats
  ✓ data/notes.txt → 40,000 notes (5000 x 8)
  ✓ data/filiere.json → Dictionnaire des filières
  ✓ data/choix.txt → 15,000 choix (5000 x 3)
  ✓ data/rang.txt → Classement MapReduce
  ✓ data/resultats.txt → Affectations finales
  ✓ visualisations/*.png → 5 graphiques

Pipeline exécuté :
  Dataset → HDFS → MapReduce → Hive → HBase → Visualisations
  
Le projet est maintenant prêt pour :
  • La rédaction du rapport
  • La présentation au professeur
  • L'évaluation selon la grille (20 points)
""")
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
