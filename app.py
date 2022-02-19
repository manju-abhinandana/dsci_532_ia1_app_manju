import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

url = 'https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv'
gapminder = pd.read_csv(url,parse_dates=['year'])

gapminder['year'] = gapminder['year'].dt.year
gapminder = gapminder[(gapminder['year'] >= 2000)]

def plot_altair(region, year):
    chart = alt.Chart(gapminder.loc[(gapminder['region'] == region) & (gapminder['year'] == year)]).mark_point().encode(
        x = 'life_expectancy',
        y = 'income',
        color='country',
        size='population',
        tooltip=['country','population']).interactive().properties(title = "Life expectancy vs income")
    return chart.to_html()


app.layout = html.Div([
    html.H3('Gapminder data visualization: Income versus Life expectancy'),
    html.P('Region'),
    dcc.Dropdown(
        id='region_dropdown',
        options=[{'label': i, 'value': i} for i in gapminder.region.unique()]),
    html.P('Year'),
    dcc.Dropdown(
        id='year_dropdown',
        options=[{'label': i, 'value': i} for i in gapminder.year.unique()]),  
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'},
        srcDoc=plot_altair(region = gapminder.region.unique()[0], 
        year = gapminder.year.unique()[0]))])


@app.callback(
    Output('scatter', 'srcDoc'),
    Input('region_dropdown', 'value'),
    Input('year_dropdown', 'value'))
def update_output(region, year):
    return plot_altair(region, year)

if __name__ == '__main__':
    app.run_server(debug=True)