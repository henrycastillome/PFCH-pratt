"""Dash app."""
import os
import json
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dotenv import load_dotenv
import geopandas as gpd
import plotly.express as px
from src.function_graphs.choropletmapborough import create_choroplet_map
from src.function_graphs.markersallrestaurants import markers_allrestaurants
from src.function_graphs.criticalrestaurants import critical_restaurants
import plotly.graph_objs as go
import dash_bootstrap_components as dbc




load_dotenv()
mapbox_key = os.environ['apikey']

DATA = 'https://raw.githubusercontent.com/henrycastillome/PFCH/main/assets/restaurant_data.csv'
DATA_BARCHART = 'https://raw.githubusercontent.com/henrycastillome/PFCH/main/assets/violation_data.csv'
violation_data = pd.read_csv(DATA_BARCHART)

suppress_callback_exceptions=True

restaurants_data = pd.read_csv(DATA)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": '#313131',
    "font-family": "Be Vietnam Pro", 
    
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "NYC's restaurant inspection dataset", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Analytics", href="/", active="exact"),
                dbc.NavLink("Search bar", href="/page-1", active="exact"),
                dbc.NavLink("About", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
text_input = html.Div(
    [
        dbc.Row(
    [
        dbc.Col(dbc.Input(id='search-bar',type="search", placeholder="Type the name of your favorite restaurant")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0, id='btn-nclicks-1'
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)
    ]
)


content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
    
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)

def render_page_content(pathname):
    if pathname == "/":
        return [html.H1(children="Exploring New York City's Dirtiest Restaurants", style={'text-align': 'center'}, className='title'),
                html.Div(children=' Based on the New York City resutaurant inspection DataSet by the DOHMH', style={
                        'text-align': 'center'}),
                html.Br(),

                html.Div([
                    dcc.Graph(id='graph', style={
                            'padding-bottom': '2px', 'paddingLeft': '2px',
                            'height': '75vh', 'background-color':' #313131'})
                ], className='nine-columns'),

    html.Div([
        html.Br(),
        html.Div(id='output_data', className='graph'),
        html.Br(),
        html.Label(['Choose a graph:'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='dropdown',
            options={"All NYC restaurants": "How big is the NYC's restaurant industry?",
                     'Choroplet map': 'Check which borough is the dirtiest',
                     'All critical restaurants': 'Find the violation of your favorite restaurant in a map',
                     'Barchart': "Top 5 violations of all NYC's restaurants",
                                 'scatter': 'Find out what kind of cuisine has the worst scores'},
            value='All NYC restaurants',
            style={"width": "60%", 'color':'#000000'},
            persistence=True,

            persistence_type='memory',  # keep the current page until the tab is closed

        ),
    ], className='Three-columns') 
        ]

    elif pathname == "/page-1":
        return [
                html.Div([
                html.Br(),
                html.H1(children='Ready to find out if you want to come back to your favorite restaurant', style={'text-align':'center'}),
                html.P(id='table_out'),
                html.P(text_input),
                html.P(children='Click and drag to scroll through the table'),
                # dcc.Input(id='search-bar', type='text', placeholder='Type the name of your favorite restaurant and press enter',style={'height':'75px', 'width': '1000px', 'font-size': 35}, debounce=True, className='search-bar'),
                dcc.Graph(id='plot', style={'height':'75vh'},), ])
        
    
                ]
    elif pathname == "/page-2":
        return[
            html.Div([ 
                html.Div([
                html.H1(children="Data Visualization of New York City's Restaurant Inspection", style={'text-align':'center'}),
                html.H6(children="by Henry Castillo", style={'text-align':'center'}),
                html.Br(),
                html.P(children="Understanding the violation problem of New York City's restaurant. It uses the dataset inspection by the Deparment of Health and Mental Hygiene. " + 
                               "I was able to clean the data using python. Then, I could  plot five types of figures using plotly and show two scattermapbox, one choroplet map, one barchar and one scatterbox. Also, " + 
                               " I could add a search bar where users can type their favorite restaurant and print a table and they can see the violations the their favorite restaurant has" +
                               " And lastly, I used the library Dash to create this site", style={'text-align':'left'}),
                html.Br(),
                html.H5(children="Thanks for checking my work and let's get in touch. This is my email"),
                html.U(children="hcasti40@pratt.edu")],
                style={'background-color':'#313131', 'border-radius':'25px', 'padding':'20px'}),
                

            ])

            
        ]



@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)
def select_graph(value):
    """Function for the dropdown menu."""

    if value == 'Choroplet map':
        boro = restaurants_data[['BORO', 'CRITICAL FLAG']]
        boro = boro[(boro['CRITICAL FLAG'] != 'Not Critical')
                    & (boro['BORO'] != '0')]

        # grouping the data by borough
        boro_grouped = pd.DataFrame(
            boro.groupby('BORO')['CRITICAL FLAG'].count())

        boro_grouped = boro_grouped.reset_index()

        boro_grouped.rename(
            columns={'BORO': 'BOROUGH', "CRITICAL FLAG": 'Total Critical'}, inplace=True)

        boro_grouped.columns = list(map(str, boro_grouped.columns))
        geojson = '/Users/henrycastillomelo/Documents/Full stack Bootcamp/Course 7 Ptyhon for Data science, AI and else/Project Pratt copy/src/function_graphs/Borough Boundaries.geojson'

        with open(geojson, encoding='utf-8') as json_file:
            data_geojson = json.load(json_file)

        gdf_choroplet = (
            gpd.GeoDataFrame.from_features(data_geojson)
            .set_index('boro_name'))

        gdf_choroplet.sort_index(key=lambda x: x.str.lower(), inplace=True)

        gdf_choroplet = (gdf_choroplet.merge(boro_grouped, on=boro_grouped["BOROUGH"])
                         .assign(lat=lambda d: d.geometry.centroid.y,
                         lon=lambda d: d.geometry.centroid.x)
                         )

        categories = gdf_choroplet['BOROUGH']
        critical = gdf_choroplet['Total Critical']

        return create_choroplet_map(gdf_choroplet, categories, critical, data_geojson, mapbox_key)

    if value == "All NYC restaurants":

        res_lat = restaurants_data['Latitude']
        res_lon = restaurants_data['Longitude']
        res_name = restaurants_data['RESTAURANT']
        total_nyc = restaurants_data.shape[0]
        address = (restaurants_data[['BUILDING', 'STREET']])

        return markers_allrestaurants(res_lat, res_lon, address, res_name, total_nyc, mapbox_key)

    if value == 'All critical restaurants':

        critical_data = restaurants_data[(restaurants_data['CRITICAL FLAG'] != 'Not Critical') & (
            restaurants_data['CRITICAL FLAG'] != "Not Applicable")]

        cri_lat = critical_data['Latitude']
        cri_lon = critical_data['Longitude']
        cri_name = critical_data['RESTAURANT']
        total_cri = critical_data.shape[0]

        problem = restaurants_data['VIOLATION DESCRIPTION']

        return critical_restaurants(cri_lat, cri_lon, cri_name, total_cri, problem, mapbox_key)

    if value == 'Barchart':
        fig = px.bar(violation_data, x='VIOLATION', y='Total',
        color='VIOLATION', pattern_shape='VIOLATION'
                     )
        fig.update_layout(
            autosize=True
        )
        fig.update_layout(
        paper_bgcolor='#313131',
        plot_bgcolor='#a6a6a6',
        font_family="sans-serif",
        font_color="#969593",
        title_font_family="Be Vietnam Pro",
        title_font_color='#f1f1f1',
        font_size=16,
        legend_title_font_color='#f1f1f1',
        font=dict(
            family="Be Vietnam Pro, sans-serif",
            size=18,
            color='#969593'))
        fig.update_xaxes(title_font_family="Be Vietnam Pro")

        return fig

    if value == 'scatter':

        df_restaurant = restaurants_data

        df_restaurant = df_restaurant[df_restaurant['CRITICAL FLAG'] != "Not Applicable"]
        df_restaurant = df_restaurant[df_restaurant['CUISINE DESCRIPTION'] != "Not Applicable"]
        df_restaurant =df_restaurant[df_restaurant['GRADE'] != 'Z']
        df_restaurant = df_restaurant[df_restaurant['GRADE'] != 'N']
        df_restaurant = df_restaurant[df_restaurant['GRADE'] != 'P']
        df_restaurant.dropna(subset=['SCORE'], inplace=True)

        dataframe = df_restaurant[['CUISINE DESCRIPTION',
                        'CRITICAL FLAG', 'SCORE', 'GRADE']]

        dataframe.sort_values('CUISINE DESCRIPTION',
                              ascending=False, inplace=True)

        fig = px.scatter(dataframe, x='SCORE', y='CUISINE DESCRIPTION',
                         size='SCORE', color='GRADE', hover_name='CRITICAL FLAG')

        fig.update_layout(
        paper_bgcolor='#313131',
        plot_bgcolor='#a6a6a6',
        font_family="sans-serif",
        font_color="#969593",
        title_font_family="Be Vietnam Pro",
        title_font_color='#f1f1f1',
        font_size=16,
        legend_title_font_color='#f1f1f1',
        font=dict(
            family="Be Vietnam Pro, sans-serif",
            size=18,
            color='#969593')     )
        fig.update_xaxes(title_font_family="Be Vietnam Pro")

        return fig

@app.callback(
    Output(component_id='plot', component_property='figure'),
    [Input(component_id='search-bar', component_property='value', ),
    
    ]
)


def update_plot(search_term):

    if search_term:

        

        # filter the data based on the search term
        data_table= '/Users/henrycastillomelo/Documents/Full stack Bootcamp/Course 7 Ptyhon for Data science, AI and else/Project Pratt copy/src/function_graphs/restaurant_data_table.csv'
        df=pd.read_csv(data_table)


        filtered_df = df[df['RESTAURANT'].str.contains(search_term, case=False, na=False)]
        # Group the data by Month and compute average over arrival delay time.
    
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(filtered_df.columns),
                        fill_color='#bdbbb7',
                        align='left'),
            cells=dict(values=[filtered_df['RESTAURANT'],filtered_df['BOROUGH'], filtered_df['BUILDING'],filtered_df['STREET'], filtered_df['INSPECTION DATE'],filtered_df['VIOLATION DESCRIPTION'], filtered_df['CRITICAL FLAG']],
            fill_color='#1f1f1f',
            align='left'))
        ])
        fig.update_layout(
        paper_bgcolor='#313131',
        plot_bgcolor='#a6a6a6',
        font_family="sans-serif",
        font_color="#ffffff",
        title_font_family="Be Vietnam Pro",
        title_font_color='#f1f1f1',
        font_size=12,
        legend_title_font_color='#f1f1f1',
        font=dict(
            family="Be Vietnam Pro, sans-serif",
            size=10,
            color='#f1f1f1')     )

        return fig

       

    else:
        return {}




@app.callback(Output('plot', 'style'), [Input('search-bar', 'value')])

def hide_graph(my_input):
    if my_input:
        return {'display':'block'}
    return {'display':'none'}





if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False, host='0.0.0.0', port=8050)
