# ============================================================================
# MODULE : MAPREDUCE POUR CALCUL DU SCORE FG ET RANG
# Objectif : Lire candidats + notes, calculer FG, trier et générer rang.txt
# ============================================================================

import os

# ============================================================================
# MAPPER : Lire et fusionner les données
# ============================================================================

def mapper_fusion(fichier_candidats="data/candidats.txt", 
                  fichier_notes="data/notes.txt"):
    """
    PHASE MAPPER : Fusionne les données candidats et notes
    et émet (Num_CIN, données_fusionnees)
    
    Processus :
    1. Charger les candidats en mémoire avec leur Num_CIN
    2. Pour chaque ligne de notes, chercher le candidat correspondant
    3. Émettre (Num_CIN, notes_ET_donnees_candidat)
    """
    
    # Étape 1 : Charger les candidats
    print("📖 MAPPER : Chargement des candidats...")
    candidats_dict = {}
    
    with open(fichier_candidats, 'r', encoding='utf-8') as f:
        # Ignorer l'en-tête
        f.readline()
        
        for ligne in f:
            parties = ligne.strip().split()
            if len(parties) >= 4:
                num_cin = parties[0]
                nom = parties[1]
                prenom = parties[2]
                filiere = parties[3]
                
                candidats_dict[num_cin] = {
                    "nom": nom,
                    "prenom": prenom,
                    "filiere": filiere
                }
    
    print(f"   ✓ {len(candidats_dict)} candidats chargés")
    
    # Étape 2 : Fusionner avec les notes
    print("📖 MAPPER : Fusion avec les notes...")
    donnees_fusionnees = {}
    
    with open(fichier_notes, 'r', encoding='utf-8') as f:
        # Lire l'en-tête pour connaître l'ordre des matières
        entete = f.readline().strip().split()
        
        for ligne in f:
            parties = ligne.strip().split()
            if len(parties) > 1:
                num_cin = parties[0]
                
                # Extraire les notes
                notes = {}
                for i, matiere in enumerate(entete[1:], 1):
                    if i < len(parties):
                        notes[matiere] = float(parties[i])
                
                # Fusionner avec les données du candidat
                if num_cin in candidats_dict:
                    donnees_fusionnees[num_cin] = {
                        **candidats_dict[num_cin],
                        "notes": notes
                    }
    
    print(f"   ✓ {len(donnees_fusionnees)} candidats fusionnés")
    
    return donnees_fusionnees


# ============================================================================
# REDUCER : Calculer le score FG
# ============================================================================

def calculer_score_fg(notes):
    """
    FORMULE DU SCORE FG (Score Global pondéré) :
    FG = Analyse*8 + Algèbre*6 + Physique*8 + Chimie*6 + 
         Informatique*6 + STA*4 + Français*3 + Anglais*3
    
    Cette formule privilégie les matières scientifiques.
    """
    
    # Poids de chaque matière
    poids = {
        "Analyse": 8,
        "Algèbre": 6,
        "Physique": 8,
        "Chimie": 6,
        "Informatique": 6,
        "STA": 4,
        "Français": 3,
        "Anglais": 3
    }
    
    # Calcul du score
    fg = 0
    for matiere, poids_matiere in poids.items():
        if matiere in notes:
            fg += notes[matiere] * poids_matiere
    
    return round(fg, 2)


def reducer_calcul_rang(donnees_fusionnees):
    """
    PHASE REDUCER : Calculer le score FG pour chaque candidat
    et générer les données de rang
    
    Processus :
    1. Pour chaque candidat, calculer son score FG
    2. Trier les candidats par score FG décroissant
    3. Assigner les rangs
    4. Retourner la liste triée avec les rangs
    """
    
    print("🔄 REDUCER : Calcul des scores FG...")
    
    # Étape 1 : Calculer les scores FG
    resultats = []
    for num_cin, donnees in donnees_fusionnees.items():
        fg = calculer_score_fg(donnees["notes"])
        resultats.append({
            "Num_CIN": num_cin,
            "FG": fg,
            "nom": donnees["nom"],
            "prenom": donnees["prenom"],
            "filiere": donnees["filiere"]
        })
    
    print(f"   ✓ {len(resultats)} scores FG calculés")
    
    # Étape 2 : Trier par FG décroissant
    print("🔄 REDUCER : Tri par score FG décroissant...")
    resultats_tries = sorted(resultats, key=lambda x: x["FG"], reverse=True)
    
    # Étape 3 : Assigner les rangs
    print("🔄 REDUCER : Attribution des rangs...")
    for i, resultat in enumerate(resultats_tries, 1):
        resultat["Rang"] = i
    
    print(f"   ✓ {len(resultats_tries)} candidats classés")
    
    return resultats_tries


# ============================================================================
# JOB MAPREDUCE COMPLET
# ============================================================================

def job_mapreduce_score_fg(fichier_candidats="data/candidats.txt",
                           fichier_notes="data/notes.txt",
                           fichier_rang="data/rang.txt"):
    """
    JOB MAPREDUCE COMPLET :
    1. MAPPER : Fusionner candidats + notes
    2. REDUCER : Calculer FG et assigner les rangs
    3. OUTPUT : Générer le fichier rang.txt
    """
    
    print("\n" + "="*70)
    print("JOB MAPREDUCE : CALCUL DU SCORE FG ET RANG")
    print("="*70)
    
    # MAPPER
    donnees_fusionnees = mapper_fusion(fichier_candidats, fichier_notes)
    
    # REDUCER
    print()
    resultats_tries = reducer_calcul_rang(donnees_fusionnees)
    
    # OUTPUT : Sauvegarder le fichier rang.txt
    print("\n📝 Génération du fichier rang.txt...")
    os.makedirs(os.path.dirname(fichier_rang), exist_ok=True)
    
    with open(fichier_rang, 'w', encoding='utf-8') as f:
        # En-tête
        f.write("Num_CIN FG Rang\n")
        
        # Données triées par rang
        for resultat in resultats_tries:
            ligne = f"{resultat['Num_CIN']} {resultat['FG']} {resultat['Rang']}\n"
            f.write(ligne)
    
    print(f"   ✓ Fichier {fichier_rang} généré avec {len(resultats_tries)} candidats")
    
    print("\n" + "="*70)
    print("✅ JOB MAPREDUCE TERMINÉ")
    print("="*70 + "\n")
    
    # Afficher les statistiques
    print("📊 STATISTIQUES DES RANGS :")
    print(f"   • Total candidats : {len(resultats_tries)}")
    print(f"   • Score FG minimal : {resultats_tries[-1]['FG']:.2f}")
    print(f"   • Score FG maximal : {resultats_tries[0]['FG']:.2f}")
    print(f"   • Score FG moyen : {sum(r['FG'] for r in resultats_tries) / len(resultats_tries):.2f}")
    print()
    
    # Afficher les TOP 10
    print("🏆 TOP 10 DES MEILLEURS SCORES :")
    for i, resultat in enumerate(resultats_tries[:10], 1):
        print(f"   {i:2d}. {resultat['Num_CIN']} - {resultat['nom']:12s} {resultat['prenom']:12s} - FG: {resultat['FG']:.2f}")
    print()
    
    return resultats_tries


if __name__ == "__main__":
    # Exécuter le job MapReduce
    job_mapreduce_score_fg()
