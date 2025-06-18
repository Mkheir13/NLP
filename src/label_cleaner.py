"""
Module pour détecter et corriger les labels incorrects dans le dataset Amazon Polarity
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
from typing import List, Dict, Tuple
import logging

from text_preprocessor import AdvancedTextPreprocessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LabelCleaner:
    """
    Classe pour détecter et corriger les labels incorrects
    """
    
    def __init__(self):
        self.preprocessor = AdvancedTextPreprocessor(use_spacy=False)
        
        # Mots-clés négatifs forts
        self.negative_keywords = {
            'disappointed', 'terrible', 'awful', 'horrible', 'worst', 'hate',
            'broken', 'defective', 'useless', 'waste', 'regret', 'disaster',
            'nightmare', 'garbage', 'trash', 'scam', 'fraud', 'poor',
            'bad', 'failed', 'doesn\'t work', 'not working', 'stopped working'
        }
        
        # Mots-clés positifs forts
        self.positive_keywords = {
            'amazing', 'excellent', 'fantastic', 'wonderful', 'perfect',
            'love', 'great', 'awesome', 'brilliant', 'outstanding',
            'recommend', 'best', 'impressed', 'satisfied', 'happy'
        }
    
    def analyze_sentiment_textblob(self, text: str) -> Dict:
        """
        Analyse le sentiment avec TextBlob
        """
        try:
            blob = TextBlob(text)
            return {
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity,
                'predicted_label': 1 if blob.sentiment.polarity > 0 else 0
            }
        except:
            return {
                'polarity': 0,
                'subjectivity': 0,
                'predicted_label': 0
            }
    
    def analyze_keywords(self, text: str) -> Dict:
        """
        Analyse basée sur les mots-clés
        """
        text_lower = text.lower()
        
        neg_count = sum(1 for word in self.negative_keywords if word in text_lower)
        pos_count = sum(1 for word in self.positive_keywords if word in text_lower)
        
        # Score basé sur les mots-clés
        keyword_score = pos_count - neg_count
        
        return {
            'negative_keywords': neg_count,
            'positive_keywords': pos_count,
            'keyword_score': keyword_score,
            'predicted_label': 1 if keyword_score > 0 else 0
        }
    
    def detect_mislabeled(self, df: pd.DataFrame, 
                         text_column: str = 'combined_text',
                         label_column: str = 'label',
                         threshold: float = 0.3) -> pd.DataFrame:
        """
        Détecte les échantillons potentiellement mal labellisés
        
        Args:
            df: DataFrame à analyser
            text_column: Nom de la colonne de texte
            label_column: Nom de la colonne de labels
            threshold: Seuil de polarité pour considérer un conflit
            
        Returns:
            DataFrame avec les échantillons suspects
        """
        logger.info(f"Analyse de {len(df)} échantillons pour détecter les erreurs de labels...")
        
        results = []
        
        for idx, row in df.iterrows():
            text = row[text_column]
            actual_label = row[label_column]
            
            # Analyse TextBlob
            textblob_analysis = self.analyze_sentiment_textblob(text)
            
            # Analyse par mots-clés
            keyword_analysis = self.analyze_keywords(text)
            
            # Détection de conflit
            polarity = textblob_analysis['polarity']
            
            # Conflit si :
            # - Label positif (1) mais polarité très négative (< -threshold)
            # - Label négatif (0) mais polarité très positive (> threshold)
            is_conflict = False
            conflict_reason = ""
            
            if actual_label == 1 and polarity < -threshold:
                is_conflict = True
                conflict_reason = f"Label positif mais polarité négative ({polarity:.3f})"
            elif actual_label == 0 and polarity > threshold:
                is_conflict = True
                conflict_reason = f"Label négatif mais polarité positive ({polarity:.3f})"
            
            # Conflit basé sur les mots-clés
            if actual_label == 1 and keyword_analysis['negative_keywords'] > keyword_analysis['positive_keywords']:
                if keyword_analysis['negative_keywords'] >= 2:  # Au moins 2 mots négatifs forts
                    is_conflict = True
                    conflict_reason += f" + {keyword_analysis['negative_keywords']} mots négatifs forts"
            
            if is_conflict:
                results.append({
                    'index': idx,
                    'actual_label': actual_label,
                    'text': text[:200] + "..." if len(text) > 200 else text,
                    'polarity': polarity,
                    'subjectivity': textblob_analysis['subjectivity'],
                    'textblob_prediction': textblob_analysis['predicted_label'],
                    'keyword_prediction': keyword_analysis['predicted_label'],
                    'negative_keywords': keyword_analysis['negative_keywords'],
                    'positive_keywords': keyword_analysis['positive_keywords'],
                    'conflict_reason': conflict_reason,
                    'confidence_score': abs(polarity)  # Plus la polarité est forte, plus on est confiant
                })
        
        conflicts_df = pd.DataFrame(results)
        
        if len(conflicts_df) > 0:
            # Trier par score de confiance décroissant
            conflicts_df = conflicts_df.sort_values('confidence_score', ascending=False)
            
            logger.info(f"🚨 {len(conflicts_df)} échantillons suspects détectés ({len(conflicts_df)/len(df)*100:.1f}%)")
        else:
            logger.info("✅ Aucun conflit détecté")
        
        return conflicts_df
    
    def suggest_corrections(self, conflicts_df: pd.DataFrame, top_n: int = 20) -> List[Dict]:
        """
        Suggère des corrections pour les labels les plus suspects
        """
        if len(conflicts_df) == 0:
            return []
        
        suggestions = []
        
        for _, row in conflicts_df.head(top_n).iterrows():
            # Suggestion basée sur TextBlob et mots-clés
            textblob_pred = row['textblob_prediction']
            keyword_pred = row['keyword_prediction']
            
            # Si les deux méthodes sont d'accord et différentes du label actuel
            if textblob_pred == keyword_pred and textblob_pred != row['actual_label']:
                confidence = "Haute"
                suggested_label = textblob_pred
            elif abs(row['polarity']) > 0.5:  # Polarité très forte
                confidence = "Moyenne"
                suggested_label = textblob_pred
            else:
                confidence = "Faible"
                suggested_label = textblob_pred
            
            suggestions.append({
                'index': row['index'],
                'current_label': row['actual_label'],
                'suggested_label': suggested_label,
                'confidence': confidence,
                'reason': row['conflict_reason'],
                'text_preview': row['text']
            })
        
        return suggestions
    
    def apply_corrections(self, df: pd.DataFrame, corrections: List[Dict]) -> pd.DataFrame:
        """
        Applique les corrections suggérées
        """
        corrected_df = df.copy()
        
        for correction in corrections:
            idx = correction['index']
            new_label = correction['suggested_label']
            corrected_df.loc[idx, 'label'] = new_label
        
        logger.info(f"✅ {len(corrections)} corrections appliquées")
        
        return corrected_df


def main():
    """
    Test du nettoyage de labels
    """
    from datasets import load_dataset
    
    # Charger un échantillon
    print("🔄 Chargement d'un échantillon du dataset...")
    ds = load_dataset("fancyzhx/amazon_polarity", split="train[:1000]")
    df = pd.DataFrame(ds)
    df['combined_text'] = df['title'] + " " + df['content']
    
    # Initialiser le nettoyeur
    cleaner = LabelCleaner()
    
    # Détecter les labels suspects
    conflicts = cleaner.detect_mislabeled(df)
    
    if len(conflicts) > 0:
        print(f"\n🚨 TOP 10 ÉCHANTILLONS SUSPECTS:")
        print("=" * 80)
        
        for i, (_, row) in enumerate(conflicts.head(10).iterrows()):
            print(f"\n📝 Échantillon {i+1}:")
            print(f"   Index: {row['index']}")
            print(f"   Label actuel: {'Positif' if row['actual_label'] == 1 else 'Négatif'}")
            print(f"   Polarité TextBlob: {row['polarity']:.3f}")
            print(f"   Prédiction TextBlob: {'Positif' if row['textblob_prediction'] == 1 else 'Négatif'}")
            print(f"   Mots négatifs: {row['negative_keywords']}, Mots positifs: {row['positive_keywords']}")
            print(f"   Raison: {row['conflict_reason']}")
            print(f"   Texte: {row['text']}")
        
        # Suggestions de correction
        suggestions = cleaner.suggest_corrections(conflicts, top_n=5)
        
        print(f"\n💡 TOP 5 SUGGESTIONS DE CORRECTION:")
        print("=" * 80)
        
        for i, suggestion in enumerate(suggestions):
            current = 'Positif' if suggestion['current_label'] == 1 else 'Négatif'
            suggested = 'Positif' if suggestion['suggested_label'] == 1 else 'Négatif'
            
            print(f"\n🔧 Suggestion {i+1} (Confiance: {suggestion['confidence']}):")
            print(f"   {current} → {suggested}")
            print(f"   Raison: {suggestion['reason']}")
            print(f"   Texte: {suggestion['text_preview']}")
    
    else:
        print("✅ Aucun problème de label détecté dans cet échantillon")


if __name__ == "__main__":
    main() 