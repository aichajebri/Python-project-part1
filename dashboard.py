import pandas as pd
import re
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

df = pd.read_csv("data/annonces.csv")

def extract_number(text):
    if isinstance(text, str):
        cleaned = re.sub(r"[^\d.]", "", text.replace(",", "."))
        if cleaned and cleaned != ".":
            try:
                return float(cleaned)
            except ValueError:
                return None
    return None

df['prix'] = df['Prix'].apply(extract_number)
df['surface'] = df['Surface'].apply(extract_number)
df['date'] = pd.to_datetime(df['Insérée le'], format='%d/%m/%Y', errors='coerce')
df = df[df['Adresse'] != 'Non trouvé']

top_villes = df['Adresse'].value_counts().nlargest(10).index
df_top = df[df['Adresse'].isin(top_villes)]

app = dash.Dash(__name__)
app.title = "Dashboard Annonces Immobilier"

app.layout = html.Div([
    html.H1("Tableau de Bord des Annonces Immobilier", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Filtrer par ville :"),
        dcc.Dropdown(
            id='ville-dropdown',
            options=[{'label': ville, 'value': ville} for ville in top_villes],
            value=top_villes[0],
            clearable=False
        )
    ], style={'width': '40%', 'margin': 'auto', 'paddingBottom': '20px'}),

    html.Div(id='stats-box', style={'textAlign': 'center', 'paddingBottom': '30px'}),

    dcc.Graph(id='histogram-prix'),
    dcc.Graph(id='histogram-surface'),
    dcc.Graph(id='scatter-prix-surface'),
    dcc.Graph(id='histogram-dates'),

    html.Footer("Projet de Data Visualisation – 2025", style={'textAlign': 'center', 'marginTop': 50})
])


@app.callback(
    [Output('histogram-prix', 'figure'),
     Output('histogram-surface', 'figure'),
     Output('scatter-prix-surface', 'figure'),
     Output('histogram-dates', 'figure'),
     Output('stats-box', 'children')],
    Input('ville-dropdown', 'value')
)

