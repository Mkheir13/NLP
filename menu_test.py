"""
Menu des options de test pour le pipeline de preprocessing
"""

def show_menu():
    """
    Affiche le menu des options de test
    """
    print("🚀 MENU DES OPTIONS DE TEST - PIPELINE PREPROCESSING")
    print("=" * 70)
    print()
    print("📊 OPTIONS DISPONIBLES:")
    print()
    print("1️⃣  MINI TEST (50 échantillons + tables de sauvegarde)")
    print("    📁 Commande: python test_mini_sample.py")
    print("    ⏱️  Durée: ~10 secondes")
    print("    💾 Sortie: data/mini_test/")
    print("    🎯 Objectif: Vérifier que le pipeline fonctionne")
    print()
    print("2️⃣  ANALYSE DU MINI TEST")
    print("    📁 Commande: python analyze_mini_results.py")
    print("    ⏱️  Durée: ~2 secondes")
    print("    🎯 Objectif: Analyser les résultats du mini test")
    print()
    print("3️⃣  TEST MOYEN (10,000 échantillons)")
    print("    📁 Commande: python test_massive_pipeline.py")
    print("    ⏱️  Durée: ~2-3 minutes")
    print("    💾 Sortie: data/test_processed/")
    print("    🎯 Objectif: Test sur échantillon représentatif")
    print()
    print("4️⃣  PREPROCESSING COMPLET (4,000,000 échantillons)")
    print("    📁 Commande: python run_full_preprocessing.py")
    print("    ⏱️  Durée: ~2-3 heures")
    print("    💾 Sortie: data/processed_full/")
    print("    🎯 Objectif: Traitement complet du dataset")
    print()
    print("🔧 PROGRESSION RECOMMANDÉE:")
    print("-" * 40)
    print("1. Commencer par le MINI TEST pour vérifier")
    print("2. Analyser les résultats avec l'analyse")
    print("3. Si satisfait, passer au TEST MOYEN")
    print("4. Enfin, lancer le PREPROCESSING COMPLET")
    print()
    print("💡 AVANTAGES DU MINI TEST:")
    print("-" * 40)
    print("✅ Très rapide (10 secondes)")
    print("✅ Tables de sauvegarde multiples")
    print("✅ Analyse détaillée des résultats")
    print("✅ Détection des erreurs de pipeline")
    print("✅ Validation des features créées")
    print("✅ Exemples de preprocessing visibles")
    print("✅ Statistiques complètes")
    print()
    print("📋 FICHIERS CRÉÉS PAR LE MINI TEST:")
    print("-" * 40)
    print("• raw_train_backup.csv       (données originales)")
    print("• raw_test_backup.csv        (données originales)")
    print("• processed_train_backup.csv (données preprocessées)")
    print("• processed_test_backup.csv  (données preprocessées)")
    print("• *.parquet                  (format optimisé)")
    print("• *.pkl                      (format pickle)")
    print("• processing_summary.json    (résumé du traitement)")
    print("• detailed_analysis.json     (analyse détaillée)")
    print("• processing_stats.json      (statistiques)")
    print()
    print("🎯 INFORMATIONS IMPORTANTES:")
    print("-" * 40)
    print("• Le mini test utilise seulement 50 échantillons train + 10 test")
    print("• Toutes les sauvegardes sont créées automatiquement")
    print("• Le système détecte les erreurs de labels automatiquement")
    print("• Ratio de compression ~39% (très efficace)")
    print("• 20 features créées par échantillon")
    print("• Multiprocessing désactivé pour le mini test")
    print()

def main():
    """
    Affiche le menu et demande à l'utilisateur ce qu'il veut faire
    """
    show_menu()
    
    print("❓ QUE VOULEZ-VOUS FAIRE ?")
    print("-" * 30)
    print("1 - Mini test (50 échantillons)")
    print("2 - Analyser mini test")
    print("3 - Test moyen (10k échantillons)")
    print("4 - Preprocessing complet (4M échantillons)")
    print("5 - Afficher ce menu")
    print("0 - Quitter")
    print()
    
    while True:
        choice = input("Votre choix (0-5): ").strip()
        
        if choice == "0":
            print("👋 Au revoir !")
            break
        elif choice == "1":
            print("🚀 Lancement du mini test...")
            import subprocess
            subprocess.run(["python", "test_mini_sample.py"])
            break
        elif choice == "2":
            print("🔍 Analyse du mini test...")
            import subprocess
            subprocess.run(["python", "analyze_mini_results.py"])
            break
        elif choice == "3":
            print("🚀 Lancement du test moyen...")
            import subprocess
            subprocess.run(["python", "test_massive_pipeline.py"])
            break
        elif choice == "4":
            print("⚠️  ATTENTION: Le preprocessing complet peut prendre 2-3 heures!")
            confirm = input("Êtes-vous sûr ? (oui/non): ").strip().lower()
            if confirm in ["oui", "o", "yes", "y"]:
                print("🚀 Lancement du preprocessing complet...")
                import subprocess
                subprocess.run(["python", "run_full_preprocessing.py"])
            else:
                print("❌ Annulé")
            break
        elif choice == "5":
            show_menu()
        else:
            print("❌ Choix invalide. Veuillez choisir entre 0 et 5.")

if __name__ == "__main__":
    main() 