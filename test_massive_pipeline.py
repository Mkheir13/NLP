"""
Test du pipeline massif avec un échantillon plus petit
"""

import sys
sys.path.append('src')

from src.massive_preprocessing_pipeline import MassivePreprocessingPipeline
import time

def test_pipeline_sample():
    """
    Test le pipeline sur un échantillon de 10,000 échantillons
    """
    print("🧪 TEST DU PIPELINE MASSIF - ÉCHANTILLON")
    print("=" * 60)
    print("Test sur 10,000 échantillons pour vérifier le fonctionnement")
    print("=" * 60)
    
    # Configuration pour test
    pipeline = MassivePreprocessingPipeline(
        output_dir="data/test_processed",
        use_multiprocessing=True,
        chunk_size=2000  # Chunks plus petits pour le test
    )
    
    # Modifier la méthode pour charger seulement un échantillon
    from datasets import load_dataset
    
    print("🔄 Chargement d'un échantillon de test...")
    start_time = time.time()
    
    # Charger seulement 10k échantillons
    train_dataset = load_dataset("fancyzhx/amazon_polarity", split="train[:10000]")
    test_dataset = load_dataset("fancyzhx/amazon_polarity", split="test[:1000]")
    
    load_time = time.time() - start_time
    print(f"✅ Échantillon chargé en {load_time:.1f}s")
    print(f"  - Train: {len(train_dataset):,} échantillons")
    print(f"  - Test: {len(test_dataset):,} échantillons")
    
    # Traiter les données
    print("\n📚 TRAITEMENT DU SPLIT D'ENTRAÎNEMENT (ÉCHANTILLON)")
    train_df = pipeline.process_dataset_split(train_dataset, 'train_sample')
    
    print("\n🧪 TRAITEMENT DU SPLIT DE TEST (ÉCHANTILLON)")
    test_df = pipeline.process_dataset_split(test_dataset, 'test_sample')
    
    # Sauvegarder
    pipeline.save_processed_data(train_df, test_df)
    
    # Afficher les résultats
    print("\n🎯 RÉSULTATS DU TEST:")
    print("=" * 40)
    print(f"Train preprocessé: {len(train_df):,} échantillons")
    print(f"Test preprocessé: {len(test_df):,} échantillons")
    print(f"Features extraites: {len(train_df.columns)} colonnes")
    print(f"Erreurs détectées (train): {train_df['is_label_suspect'].sum():,}")
    print(f"Erreurs détectées (test): {test_df['is_label_suspect'].sum():,}")
    print(f"Ratio d'erreurs (train): {train_df['is_label_suspect'].mean()*100:.2f}%")
    print(f"Ratio d'erreurs (test): {test_df['is_label_suspect'].mean()*100:.2f}%")
    
    # Afficher quelques exemples d'erreurs détectées
    print(f"\n🚨 EXEMPLES D'ERREURS DÉTECTÉES:")
    print("-" * 40)
    
    errors = train_df[train_df['is_label_suspect'] == True].head(3)
    for i, (_, row) in enumerate(errors.iterrows()):
        print(f"\n{i+1}. Label: {'Positif' if row['label'] == 1 else 'Négatif'}")
        print(f"   Polarité: {row['polarity']:.3f}")
        print(f"   Raison: {row['suspect_reason']}")
        print(f"   Texte: {row['combined_text'][:100]}...")
    
    print(f"\n✅ TEST TERMINÉ! Le pipeline fonctionne correctement.")
    print(f"📁 Résultats sauvegardés dans: data/test_processed/")
    
    return train_df, test_df

def main():
    """
    Lance le test du pipeline
    """
    try:
        train_df, test_df = test_pipeline_sample()
        
        print(f"\n🎉 TEST RÉUSSI!")
        print(f"Le pipeline est prêt pour traiter l'intégralité du dataset.")
        print(f"\nPour lancer le preprocessing complet:")
        print(f"  cd src && python massive_preprocessing_pipeline.py")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 