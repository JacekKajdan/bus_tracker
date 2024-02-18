def calculate_vel(time_start, time_end, lon1, lat1, lon2, lat2):
    from geopy import distance
    delta = (time_end - time_start).total_seconds() / 3600
    dist = distance.distance((lon1, lat1), (lon2, lat2)).km
    return dist / delta


def get_speeding(data, target_name):
    import pandas as pd

    df = pd.read_csv(data, converters={'Lines': str, 'VehicleNumber': str, 'Time': str, 'Lon': float, 'Lat': float,
                                       'Brigade': str})

    df_res = pd.DataFrame(columns=['Lines', 'VehicleNumber', 'Lon', 'Lat', 'Velocity'])
    print(len(df.index))
    for id in range(1, len(df.index)):

        if df['VehicleNumber'][id] == df['VehicleNumber'][id - 1] and df['Lines'][id] == df['Lines'][id - 1]:
            time_start = pd.to_datetime(df['Time'][id - 1])
            time_end = pd.to_datetime(df['Time'][id])
            vel = calculate_vel(time_start, time_end, df['Lon'][id - 1], df['Lat'][id - 1], df['Lon'][id],
                                df['Lat'][id])

            if 50 < vel < 100:  # 100 przyjęte jako maksymalna realna prędkość
                row = {'Lines': df['Lines'][id], 'VehicleNumber': df['VehicleNumber'][id], 'Lon': df['Lon'][id],
                       'Lat': df['Lat'][id], 'Velocity': vel}
                df_res.loc[len(df_res)] = row
    df_res.to_csv(target_name, index=False)

