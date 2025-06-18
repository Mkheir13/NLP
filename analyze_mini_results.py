"""
Script pour analyser les résultats du mini test
"""

import pandas as pd
import json
from pathlib import Path

def analyze_mini_results():
    """
    Analyse les résultats du mini test
    """
    print("🔍 ANALYSE DES RÉSULTATS DU MINI TEST")
    print("=" * 60)
    
    # Charger les données
    data_dir = Path("data/mini_test")
    
    if not data_dir.exists():
        print("❌ Dossier de mini test non trouvé. Lancez d'abord test_mini_sample.py")
        return
    
    # Charger les DataFrames
    train_df = pd.read_csv(data_dir / "processed_train_backup.csv")
    test_df = pd.read_csv(data_dir / "processed_test_backup.csv")
    
    # Charger l'analyse détaillée
    with open(data_dir / "detailed_analysis.json", 'r', encoding='utf-8') as f:
        detailed_stats = json.load(f)
    
    print(f"📊 DONNÉES CHARGÉES:")
    print(f"  - Train: {len(train_df)} échantillons")
    print(f"  - Test: {len(test_df)} échantillons")
    print(f"  - Colonnes: {len(train_df.columns)}")
    
    # Analyse des features
    print(f"\n📝 FEATURES CRÉÉES:")
    print("-" * 40)
    feature_categories = {
        'Originales': ['title', 'content', 'label'],
        'Texte combiné': ['combined_text', 'processed_text'],
        'Métriques de base': ['text_length', 'processed_length', 'word_count', 'sentence_count'],
        'Sentiment': ['polarity', 'subjectivity'],
        'Style': ['exclamation_count', 'question_count', 'upper_case_ratio', 'punctuation_ratio', 'unique_word_ratio'],
        'Qualité': ['is_label_suspect', 'suspect_reason', 'suggested_label', 'confidence_score']
    }
    
    for category, features in feature_categories.items():
        print(f"\n{category}:")
        for feature in features:
            if feature in train_df.columns:
                print(f"  ✅ {feature}")
            else:
                print(f"  ❌ {feature} (manquant)")
    
    # Analyse des erreurs détectées
    print(f"\n🚨 ANALYSE DES ERREURS DE LABELS:")
    print("-" * 40)
    
    train_errors = train_df[train_df['is_label_suspect'] == True]
    test_errors = test_df[test_df['is_label_suspect'] == True]
    
    print(f"Train: {len(train_errors)}/{len(train_df)} erreurs ({len(train_errors)/len(train_df)*100:.1f}%)")
    print(f"Test: {len(test_errors)}/{len(test_df)} erreurs ({len(test_errors)/len(test_df)*100:.1f}%)")
    
    if len(train_errors) > 0:
        print(f"\n🔍 DÉTAIL DES ERREURS TRAIN:")
        for i, (_, row) in enumerate(train_errors.iterrows()):
            print(f"\n{i+1}. Label: {'Positif' if row['label'] == 1 else 'Négatif'}")
            print(f"   Polarité: {row['polarity']:.3f}")
            print(f"   Confiance: {row['confidence_score']:.3f}")
            print(f"   Raison: {row['suspect_reason']}")
            print(f"   Titre: {row['title'][:60]}...")
    
    if len(test_errors) > 0:
        print(f"\n🔍 DÉTAIL DES ERREURS TEST:")
        for i, (_, row) in enumerate(test_errors.iterrows()):
            print(f"\n{i+1}. Label: {'Positif' if row['label'] == 1 else 'Négatif'}")
            print(f"   Polarité: {row['polarity']:.3f}")
            print(f"   Confiance: {row['confidence_score']:.3f}")
            print(f"   Raison: {row['suspect_reason']}")
            print(f"   Titre: {row['title'][:60]}...")
    
    # Analyse des statistiques de texte
    print(f"\n📊 STATISTIQUES DE TEXTE:")
    print("-" * 40)
    print(f"Longueur originale:")
    print(f"  - Moyenne: {train_df['text_length'].mean():.1f} caractères")
    print(f"  - Min: {train_df['text_length'].min()} caractères")
    print(f"  - Max: {train_df['text_length'].max()} caractères")
    
    print(f"\nLongueur preprocessée:")
    print(f"  - Moyenne: {train_df['processed_length'].mean():.1f} caractères")
    print(f"  - Min: {train_df['processed_length'].min()} caractères")
    print(f"  - Max: {train_df['processed_length'].max()} caractères")
    
    compression_ratio = (1 - train_df['processed_length'].mean() / train_df['text_length'].mean()) * 100
    print(f"\nRatio de compression: {compression_ratio:.1f}%")
    
    # Analyse du sentiment
    print(f"\n🎭 ANALYSE DU SENTIMENT:")
    print("-" * 40)
    print(f"Polarité:")
    print(f"  - Moyenne: {train_df['polarity'].mean():.3f}")
    print(f"  - Min: {train_df['polarity'].min():.3f}")
    print(f"  - Max: {train_df['polarity'].max():.3f}")
    
    print(f"\nSubjectivité:")
    print(f"  - Moyenne: {train_df['subjectivity'].mean():.3f}")
    print(f"  - Min: {train_df['subjectivity'].min():.3f}")
    print(f"  - Max: {train_df['subjectivity'].max():.3f}")
    
    # Distribution des labels
    print(f"\n📈 DISTRIBUTION DES LABELS:")
    print("-" * 40)
    train_label_dist = train_df['label'].value_counts()
    test_label_dist = test_df['label'].value_counts()
    
    print(f"Train:")
    print(f"  - Négatif (0): {train_label_dist.get(0, 0)} ({train_label_dist.get(0, 0)/len(train_df)*100:.1f}%)")
    print(f"  - Positif (1): {train_label_dist.get(1, 0)} ({train_label_dist.get(1, 0)/len(train_df)*100:.1f}%)")
    
    print(f"\nTest:")
    print(f"  - Négatif (0): {test_label_dist.get(0, 0)} ({test_label_dist.get(0, 0)/len(test_df)*100:.1f}%)")
    print(f"  - Positif (1): {test_label_dist.get(1, 0)} ({test_label_dist.get(1, 0)/len(test_df)*100:.1f}%)")
    
    # Exemples de preprocessing
    print(f"\n🔍 EXEMPLES DE PREPROCESSING:")
    print("-" * 40)
    
    for i in range(min(3, len(train_df))):
        row = train_df.iloc[i]
        print(f"\n{i+1}. Label: {'Positif' if row['label'] == 1 else 'Négatif'}")
        print(f"   Original: {row['combined_text'][:80]}...")
        print(f"   Preprocessé: {row['processed_text'][:80]}...")
        print(f"   Compression: {len(row['combined_text'])} → {len(row['processed_text'])} chars")
        print(f"   Polarité: {row['polarity']:.3f}")
    
    # Fichiers créés
    print(f"\n💾 FICHIERS CRÉÉS:")
    print("-" * 40)
    
    files_to_check = [
        "raw_train_backup.csv",
        "raw_test_backup.csv",
        "processed_train_backup.csv",
        "processed_test_backup.csv",
        "train_processed.parquet",
        "test_processed.parquet",
        "processing_summary.json",
        "detailed_analysis.json"
    ]
    
    total_size = 0
    for filename in files_to_check:
        filepath = data_dir / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            total_size += size_kb
            print(f"  ✅ {filename} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {filename} (manquant)")
    
    print(f"\nTaille totale: {total_size:.1f} KB ({total_size/1024:.1f} MB)")
    
    # Recommandations
    print(f"\n🎯 RECOMMANDATIONS:")
    print("-" * 40)
    
    if len(train_errors) + len(test_errors) > 0:
        print(f"✅ Le système de détection d'erreurs fonctionne")
        print(f"   → {len(train_errors) + len(test_errors)} erreurs détectées au total")
    
    if compression_ratio > 30:
        print(f"✅ Bon ratio de compression ({compression_ratio:.1f}%)")
        print(f"   → Le preprocessing nettoie efficacement le texte")
    
    print(f"✅ Pipeline fonctionnel sur mini échantillon")
    print(f"   → Prêt pour test sur échantillon plus grand")
    
    print(f"\n🚀 PROCHAINES ÉTAPES:")
    print(f"  1. python test_massive_pipeline.py  (10k échantillons)")
    print(f"  2. python run_full_preprocessing.py  (4M échantillons)")
    
    return train_df, test_df

def main():
    """
    Lance l'analyse
    """
    try:
        train_df, test_df = analyze_mini_results()
        print(f"\n✅ ANALYSE TERMINÉE!")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DE L'ANALYSE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 