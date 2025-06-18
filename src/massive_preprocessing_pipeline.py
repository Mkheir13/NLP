"""
Pipeline de preprocessing massif pour l'intégralité du dataset Amazon Polarity
Optimisé pour traiter 4 millions d'échantillons efficacement
"""

import pandas as pd
import numpy as np
from datasets import load_dataset
import logging
import time
import gc
import os
from pathlib import Path
from typing import Dict, List, Optional
import pickle
import json
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

from text_preprocessor import AdvancedTextPreprocessor
from label_cleaner import LabelCleaner

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('preprocessing_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MassivePreprocessingPipeline:
    """
    Pipeline optimisé pour le preprocessing massif du dataset Amazon Polarity
    """
    
    def __init__(self, 
                 output_dir: str = "../data/processed_full",
                 use_multiprocessing: bool = True,
                 n_workers: int = None,
                 chunk_size: int = 50000):
        """
        Initialise le pipeline
        
        Args:
            output_dir: Répertoire de sortie
            use_multiprocessing: Utiliser le multiprocessing
            n_workers: Nombre de workers (None = auto)
            chunk_size: Taille des chunks pour le traitement
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.use_multiprocessing = use_multiprocessing
        self.n_workers = n_workers or max(1, mp.cpu_count() - 1)
        self.chunk_size = chunk_size
        
        # Initialiser les outils
        self.preprocessor = AdvancedTextPreprocessor(use_spacy=False)  # spaCy plus lent
        self.label_cleaner = LabelCleaner()
        
        # Statistiques
        self.stats = {
            'total_processed': 0,
            'errors_detected': 0,
            'processing_time': 0,
            'chunks_processed': 0
        }
        
        logger.info(f"Pipeline initialisé:")
        logger.info(f"  - Output dir: {self.output_dir}")
        logger.info(f"  - Multiprocessing: {self.use_multiprocessing}")
        logger.info(f"  - Workers: {self.n_workers}")
        logger.info(f"  - Chunk size: {self.chunk_size}")
    
    def load_full_dataset(self) -> Dict:
        """
        Charge l'intégralité du dataset Amazon Polarity
        """
        logger.info("🔄 Chargement de l'intégralité du dataset Amazon Polarity...")
        start_time = time.time()
        
        try:
            # Charger le dataset complet
            dataset = load_dataset("fancyzhx/amazon_polarity")
            
            load_time = time.time() - start_time
            logger.info(f"✅ Dataset chargé en {load_time:.1f}s")
            logger.info(f"  - Train: {len(dataset['train']):,} échantillons")
            logger.info(f"  - Test: {len(dataset['test']):,} échantillons")
            logger.info(f"  - Total: {len(dataset['train']) + len(dataset['test']):,} échantillons")
            
            return dataset
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement: {e}")
            raise
    
    def process_chunk(self, chunk_data: List[Dict], chunk_id: int) -> Dict:
        """
        Traite un chunk de données
        
        Args:
            chunk_data: Liste des échantillons à traiter
            chunk_id: ID du chunk
            
        Returns:
            Dictionnaire avec les résultats du chunk
        """
        logger.info(f"🔄 Traitement du chunk {chunk_id} ({len(chunk_data)} échantillons)...")
        
        results = []
        errors_in_chunk = 0
        
        for i, sample in enumerate(chunk_data):
            try:
                # Créer le texte combiné
                combined_text = sample['title'] + " " + sample['content']
                
                # Preprocessing complet
                processed_text = self.preprocessor.preprocess_text(
                    combined_text,
                    full_pipeline=True,
                    return_string=True
                )
                
                # Extraction de features
                features = self.preprocessor.extract_features(combined_text)
                
                # Détection d'erreurs de label
                textblob_analysis = self.label_cleaner.analyze_sentiment_textblob(combined_text)
                keyword_analysis = self.label_cleaner.analyze_keywords(combined_text)
                
                # Déterminer si le label est suspect
                actual_label = sample['label']
                is_label_suspect = False
                suspect_reason = ""
                
                # Critères de suspicion
                polarity = textblob_analysis['polarity']
                if actual_label == 1 and polarity < -0.3:  # Positif mais très négatif
                    is_label_suspect = True
                    suspect_reason = f"Positif mais polarité {polarity:.3f}"
                elif actual_label == 0 and polarity > 0.3:  # Négatif mais très positif
                    is_label_suspect = True
                    suspect_reason = f"Négatif mais polarité {polarity:.3f}"
                
                # Ajouter critère par mots-clés
                if actual_label == 1 and keyword_analysis['negative_keywords'] >= 2:
                    is_label_suspect = True
                    suspect_reason += f" + {keyword_analysis['negative_keywords']} mots négatifs"
                
                if is_label_suspect:
                    errors_in_chunk += 1
                
                # Compiler les résultats
                result = {
                    # Données originales
                    'title': sample['title'],
                    'content': sample['content'],
                    'label': actual_label,
                    'combined_text': combined_text,
                    
                    # Données preprocessées
                    'processed_text': processed_text,
                    
                    # Features de base
                    'text_length': len(combined_text),
                    'processed_length': len(processed_text),
                    'word_count': features['word_count'],
                    'sentence_count': features['sentence_count'],
                    
                    # Features avancées
                    'polarity': features['polarity'],
                    'subjectivity': features['subjectivity'],
                    'exclamation_count': features['exclamation_count'],
                    'question_count': features['question_count'],
                    'upper_case_ratio': features['upper_case_ratio'],
                    'punctuation_ratio': features['punctuation_ratio'],
                    'unique_word_ratio': features['unique_word_ratio'],
                    
                    # Détection d'erreurs
                    'is_label_suspect': is_label_suspect,
                    'suspect_reason': suspect_reason,
                    'suggested_label': textblob_analysis['predicted_label'] if is_label_suspect else actual_label,
                    'confidence_score': abs(polarity)
                }
                
                results.append(result)
                
            except Exception as e:
                logger.warning(f"Erreur lors du traitement de l'échantillon {i} du chunk {chunk_id}: {e}")
                continue
        
        logger.info(f"✅ Chunk {chunk_id} traité: {len(results)} échantillons, {errors_in_chunk} erreurs détectées")
        
        return {
            'chunk_id': chunk_id,
            'results': results,
            'errors_detected': errors_in_chunk,
            'processed_count': len(results)
        }
    
    def process_dataset_split(self, dataset_split, split_name: str) -> pd.DataFrame:
        """
        Traite un split du dataset (train ou test)
        
        Args:
            dataset_split: Split du dataset à traiter
            split_name: Nom du split ('train' ou 'test')
            
        Returns:
            DataFrame preprocessé
        """
        logger.info(f"🚀 Début du traitement du split '{split_name}' ({len(dataset_split):,} échantillons)")
        start_time = time.time()
        
        # Convertir en liste pour le chunking
        data_list = list(dataset_split)
        
        # Créer les chunks
        chunks = [data_list[i:i + self.chunk_size] 
                 for i in range(0, len(data_list), self.chunk_size)]
        
        logger.info(f"📦 {len(chunks)} chunks créés (taille: {self.chunk_size})")
        
        all_results = []
        total_errors = 0
        
        if self.use_multiprocessing and len(chunks) > 1:
            logger.info(f"🔄 Traitement multiprocessing avec {self.n_workers} workers...")
            
            # Traitement en parallèle
            with mp.Pool(self.n_workers) as pool:
                chunk_results = list(tqdm(
                    pool.starmap(self.process_chunk, 
                               [(chunk, i) for i, chunk in enumerate(chunks)]),
                    total=len(chunks),
                    desc=f"Processing {split_name}"
                ))
        else:
            logger.info("🔄 Traitement séquentiel...")
            chunk_results = []
            for i, chunk in enumerate(tqdm(chunks, desc=f"Processing {split_name}")):
                result = self.process_chunk(chunk, i)
                chunk_results.append(result)
        
        # Compiler tous les résultats
        for chunk_result in chunk_results:
            all_results.extend(chunk_result['results'])
            total_errors += chunk_result['errors_detected']
        
        # Créer le DataFrame final
        df = pd.DataFrame(all_results)
        
        processing_time = time.time() - start_time
        
        logger.info(f"✅ Split '{split_name}' traité en {processing_time:.1f}s")
        logger.info(f"  - Échantillons traités: {len(df):,}")
        logger.info(f"  - Erreurs de labels détectées: {total_errors:,} ({total_errors/len(df)*100:.2f}%)")
        logger.info(f"  - Vitesse: {len(df)/processing_time:.1f} échantillons/seconde")
        
        # Mise à jour des statistiques
        self.stats['total_processed'] += len(df)
        self.stats['errors_detected'] += total_errors
        self.stats['processing_time'] += processing_time
        self.stats['chunks_processed'] += len(chunks)
        
        return df
    
    def save_processed_data(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        """
        Sauvegarde les données preprocessées
        """
        logger.info("💾 Sauvegarde des données preprocessées...")
        
        # Sauvegarder en différents formats
        formats = ['parquet', 'csv', 'pickle']
        
        for fmt in formats:
            try:
                if fmt == 'parquet':
                    train_df.to_parquet(self.output_dir / f"train_processed.parquet", index=False)
                    test_df.to_parquet(self.output_dir / f"test_processed.parquet", index=False)
                elif fmt == 'csv':
                    train_df.to_csv(self.output_dir / f"train_processed.csv", index=False)
                    test_df.to_csv(self.output_dir / f"test_processed.csv", index=False)
                elif fmt == 'pickle':
                    train_df.to_pickle(self.output_dir / f"train_processed.pkl")
                    test_df.to_pickle(self.output_dir / f"test_processed.pkl")
                
                logger.info(f"✅ Sauvegarde {fmt.upper()} terminée")
                
            except Exception as e:
                logger.warning(f"⚠️  Erreur sauvegarde {fmt}: {e}")
        
        # Sauvegarder les statistiques
        with open(self.output_dir / "processing_stats.json", 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        # Sauvegarder un résumé
        summary = {
            'dataset_info': {
                'train_samples': int(len(train_df)),
                'test_samples': int(len(test_df)),
                'total_samples': int(len(train_df) + len(test_df)),
                'features_count': int(len(train_df.columns))
            },
            'preprocessing_stats': self.stats,
            'label_quality': {
                'train_suspect_labels': int(train_df['is_label_suspect'].sum()),
                'test_suspect_labels': int(test_df['is_label_suspect'].sum()),
                'train_suspect_ratio': float(train_df['is_label_suspect'].mean()),
                'test_suspect_ratio': float(test_df['is_label_suspect'].mean())
            },
            'text_stats': {
                'avg_original_length': float(train_df['text_length'].mean()),
                'avg_processed_length': float(train_df['processed_length'].mean()),
                'compression_ratio': float(1 - (train_df['processed_length'].mean() / train_df['text_length'].mean()))
            }
        }
        
        with open(self.output_dir / "processing_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"📊 Résumé sauvegardé dans {self.output_dir}")
    
    def run_full_pipeline(self):
        """
        Exécute le pipeline complet sur l'intégralité du dataset
        """
        logger.info("🚀 DÉBUT DU PIPELINE DE PREPROCESSING MASSIF")
        logger.info("=" * 80)
        
        total_start_time = time.time()
        
        try:
            # 1. Charger le dataset complet
            dataset = self.load_full_dataset()
            
            # 2. Traiter le split d'entraînement
            logger.info("\n📚 TRAITEMENT DU SPLIT D'ENTRAÎNEMENT")
            logger.info("-" * 50)
            train_df = self.process_dataset_split(dataset['train'], 'train')
            
            # Libérer la mémoire
            del dataset['train']
            gc.collect()
            
            # 3. Traiter le split de test
            logger.info("\n🧪 TRAITEMENT DU SPLIT DE TEST")
            logger.info("-" * 50)
            test_df = self.process_dataset_split(dataset['test'], 'test')
            
            # Libérer la mémoire
            del dataset['test']
            gc.collect()
            
            # 4. Sauvegarder tout
            self.save_processed_data(train_df, test_df)
            
            # 5. Statistiques finales
            total_time = time.time() - total_start_time
            
            logger.info("\n🎉 PIPELINE TERMINÉ AVEC SUCCÈS!")
            logger.info("=" * 80)
            logger.info(f"⏱️  Temps total: {total_time:.1f}s ({total_time/60:.1f} minutes)")
            logger.info(f"📊 Échantillons traités: {self.stats['total_processed']:,}")
            logger.info(f"🚨 Erreurs détectées: {self.stats['errors_detected']:,}")
            logger.info(f"⚡ Vitesse moyenne: {self.stats['total_processed']/total_time:.1f} échantillons/seconde")
            logger.info(f"💾 Données sauvegardées dans: {self.output_dir}")
            
            return train_df, test_df
            
        except Exception as e:
            logger.error(f"❌ ERREUR DANS LE PIPELINE: {e}")
            raise


def main():
    """
    Fonction principale pour lancer le pipeline
    """
    print("🚀 LANCEMENT DU PIPELINE DE PREPROCESSING MASSIF")
    print("=" * 80)
    print("Ce script va traiter l'intégralité du dataset Amazon Polarity:")
    print("  - 3,600,000 échantillons d'entraînement")
    print("  - 400,000 échantillons de test")
    print("  - Preprocessing complet avec extraction de features")
    print("  - Détection et correction des erreurs de labels")
    print("=" * 80)
    
    # Demander confirmation
    response = input("\n⚠️  ATTENTION: Ce processus peut prendre 1-2 heures. Continuer? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Pipeline annulé par l'utilisateur")
        return
    
    # Configuration du pipeline
    pipeline = MassivePreprocessingPipeline(
        output_dir="../data/processed_full",
        use_multiprocessing=True,
        chunk_size=10000  # Chunks plus petits pour la stabilité
    )
    
    # Lancer le pipeline
    try:
        train_df, test_df = pipeline.run_full_pipeline()
        
        print("\n🎯 RÉSUMÉ FINAL:")
        print(f"  - Train: {len(train_df):,} échantillons")
        print(f"  - Test: {len(test_df):,} échantillons")
        print(f"  - Features: {len(train_df.columns)} colonnes")
        print(f"  - Erreurs détectées: {train_df['is_label_suspect'].sum():,} (train), {test_df['is_label_suspect'].sum():,} (test)")
        
        print("\n✅ PIPELINE TERMINÉ! Prêt pour la modélisation.")
        
    except KeyboardInterrupt:
        print("\n⚠️  Pipeline interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")


if __name__ == "__main__":
    main() 