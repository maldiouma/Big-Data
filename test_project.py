#!/usr/bin/env python3
"""
Script de test - Vérifier que tout fonctionne
Exécuter : python test_project.py
"""

import os
import sys
import json
from pathlib import Path

def afficher_titre(titre):
    print("\n" + "="*60)
    print(f"  {titre}")
    print("="*60 + "\n")

def test_structure():
    """Vérifier la structure des répertoires"""
    afficher_titre("1️⃣  TEST STRUCTURE")
    
    dossiers_requis = [
        "scripts",
        "data",
        "visualisations",
        "rapport"
    ]
    
    fichiers_requis = [
        "main.py",
        "DEMO_COMPLETE.py",
        "NOTEBOOK_SOUMISSION.ipynb",
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        ".env",
        ".dockerignore",
        "start.bat",
        "start.sh",
        "DOCKER_GUIDE.md",
        "GETTING_STARTED.md"
    ]
    
    all_ok = True
    
    print("Dossiers :")
    for folder in dossiers_requis:
        exists = os.path.isdir(folder)
        status = "✓" if exists else "✗"
        print(f"  {status} {folder}/")
        if not exists:
            all_ok = False
    
    print("\nFichiers principaux :")
    for file in fichiers_requis:
        exists = os.path.isfile(file)
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")
        if not exists:
            all_ok = False
    
    return all_ok

def test_python_env():
    """Vérifier Python et les imports"""
    afficher_titre("2️⃣  TEST ENVIRONNEMENT PYTHON")
    
    print(f"Python version  : {sys.version.split()[0]}")
    print(f"Plateforme      : {sys.platform}")
    print(f"Répertoire courant : {os.getcwd()}")
    
    # Tester imports
    print("\nTest imports :")
    imports_tests = [
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("matplotlib", "Matplotlib"),
        ("json", "JSON"),
    ]
    
    all_ok = True
    for module, name in imports_tests:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ⚠️  {name} (non installé)")
            all_ok = False
    
    return all_ok

def test_fichiers_data():
    """Vérifier les fichiers de données"""
    afficher_titre("3️⃣  TEST FICHIERS DE DONNÉES")
    
    fichiers_data = [
        ("data/candidats.txt", "Candidats"),
        ("data/notes.txt", "Notes"),
        ("data/choix.txt", "Choix"),
        ("data/filiere.json", "Filières"),
        ("data/rang.txt", "Classement"),
        ("data/resultats.txt", "Résultats")
    ]
    
    all_ok = True
    for filepath, label in fichiers_data:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath) / 1024
            lines = sum(1 for _ in open(filepath, 'r', encoding='utf-8', errors='ignore'))
            print(f"  ✓ {label:20s} ({size:>8.2f} KB, {lines:>5d} lignes)")
        else:
            print(f"  ✗ {label:20s} (MANQUANT)")
            all_ok = False
    
    return all_ok

def test_docker():
    """Vérifier Docker"""
    afficher_titre("4️⃣  TEST DOCKER")
    
    import subprocess
    
    tests = [
        ("docker --version", "Docker"),
        ("docker-compose --version", "Docker Compose"),
    ]
    
    all_ok = True
    for cmd, name in tests:
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                print(f"  ✓ {name:20s} {version}")
            else:
                print(f"  ⚠️  {name:20s} (non disponible)")
                all_ok = False
        except Exception as e:
            print(f"  ⚠️  {name:20s} ({str(e)})")
            all_ok = False
    
    return all_ok

def test_modules_scripts():
    """Tester l'import des modules du projet"""
    afficher_titre("5️⃣  TEST MODULES PROJET")
    
    sys.path.insert(0, 'scripts')
    
    modules_tests = [
        ("generation_dataset", "Génération Dataset"),
        ("mapreduce_job", "MapReduce"),
        ("hive_queries", "Hive"),
        ("hbase_operations", "HBase"),
        ("visualisations", "Visualisations"),
    ]
    
    all_ok = True
    for module_name, label in modules_tests:
        try:
            __import__(module_name)
            print(f"  ✓ {label:20s} (importable)")
        except Exception as e:
            print(f"  ⚠️  {label:20s} ({str(e)[:50]}...)")
            all_ok = False
    
    return all_ok

def resumé_final(resultats):
    """Afficher un résumé final"""
    afficher_titre("📋 RÉSUMÉ FINAL")
    
    tests_names = [
        "Structure",
        "Python",
        "Données",
        "Docker",
        "Modules",
    ]
    
    passed = sum(resultats)
    total = len(resultats)
    
    print(f"Tests passés : {passed}/{total}\n")
    
    for name, result in zip(tests_names, resultats):
        status = "✓" if result else "⚠️ "
        print(f"  {status} {name}")
    
    if passed == total:
        print("\n✅ TOUS LES TESTS PASSENT !")
        print("\n🚀 Prochaine étape :")
        print("   1. Lancer : docker-compose up -d")
        print("   2. Ouvrir : http://localhost:8888")
        print("   3. Exécuter NOTEBOOK_SOUMISSION.ipynb")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) à corriger")
        print("\nConsultez GETTING_STARTED.md pour l'aide")
        return 1

if __name__ == "__main__":
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + "  TEST COMPLET - PROJET BIG DATA ".center(58) + "║")
    print("╚" + "═"*58 + "╝")
    
    resultats = [
        test_structure(),
        test_python_env(),
        test_fichiers_data(),
        test_docker(),
        test_modules_scripts(),
    ]
    
    exit_code = resumé_final(resultats)
    sys.exit(exit_code)
