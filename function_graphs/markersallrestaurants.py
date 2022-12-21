"""function for the dash app"""


import plotly.graph_objects as go




def markers_allrestaurants(res_lat, res_lon, address, res_name, total_nyc, mapbox_key):
    """function that creates a scatter mapbox with all restaurants"""

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=res_lat,
        lon=res_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(51, 153, 255)',
            opacity=0.7
        ),

    ))

    fig.add_trace(go.Scattermapbox(
        lat=res_lat,
        lon=res_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=4,
            color='rgb(51, 153, 255)',
            opacity=0.7,

        ),
        text=address,
        hoverinfo='text',
        hovertext=res_name,
        hovertemplate='<b>%{hovertext}<b>' +
        '<br><extra>%{text}</extra><br>'

    ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_key,
            bearing=0,
            center=dict(
                lat=40.730610,
                lon=-73.935242
            ),
            pitch=0,
            zoom=9,
            style='light'
        ),
    )
    fig.update_layout(

        title=go.layout.Title(
            text=f"<b>How big is the NYC's restaurant industry? <b> <br><sup>{total_nyc:,d} Total" ,
            xref="paper",
            x=0
        ),
        font_family="sans-serif",
        font_color="blue",
        title_font_family="Be Vietnam Pro",
        title_font_color='#f1f1f1',
        font_size=16,
    )

    fig.update_layout(
        paper_bgcolor='#313131',

    )

    return fig

# total_restaurants=(restaurants_data.shape[0])


# site_lat = restaurants_data['Latitude']
# site_lon = restaurants_data['Longitude']
# locations_name = restaurants_data['RESTAURANT']

# markers_allrestaurants(site_lat, site_lon, locations_name, total_restaurants)
