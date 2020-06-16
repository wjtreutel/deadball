from random import randint,shuffle
import names
import jsonpickle
import os
from sys import argv

# Just a simple team generator for Deadball
# Plug and play

class Player(object):
    def __init__(self,position = 'SDP',rank = 0):
        self.rank = rank
        self.firstName = names.get_first_name()
        self.lastName = names.get_last_name()
        self.fullName = self.firstName + ' ' + self.lastName
        self.position = position
        self.battingAverage = self.rollBattingAverage()
        self.onBasePercentage = self.battingAverage + randint(1,6) + randint(1,6)
        self.handedness = self.rollHandedness()
        self.traits = self.rollTraits()
    

    
    def rollHandedness(self):
        roll = randint(1,10)
        if roll in range(0,7):
            return 'R'
        if roll in range(7,10):
            return 'L'
        if roll is 10:
            return 'S'


    def rollBattingAverage(self):
        return 20.0 # Mendoza Line 

    def rollTraits(self):
        traits = []
        return traits



    def display(self):
        traitList = ' '.join(self.traits) 
        print "{:2d} | {:2} | {:22} | {} | {:6} | BT: {:2.0f} / WT: {:2.0f}".format(self.rank,self.position,self.fullName,self.handedness,traitList,self.battingAverage,self.onBasePercentage)
      

class Hitter(Player):
    def rollBattingAverage(self):
        return (randint(1,10) + randint(1,10) + 15.0)

    def rollTraits(self):
        traits = []
        roll = randint(1,6) + randint(1,6)
        if roll in [2,3]:
            traits.append('S+')
        if roll in [2,4]:
            traits.append('D+')
        if roll == 10:
            traits.append('P+')
        if roll == 11:
            traits.append('C+')
        if roll == 12:
            traits.append('P++')
        return traits




class PinchHitter(Player):
    def rollBattingAverage(self):
        return (randint(1,10) + 15.0)

    def rollTraits(self):
        traits = []
        roll = randint(1,6) + randint(1,6)
        if roll == 2:
            traits.append('S+')
        if roll == 3:
            traits.append('C+')
        if roll == 11:
            traits.append('D+')
        if roll == 12:
            traits.append('P+')
        return traits


class StartingPitcher(Player):
    def __init__(self,position='SDP',rank=0):
        self.pitchDie = self.rollPitcherAbility()
        super(StartingPitcher,self).__init__(position,rank)

    def rollBattingAverage(self):
        return (randint(1,10) + 5.0)

    def rollHandedness(self):
        roll = randint(1,10)
        if roll in range(0,7):
            return 'R'
        return 'L'

    def rollTraits(self):
        traits = []
        roll = randint(1,6) + randint(1,6)
        if roll == 2:
            traits.append('GB+')
        if roll == 3:
            traits.append('K+')
        if roll == 11:
            traits.append('ST+')
        if roll == 12:
            traits.append('CN+')
        return traits

    def rollPitcherAbility(self):
        roll = randint(1,8)
        if roll == 1:
            self.pitchScore = 12
            return 'd12'
        elif roll < 4:
            self.pitchScore = 8
            return 'd8'
        elif roll < 7:
            self.pitchScore = 4
            return 'd4'
        else:
            self.pitchScore = -4
            return '-d4'

    def display(self):
        traitList = ' '.join(self.traits)

        print "{:2d} | {:2} | {:22} | {} | {:6} | BT: {:2.0f} / WT: {:2.0f} | {}".format(self.rank,self.position,self.fullName,self.handedness,traitList,self.battingAverage,self.onBasePercentage,self.pitchDie)


class Team:
    def __init__(self):
        self.jerseyPool = range(0,100)
        self.positionPool = ['C','1B','2B','3B','SS','LF','CF','RF']
        self.city = "Seattle"
        self.name = "Pilots"
        self.stadium = "Sick Stadium"
        self.manager = names.get_full_name()
        self.teamScore = 0

        batterScore = 0
        pitcherScore = 0

        # Fill the Roster
        self.roster = []

        #Shuffle the jersey numbers (simpler way to randomize)
        shuffle(self.jerseyPool)

        for pos in self.positionPool: 
            newPlayer = Hitter(position=pos,rank=self.jerseyPool.pop())
            batterScore = batterScore + newPlayer.battingAverage
            self.roster.append(newPlayer)
       
        # Generate 5 pinch hitters
        for x in range(0,5):
            newPH = PinchHitter("PH",self.jerseyPool.pop())
            batterScore = batterScore + newPH.battingAverage
            self.roster.append(newPH)

        # Generate 5 Starting Pitchers
        for x in range (0,5):
            newPitcher = StartingPitcher("SP",self.jerseyPool.pop())
            pitcherScore = pitcherScore + newPitcher.pitchScore
            self.roster.append(newPitcher)

        # Generate 7 relievers
        for x in range (0,7):
            newReliever = StartingPitcher("RP",self.jerseyPool.pop())
            pitcherScore = pitcherScore + newReliever.pitchScore
            self.roster.append(newReliever)
        
        self.teamScore = (batterScore + (pitcherScore * 7)) / 10

    def displayTeam(self):
       # print "[ {} {} ]".format(self.city,self.name)
       # print "Managed by {}".format(self.manager)

        
        print "=" * 64
        for player in self.roster[0:8]:
            player.display()

        print "=" * 64
        for player in self.roster[8:13]:
            player.display()

        print "=" * 64
        for player in self.roster[13:18]:
            player.display()

        print "=" * 64
        for player in self.roster[18:]:
            player.display()
        print "=" *  64 

        print "TEAM SCORE: {}".format(int(round(self.teamScore)))

    def generateBattingOrder(self):
        battingOrder = self.roster[0:8]
        battingOrder.append(self.roster[11])
        shuffle(battingOrder)
        for player in battingOrder:
            player.display()


# Process command line arguments
minimumScore = 0
maximumScore = 999

if len(argv) > 3:
    print argv
    print "ERROR: Too many arguments"
    print "(Usage: python teamgenerator.py <optional minimum score, or 0 if using max score> <optional maximum score>)"
    exit()
if len(argv) == 3:
    try:
        maximumScore = int(argv[2])
    except:
        print "ERROR: Cannot convert '{}' to integer".format(argv[2])
        exit()
if len(argv) >= 2:
    try:
        minimumScore = int(argv[1])
    except:
        print "ERROR: Cannot convert '{}' to integer".format(argv[1])
        exit()



newTeam = Team()
while (newTeam.teamScore < minimumScore) or (newTeam.teamScore > maximumScore):
    newTeam = Team()
newTeam.displayTeam()

teamData = jsonpickle.encode(newTeam)


print "Would you like to save this team?"
reply = raw_input('> ')
if (reply in ['Y','y','yes','YES','Yes']):
    print "Enter filename (.txt) you would like to save to:"
    reply = raw_input('> ')
    # Save
    outfile = "{}.roster".format(reply)
    print outfile
    while os.path.exists(outfile):
        print "ERROR: '{}' already exists".format(outfile)
        print "Please enter a different filename"
        reply = raw_input('> ')
        outfile = "{}.roster".format(reply)
    savefile = open(outfile,'w')
    savefile.write(teamData)
    savefile.close()
    print "<<Output to file>>"

else:
    print "Exiting . . ."
