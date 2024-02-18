def get_dict_schedule(schedule):
    import pandas as pd

    df = pd.read_csv(schedule,
                     converters={'linia': str, 'trasa': str, 'brygada': str, 'zespol': str, 'slupek': str, 'czas': str})
    d = {}
    for x in df.index:
        lin = df['linia'][x]
        bry = df['brygada'][x]
        zesp = df['zespol'][x]
        slu = df['slupek'][x]
        if lin not in d.keys():
            d[lin] = {}
        if bry not in d[lin].keys():
            d[lin][bry] = {}
        if zesp not in d[lin][bry].keys():
            d[lin][bry][zesp] = {}
        if slu not in d[lin][bry][zesp].keys():
            d[lin][bry][zesp][slu] = []
        d[lin][bry][zesp][slu].append(df['czas'][x])
    return d


def get_dict_lines_for_stop():
    import pandas as pd

    df = pd.read_csv('rozklad.csv',
                     converters={'linia': str, 'trasa': str, 'brygada': str, 'zespol': str, 'slupek': str, 'czas': str})
    d = {}
    for x in df.index:
        lin = df['linia'][x]
        zesp = df['zespol'][x]
        slu = df['slupek'][x]
        if zesp not in d.keys():
            d[zesp] = {}
        if slu not in d[zesp].keys():
            d[zesp][slu] = []
        if lin not in d[zesp][slu]:
            d[zesp][slu].append(lin)
    return d


def get_dict_stop_names():
    import pandas as pd

    wsp = pd.read_csv('wspolrzedne.csv',
                      converters={'nazwa_zespolu': str, 'zespol': str, 'slupek': str, 'szer_geo': float,
                                  'dlug_geo': float})
    d = {}
    for index, row in wsp.iterrows():
        d[row['zespol']] = row['nazwa_zespolu']
    return d
