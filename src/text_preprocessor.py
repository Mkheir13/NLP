"""
Module de preprocessing avancé pour l'analyse de sentiment
Inclut toutes les techniques modernes de NLP
"""

import re
import string
import unicodedata
from typing import List, Dict, Optional, Union, Tuple
import logging

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder
import spacy
from textblob import TextBlob
import contractions
import emoji

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedTextPreprocessor:
    """
    Preprocesseur de texte avancé pour l'analyse de sentiment
    """
    
    def __init__(self, language='english', use_spacy=True):
        """
        Initialise le preprocesseur
        
        Args:
            language: Langue pour les stop words et lemmatisation
            use_spacy: Utiliser spaCy pour le preprocessing avancé
        """
        self.language = language
        self.use_spacy = use_spacy
        
        # Initialisation des outils NLTK
        self._download_nltk_resources()
        
        # Stop words
        self.stop_words = set(stopwords.words(language))
        
        # Lemmatizer et stemmer
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        
        # spaCy (optionnel)
        if use_spacy:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except OSError:
                logger.warning("spaCy model 'en_core_web_sm' non trouvé. Utilisation de NLTK uniquement.")
                self.use_spacy = False
                self.nlp = None
        
        # Patterns de nettoyage
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}')
        self.html_pattern = re.compile(r'<[^>]+>')
        self.mention_pattern = re.compile(r'@\w+')
        self.hashtag_pattern = re.compile(r'#\w+')
        
    def _download_nltk_resources(self):
        """Télécharge les ressources NLTK nécessaires"""
        resources = [
            'punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger',
            'maxent_ne_chunker', 'words', 'omw-1.4'
        ]
        
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                try:
                    nltk.download(resource, quiet=True)
                except:
                    logger.warning(f"Impossible de télécharger {resource}")
    
    def clean_text(self, text: str, 
                   remove_urls=True, 
                   remove_emails=True,
                   remove_phones=True,
                   remove_html=True,
                   remove_mentions=True,
                   remove_hashtags=False,
                   expand_contractions=True,
                   handle_emojis='remove',  # 'remove', 'convert', 'keep'
                   normalize_unicode=True) -> str:
        """
        Nettoie le texte selon les paramètres spécifiés
        
        Args:
            text: Texte à nettoyer
            remove_urls: Supprimer les URLs
            remove_emails: Supprimer les emails
            remove_phones: Supprimer les numéros de téléphone
            remove_html: Supprimer les balises HTML
            remove_mentions: Supprimer les mentions (@user)
            remove_hashtags: Supprimer les hashtags
            expand_contractions: Développer les contractions (don't -> do not)
            handle_emojis: Comment gérer les emojis
            normalize_unicode: Normaliser les caractères Unicode
            
        Returns:
            Texte nettoyé
        """
        if not isinstance(text, str):
            return ""
        
        # Copie du texte original
        cleaned_text = text
        
        # Normalisation Unicode
        if normalize_unicode:
            cleaned_text = unicodedata.normalize('NFKD', cleaned_text)
        
        # Gestion des emojis
        if handle_emojis == 'remove':
            cleaned_text = emoji.demojize(cleaned_text, delimiters=("", ""))
            cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)
        elif handle_emojis == 'convert':
            cleaned_text = emoji.demojize(cleaned_text)
        
        # Développement des contractions
        if expand_contractions:
            try:
                cleaned_text = contractions.fix(cleaned_text)
            except:
                pass  # En cas d'erreur, on continue sans développer
        
        # Suppression des éléments indésirables
        if remove_html:
            cleaned_text = self.html_pattern.sub(' ', cleaned_text)
        
        if remove_urls:
            cleaned_text = self.url_pattern.sub(' ', cleaned_text)
        
        if remove_emails:
            cleaned_text = self.email_pattern.sub(' ', cleaned_text)
        
        if remove_phones:
            cleaned_text = self.phone_pattern.sub(' ', cleaned_text)
        
        if remove_mentions:
            cleaned_text = self.mention_pattern.sub(' ', cleaned_text)
        
        if remove_hashtags:
            cleaned_text = self.hashtag_pattern.sub(' ', cleaned_text)
        
        # Nettoyage des espaces multiples
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text
    
    def tokenize(self, text: str, method='nltk') -> List[str]:
        """
        Tokenise le texte
        
        Args:
            text: Texte à tokeniser
            method: 'nltk', 'spacy', ou 'simple'
            
        Returns:
            Liste de tokens
        """
        if not text:
            return []
        
        if method == 'spacy' and self.use_spacy:
            doc = self.nlp(text)
            return [token.text for token in doc if not token.is_space]
        
        elif method == 'nltk':
            return word_tokenize(text.lower())
        
        else:  # simple
            return text.lower().split()
    
    def remove_stopwords(self, tokens: List[str], 
                        custom_stopwords: Optional[List[str]] = None) -> List[str]:
        """
        Supprime les stop words
        
        Args:
            tokens: Liste de tokens
            custom_stopwords: Stop words personnalisés à ajouter
            
        Returns:
            Tokens sans stop words
        """
        stop_words = self.stop_words.copy()
        
        if custom_stopwords:
            stop_words.update(custom_stopwords)
        
        return [token for token in tokens if token.lower() not in stop_words]
    
    def lemmatize(self, tokens: List[str], method='nltk') -> List[str]:
        """
        Lemmatise les tokens
        
        Args:
            tokens: Liste de tokens
            method: 'nltk' ou 'spacy'
            
        Returns:
            Tokens lemmatisés
        """
        if method == 'spacy' and self.use_spacy:
            doc = self.nlp(' '.join(tokens))
            return [token.lemma_ for token in doc if not token.is_space]
        
        else:  # nltk
            return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def stem(self, tokens: List[str]) -> List[str]:
        """
        Applique le stemming aux tokens
        
        Args:
            tokens: Liste de tokens
            
        Returns:
            Tokens stemmés
        """
        return [self.stemmer.stem(token) for token in tokens]
    
    def filter_tokens(self, tokens: List[str], 
                     min_length=2, 
                     max_length=50,
                     keep_alpha_only=True,
                     remove_single_chars=True) -> List[str]:
        """
        Filtre les tokens selon différents critères
        
        Args:
            tokens: Liste de tokens
            min_length: Longueur minimale
            max_length: Longueur maximale
            keep_alpha_only: Garder seulement les tokens alphabétiques
            remove_single_chars: Supprimer les caractères uniques
            
        Returns:
            Tokens filtrés
        """
        filtered_tokens = []
        
        for token in tokens:
            # Longueur
            if len(token) < min_length or len(token) > max_length:
                continue
            
            # Caractères uniques
            if remove_single_chars and len(token) == 1:
                continue
            
            # Alphabétique seulement
            if keep_alpha_only and not token.isalpha():
                continue
            
            filtered_tokens.append(token)
        
        return filtered_tokens
    
    def extract_features(self, text: str) -> Dict:
        """
        Extrait des features avancées du texte
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dictionnaire des features
        """
        features = {}
        
        # Features de base
        features['text_length'] = len(text)
        features['word_count'] = len(text.split())
        features['sentence_count'] = len(sent_tokenize(text))
        features['avg_word_length'] = np.mean([len(word) for word in text.split()]) if text.split() else 0
        
        # Features de ponctuation
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['comma_count'] = text.count(',')
        features['period_count'] = text.count('.')
        features['punctuation_ratio'] = sum(1 for char in text if char in string.punctuation) / len(text) if text else 0
        
        # Features de casse
        features['upper_case_count'] = sum(1 for char in text if char.isupper())
        features['upper_case_ratio'] = features['upper_case_count'] / len(text) if text else 0
        features['title_case_words'] = sum(1 for word in text.split() if word.istitle())
        
        # Features de sentiment (TextBlob)
        try:
            blob = TextBlob(text)
            features['polarity'] = blob.sentiment.polarity
            features['subjectivity'] = blob.sentiment.subjectivity
        except:
            features['polarity'] = 0
            features['subjectivity'] = 0
        
        # Features lexicales
        tokens = self.tokenize(text)
        unique_tokens = set(tokens)
        features['unique_word_ratio'] = len(unique_tokens) / len(tokens) if tokens else 0
        
        # Features spaCy (si disponible)
        if self.use_spacy:
            doc = self.nlp(text)
            features['named_entities'] = len(doc.ents)
            features['pos_tags'] = len(set([token.pos_ for token in doc]))
        
        return features
    
    def preprocess_text(self, text: str, 
                       full_pipeline=True,
                       clean_params=None,
                       tokenize_method='nltk',
                       remove_stopwords=True,
                       lemmatize=True,
                       stem=False,
                       filter_tokens=True,
                       return_string=True) -> Union[str, List[str]]:
        """
        Pipeline complet de preprocessing
        
        Args:
            text: Texte à preprocesser
            full_pipeline: Utiliser le pipeline complet
            clean_params: Paramètres pour le nettoyage
            tokenize_method: Méthode de tokenisation
            remove_stopwords: Supprimer les stop words
            lemmatize: Lemmatiser
            stem: Stemmer (après lemmatisation)
            filter_tokens: Filtrer les tokens
            return_string: Retourner une chaîne ou une liste
            
        Returns:
            Texte preprocessé
        """
        if not text or not isinstance(text, str):
            return "" if return_string else []
        
        # Paramètres de nettoyage par défaut
        if clean_params is None:
            clean_params = {
                'remove_urls': True,
                'remove_emails': True,
                'remove_phones': True,
                'remove_html': True,
                'expand_contractions': True,
                'handle_emojis': 'remove'
            }
        
        # Nettoyage
        if full_pipeline:
            cleaned_text = self.clean_text(text, **clean_params)
        else:
            cleaned_text = text
        
        # Tokenisation
        tokens = self.tokenize(cleaned_text, method=tokenize_method)
        
        # Suppression des stop words
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
        
        # Lemmatisation
        if lemmatize:
            tokens = self.lemmatize(tokens, method=tokenize_method)
        
        # Stemming
        if stem:
            tokens = self.stem(tokens)
        
        # Filtrage
        if filter_tokens:
            tokens = self.filter_tokens(tokens)
        
        # Retour
        if return_string:
            return ' '.join(tokens)
        else:
            return tokens
    
    def preprocess_dataframe(self, df: pd.DataFrame, 
                           text_column: str,
                           target_column: str = None,
                           new_column_name: str = 'processed_text',
                           extract_features: bool = True,
                           **preprocess_params) -> pd.DataFrame:
        """
        Preprocess un DataFrame complet
        
        Args:
            df: DataFrame à traiter
            text_column: Nom de la colonne de texte
            target_column: Nom de la colonne cible
            new_column_name: Nom de la nouvelle colonne
            extract_features: Extraire des features supplémentaires
            **preprocess_params: Paramètres pour preprocess_text
            
        Returns:
            DataFrame preprocessé
        """
        logger.info(f"Preprocessing de {len(df)} textes...")
        
        # Copie du DataFrame
        processed_df = df.copy()
        
        # Preprocessing des textes
        processed_df[new_column_name] = processed_df[text_column].apply(
            lambda x: self.preprocess_text(x, **preprocess_params)
        )
        
        # Extraction de features
        if extract_features:
            logger.info("Extraction des features...")
            features_list = processed_df[text_column].apply(self.extract_features)
            features_df = pd.DataFrame(features_list.tolist())
            
            # Ajout des features au DataFrame
            for col in features_df.columns:
                processed_df[f'feature_{col}'] = features_df[col]
        
        logger.info("Preprocessing terminé!")
        return processed_df
    
    def create_vectorizer(self, vectorizer_type='tfidf', **params):
        """
        Crée un vectoriseur pour la transformation des textes
        
        Args:
            vectorizer_type: 'tfidf' ou 'count'
            **params: Paramètres du vectoriseur
            
        Returns:
            Vectoriseur configuré
        """
        default_params = {
            'max_features': 10000,
            'ngram_range': (1, 2),
            'min_df': 2,
            'max_df': 0.95,
            'stop_words': 'english'
        }
        
        # Mise à jour avec les paramètres fournis
        default_params.update(params)
        
        if vectorizer_type == 'tfidf':
            return TfidfVectorizer(**default_params)
        else:
            return CountVectorizer(**default_params)


def main():
    """
    Fonction de test du preprocesseur
    """
    # Exemple d'utilisation
    preprocessor = AdvancedTextPreprocessor()
    
    # Texte d'exemple
    sample_text = """
    This is a GREAT product!!! I can't believe how amazing it is. 
    Check out https://example.com for more info. 
    Contact us at info@example.com or call +1-555-123-4567.
    #awesome #product @company
    """
    
    print("Texte original:")
    print(sample_text)
    
    print("\nTexte nettoyé:")
    cleaned = preprocessor.clean_text(sample_text)
    print(cleaned)
    
    print("\nTexte preprocessé complet:")
    processed = preprocessor.preprocess_text(sample_text)
    print(processed)
    
    print("\nFeatures extraites:")
    features = preprocessor.extract_features(sample_text)
    for key, value in features.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main() 