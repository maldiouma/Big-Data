# ============================================================================
# MODULE : REQUÊTES HIVE POUR ANALYSES
# Objectif : Effectuer les analyses statistiques sur les données
# ============================================================================

import os

# ============================================================================
# CLASSE POUR SIMULER HIVE
# (En production, on utiliserait HiveServer2 ou SparkSQL)
# ============================================================================

class HiveSimulee:
    """
    Simulation d'une base Hive pour les analyses analytiques
    Les requêtes sont exécutées sur les données en mémoire
    """
    
    def __init__(self):
        # Charger les données principales
        self.candidats = {}
        self.notes = {}
        self.rangs = {}
        self.choix = {}
        self.resultats = {}
    
    def charger_donnees(self, fichier_candidats, fichier_notes, 
                       fichier_rang, fichier_choix, fichier_resultats):
        """
        Charger toutes les données en mémoire
        """
        
        print("📥 Hive - Chargement des données dans les tables...")
        
        # Charger candidats
        with open(fichier_candidats, 'r', encoding='utf-8') as f:
            f.readline()
            for ligne in f:
                parties = ligne.strip().split()
                if len(parties) >= 4:
                    num_cin = parties[0]
                    self.candidats[num_cin] = {
                        "nom": parties[1],
                        "prenom": parties[2],
                        "filiere": parties[3]
                    }
        print(f"   ✓ Table 'candidats' : {len(self.candidats)} lignes")
        
        # Charger notes
        with open(fichier_notes, 'r', encoding='utf-8') as f:
            entete = f.readline().strip().split()
            for ligne in f:
                parties = ligne.strip().split()
                if len(parties) > 1:
                    num_cin = parties[0]
                    notes_dict = {}
                    for i, matiere in enumerate(entete[1:], 1):
                        if i < len(parties):
                            notes_dict[matiere] = float(parties[i])
                    self.notes[num_cin] = notes_dict
        print(f"   ✓ Table 'notes' : {len(self.notes)} lignes")
        
        # Charger rangs
        with open(fichier_rang, 'r', encoding='utf-8') as f:
            f.readline()
            for ligne in f:
                parties = ligne.strip().split()
                if len(parties) >= 3:
                    num_cin = parties[0]
                    self.rangs[num_cin] = {
                        "fg": float(parties[1]),
                        "rang": int(parties[2])
                    }
        print(f"   ✓ Table 'rang' : {len(self.rangs)} lignes")
        
        # Charger choix
        with open(fichier_choix, 'r', encoding='utf-8') as f:
            f.readline()
            for ligne in f:
                parties = ligne.strip().split()
                if len(parties) >= 4:
                    num_cin = parties[0]
                    self.choix[num_cin] = [parties[1], parties[2], parties[3]]
        print(f"   ✓ Table 'choix' : {len(self.choix)} lignes")
        
        # Charger résultats
        with open(fichier_resultats, 'r', encoding='utf-8') as f:
            f.readline()
            for ligne in f:
                parties = ligne.strip().split()
                if len(parties) >= 2:
                    num_cin = parties[0]
                    self.resultats[num_cin] = parties[1]
        print(f"   ✓ Table 'resultats' : {len(self.resultats)} lignes\n")
    
    # ========================================================================
    # REQUÊTE 1 : MOYENNE PAR MATIÈRE
    # ========================================================================
    
    def query_moyenne_par_matiere(self):
        """
        SELECT matiere, AVG(note) as moyenne
        FROM notes
        GROUP BY matiere
        """
        
        print("🔍 REQUÊTE HIVE #1 : Moyenne par matière")
        print("="*70)
        print("SELECT matiere, AVG(note) as moyenne FROM notes GROUP BY matiere\n")
        
        # Initialiser les statistiques
        matieres = set()
        stats_matieres = {}
        
        for num_cin, notes_candidat in self.notes.items():
            for matiere, note in notes_candidat.items():
                matieres.add(matiere)
                if matiere not in stats_matieres:
                    stats_matieres[matiere] = {"somme": 0, "count": 0}
                stats_matieres[matiere]["somme"] += note
                stats_matieres[matiere]["count"] += 1
        
        # Afficher les résultats
        print(f"{'Matière':<20} {'Moyenne':<15} {'Min':<10} {'Max':<10}")
        print("-"*70)
        
        for matiere in sorted(matieres):
            moyenne = stats_matieres[matiere]["somme"] / stats_matieres[matiere]["count"]
            
            # Calculer min et max
            notes_matiere = [self.notes[num_cin][matiere] for num_cin in self.notes 
                            if matiere in self.notes[num_cin]]
            
            print(f"{matiere:<20} {moyenne:>6.2f}<20 {min(notes_matiere):>6.2f}          {max(notes_matiere):>6.2f}")
        
        print("-"*70 + "\n")
    
    # ========================================================================
    # REQUÊTE 2 : MOYENNE DES SCORES FG
    # ========================================================================
    
    def query_moyenne_fg(self):
        """
        SELECT AVG(FG) as moyenne_fg, MIN(FG), MAX(FG), STDDEV(FG)
        FROM rang
        """
        
        print("🔍 REQUÊTE HIVE #2 : Statistiques des scores FG")
        print("="*70)
        print("SELECT AVG(FG), MIN(FG), MAX(FG), STDDEV(FG) FROM rang\n")
        
        # Récupérer tous les FG
        fgs = [self.rangs[num_cin]["fg"] for num_cin in self.rangs]
        
        # Calculer les statistiques
        moyenne_fg = sum(fgs) / len(fgs)
        min_fg = min(fgs)
        max_fg = max(fgs)
        
        # Calculer l'écart-type
        variance = sum((fg - moyenne_fg)**2 for fg in fgs) / len(fgs)
        ecart_type = variance**0.5
        
        print(f"Moyenne FG          : {moyenne_fg:>6.2f}")
        print(f"Score FG Minimum    : {min_fg:>6.2f}")
        print(f"Score FG Maximum    : {max_fg:>6.2f}")
        print(f"Écart-type          : {ecart_type:>6.2f}")
        print("-"*70 + "\n")
    
    # ========================================================================
    # REQUÊTE 3 : DISTRIBUTION DES FILIÈRES MP vs PC
    # ========================================================================
    
    def query_distribution_filieres(self):
        """
        SELECT filiere, COUNT(*) as nombre, ROUND(100.0*COUNT(*)/TOTAL(*),2) as pourcentage
        FROM candidats
        GROUP BY filiere
        """
        
        print("🔍 REQUÊTE HIVE #3 : Distribution des filières (Candidats)")
        print("="*70)
        print("SELECT filiere, COUNT(*), 100*COUNT(*)/TOTAL(*) FROM candidats GROUP BY filiere\n")
        
        # Compter les filières
        filieres = {}
        total = len(self.candidats)
        
        for num_cin, candidat in self.candidats.items():
            filiere = candidat["filiere"]
            if filiere not in filieres:
                filieres[filiere] = 0
            filieres[filiere] += 1
        
        print(f"{'Filière':<20} {'Nombre':<15} {'Pourcentage':<15}")
        print("-"*70)
        
        for filiere in sorted(filieres.keys()):
            nombre = filieres[filiere]
            pourcentage = (nombre / total * 100) if total > 0 else 0
            print(f"{filiere:<20} {nombre:<15} {pourcentage:>6.2f}%")
        
        print("-"*70 + "\n")
    
    # ========================================================================
    # REQUÊTE 4 : TOP 10 MEILLEURS SCORES
    # ========================================================================
    
    def query_top_10(self):
        """
        SELECT c.Num_CIN, c.Nom, c.Prenom, r.FG, r.Rang
        FROM candidats c
        JOIN rang r ON c.Num_CIN = r.Num_CIN
        ORDER BY r.FG DESC
        LIMIT 10
        """
        
        print("🔍 REQUÊTE HIVE #4 : TOP 10 des meilleurs scores")
        print("="*70)
        print("SELECT Num_CIN, Nom, Prenom, FG FROM rang JOIN candidats ORDER BY FG DESC LIMIT 10\n")
        
        # Trier par FG décroissant et prendre les 10 premiers
        rangs_tries = sorted(self.rangs.items(), key=lambda x: x[1]["fg"], reverse=True)[:10]
        
        print(f"{'Rang':<6} {'Num_CIN':<10} {'Nom':<15} {'Prénom':<15} {'Score FG':<10}")
        print("-"*70)
        
        for i, (num_cin, rang_data) in enumerate(rangs_tries, 1):
            if num_cin in self.candidats:
                candidat = self.candidats[num_cin]
                print(f"{rang_data['rang']:<6} {num_cin:<10} {candidat['nom']:<15} {candidat['prenom']:<15} {rang_data['fg']:>6.2f}")
        
        print("-"*70 + "\n")
    
    # ========================================================================
    # REQUÊTE 5 : STATISTIQUES DES AFFECTATIONS PAR FILIÈRE
    # ========================================================================
    
    def query_stats_affectations(self):
        """
        SELECT filiere_affectee, COUNT(*) as nombre, ROUND(100.0*COUNT(*)/TOTAL(*),2) as pourcentage
        FROM resultats
        GROUP BY filiere_affectee
        """
        
        print("🔍 REQUÊTE HIVE #5 : Répartition des affectations")
        print("="*70)
        print("SELECT filiere_affectee, COUNT(*), 100*COUNT(*)/TOTAL(*) FROM resultats GROUP BY filiere_affectee\n")
        
        # Compter les affectations
        affectations = {}
        total_affectations = len(self.resultats)
        
        for num_cin, filiere in self.resultats.items():
            if filiere not in affectations:
                affectations[filiere] = 0
            affectations[filiere] += 1
        
        print(f"{'Filière Affectée':<25} {'Nombre d\'Affectations':<20} {'Pourcentage':<15}")
        print("-"*70)
        
        for filiere in sorted(affectations.keys()):
            nombre = affectations[filiere]
            pourcentage = (nombre / total_affectations * 100) if total_affectations > 0 else 0
            print(f"{filiere:<25} {nombre:<20} {pourcentage:>6.2f}%")
        
        print("-"*70 + "\n")


# ============================================================================
# FONCTION PRINCIPALE D'EXÉCUTION DES REQUÊTES
# ============================================================================

def executer_requetes_hive(fichier_candidats="data/candidats.txt",
                          fichier_notes="data/notes.txt",
                          fichier_rang="data/rang.txt",
                          fichier_choix="data/choix.txt",
                          fichier_resultats="data/resultats.txt"):
    """
    Exécuter toutes les requêtes Hive
    """
    
    print("\n" + "="*70)
    print("ANALYSE HIVE - REQUÊTES ANALYTIQUES")
    print("="*70 + "\n")
    
    # Initialiser Hive et charger les données
    hive = HiveSimulee()
    hive.charger_donnees(fichier_candidats, fichier_notes, 
                         fichier_rang, fichier_choix, fichier_resultats)
    
    # Exécuter les requêtes
    print("="*70)
    print("EXÉCUTION DES REQUÊTES HIVE")
    print("="*70 + "\n")
    
    hive.query_moyenne_par_matiere()
    hive.query_moyenne_fg()
    hive.query_distribution_filieres()
    hive.query_top_10()
    hive.query_stats_affectations()
    
    print("="*70)
    print("✅ TOUTES LES REQUÊTES HIVE EXÉCUTÉES")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Exécuter les requêtes Hive
    executer_requetes_hive()
