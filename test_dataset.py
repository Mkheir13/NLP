#!/usr/bin/env python3
"""
Test simple pour vérifier le chargement du dataset Amazon Polarity
"""

print("🔄 Test du chargement direct du dataset Amazon Polarity...")

try:
    from datasets import load_dataset
    
    # Chargement direct comme recommandé sur le site Hugging Face
    print("📥 Chargement du dataset...")
    ds = load_dataset("fancyzhx/amazon_polarity")
    
    print("✅ Dataset chargé avec succès!")
    print(f"   - Train: {len(ds['train']):,} échantillons")
    print(f"   - Test: {len(ds['test']):,} échantillons")
    
    # Affichage d'un échantillon
    print("\n📋 Premier échantillon du train:")
    sample = ds['train'][0]
    print(f"   - Label: {sample['label']} ({'Positif' if sample['label'] == 1 else 'Négatif'})")
    print(f"   - Titre: {sample['title']}")
    print(f"   - Contenu: {sample['content'][:200]}...")
    
    # Structure du dataset
    print(f"\n📊 Structure du dataset:")
    print(f"   - Features: {ds['train'].features}")
    
    # Test de notre data_loader
    print("\n🔄 Test de notre data_loader personnalisé...")
    import sys
    sys.path.append('src')
    from data_loader import AmazonPolarityLoader
    
    loader = AmazonPolarityLoader()
    dataset_custom = loader.load_dataset(subset_size=1000)  # Petit échantillon
    
    print("✅ Notre data_loader fonctionne aussi!")
    print(f"   - Train custom: {len(dataset_custom['train'])} échantillons")
    print(f"   - Test custom: {len(dataset_custom['test'])} échantillons")
    
    print("\n🎉 TOUS LES TESTS RÉUSSIS!")
    print("Le dataset Amazon Polarity est prêt à être utilisé.")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc() 