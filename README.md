# 🎓 PROJET BIG DATA - SYSTÈME D'ORIENTATION NATIONALE

## 📝 Vue d'ensemble

Ce projet implémente une **solution Big Data complète** pour gérer un système d'orientation nationale utilisant les technologies Hadoop, MapReduce, Hive et HBase.

- **Objectif** : Générer un dataset massif, calculer les scores, affecter les candidats aux filières selon le système de mérite
- **Volume** : Minimum 5000 candidats avec 8 matières chacun
- **Technologies** : Python, Hadoop, MapReduce, Hive, HBase, Matplotlib

---

## 🏗️ STRUCTURE DU PROJET

```
Projet-Big-Data/
├── main.py                          # ✅ MENU PRINCIPAL INTERACTIF
│
├── scripts/                         # Modules Python
│   ├── generation_dataset.py       # Génération du dataset
│   ├── mapreduce_job.py            # Job MapReduce (scores FG et rangs)
│   ├── hive_queries.py             # Requêtes Hive analytiques
│   ├── hbase_operations.py         # Simulation HBase + affectations
│   └── visualisations.py           # Graphiques (matplotlib)
│
├── data/                            # Fichiers de données générés
│   ├── candidats.txt               # Liste des candidats
│   ├── notes.txt                   # Notes par matière
│   ├── choix.txt                   # 3 choix par candidat
│   ├── filiere.json                # Dictionnaire des filières
│   ├── rang.txt                    # Classement (MapReduce output)
│   └── resultats.txt               # Affectations finales (HBase output)
│
├── visualisations/                  # Graphiques PNG (générés)
│   ├── Histogrammes_Matieres.png
│   ├── Distribution_Filieres.png
│   ├── Courbe_Moyennes.png
│   ├── Histogramme_FG.png
│   └── Repartition_Affectations.png
│
└── rapport/                         # Documents/rapports
    └── rapport.md
```

---

## 🚀 DÉMARRAGE RAPIDE

### Option 1 : Pipeline Complet (Recommandé)

```bash
# Lancer le menu interactif
python main.py

# Choisir l'option 7 pour exécuter le pipeline complet
# Cela exécutera automatiquement toutes les étapes
```

### Option 2 : Étape par étape

```bash
python main.py

# Puis utiliser le menu:
# 1️⃣  Générer dataset
# 2️⃣  Afficher fichiers
# 3️⃣  MapReduce
# 4️⃣  Hive
# 5️⃣  HBase
# 6️⃣  Visualisations
# 9️⃣  Quitter
```

### Option 3 : Exécution directe des modules

```bash
# Générer le dataset
python scripts/generation_dataset.py

# Exécuter MapReduce
python scripts/mapreduce_job.py

# Exécuter Hive
python scripts/hive_queries.py

# Exécuter HBase + affectations
python scripts/hbase_operations.py

# Générer les graphiques
python scripts/visualisations.py
```

---

## 📊 PHASE 1 : GÉNÉRATION DU DATASET

### Fichiers générés :

#### 1️⃣ **candidats.txt**
Format : `Num_CIN Nom Prenom Filiere`

```
Num_CIN Nom Prenom Filiere
000001 BENNANI Ali MP
000002 TAHA Mohammed PC
000003 MOROCCO Fatima MP
...
```

#### 2️⃣ **notes.txt**
Format : `Num_CIN Analyse Algèbre Physique Chimie Informatique STA Français Anglais`

```
Num_CIN Analyse Algèbre Physique Chimie Informatique STA Français Anglais
000001 14.5 13.2 15.8 12.3 16.1 14.7 11.2 9.8
000002 12.1 14.3 13.9 15.6 12.8 13.4 10.1 11.3
...
```

#### 3️⃣ **choix.txt**
Format : `Num_CIN Choix1 Choix2 Choix3`

```
Num_CIN Choix1 Choix2 Choix3
000001 E101 E205 E301
000002 E402 E503 E101
...
```

#### 4️⃣ **filiere.json**
Dictionnaire des filières avec leurs codes et capacités

```json
{
  "E101": ["École d'Ingénierie MP", 200],
  "E205": ["École d'Ingénierie PC", 150],
  "E301": ["École Polytechnique", 100],
  "E402": ["Institut Technologique", 180],
  "E503": ["École Managériale", 250]
}
```

---

## 🗺️ PHASE 2 : STOCKAGE HDFS

**Commandes HDFS simulées** (en production) :

```bash
# Créer le répertoire /orientation
hdfs dfs -mkdir -p /orientation

# Importer les fichiers
hdfs dfs -put data/candidats.txt /orientation/
hdfs dfs -put data/notes.txt /orientation/
hdfs dfs -put data/choix.txt /orientation/
hdfs dfs -put data/filiere.json /orientation/

# Vérifier l'import
hdfs dfs -ls /orientation/
```

---

## 🔧 PHASE 3 : MAPREDUCE - CALCUL DU SCORE FG

### Formule du Score FG :

```
FG = Analyse*8 + Algèbre*6 + Physique*8 + Chimie*6 
     + Informatique*6 + STA*4 + Français*3 + Anglais*3
```

### Processus :

1. **MAPPER** : Fusionne `candidats.txt` + `notes.txt`
2. **REDUCER** : Calcule le FG, trie par score décroissant, assigne les rangs
3. **OUTPUT** : Génère `rang.txt`

### Fichier de sortie : **rang.txt**
Format : `Num_CIN FG Rang`

```
Num_CIN FG Rang
000042 298.5 1
000157 295.3 2
000089 292.1 3
...
```

---

## 📊 PHASE 4 : HIVE - ANALYSES ANALYTIQUES

### Requêtes exécutées :

#### 1. Moyenne par matière
```sql
SELECT matiere, AVG(note) FROM notes GROUP BY matiere
```

#### 2. Statistiques FG
```sql
SELECT AVG(FG), MIN(FG), MAX(FG), STDDEV(FG) FROM rang
```

#### 3. Distribution MP vs PC
```sql
SELECT filiere, COUNT(*), 100*COUNT(*)/TOTAL(*) FROM candidats GROUP BY filiere
```

#### 4. Top 10 meilleurs scores
```sql
SELECT * FROM rang ORDER BY FG DESC LIMIT 10
```

#### 5. Répartition des affectations
```sql
SELECT filiere_affectee, COUNT(*) FROM resultats GROUP BY filiere_affectee
```

---

## 🔶 PHASE 5 : HBASE - AFFECTATIONS

### Tables HBase :

#### Table 1 : FILIERE
```
Clé : code_filiere
Colonne : {capacite, places_restantes, nom_ecole}

E101 | capacite=200 | places_restantes=145 | nom=École d'Ingénierie MP
E205 | capacite=150 | places_restantes=89  | nom=École d'Ingénierie PC
...
```

#### Table 2 : CHOIX
```
Clé : Num_CIN
Colonne : {choix1, choix2, choix3}

000001 | [E101, E205, E301]
000002 | [E402, E503, E101]
...
```

#### Table 3 : RESULTATS
```
Clé : Num_CIN
Colonne : {filiere_affectee, rang}

000042 | filiere_affectee=E101 | rang=1
000157 | filiere_affectee=E205 | rang=2
...
```

### Algorithme d'affectation :

```
Pour chaque candidat (par ordre de rang décroissant) :
    Si choix1 disponible → Affecter à choix1
    Sinon si choix2 disponible → Affecter à choix2
    Sinon si choix3 disponible → Affecter à choix3
    Sinon → Pas d'affectation (AUCUNE)
    
    Décrémenter la capacité dans HBase
```

### Fichier de sortie : **resultats.txt**
Format : `Num_CIN Filiere_Affectee`

```
Num_CIN Filiere_Affectee
000042 E101
000157 E205
000089 E301
...
005000 AUCUNE
```

---

## 📈 PHASE 6 : VISUALISATIONS

Les graphiques générés dans `visualisations/` :

### 1. **Histogrammes_Matieres.png**
Distribution des notes pour chaque matière (8 graphiques)

### 2. **Distribution_Filieres.png**
Répartition MP vs PC (camembert)

### 3. **Courbe_Moyennes.png**
Courbe des moyennes par matière avec écart-type

### 4. **Histogramme_FG.png**
Distribution des scores FG de tous les candidats

### 5. **Repartition_Affectations.png**
Nombre d'affectations par filière (barres)

---

## 💡 POINTS CLÉS DE L'IMPLÉMENTATION

### 1. **Mérité respecté**
- Les candidats avec les meilleures notes sont testés en premier
- Chacun peut choisir sa filière mais selon le rang
- Pas de discrimination

### 2. **Capacités respectées**
- Chaque filière a une capacité maximum
- Le système décrémente la capacité à chaque affectation
- Les derniers candidats peuvent ne pas être affectés

### 3. **Scalabilité Big Data**
- Datasets massifs (5000+ candidats)
- Utilisation de streaming et agrégations
- Traitements parallélisables (MapReduce)

### 4. **Modularité**
- Chaque module est indépendant
- Peuvent être exécutés séparement ou ensemble
- Facile à tester et maintenir

---

## 📋 GRILLE D'ÉVALUATION

| Criterion | Points | Status |
|-----------|--------|--------|
| Génération dataset | 4 | ✅ |
| HDFS | 2 | ✅ |
| MapReduce | 4 | ✅ |
| Hive | 3 | ✅ |
| HBase | 3 | ✅ |
| Visualisation | 2 | ✅ |
| Menu principal | 1 | ✅ |
| Rapport | 1 | ⏳ |
| **TOTAL** | **20** | **16/20** |

---

## 🔍 EXEMPLES DE COMMANDES

### Tester la génération du dataset
```bash
python -c "from scripts.generation_dataset import *; generer_dataset_complet(100)"
```

### Tester MapReduce
```bash
python -c "from scripts.mapreduce_job import *; job_mapreduce_score_fg()"
```

### Tester Hive
```bash
python -c "from scripts.hive_queries import *; executer_requetes_hive()"
```

### Tester HBase
```bash
python -c "from scripts.hbase_operations import *; creation_resultat()"
```

### Générer les graphiques
```bash
python -c "from scripts.visualisations import *; trace_courbes()"
```

---

## ⚠️ PRÉREQUIS

```
Python 3.8+
matplotlib >= 3.5.0
numpy >= 1.20.0
```

**Installation des dépendances :**
```bash
pip install matplotlib numpy
```

---

## 📝 COMMENTAIRES INCLUS

Tous les fichiers Python incluent :
- ✅ Commentaires en français détaillés
- ✅ Docstrings pour chaque fonction
- ✅ Explications du flux de données
- ✅ Notes sur les décisions d'implémentation
- ✅ Formules mathématiques expliquées

---

## 🎯 RÉSUMÉ

Ce projet démontre une **pipeline Big Data complète** :

```
Dataset (5000 candidats) 
    ↓
HDFS (stockage distribué)
    ↓
MapReduce (calcul des scores)
    ↓
Hive (analyses analytiques)
    ↓
HBase (affectations)
    ↓
Visualisations (graphiques)
    ↓
Rapport final
```

**Tout automatisé via un menu interactif Python ! 🐍**

---

## 📞 Support

En cas de problème :
1. Vérifiez que tous les fichiers sont dans le bon répertoire
2. Vérifiez que Python 3.8+ est installé
3. Vérifiez que matplotlib est installé
4. Consultez les messages d'erreur du programme

---

**Projet créé pour le cours Hadoop/Big Data - S10**  
*Bonne chance pour votre projet ! 🚀*
