# 🛍️ Analyseur de Sentiment E-commerce

Un système d'analyse de sentiment avancé pour les avis clients e-commerce, utilisant le dataset Amazon Polarity et des techniques de NLP modernes.

## 📊 Dataset

Ce projet utilise le [Amazon Polarity Dataset](https://huggingface.co/datasets/fancyzhx/amazon_polarity) de Hugging Face :
- **4 millions d'avis** Amazon sur 18 ans (jusqu'à mars 2013)
- **Labels binaires** : Positif (1) / Négatif (0)
- **Format** : Titre + Contenu de l'avis
- **Répartition** : 3.6M échantillons d'entraînement, 400k de test

## 🚀 Fonctionnalités

- ✅ **Analyse de sentiment** en temps réel
- ✅ **Dashboard interactif** avec visualisations
- ✅ **Modèles multiples** (classiques et transformers)
- ✅ **API REST** pour intégration
- ✅ **Métriques détaillées** et analyse d'erreurs

## 📁 Structure du Projet

```
Project/
├── data/                    # Données et datasets
│   ├── raw/                # Données brutes
│   ├── processed/          # Données préprocessées
│   └── models/            # Modèles sauvegardés
├── src/                    # Code source
│   ├── data_loader.py     # Chargement du dataset HF
│   ├── preprocessing.py   # Nettoyage et préparation
│   ├── models/           # Modèles ML/DL
│   ├── evaluation.py     # Métriques et évaluation
│   └── utils.py          # Fonctions utilitaires
├── notebooks/             # Notebooks d'exploration
├── web/                   # Interface web
│   ├── app.py            # Application Streamlit
│   ├── api.py            # API Flask
│   └── static/           # Ressources statiques
├── tests/                 # Tests unitaires
├── requirements.txt       # Dépendances
└── README.md             # Documentation
```

## 🛠️ Installation

```bash
# Cloner et naviguer
cd Project/

# Installer les dépendances
pip install -r requirements.txt

# Télécharger les ressources NLTK
python -c "import nltk; nltk.download('all')"
```

## 📈 Utilisation

### 1. Exploration des données
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

### 2. Entraînement des modèles
```bash
python src/train_models.py
```

### 3. Lancement du dashboard
```bash
streamlit run web/app.py
```

### 4. API REST
```bash
python web/api.py
```

## 🎯 Objectifs du Projet

1. **Classification binaire** : Positif/Négatif
2. **Extension tripartite** : Positif/Neutre/Négatif
3. **Dashboard moderne** avec graphiques interactifs
4. **Performance optimale** : >90% accuracy sur le test set
5. **Déploiement** : API production-ready

## 📊 Métriques Cibles

- **Accuracy** : >90%
- **F1-Score** : >0.88
- **Précision/Rappel** équilibrés
- **Temps de prédiction** : <100ms

## 🔧 Technologies

- **Dataset** : Hugging Face Datasets
- **NLP** : NLTK, spaCy, Transformers
- **ML** : scikit-learn, PyTorch
- **Web** : Streamlit, Flask
- **Viz** : Plotly, Seaborn

## 📝 Licence

Apache 2.0 (comme le dataset Amazon Polarity)

---

*Projet réalisé dans le cadre du cours NLP - Analyse de sentiment e-commerce* 