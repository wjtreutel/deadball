from lambda_retrieveMLBRoster import getRoster
import json
from support import *

'''
org_id, year,
players:
    id,jersey
    first_name,last_name
    handedness,position
    batting_average,on_base_percentage,earned_run_average
    traits
'''

def displayPlayer(player):
    full_name = player['first_name'] + ' ' + player['last_name'] 
    batting_target = int(player['batting_target'])
    walk_target = int(player['walk_target'])
    pitch_die = ""

    if player.get('pitch_die') != None:
        pitch_die = player['pitch_die']


    print "#{:2} | {:2} | {:24} | Bats: {} | BT: {:2} | WT: {:2} | {:4} | {}".format(player['jersey'],player['position'],full_name,player['handedness'],batting_target,walk_target,pitch_die,player['traits'])




print "Select Year (1900 - 2019)"
year = raw_input('year> ')

while int(year) not in range (1900,2020):
    print "Invalid response. Please select a year between 1900 and 2019."
    year = raw_input('year> ')


print "Select Team (enter ? for list of team codes)"
team = raw_input('team> ')

while (team == '?') or (int(team) not in mlb_teams):
    if team == '?':
        for code in mlb_teams:
            print "{}) {}".format(code,org_ids[code])
        team = raw_input('team> ')

    else:
        print "Invalid response. Please input a valid team code (press ? for a list of team codes)"
        team = raw_input('team> ')



roster = json.loads(getRoster(year,team))

if roster['player_count'] == 0:
    print "ERROR: No data found for that year/team combination. (Are you sure it existed at the time?)"
    print "Exiting . . . "
    exit()

#inFile = open('test1985.roster','r')
#roster = json.loads(inFile.read())

players = roster['players']

positions = ['1B','2B','3B','SS','LF','CF','RF','C','IF','OF','DH','UT']



sorted_roster = []
pitchers = []

for position in positions:
    sub_list = []
    for player in players:
        if player['position'] == position:
            sorted_roster.append(player)

pitchers = [x for x in players if x['position'] in ['SP','RP','P']]


print "SORTED: {} / PITCHERS: {}".format(len(sorted_roster),len(pitchers))

for player in sorted_roster:
    displayPlayer(player)

for player in pitchers:
    displayPlayer(player)
