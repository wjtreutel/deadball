from random import randint,shuffle
from baseballteam import *

class League(object):
    def __init__(self,league_name,name_list):
        self.name = league_name
        self.total_number_of_teams = 0
        self.teams = list()
        self.current_teams = list()
        self.former_teams = list()
        self.divisions = list()



        for name in name_list:
            self.add_team(name)


        # Allows schedule to be referred to abstractly
        # Might be useful in the future
        self.schedule_system = self.simple_round_robin
        self.schedule_rounds = 11

        self.history = dict()



    def get_current_teams(self):
        return [x for x in self.teams if x.id in self.current_teams]

    def get_rankings(self):
        return sorted(self.teams, key= lambda x: x.results['W'],reverse = True)



    # Team Management
    def add_team(self,name):
        newTeam = Team(self,self.total_number_of_teams,name)
        self.current_teams.append(self.total_number_of_teams)
        self.total_number_of_teams += 1
        self.teams.append(newTeam)
        return


    def retire_team(self,id):
        self.current_teams.remove(id)
        self.former_teams.append(id)
        return





    # This is the meat of the simulation function
    def simulate_year(self,year):
        curr_year = dict()

        # List of Teams
        curr_year['teams'] = dict()
        for team in self.get_current_teams():
            curr_team = dict()
            curr_team['name'] = team.name
            curr_team['id'] = team.id
            curr_team['W'] = 0
            curr_team['L'] = 0
            team.results['W'] = 0
            team.results['L'] = 0
            curr_year['teams'][team.id] = curr_team


        for i in range(0,self.schedule_rounds):
            self.schedule_system()

        for team in self.get_current_teams():
            curr_year['teams'][team.id]['W'] = team.results['W']
            curr_year['teams'][team.id]['L'] = team.results['L']

        self.history[year] = curr_year



    # Simulate a single game
    # TODO: Switch this out to generate more detailed statistics
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


    # SCHEDULING SYSTEMS
    def simple_round_robin(self):
        n = len(self.current_teams) - 1

        home = self.get_current_teams()
        away = self.get_current_teams()

        for i in range(n):
            away = away[n:] + away[:n]
            round = list(zip(home,away))

            for match in round:
                self.play_game(match[0],match[1])







    # IDEA: configure with divisions, each division is 1/3 of screen
    def display_standings(self,year=""):
        # Sort teams by win total, display display_standings

        team_list = self.get_current_teams()

        print(("    {:20} Standings {}".format(self.name,year)))
        print("    =======================================")

        print("              Name           |  W  |  L  |  %  ")
        for team in team_list:
            try:
                win_percentage = float(team.results['W']) / (team.results['W'] + team.results['L'])

            except Exception as e:
                win_percentage = .000

            print("-----------------------------------------------")
            print(("{:28} | {:>3} | {:>3} | {:.3f}".format(team.name,team.results['W'],team.results['L'],win_percentage)))


    def display_historic_standings(self,year):

        team_list = self.history[year]

        print(("    {:20} Standings {}".format(self.name,year)))
        print("    =======================================")

        print("              Name           |  W  |  L  |  %  ")
        for team in [team_list['teams'][x] for x in team_list['teams']]:

            try:
                win_percentage = float(team['W']) / (team['W'] + team['L'])

            except Exception as e:
                win_percentage = .000

            print("-----------------------------------------------")
            print(("{:28} | {:>3} | {:>3} | {:.3f}".format(team['name'],team['W'],team['L'],win_percentage)))
