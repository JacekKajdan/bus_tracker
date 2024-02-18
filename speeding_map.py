def show_speeding_map(name):
    import folium
    import pandas as pd
    from folium.plugins import FastMarkerCluster

    mapa = folium.Map(location=[52.237049, 21.017532], zoom_start=11)

    df = pd.read_csv(name)

    coords = list(zip(df['Lat'], df['Lon']))

    FastMarkerCluster(coords).add_to(mapa)

    mapa.show_in_browser()


def show_n_speeding_clusters(num_clusters, name):
    import folium
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans

    df = pd.read_csv(name,
                     converters={'Lines': str, 'VehicleNumber': str, 'Lon': float, 'Lat': float, 'Velocity': float})
    X = df['Lon']
    y = df['Lat']

    dane = np.array([np.array(X).reshape(-1, 1), np.array(y).reshape(-1, 1)]).reshape(2, 44981).T

    kmeans = KMeans(n_clusters=num_clusters, random_state=2, n_init=10)
    kmeans.fit(dane)

    mapa = folium.Map(location=[52.237049, 21.017532], zoom_start=11)
    for center in kmeans.cluster_centers_:
        center = center[:2]
        folium.Marker((center[1], center[0])).add_to(map)
    mapa.show_in_browser()

