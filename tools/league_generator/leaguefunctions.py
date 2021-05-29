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
                self.play_game(match[0],match[1])

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