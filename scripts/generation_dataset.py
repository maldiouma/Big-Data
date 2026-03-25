# ============================================================================
# MODULE : GÉNÉRATION DU DATASET
# Objectif : Créer un dataset massif pour le système d'orientation nationale
# ============================================================================

import random
import json
import os
from datetime import datetime

# ============================================================================
# 1. GÉNÉRATION DES CANDIDATS
# ============================================================================

def creation_liste_candidats(nombre_candidats=5000):
    """
    Génère une liste massive de candidats avec leurs informations
    
    Paramètres :
        nombre_candidats (int) : Nombre de candidats à générer (défaut: 5000)
    
    Retour :
        list : Liste des candidats avec [Num_CIN, Nom, Prenom, Filiere]
    """
    
    # Listes de données pour générer des candidats réalistes
    noms = [
        "BENNANI", "TAHA", "MOROCCO", "HASSAN", "FATIMA", "AMIRA", 
        "KARIM", "SAFIYA", "YOUSSEF", "LEILA", "AHMED", "ZAINAB",
        "OMAR", "NOOR", "KHALID", "HANA", "IBRAHIM", "YASMIN"
    ] * 300  # Répéter pour avoir assez de variété
    
    prenoms = [
        "Ali", "Mohammed", "Fatima", "Amina", "Sara", "Yasmine",
        "Hassan", "Ibrahim", "Leila", "Noor", "Karim", "Zahra",
        "Rabab", "Samira", "Hicham", "Souad", "Tariq", "Nadia"
    ] * 300
    
    # Filières disponibles
    filieres = ["MP", "PC"]
    
    # Générer les candidats
    candidats = []
    for i in range(1, nombre_candidats + 1):
        # Numéro CIN unique
        num_cin = f"{i:06d}"
        
        # Sélectionner nom et prénom aléatoirement
        nom = random.choice(noms)
        prenom = random.choice(prenoms)
        
        # Sélectionner filière aléatoirement
        filiere = random.choice(filieres)
        
        # Ajouter le candidat à la liste
        candidats.append({
            "Num_CIN": num_cin,
            "Nom": nom,
            "Prenom": prenom,
            "Filiere": filiere
        })
    
    return candidats


def sauvegarder_candidats(candidats, chemin_fichier="data/candidats.txt"):
    """
    Sauvegarde la liste des candidats dans un fichier texte
    Format : Num_CIN Nom Prenom Filiere
    """
    
    # Créer le répertoire s'il n'existe pas
    os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)
    
    # Écrire dans le fichier
    with open(chemin_fichier, 'w', encoding='utf-8') as f:
        # En-tête
        f.write("Num_CIN Nom Prenom Filiere\n")
        
        # Données
        for candidat in candidats:
            ligne = f"{candidat['Num_CIN']} {candidat['Nom']} {candidat['Prenom']} {candidat['Filiere']}\n"
            f.write(ligne)
    
    print(f"✓ {len(candidats)} candidats sauvegardés dans {chemin_fichier}")
    
    return chemin_fichier


# ============================================================================
# 2. GÉNÉRATION DES NOTES
# ============================================================================

def creation_notes(candidats):
    """
    Génère les notes pour chaque candidat (8 matières)
    
    Paramètres :
        candidats (list) : Liste des candidats générés
    
    Retour :
        list : Liste des notes [Num_CIN, Analyse, Algèbre, Physique, ...]
    """
    
    # Matières évaluées
    matieres = ["Analyse", "Algèbre", "Physique", "Chimie", "Informatique", "STA", "Français", "Anglais"]
    
    # Générer les notes
    notes = []
    for candidat in candidats:
        num_cin = candidat["Num_CIN"]
        
        # Générer des notes réalistes (8-18 en majorité, quelques valeurs extrêmes)
        notes_candidat = {
            "Num_CIN": num_cin,
        }
        
        for matiere in matieres:
            # Générer une note entre 0 et 20 avec distribution réaliste
            # 70% des notes entre 8 et 18
            if random.random() < 0.7:
                note = random.uniform(8, 18)
            else:
                note = random.uniform(0, 20)
            
            notes_candidat[matiere] = round(note, 2)
        
        notes.append(notes_candidat)
    
    return notes


def sauvegarder_notes(notes, chemin_fichier="data/notes.txt"):
    """
    Sauvegarde les notes dans un fichier texte
    Format : Num_CIN Analyse Algèbre Physique Chimie Informatique STA Français Anglais
    """
    
    os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)
    
    matieres = ["Analyse", "Algèbre", "Physique", "Chimie", "Informatique", "STA", "Français", "Anglais"]
    
    with open(chemin_fichier, 'w', encoding='utf-8') as f:
        # En-tête
        f.write("Num_CIN " + " ".join(matieres) + "\n")
        
        # Données
        for note_dict in notes:
            ligne = note_dict["Num_CIN"]
            for matiere in matieres:
                ligne += f" {note_dict[matiere]}"
            f.write(ligne + "\n")
    
    print(f"✓ Notes de {len(notes)} candidats sauvegardées dans {chemin_fichier}")
    
    return chemin_fichier


# ============================================================================
# 3. GÉNÉRATION DES CHOIX (3 choix par candidat)
# ============================================================================

def creation_choix(candidats, codes_filieres=None):
    """
    Génère les 3 choix de filière pour chaque candidat
    
    Paramètres :
        candidats (list) : Liste des candidats
        codes_filieres (list) : Codes des filières disponibles
    
    Retour :
        dict : Dictionnaire {Num_CIN: [Choix1, Choix2, Choix3]}
    """
    
    # Codes des filières disponibles
    if codes_filieres is None:
        codes_filieres = ["E101", "E205", "E301", "E402", "E503"]
    
    # Générer les choix
    choix = {}
    for candidat in candidats:
        num_cin = candidat["Num_CIN"]
        
        # Sélectionner 3 choix différents de manière aléatoire
        trois_choix = random.sample(codes_filieres, min(3, len(codes_filieres)))
        
        choix[num_cin] = trois_choix
    
    return choix


def sauvegarder_choix(choix, chemin_fichier="data/choix.txt"):
    """
    Sauvegarde les choix dans un fichier texte
    Format : Num_CIN Choix1 Choix2 Choix3
    """
    
    os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)
    
    with open(chemin_fichier, 'w', encoding='utf-8') as f:
        # En-tête
        f.write("Num_CIN Choix1 Choix2 Choix3\n")
        
        # Données
        for num_cin, choix_list in choix.items():
            ligne = f"{num_cin}"
            for c in choix_list:
                ligne += f" {c}"
            f.write(ligne + "\n")
    
    print(f"✓ Choix de {len(choix)} candidats sauvegardés dans {chemin_fichier}")
    
    return chemin_fichier


# ============================================================================
# 4. CRÉATION DU DICTIONNAIRE DES FILIÈRES
# ============================================================================

def creation_filiere():
    """
    Crée le dictionnaire des filières avec leurs codes écoles et capacités
    
    Retour :
        dict : Dictionnaire {code_filiere: [code_ecole, capacité]}
    """
    
    # Dictionnaire des filières
    # Format : "CODE_FILIERE" : ["CODE_ECOLE", CAPACITÉ]
    filieres = {
        "E101": ["École d'Ingénierie MP", 200],
        "E205": ["École d'Ingénierie PC", 150],
        "E301": ["École Polytechnique", 100],
        "E402": ["Institut Technologique", 180],
        "E503": ["École Managériale", 250]
    }
    
    return filieres


def sauvegarder_filieres(filieres, chemin_fichier="data/filiere.json"):
    """
    Sauvegarde le dictionnaire des filières en JSON
    """
    
    os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)
    
    with open(chemin_fichier, 'w', encoding='utf-8') as f:
        json.dump(filieres, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Dictionnaire des filières sauvegardé dans {chemin_fichier}")
    
    return chemin_fichier


# ============================================================================
# FONCTION PRINCIPALE DE GÉNÉRATION
# ============================================================================

def generer_dataset_complet(nombre_candidats=5000):
    """
    Génère le dataset complet en appelant toutes les sous-fonctions
    """
    
    print("\n" + "="*70)
    print("GÉNÉRATION DU DATASET COMPLET")
    print("="*70)
    
    # 1. Générer et sauvegarder les candidats
    print("\n1️⃣  Génération des candidats...")
    candidats = creation_liste_candidats(nombre_candidats)
    sauvegarder_candidats(candidats)
    
    # 2. Générer et sauvegarder les notes
    print("\n2️⃣  Génération des notes...")
    notes = creation_notes(candidats)
    sauvegarder_notes(notes)
    
    # 3. Générer et sauvegarder les filières
    print("\n3️⃣  Création du dictionnaire des filières...")
    filieres = creation_filiere()
    sauvegarder_filieres(filieres)
    
    # 4. Générer et sauvegarder les choix
    print("\n4️⃣  Génération des choix de filière...")
    codes_filieres = list(filieres.keys())
    choix = creation_choix(candidats, codes_filieres)
    sauvegarder_choix(choix)
    
    print("\n" + "="*70)
    print(f"✅ DATASET COMPLET GÉNÉRÉ ({nombre_candidats} candidats)")
    print("="*70 + "\n")
    
    # Afficher des statistiques
    print("📊 STATISTIQUES DU DATASET :")
    print(f"   • Nombre de candidats : {len(candidats)}")
    print(f"   • Filière MP : {sum(1 for c in candidats if c['Filiere'] == 'MP')}")
    print(f"   • Filière PC : {sum(1 for c in candidats if c['Filiere'] == 'PC')}")
    print(f"   • Nombre de filières : {len(filieres)}")
    print()


if __name__ == "__main__":
    # Générer le dataset complet avec 5000 candidats
    generer_dataset_complet(5000)
