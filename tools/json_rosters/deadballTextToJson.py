# Python program to convert text 
# file to JSON 
 
## HOW TO USE ##
# Call with "deadballTextToJson.py <inputfile> <outputfile>"

import json, sys 
  
filename = sys.argv[1]
  
  
# dictionary where the lines from 
# text will be stored 
dict1 = {} 
  
with open(filename) as fp:    
    dict1['abbreviation'] = fp.readline().strip()
    dict1['team_name'] = fp.readline().strip()
    dict1['year'] = fp.readline().strip()
    
    
    dict1['players'] = []
    
    line = fp.readline()
    
    while line:
        new_player = {} 
        
       
        new_player['first_name'] = fp.readline().strip()
        new_player['last_name'] = fp.readline().strip()
        new_player['full_name'] = "{} {}".format(new_player['first_name'],new_player['last_name'])
        line = fp.readline()
        
        print(new_player['full_name'])
        player_values = line.strip().split()
        
        if len(player_values) == 4:
            position,handedness,batting_target,walk_target = player_values
            pitch_die = 'N/A'
        else:
            position,pitch_die,handedness,batting_target,walk_target = player_values
            
        new_player['jersey'] = "0"
        new_player['position'] = position
        new_player['handedness'] = handedness
        new_player['batting_target'] = batting_target
        new_player['walk_target'] = walk_target
        new_player['pitch_die'] = pitch_die
        
        line = fp.readline()
        
        
        if line.strip() not in ['-','---']:
            new_player['traits'] = line.strip()
            line = fp.readline()
        else:
            new_player['traits'] = ""
            
        dict1['players'].append(new_player)

    dict1['player_count'] = len(dict1['players'])

# creating json file 
# the JSON file is named as test1 
out_file = open(sys.argv[2], "w") 
json.dump(dict1, out_file, indent = 4, sort_keys = False) 
out_file.close() 
