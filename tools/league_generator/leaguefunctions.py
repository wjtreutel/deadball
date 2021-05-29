# TeamGenerator.py
#
# Created: 5/29/21
#
# Library file for high-level team functions


from random import randint,shuffle


# I legitimately can't remember if class creators are private,
# so I hastily made this wrapper function
# and I need to fix this later
def new_league(names):
    return League(names)



class League(object):
    def __init__(self,name_list):
        self.name = 'Example Baseball League'
        self.teams = self.generate_teams(generate_names(6))
        self.former_teams = list()
        self.total_number_of_teams = 0

        # Allows schedule to be referred to abstractly
        # Might be useful in the future
        self.schedule_system = self.simple_round_robin
        self.schedule_rounds = 11

        self.years = dict()







    def generate_teams(self,names):
        team_list = list()
        x = 0

        for name in names:
            team_list.append(Team(self,name))

        return team_list


    def play_game(self,home_team,away_team):
            home_team.results['HomeGames'] += 1
            away_team.results['AwayGames'] += 1

            gamescore = randint(0,99)


            # Technically this gives the home team a slight (1%)
            # advantage if they're worse than the away team,
            # but I'll chalk that up to home field advantage
            # rather than spend time making a cleaner calculation
            home_team_odds = home_team.team_score - away_team.team_score + 50

            if (gamescore < home_team_odds):
                winner = home_team
                loser  = away_team
            else:
                winner = away_team
                loser  = home_team

            winner.results['W'] += 1
            loser.results['L']  += 1


    def simple_round_robin(self):
        n = len(self.teams) - 1

        home = self.teams
        away = self.teams

        for i in range(n):
            away = away[n:] + away[:n]
            round = zip(home,away)

            for match in round:
                self.play_game(match[0],match[1])


    def get_rankings(self):
        return sorted(self.teams, key= lambda x: x.results['W'],reverse = True)


    # IDEA: configure with divisions, each division is 1/3 of screen
    def display_standings(self):
        # Sort teams by win total, display display_standings

        print "    {:20} Standings {}".format(self.name,randint(1885,2020))
        print "    ======================================="

        print "              Name           |  W  |  L  |  %  "
        for team in self.teams:
            win_percentage = float(team.results['W']) / (team.results['W'] + team.results['L'])
            print "-----------------------------------------------"
            print "{:28} | {:>3} | {:>3} | {:.3f}".format(team.name,team.results['W'],team.results['L'],win_percentage)


#
# TEAM OBJECT
#

class Team(object):
    def __init__(self,league,id,name):
        self.league = league
        self.name = name
        self.id = id
        self.results = dict()
        self.team_score = randint(20,80)
        for attribute in ['W','L','HomeGames','AwayGames']:
            self.results[attribute] = 0


    def disband_team(self):
        print "[disband_team] not implemented"


# Function taken from Makis on StackOverflow
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


def generate_names(x):
    cities = [
    'Chicago','Indianapolis','Bloomington','St. Louis',
    'Boston','Seattle','Portland','Nashville']

    names = ['Robins','Larks','Warblers','Cardinals','Wrens',
             'Athletics','Baseball Club','All-Stars','Millionaires',
             'Seadogs','Men-of-War','Corsairs','Pirates',
             'Hounds','Bulldogs','Kingfishers','Harriers']

    shuffle(names)

    results = []

    for i in range(x):
        curr = "{} {}".format(cities[randint(0,len(cities)-1)],
                              names.pop())
        results.append(curr)

    return results
