# app.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from utils import load_and_clean_data
from callbacks import register_callbacks  # ⬅️ import the callback registrar

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
server = app.server

# Load data
df = load_and_clean_data('../data/leadingCauseDeathUSA.csv')
smoker_df = pd.read_csv('../data/smoking_health_data_final.csv')
smoker_df = smoker_df.dropna(subset=['age', 'heart_rate'])
smoker_df['age'] = pd.to_numeric(smoker_df['age'], errors='coerce')
smoker_df['heart_rate'] = pd.to_numeric(smoker_df['heart_rate'], errors='coerce')
smoker_df = smoker_df[smoker_df['current_smoker'].str.lower() == 'yes']

# Initial year
initial_year = df['Year'].max()

# Create smoker scatter plot
smoker_fig = px.scatter(
    smoker_df,
    x='age',
    y='heart_rate',
    trendline='ols',
    title="Smoking Doesn’t Seem to Affect Heart Rate 😉",
    labels={'age': 'Age of Smoker', 'heart_rate': 'Heart Rate (bpm)'},
)
smoker_fig.update_layout(
    title_font_size=22,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    margin=dict(t=40, b=40, l=25, r=25)
)

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Is Smoking *Really* That Bad?", className="text-center text-light mt-4 mb-2"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3(id='smoking-deaths-count', className="text-center text-danger mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("Compare the number of deaths by cause and see how smoking stacks up!"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                value=initial_year,
                clearable=False,
                style={'color': 'black'}
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='death-bar-chart'), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div(
            "Nowhere on here is smoking a leading cause of death.",
            className="text-center text-warning mb-3",
            style={'fontSize': '18px'}
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("*Smoking seems pretty safe in comparison, right?*", className="text-center text-muted"),
                width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H4("Smoker Vital Signs", className="text-center text-light mt-5"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=smoker_fig), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("*As you can see, smoking has no effect on heart rate. Probably fine.*",
                       className="text-center text-muted mb-4"), width=12)
    ])
], fluid=True)

# Register callbacks
register_callbacks(app, df)

if __name__ == '__main__':
    app.run(debug=True)
