# ============================================================================
# MODULE : VISUALISATIONS GRAPHIQUES
# Objectif : Tracer les graphiques statistiques avec matplotlib
# ============================================================================

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import rcParams

# Configurer matplotlib pour les caractères Unicode
rcParams['font.sans-serif'] = ['DejaVu Sans']

# ============================================================================
# CLASSE POUR GÉRER LES VISUALISATIONS
# ============================================================================

class VisualisationsDonnees:
    """
    Classe pour tracer tous les graphiques statistiques du projet
    """
    
    def __init__(self):
        self.candidats = {}
        self.notes = {}
        self.rangs = {}
        self.resultats = {}
        self.figs = []
    
    def charger_donnees(self, fichier_candidats, fichier_notes, 
                       fichier_rang, fichier_resultats):
        """
        Charger les données nécessaires pour les graphiques
        """
        
        print("📊 Chargement des données pour visualisation...")
        
        # Charger candidats
        with open(fichier_candidats, 'r', encoding='utf-8') as f:
            f.readline()
            for ligne in f:
                parties = ligne.strip().split()
                if len(parties) >= 4:
                    num_cin = parties[0]
                    self.candidats[num_cin] = {
                        "nom": parties[1],
                        "filiere": parties[3]
                    }
        
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
        
        # Charger rangs (scores FG)
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
        
        # Charger résultats
        with open(fichier_resultats, 'r', encoding='utf-8') as f:
            f.readline()
            for ligne in f:
                parties = ligne.strip().split()
                if len(parties) >= 2:
                    num_cin = parties[0]
                    self.resultats[num_cin] = parties[1]
        
        print(f"   ✓ {len(self.candidats)} candidats chargés")
        print(f"   ✓ {len(self.notes)} fichiers de notes chargés")
        print(f"   ✓ {len(self.rangs)} scores FG chargés")
        print(f"   ✓ {len(self.resultats)} résultats chargés\n")
    
    # ========================================================================
    # GRAPHIQUE 1 : HISTOGRAMMES DES NOTES PAR MATIÈRE
    # ========================================================================
    
    def tracer_histogrammes_matieres(self):
        """
        Tracer un histogramme pour chaque matière montrant
        la distribution des notes des candidats
        """
        
        print("📈 Graphique 1 : Histogrammes des notes par matière...")
        
        # Récupérer toutes les matières
        matieres = set()
        for num_cin in self.notes:
            matieres.update(self.notes[num_cin].keys())
        matieres = sorted(matieres)
        
        # Créer une figure avec plusieurs sous-graphiques
        fig, axes = plt.subplots(2, 4, figsize=(16, 10))
        fig.suptitle('Distribution des Notes par Matière', fontsize=16, fontweight='bold')
        
        axes = axes.flatten()
        
        # Tracer un histogramme pour chaque matière
        for idx, matiere in enumerate(matieres[:8]):
            # Récupérer les notes pour cette matière
            notes_matiere = []
            for num_cin in self.notes:
                if matiere in self.notes[num_cin]:
                    notes_matiere.append(self.notes[num_cin][matiere])
            
            # Tracer l'histogramme
            axes[idx].hist(notes_matiere, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
            axes[idx].set_title(f'{matiere}', fontweight='bold')
            axes[idx].set_xlabel('Note')
            axes[idx].set_ylabel('Nombre de candidats')
            axes[idx].grid(axis='y', alpha=0.3)
            
            # Ajouter des statistiques
            moyenne = np.mean(notes_matiere)
            axes[idx].axvline(moyenne, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {moyenne:.2f}')
            axes[idx].legend()
        
        plt.tight_layout()
        self.figs.append(("Histogrammes_Matieres", fig))
        print("   ✓ Graphique sauvegardé")
    
    # ========================================================================
    # GRAPHIQUE 2 : DISTRIBUTION MP vs PC
    # ========================================================================
    
    def tracer_distribution_filieres(self):
        """
        Tracer un graphique camembert (pie chart) montrant
        la répartition MP vs PC
        """
        
        print("📊 Graphique 2 : Distribution des filières (MP vs PC)...")
        
        # Compter MP et PC
        distribution = {"MP": 0, "PC": 0}
        for num_cin in self.candidats:
            filiere = self.candidats[num_cin]["filiere"]
            if filiere in distribution:
                distribution[filiere] += 1
        
        # Créer le graphique camembert
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = list(distribution.keys())
        sizes = [distribution[f] for f in labels]
        colors = ['#ff9999', '#66b3ff']
        explode = (0.05, 0.05)
        
        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                           colors=colors, startangle=90, textprops={'fontsize': 14})
        
        # Styliser les textes
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)
        
        ax.set_title('Distribution des Filières - Candidats\n(MP vs PC)', fontsize=14, fontweight='bold')
        
        # Ajouter une légende avec les counts
        legend_labels = [f'{f}: {distribution[f]} candidats' for f in labels]
        ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        self.figs.append(("Distribution_Filieres", fig))
        print("   ✓ Graphique sauvegardé")
    
    # ========================================================================
    # GRAPHIQUE 3 : COURBE DES MOYENNES PAR MATIÈRE
    # ========================================================================
    
    def tracer_courbe_moyennes(self):
        """
        Tracer une courbe ligne montrant la moyenne de chaque matière
        et l'écart-type
        """
        
        print("📈 Graphique 3 : Courbe des moyennes par matière...")
        
        # Récupérer toutes les matières
        matieres = set()
        for num_cin in self.notes:
            matieres.update(self.notes[num_cin].keys())
        matieres = sorted(matieres)
        
        # Calculer les moyennes et écarts-types
        moyennes = []
        ecarts_types = []
        
        for matiere in matieres:
            notes_matiere = []
            for num_cin in self.notes:
                if matiere in self.notes[num_cin]:
                    notes_matiere.append(self.notes[num_cin][matiere])
            
            if notes_matiere:
                moyennes.append(np.mean(notes_matiere))
                ecarts_types.append(np.std(notes_matiere))
            else:
                moyennes.append(0)
                ecarts_types.append(0)
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(12, 7))
        
        x = np.arange(len(matieres))
        
        # Tracer la ligne des moyennes
        ax.plot(x, moyennes, marker='o', linewidth=2.5, markersize=8, 
                color='darkblue', label='Moyenne')
        
        # Ajouter la zone d'écart-type
        ax.fill_between(x, 
                        np.array(moyennes) - np.array(ecarts_types),
                        np.array(moyennes) + np.array(ecarts_types),
                        alpha=0.2, color='lightblue', label='Ecart-type')
        
        # Ajouter une ligne horizontale à 10 (moyen)
        ax.axhline(y=10, color='red', linestyle='--', linewidth=2, label='Note moyenne (10)')
        
        # Configurer les axes
        ax.set_xlabel('Matière', fontweight='bold', fontsize=12)
        ax.set_ylabel('Moyenne des notes', fontweight='bold', fontsize=12)
        ax.set_title('Evolution des Moyennes par Matière', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(matieres, rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')
        ax.set_ylim(0, 20)
        
        plt.tight_layout()
        self.figs.append(("Courbe_Moyennes", fig))
        print("   ✓ Graphique sauvegardé")
    
    # ========================================================================
    # GRAPHIQUE 4 : HISTOGRAMME DES SCORES FG
    # ========================================================================
    
    def tracer_histogramme_fg(self):
        """
        Tracer un histogramme montrant la distribution des scores FG
        """
        
        print("📈 Graphique 4 : Histogramme des scores FG...")
        
        # Récupérer tous les scores FG
        scores_fg = [self.rangs[num_cin]['fg'] for num_cin in self.rangs]
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Tracer l'histogramme
        n, bins, patches = ax.hist(scores_fg, bins=50, color='forestgreen', edgecolor='black', alpha=0.7)
        
        # Ajouter la moyenne
        moyenne_fg = np.mean(scores_fg)
        ax.axvline(moyenne_fg, color='red', linestyle='--', linewidth=2.5, label=f'Moyenne: {moyenne_fg:.2f}')
        
        # Ajouter la médiane
        mediane_fg = np.median(scores_fg)
        ax.axvline(mediane_fg, color='orange', linestyle='--', linewidth=2.5, label=f'Médiane: {mediane_fg:.2f}')
        
        # Configurer le graphique
        ax.set_xlabel('Score FG', fontweight='bold', fontsize=12)
        ax.set_ylabel('Nombre de candidats', fontweight='bold', fontsize=12)
        ax.set_title('Distribution des Scores FG\n(Tous les candidats)', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        ax.legend(fontsize=11)
        
        # Ajouter des statistiques texte
        stats_text = f'Après analyse de {len(scores_fg)} candidats:\n'
        stats_text += f'Min: {min(scores_fg):.2f}\n'
        stats_text += f'Max: {max(scores_fg):.2f}\n'
        stats_text += f'Ecart-type: {np.std(scores_fg):.2f}'
        
        ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, 
                fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        self.figs.append(("Histogramme_FG", fig))
        print("   ✓ Graphique sauvegardé")
    
    # ========================================================================
    # GRAPHIQUE BONUS : RÉPARTITION DES AFFECTATIONS
    # ========================================================================
    
    def tracer_repartition_affectations(self):
        """
        Tracer un graphique montrant le nombre d'affectations par filière
        """
        
        print("📊 Graphique 5 : Répartition des affectations par filière...")
        
        # Compter les affectations par filière
        affectations = {}
        for num_cin, filiere in self.resultats.items():
            if filiere not in affectations:
                affectations[filiere] = 0
            affectations[filiere] += 1
        
        # Créer le graphique en barres
        fig, ax = plt.subplots(figsize=(12, 7))
        
        filieres = sorted(affectations.keys())
        nombres = [affectations[f] for f in filieres]
        
        # Couleurs différentes pour AUCUNE vs autres
        colors = ['#ff6b6b' if f == 'AUCUNE' else '#51cf66' for f in filieres]
        
        bars = ax.bar(filieres, nombres, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
        
        # Ajouter les valeurs sur les barres
        for bar, nombre in zip(bars, nombres):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(nombre)}',
                    ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Configurer le graphique
        ax.set_xlabel('Filière', fontweight='bold', fontsize=12)
        ax.set_ylabel('Nombre d\'affectations', fontweight='bold', fontsize=12)
        ax.set_title('Répartition des Affectations par Filière', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Rotation des labels si nécessaire
        if len(filieres) > 5:
            plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        self.figs.append(("Repartition_Affectations", fig))
        print("   ✓ Graphique sauvegardé")
    
    # ========================================================================
    # SAUVEGARDE ET AFFICHAGE
    # ========================================================================
    
    def sauvegarder_graphiques(self, dossier_output="visualisations"):
        """
        Sauvegarder tous les graphiques dans des fichiers PNG
        """
        
        print(f"\n🖼️  Sauvegarde des graphiques dans '{dossier_output}'...\n")
        
        import os
        os.makedirs(dossier_output, exist_ok=True)
        
        for nom, fig in self.figs:
            chemin = os.path.join(dossier_output, f"{nom}.png")
            fig.savefig(chemin, dpi=300, bbox_inches='tight')
            print(f"   ✓ {nom}.png sauvegardé")
        
        print()
    
    def afficher_graphiques(self):
        """
        Afficher tous les graphiques
        """
        plt.show()


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def trace_courbes(fichier_candidats="data/candidats.txt",
                 fichier_notes="data/notes.txt",
                 fichier_rang="data/rang.txt",
                 fichier_resultats="data/resultats.txt"):
    """
    Tracer tous les graphiques statistiques
    """
    
    print("\n" + "="*70)
    print("VISUALISATIONS STATISTIQUES")
    print("="*70 + "\n")
    
    # Initialiser les visualisations
    viz = VisualisationsDonnees()
    viz.charger_donnees(fichier_candidats, fichier_notes, 
                        fichier_rang, fichier_resultats)
    
    # Tracer tous les graphiques
    print("="*70)
    print("CRÉATION DES GRAPHIQUES")
    print("="*70 + "\n")
    
    viz.tracer_histogrammes_matieres()
    viz.tracer_distribution_filieres()
    viz.tracer_courbe_moyennes()
    viz.tracer_histogramme_fg()
    viz.tracer_repartition_affectations()
    
    # Sauvegarder les graphiques
    viz.sauvegarder_graphiques()
    
    print("="*70)
    print("✅ TOUS LES GRAPHIQUES GÉNÉRÉS")
    print("="*70)
    
    # Afficher les graphiques (optionnel)
    # viz.afficher_graphiques()


if __name__ == "__main__":
    # Tracer tous les graphiques
    trace_courbes()
