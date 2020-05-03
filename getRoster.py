import json,requests


# Input: 
#    -[JSON] player_data: Query results containing statistical data (hitting, pitching, fielding, etc.) 
#    -[List] desired_statistics: Contains names of statistics to be returnead ('obp','avg','babip')
#                                If you wish to use this function, you will need to look up the abbreviations that the MLB uses
#    -[int]  desired_team: MLB Organizational ID (org_id) for specific team you want stats from
def extractStatistics(player_data,desired_statistics,desired_team):
    result = []
    number_of_teams = int(player_data['totalSize'])



    # If a player has not hitting stats, return an array of '-' values
    if (number_of_teams < 1):
        for i in desired_statistics:
            result.append('-')
        return result

    stat_list = player_data['row']

    if (number_of_teams not in [0,1]):
        for i in range(0,number_of_teams):
            if (player_data['row'][i]['team_id'] == str(desired_team)):
                stat_list = stat_list[i]

        

    
    for item in desired_statistics:
        stat = stat_list[item]
        if stat in ['',' ']:
            stat = '0'

        result.append(stat_list[item])

    return result


        

def getRoster(selected_year,selected_team):
    roster = dict()
    roster['org_id'] = selected_team
    roster['year'] = selected_year

    # Root path to endpoint
    mlb_endpoint =  "http://lookup-service-prod.mlb.com/json/"
    team_request = "named.roster_team_alltime.bam?start_season={}&end_season={}&team_id={}".format(selected_year,selected_year,selected_team)

    response = requests.get(mlb_endpoint + team_request)


    # Check to make sure team/year combination is valid
    # TODO: L a m b d a
    if (response.json()['roster_team_alltime']['queryResults']['totalSize'] == "0"):
        return json.dumps({ "error" : "No players available"})



    # Strips out the copyright and metadata and gets straight to the good stuff
    player_list = response.json()['roster_team_alltime']['queryResults']['row']

    array_of_players = []

    for player in player_list:
        if player['primary_position'] in []:
            continue
        batting_request = "named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season={}&player_id={}".format(selected_year,player['player_id'])
        response = requests.get(mlb_endpoint + batting_request)


        number_of_teams = int(response.json()['sport_hitting_tm']['queryResults']['totalSize'])

        player_data = response.json()['sport_hitting_tm']['queryResults']

        try:
            hitting_statistics =  extractStatistics(player_data,['avg','obp','slg','d','hr','so','tpa','sb'],selected_team)
            current_batting_average,current_on_base_percentage,slg = hitting_statistics[0:3]
        except Exception, e:
            print "ERROR: " + str(e)
            current_on_base_percentage,slg,current_batting_average = ['N/A','N/A','N/A']
            hitting_traits = ''
        hitting_statistics =  extractStatistics(player_data,['avg','obp','slg','d','hr','so','tpa','sb'],selected_team)

        # Pitchers don't get hitting traits
        if player['primary_position'] not in ['P']:
            hitting_traits = getHittingTraits(hitting_statistics)
        else:
            hitting_traits = []


        current_player = dict()
        try:
            current_first_name,current_last_name = player['name_first_last'].split()
        except Exception, e:
            print "ERROR: " + str(e)
            current_first_name = player['name_first_last'].split()[0]
            current_last_name = player['name_first_last'].split()[1:]

        current_player['first_name'] = current_first_name
        current_player['last_name'] = current_last_name
        current_player['batting_average'] = current_batting_average
        current_player['on_base_percentage'] = current_on_base_percentage
        current_player['handedness'] = player['bats']
        current_player['id'] = player['player_id'] 
        current_player['jersey'] = player['jersey_number']
        current_player['position'] = player['primary_position']
        current_player['traits'] = hitting_traits
        array_of_players.append(current_player)

        
    for pitcher in array_of_players:
        if pitcher['position'] not in ['P']:
            continue
        pitching_request = "named.sport_pitching_tm.bam?league_list_id='mlb'&game_type='R'&season={}&player_id={}".format(selected_year,pitcher['id'])
        response = requests.get(mlb_endpoint + pitching_request)

        number_of_teams = int(response.json()['sport_pitching_tm']['queryResults']['totalSize'])

        try:
            pitching_data = response.json()['sport_pitching_tm']['queryResults']
            pitching_stats = extractStatistics(pitching_data,['era','k9','gidp','bb9','ip'],selected_team)
            era = pitching_stats[0]
            pitching_traits = getPitchingTraits(pitching_stats)

        except Exception, e:
            print "ERROR: " + str(e)
            era = 'N/A'
            pitching_traits = ''

        pitcher['traits'] = pitching_traits
        pitcher['earned_run_average'] = era

    roster['players'] = array_of_players
    return json.dumps(roster)


# Sets traits according to Deadball rulebook(p. 38 "Bonus Traits Guidelines")
def getHittingTraits(hitting_stats):
    result = []


    # Skip players with insufficient data
    if '.---' in hitting_stats:
        return result
    
    batting_average,on_base_percentage,slugging,doubles,home_runs,strikeouts,plate_appearances,steals = [float(x) for x in hitting_stats]

    # Derived Statistics
    k_percentage = strikeouts / plate_appearances
    isolated_power = float(slugging) - float(batting_average)


    # Power Stats - P+ (20HR || 450 SLG) / P++ (35 HR, 540 SLG)
    #               P- (10HRs or fewer)  / P-- (5 HRs or fewer)  
    if ((home_runs >= 35) or (slugging > .540) or (isolated_power >= .250)):
        result.append('P++')
    elif ((home_runs >= 20) or (slugging > .450) or (isolated_power >= .170)):
        result.append('P+')
    elif ((home_runs <= 5) or (isolated_power <= .120)):
        result.append('P-')
    elif ((home_runs <= 10) or (isolated_power < .090)):
        result.append('P--')


    # Contact - C+ (35 doubles || K% <= 10)
    #           C- (K% >= 25)
    if ((doubles > 35) or (k_percentage <= .100)):
        result.append('C+')
    elif (k_percentage >= .250):
        result.append('C-')


    # Speed - S+ (20 steals) / S- ( 0 steals)
    if (steals >= 20):
        result.append('S+')
    if (steals == 0):
        result.append('S-')

    return result

# Sets pitcher bonus traits according to Deadball rulebook (p. 39)
def getPitchingTraits(pitching_stats):
    result = []

    # The MLB Endpoint does not provide GIDP before 1998
    # This is a messy workaround
    # TODO: Fix
    if len(pitching_stats[2]) == 0:
            pitching_stats[2] = '0'



    earned_run_average,strikeouts_per_nine,ground_into_double_play,walks_per_nine,innings_pitched = [float(x) for x in pitching_stats]


    # Strikeout Artist - 9+ strikeouts per nine innings 
    if (strikeouts_per_nine >= 9):
        result.append('K+')
    
    # Groundball Machine - 5+ GIDP
    # The MLB data source does not include GB% or the stats necessary to 
    # calculate it (groundballs / balls in play), so I set the GB+ 
    # threshold as being in the top 30% of pitchers for GIDP in 2017
    if (ground_into_double_play > 5):
        result.append('GB+')

    # Control (BB/9 less than or equal to 2)
    if (walks_per_nine <= 2): 
        result.append('CN+')

    # Stamina (200+ IP)
    if (innings_pitched > 200):
        result.append('ST+')

    return result
