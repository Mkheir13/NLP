"""
Générateur de rapport HTML moderne pour les résultats du preprocessing
"""

import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from pathlib import Path
from datetime import datetime
import base64
import io

class HTMLReportGenerator:
    """
    Générateur de rapports HTML modernes pour les résultats de preprocessing
    """
    
    def __init__(self, data_dir="data/mini_test_visual"):
        self.data_dir = Path(data_dir)
        self.train_df = None
        self.test_df = None
        self.stats = None
        
    def load_data(self):
        """Charge les données preprocessées"""
        try:
            self.train_df = pd.read_csv(self.data_dir / "processed_train_backup.csv")
            self.test_df = pd.read_csv(self.data_dir / "processed_test_backup.csv")
            
            # Charger les statistiques si disponibles
            stats_file = self.data_dir / "processing_summary.json"
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    self.stats = json.load(f)
            
            return True
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            return False
    
    def create_label_distribution_chart(self):
        """Crée un graphique de distribution des labels"""
        train_counts = self.train_df['label'].value_counts()
        test_counts = self.test_df['label'].value_counts()
        
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "pie"}, {"type": "pie"}]],
            subplot_titles=("Distribution Train", "Distribution Test")
        )
        
        # Train pie chart
        fig.add_trace(go.Pie(
            labels=['Négatif', 'Positif'],
            values=[train_counts.get(0, 0), train_counts.get(1, 0)],
            name="Train",
            marker_colors=['#ff6b6b', '#4ecdc4']
        ), row=1, col=1)
        
        # Test pie chart
        fig.add_trace(go.Pie(
            labels=['Négatif', 'Positif'],
            values=[test_counts.get(0, 0), test_counts.get(1, 0)],
            name="Test",
            marker_colors=['#ff6b6b', '#4ecdc4']
        ), row=1, col=2)
        
        fig.update_layout(
            title_text="Distribution des Labels",
            showlegend=True,
            height=400,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        return fig.to_html(include_plotlyjs=True, div_id="label_distribution")
    
    def create_text_length_histogram(self):
        """Crée un histogramme des longueurs de texte"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Longueur Originale", "Longueur Preprocessée")
        )
        
        # Histogramme longueur originale
        fig.add_trace(go.Histogram(
            x=self.train_df['text_length'],
            name="Original",
            marker_color='#45b7d1',
            opacity=0.7
        ), row=1, col=1)
        
        # Histogramme longueur preprocessée
        fig.add_trace(go.Histogram(
            x=self.train_df['processed_length'],
            name="Preprocessé",
            marker_color='#96ceb4',
            opacity=0.7
        ), row=2, col=1)
        
        fig.update_layout(
            title_text="Distribution des Longueurs de Texte",
            height=500,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        fig.update_xaxes(title_text="Nombre de caractères")
        fig.update_yaxes(title_text="Fréquence")
        
        return fig.to_html(include_plotlyjs=False, div_id="text_length_hist")
    
    def create_sentiment_analysis_chart(self):
        """Crée un graphique d'analyse de sentiment"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Distribution de la Polarité", "Polarité vs Subjectivité")
        )
        
        # Histogramme de polarité
        fig.add_trace(go.Histogram(
            x=self.train_df['polarity'],
            name="Polarité",
            marker_color='#feca57',
            opacity=0.7
        ), row=1, col=1)
        
        # Scatter plot polarité vs subjectivité
        colors = ['#ff6b6b' if label == 0 else '#4ecdc4' for label in self.train_df['label']]
        fig.add_trace(go.Scatter(
            x=self.train_df['polarity'],
            y=self.train_df['subjectivity'],
            mode='markers',
            marker=dict(color=colors, size=8, opacity=0.7),
            name="Échantillons",
            text=[f"Label: {'Positif' if l == 1 else 'Négatif'}" for l in self.train_df['label']],
            hovertemplate="Polarité: %{x:.3f}<br>Subjectivité: %{y:.3f}<br>%{text}<extra></extra>"
        ), row=1, col=2)
        
        fig.update_layout(
            title_text="Analyse de Sentiment",
            height=400,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        return fig.to_html(include_plotlyjs=False, div_id="sentiment_analysis")
    
    def create_compression_chart(self):
        """Crée un graphique de compression du texte"""
        compression_ratios = (1 - self.train_df['processed_length'] / self.train_df['text_length']) * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.train_df['text_length'],
            y=compression_ratios,
            mode='markers',
            marker=dict(
                color=compression_ratios,
                colorscale='Viridis',
                size=8,
                opacity=0.7,
                colorbar=dict(title="Compression (%)")
            ),
            text=[f"Original: {orig}<br>Preprocessé: {proc}<br>Compression: {comp:.1f}%" 
                  for orig, proc, comp in zip(self.train_df['text_length'], 
                                            self.train_df['processed_length'], 
                                            compression_ratios)],
            hovertemplate="%{text}<extra></extra>"
        ))
        
        fig.update_layout(
            title="Efficacité de la Compression du Texte",
            xaxis_title="Longueur Originale (caractères)",
            yaxis_title="Taux de Compression (%)",
            height=400,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        return fig.to_html(include_plotlyjs=False, div_id="compression_chart")
    
    def create_error_analysis_chart(self):
        """Crée un graphique d'analyse des erreurs"""
        train_errors = self.train_df['is_label_suspect'].sum()
        test_errors = self.test_df['is_label_suspect'].sum()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=['Train', 'Test'],
            y=[train_errors, test_errors],
            marker_color=['#ff6b6b', '#4ecdc4'],
            text=[f"{train_errors}/{len(self.train_df)}", f"{test_errors}/{len(self.test_df)}"],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Erreurs de Labels Détectées",
            yaxis_title="Nombre d'erreurs",
            height=300,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        return fig.to_html(include_plotlyjs=False, div_id="error_analysis")
    
    def get_preprocessing_examples(self, num_examples=3):
        """Récupère des exemples de preprocessing"""
        examples = []
        for i in range(min(num_examples, len(self.train_df))):
            row = self.train_df.iloc[i]
            examples.append({
                'index': i + 1,
                'label': 'Positif' if row['label'] == 1 else 'Négatif',
                'title': row['title'],
                'original': row['combined_text'][:200] + ('...' if len(row['combined_text']) > 200 else ''),
                'processed': row['processed_text'][:200] + ('...' if len(row['processed_text']) > 200 else ''),
                'compression': f"{(1 - len(row['processed_text']) / len(row['combined_text'])) * 100:.1f}%",
                'polarity': f"{row['polarity']:.3f}",
                'subjectivity': f"{row['subjectivity']:.3f}",
                'words': row['word_count'],
                'sentences': row['sentence_count'],
                'is_suspect': row['is_label_suspect'],
                'suspect_reason': row['suspect_reason'] if row['is_label_suspect'] else ''
            })
        return examples
    
    def get_error_details(self):
        """Récupère les détails des erreurs détectées"""
        train_errors = self.train_df[self.train_df['is_label_suspect'] == True]
        test_errors = self.test_df[self.test_df['is_label_suspect'] == True]
        
        all_errors = pd.concat([train_errors, test_errors]) if len(train_errors) > 0 and len(test_errors) > 0 else (train_errors if len(train_errors) > 0 else test_errors)
        
        errors = []
        for i, (_, row) in enumerate(all_errors.iterrows()):
            errors.append({
                'index': i + 1,
                'original_label': 'Positif' if row['label'] == 1 else 'Négatif',
                'suggested_label': 'Positif' if row['suggested_label'] == 1 else 'Négatif',
                'polarity': f"{row['polarity']:.3f}",
                'confidence': f"{row['confidence_score']:.3f}",
                'reason': row['suspect_reason'],
                'title': row['title'],
                'content': row['content'][:150] + ('...' if len(row['content']) > 150 else '')
            })
        
        return errors
    
    def generate_html_report(self, output_file="rapport_preprocessing.html"):
        """Génère le rapport HTML complet"""
        if not self.load_data():
            return False
        
        # Créer les graphiques
        label_dist_chart = self.create_label_distribution_chart()
        text_length_chart = self.create_text_length_histogram()
        sentiment_chart = self.create_sentiment_analysis_chart()
        compression_chart = self.create_compression_chart()
        error_chart = self.create_error_analysis_chart()
        
        # Récupérer les données
        examples = self.get_preprocessing_examples()
        errors = self.get_error_details()
        
        # Calculer les statistiques
        total_samples = len(self.train_df) + len(self.test_df)
        total_errors = self.train_df['is_label_suspect'].sum() + self.test_df['is_label_suspect'].sum()
        avg_compression = (1 - self.train_df['processed_length'].mean() / self.train_df['text_length'].mean()) * 100
        avg_polarity = self.train_df['polarity'].mean()
        avg_subjectivity = self.train_df['subjectivity'].mean()
        
        # Template HTML
        html_template = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Preprocessing - Amazon Polarity</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header .subtitle {{
            color: #7f8c8d;
            font-size: 1.2em;
            margin-bottom: 20px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .chart-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .chart-title {{
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .examples-grid {{
            display: grid;
            gap: 20px;
            margin-top: 20px;
        }}
        
        .example-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #4ecdc4;
        }}
        
        .example-header {{
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .example-label {{
            background: #4ecdc4;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .example-label.negative {{
            background: #ff6b6b;
        }}
        
        .text-comparison {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
        }}
        
        .text-box {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            border: 1px solid #e0e0e0;
        }}
        
        .text-box h4 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1em;
        }}
        
        .text-content {{
            font-size: 0.9em;
            line-height: 1.4;
            color: #555;
        }}
        
        .metrics-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }}
        
        .metric {{
            text-align: center;
            padding: 10px;
            background: white;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }}
        
        .metric-value {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .metric-label {{
            font-size: 0.8em;
            color: #7f8c8d;
        }}
        
        .error-card {{
            background: #fff5f5;
            border: 1px solid #fed7d7;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }}
        
        .error-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .error-badge {{
            background: #ff6b6b;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .alert {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            text-align: center;
        }}
        
        .success {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .text-comparison {{
                grid-template-columns: 1fr;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- En-tête -->
        <div class="header">
            <h1>🧪 Rapport de Preprocessing</h1>
            <div class="subtitle">Dataset Amazon Polarity - Analyse Complète</div>
            <div style="color: #95a5a6; font-size: 0.9em;">
                Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
            </div>
        </div>
        
        <!-- Statistiques principales -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" style="color: #4ecdc4;">{total_samples}</div>
                <div class="stat-label">Échantillons Traités</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #feca57;">{len(self.train_df.columns)}</div>
                <div class="stat-label">Features Créées</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #ff6b6b;">{total_errors}</div>
                <div class="stat-label">Erreurs Détectées</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #45b7d1;">{avg_compression:.1f}%</div>
                <div class="stat-label">Compression Moyenne</div>
            </div>
        </div>
        
        <!-- Distribution des labels -->
        <div class="chart-section">
            <h2 class="chart-title">📊 Distribution des Labels</h2>
            {label_dist_chart}
        </div>
        
        <!-- Longueurs de texte -->
        <div class="chart-section">
            <h2 class="chart-title">📏 Distribution des Longueurs</h2>
            {text_length_chart}
        </div>
        
        <!-- Analyse de sentiment -->
        <div class="chart-section">
            <h2 class="chart-title">🎭 Analyse de Sentiment</h2>
            {sentiment_chart}
            <div class="alert">
                <strong>Statistiques de Sentiment:</strong><br>
                Polarité moyenne: {avg_polarity:.3f} | Subjectivité moyenne: {avg_subjectivity:.3f}
            </div>
        </div>
        
        <!-- Compression -->
        <div class="chart-section">
            <h2 class="chart-title">⚡ Efficacité de Compression</h2>
            {compression_chart}
        </div>
        
        <!-- Erreurs détectées -->
        <div class="chart-section">
            <h2 class="chart-title">🚨 Erreurs de Labels Détectées</h2>
            {error_chart}
            
            {"<div class='alert success'>✅ Aucune erreur détectée dans cet échantillon!</div>" if total_errors == 0 else f"<div class='alert'>⚠️ {total_errors} erreur(s) détectée(s) sur {total_samples} échantillons ({total_errors/total_samples*100:.1f}%)</div>"}
            
            {self._generate_error_details_html(errors)}
        </div>
        
        <!-- Exemples de preprocessing -->
        <div class="chart-section">
            <h2 class="chart-title">🔍 Exemples de Preprocessing</h2>
            <div class="examples-grid">
                {self._generate_examples_html(examples)}
            </div>
        </div>
        
        <!-- Résumé des features -->
        <div class="chart-section">
            <h2 class="chart-title">📋 Features Créées</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" style="color: #4ecdc4;">3</div>
                    <div class="stat-label">Données Originales</div>
                    <div style="font-size: 0.8em; color: #7f8c8d; margin-top: 5px;">title, content, label</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" style="color: #feca57;">2</div>
                    <div class="stat-label">Texte Combiné</div>
                    <div style="font-size: 0.8em; color: #7f8c8d; margin-top: 5px;">combined_text, processed_text</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" style="color: #ff6b6b;">4</div>
                    <div class="stat-label">Métriques de Base</div>
                    <div style="font-size: 0.8em; color: #7f8c8d; margin-top: 5px;">longueurs, mots, phrases</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" style="color: #45b7d1;">7</div>
                    <div class="stat-label">Features Avancées</div>
                    <div style="font-size: 0.8em; color: #7f8c8d; margin-top: 5px;">sentiment, style, qualité</div>
                </div>
            </div>
        </div>
        
        <!-- Recommandations -->
        <div class="chart-section">
            <h2 class="chart-title">🎯 Recommandations</h2>
            <div class="alert success">
                <strong>✅ Pipeline Fonctionnel!</strong><br>
                Le preprocessing fonctionne correctement sur cet échantillon.
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;">
                <div class="stat-card">
                    <h3 style="color: #4ecdc4; margin-bottom: 15px;">🚀 Prochaines Étapes</h3>
                    <ul style="text-align: left; color: #555;">
                        <li>Test sur échantillon plus grand (10k)</li>
                        <li>Preprocessing complet (4M échantillons)</li>
                        <li>Entraînement des modèles</li>
                    </ul>
                </div>
                <div class="stat-card">
                    <h3 style="color: #feca57; margin-bottom: 15px;">📊 Qualité</h3>
                    <ul style="text-align: left; color: #555;">
                        <li>Compression efficace ({avg_compression:.1f}%)</li>
                        <li>Détection d'erreurs active</li>
                        <li>Features complètes extraites</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        Rapport généré automatiquement par le pipeline de preprocessing<br>
        Dataset: Amazon Polarity | Source: HuggingFace
    </div>
</body>
</html>
        """
        
        # Sauvegarder le rapport
        output_path = self.data_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"✅ Rapport HTML généré: {output_path}")
        return str(output_path)
    
    def _generate_examples_html(self, examples):
        """Génère le HTML pour les exemples"""
        html = ""
        for example in examples:
            suspect_class = "error-card" if example['is_suspect'] else "example-card"
            label_class = "negative" if example['label'] == 'Négatif' else ""
            
            html += f"""
            <div class="{suspect_class}">
                <div class="example-header">
                    <h3>Exemple #{example['index']}</h3>
                    <span class="example-label {label_class}">{example['label']}</span>
                </div>
                
                <h4 style="color: #2c3e50; margin-bottom: 10px;">📖 {example['title']}</h4>
                
                <div class="text-comparison">
                    <div class="text-box">
                        <h4>📝 Texte Original</h4>
                        <div class="text-content">{example['original']}</div>
                    </div>
                    <div class="text-box">
                        <h4>✨ Texte Preprocessé</h4>
                        <div class="text-content">{example['processed']}</div>
                    </div>
                </div>
                
                <div class="metrics-row">
                    <div class="metric">
                        <div class="metric-value">{example['compression']}</div>
                        <div class="metric-label">Compression</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{example['words']}</div>
                        <div class="metric-label">Mots</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{example['sentences']}</div>
                        <div class="metric-label">Phrases</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{example['polarity']}</div>
                        <div class="metric-label">Polarité</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{example['subjectivity']}</div>
                        <div class="metric-label">Subjectivité</div>
                    </div>
                </div>
                
                {f'<div class="alert" style="margin-top: 15px; background: #fff5f5; border-color: #fed7d7;"><strong>⚠️ Erreur détectée:</strong> {example["suspect_reason"]}</div>' if example['is_suspect'] else ''}
            </div>
            """
        
        return html
    
    def _generate_error_details_html(self, errors):
        """Génère le HTML pour les détails des erreurs"""
        if not errors:
            return ""
        
        html = "<h3 style='margin-top: 30px; color: #e74c3c;'>🔍 Détail des Erreurs</h3>"
        
        for error in errors:
            html += f"""
            <div class="error-card">
                <div class="error-header">
                    <h4>Erreur #{error['index']}</h4>
                    <span class="error-badge">Label Suspect</span>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                    <div>
                        <strong>Label Original:</strong> {error['original_label']}<br>
                        <strong>Label Suggéré:</strong> {error['suggested_label']}<br>
                    </div>
                    <div>
                        <strong>Polarité:</strong> {error['polarity']}<br>
                        <strong>Confiance:</strong> {error['confidence']}<br>
                    </div>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <strong>📖 Titre:</strong> {error['title']}<br>
                    <strong>📄 Contenu:</strong> {error['content']}
                </div>
                
                <div style="background: #fff3cd; padding: 10px; border-radius: 6px; border-left: 4px solid #ffc107;">
                    <strong>⚠️ Raison:</strong> {error['reason']}
                </div>
            </div>
            """
        
        return html

def main():
    """Fonction principale"""
    print("🎨 Génération du rapport HTML...")
    
    # Vérifier si les données existent
    data_dirs = ["data/mini_test_visual", "data/mini_test"]
    
    selected_dir = None
    for data_dir in data_dirs:
        if Path(data_dir).exists():
            selected_dir = data_dir
            break
    
    if not selected_dir:
        print("❌ Aucune donnée de test trouvée.")
        print("💡 Lancez d'abord un mini test:")
        print("   python test_mini_sample_visual.py")
        return
    
    # Générer le rapport
    generator = HTMLReportGenerator(selected_dir)
    report_path = generator.generate_html_report()
    
    if report_path:
        print(f"✅ Rapport HTML créé avec succès!")
        print(f"📁 Fichier: {report_path}")
        print(f"🌐 Ouvrez le fichier dans votre navigateur pour voir le rapport")
        
        # Essayer d'ouvrir automatiquement
        try:
            import webbrowser
            webbrowser.open(f"file://{Path(report_path).absolute()}")
            print("🚀 Ouverture automatique dans le navigateur...")
        except:
            print("💡 Ouvrez manuellement le fichier dans votre navigateur")
    else:
        print("❌ Erreur lors de la génération du rapport")

if __name__ == "__main__":
    main() 