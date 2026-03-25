# Dockerfile - Projet Big Data
# Technologies : Python 3.11 + Jupyter + Big Data Tools

FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier tous les fichiers du projet
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p data visualisations rapport && \
    chmod -R 755 scripts/

# Exposer les ports
EXPOSE 8888 8050 5000

# Variables d'environnement pour performance
ENV PYTHONUNBUFFERED=1 \
    OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1

# Commande par défaut : Lancer Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
