from random import randint

def new_league(names):
    return League(names)


class League(object):
    def __init__(self,name_list):
        self.name = 'Example Baseball League'
        self.teams = self.generate_teams(name_list)


    def generate_teams(self,names):
        team_list = list()

        for name in names:
            team_list.append(Team(name))

        return team_list


    def play_round_robin(self):
        n = len(self.teams) - 1

        home = self.teams
        away = self.teams


        for i in range(n):
            away = away[n:] + away[:n]
            round = zip(home,away)

            for match in round:
                match[0].results['HomeGames'] += 1
                match[1].results['AwayGames'] += 1

                gamescore = randint(0,99)


                # Technically this gives the home team a slight (1%)
                # advantage if they're worse than the away team,
                # but I'll chalk that up to home field advantage
                # rather than spend time making a cleaner calculation
                home_team_odds = match[0].team_score - match[1].team_score + 50

                if (gamescore < home_team_odds):
                    winner = match[0]
                    loser = match[1]
                else:
                    winner = match[1]
                    loser = match[0]

                winner.results['W'] += 1
                loser.results['L']  += 1






class Team(object):
    def __init__(self,name):
        self.name = name
        self.results = dict()
        self.team_score = randint(20,80)
        for attribute in ['W','L','HomeGames','AwayGames']:
            self.results[attribute] = 0





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


def simple_round_robin(teams):
    home = teams
    away = teams




def play_games(teams):
    schedule = simple_round_robin(teams)

    for day in schedule:
        for match in day:
            if (randint(0,100) % 2):
                winner = match[0]
                loser = match[1]
            else:
                winner = match[1]
                loser = match[0]

            results[winner]['W'] += 1
            results[loser]['L'] += 1
            results[match[0]]['HomeGames'] += 1
            results[match[1]]['AwayGames'] += 1
