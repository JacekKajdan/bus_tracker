# Dokumentacja

# I. cleanup.py
## cleanup(source, target_name, start, end)
Porządkuje dane na żywo o autobusach - sortuje po numerze autobusu i czasie pobrania danych
oraz usuwa dane spoza zakresu [start,end] i powtórzenia.
- source - plik źródłowy (.csv)
- target_name - plik docelowy (.csv)
- start - początkowa godzina potrzebnych danych
- end - końcowa godzina potrzebnych danych

# II. get_bus_info.py
## get_lines(zespol, slupek)
Zwraca listę linii autobusowych przejeżdzających przez dany przystanek
- zespol - numer zespolu
- slupek - numer słupka

## get_przystanki(nazwa='przystanki.csv')
Zapisuje do pliku .csv numery zespołów i słupków wszystkich przystanków
- nazwa - plik docelowy (.csv)

## get_wspolrzedne(nazwa='wspolrzedne.csv')
Zapisuje do pliku .csv numery, lokalizacje i nazwy wszytkich przystanków
- nazwa - plik docelowy (.csv)

## get_rozklad(nazwa='rozklad.csv')
Zapisuje do pliku .csv rozkład jazdy wszystkich autobusów
- nazwa - plik docelowy (.csv)

# III. get_dicts.py
## get_dict_schedule(schedule)
Zwraca słownik stworzony na podstawie rozkładu jazdy

- shcedule - plik .csv zawierający rozkład jazdy

## get_dict_lines_for_stop()
Zwraca słownik w którym dla każdego przystanku przechowywana jest lista linii przez niego przejeżdzających

## get_dict_stop_names()
Zwraca słownik, który dla każdego klucza (zespołu przystanków) przechowuje jego nazwę

# IV. get_late.py

## on_stop(linia, lon, lat, wsp, lines_for_stops)
Wykrywa czy dany autobus znajduje się na jakimś przystanku i jeżeli tak jest zwraca dane tego przystanku

- linia - linia sprawdzanego autobusu
- lon - długość geograficzna autobusu
- lat - szerokość geograficzna autobusu
- wsp - DataFrame przechowujący dane pozyskane z get_wspolrzedne
- lines_for_stops - słownik pozyskany z get_dict_lines_for_stop

## map_generation(res):
Generuje mapę z przystankami na których dochodziło do opóźnień

- res - lista danych o spóźnionych autobusach (generowana w get_late_line())

## get_late(line, brigade, stop, stopNr, arrived, d)
Wykrywa czy dany autobus spóźnił się na swój przystanek i jeśli tak to o ile
- line - linia autobusu
- brigade - brygada autobusu
- stop - numer zespołu
- stopNr - numer słupka
- arrived - godzina o której autobus dotarł na przystanek
- d - rozkład w fromie słownika (z get_dict_schedule())
## get_late_line(live_pos, line, generate_map=True)
Wypisuje wszystkie opóźnienia autobusów danej linii, ich średnie opóźnienie i opcjonalnie nanosi opóźnienia na mapę
- live_pos - plik przechowujący dane o pozycjach autobusów na żywo
- line - linia którą analizujemy
- generate_map - czy chcemy wygenerowania mapy opóźnień


# V. get_live_positions.py
## get_live_positions(time_frame, name='live_pos.csv')
Pobiera dane o aktualnych pozycjach autobusów w Warszawie
- time_frame - przez jaki czas mają być pobierane dane (w godzinach)
- name - nazwa docelowego pliku (.csv)

# VI. speeding.py
## calculate_vel(time_start, time_end, lon1, lat1, lon2, lat2)
Oblicza prędkość danego autobusu na podstawie jego lokalizacji i czasu między pomiarami
- time_start - początek rozpatrywanego fragmentu przejazdu
- time_end - koniec rozpatrywanego fragmentu przejazdu
- lon1, lat1 - współrzędne punktu startowego
- lon2, lat2 - współrzędne punktu końcowego

## get_speeding(data, target_name)
Na podstawie pozycji na żywo autobusów zapisuje do pliku .csv dane o przekroczeniach prędkości
- data - dane o lokalizacjach autobusów (plik .csv)
- dane wyjściowe (.csv)

# VII. speeding_map.py
## show_speeding_map(name)
Pokazuje mapę z miejscami w których przekraczano prędkość
- name - nazwa pliku .csv zawierającego dane o przekroczeniach prędkości (z get_speeding())
## show_n_speeding_clusters(num_clusters, name)
Pokazuje mapę z zaznaczonymi num_clusters miejscami w których średnio najczęściej przekraczano prędkość
- num_clusters - liczba miejsc do oznaczenia
- name - nazwa pliku .csv zawierającego dane o przekroczeniach prędkości (z get_speeding())

# VIII. example.py
Plik pokazujący przykładowe zastosowanie tychże funkcji (funkcje nie użyte w tym programie
są pomocnicze i nie ma potrzeby aby wywoływał je użytkownik)