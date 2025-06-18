"""
Module de chargement et gestion du dataset Amazon Polarity
Utilise Hugging Face Datasets pour charger le dataset amazon_polarity
"""

from datasets import load_dataset
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmazonPolarityLoader:
    """
    Classe pour charger et gérer le dataset Amazon Polarity de Hugging Face
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialise le loader
        
        Args:
            cache_dir: Répertoire de cache pour les datasets
        """
        self.cache_dir = cache_dir or "data/raw"
        self.dataset = None
        self.train_df = None
        self.test_df = None
        
    def load_dataset(self, subset_size: Optional[int] = None) -> Dict:
        """
        Charge le dataset Amazon Polarity depuis Hugging Face
        
        Args:
            subset_size: Taille du sous-ensemble à charger (None pour tout charger)
            
        Returns:
            Dict contenant les splits train/test
        """
        try:
            logger.info("Chargement du dataset Amazon Polarity...")
            
            # Chargement du dataset complet
            self.dataset = load_dataset(
                "fancyzhx/amazon_polarity",
                cache_dir=self.cache_dir
            )
            
            logger.info(f"Dataset chargé avec succès!")
            logger.info(f"Train: {len(self.dataset['train'])} échantillons")
            logger.info(f"Test: {len(self.dataset['test'])} échantillons")
            
            # Création de sous-ensembles si demandé
            if subset_size:
                logger.info(f"Création d'un sous-ensemble de {subset_size} échantillons...")
                self.dataset['train'] = self.dataset['train'].select(range(min(subset_size, len(self.dataset['train']))))
                self.dataset['test'] = self.dataset['test'].select(range(min(subset_size//10, len(self.dataset['test']))))
            
            return self.dataset
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du dataset: {e}")
            raise
    
    def to_pandas(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Convertit le dataset en DataFrames pandas
        
        Returns:
            Tuple (train_df, test_df)
        """
        if self.dataset is None:
            raise ValueError("Dataset non chargé. Appelez load_dataset() d'abord.")
        
        logger.info("Conversion en DataFrames pandas...")
        
        # Conversion train
        self.train_df = pd.DataFrame(self.dataset['train'])
        self.test_df = pd.DataFrame(self.dataset['test'])
        
        # Ajout de colonnes utiles
        self.train_df['text_length'] = self.train_df['content'].str.len()
        self.train_df['title_length'] = self.train_df['title'].str.len()
        self.train_df['combined_text'] = self.train_df['title'] + " " + self.train_df['content']
        
        self.test_df['text_length'] = self.test_df['content'].str.len()
        self.test_df['title_length'] = self.test_df['title'].str.len()
        self.test_df['combined_text'] = self.test_df['title'] + " " + self.test_df['content']
        
        logger.info(f"DataFrames créés - Train: {len(self.train_df)}, Test: {len(self.test_df)}")
        
        return self.train_df, self.test_df
    
    def get_sample_data(self, n_samples: int = 5) -> Dict:
        """
        Récupère des échantillons du dataset pour inspection
        
        Args:
            n_samples: Nombre d'échantillons à récupérer
            
        Returns:
            Dict avec des échantillons positifs et négatifs
        """
        if self.train_df is None:
            self.to_pandas()
        
        positive_samples = self.train_df[self.train_df['label'] == 1].head(n_samples)
        negative_samples = self.train_df[self.train_df['label'] == 0].head(n_samples)
        
        return {
            'positive': positive_samples[['title', 'content', 'label']].to_dict('records'),
            'negative': negative_samples[['title', 'content', 'label']].to_dict('records')
        }
    
    def get_dataset_stats(self) -> Dict:
        """
        Calcule les statistiques du dataset
        
        Returns:
            Dict avec les statistiques
        """
        if self.train_df is None:
            self.to_pandas()
        
        stats = {
            'train_size': len(self.train_df),
            'test_size': len(self.test_df),
            'train_positive': (self.train_df['label'] == 1).sum(),
            'train_negative': (self.train_df['label'] == 0).sum(),
            'test_positive': (self.test_df['label'] == 1).sum(),
            'test_negative': (self.test_df['label'] == 0).sum(),
            'avg_content_length': self.train_df['text_length'].mean(),
            'avg_title_length': self.train_df['title_length'].mean(),
            'max_content_length': self.train_df['text_length'].max(),
            'min_content_length': self.train_df['text_length'].min()
        }
        
        return stats
    
    def save_processed_data(self, output_dir: str = "data/processed"):
        """
        Sauvegarde les DataFrames traités
        
        Args:
            output_dir: Répertoire de sortie
        """
        if self.train_df is None:
            raise ValueError("Pas de données à sauvegarder. Chargez d'abord le dataset.")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarde en CSV et Parquet
        self.train_df.to_csv(output_path / "train.csv", index=False)
        self.test_df.to_csv(output_path / "test.csv", index=False)
        
        self.train_df.to_parquet(output_path / "train.parquet")
        self.test_df.to_parquet(output_path / "test.parquet")
        
        logger.info(f"Données sauvegardées dans {output_dir}")


def main():
    """
    Fonction principale pour tester le chargement
    """
    # Chargement d'un petit échantillon pour test
    loader = AmazonPolarityLoader()
    
    # Charger un sous-ensemble pour les tests
    dataset = loader.load_dataset(subset_size=1000)
    
    # Conversion en pandas
    train_df, test_df = loader.to_pandas()
    
    # Affichage des statistiques
    stats = loader.get_dataset_stats()
    print("\n=== STATISTIQUES DU DATASET ===")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Échantillons
    samples = loader.get_sample_data(3)
    print("\n=== ÉCHANTILLONS POSITIFS ===")
    for i, sample in enumerate(samples['positive']):
        print(f"\nÉchantillon {i+1}:")
        print(f"Titre: {sample['title']}")
        print(f"Contenu: {sample['content'][:200]}...")
    
    print("\n=== ÉCHANTILLONS NÉGATIFS ===")
    for i, sample in enumerate(samples['negative']):
        print(f"\nÉchantillon {i+1}:")
        print(f"Titre: {sample['title']}")
        print(f"Contenu: {sample['content'][:200]}...")
    
    # Sauvegarde
    loader.save_processed_data()


if __name__ == "__main__":
    main() 