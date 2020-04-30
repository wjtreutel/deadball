import json,requests
from support import Player,org_ids

## These will be passed in via argument

#print "Select Year (2005-2019)"
#selected_year = raw_input('> ')
ignore_unused_players = True

def getRoster(selected_year,selected_team):
    selected_team_name = org_ids[selected_team]
    # Root path to endpoint
    mlb_endpoint =  "http://lookup-service-prod.mlb.com/json/"

    team_request = "named.roster_team_alltime.bam?start_season={}&end_season={}&team_id={}".format(selected_year,selected_year,selected_team)

    response = requests.get(mlb_endpoint + team_request)

    # Strips out the copyright and metadata and gets straight to the good stuff
    roster = response.json()['roster_team_alltime']['queryResults']['row']

    array_of_players = []

    for player in roster:
        batting_request = "named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season={}&player_id={}".format(selected_year,player['player_id'])
        response = requests.get(mlb_endpoint + batting_request)

        number_of_teams = int(response.json()['sport_hitting_tm']['queryResults']['totalSize'])

        player_data = response.json()['sport_hitting_tm']['queryResults']

        if (number_of_teams in [0]):
            if ignore_unused_players:
                continue
            current_batting_average = "N/A"
            current_on_base_percentage = "N/A"
        elif (number_of_teams not in [0,1]):
            for team in player_data['row']:
                if team['team_full'] == selected_team_name:
                    current_batting_average = team['avg']
                    current_on_base_percentage = team['obp']
        else:
            try:
                current_batting_average = player_data['row']['avg']
                current_on_base_percentage = player_data['row']['obp']
            except: 
                print "Error when retrieving data for {} ({})".format(player['name_first_last'],player['player_id'])

        current_first_name,current_last_name = player['name_first_last'].split()

        current_player = Player(player['player_id'],player['jersey_number'],player['primary_position'],current_first_name,current_last_name,current_batting_average,current_on_base_percentage)
        array_of_players.append(current_player)


    for pitcher in array_of_players:
        if pitcher.position not in ['P']:
            continue
        pitching_request = "named.sport_pitching_tm.bam?league_list_id='mlb'&game_type='R'&season={}&player_id={}".format(selected_year,pitcher.id)
        response = requests.get(mlb_endpoint + pitching_request)

        number_of_teams = int(response.json()['sport_pitching_tm']['queryResults']['totalSize'])

        pitching_data = response.json()['sport_pitching_tm']['queryResults']

        if (number_of_teams in [0]):
            if ignore_unused_players:
                continue
            current_earned_run_average = "N/A"
        elif (number_of_teams not in [0,1]):
            for team in pitching_data['row']:
                if team['team_full'] == selected_team_name:
                    current_earned_run_average = team['era']
        else:
            try:
                current_earned_run_average = pitching_data['row']['era']
            except:
                print "Error retrieving pitching data for {} ({})".format(pitcher.full_name,pitcher.id)
        pitcher.setERA(current_earned_run_average)

    return array_of_players



oakland = getRoster(2010,133)

for player in oakland:
    player.display()

mariners = getRoster(2018,136)

for player in mariners:
    player.display()
