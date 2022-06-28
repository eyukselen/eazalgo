import folium
import pandas

"""This application creates a map of the US using Folium and adds markers and elevation data to the map for each Volcanoe in the data set and highlights by color
the population count. It then saves the map to a html file"""

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])


def color_producer(elevation):
    """This function calculates the color of the marker based on the elevation of volcanoes"""
    if elevation < 1000:
        return "green"
    elif elevation < 3000:
        return "orange"
    else:
        return "red"


# Starting point of the map
map = folium.Map(location=[52.56157704007144, -1.9003425849320994], zoom_start=1)

fgv = folium.FeatureGroup(name="Volcanoes")

fg = folium.FeatureGroup(name="My Map")
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            radius=8,
            popup=str(el) + "m",
            fill_color=color_producer(el),
            color="grey",
            fill_opacity=0.7,
        )
    )


fgp = folium.FeatureGroup(name="Population")

fg.add_child(
    folium.GeoJson(
        data=open("world.json", "r", encoding="utf-8-sig").read(),
        style_function=lambda x: {
            "fillColor": "green"
            if x["properties"]["POP2005"] < 10000000
            else "orange"
            if 10000000 <= x["properties"]["POP2005"] < 20000000
            else "red"
        },
    )
)


map.add_child(fg)
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl(position="bottomright"))
map.save("map1.html")
