@echo off
REM Script de lancement - Projet Big Data avec Docker (Windows)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🐳 LANCEMENT - PROJET BIG DATA AVEC DOCKER            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Vérifier si Docker est installé
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker n'est pas installé !
    echo Télécharge Docker Desktop depuis : https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✓ Docker détecté
echo ✓ Docker Compose détecté
echo.

echo Choisissez une action :
echo 1) Construire ^& Lancer (première fois^)
echo 2) Relancer les services
echo 3) Afficher les logs
echo 4) Arrêter les services
echo 5) Nettoyer complètement
echo.
set /p choice="Choix (1-5) : "

if "%choice%"=="1" (
    echo.
    echo 🔨 Construction de l'image Docker...
    docker-compose build
    echo.
    echo 🚀 Lancement des services...
    docker-compose up -d
    echo.
    echo ✓ Services lancés !
    echo.
    echo 📌 Jupyter Notebook : http://localhost:8888
    echo 📌 Fichier à ouvrir : NOTEBOOK_SOUMISSION.ipynb
    echo.
    timeout /t 2 /nobreak
    docker-compose ps
) else if "%choice%"=="2" (
    echo.
    echo 🔄 Redémarrage des services...
    docker-compose restart
    docker-compose ps
) else if "%choice%"=="3" (
    echo.
    echo 📋 Logs des services :
    docker-compose logs -f --tail=50
) else if "%choice%"=="4" (
    echo.
    echo ⏹️  Arrêt des services...
    docker-compose down
    echo ✓ Services arrêtés
) else if "%choice%"=="5" (
    echo.
    echo 🗑️  Nettoyage complet (images + volumes^)...
    set /p confirm="Êtes-vous sûr ? (y/n) : "
    if "%confirm%"=="y" (
        docker-compose down -v
        docker rmi projet-bigdata:latest
        echo ✓ Nettoyage terminé
    ) else (
        echo Annulé
    )
) else (
    echo ❌ Choix invalide
    exit /b 1
)
