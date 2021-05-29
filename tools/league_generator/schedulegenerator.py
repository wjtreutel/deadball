from leaguefunctions import *


curr_league = new_league("Example Baseball League",generate_names(6))

curr_league.simulate_year(2020)

curr_league.display_historic_standings(2020)
