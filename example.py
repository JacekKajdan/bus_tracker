from cleanup import cleanup
from get_bus_info import get_przystanki, get_wspolrzedne, get_rozklad
from get_late import get_late_line
from get_live_positions import get_live_positions
from speeding import get_speeding
from speeding_map import show_speeding_map, show_n_speeding_clusters

# Pobranie danych o lokalizacji autobusów
get_live_positions(1, 'morning.csv')

# Uporządkowanie tychże danych (sortowanie i usunięcie tych spoza zakresu czasowego i powtórek)
cleanup("morning.csv", "morning_clean.csv", "2024-02-09 07:00:00", "2024-02-09 08:00:00")

# Pobranie pozostałych potrzebnych danych
get_przystanki()
get_wspolrzedne()
get_rozklad()

# Analiza danych o przekroczeniach prędkości
get_speeding("morning_clean.csv", "morning_speeding.csv")
show_speeding_map("morning_speeding.csv")
show_n_speeding_clusters(30, "morning_speeding.csv")

# Analiza danych o spóźnieniach autobusów linii 208
get_late_line("morning_clean.csv", 208, True)
