import pandas as pd

from get_dicts import get_dict_lines_for_stop, get_dict_schedule
from get_late import on_stop, get_late


def test_on_stop():
    # Przykladowe dane przystanku i linii, która się na nim zatrzymuje
    linia = 'L51'
    zespol = '2865'
    slupek = '02'
    lat = 52.086846
    lon = 21.239291

    wsp = pd.DataFrame(columns=['nazwa_zespolu', 'zespol', 'slupek', 'szer_geo', 'dlug_geo'])
    wsp_d = {'nazwa_zespolu': 'TEMP', 'zespol': zespol, 'slupek': slupek, 'szer_geo': lat, 'dlug_geo': lon}
    wsp.loc[len(wsp)] = wsp_d
    l = get_dict_lines_for_stop()

    not_on_stop = [(50.0, 20.0), (-50.0, -20.0), (52.0, 21.0)]

    actually_on_stop = [(52.086846, 21.239291), (52.086676, 21.239111), (52.0868, 21.2392)]

    for t in not_on_stop:
        assert on_stop(linia, t[1], t[0], wsp, l)[0] is False
    for t in actually_on_stop:
        assert on_stop(linia, t[1], t[0], wsp, l)[0] is True


def test_get_late():
    linia = 'L51'
    zespol = '2862'
    slupek = '01'
    godz = pd.to_datetime("2024-02-09 19:39:00")
    brygada = '1'
    d = get_dict_schedule("rozklad.csv")
    on_time = ["2024-02-09 19:39:00", "2024-02-09 19:38:01", "2024-02-09 19:39:59"]
    late = ["2024-02-09 19:38:00", "2024-02-09 19:40:00", "2024-02-09 19:44:00"]
    for x in on_time:
        assert get_late(linia, brygada, zespol, slupek, x, d)[0] is True
    for x in late:
        assert get_late(linia, brygada, zespol, slupek, x, d)[0] is True

    assert get_late("MIMOBUS", brygada, zespol, slupek, godz, d)[0] is False
    assert get_late(linia, "31415", zespol, slupek, godz, d)[0] is False
    assert get_late(linia, brygada, "31415", slupek, godz, d)[0] is False
    assert get_late(linia, brygada, zespol, "-1", godz, d)[0] is False
