import requests

# Pulls MLB Org IDs from endpoint
# (Just a quick utility program)

requestRoot = "http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order='name_asc'&"

orgIDs = {}


print "Enter filename you would like to save IDs to"
selectedFile = raw_input('> ')

print "Are you sure you want to write to " + selectedFile + "? Type 'CONFIRM' to confirm."
response = raw_input('> ')

if response not in ['CONFIRM']:
    selectedFile = ''
    exit()



# Pulls list of teams from MLB website and extracts org IDs
for x in range(1876,2020):
    print "Retrieving {}...".format(x)
    seasonValue = "season={}".format(x)
    leagueData = requests.get(requestRoot + seasonValue)

    for team in leagueData.json()['team_all_season']['queryResults']['row']:
        try:
            currID = team['mlb_org_id']
            currName = team['name_display_full']
            orgIDs[currID] = currName
        except:
            print "Could not find org ID for {} {}".format(x,team['name_display_full'])

# Outputs to file in dictionary form
file = open(selectedFile,"w")
file.write("orgIDs = {")
for key in sorted(orgIDs.keys()):
    file.write("{} : '{}',\n".format(key,orgIDs[key]))
file.write("}")
file.close()
