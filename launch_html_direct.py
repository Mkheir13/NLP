"""
Script pour lancer DIRECTEMENT la page HTML
"""

import os
import sys
import webbrowser
import subprocess
from pathlib import Path
import time

def open_html_now(html_path):
    """Ouvre IMMÉDIATEMENT le fichier HTML avec toutes les méthodes possibles"""
    html_path = Path(html_path).absolute()
    
    print(f"🚀 OUVERTURE IMMÉDIATE: {html_path.name}")
    print("=" * 50)
    
    success = False
    
    # Méthode 1: webbrowser (standard Python)
    try:
        webbrowser.open(f"file://{html_path}")
        print("✅ Méthode 1: webbrowser - OK")
        success = True
    except Exception as e:
        print(f"❌ Méthode 1: webbrowser - {e}")
    
    # Méthode 2: os.startfile (Windows)
    if os.name == 'nt':
        try:
            os.startfile(str(html_path))
            print("✅ Méthode 2: os.startfile (Windows) - OK")
            success = True
        except Exception as e:
            print(f"❌ Méthode 2: os.startfile - {e}")
    
    # Méthode 3: subprocess start (Windows)
    if os.name == 'nt':
        try:
            subprocess.run(['start', str(html_path)], shell=True, check=True)
            print("✅ Méthode 3: subprocess start (Windows) - OK")
            success = True
        except Exception as e:
            print(f"❌ Méthode 3: subprocess start - {e}")
    
    # Méthode 4: subprocess pour Mac/Linux
    if os.name == 'posix':
        try:
            # Mac
            subprocess.run(['open', str(html_path)], check=True)
            print("✅ Méthode 4: open (Mac) - OK")
            success = True
        except:
            try:
                # Linux
                subprocess.run(['xdg-open', str(html_path)], check=True)
                print("✅ Méthode 4: xdg-open (Linux) - OK")
                success = True
            except Exception as e:
                print(f"❌ Méthode 4: open/xdg-open - {e}")
    
    print("=" * 50)
    
    if success:
        print("🎉 AU MOINS UNE MÉTHODE A FONCTIONNÉ!")
        print("🌐 Votre navigateur devrait s'ouvrir maintenant...")
    else:
        print("❌ AUCUNE MÉTHODE N'A FONCTIONNÉ")
        print(f"📁 Ouvrez manuellement: {html_path}")
    
    return success

def find_existing_html():
    """Trouve un rapport HTML existant"""
    possible_paths = [
        "data/mini_test_html/rapport_preprocessing.html",
        "data/mini_test_visual/rapport_preprocessing.html", 
        "data/mini_test/rapport_preprocessing.html",
        "data/test_processed/rapport_preprocessing.html"
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            return path
    
    return None

def create_and_launch_html():
    """Crée rapidement un rapport HTML et l'ouvre"""
    print("🔄 Aucun rapport HTML trouvé. Création rapide...")
    
    # Essayer de créer à partir de données existantes
    try:
        from generate_html_report import HTMLReportGenerator
        
        # Chercher des données existantes
        data_dirs = ["data/mini_test_visual", "data/mini_test", "data/test_processed"]
        
        for data_dir in data_dirs:
            if Path(data_dir).exists() and Path(f"{data_dir}/processed_train_backup.csv").exists():
                print(f"✅ Données trouvées dans {data_dir}")
                
                generator = HTMLReportGenerator(data_dir)
                report_path = generator.generate_html_report("rapport_preprocessing.html")
                
                if report_path:
                    print(f"✅ Rapport créé: {report_path}")
                    return report_path
        
        # Si pas de données, faire un mini test rapide
        print("🚀 Aucune donnée trouvée. Mini test rapide...")
        import subprocess
        result = subprocess.run([sys.executable, "test_mini_sample_direct_html.py"], 
                              capture_output=False, text=True)
        
        # Chercher le rapport créé
        return find_existing_html()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return None

def main():
    """Fonction principale - Lance directement le HTML"""
    print("🚀 LANCEMENT DIRECT DE LA PAGE HTML")
    print("=" * 60)
    print("🎯 Objectif: Ouvrir immédiatement le rapport HTML dans votre navigateur")
    print("=" * 60)
    
    # 1. Chercher un rapport HTML existant
    html_path = find_existing_html()
    
    if html_path:
        print(f"✅ Rapport HTML trouvé: {html_path}")
        
        # Vérifier que le fichier n'est pas vide
        if Path(html_path).stat().st_size > 1000:  # Au moins 1KB
            print("✅ Le fichier semble valide")
            
            # Ouvrir immédiatement
            success = open_html_now(html_path)
            
            if success:
                print("\n🎉 SUCCÈS! Le rapport devrait s'ouvrir dans votre navigateur")
                print("📊 Vous pouvez maintenant voir toutes les statistiques visuelles")
            else:
                print(f"\n❌ Échec de l'ouverture automatique")
                print(f"📁 Ouvrez manuellement: {Path(html_path).absolute()}")
        else:
            print("❌ Le fichier semble corrompu ou vide")
            html_path = create_and_launch_html()
    else:
        print("❌ Aucun rapport HTML trouvé")
        html_path = create_and_launch_html()
    
    # Si on a créé un nouveau rapport, l'ouvrir
    if html_path and html_path != find_existing_html():
        print(f"\n🆕 Nouveau rapport créé: {html_path}")
        open_html_now(html_path)
    
    print("\n" + "=" * 60)
    print("✅ SCRIPT TERMINÉ")
    print("🌐 Votre rapport HTML devrait être ouvert maintenant!")
    print("=" * 60)

if __name__ == "__main__":
    main() 