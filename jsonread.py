import json

myfile = open('redsroster.json','r')

teamData = myfile.read()

jsonData = json.loads(teamData)

print jsonData['year']
for player in jsonData['players']:
    print " #{:2} | {}".format(player['jersey'],player['last_name'])
