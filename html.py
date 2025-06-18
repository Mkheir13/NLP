"""
Script ultra-simple: lance directement la page HTML
Utilisation: python html.py
"""

import os
import webbrowser
import subprocess
from pathlib import Path

def main():
    """Lance immédiatement la page HTML"""
    
    # Chercher le rapport HTML
    paths = [
        "data/mini_test_html/rapport_preprocessing.html",
        "data/mini_test_visual/rapport_preprocessing.html", 
        "data/mini_test/rapport_preprocessing.html"
    ]
    
    html_path = None
    for path in paths:
        if Path(path).exists():
            html_path = Path(path).absolute()
            break
    
    if html_path:
        print(f"🚀 Ouverture: {html_path.name}")
        
        # Ouvrir avec toutes les méthodes
        try:
            webbrowser.open(f"file://{html_path}")
        except:
            pass
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(str(html_path))
        except:
            pass
        
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['start', str(html_path)], shell=True)
        except:
            pass
        
        print("✅ Ouvert dans votre navigateur!")
    else:
        print("❌ Aucun rapport trouvé")
        print("💡 Lancez d'abord: python test_mini_sample_with_html.py")

if __name__ == "__main__":
    main() 