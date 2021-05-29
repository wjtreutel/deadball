from random import randint

#
# TEAM OBJECT
#

class Team(object):
    def __init__(self,league,id,name):
        self.league = league
        self.city = ""
        self.name = name
        self.id = id
        self.results = dict()
        self.team_score = randint(20,80)
        for attribute in ['W','L','HomeGames','AwayGames']:
            self.results[attribute] = 0


    def get_record(self):
        return self.results


def generate_names(x):
    cities = [
    'Chicago','Indianapolis','Bloomington','St. Louis',
    'Boston','Seattle','Portland','Nashville']

    names = ['Robins','Larks','Warblers','Cardinals','Wrens',
             'Athletics','Baseball Club','All-Stars','Millionaires',
             'Seadogs','Men-of-War','Corsairs','Pirates',
             'Hounds','Bulldogs','Kingfishers','Harriers']


    results = []

    for i in range(x):
        curr = "{} {}".format(cities[randint(0,len(cities)-1)],
                              names[randint(0,len(names)-1)])
        results.append(curr)

    if x == 1:
        return results[0]

    return results
