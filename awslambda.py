import json
from botocore.vendored import requests

def lambda_handler(event, context):
    # TODO implement
    
    info = getRoster(event['selected_year'],event['selected_team'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(info)
    }
    

# TODO: Find a better way of doing this
org_ids = {
108 : 'Los Angeles Angels',
109 : 'Arizona Diamondbacks',
110 : 'Baltimore Orioles',
111 : 'Boston Red Sox',
112 : 'Chicago Cubs',
113 : 'Cincinnati Reds',
114 : 'Cleveland Indians',
115 : 'Colorado Rockies',
116 : 'Detroit Tigers',
117 : 'Houston Astros',
118 : 'Kansas City Royals',
119 : 'Los Angeles Dodgers',
120 : 'Washington Nationals',
121 : 'New York Mets',
123 : 'Hartford Dark Blues',
124 : 'Indianapolis Blues',
125 : 'Indianapolis Blues',
126 : 'Indianapolis Hoosiers',
127 : 'Kansas City Blues',
128 : 'Kansas City Packers',
129 : 'Kansas City Cowboys',
130 : 'Kansas City Unions',
132 : 'Louisville Grays',
133 : 'Oakland Athletics',
134 : 'Pittsburgh Pirates',
135 : 'San Diego Padres',
136 : 'Seattle Mariners',
137 : 'San Francisco Giants',
138 : 'St. Louis Cardinals',
139 : 'Tampa Bay Rays',
140 : 'Texas Rangers',
141 : 'Toronto Blue Jays',
142 : 'Minnesota Twins',
143 : 'Philadelphia Phillies',
144 : 'Atlanta Braves',
145 : 'Chicago White Sox',
146 : 'Miami Marlins',
147 : 'New York Yankees',
148 : 'Louisville Colonels',
150 : 'Milwaukee Cream Citys',
151 : 'Milwaukee Brewers',
152 : 'Milwaukee Unions',
153 : 'Newark Peppers',
155 : 'New York Mutuals',
156 : 'New York Metropolitans',
157 : 'New York Giants',
158 : 'Milwaukee Brewers',
161 : 'Altoona Pride',
163 : 'Baltimore Orioles',
165 : 'Baltimore Terrapins',
166 : 'Baltimore Orioles',
167 : 'Baltimore Monumentals',
168 : 'Boston Reds',
169 : 'Boston Unions',
172 : 'Philadelphia Athletics',
173 : 'Philadelphia Athletics',
174 : 'Philadelphia Quakers',
175 : 'Philadelphia Keystones',
176 : 'Pittsburgh Rebels',
177 : 'Pittsburgh Burghers',
178 : 'St. Louis Cardinals',
180 : 'Rochester Hop Bitters',
181 : 'Richmond Virginias',
184 : 'Brooklyn Gladiators',
185 : 'Brooklyn Feds',
186 : 'Brooklyn Wonders',
187 : 'Buffalo Bisons',
188 : 'Buffalo Bisons',
189 : 'Buffalo Feds',
191 : 'Chicago Whales',
192 : 'Chicago Pirates',
193 : 'Chicago Unions',
195 : 'St. Louis Brown Stockings',
196 : 'St. Louis Maroons',
197 : 'St. Louis Terriers',
198 : 'St. Paul Saints',
199 : 'Syracuse Stars',
200 : 'Syracuse Stars',
201 : 'Toledo Blue Stockings',
202 : 'Toledo Maumees',
204 : 'Cincinnati Reds',
205 : "Cincinnati Kelly's Killers",
206 : 'Cincinnati Outlaw Reds',
208 : 'Cleveland Spiders',
209 : 'Cleveland Spiders',
210 : 'Columbus Colts',
211 : 'Columbus Colts',
212 : 'Cleveland Infants',
213 : 'Detroit Wolverines',
219 : 'Washington Nationals',
220 : 'Washington Senators',
221 : 'Washington Senators',
222 : 'Washington Nationals',
223 : 'Wilmington Quicksteps',
224 : 'Providence Grays',
297 : 'Worcester Brown Stockings',
298 : 'Baltimore Orioles',
299 : 'Troy Trojans'
}


def extractStatistics(player_data,desired_statistics,desired_team):
    result = []
    number_of_teams = int(player_data['totalSize'])

    if (number_of_teams in [0]):
        for i in desired_statistics:
            result.append('N/A')
    elif (number_of_teams not in [0,1]):
        for team in player_data['row']:
            if team['team_full'] == desired_team:
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
    selected_team_name = org_ids[selected_team]
    roster = dict()
    roster['team_name'] = selected_team_name
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
        
        try:
            current_first_name,current_last_name = player['name_first_last'].split()
        except: 
            current_first_name = player['name_first_last'].split()[0]
            current_last_name  = player['name_first_last'].split()[1:]
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
        
        era,whip,k9 = extractStatistics(pitching_data,['era','whip','k9'],org_ids[selected_team])
        pitcher['earned_run_average'] = era
        pitcher['whip'] = whip
        pitcher['k9'] = k9

    roster['players'] = array_of_players
    return roster