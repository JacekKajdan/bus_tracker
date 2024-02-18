def on_stop(linia, lon, lat, wsp, lines_for_stops):
    from geopy.distance import distance

    dist_buffer = 25

    for x in wsp.index:
        try:
            if linia in lines_for_stops[wsp['zespol'][x]][wsp['slupek'][x]]:
                dist = distance((lat, lon), (wsp['szer_geo'][x], wsp['dlug_geo'][x])).meters
                if dist < dist_buffer:
                    return (True, wsp['zespol'][x], wsp['slupek'][x], wsp['szer_geo'][x], wsp['dlug_geo'][x])
        except KeyError as e:
            continue
    return (False,)


def map_generation(res):
    from folium import folium
    from folium.plugins import FastMarkerCluster

    lat = [float(a[8]) for a in res]
    lon = [float(a[9]) for a in res]
    mapa = folium.Map(location=[sum(lat) / len(lat), sum(lon) / len(lon)], zoom_start=13)

    coords = list(zip(lat, lon))

    FastMarkerCluster(coords).add_to(mapa)

    mapa.show_in_browser()


def get_late(line, brigade, stop, stopNr, arrived, d):
    from datetime import datetime, date
    import pandas as pd

    if line not in d.keys():
        return (False,)
    if brigade not in d[line].keys():
        return (False,)
    if stop not in d[line][brigade].keys():
        return (False,)
    if stopNr not in d[line][brigade][stop].keys():
        return (False,)

    arr = pd.to_datetime(arrived).time()
    times = [pd.to_datetime(x).time() for x in d[line][brigade][stop][stopNr]]

    for i in range(0, len(times) - 1):
        if times[i] <= arr < times[i + 1]:
            return (
                True, (datetime.combine(date.today(), arr) - datetime.combine(date.today(), times[i])).total_seconds(),
                times[i])

    if times[len(times) - 1] <= arr:
        return (True, (datetime.combine(date.today(), arr) - datetime.combine(date.today(),
                                                                              times[len(times) - 1])).total_seconds(),
                times[len(times) - 1])
    return (False,)


def get_late_line(live_pos, line, generate_map=True):
    import pandas as pd
    from get_dicts import get_dict_lines_for_stop, get_dict_stop_names, get_dict_schedule

    wsp = pd.read_csv('wspolrzedne.csv',
                      converters={'nazwa_zespolu': str, 'zespol': str, 'slupek': str, 'szer_geo': float,
                                  'dlug_geo': float})
    l = get_dict_lines_for_stop()
    df = pd.read_csv(live_pos,
                     converters={'Lines': str, 'VehicleNumber': str, 'Time': str, 'Lon': float, 'Lat': float,
                                 'Brigade': str})
    d = get_dict_schedule("rozklad.csv")

    captured = []
    for index, row in df.iterrows():
        if row['Lines'] != line:
            continue

        stop = on_stop(row['Lines'], row['Lon'], row['Lat'], wsp, l)
        if stop[0]:
            late = get_late(row['Lines'], row['Brigade'], stop[1], stop[2], row['Time'], d)
            if late[0] and 60 <= late[1] <= 300:
                print(
                    f'{row["Lines"]} {stop[1]} {stop[2]} Schedule: {late[2]} Arrived: {row["Time"]} Late: {int(late[1] // 60)}min {int(late[1] % 60)}s {row["Brigade"]}')
                captured.append((row['Lines'], row['VehicleNumber'], row['Brigade'], stop[1], stop[2], late[2],
                                 row['Time'], late[1], stop[3], stop[4]))

    captured = sorted(captured)
    res = []
    if len(captured) > 0:
        res.append(captured[0])
    for i in range(1, len(captured)):
        for j in range(6):
            if captured[i][j] != captured[i - 1][j]:
                res.append(captured[i])
                break

    names = get_dict_stop_names()
    avg = 0
    for x in res:
        avg += x[7]
        print(
            f'Autobus nr {x[1]} linii {x[0]} dojechał na przytanek {names[x[3]]} {x[4]} z opóźnieniem {int(x[7] // 60)}min {int(x[7] % 60)}s o godzinie {pd.to_datetime(x[6]).time()} (Planowy przyjazd: {x[5]})')

    print(
        f'Średnie opóżnienie linii {line} to {int(int((avg / len(res))) // 60)}min {int(int((avg / len(res))) % 60)}s')

    if generate_map:
        map_generation(res)

