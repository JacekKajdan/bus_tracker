def cleanup(source, target_name, start, end):
    import pandas as pd

    df = pd.read_csv(source,
                     converters={'Lines': str, 'VehicleNumber': str, 'Time': str, 'Lon': float, 'Lat': float,
                                 'Brigade': str})

    df = df.sort_values(['VehicleNumber', 'Time'])
    df = df.reset_index(drop=True)

    do_usuniecia = []
    for id in range(1, len(df.index)):
        if df['VehicleNumber'][id] == df['VehicleNumber'][id - 1] and df['Time'][id] == df['Time'][id - 1]:
            do_usuniecia.append(id)
    df = df.drop(index=do_usuniecia)
    df = df.reset_index(drop=True)

    dt = pd.to_datetime(start)
    dt2 = pd.to_datetime(end)

    do_usuniecia = []
    for id in df.index:
        try:
            dt_cur = pd.to_datetime(df['Time'][id])
            if dt > dt_cur or dt_cur > dt2:
                do_usuniecia.append(id)
        except Exception as e:
            do_usuniecia.append(id)

    df = df.drop(index=do_usuniecia)
    df = df.reset_index(drop=True)

    df.to_csv(target_name, index=False)
