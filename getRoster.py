import requests
import json

# This will be selected via dropdown
selectedTeam = 133

#print "Select Year (2005-2019)"
#selectedYear = raw_input('> ')
selectedYear = 2010


# Root path of MLB JSON Endpoint
mlbEndpoint =  "http://lookup-service-prod.mlb.com/json/"

# Path for team request (the Oakland As, in this case)
teamRequest = "named.roster_team_alltime.bam?start_season={}&end_season={}&team_id={}".format(selectedYear,selectedYear,selectedTeam)

url = mlbEndpoint + teamRequest

response = requests.get(url)

# Strips out the copyright and metadata and gets straight to the good stuff
roster = response.json()['roster_team_alltime']['queryResults']['row']




for player in roster:
    print player['name_first_last']
    
    playerStats = "named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season={}&player_id={}".format(selectedYear,player['player_id'])
    playerData = requests.get(mlbEndpoint + playerStats)

    currPlayer = {}
    currPlayer['name'] = player['name_first_last']
    
    '''

    if (playerData.json()['sport_hitting_tm']['queryResults']['totalSize'] in ['0']):
        print "Could not find major league data for {} ({})".format(player['name_first_last'],player[player_id])
    else:
        try:
            print currPlayer['name']
            currPlayer['battingAverage'] = playerData.json()['sport_hitting_tm']['queryResults']['row']['avg']
            currPlayer['onBase'] = playerData.json()['sport_hitting_tm']['queryResults']['row']['obp']
            print "{} | {} / {}".format(currPlayer['name'],currPlayer['battingAverage'],currPlayer['onBase'])
        except: 
            print "Error when retrieving data for {}".format(player['name_first_last'])
           ''' 
