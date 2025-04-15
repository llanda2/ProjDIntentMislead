# callbacks.py
from dash import Input, Output
import plotly.express as px

def register_callbacks(app, df):
    @app.callback(
        Output('smoking-deaths-count', 'children'),
        Input('year-dropdown', 'value')
    )
    def update_smoking_deaths(selected_year):
        return f"Total Smoking Deaths in {selected_year}: 0"

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
