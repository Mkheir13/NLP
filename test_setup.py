#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration et le chargement du dataset Amazon Polarity
"""

import sys
import os
sys.path.append('src')

def test_imports():
    """Test des imports essentiels"""
    print("🔄 Test des imports...")
    
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        from datasets import load_dataset
        print("✅ Imports de base réussis")
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    
    try:
        from data_loader import AmazonPolarityLoader
        print("✅ Import du data loader réussi")
    except ImportError as e:
        print(f"❌ Erreur d'import data_loader: {e}")
        return False
        
    return True

def test_dataset_loading():
    """Test du chargement du dataset"""
    print("\n🔄 Test du chargement du dataset...")
    
    try:
        from data_loader import AmazonPolarityLoader
        
        # Initialisation
        loader = AmazonPolarityLoader()
        print("✅ Loader initialisé")
        
        # Chargement d'un petit échantillon
        dataset = loader.load_dataset(subset_size=100)
        print("✅ Dataset chargé (100 échantillons)")
        
        # Conversion en pandas
        train_df, test_df = loader.to_pandas()
        print(f"✅ Conversion pandas réussie - Train: {len(train_df)}, Test: {len(test_df)}")
        
        # Statistiques
        stats = loader.get_dataset_stats()
        print("✅ Statistiques calculées")
        
        # Échantillons
        samples = loader.get_sample_data(2)
        print("✅ Échantillons récupérés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return False

def test_directory_structure():
    """Test de la structure des répertoires"""
    print("\n🔄 Test de la structure des répertoires...")
    
    required_dirs = [
        'data', 'src', 'notebooks', 'web', 'tests'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Répertoires manquants: {missing_dirs}")
        return False
    else:
        print("✅ Structure des répertoires OK")
        return True

def test_requirements():
    """Test des requirements"""
    print("\n🔄 Test du fichier requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ Fichier requirements.txt manquant")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
        
    required_packages = ['datasets', 'transformers', 'pandas', 'numpy', 'matplotlib', 'seaborn']
    missing_packages = []
    
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Packages manquants dans requirements.txt: {missing_packages}")
        return False
    else:
        print("✅ Requirements.txt OK")
        return True

def main():
    """Fonction principale de test"""
    print("🚀 TESTS DE CONFIGURATION - ANALYSEUR DE SENTIMENT E-COMMERCE")
    print("=" * 60)
    
    tests = [
        ("Structure des répertoires", test_directory_structure),
        ("Requirements", test_requirements),
        ("Imports", test_imports),
        ("Chargement dataset", test_dataset_loading)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS DES TESTS:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RÉSUMÉ: {passed}/{len(tests)} tests réussis")
    
    if passed == len(tests):
        print("🎉 Tous les tests sont passés! Vous pouvez commencer le développement.")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez la configuration.")
        
        print("\n🔧 ACTIONS RECOMMANDÉES:")
        if not results[0][1]:  # Structure
            print("   - Créer les répertoires manquants")
        if not results[1][1]:  # Requirements
            print("   - Vérifier le fichier requirements.txt")
        if not results[2][1]:  # Imports
            print("   - Installer les dépendances: pip install -r requirements.txt")
        if not results[3][1]:  # Dataset
            print("   - Vérifier la connexion internet pour télécharger le dataset")

if __name__ == "__main__":
    main() 