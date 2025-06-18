"""
Script automatisé pour lancer le preprocessing complet sur l'intégralité du dataset
"""

import sys
import time
sys.path.append('src')

from src.massive_preprocessing_pipeline import MassivePreprocessingPipeline

def main():
    """
    Lance le preprocessing complet automatiquement
    """
    print("🚀 PREPROCESSING AUTOMATIQUE DE L'INTÉGRALITÉ DU DATASET AMAZON POLARITY")
    print("=" * 80)
    print("📊 Dataset à traiter:")
    print("  - 3,600,000 échantillons d'entraînement")
    print("  - 400,000 échantillons de test")
    print("  - Total: 4,000,000 échantillons")
    print("=" * 80)
    print("🔧 Configuration:")
    print("  - Preprocessing complet avec toutes les features")
    print("  - Détection et flagging des erreurs de labels")
    print("  - Multiprocessing optimisé")
    print("  - Sauvegarde en multiple formats")
    print("=" * 80)
    
    start_time = time.time()
    
    # Configuration du pipeline pour traitement complet
    pipeline = MassivePreprocessingPipeline(
        output_dir="data/processed_full",
        use_multiprocessing=True,
        chunk_size=5000  # Chunks optimisés pour 4M d'échantillons
    )
    
    try:
        print("🚀 DÉBUT DU TRAITEMENT COMPLET...")
        print("⏱️  Temps estimé: 2-3 heures")
        print("📊 Vitesse attendue: ~450 échantillons/seconde")
        print("-" * 80)
        
        # Lancer le pipeline complet
        train_df, test_df = pipeline.run_full_pipeline()
        
        total_time = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("🎉 PREPROCESSING COMPLET TERMINÉ AVEC SUCCÈS!")
        print("=" * 80)
        print(f"⏱️  Temps total: {total_time:.1f}s ({total_time/3600:.2f} heures)")
        print(f"📊 Échantillons traités: {len(train_df) + len(test_df):,}")
        print(f"⚡ Vitesse moyenne: {(len(train_df) + len(test_df))/total_time:.1f} échantillons/seconde")
        print()
        print("📈 RÉSULTATS FINAUX:")
        print(f"  🔸 Train: {len(train_df):,} échantillons")
        print(f"  🔸 Test: {len(test_df):,} échantillons")
        print(f"  🔸 Features: {len(train_df.columns)} colonnes")
        print(f"  🔸 Erreurs détectées (train): {train_df['is_label_suspect'].sum():,} ({train_df['is_label_suspect'].mean()*100:.2f}%)")
        print(f"  🔸 Erreurs détectées (test): {test_df['is_label_suspect'].sum():,} ({test_df['is_label_suspect'].mean()*100:.2f}%)")
        print()
        print("💾 DONNÉES SAUVEGARDÉES:")
        print("  📁 data/processed_full/train_processed.parquet")
        print("  📁 data/processed_full/test_processed.parquet")
        print("  📁 data/processed_full/train_processed.csv")
        print("  📁 data/processed_full/test_processed.csv")
        print("  📁 data/processed_full/processing_summary.json")
        print()
        print("✅ LE DATASET EST PRÊT POUR LA MODÉLISATION!")
        print("🎯 Prochaine étape: Entraînement des modèles de classification")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  TRAITEMENT INTERROMPU PAR L'UTILISATEUR")
        print("💡 Le traitement peut être repris plus tard")
        return False
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TRAITEMENT: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎊 FÉLICITATIONS! Votre dataset est maintenant preprocessé au niveau professionnel!")
        print("🚀 Vous pouvez maintenant passer à la modélisation avancée.")
    else:
        print("\n😞 Le preprocessing n'a pas pu être terminé.")
        print("💡 Vérifiez les logs pour plus d'informations.") 