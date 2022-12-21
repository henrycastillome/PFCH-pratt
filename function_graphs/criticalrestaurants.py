"""module for the dash app"""
import plotly.graph_objects as go



def critical_restaurants(cri_lat, cri_lon, cri_name, total_cri, problem, mapbox_key):
    """function that creates a scatter mapbox """
    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=cri_lat,
        lon=cri_lon,
        mode='markers',

        marker=go.scattermapbox.Marker(
            size=12,
            color='rgb(255, 0, 0)',
            opacity=0.7),


    ))

    fig.add_trace(go.Scattermapbox(
        lat=cri_lat,
        lon=cri_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=4,
            color='rgb(255, 255, 0)',
            opacity=0.7,

        ),

        text=problem,
        hoverinfo='text',
        hovertext=cri_name,
        hovertemplate='<b>%{hovertext}<b>' +
        '<br><sup>%{text}<sup><br>'


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
            text=f"<b>Zoom in to find your favorite restaurant and Hover to see its violations<b> <br><sup>{total_cri:,d} Total in critical situation</sup>",
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
