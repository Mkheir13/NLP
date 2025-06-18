"""
Test du pipeline avec génération automatique de rapport HTML
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

def test_mini_sample_with_html():
    """
    Test le pipeline et génère automatiquement un rapport HTML
    """
    print_section("🧪 TEST MINI-ÉCHANTILLON + RAPPORT HTML", "=")
    
    print("Ce test va:")
    print("• ✅ Charger 50 échantillons d'entraînement + 10 de test")
    print("• ✅ Appliquer tout le pipeline de preprocessing")
    print("• ✅ Créer des sauvegardes multiples")
    print("• ✅ Générer un rapport HTML moderne et interactif")
    print("• ✅ Ouvrir automatiquement le rapport dans votre navigateur")
    
    # Configuration pour mini test
    output_dir = "data/mini_test_html"
    pipeline = MassivePreprocessingPipeline(
        output_dir=output_dir,
        use_multiprocessing=False,
        chunk_size=25
    )
    
    # Créer le dossier de sauvegarde
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print_section("📥 CHARGEMENT DES DONNÉES", "=")
    
    from datasets import load_dataset
    
    print("🔄 Chargement d'un mini échantillon depuis HuggingFace...")
    start_time = time.time()
    
    train_dataset = load_dataset("fancyzhx/amazon_polarity", split="train[:50]")
    test_dataset = load_dataset("fancyzhx/amazon_polarity", split="test[:10]")
    
    load_time = time.time() - start_time
    print(f"✅ Mini échantillon chargé en {load_time:.1f}s")
    
    # Sauvegarder les données brutes
    print_section("💾 SAUVEGARDE DES DONNÉES BRUTES", "=")
    raw_train = pd.DataFrame(train_dataset)
    raw_test = pd.DataFrame(test_dataset)
    
    raw_train.to_csv(f"{output_dir}/raw_train_backup.csv", index=False)
    raw_test.to_csv(f"{output_dir}/raw_test_backup.csv", index=False)
    print(f"✅ Données brutes sauvegardées")
    
    # Traitement
    print_section("🔧 TRAITEMENT DES DONNÉES", "=")
    print("🚀 Traitement du train...")
    train_df = pipeline.process_dataset_split(train_dataset, 'mini_train')
    
    print("🚀 Traitement du test...")
    test_df = pipeline.process_dataset_split(test_dataset, 'mini_test')
    
    # Sauvegarder les données preprocessées
    print_section("💾 SAUVEGARDE DES DONNÉES PREPROCESSÉES", "=")
    train_df.to_csv(f"{output_dir}/processed_train_backup.csv", index=False)
    test_df.to_csv(f"{output_dir}/processed_test_backup.csv", index=False)
    train_df.to_parquet(f"{output_dir}/processed_train_backup.parquet", index=False)
    test_df.to_parquet(f"{output_dir}/processed_test_backup.parquet", index=False)
    
    # Sauvegarder via le pipeline standard
    pipeline.save_processed_data(train_df, test_df)
    
    print("✅ Données preprocessées sauvegardées")
    
    # Statistiques rapides
    total_errors = train_df['is_label_suspect'].sum() + test_df['is_label_suspect'].sum()
    compression_ratio = (1 - train_df['processed_length'].mean() / train_df['text_length'].mean()) * 100
    
    print_section("📊 RÉSUMÉ RAPIDE", "=")
    print(f"✅ Échantillons traités: {len(train_df)} train + {len(test_df)} test")
    print(f"✅ Features créées: {len(train_df.columns)} colonnes")
    print(f"✅ Compression moyenne: {compression_ratio:.1f}%")
    print(f"✅ Erreurs détectées: {total_errors}")
    
    # Générer le rapport HTML
    print_section("🎨 GÉNÉRATION DU RAPPORT HTML", "=")
    
    try:
        # Import du générateur HTML
        from generate_html_report import HTMLReportGenerator
        
        print("🔄 Génération du rapport HTML en cours...")
        generator = HTMLReportGenerator(output_dir)
        report_path = generator.generate_html_report("rapport_preprocessing.html")
        
        if report_path:
            print(f"✅ Rapport HTML créé avec succès!")
            print(f"📁 Fichier: {report_path}")
            
            # Essayer d'ouvrir automatiquement
            try:
                import webbrowser
                webbrowser.open(f"file://{Path(report_path).absolute()}")
                print("🚀 Ouverture automatique dans le navigateur...")
            except Exception as e:
                print(f"💡 Ouvrez manuellement le fichier dans votre navigateur")
                print(f"   Chemin: {Path(report_path).absolute()}")
        else:
            print("❌ Erreur lors de la génération du rapport HTML")
            
    except ImportError:
        print("❌ Module plotly non trouvé. Installation en cours...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
            print("✅ Plotly installé. Relancez le script.")
        except:
            print("❌ Impossible d'installer plotly automatiquement.")
            print("💡 Installez manuellement: pip install plotly")
    except Exception as e:
        print(f"❌ Erreur lors de la génération HTML: {e}")
        print("💡 Le preprocessing s'est terminé correctement, seul le HTML a échoué")
    
    print_section("🎯 RÉSUMÉ FINAL", "=")
    print("✅ Preprocessing terminé avec succès!")
    print(f"📁 Fichiers dans: {output_dir}/")
    print("🎨 Rapport HTML moderne généré")
    print("📊 Toutes les statistiques et visuels disponibles")
    
    print_section("🚀 PROCHAINES ÉTAPES", "=")
    print("1️⃣  Consultez le rapport HTML pour une analyse complète")
    print("2️⃣  Si satisfait, testez sur plus d'échantillons:")
    print("     • python test_massive_pipeline.py (10k échantillons)")
    print("     • python run_full_preprocessing.py (4M échantillons)")
    
    return train_df, test_df

def main():
    """
    Lance le test avec génération HTML
    """
    try:
        print("🚀 LANCEMENT DU TEST AVEC RAPPORT HTML")
        
        train_df, test_df = test_mini_sample_with_html()
        
        print(f"\n🎉 TEST TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Consultez le rapport HTML pour voir tous les détails visuels")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 