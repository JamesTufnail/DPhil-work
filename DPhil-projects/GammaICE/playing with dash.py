from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.io as pio

###### Functions ######
# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ],
#         style = {'width': '50%'}
#         ),
        
#     ])


# Initialise
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # External CSS stylesheet
app = Dash(__name__) # Dash constructor - creates a new Dash application
pio.templates.default = 'plotly_white' # Setting the default template for the plots

# Read in the data
hist_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
scat_data = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Define figures

fig2 = px.scatter(scat_data, x = 'gdp per capita', y = 'life expectancy',
                  size = 'population', color = 'continent', hover_name = 'country',
                  log_x = True, size_max = 60, title = 'Gapminder 2007')



# Represents the components that will be displayed in the web browser, normally within a html.Div
# Has 'components' that are children of the 'layout' component
# id are set and used in callbacks
app.layout = html.Div([
    html.H1(
        children='Big Data Analytics - Dash App', # Text that will be displayed
        style={'textAlign': 'center', # CSS styling
               'color': colors['text'],
               'fontSize': 50} # Font size
    ),
    html.Div(className='row', children='An app that has interactive components!',
             style={'textAlign': 'center',
                     'color': colors['text'],
                     'fontSize': 30}), # Using CSS to style the text
    html.Hr(), # draws horizontal rule
    html.Div(className='row', children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                        value='lifeExp',
                        id='controls-and-radio-buttons')],
                        style = {'color': 'blue', 'fontSize': 20}    
            ),
    html.Div(className='row', children=[
        dash_table.DataTable(data=hist_data.to_dict('records'), page_size=10)],
        style={'width': '50%', 'display': 'inline-block'}
    ),
        # dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
    html.Div(className='row', children=[
        dcc.Graph(figure={}, id='controls-and-graph')],
        style={'width': '50%', 'display': 'inline-block'}),

    html.Hr(),

    # generate_table(hist_data),
    html.Div(className='row', children=[
        dash_table.DataTable(data=scat_data.to_dict('records'), page_size=10)],
        style={'width': '50%', 'display': 'inline-block'}
    ),

    html.Div(className='row', children=[
        dcc.Graph(figure=fig2, id='scatter-plot')],
        style={'width': '50%', 'display': 'inline-block'}),
    
    
    ])



# # Creating callback to interact between the radio buttons and the graph
# # @app.callback(
# #     Output(component_id='controls-and-graph', component_property='figure'), # Setting the components property that will be updated
# #     Input(component_id='controls-and-radio-buttons', component_property='value') # Setting component property that will trigger the callback
# # )

# # function that is 'decorated' by the callback
# # Meaning this will be calld implicity when the input component property is changed (i.e. the callback is triggered)
# # def update_graph(col_chosen):
# #     fig = px.histogram(hist_data, x='continent', y=col_chosen, histfunc='avg')

# #     # fig.update_layout(
# #     #     plot_bgcolor=colors['background'],
# #     #     paper_bgcolor=colors['background'],
# #     #     font_color=colors['text']
# #     # )
# #     return fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

