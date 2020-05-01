import json,requests

def extractStatistics(player_data,desired_statistics,desired_team):
    result = []
    number_of_teams = int(player_data['totalSize'])

    if (number_of_teams < 1):
        for i in desired_statistics:
            result.append('N/A')
    elif (number_of_teams not in [0,1]):
        for team in player_data['row']:
            if team['team_id'] == desired_team:
                for stat in desired_statistics:
                    result.append(team[stat])
            return result
    else:
        try:
            for stat in desired_statistics:
                result.append(player_data['row'][stat])
        except: 
            print "Error when retrieving {} for player #{}".format(desired_statistics,player_data['row']['player_id'])
    return result


        

def getRoster(selected_year,selected_team):
    roster = dict()
    roster['org_id'] = selected_team
    roster['year'] = selected_year

    # Root path to endpoint
    mlb_endpoint =  "http://lookup-service-prod.mlb.com/json/"
    team_request = "named.roster_team_alltime.bam?start_season={}&end_season={}&team_id={}".format(selected_year,selected_year,selected_team)

    response = requests.get(mlb_endpoint + team_request)

    # Strips out the copyright and metadata and gets straight to the good stuff
    player_list = response.json()['roster_team_alltime']['queryResults']['row']

    array_of_players = []

    for player in player_list:
        batting_request = "named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season={}&player_id={}".format(selected_year,player['player_id'])
        response = requests.get(mlb_endpoint + batting_request)


        number_of_teams = int(response.json()['sport_hitting_tm']['queryResults']['totalSize'])

        player_data = response.json()['sport_hitting_tm']['queryResults']
        try:
            current_on_base_percentage,slg,current_batting_average = extractStatistics(player_data,['obp','slg','avg'],selected_team)
        except:
            current_on_base_percentage,slg,current_batting_average = ['N/A','N/A','N/A']


        current_player = dict()
        current_first_name,current_last_name = player['name_first_last'].split()
        current_player['batting_average'] = current_batting_average
        current_player['on_base_percentage'] = current_on_base_percentage
        current_player['id'] = player['player_id'] 
        current_player['jersey'] = player['jersey_number']
        current_player['position'] = player['primary_position']
        current_player['first_name'] = current_first_name
        current_player['last_name'] = current_last_name
        array_of_players.append(current_player)

        
    for pitcher in array_of_players:
        if pitcher['position'] not in ['P']:
            continue
        pitching_request = "named.sport_pitching_tm.bam?league_list_id='mlb'&game_type='R'&season={}&player_id={}".format(selected_year,pitcher['id'])
        response = requests.get(mlb_endpoint + pitching_request)

        number_of_teams = int(response.json()['sport_pitching_tm']['queryResults']['totalSize'])

        try:
            pitching_data = response.json()['sport_pitching_tm']['queryResults']
            era,whip,k9 = extractStatistics(pitching_data,['era','whip','k9'],selected_team)
        except:
            era,whip,k9 = ['N/A','N/A','N/A']


        pitcher['earned_run_average'] = era
        pitcher['whip'] = whip
        pitcher['k9'] = k9

    roster['players'] = array_of_players
    return json.dumps(roster)


print getRoster(2011,113)
