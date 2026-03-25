# 📚 GUIDE DE DÉMARRAGE - Projet Big Data

Bienvenue ! Voici comment démarrer le projet **Orientation Nationale - Big Data**.

---

## ⚡ Démarrage Ultra-Rapide (3 min)

### Pour Windows :
```batch
# Double-cliquez sur :
start.bat

# Choisir option 1
# Ouvrir http://localhost:8888 dans le navigateur
```

### Pour Linux / Mac :
```bash
chmod +x start.sh
./start.sh
# Choisir option 1
# Ouvrir http://localhost:8888 dans le navigateur
```

---

## 📋 Prérequis

- **Docker Desktop** : https://www.docker.com/products/docker-desktop
- **RAM disponible** : au minimum 4 GB
- **Espace disque** : 2 GB

## 🚀 Installation Complète (5 min)

### Étape 1 : Vérifier Docker
```bash
docker --version
docker-compose --version
```

### Étape 2 : Construire l'image
```bash
cd "Projet Big Data"
docker-compose build
```

### Étape 3 : Lancer les services
```bash
docker-compose up -d
```

### Étape 4 : Accéder à Jupyter
Ouvrir dans votre navigateur : **http://localhost:8888**

### Étape 5 : Ouvrir le notebook
- Cliquer sur `NOTEBOOK_SOUMISSION.ipynb`
- Exécuter les cellules dans l'ordre

---

## 📂 Structure du Projet

```
Projet Big Data/
│
├── 🎯 FICHIERS RACINE
│   ├── NOTEBOOK_SOUMISSION.ipynb    ← À OUVRIR DANS JUPYTER
│   ├── main.py                      ← Menu interactif
│   ├── DEMO_COMPLETE.py             ← Démonstration
│   ├── README.md                    ← Documentation
│   │
│   ├── 🐳 FICHIERS DOCKER (Nouveaux!)
│   ├── Dockerfile                   ← Image de base
│   ├── docker-compose.yml           ← Configuration services
│   ├── requirements.txt              ← Dépendances Python
│   ├── DOCKER_GUIDE.md              ← Guide Docker détaillé
│   ├── .env                         ← Variables d'env
│   ├── .dockerignore                ← Fichiers ignorés
│   ├── start.bat                    ← Script Windows
│   └── start.sh                     ← Script Linux/Mac
│
├── 📁 scripts/                      → Code du projet
│   ├── generation_dataset.py        → Génère 5000 candidats
│   ├── mapreduce_job.py             → Calcul des rangs
│   ├── hive_queries.py              → Requêtes analytiques
│   ├── hbase_operations.py          → Affectations nationales
│   └── visualisations.py            → Graphiques (PNG)
│
├── 📂 data/                         → Fichiers de données
│   ├── candidats.txt                → Liste candidats
│   ├── notes.txt                    → Notes par matière
│   ├── choix.txt                    → Choix d'écoles
│   ├── filiere.json                 → Écoles disponibles
│   ├── rang.txt                     → Classement (MapReduce)
│   └── resultats.txt                → Affectations (HBase)
│
├── 📷 visualisations/               → Graphiques générés
│   ├── Histogrammes_Matieres.png
│   ├── Distribution_Filieres.png
│   ├── Courbe_Moyennes.png
│   ├── Histogramme_FG.png
│   └── Repartition_Affectations.png
│
└── 📄 rapport/
    └── RAPPORT.md
```

---

## 💻 Options d'Exécution

### Option A : Avec Docker (Recommandé) ✅
**Avantages :**
- ✅ Environnement isolé et reproductible
- ✅ Pas de conflits de dépendances
- ✅ Portable sur n'importe quel ordinateur
- ✅ Facile à deployer

**Commande :**
```bash
docker-compose up -d
# Accéder à : http://localhost:8888
```

### Option B : Installation Locale
**Prérequis :**
- Python 3.11+
- pip

**Installation :**
```bash
# 1. Créer un environnement virtuel
python -m venv .venv

# 2. Activer l'environnement
# Windows :
.venv\Scripts\activate
# Linux/Mac :
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer Jupyter
jupyter notebook

# 5. Ouvrir NOTEBOOK_SOUMISSION.ipynb
```

### Option C : Menu Interactif (Sans Jupyter)
```bash
# Avec Docker :
docker exec -it projet-bigdata-app python main.py

# Localement :
python main.py
```

---

## 🎯 Workflow Principal

Le projet suit ce pipeline :

```
1. GÉNÉRATION (5000 candidats)
   ↓
2. MAPREDUCE (Calcul des scores FG)
   ↓
3. HIVE (Analyses statistiques)
   ↓
4. HBASE (Algorithm d'affectation)
   ↓
5. VISUALISATION (Graphiques PNG)
```

Chaque étape peut être exécutée individuellement depuis le **menu principal** ou directement dans le **notebook Jupyter**.

---

## 🐳 Commandes Docker Utiles

```bash
# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f bigdata-app

# Arrêter
docker-compose down

# Nettoyer
docker-compose down -v

# Relancer
docker-compose restart

# Exécuter une commande dans le conteneur
docker exec -it projet-bigdata-app python main.py
```

Pour plus de détails, consulter **DOCKER_GUIDE.md**

---

## 🔧 Dépannage

### Port 8888 déjà utilisé
```bash
# Solution 1 : Arrêter le service existant
docker-compose down

# Solution 2 : Changer le port dans docker-compose.yml
# Remplacer "8888:8888" par "8889:8888"
```

### Erreur "Docker not found"
Installer Docker Desktop : https://www.docker.com/products/docker-desktop

### Mémoire insuffisante
```bash
# Réduire les threads Python dans .env
OPENBLAS_NUM_THREADS=1
OMP_NUM_THREADS=1
```

### Affichage lent sous Windows
WSL2 peut être lent avec les chemins partagés. Solutions :
1. Placer le projet dans `C:\Users\<username>`
2. Ou installer le projet dans le WSL lui-même

---

## 📊 Résultats Attendus

Après exécution complète du pipeline :

✅ **5000 candidats** générés  
✅ **40 000 notes** créées  
✅ **FG scores** calculés (0-200)  
✅ **Affectations** générées  
✅ **5 graphiques PNG** générés  

**Durée estimée :** 3-5 minutes

---

## 📞 Support

### Common Questions

**Q : Puis-je modifier le code dans le conteneur ?**
A : Oui ! Les fichiers dans `scripts/` sont mappés via volumes. Les modifications sont immédiatement visibles.

**Q : Comment sauvegarde-t-on les résultats ?**
A : Les données dans `data/` et `visualisations/` persisten automatiquement.

**Q : Puis-je exécuter 10 000 candidats ?**
A : Oui, modifier `generer_dataset_complet(10000)` dans le notebook.

**Q : Docker prend beaucoup de place ?**
A : Oui (~2GB). Nettoyer avec `docker-compose down -v`

---

## 🎓 Apprentissage

Ce projet enseigne :
- **Big Data** : Génération et traitement massif
- **MapReduce** : Paradigme distribué
- **Hive/SQL** : Requêtes analytiques
- **HBase** : Algorithmes d'affectation
- **Visualisation** : Matplotlib/Plots
- **Docker** : Containerisation & DevOps

---

## 📄 Fichiers Importants

| Fichier | Description |
|---------|-------------|
| [NOTEBOOK_SOUMISSION.ipynb](NOTEBOOK_SOUMISSION.ipynb) | **À exécuter** |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | Guide Docker complet |
| [docker-compose.yml](docker-compose.yml) | Configuration Docker |
| [requirements.txt](requirements.txt) | Dépendances Python |
| [main.py](main.py) | Menu interactif |

---

**Bon travail ! 🚀**
