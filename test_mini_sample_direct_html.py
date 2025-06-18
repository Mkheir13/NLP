"""
Test du pipeline avec ouverture DIRECTE de la page HTML
"""

import sys
import os
sys.path.append('src')

from src.massive_preprocessing_pipeline import MassivePreprocessingPipeline
import time
import pandas as pd
import json
from pathlib import Path
import webbrowser
import subprocess

def open_html_immediately(html_path):
    """Ouvre immédiatement le fichier HTML dans le navigateur"""
    html_path = Path(html_path).absolute()
    
    print(f"🚀 Ouverture immédiate de: {html_path}")
    
    # Essayer plusieurs méthodes pour être sûr que ça s'ouvre
    try:
        # Méthode 1: webbrowser (standard)
        webbrowser.open(f"file://{html_path}")
        print("✅ Ouvert avec webbrowser")
    except:
        pass
    
    try:
        # Méthode 2: Commande système Windows
        if os.name == 'nt':  # Windows
            os.startfile(str(html_path))
            print("✅ Ouvert avec startfile (Windows)")
    except:
        pass
    
    try:
        # Méthode 3: Subprocess pour Windows
        if os.name == 'nt':
            subprocess.run(['start', str(html_path)], shell=True)
            print("✅ Ouvert avec subprocess (Windows)")
    except:
        pass
    
    try:
        # Méthode 4: Pour Mac/Linux
        if os.name == 'posix':
            subprocess.run(['open', str(html_path)])  # Mac
            print("✅ Ouvert avec open (Mac)")
    except:
        try:
            subprocess.run(['xdg-open', str(html_path)])  # Linux
            print("✅ Ouvert avec xdg-open (Linux)")
        except:
            pass

def test_mini_sample_direct_html():
    """
    Test le pipeline et ouvre DIRECTEMENT la page HTML
    """
    print("🚀 TEST MINI-ÉCHANTILLON → OUVERTURE DIRECTE HTML")
    print("=" * 60)
    print("Ce test va:")
    print("• ✅ Faire le preprocessing (50 échantillons)")
    print("• ✅ Générer le rapport HTML")
    print("• 🚀 OUVRIR DIRECTEMENT la page dans votre navigateur")
    print("=" * 60)
    
    # Configuration pour mini test
    output_dir = "data/mini_test_direct"
    pipeline = MassivePreprocessingPipeline(
        output_dir=output_dir,
        use_multiprocessing=False,
        chunk_size=25
    )
    
    # Créer le dossier de sauvegarde
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print("\n🔄 Chargement des données...")
    
    from datasets import load_dataset
    
    start_time = time.time()
    train_dataset = load_dataset("fancyzhx/amazon_polarity", split="train[:50]")
    test_dataset = load_dataset("fancyzhx/amazon_polarity", split="test[:10]")
    
    print(f"✅ Données chargées en {time.time() - start_time:.1f}s")
    
    # Sauvegarder les données brutes rapidement
    raw_train = pd.DataFrame(train_dataset)
    raw_test = pd.DataFrame(test_dataset)
    raw_train.to_csv(f"{output_dir}/raw_train_backup.csv", index=False)
    raw_test.to_csv(f"{output_dir}/raw_test_backup.csv", index=False)
    
    print("\n🔧 Preprocessing en cours...")
    
    # Traitement rapide
    train_df = pipeline.process_dataset_split(train_dataset, 'mini_train')
    test_df = pipeline.process_dataset_split(test_dataset, 'mini_test')
    
    # Sauvegarder rapidement
    train_df.to_csv(f"{output_dir}/processed_train_backup.csv", index=False)
    test_df.to_csv(f"{output_dir}/processed_test_backup.csv", index=False)
    pipeline.save_processed_data(train_df, test_df)
    
    print("✅ Preprocessing terminé!")
    
    # Générer le rapport HTML IMMÉDIATEMENT
    print("\n🎨 Génération du rapport HTML...")
    
    try:
        from generate_html_report import HTMLReportGenerator
        
        generator = HTMLReportGenerator(output_dir)
        report_path = generator.generate_html_report("rapport_preprocessing.html")
        
        if report_path:
            print(f"✅ Rapport HTML créé: {report_path}")
            
            # OUVERTURE IMMÉDIATE
            print("\n🚀 OUVERTURE IMMÉDIATE DU RAPPORT HTML...")
            print("=" * 50)
            
            # Ouvrir immédiatement avec plusieurs méthodes
            open_html_immediately(report_path)
            
            print("=" * 50)
            print("🎉 LE RAPPORT DEVRAIT S'OUVRIR MAINTENANT!")
            print("=" * 50)
            
            # Afficher le chemin au cas où
            print(f"\n📁 Si ça ne s'ouvre pas automatiquement:")
            print(f"   Chemin: {Path(report_path).absolute()}")
            print(f"   Double-cliquez sur le fichier ou copiez le chemin dans votre navigateur")
            
        else:
            print("❌ Erreur lors de la génération du rapport HTML")
            
    except ImportError:
        print("❌ Plotly non installé. Installation...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
            print("✅ Plotly installé. Relancez le script.")
        except:
            print("❌ Installation échouée. Installez manuellement: pip install plotly")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Statistiques rapides
    total_errors = train_df['is_label_suspect'].sum() + test_df['is_label_suspect'].sum()
    compression_ratio = (1 - train_df['processed_length'].mean() / train_df['text_length'].mean()) * 100
    
    print(f"\n📊 RÉSUMÉ RAPIDE:")
    print(f"✅ {len(train_df)} + {len(test_df)} échantillons traités")
    print(f"✅ {len(train_df.columns)} features créées")
    print(f"✅ {compression_ratio:.1f}% compression moyenne")
    print(f"✅ {total_errors} erreurs détectées")
    
    return train_df, test_df

def main():
    """
    Lance le test avec ouverture directe HTML
    """
    try:
        print("🚀 LANCEMENT DU TEST AVEC OUVERTURE DIRECTE HTML")
        print("🎯 La page va s'ouvrir automatiquement dans votre navigateur!")
        print()
        
        train_df, test_df = test_mini_sample_direct_html()
        
        print(f"\n🎉 TEST TERMINÉ!")
        print(f"🌐 Le rapport HTML devrait être ouvert dans votre navigateur")
        print(f"📊 Consultez-le pour voir toutes les statistiques visuelles")
        
        # Petit délai pour laisser le temps au navigateur de s'ouvrir
        print(f"\n⏱️  Attente de 2 secondes pour l'ouverture du navigateur...")
        time.sleep(2)
        print(f"✅ Terminé!")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 