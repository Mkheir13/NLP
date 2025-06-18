"""
Menu final des options de test avec rapport HTML
"""

def show_menu():
    """
    Affiche le menu final avec l'option HTML
    """
    print("🚀 MENU FINAL DES OPTIONS DE TEST - PIPELINE PREPROCESSING")
    print("=" * 80)
    print()
    print("📊 OPTIONS DISPONIBLES:")
    print()
    print("1️⃣  MINI TEST + RAPPORT HTML ⭐ **RECOMMANDÉ**")
    print("    📁 Commande: python test_mini_sample_with_html.py")
    print("    ⏱️  Durée: ~20 secondes")
    print("    💾 Sortie: data/mini_test_html/ + rapport HTML")
    print("    🎯 Objectif: Test complet avec rapport visuel moderne")
    print("    ✨ NOUVEAU: Interface web épurée et moderne")
    print()
    print("2️⃣  MINI TEST VISUEL (ligne de commande)")
    print("    📁 Commande: python test_mini_sample_visual.py")
    print("    ⏱️  Durée: ~15 secondes")
    print("    💾 Sortie: data/mini_test_visual/")
    print("    🎯 Objectif: Explications détaillées en console")
    print()
    print("3️⃣  GÉNÉRER RAPPORT HTML (depuis données existantes)")
    print("    📁 Commande: python generate_html_report.py")
    print("    ⏱️  Durée: ~3 secondes")
    print("    🎯 Objectif: Créer un rapport HTML à partir de données existantes")
    print()
    print("4️⃣  MINI TEST SIMPLE")
    print("    📁 Commande: python test_mini_sample.py")
    print("    ⏱️  Durée: ~10 secondes")
    print("    🎯 Objectif: Test rapide basique")
    print()
    print("5️⃣  TEST MOYEN (10,000 échantillons)")
    print("    📁 Commande: python test_massive_pipeline.py")
    print("    ⏱️  Durée: ~2-3 minutes")
    print("    🎯 Objectif: Validation sur échantillon représentatif")
    print()
    print("6️⃣  PREPROCESSING COMPLET (4,000,000 échantillons)")
    print("    📁 Commande: python run_full_preprocessing.py")
    print("    ⏱️  Durée: ~2-3 heures")
    print("    🎯 Objectif: Traitement complet pour production")
    print()
    print("🔧 PROGRESSION RECOMMANDÉE:")
    print("-" * 50)
    print("1. ✨ MINI TEST + RAPPORT HTML (pour découvrir)")
    print("2. 🔧 TEST MOYEN (si satisfait)")
    print("3. 💪 PREPROCESSING COMPLET (pour production)")
    print()
    print("🎨 AVANTAGES DU RAPPORT HTML:")
    print("-" * 50)
    print("✅ Interface moderne et épurée")
    print("✅ Graphiques interactifs (Plotly)")
    print("✅ Histogrammes visuels colorés")
    print("✅ Analyse de sentiment en graphiques")
    print("✅ Exemples de preprocessing avec comparaisons")
    print("✅ Détection d'erreurs avec explications visuelles")
    print("✅ Statistiques complètes en cartes")
    print("✅ Design responsive (mobile-friendly)")
    print("✅ Ouverture automatique dans le navigateur")
    print()
    print("📋 CE QUE CONTIENT LE RAPPORT HTML:")
    print("-" * 50)
    print("🎯 Statistiques principales en cartes colorées")
    print("📊 Graphiques en secteurs pour les distributions")
    print("📏 Histogrammes des longueurs de texte")
    print("🎭 Scatter plot de l'analyse de sentiment")
    print("⚡ Graphique d'efficacité de compression")
    print("🚨 Analyse visuelle des erreurs détectées")
    print("🔍 Exemples de preprocessing avant/après")
    print("📋 Résumé des features créées")
    print("🎯 Recommandations pour la suite")
    print()

def show_html_preview():
    """
    Montre un aperçu de ce que contient le rapport HTML
    """
    print("🎨 APERÇU DU RAPPORT HTML:")
    print("=" * 80)
    print()
    print("📱 DESIGN MODERNE:")
    print("  • Interface épurée avec dégradé de couleurs")
    print("  • Cartes avec ombres et animations au survol")
    print("  • Typographie moderne (Segoe UI)")
    print("  • Design responsive pour tous les écrans")
    print()
    print("📊 GRAPHIQUES INTERACTIFS:")
    print("  • Camemberts pour la distribution des labels")
    print("  • Histogrammes colorés des longueurs")
    print("  • Scatter plot interactif sentiment/polarité")
    print("  • Graphique de compression avec colormap")
    print("  • Barres d'erreurs avec tooltips")
    print()
    print("🎯 SECTIONS PRINCIPALES:")
    print("  1. En-tête avec statistiques clés")
    print("  2. Distribution des labels (graphiques)")
    print("  3. Analyse des longueurs de texte")
    print("  4. Analyse de sentiment interactive")
    print("  5. Efficacité de compression")
    print("  6. Erreurs détectées avec explications")
    print("  7. Exemples de preprocessing détaillés")
    print("  8. Résumé des features créées")
    print("  9. Recommandations personnalisées")
    print()
    print("🎨 COULEURS ET STYLE:")
    print("  • Palette moderne: bleu (#4ecdc4), orange (#feca57)")
    print("  • Rouge (#ff6b6b) pour les erreurs")
    print("  • Fond avec dégradé violet-bleu")
    print("  • Cartes blanches semi-transparentes")
    print("  • Animations fluides et transitions")
    print()

def main():
    """
    Affiche le menu et gère les choix
    """
    show_menu()
    show_html_preview()
    
    print("❓ QUE VOULEZ-VOUS FAIRE ?")
    print("-" * 50)
    print("1 - ✨ Mini test + Rapport HTML (RECOMMANDÉ)")
    print("2 - 📊 Mini test visuel (ligne de commande)")
    print("3 - 🎨 Générer rapport HTML seulement")
    print("4 - 🚀 Mini test simple")
    print("5 - 🔧 Test moyen (10k échantillons)")
    print("6 - 💪 Preprocessing complet (4M échantillons)")
    print("7 - 📋 Afficher ce menu")
    print("8 - 🎨 Voir l'aperçu HTML")
    print("0 - 👋 Quitter")
    print()
    
    while True:
        choice = input("Votre choix (0-8): ").strip()
        
        if choice == "0":
            print("👋 Au revoir !")
            break
        elif choice == "1":
            print("✨ Lancement du mini test avec rapport HTML...")
            print("🎯 Vous allez voir le preprocessing + un rapport web moderne!")
            print("🚀 Installation automatique de plotly si nécessaire...")
            import subprocess
            subprocess.run(["python", "test_mini_sample_with_html.py"])
            break
        elif choice == "2":
            print("📊 Lancement du mini test visuel (ligne de commande)...")
            import subprocess
            subprocess.run(["python", "test_mini_sample_visual.py"])
            break
        elif choice == "3":
            print("🎨 Génération du rapport HTML à partir des données existantes...")
            import subprocess
            subprocess.run(["python", "generate_html_report.py"])
            break
        elif choice == "4":
            print("🚀 Lancement du mini test simple...")
            print("💡 Conseil: L'option 1 (HTML) est plus visuelle!")
            import subprocess
            subprocess.run(["python", "test_mini_sample.py"])
            break
        elif choice == "5":
            print("🔧 Lancement du test moyen...")
            print("⏱️  Cela prendra environ 2-3 minutes...")
            import subprocess
            subprocess.run(["python", "test_massive_pipeline.py"])
            break
        elif choice == "6":
            print("⚠️  ATTENTION: Le preprocessing complet peut prendre 2-3 heures!")
            print("💡 Assurez-vous d'avoir testé les options plus petites d'abord.")
            confirm = input("Êtes-vous sûr ? (oui/non): ").strip().lower()
            if confirm in ["oui", "o", "yes", "y"]:
                print("💪 Lancement du preprocessing complet...")
                import subprocess
                subprocess.run(["python", "run_full_preprocessing.py"])
            else:
                print("❌ Annulé - Bonne décision! Testez d'abord l'option 1.")
            break
        elif choice == "7":
            show_menu()
        elif choice == "8":
            show_html_preview()
        else:
            print("❌ Choix invalide. Veuillez choisir entre 0 et 8.")
            print("💡 Conseil: Choisissez 1 pour le test avec rapport HTML (recommandé)")

if __name__ == "__main__":
    main() 