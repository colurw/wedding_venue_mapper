import plotly.express as px
import pickle

# load pickled file
with open('pickled/df_venues.pkl', 'rb') as file:
     df_venues = pickle.load(file)

# search parameters
SEARCH_TERMS = "farm|meadow| field|glebe|lea|marsh|park|tipi|tepee|canvas|yurt|holiday|festival|camp|outdoor|glamp"
DROP_TERMS = "holiday inn|hotel|golf"
MAX_DIST_TO_STATION = 10
MAX_DIST_TO_AIRPORT = 50

# filter dataframe according to search parameters
df_venues = df_venues[df_venues["name"].str.contains(SEARCH_TERMS.upper())]
df_venues = df_venues[df_venues["name"].str.contains(DROP_TERMS.upper()) == False]
df_venues = df_venues[df_venues["station"] <= MAX_DIST_TO_STATION]
df_venues = df_venues[df_venues["airport"] <= MAX_DIST_TO_AIRPORT]
print(df_venues.shape[0], "venues found")

# generate map in browser
fig = px.scatter_mapbox(data_frame=df_venues, 
                        lat="latitude", 
                        lon="longitude", 
                        text="name",
                        hover_data=["phone", "station", "airport"],
                        color_discrete_sequence=["fuchsia"],
                        zoom=5, 
                        height=600)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
