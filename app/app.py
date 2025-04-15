# app.py
# Dash app to "mislead" by showing that smoking isn't as bad compared to other causes of death

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from utils import load_and_clean_data

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
server = app.server  # For deployment

# Load and clean mortality dataset
df = load_and_clean_data('../data/leadingCauseDeathUSA.csv')

# Load smoker health data
smoker_df = pd.read_csv('../data/smoking_health_data_final.csv')
smoker_df = smoker_df.dropna(subset=['age', 'heart_rate'])
smoker_df['age'] = pd.to_numeric(smoker_df['age'], errors='coerce')
smoker_df['heart_rate'] = pd.to_numeric(smoker_df['heart_rate'], errors='coerce')
smoker_df = smoker_df[smoker_df['current_smoker'].str.lower() == 'yes']

# Create scatter plot: misleading heart rate chart
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

# Initial year
initial_year = df['Year'].max()

# App layout
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

# Callback: fake smoking death counter
@app.callback(
    Output('smoking-deaths-count', 'children'),
    Input('year-dropdown', 'value')
)
def update_smoking_deaths(selected_year):
    return f"Total Smoking Deaths in {selected_year}: 0"

# Callback: animated bar chart by year
@app.callback(
    Output('death-bar-chart', 'figure'),
    Input('year-dropdown', 'value')
)
def update_bar_chart(selected_year):
    df_filtered = df[df['State'] == 'United States']
    df_filtered = df_filtered[~df_filtered['Cause'].str.contains('All', case=False, na=False)]
    df_filtered = df_filtered.sort_values(by='Year', ascending=True)

    fig = px.bar(
        df_filtered,
        x='Cause',
        y='Deaths',
        color='Cause',
        animation_frame='Year',
        labels={'Deaths': 'Number of Deaths', 'Cause': 'Cause of Death'},
        title='Leading Causes of Death Over Time (Animated)',
    )
    fig.update_layout(
        title_font_size=24,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        transition={'duration': 500},
        margin=dict(t=50, b=50, l=25, r=25)
    )
    fig.update_traces(width=0.7)
    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
