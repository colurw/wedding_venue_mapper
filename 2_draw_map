import plotly.express as px
import pickle

# load pickled file
with open('pickled/df_venues.pkl', 'rb') as file:
     df_venues = pickle.load(file)

# filter dataframe according to search term
search_term = input("\n >>> Enter search term, or press ENTER for all: ").upper()
df_filtered = df_venues[df_venues["name"].str.contains(search_term)]

# generate map in browser
fig = px.scatter_mapbox(data_frame=df_filtered, 
                        lat="latitude", 
                        lon="longitude", 
                        text="name",
                        hover_data="phone", 
                        color_discrete_sequence=["fuchsia"],
                        zoom=5, 
                        height=600)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
