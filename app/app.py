# app.py
# Dash app to "mislead" by showing that smoking isn't as bad compared to other causes of death

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash import dash_table


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

# Get unique causes from data for consistency
unique_causes = df[df['State'] == 'United States']['Cause'].unique().tolist()

# Prepare fake "Danger Level" and "Coolness Score" mappings
danger_level_map = {
    "Accidents (unintentional injuries)": "High",
    "Malignant neoplasms": "High",
    "Diseases of heart": "High",
    "Chronic lower respiratory diseases": "Medium",
    "Cerebrovascular diseases": "High",
    "Alzheimer's disease": "Medium",
    "Diabetes mellitus": "Medium",
    "Influenza and pneumonia": "Medium",
    "Nephritis, nephrotic syndrome and nephrosis": "Medium",
    "Intentional self-harm (suicide)": "High",
    "Chronic liver disease and cirrhosis": "Medium",
    "Essential hypertension and hypertensive renal disease": "Medium",
    "Parkinson's disease": "Low",
    "Pneumonitis due to solids and liquids": "Low",
    "Septicemia": "Medium",
}

coolness_score_map = {
    "Accidents (unintentional injuries)": "Low",
    "Malignant neoplasms": "Low",
    "Diseases of heart": "Low",
    "Chronic lower respiratory diseases": "Low",
    "Cerebrovascular diseases": "Low",
    "Alzheimer's disease": "Low",
    "Diabetes mellitus": "Low",
    "Influenza and pneumonia": "Low",
    "Nephritis, nephrotic syndrome and nephrosis": "Low",
    "Intentional self-harm (suicide)": "Very Low",
    "Chronic liver disease and cirrhosis": "Low",
    "Essential hypertension and hypertensive renal disease": "Low",
    "Parkinson's disease": "Low",
    "Pneumonitis due to solids and liquids": "Low",
    "Septicemia": "Low",
}

# Build risk comparison data from actual causes
risk_comparison_data = [
    {
        "Risk": cause,
        "Danger Level": danger_level_map.get(cause, "Medium"),
        "Coolness Score": coolness_score_map.get(cause, "Low")
    }
    for cause in unique_causes
]

# 🔥 Manually hardcode Smoking into the table as the coolest
risk_comparison_data.insert(0, {
    "Risk": "Smoking",
    "Danger Level": "Low",
    "Coolness Score": "High 😎"
})


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
    dbc.Col(html.H4("Risk Comparison Table", className="text-center text-light mb-3"), width=12),
]),
dbc.Row([
    dbc.Col(dash_table.DataTable(
        id='risk-comparison-table',
        columns=[{"name": col, "id": col} for col in ["Risk", "Danger Level", "Coolness Score"]],
        data=risk_comparison_data,
        style_cell={'textAlign': 'center', 'backgroundColor': '#2a2a2a', 'color': 'white'},
        style_header={
            'backgroundColor': '#1a1a1a',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{Risk} contains "smoking"', 'column_id': 'Risk'},
                'backgroundColor': '#1f77b4',
                'color': 'white',
                'fontWeight': 'bold'
            }
        ]
    ), width=12)
]),

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
    # Prepare data for animation: filter only to United States
    df_filtered = df[df['State'] == 'United States']

    # Filter out "All Causes"
    df_filtered = df_filtered[~df_filtered['Cause'].str.contains('All', case=False, na=False)]

    # ✅ Sort by Year in ascending order so the animation plays from oldest to newest
    df_filtered = df_filtered.sort_values(by='Year', ascending=True)

    # Create animated bar chart
    fig = px.bar(
        df_filtered,
        x='Cause',
        y='Deaths',
        color='Cause',
        animation_frame='Year',
        labels={'Deaths': 'Number of Deaths', 'Cause': 'Cause of Death'},
        title='Leading Causes of Death Over Time (Animated)',
    )

    # Style updates
    fig.update_layout(
        title_font_size=24,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        transition={'duration': 500},
        margin=dict(t=50, b=50, l=25, r=25)
    )

    # Optional: wider bars
    fig.update_traces(width=0.7)

    return fig





# Run the app
if __name__ == '__main__':
    app.run(debug=True)
