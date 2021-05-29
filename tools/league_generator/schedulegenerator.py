from leaguefunctions import *


names = ['A','B','C','D','E','F','G','H']


curr_league = new_league(names)


for i in range(0,11):
    curr_league.play_round_robin()

for x in curr_league.teams:
    print x.name
    print x.results

'''
print "# of Rounds?"
choice = raw_input('> ')
for i in range (0,int(choice)):
    play_games(league)

print results
'''
