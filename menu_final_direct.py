"""
Menu final avec lancement DIRECT de la page HTML
"""

def show_menu():
    """
    Affiche le menu final avec l'option de lancement direct HTML
    """
    print("🚀 MENU FINAL - LANCEMENT DIRECT HTML")
    print("=" * 70)
    print()
    print("📊 OPTIONS DISPONIBLES:")
    print()
    print("1️⃣  🌐 LANCER LA PAGE HTML DIRECTEMENT ⭐ **ULTRA-RECOMMANDÉ**")
    print("    📁 Commande: python launch_html_direct.py")
    print("    ⏱️  Durée: ~2 secondes")
    print("    🎯 Objectif: Ouvrir immédiatement le rapport dans votre navigateur")
    print("    ✨ DIRECT: Trouve et ouvre automatiquement le rapport HTML")
    print()
    print("2️⃣  🧪 MINI TEST + RAPPORT HTML (complet)")
    print("    📁 Commande: python test_mini_sample_direct_html.py")
    print("    ⏱️  Durée: ~20 secondes")
    print("    🎯 Objectif: Preprocessing + Génération + Ouverture automatique")
    print()
    print("3️⃣  📊 MINI TEST VISUEL (ligne de commande)")
    print("    📁 Commande: python test_mini_sample_visual.py")
    print("    ⏱️  Durée: ~15 secondes")
    print("    🎯 Objectif: Explications détaillées en console")
    print()
    print("4️⃣  🎨 GÉNÉRER RAPPORT HTML SEULEMENT")
    print("    📁 Commande: python generate_html_report.py")
    print("    ⏱️  Durée: ~3 secondes")
    print("    🎯 Objectif: Créer un rapport à partir de données existantes")
    print()
    print("5️⃣  🚀 MINI TEST SIMPLE")
    print("    📁 Commande: python test_mini_sample.py")
    print("    ⏱️  Durée: ~10 secondes")
    print("    🎯 Objectif: Test rapide basique")
    print()
    print("6️⃣  🔧 TEST MOYEN (10,000 échantillons)")
    print("    📁 Commande: python test_massive_pipeline.py")
    print("    ⏱️  Durée: ~2-3 minutes")
    print("    🎯 Objectif: Validation sur échantillon représentatif")
    print()
    print("🔧 PROGRESSION ULTRA-SIMPLE:")
    print("-" * 50)
    print("1. 🌐 LANCER LA PAGE HTML DIRECTEMENT (pour voir immédiatement)")
    print("2. 🧪 Mini test complet (si pas de données existantes)")
    print("3. 🔧 Test moyen (si satisfait)")
    print()
    print("💡 POURQUOI CHOISIR L'OPTION 1 ?")
    print("-" * 50)
    print("✅ IMMÉDIAT: S'ouvre en 2 secondes")
    print("✅ INTELLIGENT: Trouve automatiquement le rapport existant")
    print("✅ MULTI-MÉTHODE: 3 techniques d'ouverture pour garantir le succès")
    print("✅ FALLBACK: Crée un rapport si aucun n'existe")
    print("✅ ZERO EFFORT: Juste cliquer et regarder")
    print()
    print("🎨 CE QUE VOUS VERREZ DANS LE RAPPORT HTML:")
    print("-" * 50)
    print("📊 Graphiques interactifs colorés (Plotly)")
    print("🎯 Statistiques en cartes modernes")
    print("📏 Histogrammes des longueurs de texte")
    print("🎭 Analyse de sentiment visualisée")
    print("⚡ Efficacité de compression en graphique")
    print("🚨 Erreurs détectées avec explications")
    print("🔍 Exemples de preprocessing avant/après")
    print("📋 Résumé professionnel des features")
    print()

def show_direct_launch_info():
    """
    Montre les détails du lancement direct
    """
    print("🌐 LANCEMENT DIRECT HTML - DÉTAILS:")
    print("=" * 70)
    print()
    print("🎯 FONCTIONNEMENT:")
    print("  1. 🔍 Cherche un rapport HTML existant")
    print("  2. ✅ Vérifie que le fichier est valide")
    print("  3. 🚀 Ouvre avec 3 méthodes différentes:")
    print("     • webbrowser (Python standard)")
    print("     • os.startfile (Windows natif)")
    print("     • subprocess (commande système)")
    print("  4. 🎉 Succès garanti sur Windows!")
    print()
    print("📁 RAPPORTS RECHERCHÉS:")
    print("  • data/mini_test_html/rapport_preprocessing.html")
    print("  • data/mini_test_visual/rapport_preprocessing.html")
    print("  • data/mini_test/rapport_preprocessing.html")
    print("  • data/test_processed/rapport_preprocessing.html")
    print()
    print("🆘 SI AUCUN RAPPORT TROUVÉ:")
    print("  • Création automatique à partir de données existantes")
    print("  • Ou lancement d'un mini test rapide")
    print("  • Puis ouverture immédiate du nouveau rapport")
    print()
    print("⚡ AVANTAGES:")
    print("  ✅ Ultra-rapide (2 secondes)")
    print("  ✅ Intelligent (trouve automatiquement)")
    print("  ✅ Robuste (3 méthodes d'ouverture)")
    print("  ✅ Fallback (crée si nécessaire)")
    print("  ✅ Zero configuration")
    print()

def main():
    """
    Affiche le menu et gère les choix
    """
    show_menu()
    show_direct_launch_info()
    
    print("❓ QUE VOULEZ-VOUS FAIRE ?")
    print("-" * 60)
    print("1 - 🌐 LANCER LA PAGE HTML DIRECTEMENT (ULTRA-RECOMMANDÉ)")
    print("2 - 🧪 Mini test + Rapport HTML complet")
    print("3 - 📊 Mini test visuel (ligne de commande)")
    print("4 - 🎨 Générer rapport HTML seulement")
    print("5 - 🚀 Mini test simple")
    print("6 - 🔧 Test moyen (10k échantillons)")
    print("7 - 📋 Afficher ce menu")
    print("8 - 🌐 Voir détails lancement direct")
    print("0 - 👋 Quitter")
    print()
    
    while True:
        choice = input("Votre choix (0-8): ").strip()
        
        if choice == "0":
            print("👋 Au revoir !")
            break
        elif choice == "1":
            print("🌐 LANCEMENT DIRECT DE LA PAGE HTML...")
            print("🚀 Ouverture immédiate dans votre navigateur!")
            print("⏱️  Cela ne prendra que 2 secondes...")
            import subprocess
            subprocess.run(["python", "launch_html_direct.py"])
            break
        elif choice == "2":
            print("🧪 Lancement du mini test avec rapport HTML...")
            print("🎯 Preprocessing + Génération + Ouverture automatique!")
            import subprocess
            subprocess.run(["python", "test_mini_sample_direct_html.py"])
            break
        elif choice == "3":
            print("📊 Lancement du mini test visuel (ligne de commande)...")
            import subprocess
            subprocess.run(["python", "test_mini_sample_visual.py"])
            break
        elif choice == "4":
            print("🎨 Génération du rapport HTML seulement...")
            import subprocess
            subprocess.run(["python", "generate_html_report.py"])
            break
        elif choice == "5":
            print("🚀 Lancement du mini test simple...")
            print("💡 Conseil: L'option 1 (HTML direct) est plus visuelle!")
            import subprocess
            subprocess.run(["python", "test_mini_sample.py"])
            break
        elif choice == "6":
            print("🔧 Lancement du test moyen...")
            print("⏱️  Cela prendra environ 2-3 minutes...")
            import subprocess
            subprocess.run(["python", "test_massive_pipeline.py"])
            break
        elif choice == "7":
            show_menu()
        elif choice == "8":
            show_direct_launch_info()
        else:
            print("❌ Choix invalide. Veuillez choisir entre 0 et 8.")
            print("💡 Conseil: Choisissez 1 pour voir immédiatement le rapport HTML!")

if __name__ == "__main__":
    main() 