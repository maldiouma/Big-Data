# 🐳 GUIDE DOCKER - Projet Big Data

## 📋 Prérequis
- Docker Desktop (v20.10+)
- Docker Compose (v1.29+)
- Au minimum 4GB de RAM disponible

## 🚀 Démarrage Rapide

### Option 1 : Avec Docker Compose (Recommandé)

```bash
# 1. Construire l'image Docker
docker-compose build

# 2. Lancer les services
docker-compose up -d

# 3. Accéder à Jupyter
# http://localhost:8888
# Pas de mot de passe requis
```

### Option 2 : Avec Docker CLI seul

```bash
# 1. Construire l'image
docker build -t projet-bigdata:latest .

# 2. Lancer le conteneur
docker run -d \
  --name bigdata-app \
  -p 8888:8888 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/visualisations:/app/visualisations \
  -v $(pwd)/rapport:/app/rapport \
  projet-bigdata:latest

# 3. Voir les logs
docker logs -f bigdata-app
```

## 📂 Structure dans Docker

```
/app/
├── scripts/              # Modules Python
├── data/                # Données générées
├── visualisations/      # Graphiques PNG
├── NOTEBOOK_SOUMISSION.ipynb  # Notebook exécutable
└── ...
```

## 🔧 Commandes Utiles

### Vérifier le statut
```bash
docker-compose ps
docker-compose logs bigdata-app
```

### Arrêter les services
```bash
docker-compose down
```

### Nettoyer complètement
```bash
docker-compose down -v
docker rmi projet-bigdata:latest
```

### Exécuter des commandes dans le conteneur
```bash
# Lancer le menu interactif
docker exec -it projet-bigdata-app python main.py

# Lancer le notebook
docker exec -it projet-bigdata-app jupyter notebook list
```

### Copier des fichiers hors du conteneur
```bash
docker cp projet-bigdata-app:/app/data/resultats.txt ./data/
```

## 📊 Accès aux Services

| Service | URL | Description |
|---------|-----|-------------|
| Jupyter | http://localhost:8888 | Notebook NOTEBOOK_SOUMISSION.ipynb |
| Visualizer | http://localhost:8050 | Dashboard Dash (optionnel) |

## 🔐 Sécurité & Performance

### Ajouter un mot de passe Jupyter
```yaml
# Dans docker-compose.yml, remplacer la commande par:
command: jupyter notebook --ip=0.0.0.0 --port=8888
```

### Augmenter les ressources
```yaml
# Dans docker-compose.yml, ajouter:
services:
  bigdata-app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

## ✅ Vérifier que tout fonctionne

1. Ouvrir http://localhost:8888
2. Cliquer sur `NOTEBOOK_SOUMISSION.ipynb`
3. Exécuter la première cellule
4. Vérifier que les imports réussissent ✅

## 📝 Notes

- Les données sont persistantes (volumes Docker)
- Les modifications locales dans `./data` sont visibles dans Docker
- Le conteneur se reconstruit si vous changez `requirements.txt`
- N'oubliez pas `docker-compose pull` pour les mises à jour

## 🐛 Dépannage

### Port 8888 déjà utilisé
```bash
docker-compose down  # ou tuer le conteneur
# Ou changer le port dans docker-compose.yml
```

### Mémoire insuffisante
```bash
# Réduire les threads numpy
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
```

### Build lent
```bash
# Utiliser le cache
docker-compose build --progress=plain
```
