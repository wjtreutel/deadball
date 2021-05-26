from random import randint

def create_schedule(list):
    """ Create a schedule for the teams in the list and return it"""
    s = []

    if len(list) % 2 == 1: 
        list = list + ["BYE"]

    for i in range(len(list)-1):
        mid = int(len(list) / 2)
        l1 = list[:mid]
        l2 = list[mid:]
        l2.reverse()    

        # Switch sides after each round
        if(i % 2 == 1):
               s = s + [ zip(l1, l2) ]
        else:
                s = s + [ zip(l2, l1) ]

        list.insert(1, list.pop())

    return s



east_league = ['Athletics','Tigers','Mariners','Giants']
west_league = ['Monarchs','Seagulls','Aggies','Brewers']

schedule = create_schedule(league)

results = dict()

for team in league:
    results[team] = dict()
    results[team]['W'] = 0
    results[team]['L'] = 0

for day in schedule: 
    for match in day:
        print match[0]
        if (randint(0,100) % 1):
            winner = match[0]
            loser = match[1]
        else:
            winner = match[1]
            loser = match[0]

        results[winner]['W'] += 1
        results[loser]['L'] += 1

print results
