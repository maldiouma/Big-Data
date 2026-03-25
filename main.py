# ============================================================================
# SCRIPT PRINCIPAL - MENU INTERACTIF
# Objectif : Menu principal pour exécuter toutes les étapes du projet
# ============================================================================

import sys
import os

# Ajouter le répertoire scripts au chemin Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

# Importer tous les modules du projet
from generation_dataset import generer_dataset_complet
from mapreduce_job import job_mapreduce_score_fg
from hive_queries import executer_requetes_hive
from hbase_operations import creation_resultat
from visualisations import trace_courbes

# ============================================================================
# MENU INTERACTIF
# ============================================================================

def afficher_banniere():
    """
    Afficher la bannière du projet
    """
    print("\n" + "="*70)
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "SYSTÈME D'ORIENTATION NATIONALE" + " "*23 + "║")
    print("║" + " "*20 + "PROJET BIG DATA - S10" + " "*28 + "║")
    print("╚" + "═"*68 + "╝")
    print("="*70)
    print("Hadoop | YARN | MapReduce | Hive | HBase | Python")
    print("="*70 + "\n")


def afficher_menu():
    """
    Afficher le menu principal avec les options disponibles
    """
    print("\n" + "─"*70)
    print("MENU PRINCIPAL - Choisissez une option")
    print("─"*70)
    print("""
1. 🔧 Générer le dataset (Candidats + Notes + Choix + Filières)
2. 🗂️  Afficher les fichiers générés et statistiques
3. 🖥️  Calculer le rang via MapReduce
4. 🏛️  Charger dans Hive et exécuter requêtes analytiques
5. 🔶 Traiter avec HBase et générer résultats d'orientation
6. 📈 Visualiser les statistiques (graphiques)
7. 🚀 EXÉCUTER LE PIPELINE COMPLET (1 → 6)
8. 📊 Afficher les résumés finaux
9. ❌ Quitter
""")
    print("─"*70 + "\n")


def option_1_gener_dataset():
    """
    Option 1 : Générer le dataset
    """
    print("\n" + "="*70)
    print("OPTION 1 - GÉNÉRATION DU DATASET")
    print("="*70)
    
    try:
        # Demander le nombre de candidats
        nb = input("\nNombre de candidats à générer (défaut: 5000) : ").strip()
        nombre_candidats = int(nb) if nb else 5000
        
        # Générer le dataset
        generer_dataset_complet(nombre_candidats)
        
        print("\n✅ ÉTAPE RÉUSSIE : Dataset généré avec succès!")
        
    except ValueError:
        print("❌ ERREUR : Veuillez entrer un nombre valide")
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


def option_2_afficher_fichiers():
    """
    Option 2 : Afficher les fichiers et statistiques
    """
    print("\n" + "="*70)
    print("OPTION 2 - FICHIERS GÉNÉRÉS")
    print("="*70)
    
    try:
        dossier_data = "data"
        
        if not os.path.exists(dossier_data):
            print(f"❌ ERREUR : Le dossier '{dossier_data}' n'existe pas")
            return
        
        # Lister les fichiers
        fichiers = os.listdir(dossier_data)
        
        if not fichiers:
            print(f"❌ ERREUR : Aucun fichier dans '{dossier_data}'")
            return
        
        print(f"\n📁 Fichiers dans '{dossier_data}' :")
        print("-"*70)
        
        total_size = 0
        for fichier in sorted(fichiers):
            chemin_complet = os.path.join(dossier_data, fichier)
            size = os.path.getsize(chemin_complet)
            size_mb = size / (1024 * 1024)
            total_size += size
            print(f"   • {fichier:<30} {size_mb:>8.2f} MB")
        
        print("-"*70)
        print(f"   {'TOTAL':<30} {total_size/(1024*1024):>8.2f} MB")
        
        # Afficher un aperçu du fichier candidats.txt
        print("\n📄 Aperçu du fichier 'candidats.txt' (5 premières lignes) :")
        print("-"*70)
        
        with open(os.path.join(dossier_data, "candidats.txt"), 'r', encoding='utf-8') as f:
            for i, ligne in enumerate(f):
                if i < 6:  # En-tête + 5 lignes
                    print(f"   {ligne.strip()}")
                else:
                    break
        
        print("-"*70)
        print("\n✅ Fichiers affichés avec succès")
        
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


def option_3_mapreduce():
    """
    Option 3 : Exécuter MapReduce pour calculer les rangs
    """
    print("\n" + "="*70)
    print("OPTION 3 - JOB MAPREDUCE")
    print("="*70)
    
    try:
        # Vérifier que les fichiers existent
        if not os.path.exists("data/candidats.txt") or not os.path.exists("data/notes.txt"):
            print("❌ ERREUR : Les fichiers candidats.txt et/ou notes.txt n'existent pas")
            print("   Veuillez d'abord générer le dataset (Option 1)")
            return
        
        # Exécuter MapReduce
        job_mapreduce_score_fg()
        
        print("✅ ÉTAPE RÉUSSIE : MapReduce exécuté avec succès!")
        
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


def option_4_hive():
    """
    Option 4 : Exécuter les requêtes Hive
    """
    print("\n" + "="*70)
    print("OPTION 4 - REQUÊTES HIVE")
    print("="*70)
    
    try:
        # Vérifier que les fichiers existent
        fichiers_requis = [
            "data/candidats.txt",
            "data/notes.txt",
            "data/rang.txt",
            "data/choix.txt"
        ]
        
        for fichier in fichiers_requis:
            if not os.path.exists(fichier):
                print(f"❌ ERREUR : Le fichier '{fichier}' n'existe pas")
                print("   Veuillez d'abord exécuter MapReduce (Option 3)")
                return
        
        # Exécuter les requêtes Hive
        executer_requetes_hive()
        
        print("✅ ÉTAPE RÉUSSIE : Requêtes Hive exécutées avec succès!")
        
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


def option_5_hbase():
    """
    Option 5 : HBase et résultats d'orientation
    """
    print("\n" + "="*70)
    print("OPTION 5 - HBASE ET RÉSULTATS D'ORIENTATION")
    print("="*70)
    
    try:
        # Vérifier que les fichiers existent
        fichiers_requis = [
            "data/rang.txt",
            "data/choix.txt",
            "data/filiere.json"
        ]
        
        for fichier in fichiers_requis:
            if not os.path.exists(fichier):
                print(f"❌ ERREUR : Le fichier '{fichier}' n'existe pas")
                return
        
        # Exécuter l'algorithme d'affectation
        creation_resultat()
        
        print("✅ ÉTAPE RÉUSSIE : Affectations calculées avec succès!")
        
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


def option_6_visualisations():
    """
    Option 6 : Générer les graphiques
    """
    print("\n" + "="*70)
    print("OPTION 6 - VISUALISATIONS")
    print("="*70)
    
    try:
        # Vérifier que les fichiers existent
        fichiers_requis = [
            "data/candidats.txt",
            "data/notes.txt",
            "data/rang.txt",
            "data/resultats.txt"
        ]
        
        for fichier in fichiers_requis:
            if not os.path.exists(fichier):
                print(f"❌ ERREUR : Le fichier '{fichier}' n'existe pas")
                return
        
        # Générer les visualisations
        trace_courbes()
        
        print("\n📁 Les graphiques sont sauvegardés dans le dossier 'visualisations/'")
        print("✅ ÉTAPE RÉUSSIE : Visualisations générées avec succès!")
        
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


def option_7_pipeline_complet():
    """
    Option 7 : Exécuter le pipeline complet
    """
    print("\n" + "="*70)
    print("OPTION 7 - PIPELINE COMPLET")
    print("="*70)
    
    try:
        print("\n🚀 Lancement du pipeline complet (toutes les étapes)...\n")
        
        # Étape 1 : Générer dataset
        print("1️⃣  ÉTAPE 1 : Génération du dataset...")
        generer_dataset_complet(5000)
        
        # Étape 2 : MapReduce
        print("\n2️⃣  ÉTAPE 2 : Calcul du rang (MapReduce)...")
        job_mapreduce_score_fg()
        
        # Étape 3 : Hive
        print("\n3️⃣  ÉTAPE 3 : Requêtes analytiques (Hive)...")
        executer_requetes_hive()
        
        # Étape 4 : HBase
        print("\n4️⃣  ÉTAPE 4 : Affectations (HBase)...")
        creation_resultat()
        
        # Étape 5 : Visualisations
        print("\n5️⃣  ÉTAPE 5 : Visualisations...")
        trace_courbes()
        
        print("\n" + "="*70)
        print("🎉 PIPELINE COMPLET EXÉCUTÉ AVEC SUCCÈS!")
        print("="*70)
        
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


def option_8_resumes():
    """
    Option 8 : Afficher les résumés finaux
    """
    print("\n" + "="*70)
    print("OPTION 8 - RÉSUMÉS FINAUX")
    print("="*70)
    
    try:
        # Résumé : Total candidats
        with open("data/candidats.txt", 'r', encoding='utf-8') as f:
            total_candidats = len(f.readlines()) - 1  # Exclure l'en-tête
        
        # Résumé : Top 10
        print("\n📊 RÉSUMÉ : Top 10 des meilleurs candidats")
        print("-"*70)
        
        with open("data/rang.txt", 'r', encoding='utf-8') as f:
            f.readline()  # Ignorer l'en-tête
            for i, ligne in enumerate(f):
                if i < 10:
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
                                    nom = parties_c[1] + " " + parties_c[2]
                                    print(f"  {rang:2d}. {num_cin} - {nom:30s} - FG: {fg:6.2f}")
                                    break
        
        # Résumé : Affectations
        print("\n📊 RÉSUMÉ : Statistiques d'affectation")
        print("-"*70)
        
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
        
        for filiere in sorted(affectations.keys()):
            pourcentage = (affectations[filiere] / total_candidats * 100)
            print(f"  • {filiere:15s} : {affectations[filiere]:5d} candidats ({pourcentage:5.1f}%)")
        
        print(f"\n  TOTAL : {total_candidats} candidats")
        
        print("\n✅ Résumés affichés avec succès")
        
    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")


def main():
    """
    Boucle principale du menu interactif
    """
    
    afficher_banniere()
    
    while True:
        afficher_menu()
        
        try:
            choix = input("Entrez votre choix (1-9) : ").strip()
            
            if choix == "1":
                option_1_gener_dataset()
            elif choix == "2":
                option_2_afficher_fichiers()
            elif choix == "3":
                option_3_mapreduce()
            elif choix == "4":
                option_4_hive()
            elif choix == "5":
                option_5_hbase()
            elif choix == "6":
                option_6_visualisations()
            elif choix == "7":
                option_7_pipeline_complet()
            elif choix == "8":
                option_8_resumes()
            elif choix == "9":
                print("\n" + "="*70)
                print("Au revoir! Merci d'avoir utilisé ce programme.")
                print("="*70 + "\n")
                break
            else:
                print("❌ ERREUR : Choix invalide. Veuillez entrer un nombre entre 1 et 9")
        
        except KeyboardInterrupt:
            print("\n\n❌ Programme interrompu par l'utilisateur")
            break
        except Exception as e:
            print(f"❌ ERREUR : {str(e)}")


if __name__ == "__main__":
    main()
