def get_lines(zespol, slupek):
    import requests
    import time

    url = (f'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId'
           f'={zespol}&busstopNr={slupek}&apikey=9633bd3b-1bf3-4a28-9802-16691f479f25')
    response = requests.get(url)
    l = response.json()['result']
    while type(l) == str:
        print("Blad")
        time.sleep(30)
        response = requests.get(url)
        l = response.json()['result']

    lines_list = []
    for x in l:
        if type(x) != str:
            lines_list.append(x['values'][0]['value'])

    return lines_list


def get_przystanki(nazwa='przystanki.csv'):
    import requests
    import pandas as pd

    url = "https://api.um.warszawa.pl/api/action/public_transport_routes/?apikey=9633bd3b-1bf3-4a28-9802-16691f479f25"

    response = requests.get(url)

    d = response.json()['result']
    df = pd.DataFrame(columns=['nr_zespolu', 'nr_przystanku'])

    for x1 in d.values():
        for x2 in x1.values():
            for x3 in x2.values():
                row = {'nr_zespolu': x3['nr_zespolu'], 'nr_przystanku': x3['nr_przystanku']}
                good = True
                for i in df.index:
                    if df['nr_zespolu'][i] == row['nr_zespolu'] and df['nr_przystanku'][i] == row['nr_przystanku']:
                        good = False
                        break
                if good:
                    df.loc[len(df)] = row

    df.to_csv(nazwa, index=False)


def get_wspolrzedne(nazwa='wspolrzedne.csv'):
    import requests
    import pandas as pd

    url = ("https://api.um.warszawa.pl/api/action/dbstore_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey=9633bd3b"
           "-1bf3-4a28-9802-16691f479f25")

    response = requests.get(url)

    l = response.json()['result']
    df = pd.DataFrame(columns=['nazwa_zespolu', 'zespol', 'slupek', 'szer_geo', 'dlug_geo'])

    for x1 in l:
        row = {'nazwa_zespolu': '', 'zespol': '', 'slupek': '', 'szer_geo': '', 'dlug_geo': ''}
        for x2 in x1['values']:
            if x2['key'] in row.keys():
                row[x2['key']] = x2['value']
        df.loc[len(df)] = row

    df.to_csv(nazwa, index=False)


def get_rozklad(nazwa='rozklad.csv'):
    import requests
    import pandas as pd
    import time

    dfp = pd.read_csv('przystanki.csv', converters={'nr_zespolu': str, 'nr_przystanku': str})
    df = pd.DataFrame(columns=['linia', 'trasa', 'brygada', 'zespol', 'slupek', 'czas'])

    for x in dfp.index:
        lines_list = get_lines(dfp['nr_zespolu'][x], dfp['nr_przystanku'][x])

        row = {'zespol': dfp['nr_zespolu'][x], 'slupek': dfp['nr_przystanku'][x]}

        for line in lines_list:

            row['linia'] = line
            url = (f"https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238"
                   f"&busstopId={dfp['nr_zespolu'][x]}&busstopNr={dfp['nr_przystanku'][x]}&line={line}&apikey"
                   f"=9633bd3b-1bf3-4a28-9802-16691f479f25")
            response = requests.get(url)
            l = response.json()['result']

            while type(l) == str:
                time.sleep(3)
                response = requests.get(url)
                l = response.json()['result']

            for y in l:
                for z in y['values']:
                    if z['key'] == 'czas':
                        row['czas'] = z['value']
                    if z['key'] == 'trasa':
                        row['trasa'] = z['value']
                    if z['key'] == 'brygada':
                        row['brygada'] = z['value']
                df.loc[len(df)] = row

    df.to_csv(nazwa, index=False)

