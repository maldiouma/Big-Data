#!/bin/bash
# Script de lancement - Projet Big Data avec Docker

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🐳 LANCEMENT - PROJET BIG DATA AVEC DOCKER            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Couleurs pour l'output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}❌ Docker n'est pas installé !${NC}"
    echo "Télécharge Docker Desktop depuis : https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  docker-compose n'est pas disponible${NC}"
    echo "Installe Docker Desktop qui inclut docker-compose"
    exit 1
fi

echo -e "${GREEN}✓ Docker détecté${NC}"
echo -e "${GREEN}✓ Docker Compose détecté${NC}"
echo ""

# Menu d'options
echo -e "${BLUE}Choisissez une action :${NC}"
echo "1) Construire & Lancer (première fois)"
echo "2) Relancer les services"
echo "3) Afficher les logs"
echo "4) Arrêter les services"
echo "5) Nettoyer complètement"
echo ""
read -p "Choix (1-5) : " choice

case $choice in
    1)
        echo -e "${BLUE}🔨 Construction de l'image Docker...${NC}"
        docker-compose build
        echo ""
        echo -e "${BLUE}🚀 Lancement des services...${NC}"
        docker-compose up -d
        echo ""
        echo -e "${GREEN}✓ Services lancés !${NC}"
        echo ""
        echo -e "${YELLOW}📌 Jupyter Notebook : http://localhost:8888${NC}"
        echo -e "${YELLOW}📌 Fichier à ouvrir : NOTEBOOK_SOUMISSION.ipynb${NC}"
        echo ""
        sleep 2
        docker-compose ps
        ;;
    2)
        echo -e "${BLUE}🔄 Redémarrage des services...${NC}"
        docker-compose restart
        docker-compose ps
        ;;
    3)
        echo -e "${BLUE}📋 Logs des services :${NC}"
        docker-compose logs -f --tail=50
        ;;
    4)
        echo -e "${YELLOW}⏹️  Arrêt des services...${NC}"
        docker-compose down
        echo -e "${GREEN}✓ Services arrêtés${NC}"
        ;;
    5)
        echo -e "${YELLOW}🗑️  Nettoyage complet (images + volumes)...${NC}"
        read -p "Êtes-vous sûr ? (y/n) : " confirm
        if [ "$confirm" = "y" ]; then
            docker-compose down -v
            docker rmi projet-bigdata:latest
            echo -e "${GREEN}✓ Nettoyage terminé${NC}"
        else
            echo "Annulé"
        fi
        ;;
    *)
        echo -e "${YELLOW}❌ Choix invalide${NC}"
        exit 1
        ;;
esac
