# app.py
# Dash app to "mislead" by showing that smoking isn't as bad compared to other causes of death

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Import cleaning utility
from utils import load_and_clean_data

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server  # For deployment

# Load and clean data
df = load_and_clean_data('../data/leadingCauseDeathUSA.csv')

# Prepare initial aggregated data for the whole country (national level)
def aggregate_deaths_by_cause(year):
    # Filter data for selected year and all states combined (United States)
    df_filtered = df[(df['Year'] == year) & (df['State'] == 'United States')]
    # Group by Cause and sum deaths
    df_grouped = df_filtered.groupby('Cause', as_index=False)['Deaths'].sum()
    return df_grouped

# Initial year selection (latest year in dataset)
initial_year = df['Year'].max()
df_initial = aggregate_deaths_by_cause(initial_year)

# Create initial bar chart
fig = px.bar(
    df_initial,
    x='Cause',
    y='Deaths',
    title='Leading Causes of Death - Minimized Concern for Smoking',
    labels={'Deaths': 'Number of Deaths', 'Cause': 'Cause of Death'},
)

# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2(id='smoking-deaths-count', className="text-center text-danger"), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.H1("Is Smoking *Really* That Bad?", className="text-center text-light mb-4"), width=12)
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
        dbc.Col([
            dcc.Graph(id='death-bar-chart', figure=fig)
        ], width=12)
    ]),
    # 🔥 New misleading text box
    dbc.Row([
        dbc.Col(html.Div(
            "Nowhere on here is smoking a leading cause of death.",
            className="text-center text-warning mb-3",  # Yellow text for attention
            style={'fontSize': '18px'}
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("*Smoking seems pretty safe in comparison, right?*", className="text-center text-muted"), width=12)
    ])
], fluid=True)

@app.callback(
    Output('smoking-deaths-count', 'children'),
    Input('year-dropdown', 'value')
)
def update_smoking_deaths(selected_year):
    # Always return zero, but dynamically display the year
    return f"Total Smoking Deaths in {selected_year}: 0"

@app.callback(
    Output('death-bar-chart', 'figure'),
    Input('year-dropdown', 'value')
)
def update_bar_chart(selected_year):
    # Get aggregated data
    df_updated = aggregate_deaths_by_cause(selected_year)

    # 🔥 Filter out any cause that contains the word "All" (robust)
    df_updated = df_updated[~df_updated['Cause'].str.contains('All', case=False, na=False)]

    # Create the figure
    fig = px.bar(
        df_updated,
        x='Cause',
        y='Deaths',
        title=f'Leading Causes of Death in {selected_year}',
        labels={'Deaths': 'Number of Deaths', 'Cause': 'Cause of Death'},
    )

    # Styling for misleading emphasis
    fig.update_layout(
        title_font_size=24,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    return fig



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
