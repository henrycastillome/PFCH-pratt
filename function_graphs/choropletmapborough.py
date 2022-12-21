"""Module os operating system interfaces."""
import os
import plotly.graph_objects as go
from dotenv import load_dotenv


load_dotenv()
mapbox_key = os.environ['apikey']

def create_choroplet_map(gdf_choroplet, categories, critical, data_geojson, mapbox_key): 
	"""Function that creates a choroplet map."""
    
	fig =go.Figure() 
	fig.add_traces(go.Choroplethmapbox(
		geojson=data_geojson,
		locations=categories,
		featureidkey="properties.boro_name",
		z=critical,
		colorscale="YlOrRd",
		marker_opacity=0.7,
		marker_line_width=0,
		hovertext=categories,
		text=critical,
		hoverinfo='text',

		hovertemplate='<b>%{hovertext}<b>' +
		'<br><extra>%{text:,d}</extra><br>'
	))
    # fig.add_trace(go.Scattermapbox(
    # 		lat=gdf_choroplet.geometry.centroid.y,
    # 		lon=gdf_choroplet.geometry.centroid.x,
    # 		mode='text',
    # 		textfont={"color":"black","size":16, "family":"Arial Black"},
    # 		text=categories,
    # 		showlegend=False,
    # 		hoverinfo='skip'))
	fig.update_layout(
		autosize=True,
		hovermode='closest',
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
		)
	)

	fig.update_layout(
		title=go.layout.Title(
		text="Is your borough the dirtiest? hover and find out the total",
		xref="paper",
		x=0
	),
		font_family="sans-serif",
		font_color=" #969593",
		title_font_family="Be Vietnam Pro",
		title_font_color='#f1f1f1',
		font_size=16,
	)
	fig.update_layout(
		paper_bgcolor='#313131',
)
	return fig