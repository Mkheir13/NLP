"""
Test du pipeline sur un mini échantillon de 50 lignes avec tables de sauvegarde
"""

import sys
import os
sys.path.append('src')

from src.massive_preprocessing_pipeline import MassivePreprocessingPipeline
import time
import pandas as pd
import json
from pathlib import Path

def test_mini_sample():
    """
    Test le pipeline sur seulement 50 échantillons avec tables de sauvegarde
    """
    print("🧪 TEST MINI-ÉCHANTILLON - 50 LIGNES AVEC SAUVEGARDES")
    print("=" * 70)
    print("Test sur 50 échantillons pour voir le fonctionnement détaillé")
    print("Avec tables de sauvegarde au cas où")
    print("=" * 70)
    
    # Configuration pour mini test
    output_dir = "data/mini_test"
    pipeline = MassivePreprocessingPipeline(
        output_dir=output_dir,
        use_multiprocessing=False,  # Pas de multiprocessing pour 50 échantillons
        chunk_size=25  # Très petits chunks
    )
    
    # Créer le dossier de sauvegarde
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Charger seulement 50 échantillons
    from datasets import load_dataset
    
    print("🔄 Chargement d'un mini échantillon...")
    start_time = time.time()
    
    # Charger seulement 50 échantillons train et 10 test
    train_dataset = load_dataset("fancyzhx/amazon_polarity", split="train[:50]")
    test_dataset = load_dataset("fancyzhx/amazon_polarity", split="test[:10]")
    
    load_time = time.time() - start_time
    print(f"✅ Mini échantillon chargé en {load_time:.1f}s")
    print(f"  - Train: {len(train_dataset)} échantillons")
    print(f"  - Test: {len(test_dataset)} échantillons")
    
    # SAUVEGARDE 1: Données brutes
    print("\n💾 SAUVEGARDE 1: Données brutes")
    raw_train = pd.DataFrame(train_dataset)
    raw_test = pd.DataFrame(test_dataset)
    
    raw_train.to_csv(f"{output_dir}/raw_train_backup.csv", index=False)
    raw_test.to_csv(f"{output_dir}/raw_test_backup.csv", index=False)
    print(f"  ✅ Sauvegardé: raw_train_backup.csv ({len(raw_train)} lignes)")
    print(f"  ✅ Sauvegardé: raw_test_backup.csv ({len(raw_test)} lignes)")
    
    # Traiter les données
    print("\n📚 TRAITEMENT DU MINI TRAIN")
    print("-" * 40)
    train_df = pipeline.process_dataset_split(train_dataset, 'mini_train')
    
    # SAUVEGARDE 2: Train preprocessé
    print("\n💾 SAUVEGARDE 2: Train preprocessé")
    train_df.to_csv(f"{output_dir}/processed_train_backup.csv", index=False)
    train_df.to_parquet(f"{output_dir}/processed_train_backup.parquet", index=False)
    print(f"  ✅ Sauvegardé: processed_train_backup.csv ({len(train_df)} lignes)")
    print(f"  ✅ Sauvegardé: processed_train_backup.parquet")
    
    print("\n🧪 TRAITEMENT DU MINI TEST")
    print("-" * 40)
    test_df = pipeline.process_dataset_split(test_dataset, 'mini_test')
    
    # SAUVEGARDE 3: Test preprocessé
    print("\n💾 SAUVEGARDE 3: Test preprocessé")
    test_df.to_csv(f"{output_dir}/processed_test_backup.csv", index=False)
    test_df.to_parquet(f"{output_dir}/processed_test_backup.parquet", index=False)
    print(f"  ✅ Sauvegardé: processed_test_backup.csv ({len(test_df)} lignes)")
    print(f"  ✅ Sauvegardé: processed_test_backup.parquet")
    
    # Sauvegarder via le pipeline standard
    pipeline.save_processed_data(train_df, test_df)
    
    # SAUVEGARDE 4: Analyse détaillée
    print("\n💾 SAUVEGARDE 4: Analyse détaillée")
    
    # Analyse des colonnes
    columns_info = {
        'total_columns': len(train_df.columns),
        'column_names': list(train_df.columns),
        'data_types': {col: str(train_df[col].dtype) for col in train_df.columns}
    }
    
    # Statistiques détaillées
    detailed_stats = {
        'dataset_size': {
            'train': len(train_df),
            'test': len(test_df),
            'total': len(train_df) + len(test_df)
        },
        'columns_info': columns_info,
        'text_analysis': {
            'avg_original_length': float(train_df['text_length'].mean()),
            'max_original_length': int(train_df['text_length'].max()),
            'min_original_length': int(train_df['text_length'].min()),
            'avg_processed_length': float(train_df['processed_length'].mean()),
            'compression_ratio': float(1 - (train_df['processed_length'].mean() / train_df['text_length'].mean()))
        },
        'sentiment_analysis': {
            'avg_polarity': float(train_df['polarity'].mean()),
            'avg_subjectivity': float(train_df['subjectivity'].mean()),
            'polarity_range': [float(train_df['polarity'].min()), float(train_df['polarity'].max())]
        },
        'label_quality': {
            'train_suspect_count': int(train_df['is_label_suspect'].sum()),
            'test_suspect_count': int(test_df['is_label_suspect'].sum()),
            'train_suspect_ratio': float(train_df['is_label_suspect'].mean()),
            'test_suspect_ratio': float(test_df['is_label_suspect'].mean())
        }
    }
    
    with open(f"{output_dir}/detailed_analysis.json", 'w', encoding='utf-8') as f:
        json.dump(detailed_stats, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Sauvegardé: detailed_analysis.json")
    
    # Afficher les résultats détaillés
    print("\n🎯 RÉSULTATS DÉTAILLÉS DU MINI TEST:")
    print("=" * 50)
    print(f"📊 Données traitées:")
    print(f"  - Train: {len(train_df)} échantillons")
    print(f"  - Test: {len(test_df)} échantillons")
    print(f"  - Features extraites: {len(train_df.columns)} colonnes")
    
    print(f"\n📝 Colonnes créées:")
    for i, col in enumerate(train_df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\n📊 Statistiques texte:")
    print(f"  - Longueur moyenne originale: {train_df['text_length'].mean():.1f} caractères")
    print(f"  - Longueur moyenne preprocessée: {train_df['processed_length'].mean():.1f} caractères")
    print(f"  - Ratio de compression: {(1 - train_df['processed_length'].mean()/train_df['text_length'].mean())*100:.1f}%")
    
    print(f"\n🎭 Analyse de sentiment:")
    print(f"  - Polarité moyenne: {train_df['polarity'].mean():.3f}")
    print(f"  - Subjectivité moyenne: {train_df['subjectivity'].mean():.3f}")
    
    print(f"\n🚨 Qualité des labels:")
    print(f"  - Erreurs détectées (train): {train_df['is_label_suspect'].sum()}/{len(train_df)} ({train_df['is_label_suspect'].mean()*100:.1f}%)")
    print(f"  - Erreurs détectées (test): {test_df['is_label_suspect'].sum()}/{len(test_df)} ({test_df['is_label_suspect'].mean()*100:.1f}%)")
    
    # Afficher quelques exemples d'erreurs détectées si il y en a
    errors = train_df[train_df['is_label_suspect'] == True]
    if len(errors) > 0:
        print(f"\n🚨 EXEMPLES D'ERREURS DÉTECTÉES:")
        print("-" * 50)
        
        for i, (_, row) in enumerate(errors.head(3).iterrows()):
            print(f"\n{i+1}. Label original: {'Positif' if row['label'] == 1 else 'Négatif'}")
            print(f"   Polarité calculée: {row['polarity']:.3f}")
            print(f"   Raison: {row['suspect_reason']}")
            print(f"   Titre: {row['title'][:80]}...")
            print(f"   Contenu: {row['content'][:100]}...")
    else:
        print(f"\n✅ Aucune erreur de label détectée dans ce mini échantillon")
    
    # Afficher quelques exemples de preprocessing
    print(f"\n🔍 EXEMPLES DE PREPROCESSING:")
    print("-" * 50)
    for i in range(min(3, len(train_df))):
        row = train_df.iloc[i]
        print(f"\n{i+1}. Échantillon:")
        print(f"   Original ({len(row['combined_text'])} chars): {row['combined_text'][:100]}...")
        print(f"   Preprocessé ({len(row['processed_text'])} chars): {row['processed_text'][:100]}...")
        print(f"   Features: {row['word_count']} mots, {row['sentence_count']} phrases")
    
    print(f"\n💾 FICHIERS DE SAUVEGARDE CRÉÉS:")
    print("-" * 50)
    backup_files = [
        "raw_train_backup.csv",
        "raw_test_backup.csv", 
        "processed_train_backup.csv",
        "processed_train_backup.parquet",
        "processed_test_backup.csv",
        "processed_test_backup.parquet",
        "train_processed.csv",
        "test_processed.csv",
        "train_processed.parquet",
        "test_processed.parquet",
        "train_processed.pkl",
        "test_processed.pkl",
        "processing_stats.json",
        "processing_summary.json",
        "detailed_analysis.json"
    ]
    
    for filename in backup_files:
        filepath = Path(output_dir) / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print(f"  ✅ {filename} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {filename} (non créé)")
    
    print(f"\n✅ MINI TEST TERMINÉ!")
    print(f"📁 Tous les fichiers sont dans: {output_dir}/")
    print(f"🎯 Le pipeline fonctionne correctement sur le mini échantillon")
    
    return train_df, test_df

def main():
    """
    Lance le mini test
    """
    try:
        print("🚀 LANCEMENT DU MINI TEST (50 ÉCHANTILLONS)")
        
        train_df, test_df = test_mini_sample()
        
        print(f"\n🎉 MINI TEST RÉUSSI!")
        print(f"Le pipeline est prêt pour des échantillons plus grands.")
        print(f"\nPour tester sur 10k échantillons:")
        print(f"  python test_massive_pipeline.py")
        print(f"\nPour le preprocessing complet:")
        print(f"  python run_full_preprocessing.py")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU MINI TEST: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 