def get_live_positions(time_frame, name='live_pos.csv'):
    from time import sleep
    import requests
    import pandas as pd

    url = ('https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=%20f2e5503e-927d-4ad3-9500-4ab9e55deb59'
           '&apikey=9633bd3b-1bf3-4a28-9802-16691f479f25&type=1')

    # time_frame = 1  # w godzinach
    time_frame *= 3600
    time_frame += 60  # na zapas

    df = pd.DataFrame(columns=['Lines', 'VehicleNumber', 'Time', 'Lon', 'Lat', 'Brigade'])
    licz = 0
    err = False
    while licz < time_frame + 60:
        if not err:
            sleep(10)
            licz += 10
        else:
            sleep(1)
            licz += 1
        response = requests.get(url)

        lista = response.json()['result']
        response.raise_for_status()
        if response.status_code == 204 or (type(lista) == str):
            print(f"{licz} BLAD")
            err = True
            continue
        err = False
        df2 = pd.DataFrame(lista, columns=['Lines', 'VehicleNumber', 'Time', 'Lon', 'Lat', 'Brigade'])
        df = pd.concat([df, df2], ignore_index=True)

    df = df.reset_index(drop=True)

    df.to_csv(name, index=False)
