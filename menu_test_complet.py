"""
Menu complet des options de test pour le pipeline de preprocessing
"""

def show_menu():
    """
    Affiche le menu complet des options de test
    """
    print("🚀 MENU COMPLET DES OPTIONS DE TEST - PIPELINE PREPROCESSING")
    print("=" * 80)
    print()
    print("📊 OPTIONS DISPONIBLES:")
    print()
    print("1️⃣  MINI TEST SIMPLE (50 échantillons)")
    print("    📁 Commande: python test_mini_sample.py")
    print("    ⏱️  Durée: ~10 secondes")
    print("    💾 Sortie: data/mini_test/")
    print("    🎯 Objectif: Test rapide basique")
    print()
    print("2️⃣  MINI TEST VISUEL (50 échantillons + explications détaillées)")
    print("    📁 Commande: python test_mini_sample_visual.py")
    print("    ⏱️  Durée: ~15 secondes")
    print("    💾 Sortie: data/mini_test_visual/")
    print("    🎯 Objectif: Comprendre le preprocessing en détail")
    print("    ✨ RECOMMANDÉ pour débuter")
    print()
    print("3️⃣  ANALYSE DES RÉSULTATS")
    print("    📁 Commande: python analyze_mini_results.py")
    print("    ⏱️  Durée: ~2 secondes")
    print("    🎯 Objectif: Analyser les résultats des mini tests")
    print()
    print("4️⃣  TEST MOYEN (10,000 échantillons)")
    print("    📁 Commande: python test_massive_pipeline.py")
    print("    ⏱️  Durée: ~2-3 minutes")
    print("    💾 Sortie: data/test_processed/")
    print("    🎯 Objectif: Test sur échantillon représentatif")
    print()
    print("5️⃣  PREPROCESSING COMPLET (4,000,000 échantillons)")
    print("    📁 Commande: python run_full_preprocessing.py")
    print("    ⏱️  Durée: ~2-3 heures")
    print("    💾 Sortie: data/processed_full/")
    print("    🎯 Objectif: Traitement complet du dataset")
    print()
    print("🔧 PROGRESSION RECOMMANDÉE:")
    print("-" * 50)
    print("1. ✨ MINI TEST VISUEL (pour comprendre)")
    print("2. 📊 ANALYSE DES RÉSULTATS (pour vérifier)")
    print("3. 🚀 TEST MOYEN (si satisfait)")
    print("4. 💪 PREPROCESSING COMPLET (pour production)")
    print()
    print("💡 AVANTAGES DU MINI TEST VISUEL:")
    print("-" * 50)
    print("✅ Explications détaillées de chaque étape")
    print("✅ Histogrammes visuels des distributions")
    print("✅ Exemples avant/après preprocessing")
    print("✅ Analyse des erreurs avec explications")
    print("✅ Statistiques de compression du texte")
    print("✅ Analyse de sentiment visualisée")
    print("✅ Détection et explication des erreurs")
    print("✅ Recommandations pour la suite")
    print()
    print("📋 CE QUE VOUS APPRENDREZ:")
    print("-" * 50)
    print("🔍 Comment le texte est nettoyé et transformé")
    print("📊 Quelles features sont extraites et pourquoi")
    print("🎭 Comment l'analyse de sentiment fonctionne")
    print("🚨 Comment les erreurs de labels sont détectées")
    print("📈 Distribution des données dans votre échantillon")
    print("⚡ Performance du pipeline de preprocessing")
    print()
    print("🎯 FICHIERS CRÉÉS PAR LE MINI TEST VISUEL:")
    print("-" * 50)
    print("📁 data/mini_test_visual/")
    print("  • raw_train_backup.csv       (données originales)")
    print("  • processed_train_backup.csv (données transformées)")
    print("  • *.parquet, *.pkl           (formats optimisés)")
    print("  • processing_summary.json    (statistiques)")
    print("  • processing_stats.json      (métriques)")
    print()

def show_comparison():
    """
    Montre la comparaison entre les options
    """
    print("📊 COMPARAISON DES OPTIONS:")
    print("=" * 80)
    print()
    print("┌─────────────────┬──────────┬──────────┬────────────┬─────────────┐")
    print("│ Option          │ Durée    │ Échant.  │ Explications│ Recommandé  │")
    print("├─────────────────┼──────────┼──────────┼────────────┼─────────────┤")
    print("│ Mini Simple     │ 10s      │ 50       │ Basiques   │ Test rapide │")
    print("│ Mini Visuel     │ 15s      │ 50       │ Détaillées │ ✅ Débuter   │")
    print("│ Analyse         │ 2s       │ -        │ Moyennes   │ Vérifier    │")
    print("│ Test Moyen      │ 3min     │ 10,000   │ Basiques   │ Validation  │")
    print("│ Complet         │ 3h       │ 4M       │ Basiques   │ Production  │")
    print("└─────────────────┴──────────┴──────────┴────────────┴─────────────┘")
    print()

def show_visual_examples():
    """
    Montre des exemples de ce que produit le test visuel
    """
    print("🎨 EXEMPLES DE VISUELS PRODUITS:")
    print("=" * 80)
    print()
    print("📊 DISTRIBUTION DES LABELS:")
    print("  TRAIN:")
    print("    Positifs: ████████████████ 27 (54.0%)")
    print("    Négatifs: ██████████████ 23 (46.0%)")
    print()
    print("📏 HISTOGRAMME DES LONGUEURS:")
    print("    100-200: ████████  8")
    print("    200-300: ████████████ 12")
    print("    300-400: ████████████████ 16")
    print("    400-500: ████████████ 12")
    print("    500+:    ██  2")
    print()
    print("🎭 ANALYSE DE SENTIMENT:")
    print("    Très négatif: ███  3")
    print("    Négatif:      ████  4")
    print("    Neutre:       ████████████ 12")
    print("    Positif:      ████████████████ 16")
    print("    Très positif: ███████████████ 15")
    print()
    print("🔍 EXEMPLE DE TRANSFORMATION:")
    print("  📝 AVANT:  'This Product is AMAZING!!! I love it so much!!!'")
    print("  ✨ APRÈS: 'product amazing love much'")
    print("  📊 STATS: 47 → 23 chars (51% compression)")
    print()

def main():
    """
    Affiche le menu et demande à l'utilisateur ce qu'il veut faire
    """
    show_menu()
    show_comparison()
    show_visual_examples()
    
    print("❓ QUE VOULEZ-VOUS FAIRE ?")
    print("-" * 40)
    print("1 - 🚀 Mini test simple (50 échantillons)")
    print("2 - ✨ Mini test visuel (RECOMMANDÉ)")
    print("3 - 📊 Analyser les résultats")
    print("4 - 🔧 Test moyen (10k échantillons)")
    print("5 - 💪 Preprocessing complet (4M échantillons)")
    print("6 - 📋 Afficher ce menu")
    print("7 - 🎨 Voir les exemples visuels")
    print("0 - 👋 Quitter")
    print()
    
    while True:
        choice = input("Votre choix (0-7): ").strip()
        
        if choice == "0":
            print("👋 Au revoir !")
            break
        elif choice == "1":
            print("🚀 Lancement du mini test simple...")
            print("💡 Conseil: Le test visuel (option 2) est plus informatif!")
            import subprocess
            subprocess.run(["python", "test_mini_sample.py"])
            break
        elif choice == "2":
            print("✨ Lancement du mini test visuel (RECOMMANDÉ)...")
            print("🎯 Vous allez voir des explications détaillées!")
            import subprocess
            subprocess.run(["python", "test_mini_sample_visual.py"])
            break
        elif choice == "3":
            print("📊 Analyse des résultats...")
            import subprocess
            subprocess.run(["python", "analyze_mini_results.py"])
            break
        elif choice == "4":
            print("🔧 Lancement du test moyen...")
            print("⏱️  Cela prendra environ 2-3 minutes...")
            import subprocess
            subprocess.run(["python", "test_massive_pipeline.py"])
            break
        elif choice == "5":
            print("⚠️  ATTENTION: Le preprocessing complet peut prendre 2-3 heures!")
            print("💡 Assurez-vous d'avoir testé les options plus petites d'abord.")
            confirm = input("Êtes-vous sûr ? (oui/non): ").strip().lower()
            if confirm in ["oui", "o", "yes", "y"]:
                print("💪 Lancement du preprocessing complet...")
                import subprocess
                subprocess.run(["python", "run_full_preprocessing.py"])
            else:
                print("❌ Annulé - Bonne décision! Testez d'abord les options plus petites.")
            break
        elif choice == "6":
            show_menu()
            show_comparison()
        elif choice == "7":
            show_visual_examples()
        else:
            print("❌ Choix invalide. Veuillez choisir entre 0 et 7.")
            print("💡 Conseil: Choisissez 2 pour le test visuel (recommandé)")

if __name__ == "__main__":
    main() 