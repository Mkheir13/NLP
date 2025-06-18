"""
Test du pipeline sur un mini échantillon de 50 lignes avec explications visuelles détaillées
"""

import sys
import os
sys.path.append('src')

from src.massive_preprocessing_pipeline import MassivePreprocessingPipeline
import time
import pandas as pd
import json
from pathlib import Path

def print_section(title, char="=", width=80):
    """Affiche une section avec style"""
    print(f"\n{char * width}")
    print(f"{title:^{width}}")
    print(f"{char * width}")

def print_subsection(title, char="-", width=60):
    """Affiche une sous-section avec style"""
    print(f"\n{char * width}")
    print(f" {title}")
    print(f"{char * width}")

def show_text_comparison(original, processed, max_length=100):
    """Affiche une comparaison visuelle avant/après"""
    print(f"📝 AVANT  : {original[:max_length]}{'...' if len(original) > max_length else ''}")
    print(f"✨ APRÈS : {processed[:max_length]}{'...' if len(processed) > max_length else ''}")
    print(f"📊 STATS : {len(original)} → {len(processed)} caractères ({(1-len(processed)/len(original))*100:.1f}% compression)")

def visualize_features(row, index):
    """Affiche les features d'un échantillon de manière visuelle"""
    print(f"\n🔍 ÉCHANTILLON #{index + 1}")
    print("┌" + "─" * 78 + "┐")
    print(f"│ 🏷️  LABEL: {'✅ POSITIF' if row['label'] == 1 else '❌ NÉGATIF':<70} │")
    print(f"│ 📏 LONGUEUR: {row['text_length']} → {row['processed_length']} chars ({(1-row['processed_length']/row['text_length'])*100:.1f}% compression){'':>20} │")
    print(f"│ 📝 MOTS: {row['word_count']} mots, {row['sentence_count']} phrases{'':>35} │")
    print(f"│ 🎭 SENTIMENT: Polarité={row['polarity']:.3f}, Subjectivité={row['subjectivity']:.3f}{'':>20} │")
    print(f"│ 🚨 SUSPECT: {'⚠️  OUI - ' + row['suspect_reason'] if row['is_label_suspect'] else '✅ NON'}{'':>10} │")
    print("├" + "─" * 78 + "┤")
    print(f"│ 📖 TITRE: {row['title'][:70]:<70} │")
    print("├" + "─" * 78 + "┤")
    print(f"│ 📄 ORIGINAL: {row['combined_text'][:66]:<66} │")
    print(f"│ ✨ PREPROCESSÉ: {row['processed_text'][:62]:<62} │")
    print("└" + "─" * 78 + "┘")

def create_visual_stats(train_df, test_df):
    """Crée des statistiques visuelles"""
    print_section("📊 STATISTIQUES VISUELLES", "=")
    
    # Distribution des labels
    print_subsection("🏷️  DISTRIBUTION DES LABELS")
    train_pos = (train_df['label'] == 1).sum()
    train_neg = (train_df['label'] == 0).sum()
    test_pos = (test_df['label'] == 1).sum()
    test_neg = (test_df['label'] == 0).sum()
    
    print("TRAIN:")
    print(f"  Positifs: {'█' * (train_pos // 2)}{train_pos:>3} ({train_pos/len(train_df)*100:.1f}%)")
    print(f"  Négatifs: {'█' * (train_neg // 2)}{train_neg:>3} ({train_neg/len(train_df)*100:.1f}%)")
    
    print("\nTEST:")
    print(f"  Positifs: {'█' * test_pos}{test_pos:>3} ({test_pos/len(test_df)*100:.1f}%)")
    print(f"  Négatifs: {'█' * test_neg}{test_neg:>3} ({test_neg/len(test_df)*100:.1f}%)")
    
    # Histogramme des longueurs
    print_subsection("📏 DISTRIBUTION DES LONGUEURS DE TEXTE")
    lengths = train_df['text_length'].values
    min_len, max_len = lengths.min(), lengths.max()
    bins = 10
    hist, bin_edges = pd.cut(lengths, bins=bins, retbins=True)
    hist_counts = hist.value_counts().sort_index()
    
    print("Histogramme des longueurs (caractères):")
    max_count = hist_counts.max()
    for i, (interval, count) in enumerate(hist_counts.items()):
        bar_length = int((count / max_count) * 30)
        left, right = int(interval.left), int(interval.right)
        print(f"  {left:>4}-{right:<4}: {'█' * bar_length}{count:>3}")
    
    # Analyse du sentiment
    print_subsection("🎭 ANALYSE DU SENTIMENT")
    polarities = train_df['polarity'].values
    
    # Créer des bins pour la polarité
    very_neg = (polarities < -0.3).sum()
    neg = ((polarities >= -0.3) & (polarities < -0.1)).sum()
    neutral = ((polarities >= -0.1) & (polarities <= 0.1)).sum()
    pos = ((polarities > 0.1) & (polarities <= 0.3)).sum()
    very_pos = (polarities > 0.3).sum()
    
    print("Distribution de la polarité:")
    print(f"  Très négatif (<-0.3): {'█' * very_neg}{very_neg:>3}")
    print(f"  Négatif (-0.3 à -0.1): {'█' * neg}{neg:>3}")
    print(f"  Neutre (-0.1 à 0.1):   {'█' * neutral}{neutral:>3}")
    print(f"  Positif (0.1 à 0.3):   {'█' * pos}{pos:>3}")
    print(f"  Très positif (>0.3):   {'█' * very_pos}{very_pos:>3}")

def show_error_analysis(train_df, test_df):
    """Analyse détaillée des erreurs détectées"""
    print_section("🚨 ANALYSE DÉTAILLÉE DES ERREURS", "=")
    
    train_errors = train_df[train_df['is_label_suspect'] == True]
    test_errors = test_df[test_df['is_label_suspect'] == True]
    
    total_errors = len(train_errors) + len(test_errors)
    total_samples = len(train_df) + len(test_df)
    
    print(f"📊 RÉSUMÉ DES ERREURS:")
    print(f"  • Total d'erreurs détectées: {total_errors}/{total_samples} ({total_errors/total_samples*100:.1f}%)")
    print(f"  • Erreurs dans train: {len(train_errors)}/{len(train_df)} ({len(train_errors)/len(train_df)*100:.1f}%)")
    print(f"  • Erreurs dans test: {len(test_errors)}/{len(test_df)} ({len(test_errors)/len(test_df)*100:.1f}%)")
    
    if total_errors == 0:
        print("\n✅ EXCELLENT! Aucune erreur de label détectée dans ce mini échantillon.")
        print("   Cela suggère que la qualité des labels est bonne ou que les critères")
        print("   de détection sont appropriés.")
        return
    
    print_subsection("🔍 DÉTAIL DES ERREURS DÉTECTÉES")
    
    all_errors = pd.concat([train_errors, test_errors]) if len(train_errors) > 0 and len(test_errors) > 0 else (train_errors if len(train_errors) > 0 else test_errors)
    
    for i, (_, row) in enumerate(all_errors.iterrows()):
        print(f"\n🚨 ERREUR #{i+1}")
        print("┌" + "─" * 78 + "┐")
        print(f"│ 🏷️  Label original: {'POSITIF' if row['label'] == 1 else 'NÉGATIF':<60} │")
        print(f"│ 🎭 Polarité calculée: {row['polarity']:.3f} (confiance: {row['confidence_score']:.3f}){'':>30} │")
        print(f"│ 💡 Label suggéré: {'POSITIF' if row['suggested_label'] == 1 else 'NÉGATIF'}{'':>55} │")
        print(f"│ ⚠️  Raison: {row['suspect_reason']:<65} │")
        print("├" + "─" * 78 + "┤")
        print(f"│ 📖 TITRE: {row['title'][:70]:<70} │")
        print(f"│ 📄 CONTENU: {row['content'][:67]:<67} │")
        print("└" + "─" * 78 + "┘")
        
        # Explication de pourquoi c'est suspect
        print("💭 EXPLICATION:")
        if row['label'] == 1 and row['polarity'] < -0.3:
            print("   Le texte est étiqueté comme POSITIF mais l'analyse de sentiment")
            print("   montre une polarité très négative. Cela pourrait indiquer:")
            print("   - Une erreur d'étiquetage")
            print("   - Un sarcasme ou ironie non détectée")
            print("   - Un contexte particulier non capturé par l'analyse")
        elif row['label'] == 0 and row['polarity'] > 0.3:
            print("   Le texte est étiqueté comme NÉGATIF mais l'analyse de sentiment")
            print("   montre une polarité très positive. Cela pourrait indiquer:")
            print("   - Une erreur d'étiquetage")
            print("   - Un texte avec critique constructive")
            print("   - Une nuance non détectée par l'analyse automatique")

def show_preprocessing_examples(train_df, num_examples=3):
    """Montre des exemples détaillés de preprocessing"""
    print_section("🔍 EXEMPLES DÉTAILLÉS DE PREPROCESSING", "=")
    
    print("Ces exemples montrent comment le texte est transformé étape par étape:")
    print("• Suppression de la ponctuation excessive")
    print("• Conversion en minuscules")
    print("• Suppression des mots vides")
    print("• Lemmatisation")
    print("• Nettoyage des espaces")
    
    for i in range(min(num_examples, len(train_df))):
        row = train_df.iloc[i]
        
        print(f"\n{'='*80}")
        print(f"EXEMPLE #{i+1} - Label: {'✅ POSITIF' if row['label'] == 1 else '❌ NÉGATIF'}")
        print(f"{'='*80}")
        
        print(f"\n📝 TITRE ORIGINAL:")
        print(f"   {row['title']}")
        
        print(f"\n📄 CONTENU ORIGINAL:")
        print(f"   {row['content'][:200]}{'...' if len(row['content']) > 200 else ''}")
        
        print(f"\n🔗 TEXTE COMBINÉ ({len(row['combined_text'])} caractères):")
        print(f"   {row['combined_text'][:300]}{'...' if len(row['combined_text']) > 300 else ''}")
        
        print(f"\n✨ TEXTE PREPROCESSÉ ({len(row['processed_text'])} caractères):")
        print(f"   {row['processed_text'][:300]}{'...' if len(row['processed_text']) > 300 else ''}")
        
        print(f"\n📊 STATISTIQUES DE TRANSFORMATION:")
        compression = (1 - len(row['processed_text']) / len(row['combined_text'])) * 100
        print(f"   • Compression: {compression:.1f}% ({len(row['combined_text'])} → {len(row['processed_text'])} chars)")
        print(f"   • Mots: {row['word_count']}")
        print(f"   • Phrases: {row['sentence_count']}")
        print(f"   • Points d'exclamation: {row['exclamation_count']}")
        print(f"   • Points d'interrogation: {row['question_count']}")
        print(f"   • Ratio majuscules: {row['upper_case_ratio']:.3f}")
        print(f"   • Ratio ponctuation: {row['punctuation_ratio']:.3f}")
        print(f"   • Ratio mots uniques: {row['unique_word_ratio']:.3f}")
        
        print(f"\n🎭 ANALYSE DE SENTIMENT:")
        print(f"   • Polarité: {row['polarity']:.3f} ({'Positif' if row['polarity'] > 0 else 'Négatif' if row['polarity'] < 0 else 'Neutre'})")
        print(f"   • Subjectivité: {row['subjectivity']:.3f} ({'Subjectif' if row['subjectivity'] > 0.5 else 'Objectif'})")
        
        if row['is_label_suspect']:
            print(f"\n⚠️  ALERTE QUALITÉ:")
            print(f"   • Erreur potentielle détectée: {row['suspect_reason']}")
            print(f"   • Label suggéré: {'POSITIF' if row['suggested_label'] == 1 else 'NÉGATIF'}")

def test_mini_sample_visual():
    """
    Test le pipeline sur seulement 50 échantillons avec explications visuelles détaillées
    """
    print_section("🧪 TEST MINI-ÉCHANTILLON AVEC EXPLICATIONS VISUELLES", "=")
    
    print("Ce test va:")
    print("• ✅ Charger 50 échantillons d'entraînement + 10 de test")
    print("• ✅ Appliquer tout le pipeline de preprocessing")
    print("• ✅ Créer des sauvegardes multiples")
    print("• ✅ Analyser les résultats en détail")
    print("• ✅ Détecter les erreurs potentielles")
    print("• ✅ Fournir des explications visuelles")
    
    # Configuration pour mini test
    output_dir = "data/mini_test_visual"
    pipeline = MassivePreprocessingPipeline(
        output_dir=output_dir,
        use_multiprocessing=False,  # Pas de multiprocessing pour 50 échantillons
        chunk_size=25  # Très petits chunks
    )
    
    # Créer le dossier de sauvegarde
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print_section("📥 CHARGEMENT DES DONNÉES", "=")
    
    # Charger seulement 50 échantillons
    from datasets import load_dataset
    
    print("🔄 Chargement d'un mini échantillon depuis HuggingFace...")
    start_time = time.time()
    
    # Charger seulement 50 échantillons train et 10 test
    train_dataset = load_dataset("fancyzhx/amazon_polarity", split="train[:50]")
    test_dataset = load_dataset("fancyzhx/amazon_polarity", split="test[:10]")
    
    load_time = time.time() - start_time
    print(f"✅ Mini échantillon chargé en {load_time:.1f}s")
    print(f"   • Train: {len(train_dataset)} échantillons")
    print(f"   • Test: {len(test_dataset)} échantillons")
    print(f"   • Dataset: Amazon Polarity (reviews de produits)")
    print(f"   • Labels: 0=Négatif, 1=Positif")
    
    # Montrer quelques exemples bruts
    print_subsection("👀 APERÇU DES DONNÉES BRUTES")
    for i in range(min(3, len(train_dataset))):
        sample = train_dataset[i]
        print(f"\n📦 Échantillon {i+1}:")
        print(f"   🏷️  Label: {'✅ POSITIF' if sample['label'] == 1 else '❌ NÉGATIF'}")
        print(f"   📖 Titre: {sample['title']}")
        print(f"   📄 Contenu: {sample['content'][:100]}...")
    
    # SAUVEGARDE 1: Données brutes
    print_section("💾 SAUVEGARDE 1: DONNÉES BRUTES", "=")
    raw_train = pd.DataFrame(train_dataset)
    raw_test = pd.DataFrame(test_dataset)
    
    raw_train.to_csv(f"{output_dir}/raw_train_backup.csv", index=False)
    raw_test.to_csv(f"{output_dir}/raw_test_backup.csv", index=False)
    print(f"✅ Sauvegardé: raw_train_backup.csv ({len(raw_train)} lignes)")
    print(f"✅ Sauvegardé: raw_test_backup.csv ({len(raw_test)} lignes)")
    
    # Traitement des données
    print_section("🔧 TRAITEMENT DU MINI TRAIN", "=")
    print("Application du pipeline complet:")
    print("• Combinaison titre + contenu")
    print("• Nettoyage et normalisation du texte")
    print("• Extraction de features linguistiques")
    print("• Analyse de sentiment")
    print("• Détection d'erreurs de labels")
    
    train_df = pipeline.process_dataset_split(train_dataset, 'mini_train')
    
    # SAUVEGARDE 2: Train preprocessé
    print_section("💾 SAUVEGARDE 2: TRAIN PREPROCESSÉ", "=")
    train_df.to_csv(f"{output_dir}/processed_train_backup.csv", index=False)
    train_df.to_parquet(f"{output_dir}/processed_train_backup.parquet", index=False)
    print(f"✅ Sauvegardé: processed_train_backup.csv ({len(train_df)} lignes)")
    print(f"✅ Sauvegardé: processed_train_backup.parquet")
    print(f"📊 Features créées: {len(train_df.columns)} colonnes")
    
    print_section("🔧 TRAITEMENT DU MINI TEST", "=")
    test_df = pipeline.process_dataset_split(test_dataset, 'mini_test')
    
    # SAUVEGARDE 3: Test preprocessé
    print_section("💾 SAUVEGARDE 3: TEST PREPROCESSÉ", "=")
    test_df.to_csv(f"{output_dir}/processed_test_backup.csv", index=False)
    test_df.to_parquet(f"{output_dir}/processed_test_backup.parquet", index=False)
    print(f"✅ Sauvegardé: processed_test_backup.csv ({len(test_df)} lignes)")
    print(f"✅ Sauvegardé: processed_test_backup.parquet")
    
    # Sauvegarder via le pipeline standard
    pipeline.save_processed_data(train_df, test_df)
    
    # Créer des statistiques visuelles
    create_visual_stats(train_df, test_df)
    
    # Analyser les erreurs
    show_error_analysis(train_df, test_df)
    
    # Montrer des exemples de preprocessing
    show_preprocessing_examples(train_df, num_examples=3)
    
    # Résumé final avec style
    print_section("🎯 RÉSUMÉ FINAL", "=")
    
    total_errors = train_df['is_label_suspect'].sum() + test_df['is_label_suspect'].sum()
    compression_ratio = (1 - train_df['processed_length'].mean() / train_df['text_length'].mean()) * 100
    
    print("📊 DONNÉES TRAITÉES:")
    print(f"   ✅ Train: {len(train_df)} échantillons")
    print(f"   ✅ Test: {len(test_df)} échantillons")
    print(f"   ✅ Features: {len(train_df.columns)} colonnes créées")
    
    print("\n🔧 PERFORMANCE DU PREPROCESSING:")
    print(f"   ✅ Compression moyenne: {compression_ratio:.1f}%")
    print(f"   ✅ Mots moyens par échantillon: {train_df['word_count'].mean():.1f}")
    print(f"   ✅ Phrases moyennes par échantillon: {train_df['sentence_count'].mean():.1f}")
    
    print("\n🎭 ANALYSE DE SENTIMENT:")
    print(f"   ✅ Polarité moyenne: {train_df['polarity'].mean():.3f}")
    print(f"   ✅ Subjectivité moyenne: {train_df['subjectivity'].mean():.3f}")
    
    print("\n🚨 CONTRÔLE QUALITÉ:")
    if total_errors > 0:
        print(f"   ⚠️  {total_errors} erreur(s) potentielle(s) détectée(s)")
        print(f"   📊 Taux d'erreur: {total_errors/(len(train_df)+len(test_df))*100:.1f}%")
        print("   💡 Le système de détection fonctionne correctement")
    else:
        print("   ✅ Aucune erreur détectée dans ce mini échantillon")
        print("   💡 Qualité des labels semble bonne")
    
    print("\n💾 FICHIERS CRÉÉS:")
    print(f"   📁 Dossier: {output_dir}/")
    print("   ✅ Données brutes (CSV)")
    print("   ✅ Données preprocessées (CSV + Parquet + Pickle)")
    print("   ✅ Statistiques et analyses (JSON)")
    
    print_section("🚀 PROCHAINES ÉTAPES", "=")
    print("1️⃣  Examiner les fichiers créés pour comprendre les transformations")
    print("2️⃣  Lancer: python analyze_mini_results.py (pour plus d'analyses)")
    print("3️⃣  Si satisfait, tester sur plus d'échantillons:")
    print("     • python test_massive_pipeline.py (10k échantillons)")
    print("     • python run_full_preprocessing.py (4M échantillons)")
    
    print_section("✅ MINI TEST VISUEL TERMINÉ AVEC SUCCÈS!", "=")
    
    return train_df, test_df

def main():
    """
    Lance le mini test visuel
    """
    try:
        print("🚀 LANCEMENT DU MINI TEST AVEC EXPLICATIONS VISUELLES")
        
        train_df, test_df = test_mini_sample_visual()
        
        print(f"\n🎉 MINI TEST VISUEL RÉUSSI!")
        print(f"Le pipeline est maintenant bien documenté et testé.")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU MINI TEST VISUEL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 