from deadballRosterGenerator import getRoster
from support import *
from time import sleep

logFile = open('testResults.txt','a')

print "Run all tests?"
response = raw_input('> ')

if response in ['y','yes']:
    for team in mlb_teams:
        for year in range(1900,2019):
            try:
                print "===== {} {} =====".format(year,org_ids[team])
                logFile.write("===== {} {} =====".format(year,org_ids[team]))
                blah = {}
                blah = getRoster(year,team)
                if 'players' in blah:
                    print "Success!"
                    logFile.write("Success!")
                else:
                    logFile.write("Failure?")
                    print "Failure?"

            except Exception, e:
                print "ERROR: " + str(e)
                logFile.write("ERROR: "+ str(e))
                sleep(10)


else:
    print "Enter year (1900 - 2019)"
    selected_year = raw_input('> ')
    print "Enter team by ID ('?' to show IDs)"
    selected_team = raw_input('> ')

    while selected_team == '?':
        for team in mlb_teams:
            print "{} : {}".format(team,org_ids[team])

        print "Enter team by ID ('?' to show IDs)"
        selected_team = raw_input('> ')

    print getRoster(selected_year,selected_team)

logFile.close()
